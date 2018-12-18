import networkx as nx
import sys


def create_graph(graph_size):
    """
    :param graph_size: size of maximal polyomino from which we derive the output graph
    :return: graph induced by the square lattice
    """
    square_lattice = nx.Graph()
    graph_size = int(graph_size)
    # creating nodes and edges of first row of the graph
    first_line_path = []
    for x in range(0, graph_size):
        node = (x, 0)
        square_lattice.add_node(node)
        first_line_path.append(node)
        square_lattice.add_path(first_line_path)
    # adding the rest of the nodes of the induced graph
    for y in range(1, graph_size):
        path = []
        for x in range(-(graph_size - 1 - y), graph_size - y):
            node = (x, y)
            path.append(node)
            square_lattice.add_node(node)
        square_lattice.add_path(path)
    # adding the rest of the edges of the induced graph
    for x in range(-graph_size, graph_size):
        path = []
        for y in range(-graph_size, graph_size):
            if square_lattice.has_node((x, y)):
                node = (x, y)
                path.append(node)
        square_lattice.add_path(path)
    return square_lattice


def count_subgraphs_up_to_given_size(graph, size, maximal_size, untried_set, added_in_lattice):
    """
    :param graph: square lattice - the graph on which we want to count the amount of subraphs up to given size
    :param size: maximal size of polyomino in the square lattice - maximal subgraph size
    :param maximal_size: maximal polyomino allowed size in the square lattice
    :param untried_set: set of elements that have not been in the square lattice
    :param added_in_lattice: list of cells in square lattice
    :return: amount of fixed polyominoes up to given size <size>. This is the actual Redelmeier's algorithm.
    """
    num_elements = [0] * maximal_size
    while len(untried_set) != 0:
        random_element = untried_set[0]  # taking the *first* element of the list
        untried_set = untried_set[1:]  # step 1
        polyomino_cells_before_new_element_in_lattice = added_in_lattice.copy()
        if random_element not in added_in_lattice:
            added_in_lattice.append(random_element)  # Step 2
            num_elements[size] += 1  # Step 3
        new_element_neighbours = graph.neighbors(random_element)
        relevant_to_add = []
        for neighbour in new_element_neighbours:
            is_valid = 1
            for cell in polyomino_cells_before_new_element_in_lattice:
                if graph.has_edge(neighbour, cell) or neighbour == cell:
                    is_valid = 0
                    break
            if is_valid:
                relevant_to_add.append(neighbour)
        if size + 1 < maximal_size:  # Step 4
            new_in_untried_set = []
            for node in relevant_to_add:
                untried_set.append(node)  # (a) - adding node at *end* of the list
                new_in_untried_set.append(node)
            ret = count_subgraphs_up_to_given_size(graph, size + 1, maximal_size, untried_set,
                                                   added_in_lattice)  # (b)
            num_elements = [num_elements[i] + ret[i] for i in range(maximal_size)]
            for n in new_in_untried_set:
                untried_set.remove(n)  # (c)
        added_in_lattice.remove(random_element)  # Step 5
    return num_elements


def main(maximal_size):
    graph = create_graph(maximal_size)
    res = count_subgraphs_up_to_given_size(graph, 0, int(maximal_size), [(0, 0)], [])
    print(res)
    return res


if __name__ == "__main__":
    main(sys.argv[1])
