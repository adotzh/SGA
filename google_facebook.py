from social_graph import SocialGraph
import snap

file_name = '/home/anastasiya/Documents/DataForGraph/ego-facebook/out.ego-facebook'
facebook = SocialGraph(file_name, 'Undirected')
graph_n = facebook.create_limit_graph(1)
print graph_n.GetNodes(), graph_n.GetEdges()
print facebook.get_components_limit()