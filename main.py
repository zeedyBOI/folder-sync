import os
import sys
import argparse
from logger import Logger

def is_absolute_path(path: str):
    return path.startswith("/")


def main():
    source_folder : str
    destination_folder : str
    timeout : int
    log_path : str
    debug = False
    
    parser = argparse.ArgumentParser(description="Folder syncer script.")

    # Define command-line arguments
    parser.add_argument('-s', '--source_folder', required=True ,type=str, help='Source folder from where the file will be synced')
    parser.add_argument('-d', '--destination_folder', required=True, type=str, help='Destination folder to where the folder will be copied to')
    parser.add_argument('-t', '--time', required=True, help='Time between sync check')
    parser.add_argument('-l', '--log_path', required=True, help="Destination folder of logs")
    parser.add_argument('--debug', action=argparse.BooleanOptionalAction, help="Enable debug Logs")

    # Parse the command-line arguments
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
    else:
        print("Log path is required")
        sys.exit(-1)
    
    Logger(log_path=log_path, debug=debug)

    # Access the values using args.processes, args.traffic_influence, and args.operation
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
        if not os.path.isdir(source_folder):
            raise Exception(f"Source folder ({source_folder}) does not exist")
        
        if not os.path.isdir(destination_folder):
            path_split = destination_folder.split('/')
            print(path_split)
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
                Logger.debug(f"CHECKING IF DIRECTORY ({path_control}) EXISTS - {os.path.isdir(path_control)}")
                if not os.path.isdir(path_control):
                    os.mkdir(path_control)
                i += 1
                if i >= len(path_split):
                    break
                path_control += f"/{path_split[i]}"
        Logger.info("DONE")
    except Exception as e:
        Logger.error(f"Error on main [{e}]")
        sys.exit(-1)
    
if __name__ == "__main__":
    main()
