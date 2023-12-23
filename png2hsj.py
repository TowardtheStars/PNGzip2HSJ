import pyautogui, keyboard
from zipfile import ZipFile
import win32gui, numpy as np
import os, re
from os.path import join as pathjoin
from tqdm import tqdm

import time

leidian_handle = win32gui.FindWindow(None, '雷电模拟器')
with open('配置.txt', encoding='utf8') as file:
    png_package_path = file.readline().strip()
    simulator_share_folder_root = file.readline().strip()
    template_folder_name = '倒模'

template_folder_path = os.path.join(simulator_share_folder_root, template_folder_name)  # 模板 png 临时文件夹
if os.path.exists(template_folder_path):
    [os.remove(pathjoin(template_folder_path, p)) for p in os.listdir(template_folder_path)]
    os.rmdir(template_folder_path)
os.makedirs(template_folder_path, exist_ok=True)


init_pos = [
    (255, 940),
    (82, 781),
    (406, 294),
    (327, 192),
    (439, 961),
    (504, 973),
]

import_pos = [
    (333, 56),
    (100, 215),
    (320, 182),
    (430, 956),
    (211, 965),
    (217, 917),
    (507, 967),
]

run_flag = True
def import_png(init=False):
    if init:
        poses = init_pos
    else:
        poses = import_pos
    
    for p in poses:
        if run_flag:
            win32gui.BringWindowToTop(leidian_handle)
            leidian_rect = win32gui.GetWindowRect(leidian_handle)
            original_pos = np.array(leidian_rect[0:2])
            current_pos = np.array(pyautogui.position())
            target = (original_pos + np.array(p))
            pyautogui.leftClick(*target)
            pyautogui.moveTo(*current_pos)
            time.sleep(0.7)

def stop():
    global run_flag
    run_flag = False
    print('已停止')
keyboard.add_hotkey('F12', stop)
print('按住 F12 停止导入')

dst_path = pathjoin(template_folder_path, '00.png')
with ZipFile(png_package_path, mode='r') as zipfile:
    namelist = zipfile.namelist()
    namelist = [n.encode('cp437').decode('gbk') for n in namelist if n.endswith('.png')]
    # namelist.remove(r'格式导出由_幻梦de绮梦科技提供_.txt')
    namelist.sort(key=lambda x: int(re.search(r'\d*', x).group()))
    
    init = True
    for name in tqdm(namelist):
        if run_flag:
            zipfile.extract(name.encode('gbk').decode('cp437'), template_folder_path)
            if os.path.exists(dst_path):
                os.remove(dst_path)
            os.rename(pathjoin(template_folder_path, name.encode('gbk').decode('cp437')), dst_path)
            
            import_png(init)
            init = False
        
