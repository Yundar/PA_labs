import random
import copy


def create_graph(tops_number):
    graph = [[0 for i in range(tops_number)] for j in range(tops_number)]
    for i in range(len(graph)):
        for j in range(len(graph)):
            if i == j:
                graph[i][i] = float('inf')
            else:
                path = random.randrange(5, 50)
                graph[i][j] = path
                graph[j][i] = path
    return graph


def find_lmin(oriented_graph, top):
    visited_tops = []
    copy_graph = copy.deepcopy(oriented_graph)
    min_element = min(copy_graph[top])
    min_path = min_element
    visited_tops.append(top)
    ind = copy_graph[top].index(min_element)
    for i in range(len(copy_graph)):
        copy_graph[top][i], copy_graph[i][top] = float('inf'), float('inf')
    while len(visited_tops) != len(copy_graph):
        if len(visited_tops) == len(copy_graph) - 1:
            previous_top = ind
            visited_tops.append(previous_top)
            min_element = oriented_graph[ind][top]
            min_path += min_element
        else:
            previous_top = ind
            visited_tops.append(previous_top)
            min_element = min(copy_graph[ind])
            min_path += min_element
            ind = copy_graph[ind].index(min_element)
            for i in range(len(copy_graph)):
                copy_graph[previous_top][i], copy_graph[i][previous_top] = float('inf'), float('inf')
    return min_path


graph = create_graph(5)
for i in graph:
    print(i)
a = find_lmin(graph, 0)
print(a)


