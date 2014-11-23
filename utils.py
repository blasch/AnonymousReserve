import scipy.stats 
import matplotlib.pyplot as plt
from VickreyAuction import VickreyAuction, Bidder

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
	
def runExperimentOnAuction(auction):
	reserves = range(0,100)
	normReserves = [x / 100. for x in reserves]
	x_reserve = []
	y_revenue = []
	opt_revenue = auction.runXOptimalAuctions()
	for r in normReserves:
		auction.setAnonymousReserve(r)
		profit = auction.runXAuctions()
		x_reserve.append(r)
		y_revenue.append(profit)
	return (x_reserve, y_revenue, opt_revenue)

def getRegularDistributions():
	uni = scipy.stats.uniform()
	norm = scipy.stats.norm()
	gamma = scipy.stats.gamma(3., loc = 0., scale = 2.)
	exp = scipy.stats.expon()
	# include some fat tail distributions (alpha varied)
	return [uni, norm, gamma, exp]

dis = getRegularDistributions()
numSamples = 10000
bid1 = Bidder(dis[3], numSamples)
bid2 = Bidder(dis[0], numSamples)
auction = VickreyAuction([bid1, bid2], numSamples)
(x,y,o) = runExperimentOnAuction(auction)
(mx, my) = findMaxReserve(x,y)
print "optimal revenue: " + str(o)
print "best anonmymous reserve: " + str(mx)
print "revenue under best anonymous reserve: " + str(my)
print "ratio of opt: " + str(my/o)

graphData("test", x, y)
	