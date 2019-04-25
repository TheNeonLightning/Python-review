# Далее выделена часть, которая выполняет построение лабиринта методом обхода в глубину
import random
import maze_builder


def maze_generator_dfs(height, width,  walls_h, walls_v):  # метод генерации на основе DFS
    visited = [0 for index in range(width * height)]
    for index in range(width * height):
        if (index % width) + 1 != width:
            walls_h.append((index, index + 1))  # walls_h и walls_v - два массива для хранения пар индексов: индексов,
            # между которыми есть стена (вертикальная или горизонтальная)
    for i in range(width * height):  # первоначально заполнеяем оба массива всеми возможными стенами
        if (i / width) + 1 == height:
            break
        walls_v.append((i, i + width))
    buffer = [0]  # стек, в ктором хранятся вершины из которых ещё не вышли
    visited[0] = 1
    while(len(buffer) != 0):  # затем проходим DFS по непосещённым клеткам,
        # параллельно убирая стены, через которые проходим
        current = int(buffer[len(buffer) - 1])  # берём последнюю посещённую
        next = maze_generator_dfs_next_iteration(buffer, visited, current, width, height)  # вызываяем функцию для поиска следующего шага
        if next is None:  # если от текущего элемента нет возможности попасть в непосещённые клетки,
            # спускаемся по стеку, рассмотрим соседей других элементов
            continue
        buffer.append(next)
        visited[next] = 1
        if current < next:  # в качестве стен считаю пары, в определённом порядке: например стена между 3 и 4 это (3,4), а не (4, 3)
            pair = current, next
        else:
            pair = next, current
        if walls_h.count(pair) > 0:  # удаляю выбранную стену
            walls_h.remove(pair)
        else:
            walls_v.remove(pair)
    return maze_builder.maze_builder(height, width, walls_h, walls_v)


def maze_generator_dfs_next_iteration(buffer, visited, current, width, height):
    possible_iteration = []  # массив, который заполняем возможными вариантами следующего шага
    if current % width + 1 != width:  # для каждого возможного шага проверяем возможность выхода за границу
        if visited[current + 1] == 0:  # и смотрим был ли уже посещён элемент, здесь это шаг вправо
            possible_iteration.append(current + 1)
    if int(current / width) + 1 != height:
        if visited[current + width] == 0:  # шаг вниз
            possible_iteration.append(current + width)
    if current % width != 0:
        if visited[current - 1] == 0:  # шаг вниз
            possible_iteration.append(current - 1)
    if int(current / width) != 0:
        if visited[current - width] == 0:  # шаг вверх
            possible_iteration.append(current - width)
    if len(possible_iteration) >= 2:  # из возможных вариантов случайным образом выбираем куда идти дальше
        next = random.choice(possible_iteration)
    else:
        if len(possible_iteration) == 1:  # если от текущего элемента нет возможности попасть в непосещённые клетки,
            # спускаемся по стеку, выкидывая элементы, пока не найдем элемент, с ещё непосещёнными соседями
            next = possible_iteration[0]
        else:
            buffer.pop()
            return None
    return next
