from typing import Tuple
import cv2
import time
import numpy

length = float(input("Enter length of the rope: "))

print(f"using OpenCV v{cv2.__version__}")

capture = cv2.VideoCapture("film3_vga.mp4")
fps = round(capture.get(cv2.CAP_PROP_FPS), 2)

_, frame1 = capture.read()
_, frame2 = capture.read()

time_start = time.time()
labels = []
stops_list = []
T_list = []


def calc_avg_T() -> int:
    return round(numpy.mean(T_list), 2)


def drawText(text: str,
             color: Tuple[int, int, int],
             pos: Tuple[int, int],
             big=False,
             console=True):
    if console:
        print(text)

    if big:
        scale = 1
        thickness = 4
    else:
        scale = 0.6
        thickness = 2

    cv2.putText(frame1, str(text), org=pos, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=scale, color=color, thickness=3)


prev_moving = False
while capture.isOpened() and frame1 is not None and frame2 is not None:
    t0 = cv2.getTickCount()
    T = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(T, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, threshold = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(threshold, None, iterations=1)
    contours, _ = cv2.findContours(
        dilated, cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

    big_moving_things = 0
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 1000:
            continue
        else:
            big_moving_things += 1
            cv2.rectangle(frame1, pt1=(x, y), pt2=(x + w, y + h),
                          color=(0, 255, 0), thickness=2)

    if big_moving_things > 0:
        color = (0, 255, 0)
        msg = "MOVING"
        prev_moving = True
    else:
        color = (0, 0, 255)
        msg = "NOT MOVING"
        if prev_moving:
            time_total = round(time.time() - time_start, 2)
            stops_list.append(time_total)
            T = 0
            if len(stops_list) > 1:
                T = round(time_total - stops_list[-2], 2)

                # because sometimes the end point is detected twice
                if T >= 0.1:
                    T_list.append(T)
                    labels.append(f"T: {T}, total: {time_total}")
                    prev_moving = False

    label_y = 60
    for label in labels:

        label_y += 30
        drawText(label, color, (10, label_y), console=False)

    drawText(msg, color, (10, 40), console=False)
    drawText(f"fps: {fps}", color, (200, 40), console=False)

    T_average = calc_avg_T()
    drawText(f"T avg: {T_average}", color, (400, 40))

    cv2.imshow("feed", frame1)
    frame1 = frame2
    _, frame2 = capture.read()

    if cv2.waitKey(1) == 27:
        break

    t1 = cv2.getTickCount()
    print(
        f"processing took {round((t1-t0)/cv2.getTickFrequency(), 3)} seconds.")


print(f"Measured {len(T_list)} periods, average: {calc_avg_T()}")
g = (4 * 3.14 * 3.14 * lenght) / (calc_avg_T() * calc_avg_T())

print(f"g: {g}")

cv2.destroyAllWindows()
capture.release()
