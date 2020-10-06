import socket
import threading
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import filedialog
from DataEncrypt import DataEncrypt
data = DataEncrypt()

try:
    running = True
    # Listening to Server and Sending Nickname
    def receive():
        while running:
            try:
                # Receive Message From Server
                # If 'NICK' Send Nickname
                message = client.recv(1024)
                message = data.decryptData(message)
                if message == "NICK":
                    client.send(data.encryptData(nickname))
                else:
                    messageField.configure(state="normal")
                    messageField.insert(END, message + '\n')
                    messageField.configure(state="disable")
                    messageField.yview(END)
            except:
                # Close Connection When Error
                client.close()
                break

    # Send message
    def send(*args):
        try:
            message = textField.get()
            message = message.strip()
            if message != "":
                message = '{}: {}'.format(nickname, message)
                client.send(data.encryptData(message))
                textField.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", e)

    # Close window and leave chat
    def onClose():
        cancel = messagebox.askyesno("Exit", "Are you sure you want to exit")
        if cancel:
            global running
            root.destroy()
            running = False
            client.send("\\dis".encode('utf-8'))
            client.close()

    def addImg():
        pass
        # try:
        #     global img
        #     file = filedialog.askopenfilename()
        #     img = PhotoImage(file = file)
        #     messageField.image_create(END, image = img)
        # except Exception as e:
        #     messagebox.showerror("Error", e)

    root = Tk()
    root.title("Chat Client")
    root.geometry("600x450")
    iconImg = PhotoImage(file='icon.png')
    root.iconphoto(False, iconImg)

    # Get server name and nickname to use for server
    SERVER = simpledialog.askstring("Input", "Enter Server")
    nickname = simpledialog.askstring("Input", "Enter name")

    messageField = Text(root, height=25.5, width=80)
    textField = Entry(root, width=80, borderwidth=2)

    scroll = Scrollbar(root)
    button_send = Button(root, text="SEND", width=8, height=1, command=lambda: send())
    buttonImg = PhotoImage(file = "gallery.png")
    button_addImg = Button(root, text="Add Image", width=25, height=15, image = buttonImg, command=addImg)
    textField.bind("<Return>", send)

    scroll.pack(side=RIGHT, fill=Y)
    messageField.pack()
    textField.place(x=30, y=425)
    button_send.place(x=515, y=420)
    button_addImg.place(x=0, y=425)

    messageField.config(yscrollcommand=scroll.set)
    scroll.config(command=messageField.yview)

    # Connecting To Server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, 5050))

    # Starting Threads For Listening And Writing
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    send_thread = threading.Thread(target=send)
    send_thread.start()

    root.protocol("WM_DELETE_WINDOW", onClose)
    root.resizable(False, False)

    root.mainloop()
except Exception as e:
    messagebox.showerror("Error", str(e))
