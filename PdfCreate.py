import json
import os
from dataclasses import dataclass
from pathlib import Path

from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


@dataclass
class Rectangle:
    x: int
    y: int
    w: int = 0
    h: int = 0

    def invert_y(self, y_min, y_max):
        self.y = y_max - (self.y - y_min) - self.h


def draw_image(c: canvas.Canvas, rect: Rectangle, pic_path, link_path: Path):
    # c.rect(rect.x, rect.y, rect.w, rect.h)
    c.drawImage(pic_path, rect.x, rect.y, rect.w, rect.h, preserveAspectRatio=True, showBoundary=True)
    c.linkURL(link_path.as_uri(), (rect.x, rect.y, rect.x+rect.w, rect.y+rect.h))


def draw_project(c: canvas.Canvas, area: Rectangle, project: Path, index: int):
    c.setStrokeColorRGB(1, 1, 1)
    c.rect(area.x, area.y, area.w, area.h)
    # anchor.y += 10
    project_name = " ".join([str(index + 1) + ".", project.stem])
    c.drawString(area.x + 7, area.y + area.h - 15, project_name)

    with open(project / "project.json") as json_file:
        data = json.load(json_file)
        pictures = data['pictures']

    area.x += cm / 4
    area.w -= cm / 2
    area.y += cm / 4
    area.h -= cm
    grid = Rectangle(2, 3)

    for i, pic in enumerate(pictures):
        col = i % grid.x
        row = i // grid.x
        w = area.w / grid.x
        h = area.h / grid.y
        x = area.x + w * col
        y = area.y + h * row
        rect = Rectangle(x, y, w, h)
        rect.invert_y(area.y, area.y + area.h)
        pic_path = project / pic
        link_path = Path(pictures[pic]).parent
        draw_image(c, rect, pic_path, link_path)


def init():
    folder = Path.cwd() / "FolderTree/P/WW/"
    folder = Path.cwd() / "FolderTree/P/Krzesla/"
    projects = [p for p in folder.glob("*") if p.is_dir()]

    page_size_x, page_size_y = landscape(A4)
    grid = Rectangle(3, 2)
    projects_per_grid = grid.x * grid.y

    c = canvas.Canvas("catalogue.pdf", pagesize=[page_size_x, page_size_y])

    for i, project in enumerate(projects):
        idx_at_page = i % projects_per_grid

        column = idx_at_page % grid.x
        row = idx_at_page // grid.x

        last_on_page = idx_at_page == projects_per_grid - 1

        rect = Rectangle(page_size_x / grid.x * column,
                         page_size_y / grid.y * row,
                         page_size_x / grid.x,
                         page_size_y / grid.y)

        rect.invert_y(0, page_size_y)

        draw_project(c, rect, project, i)

        if last_on_page:
            c.showPage()  # start new page

    c.save()
    os.system("start catalogue.pdf")


if __name__ == '__main__':
    init()
