import os
app_name = "CashFlowRecorder"
app_root_path = os.path.expanduser(f"~/Documents/{app_name}/")
folder_tuple=("database",)
if not os.path.exists(app_root_path):
    os.makedirs(app_root_path)
    for folder in folder_tuple:
        os.makedirs(app_root_path+folder)
