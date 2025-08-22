import os
def create_json_file(buildDir):

    folder_name = 'CJson'
    filename = 'C0 --.json'
    
    folder_path = os.path.join(buildDir, folder_name)
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    file_path = os.path.join(folder_path, filename)
    
    with open(file_path, 'w') as file:
        file.write('{}')

def create_folder(folder_path):
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"Folder created successfully: {folder_path}")
    except Exception as e:
        print(f"Failed to create folder: {folder_path}, error: {e}")

def clear_files_in_directory(directory_path):
    """
    Clear all files in the specified directory.
    :param directory_path: Target directory path
    """
    if not os.path.exists(directory_path):
        print(f"Path {directory_path} does not exist!")
        return

    if not os.path.isdir(directory_path):
        print(f"{directory_path} is not a directory!")
        return

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path):  
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            else:
                print(f"Skipped non-file: {file_path}")
        except Exception as e:
            print(f"Unable to delete file {file_path}, error: {e}")

def clear(build_dir):
    clear_files_in_directory(os.path.join(build_dir, "CJson"))
    clear_files_in_directory(os.path.join(build_dir, "CDistance"))

def write_to_txt(directory, data, file_name):

    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, file_name), 'w') as f:
        for key, value in data.items():
            f.write(f"{key}: {value}\n")
