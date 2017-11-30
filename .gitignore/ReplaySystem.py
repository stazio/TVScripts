from tkinter import *
from tkinter.font import Font, nametofont

import telnetlib as telnet

ipAddress = None
def onConnectRequest():
    res,err = connect()
    if res:
        send_command("remote: override: true")
        showGameLayout()
    else:
        showConnectionError(err)

def onPause():
    togglePausedState(True)
    send_command("stop")

def onRecord():
    togglePausedState(False)
    send_command("record")

def play(speed=100):
    send_command("speed: {}".format(speed))
    togglePausedState(False)

def clip(iterate):
    sym = ("+" if iterate >=0 else "")
    send_command("goto clip id: {}{}".format(sym,iterate))
    
def select_cam(num):
    print("Selecting Camera: {}".format(num))

socket = None
def connect():
    global socket, ipAddress
    try:
        socket = telnet.Telnet(str(ipAddress.get()), 9993)
    except Exception as err:
        return (False, err)
    value = socket.read_until("\n").decode()
    if value.strip() == "500 connection info":
        return True
    else:
        return False

def send_command(value, wait_for_response=True):
    print(value)
    return True
    global socket
    socket.write(value.encode())
    if wait_for_response:
        return socket.read_until("\n\n")
    else:
        return None

# Layout System

def onKey(e):
    print(e.keysym, end=': ')
    if e.keysym == "space":
        if isPaused:
            onRecord()
        else:
            onPause()
    # Is Camera
    elif e.keysym == "1": select_cam(1)
    elif e.keysym == "2": select_cam(2)
    elif e.keysym == "3": select_cam(3)
    elif e.keysym == "4": select_cam(4)

    # Is Forward Speed
    elif e.keysym == "q": play(100)
    elif e.keysym == "w": play(75)
    elif e.keysym == "e": play(50)
    elif e.keysym == "r": play(25)
    elif e.keysym == "t": play(10)
    elif e.keysym == "y": play(0)

    # Is Backward Speed
    elif e.keysym == "a": play(-100)
    elif e.keysym == "s": play(-75)
    elif e.keysym == "d": play(-50)
    elif e.keysym == "f": play(-25)
    elif e.keysym == "g": play(-10)
    elif e.keysym == "h": play(0)

    # Choose Recording
    elif e.keysym == "Left": clip(-1)
    elif e.keysym == "Right": clip(+1)

active = Tk()
active.bind("<Key>", onKey)
default_font = nametofont("TkDefaultFont")
default_font.configure(size=32)
active.option_add("*Font", default_font)

def closeWindows():
    global active
    for child in active.winfo_children():
        child.destroy()

def showConnectLayout():
    global active, ipAddress
    closeWindows()
    ipAddress = StringVar()
    Label(active, text="Replay System", compound=CENTER).grid(row=0,column=0, padx=10)
    Entry(active, textvariable=ipAddress).grid(row=1,column=0,padx=10, pady=10)
    Button(active, text="Connect", command=onConnectRequest).grid(row=1,column=1,padx=10, pady=10)

def showConnectionError(text="Error!"):
    if showConnectionError.label != None:
        showConnectionError.label.destroy()
    font = Font()
    font.configure(size=12)
    showConnectionError.label = Label(active, text=text, fg="red", font = font)
    showConnectionError.label.grid(row=2, column=0, columnspan=1, padx=10, pady=10)
showConnectionError.label = None

recordingButton = None
pauseButton = None
isPaused = False
def showGameLayout():
    global active, recordingButton, pauseButton
    closeWindows()
    Label(active, text="Replay System. Built by Staz.IO").grid(row=0, column=1, columnspan=6)
    Button(active, text="Cam 1", command=lambda: select_cam(1)).grid(row=1, column=2, padx=10, pady=20)
    Button(active, text="Cam 2", command=lambda: select_cam(2)).grid(row=1, column=3, padx=10, pady=10)
    Button(active, text="Cam 3", command=lambda: select_cam( 3)).grid(row=1, column=4, padx=10, pady=10)
    Button(active, text="Cam 4", command=lambda: select_cam( 4)).grid(row=1, column=5, padx=10, pady=10)

    Button(active, text="100%", command=lambda: play( 100)).grid(row=2, column=1, padx=10, pady=10)
    Button(active, text="75%", command=lambda: play( 75)).grid(row=2, column=2, padx=10, pady=10)
    Button(active, text="50%", command=lambda: play( 50)).grid(row=2, column=3, padx=10, pady=10)
    Button(active, text="25%", command=lambda: play( 25)).grid(row=2, column=4, padx=10, pady=10)
    Button(active, text="10%", command=lambda: play( 10)).grid(row=2, column=5, padx=10, pady=10)
    Button(active, text="0%", command=onPause).grid(row=2, column=6, padx=10, pady=10)

    Button(active, text="-100%", command=lambda: play( -100)).grid(row=3, column=1, padx=10, pady=10)
    Button(active, text="-75%", command=lambda: play( -75)).grid(row=3, column=2, padx=10, pady=10)
    Button(active, text="-50%", command=lambda: play( -50)).grid(row=3, column=3, padx=10, pady=10)
    Button(active, text="-25%", command=lambda: play( -25)).grid(row=3, column=4, padx=10, pady=10)
    Button(active, text="-10%", command=lambda: play( -10)).grid(row=3, column=5, padx=10, pady=10)
    Button(active, text="0%", command=onPause).grid(row=3, column=6, padx=10, pady=10)
    
    Button(active, text="Previous Recording", command=lambda: clip( -1)).grid(row=4, column=1, columnspan=2, padx=10, pady=10)
    Button(active, text="Next Recording", command=lambda: clip( +1)).grid(row=4, column=5, columnspan=2, padx=10, pady=10)

    # Record / Stop Button
    recordingButton = Button(active, text="Record", bg="red",  command=onRecord)
    pauseButton = Button(active, text="Stop", bg="yellow", command=onPause)
    togglePausedState()

    font = Font()
    font.configure(size=12)

    Label(active, text="Recording 5 out of 10", font=font).grid(row=5, column=1, columnspan=6, padx=10, pady=0)
    Label(active, text="00:00:00", font=font, justify=CENTER).grid(row=6, column=1, columnspan=10)
    Label(active, text="Connected to 192.168.1.1", font=font).grid(row=7, column=1, columnspan=6, padx=10, pady=0)
    
def togglePausedState(newState=None):
    global isPaused, recordingButton, pauseButton
    if newState == None:
        if isPaused:
            isPaused = False
        else:
            isPaused = True
    else:
        isPaused = newState

    if isPaused:
        pauseButton.grid_forget()
        recordingButton.grid(row=4, column=3, columnspan=2, padx=10, pady=10)
    else:
        recordingButton.grid_forget()
        pauseButton.grid(row=4, column=3, columnspan=2, padx=10, pady=10)

showConnectLayout()
active.mainloop()
