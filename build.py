from PyInstaller.__main__ import run

opts = [
    'src/main.py',
    '--onefile',
    '--add-data=img;img',                   # 添加整个 img 目录，打包后保持文件夹结构
    '--uac-admin',                  # 请求管理员权限
    '--name=AutoAcceptCall'            # 输出的exe文件名
]

run(opts)