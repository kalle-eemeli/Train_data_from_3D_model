# Train_data_from_3D_model (Work in progress)

![](opengl.jpg)   ![](python.png)   ![](tf.png) 

- At the moment running *main.py* starts the rendering loop and image buffering and "bulk saving" is also functional 


- When finished, the idea of this project is to be able to create training data for a image recognition neural network by using 3D-models. At the moment it is being developed by trying out simple primitive shapes (cone, cube, sphere) with a default texture. 
- The 3D-models are currently created in [Blender](https://www.blender.org/) and exported as .obj-files. Using those files the given objects are rendered using [PyOpenGL](http://pyopengl.sourceforge.net/). 
- Those renders are then used to take snapshots of the objects in different positions, angles, (enviroments, lighting) etc. 
- These images are then saved locally for further use. In the future the idea is to create .tfrecord-files (pairing each image with a corresponding label) of these images and to upload them to a [MinIO](https://min.io/) client. Any training of an actual neural network will be done by utilizing [Tensorflow](https://www.tensorflow.org/)
