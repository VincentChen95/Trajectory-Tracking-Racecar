# Trajectory-Tracking-Racecar
## Introduction  
![pipeline](https://user-images.githubusercontent.com/36937088/54845125-d0e4bb80-4c95-11e9-8f07-fd297ad19702.jpeg)
<br>We used ‘Color Selection’, ‘Gaussian Smoothing’, ‘Canny Edge Detection’, and ‘Hough Transform’ methods for lane detection task.
Normally, the lane is yellow or white, therefore, we convert the RGB image into HSV color space which helps both the white and yellow lines to be clear and recognizable.
Gaussian blur function helps to eliminate unnecessary line that is not for road line. This can modify a lot of rough line edges which causes many noisy line edges to be detected and make the line edges more smoother. The Canny edge detection can find the edge of the image based on where the brightness of the local area changes significantly.
Lastly, the Hough transform is a technique that is used in image analysis and computer vision and digital image processing. By return values from Hough transform, we can calculate slope from our camera vision to line edge. Therefore, our angle output is successfully calculated by the slope from our camera vision.
## Color Selection
<br>The presence of shadows severely affected detection. We know that the color of the general lane line is yellow and white. If we extract the yellow and white of the picture, it will be much easier to detect the lane line later. So we transform the RGB color space into HSV color space.
## Canny Edge Detection
<br> Canny edge detection is a multi-step algorithm that can detect edges with noise supressed at the same time.  
1. Smooth the image with a Gaussian filter to reduce noise and unwanted details and textures.  
2. Compute gradient using any of the gradient operatiors (Roberts, Sobel, Prewitt, etc).  
3. Suppress non-maxima pixels in the edges in threshold to thin the edge ridges (as the edges might have been broadened in step 1).   
4. Threshold the previous result by two different thresholds to obtain two binary images.  
5. Link edge segments to form continuous edges.
<br>An Canny edge result is as follows:  
![edge](https://user-images.githubusercontent.com/36937088/54845861-bc092780-4c97-11e9-8ee8-76599c1d5d40.png)
## Result
<br> I chose the same map and select the optimal parameter for each algorithm for comparasion.
<br> The angle calculation results is as follows:    
![angle](https://user-images.githubusercontent.com/36937088/54845334-54061180-4c96-11e9-8203-8c03842357f2.jpeg)
<br> The car integrates the PID control and angle to follow the trajectory.   
 ![video12](https://user-images.githubusercontent.com/36937088/54845331-50728a80-4c96-11e9-82fd-d11d9e8df27a.png)  
![LineDetectionFinalVideo](https://user-images.githubusercontent.com/36937088/55095475-753f7700-5075-11e9-889c-30451bbd52d2.gif)
