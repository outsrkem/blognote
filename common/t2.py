import os
BASE_DIR = os.path.abspath(os.curdir)
print(BASE_DIR)
# 对路径进行组合
# FILES_DIRS = os.path.join(BASE_DIR, 'conf', 'include', 'user.conf')
picAlt = 'data'
FILES_DIRS = os.path.join(BASE_DIR, "picAlt")
print(FILES_DIRS)
