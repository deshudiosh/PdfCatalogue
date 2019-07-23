import tkinter as tk

import projectDistinguisher

def printOut(project_ist):
    f = open("pdfCatalogue.txt", "w")
    for pro in project_ist:
        print((pro["name"], pro["imgs"]), file=f)
        print((pro["name"], pro["imgs"]))

def askForFolder():
    root = tk.Tk()
    root.withdraw()
    # url = os.path.abspath(filedialog.askdirectory())
    url = "P:/WW"
    # url = "C:/GoogleDrive/PdfCatalogue/WW"

    if len(url) > 0:
        list = projectDistinguisher.getProjectsList(url)
        
        printOut(list)

        # htmlReport.create_report(list, "pdf_report.html")

        # pdfCreator.createPdf(list, "pdfCatalogue.pdf")

askForFolder()




