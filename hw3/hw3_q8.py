from typing import Dict, Set, Tuple, List


def read_data(path: str='hw3/q8-data.txt'):
    vertices = set()
    adjacency_lists = {}
    edge_count = 0

    with open(path, 'r') as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line == '':
                continue
            elif line.startswith('#'):
                continue
            
            components = line.split(',')
            components = [c.strip() for c in components]
            if len(components) == 1:
                vertices.add(components[0])
            elif len(components) == 3:
                
                start, end, dist = components

                if start not in vertices:
                    raise ValueError(f"Invalid line {i}: {start} not declared as a vertex")
                if end not in vertices:
                    raise ValueError(f"Invalid line {i}: {end} not declared as a vertex")

                if (dist.endswith("mi")) and dist[:-2].isdigit():
                    dist = float(dist[:-2])

                    if not start in adjacency_lists:
                        adjacency_lists[start] = [(end, dist)]
                    adjacency_lists[start].append((end, dist))

                    if not end in adjacency_lists:
                        adjacency_lists[end] = [(start, dist)]
                    adjacency_lists[end].append((start, dist))

                    edge_count += 1
                else:
                    raise ValueError(f"Invalid distance: {dist} on line {i+1}")
            
            else:
                raise ValueError(f"Invalid Line (Line {i+1}): {line}")
    
    return vertices, adjacency_lists, edge_count

def prims_find_mst(vertices: Set[str], adjacency_lists: Dict[str, List[Tuple[str, float]]]):

    from queue import PriorityQueue

    # pick a random vertex to start with
    start_vertex = next(iter(vertices)) 
    mst_vertices = set([start_vertex])

    # We'll create a priority queue to store the edges that go 
    # outward from current set
    candidate_edges = PriorityQueue()
    for neighbor_vertex, dist in adjacency_lists[start_vertex]:
        candidate_edges.put((dist, start_vertex, neighbor_vertex))

    vertices_added = 1
    while vertices_added < len(vertices) and not candidate_edges.empty():
        dist, from_v, to_v = candidate_edges.get()

        if to_v not in mst_vertices:
            mst_vertices.add(to_v)
            vertices_added += 1
            yield from_v, to_v, dist

            # Fill the candidate edges queue with edges from the new node
            for neighbor_vertex, dist in adjacency_lists[to_v]:
                if neighbor_vertex not in mst_vertices:
                    candidate_edges.put((dist, to_v, neighbor_vertex))


if __name__ == "__main__":
    from pathlib import Path
    print()
    print("Running script: " + str(Path(__file__).relative_to(Path.cwd())))
    print()
    
    filepath = Path(__file__).parent
    vertices, adjacency_lists, edge_count = read_data(path = str(filepath / 'q8-data.txt'))

    print(f'Data loaded successfully. {len(vertices)} vertices and {edge_count} edges.')
    print()

    print('Computing MST using Prim\'s algorithm...')
    for start_v, end_v, dist in prims_find_mst(vertices, adjacency_lists):
        print(f'\t{start_v} <-> {end_v} : {dist} mi')

    print()
    print('Done.')
    print()

# OUTPUT:
# Lethbridge <-> Calgary : 107.0 mi
# Calgary <-> Golden : 129.0 mi
# Golden <-> Revelstoke : 57.0 mi
# Golden <-> Blue River : 89.0 mi
# Revelstoke <-> Kelowna : 95.0 mi
# Kelowna <-> Vancouver : 167.0 mi
# Calgary <-> Edmonton : 174.0 mi
# Blue River <-> Prince George : 191.0 mi
# Prince George <-> Prince Rupert : 308.0 mi
