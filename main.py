import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
decetor = HandDetector(detectionCon=0.8)

ox,oy = 200,200


startDist = None
scale = 0
cx,cy = 500, 500
while True:
    success, img = cap.read()
    hands, img = decetor.findHands(img)
    img1= cv2.imread("slika.png")

    if len(hands) == 2:
        if decetor.fingersUp(hands[0])==[1,1,0,0,0] and decetor.fingersUp(hands[1])==[1,1,0,0,0]:
            lmList1 = hands[0]['lmList']
            lmList2 = hands[1]['lmList']
            lmList1[8], lmList2[8]
            if startDist is None:
                length, info, img = decetor.findDistance(hands[0]["center"], hands[1]["center"], img)
                startDist = length

            length, info, img = decetor.findDistance(hands[0]["center"], hands[1]["center"], img)
            scale = int((length - startDist)//2)
            cx,cy = info[4:]

    if hands and len(hands) !=2:
        startDist = None
        lmList = hands[0]['lmList']

        length, info, img = decetor.findDistance(lmList[8], lmList[12], img)
        print(length)

        if length < 60:
            cursor = lmList[8]

            if ox < cursor[0] < ox + w1 and oy < cursor[1] < oy + h1:
                ox, oy = cursor[0] - w1 // 2, cursor[1] - h1 // 2


    h1, w1, _ = img1.shape
    try:
        if len(hands) == 2:
                newH, newW = ((h1+scale)//2)*2, ((w1+scale)//2)*2
                img1 = cv2.resize(img1, (newH, newW))

                img[cy-newH//2:cy+newH//2, cx-newW//2:cx+newW//2] = img1
        else:
            img[oy:oy + h1, ox:ox + w1] = img1
    except:
        pass

    cv2.imshow("Image", img)
    cv2.waitKey(1)
