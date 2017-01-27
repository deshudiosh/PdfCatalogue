import webbrowser


def create_report(project_list, path):
    f = open(path, "w")

    content = "<html>\n"

    content += styles()

    for project in project_list:
        content += project_div(project)


    content += "</html>"

    f.write(content)
    f.close()

    webbrowser.open(path)


def project_div(project):
    div = """
    <div class="project">
        <div class="header">
            <div class="title"><h1>%name%</h1></div>
            <div class="url"><p>%url%</p></div>
        </div>
        <div class="imgs">
            %imgs%
        </div>
    </div>
    """

    name = project["name"]
    url = project["url"]


    div = div.replace("%name%", name)
    div = div.replace("%url%", url)

    return div

def styles():
    styles = """
    <head>
        <style type="text/css">
            *{ border:1px solid; padding:3px}
            .project {

            }
            .title, .url {
                display: inline-block;
                border: 1px solid;
			}

            .url {
                color: blue;
                float: right;
            }
        </style>
    </head>

    """
    return styles