#!/usr/bin/env python

import re,csv,sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib as mpl
import scipy.stats as stats

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

    fig = plt.figure(figsize=(10,4))

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
        

def plot_data_summary(data,keys,subtitles,plotTitle,nRows=2,nCols=4):
    fig1 = plt.figure(figsize=(9,4.5))

    ## error checking
    if len(subtitles) != len(keys):
        print "ERROR: labels and keys must be of equal size in plot_summary_data"
        return

    for i,key in enumerate(keys):
        ax = fig1.add_subplot(nRows,nCols,i+1)
        ax.hist(data[key])
        ax.locator_params(nbins=3)
        ax.set_title("%s = %s"%(subtitles[i],keys[i]))
    
    plt.suptitle(re.sub("\.png","",plotTitle))
    plt.tight_layout()
    plt.savefig(plotTitle)

def plot_predicted_cv_simple(ax,x,t,t_predict,title,loc='upper left',showLeg=True):

    def add_text1(ax,txt,xPos,yPos,ha='left',va='top'):
        fColor = 'black'
        tColor = 'white'

        ax.text(xPos,yPos,txt,color=tColor,fontsize=5,
                ha=ha, va=va,
                bbox = dict(boxstyle="round",facecolor=fColor,alpha=0.8)
                )

    def add_text2(ax,txt,xPos,yPos,ha='left',va='top'):
        fColor = 'white'
        tColor = 'black'

        ax.text(xPos,yPos,txt,color=tColor,fontsize=5,
                ha=ha, va=va,
                bbox = dict(boxstyle="round",facecolor=fColor,alpha=0.8)
                )

    ## log everything for plotting
    #t = np.log(t)
    #t_predict = np.log(t_predict)

    colors = ['#FF3300','g','r','cyan','magenta']
    ax.clear()
    rankedInds = np.argsort(t)
    p1 = ax.plot(x,t[rankedInds],marker='.',color="#FF5500",markersize=2)
    p2 = ax.plot(x,t_predict[rankedInds],color='k',marker='.',linestyle='None',markersize=2)
     
    ## show limits
    upper = t + t.std() * 0.5
    lower = t - t.std() * 0.5
    p3 = ax.plot(x,upper[rankedInds],'b')
    p4 = ax.plot(x,lower[rankedInds],'b')

    upperOutliers = np.where(t_predict > upper)[0].size
    lowerOutliers = np.where(t_predict < lower)[0].size
    toPrint = 100.0 - (float(upperOutliers+lowerOutliers) / float(x.size) * 100.0)
    add_text1(ax,"%s"%(round(toPrint,1)),0.5,1.9)

    #slope, intercept, r_value, p_value, std_err = stats.linregress(t,t_predict)
    #r2 = r_value**2
    #add_text2(ax,"%s"%(round(r2,2)),0.5,2.7)

    #ax.set_xlabel('ranked')
    #ax.set_ylabel('CV')
    ax.set_title(title,fontsize=6)
    ax.set_ylim([-1.0,2.0])
    ax.locator_params(nbins=2)
    ax.set_xlim([x.min()-1,x.max()+1])
    if showLeg == True:
        leg = ax.legend([p1[0],p2[0]],['Observed','Predicted'],loc=loc)
        ltext = leg.get_texts()
        for i in range(len(ltext)):
            plt.setp(ltext[i],fontsize=8)
    ax.set_aspect(1./ax.get_data_ratio())

def draw_graph(edgeWeights,plotName='toy_graph.png'):
    import matplotlib.pyplot as plt
    plt.figure(1)
    import networkx as nx


    edgeDict = {"w4a":("X1","X4"),"w5a":("X1","X5"),"w6a":("X1","X6"),"w7a":("X1","X7"),
                "w4b":("X2","X4"),"w5b":("X2","X5"),"w6b":("X2","X6"),"w7b":("X2","X7"),
                "w4c":("X3","X4"),"w5c":("X3","X5"),"w6c":("X3","X6"),"w7c":("X3","X7"),
                "w1":("X1","T"),"w2":("X2","T"),"w3":("X3","T"),"w4":("X4","T"),
                "w5":("X5","T"),"w6":("X6","T"),"w7":("X7","T")}

    ## initialize the graph
    G = nx.Graph()
    for node in ["X1","X2","X3","X4","X5","X6","X7","T"]:
        G.add_node(node)

    for edgeName,edge in edgeDict.iteritems():
        G.add_edge(edge[0],edge[1],weight=edgeWeights[edgeName])

    # explicitly set positions
    pos={"X1":(0.5,2),
         "X2":(3,2),
         "X3":(5.5,2),
         "X4":(1,1),
         "X5":(2.5,1),
         "X6":(3.5,1),
         "X7":(5,1),
         "T":(3,0)}

    ## get insignificant edges
    isEdges = [(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] ==0.0]

    # plot the network
    nodeSize = 2000
    colors = [edge[2]['weight'] for edge in G.edges_iter(data=True)]
    cmap = plt.cm.RdBu
    fig = plt.figure(figsize=(10,5))
    ax  = fig.add_axes([0.3, 0.0, 0.7, 1.0])
    nx.draw(G,pos,node_size=nodeSize,edge_color=colors,width=4,edge_cmap=plt.cm.RdBu,edge_vmin=-0.5,edge_vmax=0.5,ax=ax)
    nx.draw_networkx_nodes(G,pos,node_size=nodeSize,nodelist=["X1","X2","X3","T"],node_color='#FF6600',with_labels=True)
    nx.draw_networkx_nodes(G,pos,node_size=nodeSize,nodelist=["X4","X5","X6","X7"],node_color='#0066FF',with_labels=True)
    nx.draw_networkx_edges(G,pos,edgelist=isEdges,width=1,edge_color='k',style='dashed')

    ## add a colormap
    ax1 = fig.add_axes([0.05, 0.05, 0.5, 0.14])
    norm = mpl.colors.Normalize(vmin=-.5, vmax=.5)
    cb1 = mpl.colorbar.ColorbarBase(ax1,cmap=cmap,
                                    norm=norm,
                                    orientation='horizontal')


    # add an axis for the legend
    ax2 = fig.add_axes([0.05,0.25,0.32,0.65]) # l,b,w,h
    ax2.set_yticks([])
    ax2.set_xticks([])
    ax2.set_frame_on(True)
    fontSize = 12
    ax2.text(0.1,0.89,r"$X1$ = species richness",color='k',fontsize=fontSize,ha="left", va="center")
    ax2.text(0.1,0.78,r"$X2$ = CO$_2$ treatment",color='k',fontsize=fontSize,ha="left", va="center")
    ax2.text(0.1,0.67,r"$X3$ = N treatment",color='k',fontsize=fontSize,ha="left", va="center")
    ax2.text(0.1,0.56,r"$X4$ = synchrony",color='k',fontsize=fontSize,ha="left", va="center")
    ax2.text(0.1,0.45,r"$X5$ = environment variance ($\Sigma^{2}_{e}$)",color='k',fontsize=fontSize,ha="left", va="center")
    ax2.text(0.1,0.34,r"$X6$ = community biomass",color='k',fontsize=fontSize,ha="left", va="center")
    ax2.text(0.1,0.23,r"$X7$ = demographic variance ($\Sigma^{2}_{d}$)",color='k',fontsize=fontSize,ha="left", va="center")
    ax2.text(0.1,0.12,r"$T$  = observed CV ($CV^{2}$)",color='k',fontsize=fontSize,ha="left", va="center")
    plt.savefig(plotName)


