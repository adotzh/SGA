import snap
import json
import shelve
import numpy as np

LJ_user_filename = '/home/ubuntu/varlamov-data/lj-user-2017-03-06.json'
LJDataForGraph = shelve.open('LJNewFormat')


#create LiveJournal social graph
LJSocialGraph = snap.TUNGraph.New()
FOut = snap.TFOut("LJ_varlamov.graph")

n = 10e3
result = []

#create graph
print('Start create graph')
with open(LJ_user_filename, 'r') as data_profile:
    undir = 0
    unic = 0
    node_extra = 0
    i = 0
    for one_profile_info in data_profile:
        one_profile_info = json.loads(one_profile_info)
        if str(one_profile_info['value']['status']) == 'active':
            try:
                id = LJDataForGraph[str(one_profile_info['value']['login'])]
                if not LJSocialGraph.IsNode(id):
                    LJSocialGraph.AddNode(id)
                    try:
                        for Node in one_profile_info['value']['undirectedLinks']:
                            try:
                                Node_id = LJDataForGraph[str(Node)]
                                if LJSocialGraph.IsNode(Node_id):
                                    LJSocialGraph.AddEdge(id, Node_id)
                                else:
                                    LJSocialGraph.AddNode(Node_id)
                                    LJSocialGraph.AddEdge(id, Node_id)
                            except LookupError:
                                node_extra += 1
                                if node_extra % 100000 == 0:
                                    print('Lookup id Error, count = %d', node_extra)
                    except LookupError:
                        undir += 1
                        if undir % 10000 == 0:
                            print('Lookup undirectedLinks Error, count = %d', undir)
            except UnicodeError:
                unic += 1
                if unic % 1000 == 0:
                    print('UnicodeError, count = %d', unic)
        if i % n == 0:
            print(i, LJSocialGraph.GetNodes(), LJSocialGraph.GetEdges())
        i += 1
print('Finish %d, %d, %d' %(i, LJSocialGraph.GetNodes(), LJSocialGraph.GetEdges()))
#close shelve file
LJDataForGraph.close()

#save Graph in file
LJSocialGraph.Save(FOut)