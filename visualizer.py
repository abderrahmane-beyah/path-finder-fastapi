import networkx as nx
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import io
import base64
from graph import pos

def visualize_route(graph_data, paths_data, start_city, end_city):
    """
    Generates an image of the graph highlighting multiple alternative paths.
    Returns the image encoded in base64 format for web display.

    Args:
        graph_data: Dictionary of the graph
        paths_data: List of tuples (distance, path) or single path for compatibility
        start_city: Starting city
        end_city: Ending city
    """
    G = nx.Graph()

    # 1. Add nodes and edges
    for city, neighbors in graph_data.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(city, neighbor, weight=weight)

    # 2. Set node positions with real GPS coordinates
    # Using geographic coordinates (longitude, latitude) of Mauritanian cities
    # Format: (longitude, latitude) for accurate geographic display
    

    # Handle case where paths_data is a simple list (old format)
    if isinstance(paths_data, list) and len(paths_data) > 0 and not isinstance(paths_data[0], tuple):
        paths_data = [(0, paths_data)]  # Convert to new format

    # Extract all paths
    all_paths = [path for _, path in paths_data]

    # 3. Define colors for each path
    path_colors = [
        '#e67e22',  # Orange - Optimal path
        '#3498db',  # Blue - Alternative 1
        '#9b59b6',  # Purple - Alternative 2
    ]

    # 4. Define node colors (highlight start/end)
    node_colors = []
    all_path_nodes = set()
    for path in all_paths:
        all_path_nodes.update(path)

    for node in G.nodes():
        if node == start_city:
            node_colors.append('#2ecc71')  # Green for start
        elif node == end_city:
            node_colors.append('#e74c3c')  # Red for end
        elif node in all_path_nodes:
            node_colors.append('#f39c12')  # Orange for path cities
        else:
            node_colors.append('#95a5a6')  # Gray for other cities

    # 5. Prepare edges for each path
    # Create a dictionary to track which edge belongs to which path(s)
    edge_to_paths = {}
    for i, path in enumerate(all_paths):
        path_edges = list(zip(path, path[1:]))
        for edge in path_edges:
            edge_normalized = tuple(sorted(edge))
            if edge_normalized not in edge_to_paths:
                edge_to_paths[edge_normalized] = []
            edge_to_paths[edge_normalized].append(i)

    # Assign colors and widths to edges
    edge_colors = []
    edge_widths = []

    for (u, v) in G.edges():
        edge_normalized = tuple(sorted((u, v)))
        if edge_normalized in edge_to_paths:
            # This edge is part of at least one path
            path_idx = edge_to_paths[edge_normalized][0]  # Use color of first path
            edge_colors.append(path_colors[path_idx])
            edge_widths.append(4 if path_idx == 0 else 3)  # Thicker for optimal
        else:
            edge_colors.append('#bdc3c7')  # Light gray for other edges
            edge_widths.append(1)

    # 4. Create figure with larger size and improved style
    fig, ax = plt.subplots(figsize=(16, 10), facecolor='white')
    ax.set_facecolor('#f8f9fa')

    # 5. Draw graph with improved style

    # Draw edges with curved connections to reduce overlaps
    nx.draw_networkx_edges(
        G, pos,
        edge_color=edge_colors,
        width=edge_widths,
        alpha=0.7,
        arrows=True,  
        connectionstyle='arc3,rad=0.1'  # Curved edges
    )

    # Draw nodes with borders
    nx.draw_networkx_nodes(
        G, pos,
        node_color=node_colors,
        node_size=800,  # Reduced from 2000 to 800 to avoid overlaps
        edgecolors='#2c3e50',
        linewidths=1.5,  # Reduced from 2.5 to 1.5
        alpha=0.9
    )

    # Draw labels with improved style
    nx.draw_networkx_labels(
        G, pos,
        font_size=8,  # Reduced from 11 to 8
        font_weight='bold',
        font_family='sans-serif',
        font_color='white'
    )

    # Add edge labels (distances) with improved positioning
    edge_labels = nx.get_edge_attributes(G, 'weight')
    formatted_edge_labels = {k: f'{v} km' for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=formatted_edge_labels,
        font_color='#2c3e50',
        font_size=7,  # Reduced from 9 to 7
        font_weight='normal',  # Changed from 'bold' to 'normal' for less clutter
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.8)  # Reduced padding
    )

    # 6. Add title and legend
    if len(all_paths) == 1:
        route_display = ' → '.join(all_paths[0])
        total_distance = sum(graph_data[all_paths[0][i]][all_paths[0][i+1]] for i in range(len(all_paths[0])-1))
        title_text = f"Shortest route: {start_city} to {end_city}\n{route_display}\nTotal distance: {total_distance} km"
    else:
        title_text = f"Alternative routes: {start_city} to {end_city}\n{len(all_paths)} paths found"

    plt.title(
        title_text,
        fontsize=16,
        fontweight='bold',
        pad=20,
        color='#2c3e50'
    )

    # Create legend
    legend_elements = [
        mpatches.Patch(facecolor='#2ecc71', edgecolor='#2c3e50', label='Starting city', linewidth=2),
        mpatches.Patch(facecolor='#e74c3c', edgecolor='#2c3e50', label='Ending city', linewidth=2),
        mpatches.Patch(facecolor='#f39c12', edgecolor='#2c3e50', label='Path cities', linewidth=2),
        mpatches.Patch(facecolor='#95a5a6', edgecolor='#2c3e50', label='Other cities', linewidth=2),
    ]

    # Add paths to legend
    path_labels = ['Optimal', 'Alternative 1', 'Alternative 2']
    for i, path in enumerate(all_paths[:3]):
        legend_elements.append(
            plt.Line2D([0], [0], color=path_colors[i], linewidth=4 if i == 0 else 3,
                      label=f'Path {path_labels[i]}')
        )

    legend_elements.append(
        plt.Line2D([0], [0], color='#bdc3c7', linewidth=1, label='Other routes')
    )

    ax.legend(
        handles=legend_elements,
        loc='upper left',
        fontsize=10,
        frameon=True,
        fancybox=True,
        shadow=True,
        bbox_to_anchor=(0.02, 0.98)
    )

    plt.axis('off')
    plt.tight_layout()

    # 7. Save image to buffer and encode for web
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    plt.close()

    # Encode image data as base64 string
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')

    return image_base64