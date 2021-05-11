import cv2
import keyboard
import pyautogui
import time
import numpy as np
import win32api, win32con

### TUNABLE PARAMETERS ###
# button to press when selecting region and quitting
start_button = "p"

### END TUNABLE PARAMETERS ###

# position mouse to top left corner and press start_button (whatever you define) to let program record mouse location
while True:
    if keyboard.is_pressed(start_button):
        mousePos1 = pyautogui.position()
        break
    
time.sleep(1)
 
# position mouse to bottom right corner and press start_button (whatever you define) to let program record mouse location
while True:
    if keyboard.is_pressed(start_button):
        mousePos2 = pyautogui.position()
        break


# use both mouse positions to make the following variables
WIDTH = mousePos2.x - mousePos1.x
HEIGHT = mousePos2.y - mousePos1.y

min_upgrade_icon_size = 0

time.sleep(1)

coords = (mousePos1.x, mousePos1.y, mousePos2.x, mousePos2.y)
def click(x, y, delay = 0.01):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(delay)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def doNothing(arg):
    pass


# code with trackbars
'''
cv2.namedWindow('Track Bars', cv2.WINDOW_NORMAL)

cv2.createTrackbar('min_blue', 'Track Bars', 0, 255, doNothing)
cv2.createTrackbar('min_green', 'Track Bars', 0, 255, doNothing)
cv2.createTrackbar('min_red', 'Track Bars', 0, 255, doNothing)

cv2.createTrackbar('max_blue', 'Track Bars', 0, 255, doNothing)
cv2.createTrackbar('max_green', 'Track Bars', 0, 255, doNothing)
cv2.createTrackbar('max_red', 'Track Bars', 0, 255, doNothing)

scrot = np.array(pyautogui.screenshot(region = (mousePos1.x, mousePos1.y, WIDTH, HEIGHT)))

while True:
    #reading the trackbar values for thresholds
    min_blue = cv2.getTrackbarPos('min_blue', 'Track Bars')
    min_green = cv2.getTrackbarPos('min_green', 'Track Bars')
    min_red = cv2.getTrackbarPos('min_red', 'Track Bars')
    
    max_blue = cv2.getTrackbarPos('max_blue', 'Track Bars')
    max_green = cv2.getTrackbarPos('max_green', 'Track Bars')
    max_red = cv2.getTrackbarPos('max_red', 'Track Bars')
    
    #using inrange function to turn on the image pixels where object threshold is matched
    mask = cv2.inRange(scrot, (min_blue, min_green, min_red), (max_blue, max_green, max_red))
    #showing the mask image
    cv2.imshow('Mask Image', mask)
    cv2.imshow('HSV Image', scrot)

    # checking if q key is pressed to break out of loop
    key = cv2.waitKey(25)
    if keyboard.is_pressed(start_button):
        break
print(f'min_blue {min_blue}  min_green {min_green} min_red {min_red}')
print(f'max_blue {max_blue}  max_green {max_green} max_red {max_red}')'''
    

lower_buddy = (0, 0, 39)
upper_buddy = (15, 255, 255)

lower_resume = (137, 0, 0)
upper_resume = (255, 85, 120)

lower_weapons = (0, 123, 116)
upper_weapons = (88, 255, 195)

lower_buy_weapon = (109, 86, 15)
upper_buy_weapon = (255, 195, 71)

lower_exit_weapon = (163, 0, 0)
upper_exit_weapon = (255, 42, 255)

lower_ko = (255, 148, 0)
upper_ko = (255, 243, 255)

while True:
    scrot = np.array(pyautogui.screenshot(region = (mousePos1.x, mousePos1.y, WIDTH, HEIGHT)))

    mask = cv2.inRange(scrot, lower_ko, upper_ko)
    contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    for j in range(1):
        if contours:
            (x_min, y_min, box_width, box_height) = cv2.boundingRect(contours[j])
            margin = 15
            cv2.rectangle(scrot, (x_min - margin, y_min - margin), (x_min + box_width + margin, y_min + box_height + margin), (0, 255, 0), 2)
            #for i in range(100):
                #click(coords[0] + x_min + box_width // 2, coords[1] + y_min + box_height // 2)
                #pass
    cv2.imshow('image',scrot)
    cv2.waitKey(5)
    if keyboard.is_pressed(start_button):
        break


    
#destroying all windows
cv2.destroyAllWindows()