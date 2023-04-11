<h2>Green Squares Read Me File  <h2>
* The green squares program takes two photos and saves them to files, which are then displayed with an HSV mask which also allows the user to click on the desired color to detect.
* Draws contours in black and white, which are displayed, and counts the number of squares detected with that color.
* Subtracts the number of green square deteced in the first image from 64 (the total number of squares), to find the number of white squares in the first image.
* Does the same for the second image.
* Subtracts the number of white squares in the second image from the first image. If the number is negative, the anchor tear has receded, if the number is positive, the anchor tear recovers.
* Prints the number found, along with the correct deduction.