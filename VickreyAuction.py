import numpy as np
from math import *
from scipy.optimize import brentq 

class VickreyAuction:

	def __init__(self, bidders):
		self.bidders = bidders
		self.anonymousReserve = 0
		self.numSamples = None
	
	def setAnonymousReserve(self, r):
		self.anonymousReserve = r
	
	def clearBidders(self):
		self.bidders = []
		
	def addBidder(self, bidder):
		self.bidders.append(bidder)
	
	def removeBidder(self, index):
		self.bidders.remove(index)
	
	def sampleBidders(self):
		for i in xrange(len(self.bidders)):
			self.bidders[i].sample(self.numSamples)

	def setNumSamplesForAnonAuction(self):
		self.numSamples = 2 * int(pow(ceil(self.anonymousReserve), 2))


	def setNumSamplesForOptAuction(self):
		maxReserve = 0
		for i in xrange(len(self.bidders)):
			if (self.bidders[i].optimalReserve > maxReserve):
				maxReserve = self.bidders[i].optimalReserve
		self.numSamples = 2 * int(pow(ceil(maxReserve), 2))

	def runXAuctions(self):
		self.setNumSamplesForAnonAuction()
		self.sampleBidders()
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
		self.setNumSamplesForOptAuction()
		self.sampleBidders()
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
				sys.exit()
				singleAuctionRevenues.append(0)
			#there was a bid above the reserve
			else:
				indicesOfMaxBidAboveReserve = [i for i, k in enumerate(possiblePrices) if k == winningBid]
				possiblePrices.remove(winningBid)
				singleAuctionRevenues.append(max(self.bidders[indicesOfMaxBidAboveReserve[0]].optimalReserve, max (possiblePrices)))
		return sum(singleAuctionRevenues) / float(len(singleAuctionRevenues))

class OneBidder:
	def __init__(self):
		self.randomSamples = None
		self.optimalReserve = 1

	def sample(self, numSamples):
		self.randomSamples = []
		for i in range(0, numSamples):
			self.randomSamples.append(1)

class Bidder:
	def __init__(self, distribution):
		self.distribution = distribution
		self.randomSamples = None
		self.optimalReserve = None
		#self.optimalReserves = self.getOptimalReserves(1, 10, distribution)

	def sample(self, numSamples):
		self.randomSamples = []
		self.randomSamples = self.distribution.rvs(size = numSamples)
		
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
		indicesOfMaxSingleBidderRevenue = [i for i, j in enumerate(singleBidderRevenue) if (((j - 0.01) <= maxSingleBidderRevenue - 0.01) and ((j + 0.01) >= maxSingleBidderRevenue))]
		
		if (len(indicesOfMaxSingleBidderRevenue) >= 1):
			optimalReserves = []
			for i in range(0, len(indicesOfMaxSingleBidderRevenue)):
				optimalReserves.append(possibleReserves[indicesOfMaxSingleBidderRevenue[i]])
			return optimalReserves
		else:
			print "error: no optimal reserve"

		
	
