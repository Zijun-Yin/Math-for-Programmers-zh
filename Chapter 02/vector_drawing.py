"""
书P20 表2-1第一次提及本文件vector_drawing.py。

"""
from math import sqrt, pi, ceil, floor
import matplotlib
import matplotlib.patches
from matplotlib.collections import PatchCollection


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import xlim, ylim

# 定义颜色变量
blue = 'C0'
black = 'k'
red = 'C3'
green = 'C2'
purple = 'C4'
orange = 'C2'
gray = 'gray'


class Polygon():
    """多边形"""

    def __init__(self, *vertices, color=blue, fill=None, alpha=0.4):
        self.vertices = vertices
        self.color = color
        self.fill = fill
        self.alpha = alpha


class Points():
    """一个或多个点(也叫向量)"""

    def __init__(self, *vectors, color=black):
        self.vectors = list(vectors)  # 向量列表
        self.color = color  # 点的颜色默认black


class Arrow():
    """矢, 箭头
    tail是可选参数，下面展示了用法
    >>> Arrow(tip) # 从原点到tip的箭头
    >>> Arrow(tip, tail) # 从点tip到点tial的箭头
    颜色为color默认red
    """

    def __init__(self, tip, tail=(0, 0), color=red):
        self.tip = tip
        self.tail = tail
        self.color = color


class Segment():
    """线段
    从start_point到end_point
    color颜色默认为blue
    """

    def __init__(self, start_point, end_point, color=blue):
        self.start_point = start_point
        self.end_point = end_point
        self.color = color


def extract_vectors(objects):
    # helper function to extract all the vectors from a list of objects
    for object in objects:
        if type(object) == Polygon:
            for v in object.vertices:
                yield v
        elif type(object) == Points:
            for v in object.vectors:
                yield v
        elif type(object) == Arrow:
            yield object.tip
            yield object.tail
        elif type(object) == Segment:
            yield object.start_point
            yield object.end_point
        else:
            raise TypeError("Unrecognized object: {}".format(object))


def draw(*objects, origin=True, axes=True, grid=(1, 1), nice_aspect_ratio=True,
         width=6, save_as=None):
    """draw绘制图形
    save_as: 设置保存图像的路径
    """
    all_vectors = list(extract_vectors(objects))
    xs, ys = zip(*all_vectors)

    max_x, max_y, min_x, min_y = max(
        0, *xs), max(0, *ys), min(0, *xs), min(0, *ys)

    # sizing
    if grid:
        x_padding = max(ceil(0.05*(max_x-min_x)), grid[0])
        y_padding = max(ceil(0.05*(max_y-min_y)), grid[1])

        def round_up_to_multiple(val, size):
            return floor((val + size) / size) * size

        def round_down_to_multiple(val, size):
            return -floor((-val - size) / size) * size

        plt.xlim(floor((min_x - x_padding) / grid[0]) * grid[0],
                 ceil((max_x + x_padding) / grid[0]) * grid[0])
        plt.ylim(floor((min_y - y_padding) / grid[1]) * grid[1],
                 ceil((max_y + y_padding) / grid[1]) * grid[1])

    if origin:
        plt.scatter([0], [0], color='k', marker='x')

    if grid:
        plt.gca().set_xticks(np.arange(plt.xlim()[0], plt.xlim()[1], grid[0]))
        plt.gca().set_yticks(np.arange(plt.ylim()[0], plt.ylim()[1], grid[1]))
        plt.grid(True)
        plt.gca().set_axisbelow(True)

    if axes:
        plt.gca().axhline(linewidth=2, color='k')
        plt.gca().axvline(linewidth=2, color='k')

    for object in objects:
        if type(object) == Polygon:
            for i in range(0, len(object.vertices)):
                x1, y1 = object.vertices[i]
                x2, y2 = object.vertices[(i+1) % len(object.vertices)]
                plt.plot([x1, x2], [y1, y2], color=object.color)
            if object.fill:
                xs = [v[0] for v in object.vertices]
                ys = [v[1] for v in object.vertices]
                plt.gca().fill(xs, ys, object.fill, alpha=object.alpha)
        elif type(object) == Points:
            xs = [v[0] for v in object.vectors]
            ys = [v[1] for v in object.vectors]
            plt.scatter(xs, ys, color=object.color)
        elif type(object) == Arrow:
            tip, tail = object.tip, object.tail
            tip_length = (xlim()[1] - xlim()[0]) / 20.
            length = sqrt((tip[1]-tail[1])**2 + (tip[0]-tail[0])**2)
            new_length = length - tip_length
            new_y = (tip[1] - tail[1]) * (new_length / length)
            new_x = (tip[0] - tail[0]) * (new_length / length)
            plt.gca().arrow(tail[0], tail[1], new_x, new_y,
                            head_width=tip_length/1.5, head_length=tip_length,
                            fc=object.color, ec=object.color)
        elif type(object) == Segment:
            x1, y1 = object.start_point
            x2, y2 = object.end_point
            plt.plot([x1, x2], [y1, y2], color=object.color)
        else:
            raise TypeError("Unrecognized object: {}".format(object))

    fig = matplotlib.pyplot.gcf()

    if nice_aspect_ratio:
        coords_height = (ylim()[1] - ylim()[0])
        coords_width = (xlim()[1] - xlim()[0])
        fig.set_size_inches(width, width * coords_height / coords_width)

    if save_as:
        plt.savefig(save_as)

    plt.show()
