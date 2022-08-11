import os
import PySimpleGUI as sg

# --- user inputs
save_name = "datapacks"
datapack_name = "temp_name"
version_no = 10
description = "temp_pack desc"
predicates = False
tags = False
# ---

# --- const directories
saves_dir = "AppData/Roaming/.minecraft/saves"
mc_funcs = "./data/minecraft/tags/functions"
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

def createStarter(save_name, datapack_name, version_no, description, predicates, tags):
    # --- file contents
    mcmeta_conts = ["{\n", "\t\"pack\": {\n", f"\t\t\"pack_format\": {version_no},\n", f"\t\t\"description\": \"{description}\",\n", "\t}\n", "}\n"]
    load_conts = ["{\n", "\t\"values\": [\n", f"\t\t\"{datapack_name}:load\"\n", "\t]\n", "}\n"]
    tick_conts = ["{\n", "\t\"values\": [\n", f"\t\t\"{datapack_name}:tick\"\n", "\t]\n", "}\n"]
    load_mcfunc_conts = "# contents of this file are run only when the datapack is loaded"
    tick_mcfunc_conts = "# contents of this file are run every tick while the datapack is loaded"
    # ---

    home_dir = os.path.expanduser('~')
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

if __name__ == "__main__":
    # createStarter(save_name, datapack_name, version_no, description, predicates, tags)
    layout = [[sg.Text("Poggers")], [sg.Text("Poggers but on row 2"), sg.Text("Coggers on row 2")], [sg.Button("Button on Row 3")], [sg.Button("Exit button")]]
    window = sg.Window("This is the title", layout, size=(960, 540))
    event, values = window.read()
    while True:
        if event in (None, "Exit button"):
            break
        else:
            print(event)
    window.close()