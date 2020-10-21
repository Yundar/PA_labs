from graph_lab2 import create_graph, find_lmin
import random

alpha = 2
beta = 4
rho = 0.4
cities_number = 100
distance = create_graph(cities_number)
for i in distance:
    print(i)
best = find_lmin(distance)[0]
best_way = find_lmin(distance)[1]
print(best)
ants_number = 30
init_pheromone = (1 / cities_number)
max_iterations = 1000
pheromone_iter = 100


class Ant:

    def __init__(self, start_city):
        self.cur_city = start_city
        self.path = [start_city]
        self.path_length = 0.

    def move_to_city(self, city):
        global distance, cities_number
        self.path.append(city)
        self.path_length += distance[self.cur_city][city]
        if len(self.path) == cities_number:
            self.path_length += distance[self.path[-1]][self.path[0]]
        self.cur_city = city

    def can_move(self):
        global cities_number
        return len(self.path) < cities_number

    def reset(self, city):
        self.cur_city = city
        self.path = [city]
        self.path_length = 0.


ants = []
pheromone = []
best_ant = None


def init():
    global ants, cities_number, ants_number, pheromone

    for i in range(cities_number):
        pheromone.append([init_pheromone] * cities_number)

    city = random.randrange(0, cities_number - 1)
    city_with_ant = [city]
    for i in range(ants_number):
        ants.append(Ant(city))
        r = random.randrange(0, cities_number - 1)
        while r in city_with_ant:
            r = random.randrange(0, cities_number - 1)
        city = r
        city_with_ant.append(r)


def ant_product(from_city, to_city, ph=None):
    global alpha, beta, distance, pheromone
    ph = ph or pheromone[from_city][to_city]
    return (ph ** alpha) * ((1 / distance[from_city][to_city]) ** beta)


def get_random(l):
    r = random.random()
    cur_probability = 0
    cur_val = None

    for val, probability in l:
        cur_val = val
        cur_probability += probability
        if r <= cur_probability:
            break

    return cur_val


def select_next_city(ant):
    global cities_number, distance, pheromone
    su = 0
    not_visited = []

    for city in range(cities_number):
        if city not in ant.path:
            ap = ant_product(ant.cur_city, city)
            not_visited.append((city, ap))
            su += ap

    assert not_visited
    not_visited = [(val, ap / su) for (val, ap) in not_visited]
    city = get_random(not_visited)
    return city
    i = 0
    while True:
        city, ap = not_visited[i]
        p = ap / su
        if random.random() < p:
            break
        i += 1
        i = i % len(not_visited)
    assert ant.cur_city != city
    return city


def ants_move():
    global ants, cities_number
    moving = 0

    for ant in ants:
        if ant.can_move():
            ant.move_to_city(select_next_city(ant))
            moving += 1

    return moving


def update_trails():
    global cities_number, pheromone, rho, init_pheromone, ants

    for ant in ants:
        pheromone_amount = pheromone_iter / ant.path_length

        for i in range(cities_number):
            if i == cities_number - 1:
                from_city = ant.path[i]
                to_city = ant.path[0]
            else:
                from_city = ant.path[i]
                to_city = ant.path[i + 1]
            assert from_city != to_city
            pheromone[from_city][to_city] = pheromone[from_city][to_city] * (1 - rho) + pheromone_amount
            pheromone[to_city][from_city] = pheromone[from_city][to_city]


def restart_ants():
    global ants, best, best_ant, cities_number
    city = random.randrange(0, cities_number - 1)
    city_with_ant = [city]

    for ant in ants:
        if ant.path_length < best:
            best = ant.path_length
            best_ant = ant
            best_way = ant.path

        ant.reset(city)
        r = random.randrange(0, cities_number - 1)
        while r in city_with_ant:
            r = random.randrange(0, cities_number - 1)
        city = r
        city_with_ant.append(r)


if __name__ == '__main__':
    init()
    cur_iteration = 0
    while cur_iteration < max_iterations:
        cur_iteration += 1
        if cur_iteration % 20 == 0:
            print('iteration:', cur_iteration, 'of', max_iterations)
            print('best result: ', best)

        if ants_move() == 0:
            update_trails()
            cur_iteration != max_iterations and restart_ants()
    print('\n', 'best result: ', best)
    print('best path: ', best_way)
