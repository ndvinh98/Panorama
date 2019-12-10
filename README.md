# Panorama
<li>This repository contains an implementation of multiple image stitching

### Requirement
<li>python3 (or higher)

### *Install opencv-contrib-python since some none-free features are not avilable*

    pip install opencv-contrib-python==3.4.2.17 --force-reinstall

### You will need to install some package:
<li>numpy
<li>matplotlib

### Project Structure : 
		
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
		|          		|- myhouse.jpg
		|          		|- BK.jpg
		|		   	|.....etc.....

### To run : 
<li>if you want to resize images in input folder:

    `python main.py -i <input dir> -o <output dir -r 1> `
    
<li>Otherwise
	
    `python main.py -i <input dir> -o <output dir> `
    
    
## Outputs !! 

<center>
<img src="result/myhouse.jpg" ><br>
<br><br>
<img src="result/BK.jpg" ><br>
<br><br>
<img src="result/city.jpg" ><br>
</center>


### References : 
[1] https://www.mathworks.com/help/vision/examples/feature-based-panoramic-image-stitching.html

[2] https://www.pyimagesearch.com/2016/01/11/opencv-panorama-stitching/

[3] http://ppwwyyxx.com/2016/How-to-Write-a-Panorama-Stitcher/
