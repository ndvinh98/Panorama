# Panorama
<li>This repository contains an implementation of multiple image stitching

### Requirement
<li>python3 (or higher)

##### *Install opencv-contrib-python since some none-free features are not avilable*

    pip install opencv-contrib-python==3.4.2.17 --force-reinstall

##### You will need to install some package:
<li>numpy
<li>matplotlib

##### Project Structure : 
		
		|_ main.py
		|_ utils.py
        |_ features.py
        |_ stitch.py
		|	
		|_ data - |
		|			|_ myhouse
		|			|			|- 001.jpg
		|			|			|- 002.jpg
		|			|_ BK
		|			|			|- H1.jpg
		|			|			|- H2.jpg
		|			|			|- H3.jpg
		|			|.....etc.....
        |_result -|
        |          |- myhouse.jpg
        |          |- BK.jpg
        |		   |.....etc.....
