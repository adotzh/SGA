import snap
import json
from shutil import copyfile
import numpy as np
n= 342707895
FollowersCount = [50, 100, 150]
FileLink = '/home/ubuntu/main/VKFriendsData/VkFriendsAnalisys2017.json'
FullGraph = "VkAllFriends.graph"
with open(FileLink, 'w') as DataGraphFile:
    DataGraphFile.write(json.dumps([{'filename': 'VkFriendsNew'}], indent=2))

#analysis of graph
for N in FollowersCount:
    VKSocialGraph = snap.TUNGraph.New()
    # load from LJ_varlamov.graph, no change file with full graph
    print 'Start analysis graph, %d' %N
    NewFileName = 'VkFriends%d.graph'%N
    copyfile(FullGraph, NewFileName)
    FIn = snap.TFIn("VkFriends%d.graph"%N)
    print 'Start graph loadind'
    VKSocialGraph = snap.TUNGraph.Load(FIn)
    print 'Graph loadind is completed'
    DataGraph = {}
    DataGraph['FollowersLimit'] = N
    DataGraph['NodesBeforeClean'] = VKSocialGraph.GetNodes()
    # delete no popular profile, friends < N
    for profile in VKSocialGraph.Nodes():
        if profile.GetDeg() < N:
            VKSocialGraph.DelNode(profile.GetId())
    DataGraph['NodesAfter'] = VKSocialGraph.GetNodes()
    # find connected components
    ComponentsS = snap.TCnComV()
    snap.GetWccs(VKSocialGraph, ComponentsS)
    DataGraph['Components'] = ComponentsS.Len()
    DataGraph['SizeComponentsList'] = []
    for CnCom in ComponentsS:
        DataGraph['SizeComponentsList'].append(CnCom.Len())

    # load graph in file
    print 'Start graph loadind in file, %d' %N
    FOut = snap.TFOut("/home/ubuntu/main/VKFriendsData/Graphs/VkWithoutFollower%d.graph" % N)
    VKSocialGraph.Save(FOut)
    FOut.Flush()
    print 'Graph loadind is completed'
    #write data in file
    with open(FileLink) as DataGraphFile:
        feeds = json.load(DataGraphFile)
    feeds.append(DataGraph)
    with open(FileLink, mode='w') as DataGraphFile:
        DataGraphFile.write(json.dumps(feeds, indent=1))
    print 'Finish analysis graph with followers limit = %d, can open DataGraphVKNew.json' %N