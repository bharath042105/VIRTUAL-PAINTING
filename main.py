import numpy as np
#import cvzone
import cv2
#import time
import os
import Hand_Tracking_Module as htm
import mediapipe as mp

brushThickness = 15
eraserThickness= 50
#width=500
#height=800

detector=htm.handDetector(detectionCon=1,maxHands=1)
xp, yp = 0,0
imgCanvas = np.zeros((500, 800, 3), np.uint8)

folderPath="head"
myList=os.listdir('C:/Users/hp/Pictures/head')
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'C:/Users/hp/Pictures/head/{imPath}')
    overlayList.append(image)
print(len(overlayList))
head = overlayList[0]
drawColour = (255, 0, 255)

cap = cv2.VideoCapture(0)
cap.set(3,720)
cap.set(4,1280)



while True:
    success, img = cap.read()
    img=cv2.flip(img, 1)
    img=detector.findHands(img)
    lmList=detector.findPosition(img)
    flist=lmList[0]
    if len(flist)!=0:
        #print(flist)


        x1,y1=flist[8][1:]
        x2,y2=flist[12][1:]


        
        fingers = detector.fingerUp()
        #print(fingers)



        if fingers[1] and fingers[2]:
            
            print("Selection Mode")
            if y1 < 125:
                if 0 < x1 < 120:
                    head = overlayList[0]
                    drawColour = (255,0,255)
                elif 150 < x1 < 300:
                    head = overlayList[1]
                    drawColour = (255,0,0)
                elif 350 < x1 < 450:
                    head = overlayList[2]
                    drawColour = (0,255,0)    
                elif 500 < x1 < 780:
                    head = overlayList[3]
                    drawColour = (0,0,0)
            cv2.rectangle(img,(x1,y1-25), (x2,y2+25), drawColour, cv2.FILLED)

        if fingers[1] and fingers[2]==False:
            cv2.circle(img, (x1,y1), 15, drawColour, cv2.FILLED)
            print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
    
            if drawColour == (0,0,0):    
                cv2.line(img, (xp, yp), (x1,y1), drawColour, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1,y1), drawColour, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1,y1), drawColour, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1,y1), drawColour, brushThickness)

            xp, yp =x1, y1 

    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _ ,imgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    #Matres = imgCanvas & img
    #img = cv2.bitwise_and(img, imgInv, res) 
    #img = cv2.bitwise_or(img, imgCanvas, mask=None)
    img[0:125, 0:640 ] = head
    #img = cv2.addWeighted(img,0.5, imgCanvas, 0.5,0)

    cv2.imshow("Image",img)
    cv2.imshow("Canvas", imgCanvas)
    if cv2.waitKey(1)==ord('q'):
        break
