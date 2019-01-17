# Python --version 3.6.4

import sys
from cx_Freeze import setup, Executable # pip install cx_Freeze==5.1.1  (version : 5.1.1) /  python version 3.7에서 사용 불가
import os

project_name = "Ace Vision"     # exe파일로 만들 이름.
exe_name = "Ace Vision"         # exe파일로 만들 이름
version = "1.0.0"
main_script = "main.py"         # 컴파일하는 .py이름
optimization = 0

# main.py에 내가 import한 경로와 모듈 (폴더/모듈.py)
resources = ["QR_SS_Detect/QR_SS_Detect.py", "RivetDetect/RivetDetect.py"]

# 내부에 있는 모든 import한 모듈들... 총집합
packages = ["numpy", "imutils", "cv2", "more_itertools","Image","decode","PIL", "math", "datetime", "time", "os", "tkinter", "pyzbar","pylibdmtx.pylibdmtx"]

base = None
if sys.platform == "win32":
    base = "Win32GUI"
    executables = [Executable("main.py", base=base, targetName=exe_name + ".exe")]

    os.environ['TCL_LIBRARY'] = sys.exec_prefix + "\\tcl\\tcl8.6"
    os.environ['TK_LIBRARY'] = sys.exec_prefix + "\\tcl\\tk8.6"
    resources.extend([sys.exec_prefix + "\\DLLs\\tcl86t.dll", sys.exec_prefix + "\\DLLs\\tk86t.dll"])

elif sys.platform == "darwin":
    executables = [Executable("main.py", base=base)]

build_exe_options = {"optimize": optimization, "include_files": resources, "packages": packages}
mac_options = {"bundle_name": exe_name}

setup(name=project_name,
      version=version,
      options={"build_exe": build_exe_options},
      bdist_mac=mac_options,
      executables=[Executable(main_script, base=base, targetName=exe_name + ".exe")]
      )