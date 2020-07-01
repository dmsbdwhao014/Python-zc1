import cx_Oracle, os, functools
from conf import settings
import ConnectDB
import CheckResource
import CreateResource
import DropResource
import GetIP
import ShowResource

exit_flag = False
while exit_flag is not True:
    
    if __name__ == '__main__':
        show = ShowResource()
        print('PDB'.center(20, '='))
        for name,mode in show.ShowPDB():
            print('NAME: ',name,' OPEN_MODE:',mode)
