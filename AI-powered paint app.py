import cv2
import numpy as np
import HandTrackingModule as htm
cap=cv2.VideoCapture(0)
import time
import math


detector=htm.handDetector() 


drawingColor=(0,0,0)
imgCanvas = np.zeros((720,1280,3),np.uint8)



while True:
    
    sucess,image=cap.read()

    image=cv2.flip(image,1)
    image=cv2.resize(image,(1280,720))
    cv2.rectangle(image,(90,0),(1030,110),(255,255,255),cv2.FILLED)
    cv2.rectangle(image,(90,10),(270,100),(0,0,255),5)
    cv2.putText(image,'Write',(130,60),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),3)
    cv2.rectangle(image,(280,10),(460,100),(0,0,255),5)
    cv2.circle(image,(370,55),30,(0,0,0),3)
    cv2.rectangle(image,(470,10),(650,100),(0,0,255),5)
    cv2.line(image,(600,20),(510,90),(0,0,0),2)
    cv2.rectangle(image,(660,10),(840,100),(0,0,255),5)
    cv2.rectangle(image,(700,40),(800,70),(0,0,0),3)
    cv2.rectangle(image,(850,10),(1030,100),(0,0,255),5)
    cv2.putText(image,'Eraser',(880,60),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),3)
    cv2.rectangle(image,(1170,100),(1280,580),(255,255,255),cv2.FILLED)
    cv2.circle(image,(1225,150),50,(255,0,0),cv2.FILLED)
    cv2.circle(image,(1225,275),50,(0,255,0),cv2.FILLED)
    cv2.circle(image,(1225,400),50,(0,0,255),cv2.FILLED)
    cv2.circle(image,(1225,525),50,(0,255,255),cv2.FILLED)
    
    

# #2. Find Hand landmarks
    image=detector.findHands(image)
    lmlist=detector.findPosition(image)

    if len(lmlist)!=0:
        x1,y1=lmlist[8][1:]
        x2,y2=lmlist[12][1:]
        

# #3. check which finger is up

    fingers=detector.fingersUp()
    

    
# #4. Selection mode


    if fingers[1] and fingers[2]:
        xp,yp=0,0

        if y1<120:
            if 90<x1<270:
                  cv2.putText(image,'Text',(x1,y1),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),3)
                  sel='text'              

            if 280<x1<460:   
                cv2.circle(image,(x1,y1),40,drawingColor,4)
                sel='circle'

            elif 470<x1<650:               
                cv2.line(image,(x1,y1),(x1+80,y1+80),drawingColor,5)
                sel='line'          
        
            elif 660<x1<840:               
                cv2.rectangle(image,(x1,y1),(x1+20,y1+20),drawingColor,3)
                sel='rectangle'              

            elif 850<x1<1030:              
                cv2.circle(image,(x1,y1),40,drawingColor,cv2.FILLED)
                drawingColor=(0,0,0)
        
        elif x1>1170:
              if 100<y1<200:
                    drawingColor=(255,0,0)
              elif 225<y1<325:
                    drawingColor=(0,255,0)
              elif 350<y1<450:
                    drawingColor=(0,0,255)
              elif 475<y1<575:
                    drawingColor=(0,255,255)

    def write_text(drawingColor,xp,yp,x1,y1):
           cv2.line(image,(xp,yp),(x1,y1),drawingColor,15)
           cv2.line(imgCanvas,(xp,yp),(x1,y1),drawingColor,15)
           
 
    def draw_circle(drawingColor,x1,y1):
           z1,z2=lmlist[4][1:]
           dis=math.dist([x1,y1],[z1,z2])
           s = int(dis)
           cv2.circle(image,(x1,y1),s,drawingColor,4)
           if fingers[4]:                                     
                    
                      cv2.circle(imgCanvas,(x1,y1),s,drawingColor,4)
                      time.sleep(0.5)

    def draw_line(drawingColor,x1,y1):
            z1,z2=lmlist[4][1:]
            dis=math.dist([x1,y1],[z1,z2])               
            s=int(dis)
            cv2.line(image,(x1,y1),(x1+s,y1+s),drawingColor,5)
            if fingers[4]:
                            cv2.line(imgCanvas,(x1,y1),(x1+s,y1+s),drawingColor,5)
                            time.sleep(0.5)
                
    def draw_rectangle(drawingColor,x1,y1):
            z1,z2=lmlist[4][1:]
            dis=math.dist([x1,y1],[z1,z2])               
            s=int(dis)
            cv2.rectangle(image,(x1,y1),(x1+s,y1+s),drawingColor,5)
            if fingers[4]:
                            cv2.rectangle(imgCanvas,(x1,y1),(x1+s,y1+s),drawingColor,5)
                            time.sleep(0.5)               

#5. drawing mode

    if fingers[1] and not fingers[2]:
               
        if xp == 0 and yp == 0:
            xp=x1
            yp=y1     

        if drawingColor==(0,0,0):
                           
                  z1,z2=lmlist[4][1:]
                  dis=math.dist([x1,y1],[z1,z2])
                  s = int(dis)
                  cv2.line(image,(xp,yp),(x1,y1),drawingColor,s)
                  cv2.line(imgCanvas,(xp,yp),(x1,y1),drawingColor,s)

        if sel=='text':
              if drawingColor==(255,0,0):
                    write_text(drawingColor,xp,yp,x1,y1)
              elif drawingColor==(0,255,0):
                    write_text(drawingColor,xp,yp,x1,y1)
              elif drawingColor==(0,0,255):
                    write_text(drawingColor,xp,yp,x1,y1)    
              elif drawingColor==(0,255,255):
                    write_text(drawingColor,xp,yp,x1,y1)
     
        if sel=='circle':
              if drawingColor==(255,0,0):
                       draw_circle(drawingColor,x1,y1)
              elif drawingColor==(0,255,0):
                    draw_circle(drawingColor,x1,y1)
              elif drawingColor==(0,0,255):
                    draw_circle(drawingColor,x1,y1)
              elif drawingColor==(0,255,255):
                    draw_circle(drawingColor,x1,y1)

        if sel=='line':
              if drawingColor==(255,0,0):
                            draw_line(drawingColor,x1,y1)
              elif drawingColor==(0,255,0):
                     draw_line(drawingColor,x1,y1)
              elif drawingColor==(0,0,255):
                     draw_line(drawingColor,x1,y1)
              elif drawingColor==(0,255,255):
                     draw_line(drawingColor,x1,y1)
        if sel=='rectangle':
               if drawingColor==(255,0,0):
                      draw_rectangle(drawingColor,x1,y1)
               elif drawingColor==(0,255,0):
                      draw_rectangle(drawingColor,x1,y1)
               elif drawingColor==(0,0,255):
                      draw_rectangle(drawingColor,x1,y1)
               elif drawingColor==(0,255,255):
                      draw_rectangle(drawingColor,x1,y1)

        xp,yp=x1,y1
    

    
    if fingers[2] and fingers[3] and fingers[0]==0 and fingers[1]==0 and fingers[4]==0:
          imgCanvas = np.zeros((720, 1280, 3), np.uint8)

    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _,imgInv=cv2.threshold(imgGray,20,255,cv2.THRESH_BINARY_INV)
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)

    image=cv2.bitwise_and(image,imgInv)
    image=cv2.bitwise_or(image,imgCanvas)

    image=cv2.addWeighted(image,1,imgCanvas,0.5,0)




    cv2.imshow('virtual painter',image)
    if cv2.waitKey(1) & 0xFF==27:
        break