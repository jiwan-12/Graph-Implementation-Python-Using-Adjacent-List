"""This file implement the graph algorithm using adjacent list structure"""
import collections
import heapq

class Graph(object):
	def __init__(self, connection, directed=False):
		self.__graph = collections.defaultdict(set)
		self.__edge = collections.defaultdict(None)
		self.__state = collections.defaultdict(dict)
		self.__directed = directed
		self.build_graph(connection)

	def __initilize_state_BFS(self):
		for n in self.__graph:
			self.__state[n] = dict(u=None, d=0, c=-1)
		
	def __initilize_state_DFS(self):
		for n in self.__graph:
			self.__state[n] = dict(u=None, s=0, f=0,c=-1)		

	def add_node(self,n1, n2):
		if n2 is None:
			self.__graph[n1] = set()
		else:		
			self.__graph[n1].add(n2)

	def add_dege(self, n1, n2, wt=0):
		self.__edge[(n1,n2)] = wt

	def build_graph(self, connection, data_form=0):
		# data_form 0: (n1,n2,w)
		# data_form 1: (n1,n2)
		for n1, n2, wt in connection:
			self.add_node(n1, n2)
			if n2:
				self.add_dege(n1, n2, wt)
	
	

	def is_connected(self, n1, n2):
		return n2 in self.__graph[n1]

	def DFS(self, start=None):

		# initialize state
		self.__initilize_state_DFS()

		# recursive state
		self.__time = 0
		dfs_forest = []
		dfs_tree = []

		def dfs(u):
			self.__state[u]['c']=0
			self.__time += 1
			self.__state[u]['s']=self.__time
			for v in sorted(self.__graph[u]):
				if self.__state[v]['c']==-1:
					self.__state[v]['c']=1
					self.__state[v]['u']=u
					dfs(v)
					dfs_tree.append(v)
			self.__state[u]['c'] = 1
			self.__time += 1
			self.__state[u]['f'] = self.__time

		for u in self.__graph:


			if self.__state[u]['c']==-1:
				dfs_tree=[u]
				dfs(u)
				dfs_forest.append(dfs_tree)
				dfs_tree = []
		print "DFS forest: {}\n".format(dfs_forest)		
	
	def BFS(self, start=None):
		# initialize of bfs #
		self.__initilize_state_BFS()
		bfs_tree = []
		def bfs(start):
			self.__state[start]['d'] = 0
			queue = [start]
			while queue:
				u = queue.pop(0)
				for v in self.__graph[u]:
					if self.__state[v]['c']==-1:
						self.__state[v]['c']= 0
						self.__state[v]['d'] = self.__state[u]['d']+1
						self.__state[v]['u'] = u
						queue.append(v)
				self.__state[u]['c']=1
				bfs_tree.append(u)
		bfs('r')
		print "bfs tree:{}".format(bfs_tree)		

	def kruskal_MST(self, start=None):
		#** initialization **#
		disjoint_set=[]
		def make_set():
			"""Make disjoint set"""
			for v in self.__graph:
				disjoint_set.append(set(v))

		def find_set(v):
			"""Search disjoint set"""
			for s in disjoint_set:
				if v in s: return s


		def kruskal():
			make_set()
			sorted_edge = [(v, k) for k, v in self.__edge.iteritems()]
			heapq.heapify(sorted_edge)
			mst_path = []
			mst_wt = 0
			while sorted_edge:
				wt, edge = heapq.heappop(sorted_edge)
				u,v = edge
				u_set = find_set(u)
				v_set = find_set(v)
				if u_set != v_set:
					union_set = u_set.union(v_set)
					disjoint_set.remove(u_set)
					disjoint_set.remove(v_set)
					disjoint_set.append(union_set)
					mst_path.append((u,v))
					mst_wt += wt

			print 'MST using Kruskal MST WT: {}, Path : {}'.format(mst_wt, mst_path)		

		kruskal()	

	def prims_MST(self, start=None):

		def prims(start):
			state = dict()
			for u in self.__graph:
				state[u]=dict(pi=None,k=float('inf'))
			state[start]['k']=0	
			Q = [(0, start)]
			heapq.heapify(Q)
			mst_wt = 0
			mst_path = []
			while len(mst_path)<len(self.__graph):
				wt,u = heapq.heappop(Q)
				if u in mst_path: continue
				for v in self.__graph[u]:
					if v not in mst_path and self.__edge[(u,v)] < state[v]['k']:
						state[v]['k'] = self.__edge[(u,v)]
						state[v]['pi'] = u
						w = self.__edge[(u,v)]
						heapq.heappush(Q,(w,v))

				mst_path.append(u)
				mst_wt += wt

			print 'MST using prims MST WT: {}, Path : {}'.format(mst_wt, mst_path)									
		prims('a')				

	def dijkstra_SP(self, start=None):
		state = dict()
		def initialize(s):
			for v in self.__graph:
				state[v] = dict(d=float('inf'),pi=None)
			state[s]['d'] = 0
		
		def relax(u,v,w):
			if state[v]['d']>state[u]['d']+w:
				state[v]['d'] = state[u]['d']+w
				state[v]['pi'] = u

		def extract_min(S):
			temp = [(k, v['d']) for k, v in state.iteritems() if k not in S]
			temp.sort(key = lambda x:x[1])
			return temp

		def dijkstra(start):
			initialize(start)
			S = set()
			Q = extract_min(S)
			while Q:
				u , w = Q.pop(0)
				S = S.union(u)
				for v in self.__graph[u]:
					relax(u,v,self.__edge[(u,v)])
				Q = extract_min(S)			

		dijkstra('s')
		for k, v in state.iteritems():
			print "s --> {} : {}".format(k,v['d'])		

	def bellman_ford_SP(self, start=None):
		state = dict()	
		def initialize(s):
			for v in self.__graph:
				state[v]=dict(d=float('inf'),pi=None)
			state[s]['d'] = 0

		def relax(u,v,w):
			if state[v]['d'] > state[u]['d']+w:
				state[v]['d'] = state[u]['d']+w
				state[v]['pi'] = u

		def bellman_ford(start):
			initialize(start)
			for _ in xrange(0,len(self.__graph)):
				for e ,w in self.__edge.items():
					u,v = e
					relax(u,v,w)

			for e ,w in self.__edge.items():
				u,v = e
				if state[v]['d'] > state[u]['d']+w:
					return False
				return True

		print bellman_ford('s')
		for k, v in state.iteritems():
			print "s --> {} : {}".format(k,v['d'])					




	def print_graph(self):					
		print'{}({})'.format(self.__class__.__name__, dict(self.__graph))
	def print_edge(self):					
		print'{}({})'.format(self.__class__.__name__, dict(self.__edge))
	def print_state(self):
		print'{}({})'.format(self.__class__.__name__, dict(self.__state))	
		

