import cv2
import numpy as np
import telegram
import time
import asyncio

#TELEGRAM_BOT_TOKEN = 'your.token'
#TELEGRAM_CHAT_ID = '-your.chat.id'
#bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

async def main():
    TELEGRAM_BOT_TOKEN = 'your.token'
    TELEGRAM_CHAT_ID = '-your.chat.id'
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    #asyncio.run(bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=open(fname, 'rb'), caption="Motion Detected!"))
    with open('motion.jpg', 'rb') as f:
        await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=f, caption="Motion Detected!")
# Video Capture 
capture = cv2.VideoCapture(0)
#capture = cv2.VideoCapture("demo.mov")
print('Capture Video')

# History, Threshold, DetectShadows 
fgbg = cv2.createBackgroundSubtractorMOG2(50, 200, True)
#fgbg = cv2.createBackgroundSubtractorMOG2(300, 400, True)

# Keeps track of what frame we're on
frameCount = 0

while(1):
    # Return Value and the current frame
    ret, frame = capture.read()

    #  Check if a current frame actually exist
    if not ret:
        break

    frameCount += 1
    # Resize the frame
    resizedFrame = cv2.resize(frame, (0, 0), fx=0.15, fy=0.15)

    # Get the foreground mask
    fgmask = fgbg.apply(resizedFrame)

    # Count all the non zero pixels within the mask
    count = np.count_nonzero(fgmask)

    print('Frame: %d, Pixel Count: %d' % (frameCount, count))
    cv2.imshow('Frame', resizedFrame)
    cv2.imshow('Mask', fgmask)
    
    # Determine how many pixels do you want to detect to be considered "movement"
    # if (frameCount > 1 and cou`nt > 5000):
    if (frameCount > 10 and count > 1200):
        print('Motion Detected')
        #cv2.putText(resizedFrame, 'Someones stealing your honey', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        fname = ("motion.jpg")
        cv2.imwrite(fname, resizedFrame)
        time.sleep(1)
        asyncio.run(main())
        time.sleep(1)
        frameCount = 0



    k = cv2.waitKey(1) & 0xff
    if k == 27:
            break

capture.release()
cv2.destroyAllWindows()
