# Importing Modules
import tkinter
from tkinter.constants import ANCHOR
import cv2
import PIL.Image
import PIL.ImageTk
from functools import partial
import threading
import time
import imutils
import sys

# Functions for the playback

stream = cv2.VideoCapture("clip.mp4")


def play(speed):
    frames1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frames1 + speed)

    grabbed, frames = stream.read()
    if not grabbed:
        pass
    try:
        frames = imutils.resize(frames, width=SET_WIDTH, height=SET_HEIGHT)
        frames = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frames))
        canvas.image = frames
        canvas.create_image(0, 0, image=frames, anchor=tkinter.NW)
        canvas.create_text(175, 25, fill="white",
                           font="Arial 30 bold", text="Decision Pending")
    except Exception:
        canvas.create_text(1000, 25, fill="white",
                           font="Arial 30 bold", text="The End Of Clip Has Arrived")


def pending(decision):
    '''
    1. Display decision pending image
    2. Wait for a second
    3. Display Sponsor
    4. Wait for a second
    5. Display Out/NotOut
    '''
    frame = cv2.cvtColor(cv2.imread(
        "drs_pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

    time.sleep(1.5)

    frame_2 = cv2.cvtColor(cv2.imread(
        "drs_sponsor.png"), cv2.COLOR_BGR2RGB)
    frame_2 = imutils.resize(frame_2, width=SET_WIDTH, height=SET_HEIGHT)
    frame_2 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame_2))
    canvas.image = frame_2
    canvas.create_image(0, 0, image=frame_2, anchor=tkinter.NW)

    time.sleep(1.5)

    if decision == 'out':
        decisionImg = "drs_out.png"

    else:
        decisionImg = "drs_notout.png"

    frame_3 = cv2.cvtColor(cv2.imread(
        decisionImg), cv2.COLOR_BGR2RGB)
    frame_3 = imutils.resize(frame_3, width=SET_WIDTH, height=SET_HEIGHT)
    frame_3 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame_3))
    canvas.image = frame_3
    canvas.create_image(0, 0, image=frame_3, anchor=tkinter.NW)


def outFunc():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()


def NotoutFunc():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()


def exitProg():
    sys.exit()


# width and height of window
SET_WIDTH = 1280
SET_HEIGHT = 720

# tkinter gui starts here
window = tkinter.Tk()
window.title("Kuldeep's Third Umpire Review System")
cvImage = cv2.cvtColor(cv2.imread(
    "drs_welcome.png"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cvImage))
image_on_canvas = canvas.create_image(0, 0, anchor=tkinter.NW, image=photo)
canvas.pack()

# Buttons To Control The Clip
btnPF = tkinter.Button(window, text="<< Previous(fast)",
                       width=181, height=2, command=partial(play, -25))
btnPF.pack(pady=0.5)

btnPS = tkinter.Button(window, text="<< Previous(slow)",
                       width=181, height=2, command=partial(play, -2))
btnPS.pack(pady=0.5)

btnNF = tkinter.Button(window, text="Next(fast) >>",
                       width=181, height=2, command=partial(play, 25))
btnNF.pack(pady=0.5)

btnNS = tkinter.Button(window, text="Next(slow) >>",
                       width=181, height=2, command=partial(play, 2))
btnNS.pack(pady=0.5)

btnO = tkinter.Button(window, text="Give Out", width=181,
                      height=2, command=outFunc)
btnO.pack(pady=0.5)

btnNO = tkinter.Button(window, text="Give Not Out",
                       width=181, height=2, command=NotoutFunc)
btnNO.pack(pady=0.5)

btnE = tkinter.Button(window, text="Exit", width=181,
                      height=2, command=exitProg)
btnE.pack(pady=0.5)

window.mainloop()
