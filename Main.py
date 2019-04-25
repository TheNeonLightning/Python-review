# генератор лабиринтов (Еременко Илья Б05-831)
import maze_builder
import generator_dfs
import generator_eller
import path_search


walls_h = []
walls_v = []
try:
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
            path_search.path_search(height, width, walls_h, walls_v, maze)
        elif option == 1:
            with open('Maze.txt', 'w') as file:
                for i in range(height * 2 + 1):
                    for j in range(width * 2 + 1):
                        file.write(maze[i][j])
                    file.write('\n')
    else:
        print("Введите адрес фаила")
        filename = input()
        try:
            with open(filename, 'r') as file:
                width = 0
                height = 0
                for line in file:
                    width = len(line) - 3
                    break
                file.seek(0)
                for line in file:
                    height += 1
                height = (height - 1) // 2
                file.seek(0)
                index = 0
                for line in file:
                    if index % 2 == 1:
                        for i in range(4, width, 4):
                            if line[i] == '[':
                                walls_h.append(((i // 4) - 1 + (index - 1) // 2 * width // 4, i // 4 + (index - 1) // 2 *
                                                width // 4))
                    if index % 2 == 0 and index != height - 1 and index != 0:
                        for i in range(2, width, 4):
                            if line[i] == '[':
                                walls_v.append((((index - 1) // 2) * (width // 4) + (i // 4), ((index - 1) // 2) * (width // 4)
                                                + (i // 4) + (width // 4)))
                    index += 1
                width = width // 4
            print("Считанный лабириант:")
            maze = maze_builder.maze_builder(height, width, walls_h, walls_v)
            print("Решение:")
            path_search.path_search(height, width, walls_h, walls_v, maze)
        except FileNotFoundError:
            print("Фаил с указанным адресом не найден, работа прекращена")
except ValueError:
    print("Неверно введён выбраный вариант, работа прекращена")
