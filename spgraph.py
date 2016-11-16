#!/usr/bin/env python
from Queue import PriorityQueue
from random import randint
class SOPriorityQueue(PriorityQueue):
    def __init__(self):
        PriorityQueue.__init__(self)
        self.counter=0
    def put(self,item,priority):
        PriorityQueue.put(self,(priority,self.counter,item))
        self.counter +=1
    def get(self,*args,**kwargs):
        _,_, item = PriorityQueue.get(self,*args,**kwargs)
        return item
class Graph:
    def __init__(self):
        self._vertexes = {}
        self._edges = {}
        self._distance={}
        self._previous={}
        self._connectednodes = 0
    def AddEdge(self, a,b, weight=0):
            if not a in self._vertexes:
                self._vertexes[a] = {}
            if not b in self._vertexes[a]:
                self._vertexes[a][b]={}
            if not b in self._vertexes:
                self._vertexes[b] = {}
            if not a in self._vertexes[b]:
                self._vertexes[b][a]={}
            self._vertexes[b][a]=weight
            self._vertexes[a][b]=weight
    def AddVertex(self,v):
            self._vertexes[v]={}
    def __str__(self):
        return self.getDot()
    def __getitem__(self, n):
        if n in self._vertexes:
            return self._vertexes[n]
        else:
            return None
    def GetShortestPath(self,end):
        q = []
        b = end
        while self._previous[b] is not None:
            if self._distance[b]==float("inf"):
                raise Exception("Cannot cross an infinite path.")
            b = self._previous[b]
            q.append(str(b))
        q.reverse()
        q.append(str(end))
        #print "Path %s to %s has cost %s Path is: %s"%(q[0],end,self._distance[end],'->'.join(q))
        return q
    def getDot(self):
        found = {}
        s = ""
        s += 'graph G {\n node [width=.5,height=.5,shape=box,style=filled,color=skyblue];\noverlap="true";\nrankdir="LR";\n'
        for i in self._vertexes:
            for j in self._vertexes[i]:
                if not (found.has_key((j,i)) or found.has_key((i,j))): #dual edged
                    s += '      '+ str(i)
                    s +=  ' -- ' +  str(j) + ' [label="' + str(self._vertexes[i][j]) + '"] [type=s]'
                    s+=';\n'
                    found[(j,i)]=True
                    found[(i,j)]=True
        s += "}"
        return s
    def writeDotFile(self, fileName="graph.gvz"):
        f = open(fileName,'w')
        f.writelines(self.getDot())
        f.close()  
    def FindShortestPath(self,source,destination=None):
        _pq = SOPriorityQueue()
        for v in self._vertexes:
            self._previous[v] = None
            self._distance[v]=float("inf")
            if v==source:
                _pq.put(v,0)
            else:
                _pq.put(v,float("inf")) #return by lowest weight first
        self._distance[source] = 0
        while not _pq.empty():
              e = _pq.get()
              for neighbour in self._vertexes[e]:
                alt = self._distance[e] +self._vertexes[e][neighbour]
                if alt < self._distance[neighbour]:
                    self._distance[neighbour] = alt
                    self._previous[neighbour] = e
                    _pq.put(neighbour,alt)
              if self._distance[e]==float("inf"):
                  raise Exception("Some destination edge (%s) is infinite, probably not reachable so path cannot be constructed." %e)
                  break
              if destination <> None:
                 if e==destination:
                     return self.GetShortestPath(destination)
        return self._distance

