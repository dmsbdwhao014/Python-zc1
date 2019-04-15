import zipfile,tarfile,shutil,os

# if not os.path.exists("testzip.zip"):
#     z = zipfile.ZipFile("testzip.zip","a")
#     z.write("ini1")
#     z.write("ini2")
#     z.close()
# if os.path.exists("testzip.zip"):
#     os.remove("ini1")
#     os.remove("ini2")
#     z1 = zipfile.ZipFile("testzip.zip","r")
#     z1.extractall()
#     z1.close()
#

shutil.copyfile("ini1","ini3")
shutil.copyfile("ini1","ini4")
t = tarfile.TarFile("testtar.tar","w")
t.addfile("ini3")
t.addfile("ini4")
t.close()






