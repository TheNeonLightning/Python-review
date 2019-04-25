# Далее выделена часть, которая выполняет построение лабиринта методом Эллера (вроде не Эйлера), которая теперь разбита
# на лгически выделенные блоки
import random
import maze_builder


def maze_generator_eller(height, width, walls_h, walls_v):  # основывается на построчном создании лабиринта: в
    # зависимости от взаимосвязей элементов прошлой строки, ставятся некотрые рамки на конфигурацию следующей;
    # по возможности используется random
    line = [i for i in range(width)]  # выполняет роль индексов, для корректного построения стен:
    # допустим ширина 5, высота 2, тогда на первой итерации line = [0, 1, 2, 3, 4]
    # на второй line = [5, 6, 7, 8, 9] и т.д. Добавляя стены сразу смортим на line, между какими индексами будет
    # расположена стена
    current_line = [i for i in range(width)]  # выполняет роль множеств, если элементы строки лежат в одном множестве,
    # то между ними нет стены и наоборот, между двумя элементами есть стена, если они из разных множеств (верно для
    # строки => стены, о которых идёт речь горизонтальные)
    for line_number in range(height - 1):  # построчно проходим, строя лабиринт
        blocks = []  # размеры множеств из current_line
        vertical_borders = [0 for j in range(width)]  # для каждого элемента строки: 0 если под ним нет стены, 1 если
        # есть (а вернее будет)
        maze_generator_eller_horizontal_walls(line, current_line, blocks, width, walls_h)
        maze_generator_eller_vertical_walls(line, current_line, blocks, vertical_borders, width, walls_v)
        maze_generator_eller_next_line_preparation(line, current_line, vertical_borders, width)
    for i in range(width - 1):
        if current_line[i] == current_line[i + 1]:
            choice = random.randint(0, 1)
            if choice == 1:
                walls_h.append((line[i], line[i + 1]))
    return maze_builder.maze_builder(height, width, walls_h, walls_v)


def maze_generator_eller_horizontal_walls(line, current_line, blocks, width, walls_h):
    size = 0
    for i in range(width - 1):
        if current_line[i] != current_line[i + 1]:  # если элеметы не из одного множества, мы случайным образом решаем
            # ставить между ними стену или нет
            choice = random.randint(0, 1)
            if choice == 0:
                current_line[i + 1] = current_line[i]  # если не ставим, то объединяем множества
                size += 1
            else:
                walls_h.append((line[i], line[i + 1]))  # если ставим, то запоминаем стену
                blocks.append(size)  # выписываем размер получившегося блока
                size = 0
        else:
            walls_h.append((line[i], line[i + 1]))
            size += 1
    blocks.append(size)


def maze_generator_eller_vertical_walls(line, current_line, blocks, vertical_borders, width, walls_v):
    current = current_line[0]
    index = 0
    for i in range(width):
        if current_line[i] != current:  # если текущий не лежит в том же множестве, что и предыдущий:
            current = current_line[i]
            index += 1  # переходим к следующему блоку
        if blocks[index] > 0:  # если размер данного подмножества без нижних стен не равен нулю
            choice = random.randint(0, 1)  # можем поставить стену
            if choice == 1:
                blocks[index] -= 1  # нужно уменьшить размер данного множества (без элементов с нижними стенами)
                # это нужно, чтобы не было тупика и всегда был путь вниз
                walls_v.append((line[i], line[i] + width))
                vertical_borders[i] = 1


def maze_generator_eller_next_line_preparation(line, current_line, vertical_borders, width): # здесь обновляется current_line
    # для работы со след. строчкой лабиринта:
    # делится на новые множества, два элемента остаются в одном множестве, если у них обоих не добавилось нижней стенки
    # это предотвращает создание изолированных участков
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
