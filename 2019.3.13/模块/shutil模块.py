import shutil

# 拷贝文件到另一个文件
shutil.copyfileobj(open("ini","r",encoding="utf-8"),open("ini1","w",encoding="utf-8"))
# 拷贝文件
shutil.copyfile("ini","ini2")
# 拷贝文件和权限
shutil.copy("ini","ini2")
# 拷贝文件和状态
shutil.copy2("ini","ini2")
# 拷贝文件的权限,不拷贝内容
shutil.copymode("ini","ini1")
# 拷贝文件的元信息，不拷贝内容
shutil.copystat("ini","ini1")

# 忽略拷贝文件
shutil.ignore_patterns()
# 拷贝文件夹 symlinks
shutil.copytree("dir1","dir2",ignore=shutil.ignore_patterns("*.pyc","*.log"))
# 递归删除文件夹
shutil.rmtree("dir1")
# 移动文件
shutil.move("file1","file2")
# 压缩文件
shutil.make_archive("archive","gzip",root_dir="D:/Program")
# 解压缩
shutil.unpack_archive()
