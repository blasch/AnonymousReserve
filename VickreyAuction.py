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
		possiblePrices.remove(max(possiblePrices))
		if(len(possiblePrices) == 0):
			return 0
		return possiblePrices[max(possiblePrices)]
		
		
class Bidder:

	def __init__(self, distribution):
		self.distribution = distribution
		self.value = np.mean(distribution)
		