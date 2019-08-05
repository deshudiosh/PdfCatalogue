import os
import typing
from itertools import product
from pathlib import Path
from typing import NamedTuple

from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas


# class Point(NamedTuple):
#     x: int
#     y: int
Point = typing.NamedTuple("Point", [('x', int), ('y', int)])


def draw_project(c: canvas.Canvas, anchor: Point, project: Path):
    anchor.y += 10
    c.drawString(anchor.x, anchor.y, project.stem)


def init():
    folder = Path.cwd() / "FolderTree/P/WW/"
    projects = [p for p in folder.glob("*") if p.is_dir()]

    page_size_x, page_size_y = landscape(A4)
    grid = Point(3, 2)

    c = canvas.Canvas("catalogue.pdf", pagesize=[page_size_x, page_size_y], bottomup=False)

    i = 0
    for x, y, in product(range(grid.x), range(grid.y)):
        x = page_size_x / grid.x * x
        y = page_size_y / grid.y * y
        anchor = Point(x, y)
        print(anchor)
        draw_project(c, anchor, projects[i])
        i += 1

    c.showPage()
    c.save()
    os.system("start catalogue.pdf")


if __name__ == '__main__':
    init()

