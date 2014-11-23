from scipy.stats import uniform
#import matplotlib.pyplot as plt
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
	
#def graphData(graphname, x_reserves, y_revenue):
#	fig = plt.figure()
#	ax = fig.add_subplot(1,1,1)
#	v, = ax.plot(x_reserves, y_revenue, marker='D', color='blue')
#	ax.set_xlabel('Anonymous Reserve Prices')
#	ax.set_ylabel('Expected Revenue')
#	plt.savefig('graphs/' + str(graphname) + '.pdf')
#	print "graph of " + str(graphname) + " saved at graphs/" + str(graphname) + ".pdf"
	
def findMaxReserve(x_reserves, y_revenue):
	max_revenue = max(y_revenue)
	max_indices = [i for i, j in enumerate(y_revenue) if j == max_revenue]
	reserves = []
	for m in max_indices:
		reserves.append(x_reserves[m])
	return (reserves, max_revenue)
	
def runExperiment(auction):
	reserves = range(0,100)
	normReserves = [x / 100. for x in reserves]
	x_reserve = []
	y_revenue = []
	for r in normReserves:
		auction.setAnonymousReserve(r)
		profit = auction.runXAuctions()
		x_reserve.append(r)
		y_revenue.append(profit)
	return (x_reserve, y_revenue)

def getRegularDistributions():
	uni = uniform()
	uni2 = uniform()
	return [uni, uni2]

dis = getRegularDistributions()
numSamples = 10000
bid1 = Bidder(dis[0], numSamples)
bid2 = Bidder(dis[1], numSamples)
auction = VickreyAuction([bid1, bid2], numSamples)
opt = auction.runXOptimalAuctions()
(x,y) = runExperiment(auction)
(mx, my) = findMaxReserve(x,y)
print "optimal revenue: " + str(opt)
print "best anonmymous reserve: " + str(mx)
print "revenue under best anonymous reserve: " + str(my)
print "ratio of opt: " + str(my/opt)

	