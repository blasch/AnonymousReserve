import numpy as np
from math import *
from scipy.optimize import brentq, fsolve 

class VickreyAuction:

	def __init__(self, bidders):
		self.bidders = bidders
		self.anonymousReserve = 0
	
	def setAnonymousReserve(self, r):
		self.anonymousReserve = r
	
	def clearBidders(self):
		self.bidders = []
		
	def addBidder(self, bidder):
		self.bidders.append(bidder)
	
	def removeBidder(self, index):
		self.bidders.remove(index)
	
	def sampleBidders(self, numSamples):
		for i in xrange(len(self.bidders)):
			self.bidders[i].sample(numSamples)

	def getNumSamplesForAnonAuction(self):
		return max(1000, 2 * int(pow(ceil(self.anonymousReserve), 2)))


	def getNumSamplesForOptAuction(self):
		maxReserve = 0
		for i in xrange(len(self.bidders)):
			if (self.bidders[i].optimalReserve > maxReserve):
				maxReserve = self.bidders[i].optimalReserve
		return max(1000, 2 * int(pow(ceil(maxReserve), 2)))

	def runXAuctions(self):
		numSamples = self.getNumSamplesForAnonAuction()
		self.sampleBidders(numSamples)
		singleAuctionRevenues = []
		for j in range(0, numSamples):
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
		numSamples = self.getNumSamplesForOptAuction()
		self.sampleBidders(numSamples)
		singleAuctionRevenues = []
		for j in range(0, numSamples):
			possibleWinningBids = []
			for i in xrange(len(self.bidders)):
				bid = self.bidders[i].randomSamples[j]
				if ( bid >= self.bidders[i].optimalReserve):
					possibleWinningBids.append(bid)
				else:
					#in order to keep indices of bidders
					possibleWinningBids.append(-1)
			numBidsAboveReserve = 0
			for i in possibleWinningBids:
				if (i != -1):
					numBidsAboveReserve = numBidsAboveReserve + 1
			#nobody bid above their reserve and revenue is 0
			if (numBidsAboveReserve == 0):
				singleAuctionRevenues.append(0)
			#single bid above their reserve and revenue is the reserve
			elif (numBidsAboveReserve == 1):
				winningBid = max(possibleWinningBids)
				indexOfWinningBidder = [i for i, k in enumerate(possibleWinningBids) if k == winningBid]
				singleAuctionRevenues.append(self.bidders[indexOfWinningBidder[0]].optimalReserve)
			#multiple bids above their reserves
			else:
				bidders = []
				virtualBids = []
				for bidderIndex in range(0, len(possibleWinningBids)):
					if (i != -1):
						bidders.append(bidderIndex)
						virtualBids.append(self.bidders[bidderIndex].phi(possibleWinningBids[bidderIndex]))
				maxVirtualBid = max(virtualBids)
				indicesOfMaxVirtualBid = [i for i, k in enumerate(virtualBids) if k == maxVirtualBid]
				#single highest virtual value
				if (len(indicesOfMaxVirtualBid) == 1):
					winningBidder = indicesOfMaxVirtualBid[0]
					virtualBids.remove(maxVirtualBid)
					secondHighestVirtualBid = max(virtualBids)
					price = fsolve(self.bidders[winningBidder].phi, maxVirtualBid)
					print price
					singleAuctionRevenues.append(price)
				#multiple bids with same virtual value
				else:
					possiblePrices = []
					winningBidderIndex = -1
					winningBid = 0
					for bidderIndex in indicesOfMaxVirtualBid:
						possiblePrices.append(possibleWinningBids[bidderIndex])
						if (possibleWinningBids[bidderIndex] > winningBid):
							winningBid = possibleWinningBids[bidderIndex]
							winningBidderIndex = bidderIndex
					if (self.bidders[winningBidderIndex].isEVD()):
						possiblePrices.remove(winningBid)
						singleAuctionRevenues.append(max(self.bidders[winningBidderIndex].optimalReserve, max(possiblePrices)))
					else:
						singleAuctionRevenues.append(max(possiblePrices))	
		return sum(singleAuctionRevenues) / float(len(singleAuctionRevenues))

	# def findOptimalAuctionInMultipleEVDSetting(self):		
	# 	reservesToAnalyze = []
	# 	reserve = 1
	# 	while (reserve < 1000):
	# 		reservesToAnalyze.append(reserve)
	# 		if (reserve < 2):
	# 			reserve = reserve + 0.1
	# 		elif (reserve < 5):
	# 			reserve = reserve + 1
	# 		else:
	# 			reserve = reserve * 2 
	# 	revenue = []
	# 	auctionDetails = []
	# 	for r1 in reservesToAnalyze:
	# 		self.bidders[0].optimalReserve = r1
	# 		for r2 in reservesToAnalyze:
	# 			self.bidders[1].optimalReserve = r2
	# 			profit = self.runXOptimalAuctions()
	# 			revenue.append(profit)
	# 			auctionDetails.append([r1, r2, profit])
	# 	maxRevenue = max(revenue)
	# 	print auctionDetails
	# 	for auctions in auctionDetails:
	# 		if (auctions[2] == maxRevenue):
	# 			return (auctions[0], auctions[1], auctions[2])

class OneBidder:
	def __init__(self):
		self.randomSamples = None
		self.optimalReserve = 1

	def phi(self, x):
		return 0

	def sample(self, numSamples):
		self.randomSamples = []
		for i in range(0, numSamples):
			self.randomSamples.append(1)

class Bidder:
	def __init__(self, distribution, minimum, maximum):
		self.distribution = distribution
		self.randomSamples = None
		#single reserve for non EVD bidder and array of reserves for EVD bidder
		self.optimalReserve = self.setOptimalReserve(minimum, maximum)

	def isEVD(self):
		if (self.distribution.name == "equalrevdist"):	
			return True
		return False

	def phi(self, x):
		if (self.isEVD()):
			return 0
		return x - (1 - self.distribution.cdf(x))/self.distribution.pdf(x)

	def sample(self, numSamples):
		self.randomSamples = []
		self.randomSamples = self.distribution.rvs(size = numSamples)
	
	def getOptimalReservesToExplore(self, minReserve, maxReserve):
		possibleReserve = minReserve
		reservesToExplore = []
		while (possibleReserve <= maxReserve):
			reservesToExplore.append(possibleReserve)
			if (possibleReserve <= 5):
				possibleReserve = possibleReserve + 0.1
			else:
				possibleReserve = possibleReserve + 1
		return reservesToExplore

	def setOptimalReserve(self, minReserve, maxReserve):	
		reservesToExplore = self.getOptimalReservesToExplore(minReserve, maxReserve)
		if (self.isEVD()): 
			return reservesToExplore
		else:
			postedPriceRevenue = []
			for r in reservesToExplore:
				if (self.distribution.cdf(r) > 0):
					postedPriceRevenue.append(r * (1 - self.distribution.cdf(r)))
				else:
					postedPriceRevenue.append(-1)
			maxPostedPriceRevenue = max(postedPriceRevenue)
			indicesOfMaxPostedPriceRevenue = [i for i, j in enumerate(postedPriceRevenue) if (((j - 0.00001) <= maxPostedPriceRevenue) and ((j + 0.00001) >= maxSingleBidderRevenue))]
			if (len(indicesOfMaxPostedPriceRevenue) == 1):
				return reservesToExplore[indicesOfMaxPostedPriceRevenue[i]]
			else:
				print "error: no optimal reserve"


		
	
