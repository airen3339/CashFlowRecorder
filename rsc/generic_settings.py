import pathlib

app_name = "CashFlowRecorder"

app_root_path = pathlib.Path.home() / "Documents" / app_name  # 软件根目录
app_root_path.mkdir(parents=True, exist_ok=True)

folders = ("database",)  # 需要创建的文件夹列表

is_empty = not any(app_root_path.iterdir())
if is_empty:  # 如果根目录下没有任何文件/文件夹，则生成以下文件夹
    for folder in folders:
        tmp = app_root_path / folder
        tmp.mkdir(parents=True, exist_ok=True)
