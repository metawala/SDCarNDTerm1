import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

bgrImage = cv2.imread('data/IMG/center_2016_12_01_13_31_13_786.jpg')
rgbImage = cv2.cvtColor(bgrImage, cv2.COLOR_BGR2RGB)
croppedImage = rgbImage[50:137, :, :]
image = cv2.resize(croppedImage, (200, 66))
mpimg.imsave('Outputs/CroppedImage.JPG', image)
flippedImage = cv2.flip(image, 1)
mpimg.imsave('Outputs/FlippedImage.JPG', flippedImage)