if __name__=='__main__':
	conn_mst=[
		('a','b',4), ('a','h',8),
		('b','a',4), ('b','c',8), ('b','h',11),
		('c','d',7), ('c','i',2), ('c','f',4),
		('d','c',7), ('d','e',9), ('d','f',14),
		('e','d',9), ('e','f',10),
		('f','g',2), ('f','c',4), ('f','d',14),
		('g','h',1), ('g','i',6), ('g','f',2),
		('h','a',8), ('h','i',7), ('h','b',11),('h','g',1),
		('i','h',7), ('i','g',6), ('i','c',2)
		]

	conn_dfs = [
		('u','v',1),('u','x',1),
		('v','y',1),
		('w','y',1),
		('x','y',1),
		('y','x',1),
		('z','z',0),		
	]

	conn_bfs = [
		('r','v',1), ('r','s',1),
		('s','w',1), ('s','r',1),
		('t','u',1), ('t','w',1), ('t','x',1),
		('u','t',1), ('u','x',1), ('u','y',1),
		('v',None,0),
		('w','x',1), ('w','s',1), ('w','t',1),
		('x','w',1), ('x','t',1), ('x','y',1), ('x','u',1),
		('y','x',1), ('y','u',1),
	]

	cons_dijkstra = [
		('s','t',10), ('s','y',5),
		('t','y',2), ('t','x',1),
		('x','z',4),
		('y','z',2), ('y','x',9), ('y','t', 3),
		('z','x',6), ('z','s',7)
		]

	cons_bellman_ford = [
		('s','t',6), ('s','y',7),
		('t','y',8), ('t','x',5),('t','z',-4),
		('x','t',-2),
		('y','z',9), ('y','x',-3),
		('z','x',7), ('z','s',2)
		]	
	# g = Graph(conn_dfs)
	# g.print_edge()
	# g.DFS()
	# g = Graph(conn_bfs)
	# g.BFS()
	# g.print_state()
	# g = Graph(conn_mst)
	# g.kruskal_MST()	
	# g.prims_MST()
	# g.print_graph()

    g = Graph(cons_bellman_ford)
	g.bellman_ford_SP()






		
