import snap
import json
from shutil import copyfile
import numpy as np


FIn = snap.TFIn("/home/ubuntu/main/VkAllFriends.graph")
print 'Start graph loadind'
VkSocialGraph = snap.TUNGraph.Load(FIn)
print 'Graph loadind is completed'
DataGraph = {}
with open("/home/ubuntu/main/VKFriendsData/DataGraphVKFull2017.json", "w") as DataGraphFile:
    ComponentsS = snap.TCnComV()
    DataGraph['FollowersLimit'] = 'Full'
    snap.GetWccs(VkSocialGraph, ComponentsS)
    DataGraph['Components'] = ComponentsS.Len()
    DataGraph['SizeComponentsList'] = []
    for CnCom in ComponentsS:
        DataGraph['SizeComponentsList'].append(CnCom.Len())
    DataGraph['Nodes'] = VkSocialGraph.GetNodes()
    DataGraph['Edges'] = VkSocialGraph.GetEdges()
    #write in file
    DataGraphFile.write(json.dumps(DataGraph, indent=2))