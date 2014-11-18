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
		for i in xrange(len(self.bidders)):
			if(self.bidders[i].value > self.anonymousReserve):
				possiblePrices.append(self.bidders[i].value)
		#Price = second highest
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
			#nobody bid above the reserve
			if (winningBid == -1):
				return 0
			#there was a bid above the reserve
			else:
				winningBidderIndex = possiblePrices.remove(winningBid)
				return max(self.bidders[winningBidderIndex].optimalReserve, max (possiblePrices))

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
