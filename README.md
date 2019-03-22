# Trajectory-Tracking-Racecar
## Introduction
<br>We used ‘Color Selection’, ‘Gaussian Smoothing’, ‘Canny Edge Detection’, and ‘Hough Transform’ methods for lane detection task.
Normally, the lane is yellow or white, therefore, we convert the RGB image into HSV color space which helps both the white and yellow lines to be clear and recognizable.
Gaussian blur function helps to eliminate unnecessary line that is not for road line. This can modify a lot of rough line edges which causes many noisy line edges to be detected and make the line edges more smoother. The Canny edge detection can find the edge of the image based on where the brightness of the local area changes significantly.
Lastly, the Hough transform is a technique that is used in image analysis and computer vision and digital image processing. By return values from Hough transform, we can calculate slope from our camera vision to line edge. Therefore, our angle output is successfully calculated by the slope from our camera vision.
## A Star
<br>Input: A* is a graph search algorithms, which take a “graph” as input. A graph is a set of locations (“nodes”) and the connections (“edges”) between them. A* selects the path that minimizes f(n)=g(n)+h(n) where n is the next node on the path, g(n) is the cost of the path from the start node to n, and h(n) is a heuristic function that estimates the cost of the cheapest path from n to the goal.
<br> So if we change the weight of heuristic function, the result of A* will change.
<br>The algorithm in pseudocode is as follows:
![astar](https://user-images.githubusercontent.com/36937088/54732154-7a6d6500-4b4f-11e9-8f36-67a9ccfa64d0.jpeg)
## RRT
<br> A major feature of the RRT algorithm is the random search of space. Such search brings great advantages especially to path planning in high-dimensional space, but such search leads to low computational efficiency of the algorithm. The random tree search generates random points throughout the metric space until the node just extends to the vicinity of the target to end the search and generate the final path.
<br>The algorithm in pseudocode is as follows:  
![rrt](https://user-images.githubusercontent.com/36937088/54732732-8eff2c80-4b52-11e9-87a2-7459d19c383e.jpeg)
## RRT Star
<br>Although the RRT algorithm is a relatively efficient one, the RRT algorithm does not guarantee that the resulting planning path is relatively optimized. The main feature of the RRT* algorithm is that it can quickly find the initial path, and then continue to optimize as the sampling point increases until the target point is found or the set maximum number of cycles is reached. The difference between the RRT* algorithm and the RRT algorithm lies in the two recalculation processes for the new node x_new, which are:
<br>1. The process of re-selecting the parent node for x_new
<br>2. The process of rerouting a random tree
<br>The algorithm in pseudocode is as follows:  
![rrtstar](https://user-images.githubusercontent.com/36937088/54732460-21063580-4b51-11e9-8698-0dd5ce3d9d2e.jpeg)
## Result
<br> I chose the same map and select the optimal parameter for each algorithm for comparasion.
<br> The RRT* results is as follows:    
  ![rrt_p2_step](https://user-images.githubusercontent.com/36937088/54732264-1a2af300-4b50-11e9-880f-431efe67a404.jpeg)
<br> The RRT results is as follows:   
  ![rrtstart_p2_step](https://user-images.githubusercontent.com/36937088/54732274-2adb6900-4b50-11e9-9965-e32cf2f9e807.jpeg)  
<br> The A* results is as follows:   
  ![a_map2_ep=1](https://user-images.githubusercontent.com/36937088/54732282-329b0d80-4b50-11e9-8962-d5ad310c9244.jpeg)
## Comparison
Firstly, for A* method, it designs a cost function. I set the weight for the heuristic function is 1. I set the step size for A is 1 and it can move eight directions. The result for A is quite acceptable because of it almost straight. For RRT and RRT*, I design there are 5 percents possibility to select the goal point so that these two algorithms can run faster. Moreover, RRT* can re-select father node and re-wire for x_new, which cause the cost is lower than RRT.
