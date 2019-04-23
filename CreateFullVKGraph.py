import snap
import json

n = 1e6
vk_user_friends_filename = '/home/ubuntu/varlamov-data/vk-user-friends.2017-01-18.txt'

i = 0
VkSocialGraph = snap.TUNGraph.New()
FOut = snap.TFOut("VkAllFriends.graph")
#create graph
print 'Start create graph'
with open(vk_user_friends_filename, 'r') as data_profile:
    for one_profile_info in data_profile:
        one_profile_info = json.loads(one_profile_info)
        if not VkSocialGraph.IsNode(one_profile_info['id']):
            VkSocialGraph.AddNode(one_profile_info['id'])
        for Node in one_profile_info['value']:
            if not VkSocialGraph.IsNode(Node):
                VkSocialGraph.AddNode(Node)
            VkSocialGraph.AddEdge(one_profile_info['id'], Node)
        if i % n == 0:
            print(i, VkSocialGraph.GetNodes(), VkSocialGraph.GetEdges())
        i += 1
print(i, VkSocialGraph.GetNodes(), VkSocialGraph.GetEdges())

#save Graph in file
VkSocialGraph.Save(FOut)
FOut.Flush()
print 'Finish load FullGraph'

#find connected components
#DataGraph = {}
#with open("/home/ubuntu/main/VKFriendsData/DataGraphVKFull2017.json", "w") as DataGraphFile:
#    ComponentsS = snap.TCnComV()
#    DataGraph['FollowersLimit'] = 'Full'
#    snap.GetSccs(VkSocialGraph, ComponentsS)
#    DataGraph['Components'] = ComponentsS.Len()
#    DataGraph['SizeComponentsList'] = []
#    for CnCom in ComponentsS:
#        DataGraph['SizeComponentsList'].append(CnCom.Len())
#    DataGraph['Nodes'] = VkSocialGraph.GetNodes()
#    DataGraph['Edges'] = VkSocialGraph.GetEdges()
#    #write in file
#    DataGraphFile.write(json.dumps(DataGraph, indent=2))
