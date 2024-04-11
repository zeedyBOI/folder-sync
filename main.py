import os
import sys
import time
import argparse
from logger import Logger
import shutil

def filter_list(main_list, filter_list):
    return [item for item in main_list if item not in filter_list]

# ! Checks if it is a relative or an absolute path
def is_absolute_path(path: str):
    return path.startswith("/")

# ! Check if source directory exists
# ! Creates destination directory if it doesnt
def check_directories(source_folder, destination_folder):
    if not os.path.isdir(source_folder):
        raise Exception(f"Source folder ({source_folder}) does not exist")
    
    if not os.path.isdir(destination_folder):
        path_split = destination_folder.split('/')
        if len(path_split) <= 0:
            raise Exception("Invalid destination path")
        path_control = ""
        if not is_absolute_path(destination_folder):
            i = 0
        else:
            i = 1
            path_control = "/"
        path_control += path_split[i]
        while True:
            if not os.path.isdir(path_control):
                os.mkdir(path_control)
            i += 1
            if i >= len(path_split):
                break
            path_control += f"/{path_split[i]}"
    Logger.info("Source/Destination folders OK")

# ! Iterates over the items in the folder and checks if is folder or file and acts accordingly
def check_items_in_folder(source_folder, destination_folder, relative_path):
    items_source_folder = os.listdir(f"{source_folder}/{relative_path}")
    if len(relative_path) > 0 and not relative_path.startswith("/"):
        relative_path = f"/{relative_path}"
    for item in items_source_folder:
        path = f"{source_folder}{relative_path}/{item}"
        Logger.debug(f"SOURCE PATH: {path}")
        if os.path.isdir(path):
            check_folder(source_folder, destination_folder, f"{relative_path}/{item}")
        elif os.path.isfile(path):
            check_file(source_folder, destination_folder, f"{relative_path}/{item}")
    # ! After copying the necessary files it deletes the files no longer present on the source
    items_dest_folder = os.listdir(f"{destination_folder}{relative_path}")
    delete_items = filter_list(items_dest_folder, items_source_folder)
    for item in delete_items:
        path = f"{destination_folder}{relative_path}/{item}"
        Logger.debug(f"DESTINATION PATH: {path}")
        if os.path.isdir(path):
            delete_folder(path)
        elif os.path.isfile(path):
            delete_file(path)

def check_folder(source_path, destination_path, relative_folder_path):
    if not os.path.isdir(f"{destination_path}{relative_folder_path}"):
        copy_folder(f"{source_path}{relative_folder_path}", f"{destination_path}{relative_folder_path}")
        return
    check_items_in_folder(source_path, destination_path, relative_folder_path)

def copy_folder(_from, _to):
    try:
        shutil.copytree(_from, _to, symlinks=True)
        Logger.info(f"Directory copied from {_from} to {_to}")
    except Exception as e:
        Logger.error(f"Error copying file from {_from} to {_to} [{e}]")

def delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        Logger.info(f"Directory {folder_path} removed")
    except Exception as e:
        Logger.error(f"Error removing folder {folder_path} [{e}]")

# ! Verify if the file needs to be copied
def check_file(source_path, destination_path, relative_file_path):
    # ! Ignores '.swp' files
    if relative_file_path.endswith(".swp"):
        return
    source_file_path = source_path + relative_file_path
    dest_file_path = destination_path + relative_file_path
    # ! If file does not exist in destination copy it
    if not os.path.isfile(dest_file_path):
        copy_file(source_file_path, dest_file_path)
        return
    # ! If file is different (size or last_modified_date) copy it
    source_file_data = os.stat(source_file_path)
    destination_file_data = os.stat(dest_file_path)
    if source_file_data.st_size != destination_file_data.st_size or source_file_data.st_mtime > destination_file_data.st_mtime:
        copy_file(source_file_path, dest_file_path)         

def copy_file(_from, _to):
    try:
        shutil.copy(_from, _to)
        Logger.info(f"File copied from {_from} to {_to}")
    except shutil.SameFileError as e:
        Logger.error(f"Tried to copy file to the same path as source [{_from}]")

def delete_file(file_path):
    try:
        os.remove(file_path)
        Logger.info(f"File {file_path} removed")
    except Exception as e:
        Logger.error(f"Error deleting file [{file_path}]")
   

def main():
    source_folder : str
    destination_folder : str
    timeout : int
    log_path : str
    debug = False
    
    parser = argparse.ArgumentParser(description="Folder syncer script.")

    # ! Define command-line arguments
    parser.add_argument('-s', '--source_folder', required=True ,type=str, help='Source folder from where the file will be synced')
    parser.add_argument('-d', '--destination_folder', required=True, type=str, help='Destination folder to where the folder will be copied to')
    parser.add_argument('-t', '--time', required=True, type=int, help='Time between sync check (seconds)')
    parser.add_argument('-l', '--log_path', required=True, help="Destination folder of logs")
    parser.add_argument('--debug', action=argparse.BooleanOptionalAction, help="Enable debug Logs")

    # ! Parse the command-line arguments
    args = parser.parse_args()

    if args.log_path is not None:
        log_path = args.log_path
        print(f'Log path: {args.log_path}')
    else:
        print("Log path is required")
        sys.exit(-1)
    
    if args.debug is not None:
        debug = args.debug
        print(f'Debug: {args.debug}')
    
    Logger(log_path=log_path, debug=debug)

    # ! Access the arg values
    if args.source_folder is not None:
        source_folder = args.source_folder
        Logger.debug(f'Source Folder: {args.source_folder}')
    else:
        Logger.error("Source folder is required")
        sys.exit(-1)
    if len(source_folder) <= 0:
        Logger.error("Invalid source folder value!")
        sys.exit(-1)
    
    if args.destination_folder is not None:
        destination_folder = args.destination_folder
        Logger.debug(f'Destination folder: {args.destination_folder}')
    else:
        Logger.error("Destination folder is required")
        sys.exit(-1)
    if len(destination_folder) <= 0:
        Logger.error("Invalid destination folder value!")
        sys.exit(-1)
    
    if args.time is not None:
        timeout = args.time
        Logger.debug(f'Timeout: {args.time}')
    else:
        Logger.error("Timeout is required")
        sys.exit(-1)
    
    try:
        check_directories(source_folder, destination_folder)
    except Exception as e:
        Logger.error(f"Error checking directories [{e}]")
        sys.exit(-1)
    
    while True:
        check_items_in_folder(source_folder, destination_folder, "")
        time.sleep(timeout)
    
if __name__ == "__main__":
    main()

