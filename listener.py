from pynput.mouse import Button as MouseButton, Listener as MouseListener
import win32gui, numpy as np


def on_mouse_click(x, y, click, pressed):
    leidian_handle = win32gui.FindWindow(None, '雷电模拟器')
    leidian_rect = win32gui.GetWindowRect(leidian_handle)
    if click == MouseButton.left and pressed:
        if (leidian_rect[0] < x < leidian_rect[2]) and (leidian_rect[1] < y < leidian_rect[3]):
            print(tuple(np.array((x, y)) - np.array((leidian_rect[0], leidian_rect[1]))), ',')
def listener():
    with MouseListener(on_click=on_mouse_click) as mouse_listener:
        mouse_listener.join()
listener()


