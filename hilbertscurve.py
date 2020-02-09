import tkinter as tk
import colorsys
from PIL import Image

order = 1
N = 2 ** order
total = N ** 2
width = 800

window = tk.Tk()
black = '#%02x%02x%02x' % (18, 18, 18)
window.configure(bd=0, background=black)

path = []


# return xy of given point at index of where it is in the hilberts curve

def hilbert(index):
    points = [[0, 0],
              [0, 1],
              [1, 1],
              [1, 0]]

    newI = index & 3

    v = points[newI]

    for i in range(order):
        i += 1
        index = index >> 2
        newI = index & 3
        le = 2 ** i
        if newI == 0:
            z = v[0]
            v[0] = v[1]
            v[1] = z
        elif newI == 1:
            v[1] += le
        elif newI == 2:
            v[0] += le
            v[1] += le
        elif newI == 3:
            z = le - 1 - v[0]
            v[0] = le - 1 - v[1]
            v[1] = z
            v[0] += le

    return v


# create a list with all points in the curve


def createPoints():
    global path
    path = []
    for point in range(total):
        path.append(hilbert(point))
        l = width / N
        path[point] = [x * l for x in path[point]]
        path[point] = [x + (l / 2) for x in path[point]]


createPoints()

cv = tk.Canvas(window, width=width, height=800)
cv.configure(bd=0, background=black, highlightthickness=0)
cv.pack()

im = Image.open("Niccc.jpg")
pixels = im.load()

counter = 0


def draw():
    global counter
    global order
    global N
    global total
    i = counter
    speed = 1

    if order < 4:
        speed = 20

    rgb = tuple([int(round(x * 255, 0)) for x in colorsys.hls_to_rgb(i / total, 0.5, 1)])

    color = '#%02x%02x%02x' % pixels[path[i][0], path[i][1]]  # rgb to hex conversion (insert rgb instead of pixels if
    # you want rainbow colors)
    cv.create_line(path[i], path[i + 1], fill=color)
    counter += 1

    if counter >= total - 1:
        counter = 0
        if order > 8:
            return
        order += 1
        N = 2 ** order
        total = N ** 2
        createPoints()
        print(counter)
        cv.delete("all")

    cv.after(speed, draw)


draw()
window.mainloop()
