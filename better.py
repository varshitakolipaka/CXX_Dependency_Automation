import os
import shutil
from pathlib import Path
import re
import pydot


def getFolderPath(file_path):
    # get everything before the last slash
    folder_path = re.match("^(.*[\/])", file_path).group(1)
    return folder_path

def getIncludes(myline):
    # finds all instances of include patterns in a line, should find only 1
    # (#include *\"(.*?.(h|hpp))\")|
    match = re.findall('(#include *\"(.*?.(h|hpp))\")|(#include *\<(.*?.(h|hpp))\>)', myline)
    # checks in [()], and whether such an array exists, else, an include is not found
    if len(match):
        if match[0][1] != "":
            include_file_name = match[0][1]
        elif match[0][4] and match[0][4] != "":
            include_file_name = match[0][4]
    else:
        include_file_name = "INVALID" 
    
    return include_file_name
    
def getDependencies(file_path, included_libraries):
    print("----------------------")
    print("INSIDE:", file_path)
    print("----------------------")
    # gets only the folder path
    path_to_file = getFolderPath(file_path)
    # check if such a file exists, and it isn't empty stringed
    if os.path.exists(file_path) and file_path != "" and os.path.isdir(file_path) != 1:
        print("it's a real file")
        # opening the file
        myfile = open(file_path, "r")
        myline = myfile.readline()
        # do for each line in the file, while reading line by line
        while myline:
            # get an instance of #include
            include_file_name = getIncludes(myline)
            # if something is being included...
            if include_file_name != "INVALID":
                
                # if file not found, try finding file in the root directory of file
                print("Raw include:", include_file_name)
                include_file_name = compressFilePath(include_file_name, path_to_file)
                print("After compression:", include_file_name)
                include_file_name = processInputPath(path_to_file, include_file_name)

                # print("NEW PATH: ", include_file_name)
                
                print("Including: ", include_file_name)
                include_list.append(include_file_name)
                included_libraries[include_list[0]].append(include_file_name)

            myline = myfile.readline()

        myfile.close()

    return include_list

def compressFilePath(file_path, folder_path):
    if file_path.startswith("/"):
        return file_path
    if file_path.startswith("./") or file_path.startswith("../"):
        correction_required = 1
        while file_path.startswith("./"):
            file_path = file_path[2:]
        # shorten file paths by removing ../ and ./
        while file_path.startswith( "../"):
            if folder_path.endswith("/"):
                folder_path = folder_path[:-1]
            folder_path = re.match("^(.*[\/])", folder_path).group(1)
            file_path = file_path[3:]
        return folder_path, file_path
    return file_path

def find_common_path(dictionary):
    array = keys_to_arr(dictionary)
    common = os.path.commonpath(array)
    if not common.endswith("/"):
        common = re.match("^(.*[\/])", common).group(1)
    return common
    


def rename_keys_dict(common_path, required_path, dictionary):
    for key in dictionary:
        new_key = key.replace(common_path, required_path)
        # print("new_key: ",new_key)
        dictionary[new_key] = dictionary.pop(key)
        return dictionary
    
def keys_to_arr(dictionary):
    arr = []
    for key in dictionary:
        arr.append(key)
    return arr
def processIntactPath(intact_path):
    if not intact_path.startswith("/"):
        intact_path = "/" + intact_path
    if not intact_path.endswith("/"):
        intact_path = intact_path[:-1]
    return intact_path

def createDotFile(included_libraries, path_to_remove):
    graphviz_code = "strict digraph G {\n"
    for parent, children in included_libraries.items():
        clean_parent = parent.replace(path_to_remove, "")
        graphviz_code = graphviz_code + '"' + clean_parent + '"' + "-> { "
        s = "; ".join(
            str('"' + child.replace(path_to_remove, "") + '"') for child in children
        )
        graphviz_code = graphviz_code + s + "};\n"

    graphviz_code = graphviz_code + "\n}"
    # print(graphviz_code)
    graph, = pydot.graph_from_dot_data(graphviz_code)
    image_path = input("Enter Image Path:")
    graph.write_png(image_path )

def initIncludeDict(included_libraries, include_list):
    while len(include_list) > 0:
        if include_list[0] not in included_libraries:
            included_libraries[include_list[0]] = []
            getDependencies(include_list[0], included_libraries)
        include_list.pop(0)

def processInputPath(folder_path,input_path):
    print("PATH = ", input_path)
    abspath = (folder_path+input_path)
    abspath = os.path.abspath(abspath)
    print(abspath)
    path = abspath
    if not os.path.exists(abspath) or os.path == "":
        print("IT IS GOING HERE")
        temp_path = "/usr/local/Cellar/opencv/4.5.3_3/include/opencv4/" + input_path
        if os.path.exists(temp_path):
            path = temp_path
        
    return path



# Driver code ------------------------------------

# unfiltered, every include is added here
include_list = []
# final includes, with no repeats are added here
included_libraries = {}


input_path = input("File Path: ")
input_path = processInputPath("", input_path)

#  initialise the include list and the include dictionary, basically, we add the file that calls all the other fiels
include_list.append(input_path)
initIncludeDict(included_libraries, include_list)
path_to_remove = find_common_path(included_libraries)

createDotFile(included_libraries, path_to_remove)

intact_path = input("Enter the directory structure to keep intact (Must be a substring of original path from the end): ")
intact_path = processIntactPath(intact_path)

desired_path = str(
    input("Enter the desired directory, where you want your root file: ")
)
desired_path += intact_path
if not desired_path.endswith("/"):
    desired_path += "/" 

for file_path in included_libraries.items():
    exact_file_path = file_path[0].replace(path_to_remove, desired_path)
    exact_directory_path = re.match(r"^(.*[\/])", exact_file_path).group(1)
    if os.path.exists(file_path[0]):
        os.makedirs(exact_directory_path, mode=0o777, exist_ok=True)
        if os.path.isdir(exact_file_path) != 1:
            open(exact_file_path, "w").close()
            # check if file_path[0] and exact_file_path aren't the same file
            if file_path[0] != exact_file_path:
                print("Copying: ", file_path[0], " to ", exact_file_path)
                shutil.copy(file_path[0], exact_file_path)
