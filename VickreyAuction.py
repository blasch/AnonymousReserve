import numpy as np
from scipy.optimize import brentq 

class VickreyAuction:

	def __init__(self, bidders, numSamples):
		self.bidders = bidders
		self.anonymousReserve = 0
		self.numSamples = numSamples
	
	def setAnonymousReserve(self, r):
		self.anonymousReserve = r
	
	def clearBidders(self):
		self.bidders = []
		
	def addBidder(self, bidder):
		self.bidders.append(bidder)
	
	def removeBidder(self, index):
		self.bidders.remove(index)
	
	# this may be wrong
	def runXAuctions(self):
		singleAuctionRevenues = []
		for j in range(0, self.numSamples):
			possiblePrices = [self.anonymousReserve]
			for i in xrange(len(self.bidders)):
				bid = self.bidders[i].randomSamples[j]
				if(bid >= self.anonymousReserve):
					possiblePrices.append(bid)
			#Price = second highest
			possiblePrices.remove(max(possiblePrices))
			#print possiblePrices
			if (len(possiblePrices) == 0):
				singleAuctionRevenues.append(0)
			else:
				singleAuctionRevenues.append((max(possiblePrices)))
		return sum(singleAuctionRevenues) / float(len(singleAuctionRevenues))

	def runXOptimalAuctions(self):
		singleAuctionRevenues = []
		for j in range(0, self.numSamples):
			possiblePrices = []
			for i in xrange(len(self.bidders)):
				bid = self.bidders[i].randomSamples[j]
				if ( bid >= self.bidders[i].optimalReserve):
					possiblePrices.append(bid)
				else:
					#in order to keep indices of bidders
					possiblePrices.append(-1)
			winningBid = max(possiblePrices)
			#nobody bid above the reserve
			if (winningBid == -1):
				singleAuctionRevenues.append(0)
			#there was a bid above the reserve
			else:
				indicesOfMaxBidAboveReserve = [i for i, k in enumerate(possiblePrices) if k == winningBid]
				possiblePrices.remove(winningBid)
				singleAuctionRevenues.append(max(self.bidders[indicesOfMaxBidAboveReserve[0]].optimalReserve, max (possiblePrices)))
		return sum(singleAuctionRevenues) / float(len(singleAuctionRevenues))

class OneBidder:
	def __init__(self, numSamples):
		self.randomSamples = []
		for i in range(0,numSamples):
			self.randomSamples.append(1)
		#need to figure out how to compute min and max
		self.optimalReserve = 1

	

class Bidder:
	def __init__(self, distribution, numSamples):
		self.distribution = distribution
		self.randomSamples = distribution.rvs(size = numSamples)
		print max(self.randomSamples)
		#need to figure out how to compute min and max
		self.optimalReserve = self.getOptimalReserves(1, int(max(self.randomSamples)), distribution)
		#self.optimalReserve = self.getOptReserve()

	def phi(self, x):
		return x - (1 - self.distribution.cdf(x))/self.distribution.pdf(x) 

	def getOptReserve(self):
		x0 = brentq(self.phi, 1, 100000) 
		print x0
		return x0
		
	def getOptimalReserves(self, minimum, maximum, distribution):
		distributionRange = range(minimum, maximum)
		possibleReserves = distributionRange
		singleBidderRevenue = []
		for r in possibleReserves:
			if (distribution.cdf(r) > 0):
				singleBidderRevenue.append(r * (1 - distribution.cdf(r))) #is this correct?
			else:
				singleBidderRevenue.append(-1)
		maxSingleBidderRevenue = max(singleBidderRevenue)
		indicesOfMaxSingleBidderRevenue = [i for i, j in enumerate(singleBidderRevenue) if j == maxSingleBidderRevenue]
		optimalReserves = []
		if (len(indicesOfMaxSingleBidderRevenue) >= 1):
			#print possibleReserves[indicesOfMaxSingleBidderRevenue[0]]
			return possibleReserves[indicesOfMaxSingleBidderRevenue[0]]
		#need to figure out what to do in case of multiple optimal single bidder reserves
		else:
			print "error: length not right"

		
	