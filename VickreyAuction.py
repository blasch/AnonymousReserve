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
	
	def runXAuctions(self):
		singleAuctionRevenues = []
		for j in xrange(len(self.bidders)):
			self.bidders[j].resample()
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

class Bidder:

	def __init__(self, distribution, numSamples):
		self.distribution = distribution
		self.randomSamples = distribution.rvs(size = numSamples)
		#need to figure out how to compute min and max
		self.optimalReserve = self.getOptimalReserves(0, 100, distribution)
	
	def resample(self):
		self.randomSamples = self.distribution.rvs(size = len(self.randomSamples))

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

