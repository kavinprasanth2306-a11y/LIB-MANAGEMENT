"""
Learning Unit V: Graph Theory
- Library Knowledge & Recommendation Graph
  * Vertices: Books, Students, Topics/Categories
  * Edges: "co-borrowed", "same-genre", "prerequisite"
- Representations:
  * Adjacency List (Node -> List of Neighbors with Edge weights/labels)
  * Adjacency Matrix (2D grid of connection weights)
- Graph Algorithms:
  * Breadth-First Search (BFS): Shortest-hop book recommendations ("Readers who borrowed X also borrowed...")
  * Depth-First Search (DFS): Deep topic/prerequisite exploration and connected component analysis
Implemented strictly from scratch using custom queues/stacks without collections or built-in dicts for core traversal.
"""

from .unit1_linear import Queue, Stack

class GraphNode:
    def __init__(self, node_id: str, label: str, node_type: str = "book", metadata=None):
        self.node_id = node_id
        self.label = label
        self.node_type = node_type  # 'book', 'student', 'category'
        self.metadata = metadata if metadata is not None else {}


class GraphEdge:
    def __init__(self, src: str, dst: str, relation: str = "co-borrowed", weight: float = 1.0):
        self.src = src
        self.dst = dst
        self.relation = relation
        self.weight = weight


