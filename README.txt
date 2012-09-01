SPACE DOMINATION
Created by Jami Couch
Version 0.3 September 1, 2012

Licensed under GPL v3.0 or later.

ATTRIBUTIONS:
	Explosion sprites were taken from http://hasgraphics.com/phaedy-explosion-generator/ courtesy of Phaedy

AUTHOR NOTES:
	Thanks everyone for trying out my game, Space Domination. It is my sincere hope that you have an enjoyable experience.
	New features in version 0.3:
		- Redesigned menu system
		- Profiles
		- More than one player flyable ship
		- Stat tracking
	
	Anyone interested in messing with some advanced features that haven't been fully implemented, you can go into consts.py and alter the FRAMERATE, the GAMESPEED, and PARALLAX:
		- FRAMERATE - this is exactly what it sounds like, the game will update this many times per second
		- GAMESPEED - this is how many times per second the physics should update 1 full unit - so if something had a speed of "1", it will move GAMESPEED number of pixels per second
		- PARALLAX - (experimental) set this to lower than 1.0 (~0.7 is a good number) and the background will scroll more slowly than the ship is moving, giving the illusion of depth
	
	Thanks,
		Jami Couch

INSTALLATION: 
Space Domination depends on Python 2.7 and Pygame:	
	1. Python 2.7 http://python.org/download/releases/2.7.3/
		Windows users: Install 32-bit python (not x64!)
		Debian/Ubuntu: sudo apt-get install build-dep python2.7
	2. Pygame http://www.pygame.org/download.shtml
		Windows users: Install 32-bit pygame for python 2.7
		Debian/Ubuntu: sudo apt-get install python-pygame
You may download the latest version of Space Domination from:
	- http://code.google.com/p/space-domination/downloads/list

RUN THE GAME:

	Windows:
		- Double-click SpaceDominationMain.py or "Run SpaceDomination.bat"
	Linux/OSX:
		- (Experimental) Double-click "Run SpaceDomination.sh"
	All:
		- Open a console/shell
		- Navigate to the SpaceDomination folder (where SpaceDominationMain.py is located)
		- Run the following command:
			python SpaceDominationMain.py