def draw_graph_prior(edgeWeights,plotName='toy_graph.png'):
    import matplotlib.pyplot as plt
    plt.figure(1)
    import networkx as nx


    edgeDict = {"w4a":("X1","X4"),"w5a":("X1","X5"),"w6a":("X1","X6"),"w7a":("X1","X7"),
                "w1":("X1","T"),"w4":("X4","T"),
                "w5":("X5","T"),"w6":("X6","T"),"w7":("X7","T")}

    ## initialize the graph
    G = nx.Graph()
    for node in ["X1","X4","X5","X6","X7","T"]:
        G.add_node(node)

    for edgeName,edge in edgeDict.iteritems():
        G.add_edge(edge[0],edge[1],weight=edgeWeights[edgeName])

    ## get insignificant edges
    isEdges = [(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] ==0.0]

    # explicitly set positions
    pos={"X1":(3,2),
         "X4":(1,1),
         "X5":(2.5,1),
         "X6":(3.5,1),
         "X7":(5,1),
         "T":(3,0)}

    # plot the network
    nodeSize = 2000
    colors = [edge[2]['weight'] for edge in G.edges_iter(data=True)]
    cmap = plt.cm.RdBu
    fig = plt.figure(figsize=(10,5))
    ax  =fig.add_axes([0.3, 0.0, 0.7, 1.0])
    nx.draw(G,pos,node_size=nodeSize,edge_color=colors,width=4,edge_cmap=plt.cm.RdBu,edge_vmin=-0.5,edge_vmax=0.5,ax=ax)
    nx.draw_networkx_nodes(G,pos,node_size=nodeSize,nodelist=["X1","T"],node_color='#FF6600',with_labels=True)
    nx.draw_networkx_nodes(G,pos,node_size=nodeSize,nodelist=["X4","X5","X6","X7"],node_color='#0066FF',with_labels=True)
    nx.draw_networkx_edges(G,pos,edgelist=isEdges,width=1,edge_color='k',style='dashed')

    ## add a colormap
    ax1 = fig.add_axes([0.05, 0.05, 0.5, 0.14])
    norm = mpl.colors.Normalize(vmin=-.5, vmax=.5)
    cb1 = mpl.colorbar.ColorbarBase(ax1,cmap=cmap,
                                    norm=norm,
                                    orientation='horizontal')


    # add an axis for the legend
    ax2 = fig.add_axes([0.05,0.25,0.32,0.65]) # l,b,w,h
    ax2.set_yticks([])
    ax2.set_xticks([])
    ax2.set_frame_on(True)
    fontSize = 12
    ax2.text(0.1,0.89,r"$X1$ = species richness",color='k',fontsize=fontSize,ha="left", va="center")
    ax2.text(0.1,0.78,r"$X4$ = synchrony",color='k',fontsize=fontSize,ha="left", va="center")
    ax2.text(0.1,0.67,r"$X5$ = environment variance ($\Sigma^{2}_{e}$)",color='k',fontsize=fontSize,ha="left", va="center")
    ax2.text(0.1,0.56,r"$X6$ = community biomass",color='k',fontsize=fontSize,ha="left", va="center")
    ax2.text(0.1,0.45,r"$X7$ = demographic variance ($\Sigma^{2}_{d}$)",color='k',fontsize=fontSize,ha="left", va="center")
    ax2.text(0.1,0.34,r"$T$  = observed CV ($CV^{2}$)",color='k',fontsize=fontSize,ha="left", va="center")
    plt.savefig(plotName)
