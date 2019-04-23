import snap
import json

class SocialGraph(object):
    __num_limit = 1e5

    def __init__(self, file_name, type):
        self.type = type
        self.graph = snap.TUNGraph.New() if self.type == 'Undirected' else snap.TNGraph.New()
        with open(file_name, 'r') as data_profile:
            for i, one_profile_info in enumerate(data_profile):
                profile = dict(zip(['Node1', 'Node2'], [int(id) for id in one_profile_info.split(' ')[:2]]))
                self.graph.AddNode(profile['Node1']) if not self.graph.IsNode(profile['Node1']) else None
                self.graph.AddNode(profile['Node2']) if not self.graph.IsNode(profile['Node2']) else None
                self.graph.AddEdge(profile['Node1'], profile['Node2'])
                # if i % self.__num_limit == 0:
                #     print(i, self.graph.GetNodes(), self.graph.GetEdges())
        print(self.graph.GetNodes(), self.graph.GetEdges())


    def create_limit_graph(self, N_limit):
        self.N_limit = N_limit
        self.i = 0
        self.limit_graph = snap.TUNGraph.New() if self.type == 'Undirected' else snap.TNGraph.New()
        for FriendShip in self.graph.Edges():
            (User1, User2) = map(self.graph.GetNI, FriendShip.GetId())
            self.limit_graph.AddNode(User1.GetId()) if not self.limit_graph.IsNode(User1.GetId()) and User1.GetOutDeg() >= N_limit else None
            self.limit_graph.AddNode(User2.GetId()) if not self.limit_graph.IsNode(User2.GetId()) and User2.GetOutDeg() >= N_limit else None
            self.limit_graph.AddEdge(User1.GetId(), User2.GetId()) if self.limit_graph.IsNode(User1.GetId()) and self.limit_graph.IsNode(User2.GetId()) else None
        return self.limit_graph

    def get_components(self):
        ComponentsS = snap.TCnComV()
        snap.GetWccs(self.graph, ComponentsS)
        DataGraph = {'FollowersLimit': 0,
                     'NodesBeforeClean': self.graph.GetNodes(),
                     'NodesAfter': self.graph.GetNodes(),
                     'Components': ComponentsS.Len(),
                     'SizeComponentsList': []}
        for CnCom in ComponentsS:
            DataGraph['SizeComponentsList'].append(CnCom.Len())
        return DataGraph

    def get_components_limit(self):
        ComponentsS = snap.TCnComV()
        snap.GetWccs(self.limit_graph, ComponentsS)
        DataGraph = {'FollowersLimit': self.N_limit,
                     'NodesBeforeClean': self.graph.GetNodes(),
                     'NodesAfter': self.limit_graph.GetNodes(),
                     'Components': ComponentsS.Len(),
                     'SizeComponentsList': []}
        for CnCom in ComponentsS:
            DataGraph['SizeComponentsList'].append(CnCom.Len())
        return DataGraph



