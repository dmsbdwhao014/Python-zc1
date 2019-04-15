import os
PWD=os.getcwd()
if not os.path.exists(PWD + '\conf'):
    os.mkdir(PWD + '\conf')
if not os.path.exists(PWD + r'\bin'):
    os.mkdir(PWD + r'\bin')
if not os.path.exists(PWD + '\log'):
    os.mkdir(PWD + '\log')
if not os.path.exists(PWD + '\script'):
    os.mkdir(PWD + '\script')
