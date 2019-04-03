# генератор лабиринтов (Еременко Илья Б05-831)
import random

def maze_builder(height, width, walls_h, walls_v):
    maze = [['  '] * (width * 2 + 1) for i in range(height * 2 + 1)]  # после прохода получаем два массива вертикальных
    # и горизонтальных стен: по ним строи "изображение" лабиринта (со стенами [])
    # далее идёт работа с индексами
    for i in range(height * 2 + 1):
        for j in range(width * 2 + 1):
            if i == 0 or i == height * 2 or j == 0 or j == width * 2:
                maze[i][j] = '[]'
                continue
            if i % 2 == 0 and j % 2 == 0:
                maze[i][j] = '[]'
                continue
            if i % 2 == 0:
                up = i - 1
                down = i + 1
                up = int((up - 1) / 2)
                down = int((down - 1) / 2)
                number = int((j - 1) / 2)
                up = int(up * width + number)
                down = int(down * width + number)
                if walls_v.count((up, down)) > 0:
                    maze[i][j] = '[]'
                else:
                    maze[i][j] = '  '
                continue
            if j % 2 == 0:
                left = j - 1
                right = j + 1
                left = int((left - 1) / 2)
                right = int((right - 1) / 2)
                number = int((i - 1) / 2)
                left = int(number * width + left)
                right = int(number * width + right)
                if walls_h.count((left, right)) > 0:
                    maze[i][j] = '[]'
                else:
                    maze[i][j] = '  '
    maze[1][1] = 's '
    maze[height * 2 - 1][width * 2 - 1] = ' f'
    for i in range(height * 2 + 1):
        for j in range(width * 2 + 1):
            print(maze[i][j], end='')
        print()
    return maze

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
    buffer = [0]
    possible_iteration = []
    visited[0] = 1
    while(len(buffer) != 0):  # затем проходим DFS по непосещённым клеткам,
        # параллельно убирая стены, через которые проходим
        current = int(buffer[len(buffer) - 1])
        if current % width + 1 != width:  # для каждого возможного шага проверяем возможность выхода за границу
            if visited[current + 1] == 0:  # и смотрим был ли уже посещён элемент
                possible_iteration.append(current + 1)
        if int(current / width) + 1 != height:
            if visited[current + width] == 0:
                possible_iteration.append(current + width)
        if current % width != 0:
            if visited[current - 1] == 0:
                possible_iteration.append(current - 1)
        if int(current / width) != 0:
            if visited[current - width] == 0:
                possible_iteration.append(current - width)
        if len(possible_iteration) >= 2:  # из возможных вариантов случайным образом выбираем куда идти дальше
            next = random.choice(possible_iteration)
        else:
            if len(possible_iteration) == 1:  # если от текущего элемента нет возможности попасть в непосещённые клетки,
                # спускаемся по стеку, выкидывая элементы, пока не найдем элемент, с ещё непосещёнными соседями
                next = possible_iteration[0]
            else:
                buffer.pop()
                continue
        visited[next] = 1
        buffer.append(next)
        possible_iteration.clear()
        if current < next:
            pair = (current, next)
        else:
            pair = (next, current)
        if walls_h.count(pair) > 0:
            walls_h.remove(pair)
        else:
            walls_v.remove(pair)
    return maze_builder(height, width, walls_h, walls_v)


def maze_generator_eller(height, width, walls_h, walls_v):  # основывается на построчном создании лабиринта: в
    # зависимости от взаимосвязей элементов прошлой строки, ставятся некотрые рамки на конфигурацию следующей;
    # по возможности используется random
    line = [i for i in range(width)]
    current_line = [i for i in range(width)]
    for line_number in range(height - 1):
        blocks = []
        vertical_borders = [0 for j in range(width)]
        size = 0
        for i in range(width - 1):
            if current_line[i] != current_line[i + 1]:
                choice = random.randint(0, 1)
                if choice == 0:
                    current_line[i + 1] = current_line[i]
                    size += 1
                else:
                    walls_h.append((line[i], line[i + 1]))
                    blocks.append(size)
                    size = 0
            else:
                walls_h.append((line[i], line[i + 1]))
                size += 1
        blocks.append(size)
        current = current_line[0]
        index = 0
        for i in range(width):
            if current_line[i] == current:
                if blocks[index] > 0:
                    choice = random.randint(0, 1)
                    if choice == 1:
                        blocks[index] -= 1
                        walls_v.append((line[i], line[i] + width))
                        vertical_borders[i] = 1
            else:
                current = current_line[i]
                index += 1
                if blocks[index] > 0:
                    choice = random.randint(0, 1)
                    if choice == 1:
                        blocks[index] -= 1
                        walls_v.append((line[i], line[i] + width))
                        vertical_borders[i] = 1
        choice_pool = [1 for i in range(width)]
        possible = []
        for i in range(width):
            choice_pool[current_line[i]] = 0
        for i in range(width):
            if choice_pool[i] == 1:
                possible.append(i)
        for i in range(width):
            line[i] = line[i] + width
            if vertical_borders[i] == 1:
                current_line[i] = possible[len(possible) - 1]
                possible.pop()
    for i in range(width - 1):
        if current_line[i] == current_line[i + 1]:
            choice = random.randint(0, 1)
            if choice == 1:
                walls_h.append((line[i], line[i + 1]))
    return maze_builder(height, width, walls_h, walls_v)


def path_search(height, width, walls_h, walls_v, maze):  # поиск пути на основе DFS, отличие только в том, что мы смотрим
    # куда можно попасть по уже готовым массивам стен
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
        maze = maze_generator_dfs(height, width, walls_h, walls_v)
    else:
        maze = maze_generator_eller(height, width, walls_h, walls_v)
    print("Для вывода решения введите 0, для сохранения лабиринта в фаил 1, для простого завершения работы 2")
    option = int(input())
    if option == 0:
        path_search(height, width, walls_h, walls_v, maze)
    else:
        if option == 1:
            file = open('Maze.txt', 'w')
            for i in range(height * 2 + 1):
                for j in range(width * 2 + 1):
                    file.write(maze[i][j])
                file.write('\n')
            file.close()
    exit()
else:
    print("Введите адрес фаила")
    string = str(input())
    file = open(string, 'r')
    width = 0
    height = 0
    for line in file:
        width = len(line) - 3
        break
    file.close()
    file = open(string, 'r')
    for line in file:
        height += 1
    file.close()
    height = int((height - 1) / 2)
    file = open(string, 'r')
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
    file.close()
    width = int(width / 4)
    print("Считанный лабириант:")
    maze = maze_builder(height, width, walls_h, walls_v)
    print("Решение:")
    path_search(height, width, walls_h, walls_v, maze)
exit()
