import numpy as np
import cv2
import pytesseract

cap = cv2.VideoCapture(0)

while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()

	# Our operations on the frame come here
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Output OCR of frame
	# Define config parameters.
	# '-l eng'  for using the English language
	# '--oem 1' for using LSTM OCR Engine
	config = ('-l fra --oem 1 --psm 3')
	
	# Run tesseract OCR on image
	text = pytesseract.image_to_string(cv2.bitwise_not(frame), config=config)
	print(text)

	# Display the resulting frame
	cv2.imshow('frame',gray)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()