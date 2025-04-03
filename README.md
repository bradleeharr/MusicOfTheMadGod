# Music of the Mad God
Dynamic Music Support for Realm of the Mad God (RotMG)

##### Table of Contents  
* [Features](#Features)  
* [Elements](#Elements)
* [Purpose](#Purpose)  
* [Usage](#Usage)


<a name="Features"/>
<h1> Features </h1> 
 
* Customize your own playlist
* Set tracks for dungeons and different realm biomes.
* Smooth transitions with cross-fade in/out



<a name="Elements"/>
<h1> Elements </h1>

* Requires some image / video streaming to the application - uses `pywinauto` to take screenshots of the game application
* **Load Screens** (Dungeons)
  * Uses feature detection to detect load screens
* **Biomes** (in-Realm)
  * Categorizes each realm biome by average color


    
<a name="Purpose"/>
<h1> Purpose </h1> 


* The goal of this program is to add dynamic music integration in the game. 
* Currently, in various dungeons and in the Realm, there is no dynamic music integration.
* One example of this is when playing in the Realm:
  * In the main realm, the background track <a href="https://wangleline.bandcamp.com/track/odyssey" target="_blank">https://wangleline.bandcamp.com/track/odyssey</a> is repeated on end.
  * It's not quite suitable for the _intense_ situations you end up in when playing, like below:
   * <img src="https://github.com/user-attachments/assets/f7cc3a36-04ed-46bb-b05a-2450d89c986f" style="width:400px; max-width: 400px;">


<a name="Usage"/>
<h2>Usage</h2>

* Download or clone this repository
  * In a terminal, do: `git clone https://github.com/bradleeharr/MusicOfTheMadGod.git`
  * OR Download the ZIP and unzip it:
   <p align="center"> <img src="https://github.com/user-attachments/assets/191ca84c-35f6-47ce-803f-b9e41538001d"> </p>

* Place Tracks for each dungeon/area/realm in their respective folder. Example Below: 
  * <img src="https://github.com/user-attachments/assets/29c0fd3d-c44d-4452-993a-64a48027af87">
  * Note: Due to Copyright concerns that I have not yet wanted to deal with **This does not come with any music tracks**, and you will need to download and copy the tracks that you want into every folder.

* Run RotMG, then Mute in-game Music

* Install and Run the program:
   * Open a terminal and navigate to where the repository is located. Example using `git`
     * `git clone https://github.com/bradleeharr/MusicOfTheMadGod.git`
     * `cd MusicOfTheMadGod`
  * Make a python virtual environment, activate it, and install the requirements
     * `python -m venv .venv`
     * `.venv/Scripts/activate`
     * `pip install -r requirements.txt`
  * Run the program:
     * `python src/video-grabber.py`


<h1> Help! </h1>

* If you have any issue installing, send an issues ticket!
* If you have any ideas for contributions (defaut/recommended tracks to include, improvements to the detection, etc.) Please make a request!

<h1>Credits/Recommended Soundtracks</h1>

 * Download the Realm of the Mad God Soundtrack [here](https://wangleline.bandcamp.com/album/realm-of-the-mad-god-exalt-ost-vol-1)
 * Download other tracks by WangleLine! [here](https://wangleline.bandcamp.com/)

