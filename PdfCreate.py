from itertools import product
from pathlib import Path
from typing import NamedTuple

from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas


class Point(NamedTuple):
    x: int
    y: int


def draw_project(c: canvas.Canvas, anchor: Point, project: Path):
    c.drawString(anchor.x, anchor.y + 10, project.stem)


def init():
    folder = Path.cwd() / "FolderTree/P/WW/"
    projects = [dir for dir in folder.glob("*") if dir.is_dir()]

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


if __name__ == '__main__':
    init()

