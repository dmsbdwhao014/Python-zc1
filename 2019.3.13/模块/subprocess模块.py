import subprocess

# result = subprocess.call('ipconfig')
# print(result)

subprocess.check_call(["ipconfig"])
subprocess.check_call("exit 1",shell=True)
1

