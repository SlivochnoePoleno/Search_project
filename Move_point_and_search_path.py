import networkx as nx
import random
from tkinter import *

ROWS = 18
COLUMNS = 24
WIDTH = 20


def dist(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def path_find(graph, start, end):
    path = []
    try:
        path.extend(nx.astar_path(graph, start, end, heuristic=dist))
    except:
        print("shit")
    return path


def move_up(graph, canvas, point):
    x, y, x2, y2 = canvas.coords(point)
    j = int(x / WIDTH)
    i = int(y / WIDTH)
    if (i - 1, j) in graph:
        canvas.move(point, 0, -WIDTH)


def move_down(graph, canvas, point):
    x, y, x2, y2 = canvas.coords(point)
    j = int(x / WIDTH)
    i = int(y / WIDTH)
    if (i + 1, j) in graph:
        canvas.move(point, 0, WIDTH)


def move_left(graph, canvas, point):
    x, y, x2, y2 = canvas.coords(point)
    j = int(x / WIDTH)
    i = int(y / WIDTH)
    if (i, j - 1) in graph:
        canvas.move(point, -WIDTH, 0)


def move_right(graph, canvas, point):
    x, y, x2, y2 = canvas.coords(point)
    j = int(x / WIDTH)
    i = int(y / WIDTH)
    if (i, j + 1) in graph:
        canvas.move(point, WIDTH, 0)


def draw_path(graph, canvas, point, start):
    canvas.delete("pink")
    x, y, x2, y2 = canvas.coords(point)
    y3 = int(x / WIDTH)
    x3 = int(y / WIDTH)
    end = (x3, y3)
    path = path_find(graph, start, end)
    path.pop()
    for i in range(ROWS):
        for j in range(COLUMNS):
            x1 = j * WIDTH
            y1 = i * WIDTH
            x2 = j * WIDTH + WIDTH
            y2 = i * WIDTH + WIDTH
            if (i, j) in path:
                pink = canvas.create_rectangle(x1, y1, x2, y2, fill='pink')
                canvas.addtag_withtag("pink", pink)


def draw_map(graph, canvas):
    for i in range(ROWS):
        for j in range(COLUMNS):
            x1 = j * WIDTH
            y1 = i * WIDTH
            x2 = j * WIDTH + WIDTH
            y2 = i * WIDTH + WIDTH
            if (i, j) in graph:
                canvas.create_rectangle(x1, y1, x2, y2, fill='white')
            else:
                canvas.create_rectangle(x1, y1, x2, y2, fill='black')


def draw_point(canvas, coord):
    i, j = coord
    x1 = j * WIDTH
    y1 = i * WIDTH
    x2 = j * WIDTH + WIDTH
    y2 = i * WIDTH + WIDTH
    point = canvas.create_rectangle(x1, y1, x2, y2, fill='purple')
    return point


def main():
    G = nx.grid_2d_graph(ROWS, COLUMNS)

    for i in range(ROWS):
        for j in range(COLUMNS):
            result = random.choices([0, 1], weights=[20, 5], k=1)
            if result[0]:
                G.remove_node((i, j))

    number_of_nodes = nx.number_of_nodes(G)

    start = list(G.nodes())[0]
    end = list(G.nodes())[number_of_nodes - 1]

    root = Tk()
    c = Canvas(height=ROWS * WIDTH, width=COLUMNS * WIDTH, bg='white')
    c.focus_set()
    c.pack()
    draw_map(G, c)
    point = draw_point(c, start)

    c.bind('<Up>', lambda event: move_up(G, c, point))
    c.bind('<Down>', lambda event: move_down(G, c, point))
    c.bind('<Left>', lambda event: move_left(G, c, point))
    c.bind('<Right>', lambda event: move_right(G, c, point))
    c.bind('<p>', lambda event: draw_path(G, c, point, start))

    root.mainloop()


main()
