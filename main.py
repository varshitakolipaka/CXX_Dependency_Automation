from functions_main import *
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

intact_path = input("Enter the directory structure to keep intact (Must be a substring of original path from the end, please end with a '/'): ")
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
                # print("Copying: ", file_path[0], " to ", exact_file_path)
                shutil.copy(file_path[0], exact_file_path)

print(included_libraries)