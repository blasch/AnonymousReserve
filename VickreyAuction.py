import numpy as np

class VickreyAuction:

	def __init__(self, bidders):
		self.bidders = bidders
		self.anonymousReserve = 0
	
	def setAnonymousReserve(r):
		self.anonymousReserve = r
	
	def clearBidders():
		self.bidders = []
		
	def addBidder(bidder):
		self.bidders.append(bidder)
	
	def removeBidder(index):
		self.bidders.remove(index)
		
	def runAuction():
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
		