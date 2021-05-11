import cv2
import keyboard
import pyautogui
import time
import numpy as np
import win32api, win32con

### TUNABLE PARAMETERS ###
# button to press when selecting region and quitting
start_button = "p"


# color thresholds that allow program to detect the buddy and various icons
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


# the KO contour must have an area of at least 7% of the screen (determined experimentally)
KO_THRESH = 0.07

# ai will attempt to buy weapons every 5 rounds (doing so every round slows it down a bit)
buy_weapon_frequency = 5

### END TUNABLE PARAMETERS ###


min_upgrade_icon_size = 0

# we don't check for KO immediately after we resume the game because the buddy is full health
attacks_before_ko_check = 1


### BELOW WE DEFINE THE AREA USING TECHNIQUE MENTIONED IN VIDEO
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

time.sleep(1)

coords = (mousePos1.x, mousePos1.y, mousePos2.x, mousePos2.y)

# function for clicking (x,y)
def click(x, y, delay = 0.01):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(delay)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    
    
# function clicks color specified by arguments
def click_color(lower, upper):
    scrot = np.array(pyautogui.screenshot(region = (mousePos1.x, mousePos1.y, WIDTH, HEIGHT)))
    mask = cv2.inRange(scrot, lower, upper)
    contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    if contours:
        (x_min, y_min, box_width, box_height) = cv2.boundingRect(contours[0])
        click(coords[0] + x_min + box_width // 2, coords[1] + y_min + box_height // 2, delay = 0.1)
     
# code to buy a weapon
def try_upgrades():
    global min_upgrade_icon_size
    # click icon to go to weapons page
    click_color(lower_weapons, upper_weapons)
    time.sleep(2)
    
    
    # find clickable places
    coords_to_click = []
    
    scrot = np.array(pyautogui.screenshot(region = (mousePos1.x, mousePos1.y, WIDTH, HEIGHT)))

    mask = cv2.inRange(scrot, lower_buy_weapon, upper_buy_weapon)
    contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    if min_upgrade_icon_size == 0:
        min_upgrade_icon_size = int(cv2.contourArea(contours[0]) * 0.9) # multiplying to ensure we don't have false negatives
        
    # identifies all lock icons
    for j in range(10):
        if cv2.contourArea(contours[j]) < min_upgrade_icon_size:
            break
        (x_min, y_min, box_width, box_height) = cv2.boundingRect(contours[j])
        #drawing a rectangle around the object with 15 as margin
        x_mid = x_min + box_width // 2
        y_mid = y_min + box_height // 2
        score = 10 * y_mid + x_mid
        coords_to_click.append((coords[0] + x_mid, coords[1] + y_mid, score))
      
    # sorts such that we go left to right, top to down
    coords_to_click.sort(key=lambda tup: tup[2])
    
    # we click all lock icons in order
    for x, y, _ in coords_to_click:
        click(x, y, delay = 0.2)
        
    time.sleep(1)
    
    # exit the page to start another round
    click_color(lower_exit_weapon, upper_exit_weapon)
    
# function that takes 20 screenshots so that it is sure the buddy is knocked out
# I use so many to make sure the ai does not accidentally click a button and go to another webpage (as shown in video lol)
def is_knocked_out():
    ko = False
    for i in range(20):
        scrot = np.array(pyautogui.screenshot(region = (mousePos1.x, mousePos1.y, WIDTH, HEIGHT)))
        mask = cv2.inRange(scrot, lower_ko, upper_ko)
        contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        if contours:
            #if any contours are found we take the biggest contour and get bounding box
            (x_min, y_min, box_width, box_height) = cv2.boundingRect(contours[0])
            area_pct = cv2.contourArea(contours[0]) / (WIDTH * HEIGHT)
            ko = ko or area_pct >= KO_THRESH
        if keyboard.is_pressed(start_button):
            break
        time.sleep(0.1)
    return ko


rounds = 0
attacks_post_ko = 0
while True:
    
    # if knocked out
    if attacks_post_ko >= attacks_before_ko_check and is_knocked_out():
        rounds += 1
        attacks_post_ko = 0
        # either start next round or try buying weapons
        if rounds % buy_weapon_frequency == 0:
            time.sleep(0.2)
            try_upgrades()
            time.sleep(0.2)
        else:
            click_color(lower_resume, upper_resume)
    
    else:
        # find buddy and click it 20 times
        attacks_post_ko += 1
        scrot = np.array(pyautogui.screenshot(region = (mousePos1.x, mousePos1.y, WIDTH, HEIGHT)))
        mask = cv2.inRange(scrot, lower_buddy, upper_buddy)
        contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        if contours:
            (x_min, y_min, box_width, box_height) = cv2.boundingRect(contours[0])
            for i in range(20):
                click(coords[0] + x_min + box_width // 2, coords[1] + y_min + box_height // 2)
            
    # lets us stop the program if we hold start_button  
    if keyboard.is_pressed(start_button):
        break