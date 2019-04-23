import snap
import json
from shutil import copyfile
import numpy as np

FollowersCount = [1]
result = []

#analysis of graph
with open("DataGraphLiveJournalVarlamov.json", "w") as DataGraphFile:
    for N in FollowersCount:
        print 'Start analysis graph, ', N
        # load from LJ_varlamov.graph, no change file with full graph
        NewFileName = "/home/anastasiya/PycharmProjects/Snap_1/Data/LJ_varlamov%d.graph" %N
        copyfile("/home/anastasiya/PycharmProjects/Snap_1/Data/LJVarlamov/LJ_varlamov.graph", NewFileName)

        FIn = snap.TFIn(NewFileName)
        LJSocialGraph = snap.TUNGraph.Load(FIn)
        DataGraph = {}
        DataGraph['FollowersLimit'] = N
        DataGraph['NodesBeforeClean'] = LJSocialGraph.GetNodes()
        # delete no popular profile, friends < N
        if N > 0:
            for profile in LJSocialGraph.Nodes():
                if profile.GetDeg() < N:
                    LJSocialGraph.DelNode(profile.GetId())
        DataGraph['NodesAfter'] = LJSocialGraph.GetNodes()
        # find connected components
        ComponentsS = snap.TCnComV()
        snap.GetSccs(LJSocialGraph, ComponentsS)
        DataGraph['Components'] = ComponentsS.Len()
        DataGraph['SizeComponentsList'] = []
        for CnCom in ComponentsS:
            DataGraph['SizeComponentsList'].append(CnCom.Len())
        # write in file
        result.append(DataGraph)
        FOut = snap.TFOut(NewFileName)
        LJSocialGraph.Save(FOut)
        print 'Finish analysis graph, can open DataGraphLiveJournalVarlamovNew.json'
    json.dump(result, DataGraphFile)