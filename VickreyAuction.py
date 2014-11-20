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
		return possiblePrices[int(max(possiblePrices))]

	def runOptimalAuction(self):
		possiblePrices = []
		for i in xrange(len(self.bidders)):
			randomSample = self.bidders[i].distribution.rvs()
			if ( randomSample >= self.bidders[i].optimalReserve):
				possiblePrices.append(randomSample)
			else:
				#in order to keep indices of bidders
				possiblePrices.append(-1)
		winningBid = max(possiblePrices)
		#nobody bid above the reserve
		print possiblePrices
		if (winningBid == -1):
			return 0
		#there was a bid above the reserve
		else:
			indicesOfMaxBidAboveReserve = [i for i, j in enumerate(possiblePrices) if j == winningBid]
			possiblePrices.remove(winningBid)
			return max(self.bidders[indicesOfMaxBidAboveReserve[0]].optimalReserve, max (possiblePrices))

class Bidder:

	def __init__(self, distribution):
		self.distribution = distribution
		#self.value = np.mean(distribution)
		#need to figure out how to compute min and max
		self.optimalReserve = self.getOptimalReserves(0, 100, distribution)

	def getOptimalReserves(self, minimum, maximum, distribution):
		distributionRange = range(minimum, maximum)
		possibleReserves = [x / 100. for x in distributionRange]
		singleBidderRevenue = []
		for r in possibleReserves:
			if (distribution.cdf(r) > 0):
				singleBidderRevenue.append(r * (1 - distribution.cdf(r)))
			else:
				singleBidderRevenue.append(-1)
		maxSingleBidderRevenue = max(singleBidderRevenue)
		indicesOfMaxSingleBidderRevenue = [i for i, j in enumerate(singleBidderRevenue) if j == maxSingleBidderRevenue]
		optimalReserves = []
		if (len(indicesOfMaxSingleBidderRevenue) == 1):
			return possibleReserves[indicesOfMaxSingleBidderRevenue[0]]
		#need to figure out what to do in case of multiple optimal single bidder reserves
		else:
			print "error"
