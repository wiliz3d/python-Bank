# PYTHON FILE ORGANIZER
# AUTOMATION CODE FOR ORGANIZING YOUR PYTHON FILES

import os
import shutil
import logging

def organise_files(directory_path, customer_categories =None):
    if customer_categories is None:
        categories = {
            'Images': ['png','jpg','jpeg','gif'],
            'Documents':['doc','docx','pdf','txt'],
            'Videos':['mp4','avi','mkv']
        }
    else:
        categories = customer_categories
        
        for folder_name in categories:
            folder_path = os.path.join(directory_path, folder_name)
            os.makedirs(folder_path,exist_ok = True)
            
        log_path = os.path.join(directory_path, 'organizer_log.txt')
        logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s-%(message)s')
        
        def move_file(file_path, destination_folder):
            shutil.move(file_path, os.path.join(destination_folder, os.path.basename(file_path)))
            logging.info(f"Moved: {os.path.basename(file_path)} to {destination_folder}")
            
        for root, _, files in os.walk(directory_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                
                if os.path.isfile(file_path):
                    file_extension = filename.split('.')[-1].lower()
                    
                    for folder_name, extentions in categories.items():
                        if file_extension in extentions:
                            destination_folder = os.path.join(directory_path, folder_name)
                            move_file(file_path, destination_folder)
                            break
                                        

custom_categories =   categories = {
            'Images': ['png','jpg','jpeg','gif'],
            'Documents':['doc','docx','pdf','txt'],
            'Videos':['mp4','avi','mkv']
        }

organise_files('your-directory_path', custom_categories)

