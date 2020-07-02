import cx_Oracle, os, functools, sys,msvcrt

DASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DASE_DIR)
sys.path.insert(1, os.path.dirname((os.path.dirname(__file__))))

from conf import settings
from lib import ConnectDB
from lib.CheckResource import Check
from lib.CreateResource import Create
from lib.DropResource import Drop
from lib.ShowResource import Show

meun = {
    "创建": {"创建PDB", "创建用户", },
    "删除": {'删除PDB', '删除用户', },
}

def clear():os.system('cls')

check=Check()
create=Create()
drop=Drop()
show=Show()

exit_flag = True

while exit_flag:
    clear()
    for i, v in enumerate(meun.keys()):
        print(i, v)
    num_1 = input("请输入需要的操作: ").strip()
    if num_1 == 'q':
        exit_flag = False
        break
    if num_1.isdigit():
        num_1 = int(num_1)
        if num_1 <= len(meun):
            key_1 = list(meun.keys())[num_1]
            while exit_flag:
                clear()
                for i1, v1 in enumerate(meun[key_1]):
                    print(i1, v1)
                num_2 = input("请输入需要的操作: ").strip()
                if num_2 == 'q':
                    exit_flag = False
                    break
                elif num_2 == 'b':
                    break
                if num_2.isdigit():
                    num_2 = int(num_2)
                    if num_2 <= len(meun[key_1]):
                        key_2 = list(meun[key_1])[num_2]
                        if key_2 == "创建用户":
                            result = show.ShowPDB()
                            pdb_name = input("请输入PDB的名字: ").strip()
                            if check.CheckPDB(pdb_name):
                                user_name = input("请输入需要创建的用户名: ").strip()
                                while not check.CheckUser(pdb_name,user_name):
                                    if not check.CheckProfile(pdb_name):
                                        create.CreateProfile(pdb_name)
                                    if not check.CheckTBS(pdb_name,user_name):
                                        a = create.CreateTBS(pdb_name,user_name)
                                        print('表空间{}创建成功'.format(a).center(40,'#'))
                                    create.CreateUser(pdb_name,user_name)
                                    print("{} 用户创建成功".format(user_name).center(40,'#'))
                                    print("按任意键返回。")
                                    msvcrt.getwche()
                                else:
                                    print("{} 用户已存在".format(user_name))
                                    print("按任意键返回。")
                                    msvcrt.getwche()
                        elif key_2 == "删除用户":
                            result = show.ShowPDB()
                            pdb_name = input("请输入PDB的名字: ").strip()
                            if check.CheckPDB(pdb_name):
                                user_name = input("请输入需要删除的用户: ").strip()
                                while check.CheckUser(pdb_name, user_name):
                                    drop.DropUser(pdb_name,user_name)
                                    print("{} 用户删除成功".format(user_name).center(40, '#'))
                                    print("按任意键返回。")
                                    msvcrt.getwche()

