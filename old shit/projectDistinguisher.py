import os

def getProjectsList(url):

    projectsList = []

    # 1 get project folders
    # 2 for each project folder determine images to be shown in pdf
    # 3 put {project name, [images list]} data in dictonary

    projectFolders = getProjectFoldersInUrl(url)
    projectFolders = sorted(projectFolders)

    for project in projectFolders:
        projectDict = {"name": os.path.basename(project), "url" : project}

        imgs = []
        for date in getDateFolders(project):
            if os.path.isdir(date):
                img = getLastImageInFolder(date)
                if img:
                    imgs.append(img)

        projectDict["imgs"] = imgs

        projectsList.append(projectDict)

    return projectsList


def getProjectFoldersInUrl(url):
    projectFodlers = set()

    for root, dirs, files in os.walk(top = url, topdown = True):
        for name in dirs:
            # sprawdz czy folder ma w nazwie date, np: 2017.01.06
            isDateFormated = len(name)>= 10 and name[4] == "." and name[7] == "."
            if isDateFormated: projectFodlers.add(root)

    return projectFodlers



#trzeba bedzie rozszerzyc zeby brało nie tylko osttani, ale np tez przedostatni/pierwszy folder daty
def getDateFolders(url):
    datedFolders = []

    for folder in os.listdir(url):
        isDateFormated = len(folder) >= 10 and folder[4] == "." and folder[7] == "."
        if isDateFormated: datedFolders.append(os.path.join(url, folder))

    return datedFolders


def getLastImageInFolder(url):
    allFiles = os.listdir(url)
    jpgs = []
    for file in allFiles:
        if file.endswith(".jpg"):
            jpgs.append(file)

    jpgs.sort()


    #is there any jpg?
    last = None
    if len(jpgs) > 0:
        last = os.path.join(url, jpgs[-1])
        # last = last.replace("\\", "/")

    return last
