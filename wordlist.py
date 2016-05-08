#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        wordlist.py
# Purpose:
#
# Author:      blog.a20.co.za
#
# Created:     09-06-2015
#-------------------------------------------------------------------------------
import os
import re
import cPickle as pickle
from spgraph import Graph as dGraph
PERSISTENT_FILE = "nodes.bin"
WORD_FILE = "wordlist.txt"
#dictionary supports TEARS->SEARS->STARS->STARE->STALE->STILE->SMILE
class Graph(object):
	def __init__(self):
		self._nodes = {} #dict of words
		self._g = dGraph()
		pass
	def load_from_file(self, f):
		print "Loading from file."
		self._nodes = pickle.load(open(f,"rb"))
		print "Loaded from file."
		pass
	def save_to_file(self, f):
		pickle.dump(self._nodes, open(f,"wb"))
		pass
	def SetContents(self, c):
		if (c is None) or len(c.strip())==0:
			raise Exception("Word list cannot be empty.")
		self._contents = c.lower()
	def CreateEdge(self, s,e):
		if (not self._nodes[s].__contains__(e)) and e!=s:
			self._nodes[s].append(e)
			self._g.AddEdge(s,e,1)
	def BuildFromFile(self, fn):
		if not os.path.isfile(fn):
			raise Exception("Could not load the word file %s so cannot continue."%(s))
		contents = ""
		with open(fn) as f:
			contents = f.read()
			self.SetContents(contents)
			for w in contents.split():
				g.CreateNode(w.lower())
		self.BuildMatchings()
	def BuildMatchings(self):
		keys = self._nodes.keys()
		print "Building matches.. Total worlds %d." % len(keys)
		for w in keys:
			#print "Building for word %s" % (w)
			for i in range(len(w)):
				pattern = list(w) #turn into set
				pattern[i]= "[a-z]{1}"
				pattern = "".join(pattern) #turn into string
				for m in re.findall(pattern, self._contents):
					self.CreateEdge(w,m)
		print "Built matches."
	def CreateNode(self, w):
		if not self._nodes.has_key(w):
			self._nodes[w] = []
			self._g.AddVertex(w)
	def FindLadder(self, s, d):
		return self._g.FindShortestPath(s,d)
	def BuildGraph(self):
		self._g = dGraph()
		for j in self._nodes:
			self._g.AddVertex(j)
			for i in self._nodes[j]:
				self._g.AddEdge(j,i)
if __name__=="__main__":
	g = Graph()
	if not os.path.isfile(PERSISTENT_FILE):
		print "Could not find the dictionary file, rebuilding it."
		g.BuildFromFile(WORD_FILE)
		g.save_to_file(PERSISTENT_FILE)
	g.load_from_file(PERSISTENT_FILE)
	g.BuildGraph()
	r = g.FindLadder("birth","death")
	print "->".join(r)
	print "Used %d steps" %(len(r))
	print "End."
