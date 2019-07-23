from pathlib import Path
from string import digits


possible_projects = []

def is_date_string(s:str):
    just_digits = ''.join(c for c in s if c in digits)
    enough_digits = len(just_digits) >= 6
    starts_with_digit = s[0] in digits
    return all([just_digits, enough_digits, starts_with_digit])


def tree(directory):
    print(f'+ {directory}')
    for path in sorted(directory.rglob('*')):
        if path.is_dir():
            # depth = len(path.relative_to(directory).parts)
            # spacer = '    ' * depth
            # print(f'{spacer}+ {path.name}', is_date_string(path.name))
            if not is_date_string(path.name):
                possible_projects.append(path)


def create_project_folders():
    """search for images and pick few"""
    for p in possible_projects: # type:Path
        jpgs = [pic for pic in sorted(p.rglob('*.jpg'))]
        if len(jpgs) > 0:
            jpgs = sorted(jpgs, key=lambda o: o.stat().st_ctime)

            ## create folder

            ## copy files
            ## deal with idenical names
            ## resize them

            ## create xml or something smarter


def collect_data():
    folder = Path(r"P:\WW")
    tree(folder)

    create_project_folders()


collect_data()




