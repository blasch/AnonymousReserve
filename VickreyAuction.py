import numpy as np
import random

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
			bid = self.bidders[i].getValue()
			if(bid > self.anonymousReserve):
				possiblePrices.append(bid)
		#Price = second highest
		print "possible" + str(possiblePrices)
		possiblePrices.remove(max(possiblePrices))
		#print possiblePrices
		if(len(possiblePrices) == 0):
			return 0
		return possiblePrices[int(max(possiblePrices))]
			
class Bidder:

	def __init__(self, distribution):
		self.distribution = distribution
		self.lastValue = 0

	def getValue(self):
		bid = random.choice(self.distribution)
		self.lastValue = bid
		return bid
		