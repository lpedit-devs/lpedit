#!/usr/bin/env python

import re,csv,sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def read_chain_file(chainFile):
    fid = open(chainFile,'rU')
    lineCount = 0
    for linja in fid:
        lineCount +=1
    fid.close()
    results = np.zeros((lineCount,2),)
    fid = open(chainFile,'rU')
    reader = csv.reader(fid,delimiter=" ")
    lineCount = 0
    for linja in reader:
        linja = np.array([float(linja[0]),float(linja[2])])
        results[lineCount,:] = linja
        lineCount +=1
    fid.close()
    return results

def read_chain_index(indexFileName):
    results = {}
    fid = open(indexFileName,'rU')
    for linja in fid:
        linja = re.split(" ",linja)
        results[linja[0]] = (int(linja[1]),int(linja[2]))
    fid.close()
    return results

def make_plots(chainIdx,chain1,chain2,figName='plots.png',fontSize=9,
               verbose=False):

    fig = plt.figure()
    print "showing chain, parameter, mean, std..."

    ## plot chain 1
    figCount = 0
    numKeys = len(chainIdx.keys())
    for key,values in chainIdx.iteritems():
        figCount +=1
        ax = fig.add_subplot(2,numKeys,figCount)
        x = chain1[values[0]-1:values[1],0]
        y = chain1[values[0]-1:values[1],1]
        ax.plot(x,y)
        ax.set_title(key)
        ax.xaxis.set_major_locator(MaxNLocator(2))

        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(fontSize) 
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(fontSize) 

        if verbose == True:
            print 'chain1', key, y.mean(), y.std()

    ## plot chain 2
    for key,values in chainIdx.iteritems():
        figCount +=1
        ax = fig.add_subplot(2,numKeys,figCount)
        x = chain2[values[0]-1:values[1],0]
        y = chain2[values[0]-1:values[1],1]
        ax.plot(x,y)
        ax.set_title(key)
        ax.xaxis.set_major_locator(MaxNLocator(2))

        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(fontSize) 
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(fontSize) 

        if verbose == True:
            print 'chain2', key, y.mean(), y.std()

    #fig.subplots_adjust(wspace=0.4)
    fig.tight_layout()
    fig.savefig(figName,dpi=200)

def get_estimates(chainIdx,chain1,chain2):
    """
    returns the mean and std for each monitored parameter
    """
    
    estimates = {}
    numKeys = len(chainIdx.keys())
    for key,values in chainIdx.iteritems():
        y1 = chain1[values[0]-1:values[1],1]
        y2 = chain2[values[0]-1:values[1],1]
        y = np.hstack((y1,y2))
        estimates[key] = (y.mean(),y.std())
        

    return estimates

def get_posterior_sample(chainIdx,chain1,chain2,parameter,n):
    """
    return's the posterior distribution for a parameter
    """

    if chainIdx.has_key(parameter) == False:
        print 'ERROR: get_posterior - bad parameter specified'
        print '...', chainIdx.keys()
        return

    values = chainIdx[parameter]
    p1 = chain1[values[0]-1:values[1],1]
    p2 = chain2[values[0]-1:values[1],1]
    p = np.hstack((p1,p2))

    randInds = np.arange(p.size)
    np.random.shuffle(randInds)

    if n > p.size:
        print 'ERROR: get_posterior n is out of posterior range'
        print '... max = ', p.size
        return

    randInds = randInds[:n]

    return p[randInds]
        
