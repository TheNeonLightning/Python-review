import random


def path_search(height, width, walls_h, walls_v, maze):  # поиск пути на основе DFS, отличие только в том, что мы
    # смотрим куда можно попасть по уже готовым массивам стен
    visited = []
    for i in range(width * height):
        visited.append(0)
    buffer = [0]
    visited[0] = 1
    while (len(buffer) != 0):
        current = int(buffer[len(buffer) - 1])
        if current == height * width - 1:
            break
        next = path_search_dfs_next_iteration(buffer, visited, current, width, height, walls_h, walls_v)
        if next is None:
            continue
        visited[next] = 1
        buffer.append(next)
    for i in range(len(buffer)):
        index1 = buffer[i] % width
        index2 = int(buffer[i] / width)
        index1 = index1 * 2 + 1
        index2 = index2 * 2 + 1
        maze[index2][index1] = '**'
    maze[1][1] = 's '
    maze[height * 2 - 1][width * 2 - 1] = ' f'
    for first in range(height * 2 + 1):
        for second in range(width * 2 + 1):
            print(maze[first][second], end='')
        print()
    return maze


def path_search_dfs_next_iteration(buffer, visited, current, width, height, walls_h, walls_v):
    possible_iteration = []
    if current % width + 1 != width:
        if visited[current + 1] == 0:
            if walls_h.count((current, current + 1)) == 0:
                possible_iteration.append(current + 1)
    if current // width + 1 != height:
        if visited[current + width] == 0:
            if walls_v.count((current, current + width)) == 0:
                possible_iteration.append(current + width)
    if current % width != 0:
        if visited[current - 1] == 0:
            if walls_h.count((current - 1, current)) == 0:
                possible_iteration.append(current - 1)
    if current // width != 0:
        if visited[current - width] == 0:
            if walls_v.count((current - width, current)) == 0:
                possible_iteration.append(current - width)
    if len(possible_iteration) >= 2:
        next = random.choice(possible_iteration)
    else:
        if len(possible_iteration) == 1:
            next = possible_iteration[0]
        else:
            buffer.pop()
            next = None
    return next
