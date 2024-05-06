import os
from pathlib import Path

exec_path = os.getcwd()

exec_folder = exec_path.split(os.sep)[-1]

if exec_folder == "Submission_Assignment1":
    path = "./VOLUME_RENDERING/Data"
elif exec_folder == "VOLUME_RENDERING":
    path = "./Data"
else:
    print("Execute from within the Assignment folder")
    raise Exception("Execute from within the Assignment folder")

file_name = "Isabel_3D.vti"

file_path = Path(path).joinpath(file_name).resolve()
