# **German Traffic Sign Recognition**

---

## Build a Traffic Sign Recognition Project

The goals / steps of this project are the following:
* Load the data set (see below for links to the project data set)
* Explore, summarize and visualize the data set
* Design, train and test a model architecture
* Use the model to make predictions on new images
* Analyze the softmax probabilities of the new images
* Summarize the results with a written report

[//]: # (Image References)

[image1]: ./examples/visualization.png "Visualization"
[image2]: ./Downloaded_images/Arterial.jpg "Traffic Sign 1"
[image3]: ./Downloaded_images/Caution_ahead.jpg "Traffic Sign 2"
[image4]: ./Downloaded_images/Construction_ahead.jpg "Traffic Sign 3"
[image5]: ./Downloaded_images/Old_cyclists_crossing_theroad--Stock-Photo.jpg "Traffic Sign 4"
[image6]: ./Downloaded_images/pedestrian_crossing_Photo.jpg "Traffic Sign 5"
[image7]: ./Downloaded_images/slippery_road.jpg "Traffic Sign 6"
[image8]: ./Downloaded_images/Stop_Sign.jpg "Traffic Sign 7"
[image9]: ./Downloaded_images/Turn_left_ahead.jpg "Traffic Sign 8"
[image10]: ./Downloaded_images/Turn_right_ahead.jpg "Traffic Sign 9"
[image11]: ./Downloaded_images/yield_signs.jpg "Traffic Sign 10"

### Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/481/view) individually and describe how I addressed each point in my implementation.  

---
## Writeup / README

This writeup is towards the project to create a German traffic sign classifier. Here is a link to my [project code](https://github.com/metawala/SDCarNDTerm1/blob/master/P2_Traffic_Sign_Classifier/Traffic_Sign_Classifier.ipynb)

## Data Set Summary & Exploration

**Data Set Summary**

I used the pandas and pickle library to calculate summary statistics of the traffic signs data set:

* The size of training set is **34799**
* The size of the validation set is **4410**
* The size of test set is **12630**
* The shape of a traffic sign image is **(32, 32, 3)**
* The number of unique classes/labels in the data set is **43**

**Exploratory visualization of the dataset**

Here is an exploratory visualization of the data set. It is a bar chart showing how the data is distributed among all the classes.

![alt text][image1]

## Design and Test a Model Architecture

This project uses techiniques shown in lecture videos and project videos preceeding this project. The preprocessing techniques, NN architechture and any other techinques used here are primarily from those teachings. A few of my other colleagues are also taking this degree program and hence we do collaborate at times to discuss some strategies that might help improve the output of these projects. 

#### 1. Describe how we preprocessed the image data.

Preprocessing techinque shown in the project videos suggested normalizing the input images. Hence, preprocessing for each image in the training, test and validation sets were performed as follows:

1. Covert color image to gray
2. Use cv2.equalizeHist to equalize the histogram
3. Normalize the image. Normalized so that the data is zero centered and has a std deviation of 1.

#### 2. Final model architecture.

I used the LeNet architecture showing the project videos. The dataset was converted to grayscale and hence the size of the image was reduced to AxBx1. We use RELU6 instead of RELU here for activation and dropout technique discussed in lectures. My final model consisted of the following layers:

| Layer         		|     Description	        					| 
|:---------------------:|:---------------------------------------------:| 
| Input         		| 32x32x1 RGB image   							| 
| Convolution 5x5     	| 1x1 stride, 12 filters, outputs 28x28x12 	    |
| RELU6					|												|
| Max pooling	      	| 2x2 stride,  outputs 14x14x32 				|
| Convolution 5x5	    | 1x1 stride, 32 filters, outputs 10x10x32  	|
| RELU6					|												|
| Max pooling	      	| 2x2 stride,  outputs 5x5x32    				|
| Fully connected		| Input = 800, Output = 120     				|
| RELU6 				|												|
| Dropout		        | DropoutProb = 0.5								|
| Fully connected		| Input = 120, Output = 84						|
| RELU6 				|												|
| Dropout		        | DropoutProb = 0.5								|
| Fully connected		| Input = 84, Output = 43						|
| Softmax				|              									|

#### 3. Model Training.

To train the model, I used:
1. Weight Initialization = Variables initialized as truncated normal with 0 mean and 0.1 std deviation.
1. EPOCHS = 100.
2. BATCH_SIZE = 128.
3. Learning Rate = 1e-3.
4. Droupout Probability = 0.5. This value is used widely, hence we chose to use this value.
6. Optimizer = Adam Optimizer. Along with this we also use a regulizerBeta of value 1e-4.

#### 4. Solution Approach.

My final model results were:
* Average validation set accuracy of **0.961**
* Test set accuracy of **0.951**

If a well known architecture was chosen:
* What architecture was chosen - We chose the LeNet architecture for this project. The reason behind chosing this was to stay in line with architecture shown in the lectures.
* Why did you believe it would be relevant to the traffic sign application - As shown and discussed in lecture videos and notes, LeNet is a very famous algorithm for image classification. 

## Test a Model on New Images

I downloaded 10 random images from the internet. These images are saved in ./Downloaded_images/*. I decided not to modify any of these images to test how much it affects the accuracy during classification. 

### Discussion is made as to particular qualities of the images or traffic signs in the images that are of interest, such as whether they would be difficult for the model to classify.

Out of the 10 images downloded there are particular images that are of interest wrt to challanges in classification.
4 particular images are - **"Old_cyclists_crossing_theroad--Stock-Photo.jpg"**, **Arterial.jpg**, **pedestrian_crossing_Photo.jpg**, **Turn_right_ahead.jpg**

The challenges with these images is the following:
1. These images have watermarks in the background which tend to induce noise to the classifier
2. The cyclist image is an old deprecated image for cyclist crossing where as the classifier was trained on newer german sign images.
3. Arterial image is a generic caution/priority sign and is not part of the 43 classes that the classifier was trained on.

As seen from the output of the classifier, we see that most of these images are identified correctly and the classifier does a very good job at making predictions.

### The submission documents the performance of the model when tested on the captured images. The performance on the new images is compared to the accuracy results of the test set.

The performance of these new images can be seen in the section Analyze Performace. On average we see that it is 60% accurate which can also be verified with the softmax predcitions and bar plots there. We see that the classifier does a very good job with these new downloaded images. The result shows that it does not make a very big difference. May be the results could have been more accurate if the images were to be resized to (32, 32,x) but we have not tested that. Also we use 1 of the signs which belong to an older version of German traffic sign.

Here are the results of the prediction:

| Image			        |     Prediction                    |Probability |
|:---------------------:|:----------------------------------|:----------:|
| Turn right ahead 		| Turn right ahead			        | 1.0        |
| Caution ahead 		| General Caution			        | 1.0        |
| Stop sign		    	| Priority road				        | 1.0        |
| Slippery road ahead	| Slippery road				        | 1.0        |
| Turn left ahead		| Turn left ahead      		        | 1.0        |
| Arterial      		| Priority road      		        | 1.0        |
| Yield sign    		| End of speed limit(80km/h)        | 0.98       |
| Cyclist crossing		| Right of way at next intersection | 1.0        |
| Pedestrian crossing	| Right of way at next intersection | 0.75       |
| Construction ahead	| Road work           		        | 0.99       |

Based on the results above, we can see that there are a few images that are misclassified. For e.g. the image showing a Cyclist crossing is not predicted exactly as to what it is. However, it does tell some of the story by predicting it as Right of way at next intersection. In the case of a Yield sign it is predicted as a speed limit sign.

There might be other techniques in which this network could be improved. Changing the learing rate or regularising rate or learning rate might affect the accuracy of the model.