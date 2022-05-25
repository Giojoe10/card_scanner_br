import cv2
from recognize import recognize

vid = cv2.VideoCapture(0)

while(True):
    # Capture the video frame
    ret, frame = vid.read()

    # Draw the square in the middle of the screen
    w, h = frame.shape[:2]
    corner1 = ( int( (h/2) -150 ), int( (w/2) -210) )     #Proportion 5:7
    corner2 = ( int( (h/2) +150 ), int( (w/2) +210) )
    cv2.rectangle(frame, corner1, corner2, (0, 255, 0), 2)
  
    cv2.imshow('frame', frame)
      
    #"Q" quits
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #"Space" captures the image
    if cv2.waitKey(1) & 0xFF == 32:
        capture = frame
        cv2.imshow('capture',capture)
        recognize(capture)
    
  
# After the loop release the cap object and destroy all windows
vid.release()
cv2.destroyAllWindows()




