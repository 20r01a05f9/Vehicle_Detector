import cv2
import numpy as np

width_min=80 #min width rectangle
height_min=80 #min height rectangle
offset=6 #allow error btwn pixel 

position_line=550  

delay= 60 

detect = []
counter= 0

	
def center_handle(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

cap = cv2.VideoCapture('video.mp4')
algo = cv2.createBackgroundSubtractorMOG2()

while True:
    ret , frame1 = cap.read()
    grey = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey,(3,3),5)
    #applying on each frame
    img_sub = algo.apply(blur)
    a = cv2.dilate(img_sub,np.ones((5,5)))
    b = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    c = cv2.morphologyEx (a, cv2.MORPH_CLOSE , b)
    c = cv2.morphologyEx (c, cv2.MORPH_CLOSE , b)
    countershape,h=cv2.findContours(c,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.line(frame1, (25, position_line), (1200, position_line), (255,127,0), 3)
    
    for(i,c1) in enumerate(countershape):
        (x,y,w,h) = cv2.boundingRect(c1)
        validate_counter = (w >= width_min) and (h >= height_min)
        if not validate_counter:
            continue

        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(frame1, "Vehicle: "+str(counter), (x,y-20), cv2.FONT_HERSHEY_TRIPLEX , 1, (255, 244, 0),2)
        center = center_handle(x, y, w, h)
        detect.append(center)
        cv2.circle(frame1, center, 4, (0, 0,255), -1)

        for (x,y) in detect:
            if y<(position_line+offset) and y>(position_line-offset):
                counter+=1
                cv2.line(frame1, (25, position_line), (1200, position_line), (0,127,255), 3)  
                detect.remove((x,y))
                print("Vehicle Counter: "+str(counter))        
       
    cv2.putText(frame1, "VEHICLE COUNT : "+str(counter), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),5)
    cv2.imshow("Video Original" , frame1)

    if cv2.waitKey(1) == 13:
        break
    
cv2.destroyAllWindows()
cap.release()
