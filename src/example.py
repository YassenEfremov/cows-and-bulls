from tkinter import *

root = Tk()

root.title("Cows and bulls")
root.geometry("960x540")

start = Button(root, text="Create lobby", command=server.server_start)
start.pack(side=TOP)
stop = Button(root, text="Close lobby", command=test_client.server_stop)
stop.pack(side=TOP)

root.mainloop()
