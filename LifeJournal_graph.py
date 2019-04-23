import snap
import json
import numpy as np

FollowersCount = np.arange(300, 2001, 100)
n = 10e3
result = []
with open("/home/anastasiya/Documents/DataFromGraph/DataGraphLiveJournal.json", "w") as DataGraphFile:
    for N in FollowersCount:
        print('start', N)
        DataGraph = {}
        LJSocialGraph = snap.LoadEdgeList(snap.PNGraph, '/home/anastasiya/Documents/DataForGraph/soc-LiveJournal1.txt', 0, 1)
        DataGraph['FollowersCount >'] = N
        DataGraph['NodesBeforeClean'] = LJSocialGraph.GetNodes()
        #delete no popular profile, friends < N
        for profile in LJSocialGraph.Nodes():
            if profile.GetDeg() < N:
                LJSocialGraph.DelNode(profile.GetId())
        DataGraph['NodesAfter'] = LJSocialGraph.GetNodes()
        #find connected components
        ComponentsS = snap.TCnComV()
        snap.GetSccs(LJSocialGraph, ComponentsS)
        DataGraph['Components'] = ComponentsS.Len()
        DataGraph['SizeComponentsList'] = []
        for CnCom in ComponentsS:
            DataGraph['SizeComponentsList'].append(CnCom.Len())
        #write in file
        result.append(DataGraph)
        print('finish')
    json.dump(result, DataGraphFile)