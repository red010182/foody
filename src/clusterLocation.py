#!/usr/bin/python

from __future__ import with_statement
import cPickle as pickle
from matplotlib import pyplot
from numpy import zeros, array, tile, shape
from scipy.linalg import norm
import numpy.matlib as ml
import numpy as np
import random
import os
from mpl_toolkits.basemap import Basemap

def kmeans(X, k, observer=None, threshold=1e-15, maxiter=20):
    N = len(X)
    labels = zeros(N, dtype=int)
    centers = array(random.sample(X, k))

    iter = 0
 
    def calc_J():
        sum = 0
        for i in xrange(N):
            sum += norm(X[i]-centers[labels[i]])
        return sum
 
    def distmat(X, Y):
        n = len(X)
        m = len(Y)
        xx = ml.sum(X*X, axis=1)
        yy = ml.sum(Y*Y, axis=1)
        xy = ml.dot(X, Y.T)
 
        return tile(xx, (m, 1)).T+tile(yy, (n, 1)) - 2*xy
 
    Jprev = calc_J()
    while True:
        # notify the observer
        # if observer is not None:
            # observer.observe(iter, labels, X,centers)
 
        # calculate distance from x to each center
        # distance_matrix is only available in scipy newer than 0.7
        # dist = distance_matrix(X, centers)
        dist = distmat(X, centers)
        # assign x to nearst center
        labels = dist.argmin(axis=1)
        # re-calculate each center
        for j in range(k):
            idx_j = (labels == j).nonzero()
            centers[j] = X[idx_j].mean(axis=0)
 
        J = calc_J()
        iter += 1
 
        if Jprev-J < threshold:
            break
        Jprev = J
        if iter >= maxiter:
            break
 
    # final notification
    if observer is not None:
        observer.observe(iter, labels, X,centers, showPlot=True)
        # observer(iter, labels, centers,True)
    return labels

class Observer:
    def __init__(self,K,prefix=None):
        self.K = K
        self.colors = zeros((K,3))
        self.prefix = prefix or "iter"  
        for i in range(K):
            self.colors[i] = [random.randint(0,255)/255.0,random.randint(0,255)/255.0,random.randint(0,255)/255.0]

    def observe(self,iter, labels, X,centers,showPlot=False):
        
        print "%s %d." % (self.prefix, iter)

        pyplot.plot(hold=False)  # clear previous plot
        pyplot.hold(True)
        
        m = Basemap(projection='merc',resolution='h',llcrnrlon=120.0, llcrnrlat=21.5,
    urcrnrlon=123.00, urcrnrlat=25.50)
        m.drawmapboundary(fill_color='black') # fill to edge
        m.drawcountries()
        m.fillcontinents(color='white',lake_color='black',zorder=0)
        # draw parallels.
        parallels = np.arange(20.,30,.5)
        m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
        # draw meridians
        meridians = np.arange(119.,125.,.5)
        m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)
        

        # draw points
        data_colors=[self.colors[lbl] for lbl in labels]

        m.scatter(X[:, 0], X[:, 1], c=data_colors, alpha=0.5, latlon=True)
        pyplot.show()
        # pyplot.scatter(X[:, 0], X[:, 1], c=data_colors, alpha=0.5)
        # draw centers
        # pyplot.scatter(centers[:, 0], centers[:, 1], s=200, c=self.colors)
        # padding = 0.5
        # pyplot.axis([max(min(X[:,0]),119.0)-padding,min(max(X[:,0]),123.5)+padding,max(min(X[:,1]),21.0)-padding,min(max(X[:,1]),26.0)+padding])
        # ax = pyplot.gca()
        # ax.set_autoscale_on(False)
        # pyplot.savefig('kmeans/%s_%02d.png' % (self.prefix ,iter), format='png')
        # if showPlot:
        #     pyplot.show()


if __name__ == '__main__':
    K = 21 # number of big cluster (hirarchy 1 cluster)
    D = 20 # define how many points in a small cluster (hirarchy 2 cluster)
    
    # s: id,lng,lat,address
    def parseLocation(s):
    	print s
        a = s.strip().split(',')
        lng = float(a[1])
        lat = float(a[2])
        return [lng,lat]
    X = array([parseLocation(line) for line in open('location.txt','r')])
    print max(X[:,0])
    print max(X[:,1])
    

    try:
        with open('kmeans/labels_hrch1.pickle', 'r') as f:
            labels_hrch1, k = pickle.load(f)  
            if k is not K:
                raise          
    except:
        os.system('rm kmeans/*.png')
        ob = Observer(K)
        labels_hrch1 = kmeans(X, K, observer=ob)
        try:
            with open('kmeans/labels_hrch1.pickle', 'w') as f:
                pickle.dump([labels_hrch1,K], f)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)


    # print labels_hrch1
    for j in range(K):
        idx_j = (labels_hrch1==j).nonzero()[0] # n by 2 matrix, where n is number of points in j-th cluster
        k = int(shape(idx_j)[0]/D) or 1  # k = min(n / D, 1)
        ob = Observer(k,'iter_'+str(j))
        x = X[idx_j]
        # print idx_j
        # print 'k: '+ str(k)

        print 'j: %2d  |  k: %4d  |   N: %4d' % (j,k,len(x))
        if j == 17:
            print x
            kmeans(x,k,ob)
    #         pyplot.plot(hold=False)  # clear previous plot
       #      pyplot.hold(True)
             # colors = zeros((k,3))
             # for i in range(k):
       #          colors[i] = [random.randint(0,255)/255.0,random.randint(0,255)/255.0,random.randint(0,255)/255.0]

       #      # draw points
       #      data_colors=[colors[lbl] for lbl in labels]
       #      pyplot.scatter(x[:, 0], x[:, 1], c=data_colors, alpha=0.5)
       #      # draw centers
       #      pyplot.scatter(centers[:, 0], centers[:, 1], s=200, c=colors)
       #      pyplot.axis([119.0,123.5,21.0,26.0])
       #      ax = pyplot.gca()
       #      ax.set_autoscale_on(False)
       #      pyplot.savefig('kmeans/%s_%02d.png' % (self.prefix ,iter), format='png')
