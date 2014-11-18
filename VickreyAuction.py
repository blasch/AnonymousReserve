import numpy as np

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
		
	def runAuction(self):
		possiblePrices = [self.anonymousReserve]
		for i in xrange(self.bidders):
			if(self.bidders[i].value > self.anonymousReserve):
				possiblePrices.append(self.bidders[i].value)
		#Price = second highest
		#note: what happens if two people have the same bid
		possiblePrices.remove(max(possiblePrices))
		if(len(possiblePrices) == 0):
			return 0
		return possiblePrices[max(possiblePrices)]

	def runOptimalAuction(self):
		possiblePrices = []
		for i in xrange(self.bidders):
			if (self.bidders[i].value >= self.bidders[i].optimalReserve):
				possiblePrices.append(self.bidders[i].value)
			else:
				#in order to keep indices of bidders
				possiblePrices.append(-1)
			winningBid = max(possiblePrices)
			if (winningBid == -1):
				return 0
			else:
				indicesOfMaxBidAboveReserve = [i for i, j in enumerate(possiblePrices) if j == winningBid]
				#single max bid above bidder specific reserves
				if (len(indicesOfMaxBidAboveReserve) == 1):
					winningBidderIndex = possiblePrices.pop(indicesOfMaxBidAboveReserve[0])
					return max(self.bidders[winningBidderIndex].optimalReserve, max (possiblePrices))
				#multiple bids of same amount above bidder specific reserves
				else:
					return winningBid
		
class Bidder:

	def __init__(self, distribution):
		self.distribution = distribution
		self.value = np.mean(distribution)
		#need to figure out how to compute min and max
		self.optimalReserve = self.getOptimalReserves(0, 100, distribution)

	def getOptimalReserves(min, max, distribution):
		distributionRange = range(min, max)
		possibleReserves = [x / 100 for x in distributionRange]
		singleBidderRevenue = []
		for r in possibleReserves:
			singleBidderRevenue.append(r * (1 - distribution.cdf(r)))
		maxSingleBidderRevenue = max(singleBidderRevenue)
		indicesOfMaxSingleBidderRevenue = [i for i, j in enumerate(singleBidderRevenue) if j == maxSingleBidderRevenue]
		optimalReserves = []
		if (len(indicesOfMaxSingleBidderRevenue) == 1):
			return possibleReserves[indicesOfMaxSingleBidderRevenue[0]]
		#need to figure out what to do in case of multiple optimal single bidder reserves
		else:
			for m in indicesOfMaxSingleBidderRevenue:
				optimalReserves.append(possibleReserves[m])
			return optimalReserves
