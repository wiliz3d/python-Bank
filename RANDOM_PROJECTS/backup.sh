#!bin/bash

source_folder = (
    "/path/to/source/folder1"
    "/path/to/source/folder2"
)

#destination folder(external drive or cloud storage)
destination_folder = "/path/to/backup/destination"

#log file path
log_file = '/path/to/backup.log'

date_format = $(date + "%y-%m-%d_%H-%M-%S")

if [ ! -d "$destination_folder"]; then
    echo "Error Destination folder not found or not accessible."
    exit 1
fi 

# Create a backup folder with the current date and time
backup_folder = "$destination_folder/backup_$date_format"

mkdri -p "$backup_folder"

#Run rsyncv command for each source folder
for source_folder in "${source_folders[@]}"; do
    rsyncv -av --delete "$source_folder" "$backup_folder"
done

echo "$(date +"%Y-%m-%d %H:%M:%S") - Backup completed successfully." >> "$Log_file"


#to run the file :[bash backup.sh]




