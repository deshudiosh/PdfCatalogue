from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, mm
from reportlab.lib.pagesizes import A4, landscape


PROJECTS_PER_PAGE = 3
PIC_PER_PROJECT = 3
PIC_CENTERS_X = [52.833 * mm, 148.5 * mm, 244.167 * mm]
PIC_CENTERS_Y = [44.283 * mm, 111.888 * mm, 178.094 * mm]
PIC_SIZE = [95.667 * mm, 53.813 * mm]
PIC_MARGIN = [5, 5]

TITLE_POS_Y = [13.452*mm, 80.358*mm, 147.263*mm]

PAGE_MARGIN = 5*mm
PW, PH = landscape(A4)

def createPdf(projectsList, url):
    c = canvas.Canvas(filename = url,
                      pagesize = [PW, PH])

    projectIdxOnPage = 0
    for project in projectsList:

        drawProjectInfo(c, project, projectIdxOnPage)

        for pictureIdx in range(0, PIC_PER_PROJECT):
            if (pictureIdx < len(project["imgs"]) ):
                placeLinkedPicture(c, projectIdxOnPage, pictureIdx, project)

        projectIdxOnPage += 1

        if projectIdxOnPage >= PROJECTS_PER_PAGE:
            projectIdxOnPage = 0
            c.showPage()

    c.save()


def drawProjectInfo(c, project, projectIdxOnPage):

    title = project["name"].upper()
    url = project["url"]

    y = PH - TITLE_POS_Y[projectIdxOnPage]

    c.saveState()
    c.setFillColor([0, 0, 0], 0.2)
    c.rect(PAGE_MARGIN, y - 5, PW - PAGE_MARGIN * 2, 20, fill=1, stroke=0)
    c.restoreState()

    # temporary solution is to draw link rect on the titile, so its clickable
    c.linkURL(url, [PAGE_MARGIN, y - 5, PAGE_MARGIN + c.stringWidth(title) + 10, y - 5 + 20])

    c.drawString(PAGE_MARGIN + 5, y, title)
    c.drawRightString(PW - PAGE_MARGIN - 5, y , url)




def placeLinkedPicture(c, projectIdxOnPage, pictureIdx, project):
    w, h = PIC_SIZE[0] - PIC_MARGIN[0], PIC_SIZE[1] - PIC_MARGIN[1]
    x = PIC_CENTERS_X[pictureIdx] - w / 2
    y = PH - (PIC_CENTERS_Y[projectIdxOnPage] + h / 2)
    # c.rect(x, y, w, h, fill=1)
    url = project["imgs"][pictureIdx]
    c.drawImage(url, x, y, w, h)

    link = project["url"].replace("\\", "/")
    c.linkURL(link, [x, y, x+w, y+h])

    # print("projectIdx: ", projectIdx, " pictureIdx: ", pictureIdx, [x, y, w, h])
