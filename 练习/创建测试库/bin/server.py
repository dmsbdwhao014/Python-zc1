import cx_Oracle, os, functools, sys, msvcrt

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
    "创建": {"创建数据库", "创建用户", },
    "删除": {'删除数据库', '删除用户', },
}


def clear(): os.system('cls')


check = Check()
create = Create()
drop = Drop()
show = Show()

exit_flag = True
global key_2

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
                num_2 = input("当前选择的是 " + key_1 + " , 请继续输入需要的操作的序号: ").strip()
                if num_2 == 'q':
                    exit_flag = False
                    break
                elif num_2 == 'b':
                    break
                if num_2.isdigit():
                    num_2 = int(num_2)
                    if num_2 <= len(meun[key_1]):
                        key_2 = list(meun[key_1])[num_2]
                        print("当前的操作是 {}".format(key_2))
                        if key_2 == "创建用户":
                            result = show.ShowPDB()
                            pdb_name = input("请输入PDB的名字: ").strip()
                            if check.CheckPDB(pdb_name):
                                user_name = input("请输入需要创建的用户名: ").strip()
                                if not check.CheckUser(pdb_name, user_name):
                                    if not check.CheckProfile(pdb_name):
                                        create.CreateProfile(pdb_name)
                                    if not check.CheckTBS(pdb_name, user_name):
                                        a = create.CreateTBS(pdb_name, user_name)
                                        print('表空间{}创建成功'.format(a).center(40, '#'))
                                    create.CreateUser(pdb_name, user_name)
                                    show.ShowUser(pdb_name, user_name)
                                    show.ShowCONN(pdb_name, user_name)
                                    print("{} 用户创建成功".format(user_name).center(40, '#'))
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
                                show.ListUser(pdb_name)
                                user_name = input("请输入需要删除的用户: ").strip()
                                if check.CheckUser(pdb_name, user_name):
                                    drop.DropUser(pdb_name, user_name)
                                    print("{} 用户删除成功".format(user_name).center(40, '#'))
                                    print("按任意键返回。")
                                    msvcrt.getwche()
                                else:
                                    print("{} 用户删除不成功".format(user_name).center(40, '#'))
                                    print("按任意键返回。")
                                    msvcrt.getwche()
                        elif key_2 == "创建数据库" or key_2 == "删除数据库":
                            result = show.ShowPDB()
                            pdb_name = input("请输入PDB的名字: ").strip()
                            if check.CheckPDB(pdb_name):
                                if key_2 == "创建数据库":
                                    print("{} 数据库已存在".format(pdb_name).center(40, '#'))
                                    print("按任意键返回。")
                                    msvcrt.getwche()
                                elif key_2 == "删除数据库":
                                    drop.DropPDB(pdb_name)
                                    print("{} {} 成功".format(pdb_name, key_2).center(40, '#'))
                                    print("按任意键返回。")
                                    msvcrt.getwche()
                                key_2 = "创建用户"
                            else:
                                if key_2 == "创建数据库":
                                    result1 = create.CreatePDB(pdb_name)
                                    if check.CheckPDB(pdb_name):
                                        print("{} {} 成功".format(pdb_name, key_2).center(40, '#'))
                                        print("按任意键返回。")
                                        msvcrt.getwche()
                                    else:
                                        print("{} {} 失败".format(pdb_name, key_2).center(40, '#'))
                                        print("失败原因",result1)
                                        print("按任意键返回。")
                                        msvcrt.getwche()
                                else:
                                    print("{} 数据库不存在".format(pdb_name).center(40, '#'))
                                    print("按任意键返回。")
                                    msvcrt.getwche()
