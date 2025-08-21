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
    """
    在指定路径创建文件夹
    :param folder_path: 要创建的文件夹路径
    """
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"文件夹已成功创建: {folder_path}")
    except Exception as e:
        print(f"创建文件夹失败: {folder_path}，错误: {e}")

def clear_files_in_directory(directory_path):
    """
    清空指定路径下的所有文件
    :param directory_path: 目标文件夹路径
    """
    if not os.path.exists(directory_path):
        print(f"路径 {directory_path} 不存在！")
        return

    if not os.path.isdir(directory_path):
        print(f"{directory_path} 不是一个文件夹！")
        return

    # 遍历文件夹中的文件
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path):  # 仅删除文件
                os.remove(file_path)
                print(f"已删除文件: {file_path}")
            else:
                print(f"跳过非文件: {file_path}")
        except Exception as e:
            print(f"无法删除文件 {file_path}，错误: {e}")

def clear(build_dir):
    clear_files_in_directory(os.path.join(build_dir, "CJson"))
    clear_files_in_directory(os.path.join(build_dir, "CDistance"))

def write_to_txt(directory, data, file_name):
    """将数据写入文本文件"""
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, file_name), 'w') as f:
        for key, value in data.items():
            f.write(f"{key}: {value}\n")
