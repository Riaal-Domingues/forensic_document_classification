import os
import sys
import re
from tqdm import tqdm   #To display progress bars

# Import own defined functions and classes
print("Initialising the program")
modules_path = os.path.join('..','..','src','modules','')
sys.path.append(modules_path)
import eflp

src_data_root = os.path.join("..","..","data","raw")
dst_data_root = os.path.join("..","..","data","processed")

#mail_src = os.path.join(src_data_root,"maildir","allen-p")
#mail_dst = os.path.join(dst_data_root,"maildir","allen-p")
mail_src = os.path.join(src_data_root,"maildir","arnold-j")
mail_dst = os.path.join(dst_data_root,"maildir","arnold-j")


email = eflp.Email_Forensic_Processor()

# Build the file list for processing
src_dst = []
no_files = 0;
#no_files = 517403
print("Building the file list")
with tqdm(total=no_files) as pbar:
    for dir_path, dirs, files in os.walk(mail_src):
        #print(dir_path)
        src_path = dir_path
        dst_path = dir_path.replace("/raw/","/processed/")
        #print(dir_path)
        for file in files:
            #print(file)
            no_files = no_files + 1
            if (file != '') and (not re.search(r'^\.',file)):
                file_src_path = os.path.join(src_path,file)
                file_dst_path = file_src_path.replace("/raw/","/processed/")
                file_dst_path = file_dst_path + "json"
                src_dst.append((file_src_path,file_dst_path))
                pbar.update(1)
                #print("   ",file_src_path,file_dst_path)

# Preprocess the emails and store them
print("Preprocessing the files")

with tqdm(total=no_files) as pbar:
    for file_pair in src_dst:
        if os.path.exists(file_pair[1]):
            print("file exists")
        else:
            email.initMail(file_pair[0])
            email.saveMail(file_pair[1])
        pbar.update(1)

