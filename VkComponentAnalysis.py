import snap
import json
from shutil import copyfile



VKSocialGraph = snap.TUNGraph.New()
print 'Start analysis graph, %Full'
GraphFile = 'VkAllFriends.graph'
FIn = snap.TFIn(GraphFile)
print 'Start graph loadind'
VKSocialGraph = snap.TUNGraph.Load(FIn)
print 'Graph loadind is completed'


Id_List = [64649408]
Id_Components = {}
ComponentsS = snap.TCnComV()
snap.GetWccs(VKSocialGraph, ComponentsS)
i = 0
file = open('ComponentsFriend.txt', 'w')
for CnCom in ComponentsS:
    i += 1
    for NI in CnCom:
        if NI in Id_List:
            Id_Components[i] = NI
print(Id_Components)







    # if len(CnCom) < 100:
    #         tailfile.write('Component number = %d, size = %d: ' % (i, len(CnCom)))
    #         for NI in CnCom:
    #             store.append(NI)
    #         tailfile.write(str(store) + '\n')
    # else:
    #     with open('Component%d.txt'%i, 'w') as file:
    #         file.write('Component number = %d, size = %d\n' %(i, len(CnCom)))
    #         for NI in CnCom:
    #             store.append(NI)
    #         file.write(str(store))
