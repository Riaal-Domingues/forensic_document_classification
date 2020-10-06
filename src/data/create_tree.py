import os

src_data_root = os.path.join("..","..","data","raw")
#dst_data_root = os.path.join("..","..","data","processed")
#dst_experiment_root = os.path.join("..","..","data","processed")

print("Creating the required directories under processed.")
for dir_path, dirs, files in os.walk(src_data_root):
    dst_path = dir_path.replace("raw","processed")
    for dir in dirs:
        directory = os.path.join(dst_path,dir)
        experiment_directory = directory.replace("maildir","experimental_data")
        os.makedirs(directory, mode=0o777, exist_ok=True)
        os.makedirs(experiment_directory, mode=0o777, exist_ok=True)
        #print(directory)
print("Directory tree created.")
