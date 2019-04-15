# генератор лабиринтов (Еременко Илья Б05-831)
import random
import maze_builder
import generator_dfs
import generator_eller


def path_search(height, width, walls_h, walls_v, maze):  # поиск пути на основе DFS, отличие только в том, что мы
    # смотрим куда можно попасть по уже готовым массивам стен
    visited = []
    for i in range(width * height):
        visited.append(0)
    buffer = [0]
    possible_iteration = []
    visited[0] = 1
    while (len(buffer) != 0):
        current = int(buffer[len(buffer) - 1])
        if current == height * width - 1:
            break
        if current % width + 1 != width:
            if visited[current + 1] == 0:
                if walls_h.count((current, current + 1)) == 0:
                    possible_iteration.append(current + 1)
        if int(current / width) + 1 != height:
            if visited[current + width] == 0:
                if walls_v.count((current, current + width)) == 0:
                    possible_iteration.append(current + width)
        if current % width != 0:
            if visited[current - 1] == 0:
                if walls_h.count((current - 1, current)) == 0:
                    possible_iteration.append(current - 1)
        if int(current / width) != 0:
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
                continue
        visited[next] = 1
        buffer.append(next)
        possible_iteration.clear()
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


walls_h = []
walls_v = []
print("Сгенерировать новый лабиринт или загрузить лабиринт из фаила: 0/1")
option = int(input())
if option == 0:
    print("Введите высоту лабиринта")
    height = int(input())
    print("Введите ширину лабиринта")
    width = int(input())
    print("Выберите метод генерации лабиринта: 0 или 1 (DFS или Eller's Algorythm)")
    option = int(input())
    if option == 0:
        maze = generator_dfs.maze_generator_dfs(height, width, walls_h, walls_v)
    else:
        maze = generator_eller.maze_generator_eller(height, width, walls_h, walls_v)
    print("Для вывода решения введите 0, для сохранения лабиринта в фаил 1, для простого завершения работы 2")
    option = int(input())
    if option == 0:
        path_search(height, width, walls_h, walls_v, maze)
    elif option == 1:
        file = open('Maze.txt', 'w')
        for i in range(height * 2 + 1):
            for j in range(width * 2 + 1):
                file.write(maze[i][j])
            file.write('\n')
        file.close()
    exit()
else:
    print("Введите адрес фаила")
    string = input()
    with open(string, 'r') as file:  # file = open(string, 'r')
        width = 0
        height = 0
        for line in file:
            width = len(line) - 3
            break
    with open(string, 'r') as file:
        for line in file:
            height += 1
    height = int((height - 1) / 2)
    with open(string, 'r') as file:
        index = 0
        for line in file:
            if index % 2 == 1:
                for i in range(4, width, 4):
                    if line[i] == '[':
                        walls_h.append((int(i / 4) - 1 + int((index - 1) / 2) * int(width / 4), int(i / 4) + int((index - 1)
                                                                                                                 / 2) *
                                        int(width / 4)))
            if index % 2 == 0 and index != height - 1 and index != 0:
                for i in range(2, width, 4):
                    if line[i] == '[':
                        walls_v.append((int((index - 1) / 2) * int(width / 4) + int(i / 4), int((index - 1) / 2) * int(width
                                                                                                                       / 4)
                                        + int(i / 4) + int(width / 4)))
            index += 1
    width = int(width / 4)
    print("Считанный лабириант:")
    maze = maze_builder.maze_builder(height, width, walls_h, walls_v)
    print("Решение:")
    path_search(height, width, walls_h, walls_v, maze)
exit()