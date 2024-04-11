# folder-sync

Repo for synchronization of source folder to destination folder

## Requirements

- Python3 (tested with 3.9.2)

## Usage

Started as an python script through the command line with the following arguments:

```python3 main.py -s <source_folder_path> -d <destination_folder_path> -t <seconds) -l <logs_directory> --debug```

### Arguments 
 - Source folder should exist
 - Destination folder will be created if it doesnt exist
 - Timeout should be greater than 0
 - `--debug` flag is optional and will enable aditional logs
