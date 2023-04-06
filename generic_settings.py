import os
app_name = "CashFlowRecorder"
app_root_path = os.path.expanduser(f"~/Documents/{app_name}/")
folders = ("database",)
if not os.path.exists(app_root_path):
    os.makedirs(app_root_path)
    for folder in folders:
        os.makedirs(app_root_path+folder)
