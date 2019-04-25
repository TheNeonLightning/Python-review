def maze_builder(height, width, walls_h, walls_v):
    maze = [['  '] * (width * 2 + 1) for i in range(height * 2 + 1)]  # после прохода получаем два массива вертикальных
    # и горизонтальных стен: по ним строим "изображение" лабиринта (со стенами [])
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
                up = (up - 1) // 2
                down = (down - 1) // 2
                number = (j - 1) // 2
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
                left = (left - 1) // 2
                right = (right - 1) // 2
                number = (i - 1) // 2
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
