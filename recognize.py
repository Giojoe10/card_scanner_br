def recognize(im):
    import cv2
    import numpy as np
    import pytesseract as tess
    tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Get only the define square
    w, h = im.shape[:2]

    x1, y1 = int( (h/2) -150 ), int( (w/2) -210)
    x2, y2 = int( (h/2) +150 ), int( (w/2) +210)
    cropped = im[y1:y2,x1:x2]

    # Apply filters for easier detection
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    #blurred = cv2.GaussianBlur(gray, (5,5), 0)
    blurred = gray

    # Testing yhe different types of thresholding
    thresh = cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
    _, thresh = cv2.threshold(blurred,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    _, thresh = cv2.threshold(blurred,127,255,cv2.THRESH_BINARY_INV)

    cv2.imshow('gaussian',thresh)
    cv2.imshow('cropped', gray[0:25,0:w])
    #cv2.imshow('otsu',thresh2)
    #cv2.imshow('normal',thresh3)

    print(tess.image_to_string(image=gray[0:25,0:w], lang='por', config='--psm 7'))

    #cv2.imshow("cut", cropped)

