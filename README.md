<p align="center">
  <a href="#key-features">Installation</a> •
  <a href="#screenshots">Screenshots</a> •
  <a href="#technology">Technology</a> •
  <a href="#how-to-use">How To Use</a> 
</p>

## Installation

* [Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki)<br>
  * Create a folder: 'C:\Tesseract-OCR' and install the Tesseract-OCR in that folder <br>
![tesseract](readme_img\tesseract-ocr.png)<br>
* [Python](https://www.python.org/downloads/)
  * Install Python. You do not need change any installation settings<br>
![python](readme_img\python.png)<br>
* [PyCharm](https://www.jetbrains.com/pycharm/download/?section=windows)<br>
  * Ensure you are selecting the Community Edition. On the website, scroll down, and you'll be able to locate the correct version<br>
  * Install PyCharm. You do not need change any installation settings<br>
  ![pycharm](readme_img\pycharm.png)<br>

* Github - I will send you a link where you will download a <b>zip file</b>.
  * Click 'Code', and then click 'Download as ZIP'<br>
  ![github](readme_img\github.png)<br>

### Setup
  * Start up PyCharm. You will be prompted to create a new project. Simply accept the preset settings
  * This will create this directory: PyCharmProjects\PythonProject in your user folder.
    * Example, 'C:\Users\JohnSmith\PyCharmProjects\PythonProject'
  * Extract the <b>zip file</b> into the PyCharmProjects\PythonProject folder that was created above
  * In PyCharm, verify extracted zip folder in the left-side project directory
  * In PyCharm, on the bottom left, look for the 'terminal' icon ![terminal](readme_img\terminal.png) and click it to open a terminal
  * In the terminal, type:
    * pip install -r throne_script-main-<your name>\requirements.txt
  * After the installation is done, double-click the python file in the project directory:
    * throne_script_polish_crystal_dungeon.py
  * On the top right, press the green arrow button to run the script

## Screenshots
The script has specific display requirements. I will need 2 or more specific screenshots of your screen.<br>
Depending on your setup, I may ask for more, and it might require HUD adjustments to meet requirements. 
### Screenshot 1
See the example and replicate this screenshot<br>
![package_screenshot.png](readme_img/package_screenshot.png)<br>
Enter Tyrant's Isle and the ensure following is shown:
 * <font color="yellow">An active target</font>
 * <font color="royalblue">Exit dungeon button</font>
 * <font color="red">Active (as in press enter and able to type) chat box
   * Note: Create one tab that has every filter turned off except for 'System' and 'Items'</font>
 * <font color="green">Manage Party button</font>
 * <font color="cyan">Manage Party display
   * Note: if this display is blocking something on this list, take another screenshot with the Manage Party display alone</font><br>
 * <font color="purple">Active Skills (able to cast/use)
   * Note:
   * It is ideal to set your skill keybindings to a single keyboard key
   * If it is set to a mouse thumb button, does not work
   * We will discuss more about this</font>

### Screenshot 2
Open up the Co-Op dungeon menu and take a screen

## Miscellaneous Settings
* Enable 'Auto-Move within Range to Attack Target'<br>
![target-setting.png](readme_img/target-setting.png)
* Enable 'Aimed Skills Lock-on to Current Target'<br>
![aimed_locked_skills.PNG](readme_img/aimed_locked_skills.PNG)
* Set a keybind to the Co-Op dungeon (preferably F11) <br>
* ![co-op_dungeon_button.png](readme_img/co-op_dungeon_button.png)