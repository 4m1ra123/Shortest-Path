from flask import Flask, render_template, request
import osmnx as ox
import networkx as nx

app = Flask(__name__)

from math import sqrt

def distance(node1, node2):
    return sqrt((node1['x'] - node2['x'])**2 + (node1['y'] - node2['y'])**2)

def heuristic(node, target):
    return distance(node, target)

#Recuperation de la carte de la ville choisie(ici bejaia) a partir du package osmnx
def get_map_data(city_name):
        point = ox.geocode(f"{city_name}, Algeria")
        graph = ox.graph_from_point(point, dist=2000, network_type='drive')  
        return graph
   


#Pour ne pas surcharger et juste pour l'execution nous avons choisi de prendre 10 noeuds uniquement
def get_some_nodes(graph, num_nodes=10):
    if graph:
        return list(graph.nodes)[:num_nodes]
    else:
        return []


#Utilisation de l'algorithme d'A*
def find_shortest_path(graph, source, target):
    if graph:
        try:

            shortest_path = nx.astar_path(graph, source, target, weight='length')
            return shortest_path
        except nx.NetworkXNoPath:
            return "Il n'existe pas de chemins entre ces 2 regions selectionnees"
    else:
        return None

city_name = 'Bejaia'
graph = get_map_data(city_name)
nodes = get_some_nodes(graph)



def custom_astar(graph, source, target):
    if graph:
        open_set = {source}
        came_from = {}
        g_score = {source: 0}
        f_score = {source: heuristic(graph.nodes[source], graph.nodes[target])}

        while open_set:
            current = min(open_set, key=lambda x: f_score.get(x, float('inf')))
            if current == target:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path
            open_set.remove(current)

            for neighbor in graph.neighbors(current):
                tentative_g_score = g_score[current] + distance(graph.nodes[current], graph.nodes[neighbor])
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(graph.nodes[neighbor], graph.nodes[target])
                    if neighbor not in open_set:
                        open_set.add(neighbor)

        return "Il n'existe pas de chemins entre ces 2 regions selectionnees"
    else:
        return None



@app.route('/', methods=['GET', 'POST'])
def front():
    global graph, nodes
    
    if request.method == 'POST':
        source_node = int(request.form['source'])
        target_node = int(request.form['target'])

        #shortest_path = find_shortest_path(graph, source_node, target_node)
        shortest_path = custom_astar(graph, source_node, target_node)
        img_path = None
        if graph and shortest_path:
            img_path = 'static/graph.png'
            ox.plot_graph_route(graph, shortest_path, node_color='w', node_edgecolor='k', node_size=30, save=True, filepath=img_path)
        
       
        return render_template('front.html', city=city_name, nodes=nodes, shortest_path=shortest_path, img_path=img_path)
    
    else:
        return render_template('front.html', city=city_name, nodes=nodes)

if __name__ == "__main__":
    app.run(debug=True)
