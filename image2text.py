from PIL import Image
import pytesseract
import argparse
import cv2
import os

# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", required=True, 
	help="path to input image for OCR")
parser.add_argument("-p", "--preprocess", type=str, default="thresh", 
	help="type of preprocessing to be done")
args = vars(parser.parse_args())

# Load image and convert to grayscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Check prior to applying thresholding for preprocessing
if args["preprocess"] == "thresh":
	gray = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# Check prior to applying median blurring to remove noise
elif args["preprocess"] == "blur":
	gray = cv2.medianBlur(gray, 3)

# Write grayscale image to disk as temp file to apply OCR
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)

# Load Pillow image and apply OCR while deleting temp file
text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)
print(text)

# Display output images
cv2.imshow("Image", image)
cv2.imshow("Output", gray)
cv2.waitKey(0)