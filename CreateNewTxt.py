import snap
import json

n = 1e5
vk_user_friends_filename = '/home/ubuntu/varlamov-data/vk-user-friends.2016-06-10.txt'
i = 0
VkSocialGraph = snap.TUNGraph.New()
# FOut = snap.TFOut("/home/ubuntu/main/VKFriendsData/VkAllFriends.graph")
VkFullGraph = '/home/ubuntu/main/VKFriendsData/VkFullGraph2016.txt'
print 'Start create file'
with open(VkFullGraph, 'w') as file:
    a = ['# Undirected graph (each unordered pair of nodes is saved once): VkFullGraph.txt',
    '# Save as tab-separated list of edges',
    ' ',
    '# NodeId        NodeId']
    for line in a:
        file.write(line + '\n')
print "File's pattern is done"
#create graph
with open(vk_user_friends_filename, 'r') as data_profile:
    Edges_count = 0
    for one_profile_info in data_profile:
        one_profile_info = json.loads(one_profile_info)
        if not VkSocialGraph.IsNode(one_profile_info['id']):
            VkSocialGraph.AddNode(one_profile_info['id'])
        for Node in one_profile_info['value']:
            if not VkSocialGraph.IsNode(Node):
                VkSocialGraph.AddNode(Node)
                with open(VkFullGraph, 'a') as file:
                    Edges_count += 1
                    file.write('%d\t%d\n'%(one_profile_info['id'], Node))
        if i % n == 0:
            print(i, VkSocialGraph.GetNodes(), Edges_count)
        i += 1
print'# Nodes: %d Edges: %d' %(VkSocialGraph.GetNodes(), Edges_count)

#save Graph in file
# snap.SaveEdgeList(VkSocialGraph, "test.txt", "Save as tab-separated list of edges")
#
# #find connected components
# DataGraph = {}
# with open("/home/ubuntu/main/VKFriendsData/DataGraphVKFull.json", "w") as DataGraphFile:
#     ComponentsS = snap.TCnComV()
#     DataGraph['FollowersLimit'] = 'Full'
#     snap.GetSccs(VkSocialGraph, ComponentsS)
#     DataGraph['Components'] = ComponentsS.Len()
#     DataGraph['SizeComponentsList'] = []
#     for CnCom in ComponentsS:
#         DataGraph['SizeComponentsList'].append(CnCom.Len())
#     DataGraph['Nodes'] = VkSocialGraph.GetNodes()
#     DataGraph['Edges'] = VkSocialGraph.GetEdges()
#     #write in file
#     DataGraphFile.write(json.dumps(DataGraph, indent=2))
