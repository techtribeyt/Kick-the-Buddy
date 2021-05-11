import keyboard
import win32api, win32con
import time
import pyautogui
import random

def click(x, y, delay = 0.01):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(delay)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    
start_button = 'p'

while True:
    if keyboard.is_pressed(start_button):
        mousePos1 = pyautogui.position()
        break
    

time.sleep(1)

while True:
    if keyboard.is_pressed(start_button):
        mousePos2 = pyautogui.position()
        break
    
    
WIDTH = mousePos2.x - mousePos1.x
HEIGHT = mousePos2.y - mousePos1.y

time.sleep(1)

coords = (mousePos1.x, mousePos1.y, mousePos2.x, mousePos2.y)

while True:
    if keyboard.is_pressed(start_button):
        break
    
    x = int(random.random() * WIDTH + coords[0])
    y = int(random.random() * HEIGHT + coords[1])
    click(x, y)


