from email.policy import default
from ensurepip import version
import os
import PySimpleGUI as sg

# --- user inputs
save_name = ""
datapack_name = ""
version_no = 0
description = ""
predicates = False
tags = False
# ---

# --- const directories
saves_dir = "AppData/Roaming/.minecraft/saves"
mc_funcs = "./data/minecraft/tags/functions"
# ---

# --- const vars
home_dir = os.path.expanduser('~')
pack_format = {"1.13-1.14.4":4, "1.15-1.16.1":5, "1.16.2-1.16.5":6, "1.17-1.17.1":7, "1.18-1.18.1":8, "1.18.2":9, "1.19+":10}
# ---

def makeDirectory(path):
    try:
        os.makedirs(path)
    except Exception as error:
        print(error)

def fixSlash(path):
    return path.replace("\\","/")

def writeContents(file, contents):
    for line in contents:
        file.write(line)

def getSaves():
    saves_path = os.path.join(home_dir, saves_dir)
    os.chdir(saves_path)
    return os.listdir()

def createStarter(save_name, datapack_name, version_no, description, predicates, tags):
    # --- file contents
    mcmeta_conts = ["{\n", "\t\"pack\": {\n", f"\t\t\"pack_format\": {version_no},\n", f"\t\t\"description\": \"{description}\",\n", "\t}\n", "}\n"]
    load_conts = ["{\n", "\t\"values\": [\n", f"\t\t\"{datapack_name}:load\"\n", "\t]\n", "}\n"]
    tick_conts = ["{\n", "\t\"values\": [\n", f"\t\t\"{datapack_name}:tick\"\n", "\t]\n", "}\n"]
    load_mcfunc_conts = "# contents of this file are run only when the datapack is loaded"
    tick_mcfunc_conts = "# contents of this file are run every tick while the datapack is loaded"
    # ---

    saves_path = os.path.join(home_dir, saves_dir)

    datapack_dir = save_name + "/datapacks"
    datapack_path = os.path.join(saves_path, datapack_dir)

    path = os.path.join(datapack_path, datapack_name)

    makeDirectory(path)

    # change dir to use relative paths
    os.chdir(path)

    # make mcmeta file
    mcmeta_file = open("./pack.mcmeta", "w")
    writeContents(mcmeta_file, mcmeta_conts)
    mcmeta_file.close()

    makeDirectory(mc_funcs)

    os.chdir(mc_funcs)

    # make load and tick files
    load_file = open("./load.json", "w")
    writeContents(load_file, load_conts)
    load_file.close()

    tick_file = open("./tick.json", "w")
    writeContents(tick_file, tick_conts)
    tick_file.close()

    os.chdir(os.path.join(path, "data"))

    makeDirectory(f"./{datapack_name}/functions")

    os.chdir(f"./{datapack_name}/functions")

    load_mcfunc = open("./load.mcfunction", "w")
    load_mcfunc.write(load_mcfunc_conts)
    load_mcfunc.close()

    tick_mcfunc = open("./tick.mcfunction", "w")
    tick_mcfunc.write(tick_mcfunc_conts)
    tick_mcfunc.close()

    if predicates:
        os.chdir(os.path.join(path, f"data/{datapack_name}"))
        makeDirectory(f"./predicates")
    
    if tags:
        os.chdir(os.path.join(path, f"data/{datapack_name}"))
        makeDirectory(f"./tags/items")


if __name__ == "__main__":
    # page to select the save
    select_save =   [[sg.Text("Choose a Save")], 
                     [sg.Listbox(values=getSaves(), size=(50, 16), key="-SAVE-")],
                     [sg.Text("Can't Find it? Browse Instead: "), sg.FolderBrowse(key="-SAVEFOLDER-")],
                     [sg.Text(size=(40, 1), key="-ERROR-", text_color='yellow')],
                     [sg.Button("Submit"), sg.Button("Quit")]]

    # page to input pack details
    make_pack =     [[sg.Text("Datapack Name: "), sg.Input(key="-NAME-", size=(40, 1))],
                     [sg.Text("Minecraft Version: "), sg.Combo(values=list(pack_format.keys()), default_value="1.19+", key="-FORMAT-")],
                     [sg.Text("Type a Description:")],
                     [sg.Multiline(key="-DESC-", size=(50, 10))],
                     [sg.Checkbox("Use Predicates", default=False, key="-PREDS-"), sg.Checkbox("Use Item Tags", default=False, key="-TAGS-")],
                     [sg.Text(size=(40, 1), key="-ERROR2-", text_color='yellow')],
                     [sg.Button("Create Pack!"), sg.Button("Quit")]]
    
    # whole layout (using 1 to have it all in 1 window)
    layout =    [[sg.Column(select_save, key="-SELECTSAVE-"),
                 sg.Column(make_pack, key="-MAKEPACK-", visible=False)],
                ]

    # stage to mark what diff buttons do 
    stage = 1
    window = sg.Window("Datapack Starter", layout)

    # event loop
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event.startswith("Quit"):
            break
        match stage:
            case 1:
                if event == "Submit":
                    if len(values["-SAVE-"]) == 0 and len(values["-SAVEFOLDER-"]) == 0:
                        window["-ERROR-"].update("Please Select a Save")
                    else:
                        if len(values["-SAVE-"]) == 0:
                            save_name = values["-SAVEFOLDER-"].split("/")[-1]
                        else:
                            save_name = values["-SAVE-"][0]
                        window["-SELECTSAVE-"].update(visible=False)
                        window["-MAKEPACK-"].update(visible=True)
                        stage = 2
            case 2:
                if event == "Create Pack!":
                    if len(values["-NAME-"]) == 0:
                        window["-ERROR2-"].update("Please Type a Datapack Name")
                    else:
                        datapack_name = values["-NAME-"]
                        version_no = pack_format[values["-FORMAT-"]]
                        description = values["-DESC-"]
                        predicates = values["-PREDS-"]
                        tags = values["-TAGS-"]
                        break
            case _:
                continue
    window.close()
    createStarter(save_name, datapack_name, version_no, description, predicates, tags)