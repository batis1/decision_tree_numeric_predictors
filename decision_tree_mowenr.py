# -*- coding: utf-8 -*-
"""
Created on Fri May 28 15:36:04 2021

@author: mohammed batis
"""

"""
Created on Mon Apr  6 07:43:52 2020

@author: batis - 18511160002
"""

import matplotlib.pyplot as plt
from numpy import *
def ScattterPlot(dataMat):#,labelVec):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    dict1={}
    m=len(dataMat)
    for i in range(m):
        if not dict1.get(dataMat[i][-1]):
            dict1[dataMat[i][-1]]={"x":[],"y":[]}            
    
    color=["r","g","b","c","m"]
    index=0;
    for i in range(m)    :
        if dict1.get(dataMat[i][-1]):
            dict1.get(dataMat[i][-1]).get("x").append(dataMat[i][0])            
            dict1.get(dataMat[i][-1]).get("y").append(dataMat[i][1])
    for labels in dict1:
        ax.scatter(dict1.get(labels).get("x"),dict1.get(labels).get("y"),c=color[index],label=labels)                
        index=(index+1)%5
    ax.legend(loc=3)
    plt.show()
    

def splitDataSet(dataSet, axis, value):
    subset1 = []
    subset2 = []    
    for row in dataSet:
        if row[axis] < value:
            subset1.append(row)
        else:
            subset2.append(row)
    return subset1,subset2

def CalEntropy(dict1):
    total=0
    for key in dict1:
        total+=dict1[key]
    ent=0
    for key in dict1:
        p=dict1[key]/total
        if  p!=0 :
            ent+= -p *log2(p)
    return ent
 
    
def selectFeatureValue(data,fi):
    #print("feature index=",fi)
    data1=sorted(data,key=lambda x:x[fi])
    #m1=len(data1)
    midv=GetMidv(data1,fi)
    minent=9999999;minp=-1; minv=-333
    dict1={} #dict2={"Owner":12,"Nonowner":12}
    dict2=GetDict(data1)
    m1=len(midv)
    i=0
    for j in range(m1):
        v=midv[j]
        #print("j=",j,"v=",v)
        while data1[i][fi]<v:
            dict2[data1[i][-1]]=dict2[data1[i][-1]]-1
            dict1[data1[i][-1]]=dict1.get(data1[i][-1],0)+1
            i=i+1
        #print("dict1=",dict1)
        ent1=CalEntropy(dict1) #calProbb
        ent2=CalEntropy(dict2)
        t1=0;t2=0
        for k in dict1:
            t1+=dict1.get(k,0)
        for k in dict2:
            t2+=dict2.get(k,0)
        #print(t1,ent1,t2,ent2)
        ent=ent1*t1/(t1+t2)+ent2*t2/(t1+t2)
        #print("******",fi,v,ent)
        #print("ent=",ent)
        if ent<minent:
            minent=ent
            minp=j
            minv=v
    return minent,minp,minv      
    
def GetMidv(datax,fi):
    a=datax[0][fi]
    m=len(datax)
    midv=[]
    for i in range(1,m):
        if datax[i][fi]==a:
            continue
        else:
            x=(a+datax[i][fi] )/2            
            midv.append( (a+datax[i][fi] )/2)
            a=datax[i][fi]
    return midv

def GetDict(data):
    dict1={}
    m=len(data)
    for i in range(m):
        dict1[data[i][-1]]=dict1.get(data[i][-1],0)+1
    return dict1

def selectFeature(data):
    m=len(data[0])
    minv=999999
    for i in range(m-1):
        (minent,minp,minv)=selectFeatureValue(data,i)
        #print("****",i,minent)
        if minent<minv:
            a=(i,minv)
    return a   

def createTree(dataSet,titles):
    classList = [example[-1] for example in dataSet]
    #only one state,such all no, or all yes
    labelset=set(classList)
    count1=0;count2=0
    if(len(labelset)>0):
        x=labelset.pop()
        count1=classList.count(x)
    if(len(labelset)>0):
        x=labelset.pop()
        count2=classList.count(x)
    
    if classList.count(classList[0]) == len(classList):
        return "%s %d"%(classList[0],classList.count(classList[0]))
           
    (bestfeat,bestfeatv) =selectFeature(dataSet)# chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = "%s<%0.2f" % (titles[bestfeat],bestfeatv)#abels[bestFeat]
    bestFeatLabel+=" [%d,%d]" %(count1,count2)  
    myTree = {bestFeatLabel:{}}
    subset1,subset2=splitDataSet(dataSet,bestfeat,bestfeatv)
    v1="True"
    v2="False"
    myTree[bestFeatLabel][v1] = createTree(subset1,titles)
    myTree[bestFeatLabel][v2] = createTree(subset2,titles)
    return myTree 

def CreateData1():    
    data=[  [3,8,"Yes"],
            [3,4,"No"],
            [3,3,"Yes"],
            [3.5,8,"Yes"],#4 8 "yes"
            [4,7,"No"],
            [4,2,"No"]]

    return data
def CreateData2():
    data=[  [7,8,"Yes"],
            [2,4,"No"],
            [5,3,"Yes"],
            [3.5,8,"Yes"],#4 8 "yes"
            [6,7,"No"],
            [4,2,"No"]]
    return data
   

def CreateData3(filename):
    fr=open(filename)
    data=[]
    for line in fr.readlines():
        linedata=[]    
        line=line.strip()
        line=line.split(",")
        linedata.append(float(line[0]))
        linedata.append(float(line[1]))
        linedata.append(line[-1])
        data.append(linedata)
    return data
    
def Test1():
    data=CreateData1()
    ScattterPlot(data)
    res=createTree(data,["Feat1","Feat2"])
    print(res)

def Test2():
    data=CreateData2()
    ScattterPlot(data)
    m1=len(data[0])-1
    minm=999999.787989
    for i in range(m1):
        minent,p,v=selectFeatureValue(data,i)
        if minent<minm :
            a=(minent,v)
    print(a)

def Test3():
    data=[[3,"No"],[3,"Yes"],[4,"No"],[4,"No"]]
    res=selectFeature(data)
    print(res)  
      
def Test4():
    data=CreateData3("mownr.csv")    
    ScattterPlot(data)
    res=createTree(data,["Income","LotSize"])
    print(res)
    createPlot(res)
    

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt,\
    xycoords='axes fraction',
    xytext=centerPt, textcoords='axes fraction',\
    va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)

def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            numLeafs += getNumLeafs(secondDict[key])
        else: numLeafs +=1
    return numLeafs

def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else: thisDepth = 1
        if thisDepth > maxDepth: maxDepth = thisDepth
    return maxDepth

def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString)

def plotTree(myTree, parentPt, nodeTxt):
    numLeafs = getNumLeafs(myTree)
    getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW,\
    plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            plotTree(secondDict[key],cntrPt,str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff),
                 cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD

def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0;
    plotTree(inTree, (0.5,1.0), '')
    plt.show()

if __name__=="__main__":
    Test4()
