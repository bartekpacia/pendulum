from typing import Tuple
import cv2
import time
import numpy
print(f"using OpenCV v{cv2.__version__}")

capture = cv2.VideoCapture("film3.mp4")
fps = round(capture.get(cv2.CAP_PROP_FPS), 2)

ret, frame1 = capture.read()
ret, frame2 = capture.read()

time_start = time.time()
labels = []
stops_list = []
T_list = []


def drawText(text: str, color: Tuple[int, int, int], pos: Tuple[int, int]):
    cv2.putText(frame1, str(text), org=pos, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1, color=color, thickness=3)


prev_moving = False
while capture.isOpened():
    T = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(T, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, threshold = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(threshold, None, iterations=1)
    contours, _ = cv2.findContours(
        dilated, cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

    drawText("T", (255, 0, 0), (600, 400))

    big_moving_things = 0
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 2000:
            continue
        else:
            big_moving_things += 1
            cv2.rectangle(frame1, pt1=(x, y), pt2=(x + w, y + h),
                          color=(0, 255, 0), thickness=2)

    if big_moving_things > 0:
        color = (0, 255, 0)
        msg = "JEST RUCH"
        prev_moving = True
    else:
        color = (0, 0, 255)
        msg = "NIE MA RUCHU"
        if prev_moving:
            time_total = round(time.time() - time_start, 2)
            stops_list.append(time_total)
            T = 0
            if len(stops_list) > 1:
                T = round(time_total - stops_list[-2], 2)

                if T >= 0.5:
                    T_list.append(T)
                    labels.append(f"T: {T}, od poczatku: {time_total}")
                    prev_moving = False

    label_y = 60
    for label in labels:

        label_y += 30
        drawText(label, color, (10, label_y))

    drawText(msg, color, (10, 40))
    drawText(fps, color, (300, 40))

    T_average = round(numpy.mean(T_list), 2)
    drawText(f"sredni okres: {T_average}", color, (500, 40))

    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = capture.read()
    print(f"frame2: {frame2}")

    if cv2.waitKey(40) == 27:
        break


cv2.destroyAllWindows()
capture.release()
