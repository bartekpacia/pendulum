from typing import Tuple
import cv2
import time
import numpy

length = float(input("Enter length of the rope (mine's 0.62): "))

print(f"using OpenCV v{cv2.__version__}")

capture = cv2.VideoCapture("film2_vga.mp4")
fps = round(capture.get(cv2.CAP_PROP_FPS), 2)

_, frame1 = capture.read()
_, frame2 = capture.read()

time_start = time.time()
labels = []
stops_list = []
T_list = []
T_half_list = []
T_timestamps = []


def calc_avg_T() -> float:
    avg = numpy.mean(T_list)
    return round(avg, 2)


def calc_g() -> float:
    g = (4 * 3.14 * 3.14 * length) / (calc_avg_T() * calc_avg_T())
    return round(g, 2)


def drawText(text: str,
             color: Tuple[int, int, int],
             pos: Tuple[int, int],
             big=False,
             console=False):
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
stops_count = 0
while capture.isOpened() and frame1 is not None and frame2 is not None:
    t0 = cv2.getTickCount()
    T = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(T, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, threshold = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(threshold, None, iterations=1)
    contours, _ = cv2.findContours(
        dilated, cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

    time_total = round(time.time() - time_start, 2)
    big_moving_things = 0
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 300:
            continue
        else:
            big_moving_things += 1
            cv2.rectangle(frame1, pt1=(x, y), pt2=(x + w, y + h),
                          color=(0, 255, 0), thickness=2)

    if big_moving_things > 0:
        msg = "MOVING"
        color = (0, 255, 0)
        prev_moving = True
    else:
        msg = "NOT MOVING"
        color = (0, 0, 255)
        if prev_moving:
            stops_list.append(time_total)

            if len(stops_list) > 1:
                T_half = round(time_total - stops_list[-2], 2)
            else:
                T_half = 0

            if T_half >= 0.3:
                prev_moving = False
                stops_count += 1
                T_half_list.append(T)

            if (stops_count % 2 == 0):
                T_timestamp = time.time()
                T_timestamps.append(T_timestamp)
                if len(T_timestamps) > 1:
                    T = round(T_timestamp - T_timestamps[-2], 2)
                    T_list.append(T)
                    labels.append(
                        f"T: {T}")

    label_y = 60
    for label in labels:

        label_y += 30
        drawText(label, color, (10, label_y))

    drawText(msg, color, (10, 40))
    drawText(f"total: {time_total}", color, (250, 40))

    T_avg = calc_avg_T()
    drawText(f"T avg: {T_avg}", color, (400, 40))

    cv2.imshow("feed", frame1)
    frame1 = frame2
    _, frame2 = capture.read()

    if cv2.waitKey(1) == 27:
        break

    t1 = cv2.getTickCount()
    print(f"g: {calc_g()}, T avg: {T_avg}, stops_count: {stops_count}")
    print(
        f"processing took {round((t1-t0)/cv2.getTickFrequency(), 3)} seconds.")


print(f"Measured {len(T_list)} full periods, average: {calc_avg_T()}")

print(f"g: {calc_g()}")

cv2.destroyAllWindows()
capture.release()
