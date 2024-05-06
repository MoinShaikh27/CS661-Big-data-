import os

exec_path = os.getcwd()

exec_folder = exec_path.split(os.sep)[-1]

if exec_folder == "Submission_Assignment1":
    path = "./ISOCONTOUR_Q1/Data"
elif exec_folder == "ISOCONTOUR_Q1":
    path = "./Data"
else:
    print("Execute from within the Assignment folder")
    raise Exception("Execute from within the Assignment folder")

file_name = "Isabel_2D.vti"
