# Motion detection and email alerts with a USB webcam

My webcam is set up like this:

![alt tag](https://github.com/JonathanCooper/motion-detect/blob/master/doc/example.jpg)

I am performing the motion detection on the area within the green rectangle:

![alt tag](https://github.com/JonathanCooper/motion-detect/blob/master/doc/example-boxed.jpg)

I run ```scripts/detect.py``` as a deamon.  When it detects motion, it makes a nice animated gif of the "incident" and sends me an email!
