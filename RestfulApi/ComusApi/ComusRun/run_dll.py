import os
import platform
import ctypes
import sys

def run_dll(project_dir):
    system = platform.system()
    current_file_path = os.path.abspath(__file__)
    current_dir_path = os.path.dirname(current_file_path)

    if system == 'Windows':
        dll_path = os.path.join(current_dir_path, 'WinComus.dll')
        comusModel = ctypes.CDLL(dll_path)
        comusModel.RunModel.argtypes = [ctypes.c_wchar_p]
        comusModel.RunModel.restype = ctypes.c_int
        try:
            result = comusModel.RunModel(project_dir)
            print("DLL returned:", result)
        except Exception as e:
            print("Other Error:", e)
    elif system == 'Linux':
        dll_path = os.path.join(current_dir_path, 'LinuxComus.so')
        comusModel = ctypes.CDLL(dll_path)
        comusModel.RunModel.argtypes = [ctypes.c_char_p]
        comusModel.RunModel.restype = ctypes.c_int
        try:
            result = comusModel.RunModel(ctypes.c_char_p(project_dir.encode('utf-8')))
            print("DLL returned:", result)
        except Exception as e:
            print("Other Error:", e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_dll.py <project_dir>")
    else:
        run_dll(sys.argv[1])