class Graph:
    """
    Custom Library Knowledge & Recommendation Graph.
    Supports vertices, directed/undirected edges, adjacency list, adjacency matrix,
    BFS recommendations, DFS path chains, and connected components.
    """
    def __init__(self, directed: bool = False):
        self.directed = directed
        self.nodes = []       # list of GraphNode
        self.edges = []       # list of GraphEdge
        # Adjacency list stored as list of tuples (node_id, list_of_edges)
        self._adj_list = []

    def _find_node_idx(self, node_id: str) -> int:
        for i in range(len(self.nodes)):
            if self.nodes[i].node_id == node_id:
                return i
        return -1

    def add_node(self, node_id: str, label: str, node_type: str = "book", metadata=None) -> bool:
        if self._find_node_idx(node_id) != -1:
            return False
        node = GraphNode(node_id, label, node_type, metadata)
        self.nodes.append(node)
        self._adj_list.append((node_id, []))
        return True

    def add_edge(self, src: str, dst: str, relation: str = "co-borrowed", weight: float = 1.0):
        if self._find_node_idx(src) == -1 or self._find_node_idx(dst) == -1:
            return False

        edge = GraphEdge(src, dst, relation, weight)
        self.edges.append(edge)

        # Add to src adj list
        for node_id, edge_list in self._adj_list:
            if node_id == src:
                edge_list.append(edge)
                break

        if not self.directed:
            rev_edge = GraphEdge(dst, src, relation, weight)
            for node_id, edge_list in self._adj_list:
                if node_id == dst:
                    edge_list.append(rev_edge)
                    break
        return True

    def get_neighbors(self, node_id: str):
        for nid, edge_list in self._adj_list:
            if nid == node_id:
                return edge_list
        return []

    def get_adjacency_list_repr(self):
        result = []
        for nid, edge_list in self._adj_list:
            node_idx = self._find_node_idx(nid)
            node_label = self.nodes[node_idx].label if node_idx != -1 else nid
            neighbors = []
            for edge in edge_list:
                dst_idx = self._find_node_idx(edge.dst)
                dst_label = self.nodes[dst_idx].label if dst_idx != -1 else edge.dst
                neighbors.append({
                    "target_id": edge.dst,
                    "target_label": dst_label,
                    "relation": edge.relation,
                    "weight": edge.weight
                })
            result.append({
                "node_id": nid,
                "label": node_label,
                "neighbors": neighbors
            })
        return result

    def get_adjacency_matrix_repr(self):
        n = len(self.nodes)
        matrix = [[0.0] * n for _ in range(n)]

        for edge in self.edges:
            src_idx = self._find_node_idx(edge.src)
            dst_idx = self._find_node_idx(edge.dst)
            if src_idx != -1 and dst_idx != -1:
                matrix[src_idx][dst_idx] = edge.weight
                if not self.directed:
                    matrix[dst_idx][src_idx] = edge.weight

        labels = [node.label for node in self.nodes]
        node_ids = [node.node_id for node in self.nodes]

        return {
            "node_ids": node_ids,
            "labels": labels,
            "matrix": matrix
        }

    def bfs_recommendations(self, start_id: str, max_depth: int = 2):
        """
        Breadth-First Search:
        Finds shortest-hop recommendations for books borrowed by peers.
        Returns traversal steps, queue states, and discovered books grouped by hop distance.
        """
        start_idx = self._find_node_idx(start_id)
        if start_idx == -1:
            return {"error": f"Node {start_id} not found"}

        visited = []
        queue = Queue(50)
        # Store tuple: (node_id, depth, parent_id)
        queue.enqueue((start_id, 0, None))
        visited.append(start_id)

        traversal_steps = []
        recommendations = []

        step_counter = 0
        while not queue.is_empty():
            curr_id, depth, parent = queue.dequeue()
            step_counter += 1

            curr_node = self.nodes[self._find_node_idx(curr_id)]
            traversal_steps.append({
                "step": step_counter,
                "current_id": curr_id,
                "label": curr_node.label,
                "depth": depth,
                "parent": parent,
                "queue_snapshot": [item[0] for item in queue.to_list()]
            })

            if depth > 0 and curr_id != start_id and curr_node.node_type == "book":
                recommendations.append({
                    "node_id": curr_id,
                    "label": curr_node.label,
                    "hops": depth,
                    "recommended_via": parent,
                    "metadata": curr_node.metadata
                })

            if depth < max_depth:
                neighbors = self.get_neighbors(curr_id)
                for edge in neighbors:
                    neighbor_id = edge.dst
                    # Check if already visited
                    is_vis = False
                    for v in visited:
                        if v == neighbor_id:
                            is_vis = True
                            break
                    if not is_vis:
                        visited.append(neighbor_id)
                        queue.enqueue((neighbor_id, depth + 1, curr_node.label))

        return {
            "start_id": start_id,
            "start_label": self.nodes[start_idx].label,
            "max_depth": max_depth,
            "traversal_steps": traversal_steps,
            "recommendations": recommendations,
            "total_visited": len(visited)
        }

    def dfs_exploration(self, start_id: str):
        """
        Depth-First Search:
        Deep prerequisite / topic chain traversal using custom Stack.
        Returns path trace, discovery order, and backtrack events.
        """
        start_idx = self._find_node_idx(start_id)
        if start_idx == -1:
            return {"error": f"Node {start_id} not found"}

        visited = []
        stack = Stack(50)
        stack.push(start_id)

        traversal_steps = []
        exploration_order = []
        step_counter = 0

        while not stack.is_empty():
            curr_id = stack.pop()
            # check visited
            is_vis = False
            for v in visited:
                if v == curr_id:
                    is_vis = True
                    break

            if not is_vis:
                visited.append(curr_id)
                step_counter += 1
                curr_node = self.nodes[self._find_node_idx(curr_id)]
                exploration_order.append(curr_node.label)

                traversal_steps.append({
                    "step": step_counter,
                    "action": "Visit Node",
                    "node_id": curr_id,
                    "label": curr_node.label,
                    "stack_snapshot": [item for item in stack.to_list()]
                })

                # Push neighbors to stack in reverse for canonical order
                neighbors = self.get_neighbors(curr_id)
                for i in range(len(neighbors) - 1, -1, -1):
                    neighbor_id = neighbors[i].dst
                    already_seen = False
                    for v in visited:
                        if v == neighbor_id:
                            already_seen = True
                            break
                    if not already_seen:
                        stack.push(neighbor_id)

        return {
            "start_id": start_id,
            "start_label": self.nodes[start_idx].label,
            "traversal_steps": traversal_steps,
            "exploration_order": exploration_order,
            "total_explored": len(visited)
        }

    def get_graph_state(self):
        """Returns nodes and links formatted for force-directed graph visualizer."""
        nodes_data = []
        for n in self.nodes:
            nodes_data.append({
                "id": n.node_id,
                "label": n.label,
                "type": n.node_type,
                "metadata": n.metadata
            })
        edges_data = []
        for e in self.edges:
            edges_data.append({
                "source": e.src,
                "target": e.dst,
                "relation": e.relation,
                "weight": e.weight
            })
        return {
            "nodes": nodes_data,
            "edges": edges_data,
            "directed": self.directed
        }

