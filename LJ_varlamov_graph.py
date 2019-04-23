import snap
import json
import shelve
import numpy as np

FollowersCount = np.arange(300, 2001, 100)
LJ_user_filename = '/home/ubuntu/varlamov-data/lj-user-2017-03-06.json'
LJDataForGraph = shelve.open('LJNewFormat')


#create new format for data
# print('Start create new data format')
# i = 0
# with open(LJ_user_filename, 'r') as data_profile:
#    for one_profile_info in data_profile:
#        one_profile_info = json.loads(one_profile_info)
#        if str(one_profile_info['value']['status']) == 'active':
#            if i % 100000 == 0:
#                print(i, one_profile_info)
#            try:
#                LJDataForGraph[str(one_profile_info['value']['login'])] = int(one_profile_info['value']['id'])
#            except UnicodeError:
#                print('UnicodeError, ', one_profile_info['value']['login'])
#            except LookupError:
#                print('LookupError, ', one_profile_info)
#            i += 1
# print('Finish create new data format')



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

# load from LJ_varlamov.graph
# FIn = snap.TFIn("LJ_varlamov.graph")
# LJSocialGraph = snap.TUNGraph.Load(FIn)


#analysis of graph
# with open("DataGraphLiveJournalVarlamov.json", "w") as DataGraphFile:
#     for N in FollowersCount:
#         print('Start analysis graph, ', N)
#         DataGraph = {}
#         DataGraph['FollowersCount >'] = N
#         DataGraph['NodesBeforeClean'] = LJSocialGraph.GetNodes()
#         # delete no popular profile, friends < N
#         for profile in LJSocialGraph.Nodes():
#             if profile.GetDeg() < N:
#                 LJSocialGraph.DelNode(profile.GetId())
#         DataGraph['NodesAfter'] = LJSocialGraph.GetNodes()
#         # find connected components
#         ComponentsS = snap.TCnComV()
#         snap.GetSccs(LJSocialGraph, ComponentsS)
#         DataGraph['Components'] = ComponentsS.Len()
#         DataGraph['SizeComponentsList'] = []
#         for CnCom in ComponentsS:
#             DataGraph['SizeComponentsList'].append(CnCom.Len())
#         # write in file
#         result.append(DataGraph)
#         print('Finish analysis graph, can open DataGraphLiveJournalVarlamov.json')
#     json.dump(result, DataGraphFile)







