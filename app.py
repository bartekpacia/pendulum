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


def calc_T() -> tuple[float, float, float]:
    """
    Calculates T.

    Returns a 3-element tuple. First element is average T, second is minimum T,
    third is maximum T.
    """

    T_avg = numpy.mean(T_list)
    T_min = numpy.min(T_list)
    T_max = numpy.max(T_list)
    return (round(T_avg, 2), round(T_min, 2), round(T_max, 2))


def calc_g() -> tuple[float, float, float]:
    """
    Calculates g.

    Returns a 3-element tuple. First element is average g, second is minimum g,
    third is maximum g.
    """
    T_avg, T_min, T_max = calc_T()
    g_avg = (4 * 3.14 * 3.14 * length) / (T_avg**2)
    g_min = (4 * 3.14 * 3.14 * length) / (T_max**2)
    g_max = (4 * 3.14 * 3.14 * length) / (T_min**2)

    return (round(g_avg, 2), round(g_min, 2), round(g_max, 2))


def drawText(
    text: str,
    color: tuple[int, int, int],
    pos: tuple[int, int],
    big=False,
    console=False,
):
    if console:
        print(text)

    if big:
        scale = 1
    else:
        scale = 0.6

    cv2.putText(
        frame1,
        str(text),
        org=pos,
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=scale,
        color=color,
        thickness=3,
    )


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
        dilated, cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE
    )

    time_total = round(time.time() - time_start, 2)
    big_moving_things = 0
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 300:
            continue
        else:
            big_moving_things += 1
            cv2.rectangle(
                frame1, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0), thickness=2
            )

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

            if stops_count % 2 == 0:
                T_timestamp = time.time()
                T_timestamps.append(T_timestamp)
                # ignore first period, it's way too short (video's fault)
                if len(T_timestamps) > 3:
                    T = round(T_timestamp - T_timestamps[-2], 2)
                    T_list.append(T)
                    labels.append(f"T: {T}")

    label_y = 60
    for label in labels:

        label_y += 30
        drawText(label, color, (10, label_y))

    drawText(msg, color, (10, 40))
    drawText(f"total: {time_total}", color, (120, 40))

    if T_list:
        g_avg, _, _ = calc_g()
        drawText(f"g avg: {g_avg}", color, (250, 40))

        T_avg, _, _ = calc_T()
        drawText(f"T avg: {T_avg}", color, (390, 40))

        print(f"g avg: {g_avg}, T avg: {T_avg}, stops count: {stops_count}")

    t1 = cv2.getTickCount()
    processing_time = round((t1 - t0) / cv2.getTickFrequency(), 3)
    print(f"processing took {processing_time} seconds.")

    cv2.imshow("feed", frame1)
    frame1 = frame2
    _, frame2 = capture.read()
    if cv2.waitKey(1) == 27:
        break


T_avg, T_min, T_max = calc_T()
print(
    f"Measured {len(T_list)} full periods. T avg: {T_avg}, T min: {T_min}, T max: {T_max}"
)

g_avg, g_min, g_max = calc_g()
print(f"g avg: {g_avg}, g min: {g_min}, g max: {g_max}")

cv2.destroyAllWindows()
capture.release()
