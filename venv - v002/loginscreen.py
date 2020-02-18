import tkinter
from AuthenticationClient import authenticate_account
import pickle

global uid
global username
global token
global x_cord
global y_cord
global vel
global playerImg
global map_id


# Let's create the Tkinter window
window = tkinter.Tk()
window.title("Shitty Runescape Logon")
window.geometry("300x100")

# You will create two text labels namely 'username' and 'password' and and two input labels for them
blanklab = tkinter.Label(window, text = "              ").grid(row = 0, column = 0)
usnlab = tkinter.Label(window, text = "Username").grid(row = 0, column = 1) #'username' is placed on position 00 (row - 0 and column - 0)

# 'Entry' class is used to display the input-field for 'username' text label
usnval = tkinter.Entry(window) # first input-field is placed on position 01 (row - 0 and column - 1)
usnval.grid(row = 0, column = 2)
pswlab = tkinter.Label(window, text = "Password").grid(row = 1,column = 1) #'password' is placed on position 10 (row - 1 and column - 0)

pswval = tkinter.Entry(window) #second input-field is placed on position 11 (row - 1 and column - 1)
pswval.grid(row = 1, column = 2)

statustext = tkinter.StringVar()
statustext.set("Please Log In")
statuslab = tkinter.Label(window, textvariable = statustext)
statuslab.grid(row = 3, column=2)

def registered():
    print("Registered")

def submit():
    global uid
    global username
    global token
    global x_cord
    global y_cord
    global vel
    global playerImg
    global map_id

    usn = str(usnval.get())
    psw = str(pswval.get())
    response = authenticate_account(str(usn),str(psw))
    print(response)
    auth = pickle.loads(response[0])
    player = pickle.loads(response[1])


    if auth[0] == "Authentication Failure":
        statustext.set("Authentication Failure")
    elif auth[0] == "Authenticated":
        statustext.set("Authentication Success")
        uid = auth[1]
        username = auth[2]
        token = auth[3]
        x_cord = player[1]
        y_cord = player[2]
        vel = player[3]
        playerImg = player[4]
        map_id = player[5]
        window.destroy()
        print("received: ", auth, player)
    else:
        statustext.set("Error")
        print("received: ", auth)


submit_button = tkinter.Button(window,text="Submit", command=submit).grid(row = 4,column = 1 )
register_button = tkinter.Button(window,text="register", command=registered).grid(row = 4,column = 2)

window.mainloop()