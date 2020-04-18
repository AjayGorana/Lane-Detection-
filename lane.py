import cv2
import numpy as np
import matplotlib.pyplot as plt

def make_coordinates(image,line_parameters):
    slop,intercept=line_parameters
    print(image.shape)
    y1=image.shape[0]
    y2=int(y1*(3/5))
    x1=int((y1-intercept)/slop)
    x2=int((y2-intercept)/slop)
    return np.array([x1,y1,x2,y2])
def average_slop_intercept(image,lines):
    left_fit=[]
    right_fit=[]
    
    for line in lines:
        x1,y1,x2,y2=line.reshape(4)
        parameters=np.polyfit((x1,x2),(y1,y2),1)
        print(parameters)
        slop=parameters[0]
        intercept=parameters[1]
        
        if slop<0:
            left_fit.append((slop,intercept))
        else:
            right_fit.append((slop,intercept))
    #print(left_fit)
    #print(right_fit)
    left_fit_average=np.average(left_fit,axis=0)
    right_fit_average=np.average(right_fit,axis=0)
    left_line=make_coordinates(image,left_fit_average)
    right_line=make_coordinates(image,right_fit_average)
    #print(left_fit_average,"left")
    #print(right_fit_average,"right")
    return np.array([left_line,right_line])

def canny(image):
    gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    blur=cv2.GaussianBlur(gray,(5,5),0)
    canny=cv2.Canny(blur,50,150)
    return canny

def display_lines(image,lines):
    line_image=np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2=line.reshape(4)
            cv2.line(line_image,(x1,y1),(x2,y2),(0,255,0),10)
            print(line)
    return line_image
def region_of_interest(image):
    height=image.shape[0]
    ploygons=np.array([[(200,height),(1100,height),(550,250)]])
    mask=np.zeros_like(image)
    cv2.fillPoly(mask,ploygons,255)
    masked_image=cv2.bitwise_and(image,mask)
    return masked_image
    



cap=cv2.VideoCapture("test2.mp4")
while(cap.isOpened()):
   _,frame=cap.read()
   canny_image=canny(frame)
   cropped_image=region_of_interest(canny_image)
   lines=cv2.HoughLinesP(cropped_image,2,np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=5)
   averaged_lines=average_slop_intercept(frame,lines)
   line_image=display_lines(frame,averaged_lines)
   combo_image=cv2.addWeighted(frame,0.8,line_image,1,1)
   cv2.imshow("result",combo_image)
   if cv2.waitKey(1)==ord('q'):
       break
cap.release()
cv2.destroyAllWindows()

    
   
 
 
  
