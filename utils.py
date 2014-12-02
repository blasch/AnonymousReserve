import scipy.stats 
import matplotlib.pyplot as plt
from VickreyAuction import VickreyAuction, Bidder, OneBidder
from random import randint
import numpy as np

def saveDataToFile(filename, data):
	np.save(filename, data)
	
def concatInputandOutput(x_reserves, y_revenue):
	concat_data = []
	if(len(x_reserves) != len(y_revenue)):
		print "Error: input and output arrays are not aligned!"
		return []
	for i in xrange(x_reserves):
		merged = [x_reserves[i]]
		merged.append(y_revenue[i])
		concat_data.append(merged)
	return concat_data
	
def graphData(graphname, x_reserves, y_revenue):
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	v, = ax.plot(x_reserves, y_revenue, marker='D', color='blue')
	ax.set_xlabel('Anonymous Reserve Prices')
	ax.set_ylabel('Expected Revenue')
	plt.savefig('graphs/' + str(graphname) + '.pdf')
	print "graph of " + str(graphname) + " saved at graphs/" + str(graphname) + ".pdf"
	
def findMaxReserve(x_reserves, y_revenue):
	max_revenue = max(y_revenue)
	max_indices = [i for i, j in enumerate(y_revenue) if j == max_revenue]
	reserves = []
	for m in max_indices:
		reserves.append(x_reserves[m])
	return (reserves, max_revenue)
	
def runExperimentOnAuction(auction, max):
	reserves = range(1, max)
	normReserves = reserves
	x_reserve = []
	y_revenue = []
	opt_revenue = auction.runXOptimalAuctions()
	for r in normReserves:
		if (r % 10 != 0): 
			continue
		auction.setAnonymousReserve(r)
		profit = auction.runXAuctions()
		x_reserve.append(r)
		y_revenue.append(profit)
	return (x_reserve, y_revenue, opt_revenue)

def getEqualRevenueDistribution():
	class rv(scipy.stats.rv_continuous):
		def _pdf(self, x):
			return 1/(x*x)
		def _cdf(self, x):
			return 1-1/x
	return rv(name='equalrevdist', a=1, b=float("inf"))

def getSingleDefDistribution():
	pk = (1)
	xk = np.arange(1)
	return scipy.stats.rv_discrete(name='single', values=(xk, pk))

def getRegularDistributions():
	uni = scipy.stats.uniform(.5, 1)
	norm = scipy.stats.norm()
	gamma = scipy.stats.gamma(3., loc = 0., scale = 2.)
	exp = scipy.stats.expon()
	erd = getEqualRevenueDistribution()
	# include some fat tail distributions (alpha varied)
	return [uni, norm, gamma, exp, erd]

dis = getRegularDistributions()
bid1 = Bidder(dis[4], 1, 12)
bid2 = Bidder(dis[0], 0.5, 1.5)
bid3 = OneBidder()
auction = VickreyAuction([bid1, bid2, bid3])
bid1.optimalReserve = 100
(x,y,o) = runExperimentOnAuction(auction, 100)
(mx, my) = findMaxReserve(x,y)
print "optimal revenue: " + str(o)
print "best anonmymous reserve: " + str(mx)
print "revenue under best anonymous reserve: " + str(my)
print "ratio of opt: " + str(my/o)
graphData("test", x, y)
	