import scipy.stats 
import matplotlib.pyplot as plt
from VickreyAuction import VickreyAuction, Bidder, OneBidder
from random import randint
import numpy as np
import csv

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

def getAnonymousReservesToExplore(minReserve, maxReserve):
	possibleReserve = minReserve
	reservesToExplore = []
	while (possibleReserve <= maxReserve):
		reservesToExplore.append(possibleReserve)
		if (possibleReserve <= 5):
			possibleReserve = possibleReserve + 0.1
		else:
			possibleReserve = possibleReserve + 1
	return reservesToExplore

def runExperimentOnAuction(auction, min, max):
	reservesToExplore = getAnonymousReservesToExplore(min, max)
	x_reserve = []
	y_revenue = []
	opt_revenue = auction.runXOptimalAuctions()
	for r in reservesToExplore:
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

def getalphatwoDistribution():
	class rv(scipy.stats.rv_continuous):
		def _pdf(self, x):
			return 1/(x*x*x)
		def _cdf(self, x):
			return 1-1/(2*x*x)
	return rv(name='a2dist', a=1, b=float("inf"))


def getalphathreeDistribution():
	class rv(scipy.stats.rv_continuous):
		def _pdf(self, x):
			return 1/(x*x*x*x)
		def _cdf(self, x):
			return 1-1/(3*x*x*x)
	return rv(name='a3dist', a=1, b=float("inf"))


def getalphafourDistribution():
	class rv(scipy.stats.rv_continuous):
		def _pdf(self, x):
			return 1/(x*x*x*x*x)
		def _cdf(self, x):
			return 1-1/(4*x*x*x*x)
	return rv(name='a4dist', a=1, b=float("inf"))

def save_data(name, x, y, mx, my, o, ratio):
	with open(str(name) + '_data.csv', 'w') as fp:
		a = csv.writer(fp, delimiter=',')
		a.writerow(["ratio", ratio])
		a.writerow(["Anonymous"])
		a.writerow([mx, my])
		a.writerow(["optimal", o])
		for i in xrange(len(x)):
			a.writerow([x[i], y[i]])


def getRegularDistributions():
	uni = scipy.stats.uniform()
	norm = scipy.stats.norm()
	gamma = scipy.stats.gamma(3., loc = 0., scale = 2.)
	exp = scipy.stats.expon()
	erd = getEqualRevenueDistribution()
	a2 = getalphatwoDistribution()
	a3 = getalphathreeDistribution()
	a4 = getalphafourDistribution()
	# include some fat tail distributions (alpha varied)
	return [uni, norm, gamma, exp, erd, a2, a3, a4]

dis = getRegularDistributions()

#create all bidders
bid1 = OneBidder()
erd = getEqualRevenueDistribution()
bid2 = Bidder(erd, 0.1, 100)
bidders = [[bid1, bid2]]
for d in dis:
	print len(bidders)
	bidder = Bidder(d, 0.1, 100)
	bidders.append([bidder, bid2])

#Now pair up and collect data
for pair in bidders:
	graphname = str(pair[0].distribution.name) + "_" + str(pair[1].distribution.name)
	auction = VickreyAuction([pair[0], pair[1]])
	(x,y,o) = runExperimentOnAuction(auction, 1, 5)
	(mx, my) = findMaxReserve(x,y)
	print graphname
	print "optimal revenue: " + str(o)
	print "best anonymous reserve: " + str(mx)
	print "revenue under best anonymous reserve: " + str(my)
	print "ratio of opt: " + str(my/o)
	ratio = str(my/o)
	graphData(graphname, x, y)
	save_data(graphname, x, y, mx, my, o, ratio)
	