def dijkstra(graph, start_city, end_city):
    """
    Dijkstra's algorithm to find the shortest path between two cities.

    Returns:
        tuple: (total_distance, path) where path is a list of cities
    """
    distances = {city: float('inf') for city in graph}
    distances[start_city] = 0
    predecessors = {city: None for city in graph}
    visited = set()

    while len(visited) < len(graph):
        current_city = None
        current_distance = float('inf')

        for city in graph:
            if city not in visited and distances[city] < current_distance:
                current_city = city
                current_distance = distances[city]

        if current_city is None:
            break

        visited.add(current_city)
        for neighbor, weight in graph[current_city].items():
            new_distance = distances[current_city] + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_city

    path = []
    current = end_city

    while current is not None:
        path.append(current)
        if current == start_city:
            break
        current = predecessors[current]

    if path[-1] != start_city:
        return float('inf'), []

    return distances[end_city], path[::-1]


def _remove_edge(graph, u, v):
    """
    Temporarily removes edge u → v and returns its weight.

    Returns:
        float: The weight of the removed edge, or None if the edge doesn't exist
    """
    if v in graph[u]:
        weight = graph[u][v]
        del graph[u][v]
        return weight
    return None


def _restore_edge(graph, u, v, weight):
    """
    Restores a previously removed edge.

    """
    if weight is not None:
        graph[u][v] = weight


def _path_distance(graph, path):
    """
    Calculate the total distance of a path by summing edge weights.

    Returns:
        float: The total distance of the path
    """
    distance = 0
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        if v in graph[u]:
            distance += graph[u][v]
        else:
            return float('inf')
    return distance


def is_path_different(new_path, existing_paths, similarity_threshold=0.7):
    """
    Checks if a new path is sufficiently different from existing paths.

    Principle: A path is considered different if less than 70% of its edges
    are common with an already found path.

    Returns:
        bool: True if the path is sufficiently different, False otherwise
    """
    new_edges = set()
    for i in range(len(new_path) - 1):
        edge = tuple(sorted([new_path[i], new_path[i + 1]]))
        new_edges.add(edge)

    for _, existing_path in existing_paths:
        if new_path == existing_path:
            return False

        existing_edges = set()
        for i in range(len(existing_path) - 1):
            edge = tuple(sorted([existing_path[i], existing_path[i + 1]]))
            existing_edges.add(edge)

        if len(new_edges) == 0:
            continue

        shared_edges = new_edges.intersection(existing_edges)
        similarity_rate = len(shared_edges) / len(new_edges)

        if similarity_rate >= similarity_threshold:
            return False

    return True


def k_shortest_paths(graph, start_city, end_city, k=5, max_ratio=1.5):
    """
    Computes the k shortest simple paths between two cities using
    Yen's algorithm (without NetworkX).

    Returns:
        list: List of tuples (distance, path) sorted by increasing distance
    """
    optimal_distance, optimal_path = dijkstra(graph, start_city, end_city)

    if not optimal_path or optimal_distance == float('inf'):
        return []

    valid_paths = [(optimal_distance, optimal_path)]
    candidate_paths = []

    for iteration in range(1, k):
        _, previous_path = valid_paths[-1]

        for i in range(len(previous_path) - 1):
            deviation_node = previous_path[i]
            root_path = previous_path[:i + 1]
            removed_edges = []

            for _, existing_path in valid_paths:
                if len(existing_path) > i and existing_path[:i + 1] == root_path:
                    if i + 1 < len(existing_path):
                        u = existing_path[i]
                        v = existing_path[i + 1]
                        weight = _remove_edge(graph, u, v)
                        if weight is not None:
                            removed_edges.append((u, v, weight))

            for _, candidate_path in candidate_paths:
                if len(candidate_path) > i and candidate_path[:i + 1] == root_path:
                    if i + 1 < len(candidate_path):
                        u = candidate_path[i]
                        v = candidate_path[i + 1]
                        weight = _remove_edge(graph, u, v)
                        if weight is not None:
                            removed_edges.append((u, v, weight))

            removed_root_nodes = []
            for j in range(i):
                node = root_path[j]
                for neighbor in list(graph[node].keys()):
                    weight = _remove_edge(graph, node, neighbor)
                    if weight is not None:
                        removed_root_nodes.append((node, neighbor, weight))

            deviation_distance, deviation_path = dijkstra(graph, deviation_node, end_city)

            for u, v, weight in removed_root_nodes:
                _restore_edge(graph, u, v, weight)

            for u, v, weight in removed_edges:
                _restore_edge(graph, u, v, weight)

            if deviation_path and deviation_distance < float('inf'):
                total_path = root_path[:-1] + deviation_path

                if len(total_path) == len(set(total_path)):
                    total_distance = _path_distance(graph, total_path)

                    if total_distance <= optimal_distance * max_ratio:
                        if is_path_different(total_path, valid_paths):
                            path_already_present = False
                            for _, candidate in candidate_paths:
                                if candidate == total_path:
                                    path_already_present = True
                                    break

                            if not path_already_present:
                                candidate_paths.append((total_distance, total_path))

        if not candidate_paths:
            break

        candidate_paths.sort(key=lambda x: x[0])
        best_candidate = candidate_paths.pop(0)
        valid_paths.append(best_candidate)

    return valid_paths
