import json
import multiprocessing
import shutil
from pathlib import Path
from string import digits
from typing import List


def is_date_string(s:str):
    just_digits = ''.join(c for c in s if c in digits)
    enough_digits = len(just_digits) >= 6
    starts_with_digit = s[0] in digits
    return all([just_digits, enough_digits, starts_with_digit])


def tree(directory):
    print("finding possible folders: start")
    possible_projects = (path for path in sorted(directory.glob('*')) if path.is_dir() and not is_date_string(path.name))
    print("finding possible folders: done")
    return possible_projects


def choose_pictures(jpgs)->List[Path]:
    """ reverse last 6 pics for now... """
    num_pics = 6
    ## sort by date
    jpgs = sorted(jpgs, key=lambda o: o.stat().st_ctime)
    jpgs.reverse()

    if len(jpgs) > num_pics:
        jpgs = jpgs[:num_pics]

    return jpgs


def manage_possible_project(project: Path):
    jpgs = [pic for pic in sorted(project.rglob('*.jpg'))]
    if len(jpgs) < 1:
        return

    ## create folder
    ## TODO: deal with possible name duplicates
    disk_letter = project.anchor[0]
    catalog_path = Path.cwd() / "FolderTree" / disk_letter / "/".join(project.parts[1:])
    catalog_path.mkdir(parents=True, exist_ok=True)

    ## get pictures to catalogue
    jpgs = choose_pictures(jpgs)

    ## copy files
    ## TODO: deal with possible name duplicates
    pictures = {}
    copied_jpgs = []
    for jpg in jpgs:
        copy_to_path = catalog_path / jpg.name
        shutil.copy(str(jpg), copy_to_path)
        copied_jpgs.append(copy_to_path)
        pictures[jpg.name] = str(jpg)

    ## resize them

    ## dump json file
    json_file = catalog_path / "project.json"
    json_dict = {
        "date_creation": project.stat().st_ctime,
        "date_modification": project.stat().st_mtime,
        "pictures": pictures
    }
    with open(json_file, 'w') as f:
        json.dump(json_dict, f)

    #finish
    process = multiprocessing.current_process().name
    print(catalog_path.parts[-1:], "finished at process: ", process)


def collect_data():
    folder = Path(r"P:\WW")
    # folder = Path(r"P:\Krzesla")
    possible_projects = tree(folder)

    with multiprocessing.Pool() as pool:
        pool.map(manage_possible_project, possible_projects)


if __name__ == '__main__':
    collect_data()




