import pyautogui
import time

screenWidth, screenHeight = pyautogui.size()


for i in range(50):
    im1 = pyautogui.screenshot('test.png') # Not fast but not slow, may take ~100 ms

    
    try:
        location = pyautogui.locateOnScreen('images/ref/nexus.png', confidence=0.5)
        print(location)
        dungeon = ''
        print(f"Dungeon {dungeon}")
    except Exception as e:
        print(e)
    

   

    time.sleep(1)