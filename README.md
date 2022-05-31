# SelectZones
 
This program uses PyQt5 library as a GUI framework.

It is designed for scientific purposes and is property of the <i><b>FNCSR</b> (French National Center of Scientific Research).</i>

The UI was generated with Qt Designer and modified by the author in the interface_setup.py file. Please make sure to not overwrite the file by generating with the same name.

## TL;DR

The point of this program is to display an image that is imported locally from the device. That image will be spread out in the label. You are then able to draw rectangles with your mouse and adjust the last one you made directly with your mouse. The other way to adjust any rectangle of your choice is to use the bottom left panel with the sample boxes in ascending order. The values displayed on the screen are microns as intended. You can remove drawn rectangles at any given time by just clicking on the cross. You can flip the image horizontally and adjust the contrast (note that changing the contrast will NOT affect the exported data). Finally, you can export the data by clicking the save button and choose the directory in which you want the corresponding folder to be created (the created folder's name is the same as the name of the selected image).

## The exported data

The folder is composed of another/other folder(s) that contain(s) the cropped image selected by the rectangles with the text file containing the data of each column of pixel inside that rectangle.

__Author__ : Ayoub BEN FRAJ

__Last Update__ : 2022-05-31 <i>(YYYY-MM-DD)</i>

__Contact__ : https://www.linkedin.com/in/abenfraj/
