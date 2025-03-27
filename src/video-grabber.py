import cv2
import os
import numpy as np
import pyaudio
import time

import vlc



from pywinauto import Desktop, Application



app = Application(backend="uia").connect(title="RotMGExalt")
app.RotMGExalt.set_focus()

window = app.window(title="RotMGExalt")

tracks = {
    'nexus' : '12_Hadenfeer.flac',
    'realm-novice' : '02_Odyssey.flac',
    'sprite' : '15_Arc_Sancts.flac',
    'deep-sea-abyss' : '11_Mechanical_Ambivalence.flac'
}
player = vlc.MediaPlayer()

location = None
last_location = None

while True:
    game_image = window.capture_as_image()
    
    for loc in tracks.keys():
        dir = f'images/ref/{loc}/'
        for ref in os.listdir(dir):
            try:
                # Try with opencv template matching
                game_image = cv2.cvtColor(np.array(game_image), cv2.COLOR_RGB2BGR) 
                target_image = cv2.imread(dir + ref)
                result = cv2.matchTemplate(game_image, target_image, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(result)

                threshold = 0.6
                
                print(f"[DEBUG] {ref}: {max_val}")

                if max_val >= threshold:
                    x, y =  max_loc
                    location = loc
                    print(f"[DEBUG] {ref} Match found at ({x}, {y})")
            
            except Exception as e:
                print(f"[ERROR] {e}")
    
        if location != last_location: 
            last_location = location
            track = f"tracks/{tracks[location]}"
            print(f"Track: {track}")

            
            media = vlc.Media(track)

            
            player.set_media(media)
            player.play()

        if not location:
            print(location)
            player.stop()






#screenWidth, screenHeight = pyautogui.size()



#for i in range(50):
    #im1 = pyautogui.screenshot('test.png') # Not fast but not slow, may take ~100 ms

    
    #try:
        #location = pyautogui.locateOnScreen('images/ref/nexus.png', confidence=0.5)
        #print(location)
        #dungeon = ''
        #print(f"Dungeon {dungeon}")
    #except Exception as e:
     #   print(e)
    