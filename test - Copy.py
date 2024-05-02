import osmnx as ox
import matplotlib.pyplot as plt

# Définir la région de Bejaia, Algérie
place_name = "Bejaia, Algeria"

# Extraire le réseau routier dans la région de Bejaia
G = ox.graph_from_place(place_name, network_type='all')

# Extraire les points d'intérêt (écoles) dans la région de Bejaia
school_nodes = ox.pois.pois_from_place(place_name, amenities=['school'])

# Créer le graphique
fig, ax = ox.plot_graph(G, figsize=(10, 10), show=False, close=False, edge_color='gray', node_color='w', node_size=0)

# Ajouter les écoles et leurs noms
for _, node in school_nodes.iterrows():
    school_name = node['name']
    x, y = node['geometry'].x, node['geometry'].y
    ax.scatter(x, y, color='blue', s=50)
    ax.text(x, y, school_name, fontsize=8, ha='left', va='center', color='blue')

# Ajouter le titre et l'étiquette de l'axe
plt.title('Écoles dans la région de Bejaia')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

plt.tight_layout()
plt.show()
