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
	if(int(opt_revenue) == 0):
		return ("skip", "", "")
	for r in reservesToExplore:
		auction.setAnonymousReserve(r)
		profit = auction.runXAuctions()
		x_reserve.append(r)
		y_revenue.append(profit)
		if(int(opt_revenue) != 0 and float(profit)/opt_revenue > 0.66):
			return (x_reserve, y_revenue, opt_revenue)
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

def getUniformDistributions():
	dis = []
	dis.append(scipy.stats.uniform(loc=0, scale=1))
	dis.append(scipy.stats.uniform(loc=1, scale=2))
	dis.append(scipy.stats.uniform(loc=1, scale=4))
	dis.append(scipy.stats.uniform(loc=6, scale=10))
	dis.append(scipy.stats.uniform(loc=2, scale=4))
	dis.append(scipy.stats.uniform(loc=3, scale=7))
	dis.append(scipy.stats.uniform(loc=10, scale=17))
	dis.append(scipy.stats.uniform(loc=10, scale=100))
	return dis

def getNormalDistributions():
	dis = []
	dis.append(scipy.stats.norm(loc=10, scale=3))
	dis.append(scipy.stats.norm(loc=25, scale=8))
	dis.append(scipy.stats.norm(loc=3, scale=1))
	dis.append(scipy.stats.norm(loc=5, scale=1))
	dis.append(scipy.stats.norm(loc=17, scale=5))
	dis.append(scipy.stats.norm(loc=50, scale=10))
	return dis

def getGammaDistributions():
	dis = []
	dis.append(scipy.stats.norm(loc=10, scale=3))
	dis.append(scipy.stats.norm(loc=25, scale=8))
	dis.append(scipy.stats.norm(loc=3, scale=1))
	dis.append(scipy.stats.norm(loc=5, scale=1))
	dis.append(scipy.stats.norm(loc=17, scale=5))
	dis.append(scipy.stats.norm(loc=50, scale=10))
	return dis

def getExponDistributions():
	dis = []
	dis.append(scipy.stats.expon(loc=0, scale=1))
	dis.append(scipy.stats.expon(loc=10, scale=10))
	dis.append(scipy.stats.expon(loc=3, scale=5))
	dis.append(scipy.stats.expon(loc=5, scale=1))
	dis.append(scipy.stats.expon(loc=7, scale=6))
	dis.append(scipy.stats.expon(loc=50, scale=35))
	return dis

def getRegularDistributions():
	dis = []
	dis.extend(getUniformDistributions())
	dis.extend(getNormalDistributions())
	#dis.extend(getGammaDistributions())
	dis.extend(getExponDistributions())
	a2 = getalphatwoDistribution()
	a3 = getalphathreeDistribution()
	a4 = getalphafourDistribution()
	dis.append(a2)
	dis.append(a3)
	dis.append(a4)
	return dis

dis = getRegularDistributions()

#create all bidders
#bid1 = OneBidder()
#erd = getEqualRevenueDistribution()
#bid2 = Bidder(erd, 0, 100)
bidders = []
for i in xrange(len(dis)):
	for j in xrange(len(dis)):
		if(j <= i):
			continue
		print len(bidders)
		bidder = Bidder(dis[i], 0, 100)
		bidder2 = Bidder(dis[j], 0, 100)
		bidders.append([bidder, bidder2, i, j])

#Now pair up and collect data
for i in xrange(len(bidders)):
	pair = bidders[i]
	graphname = str(pair[2]) + "_" + str(pair[3]) + "_" + str(i)
	auction = VickreyAuction([pair[0], pair[1]])
	(x,y,o) = runExperimentOnAuction(auction, 0, 100)
	if(x == "skip"):
		continue
	(mx, my) = findMaxReserve(x,y)
	#print "optimal revenue: " + str(o)
	if(my/o < 0.66):
		print graphname
		print "FOUND"
	#print "best anonymous reserve: " + str(mx)
	#print "revenue under best anonymous reserve: " + str(my)
	#print "ratio of opt: " + str(my/o)
	#ratio = str(my/o)
	graphData(graphname, x, y)
	save_data(graphname, x, y, mx, my, o, ratio)

	