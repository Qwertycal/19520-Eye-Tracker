import cv2
import click_callback as callback

dots = cv2.imread('dots.png')
cv2.namedWindow('click space')
cv2.setMouseCallback("click space", callback.click_callback)


while True:

    cv2.imshow('click space', dots )




    if cv2.waitKey(1) & 0xFF == ord('q'):
        break