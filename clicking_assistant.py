import keyboard
import win32api, win32con
import time
import pyautogui

def click(x, y, delay = 0.01):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(delay)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    
start_button = 'p'

while True:
    if keyboard.is_pressed(start_button):
        break
    

time.sleep(1)

while True:
    if keyboard.is_pressed(start_button):
        break
    
    mousePos = pyautogui.position()
    click(mousePos.x, mousePos.y)