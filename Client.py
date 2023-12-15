import socket
import threading
import tkinter
from tkinter import simpledialog, messagebox
from tkinter import scrolledtext
from datetime import datetime

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 49776  # The port used by the server


class client:
    def __init__(self):
        # Create a socket object
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

        # GUI
        window = tkinter.Tk()
        window.withdraw()

        while window:

            self.username = simpledialog.askstring("Username", "Please Enter your username", parent=window)

            if self.username:
                self.gui_done = False
                self.running = True

                gui_thread = threading.Thread(target=self.GuiClient)
                receive_thread = threading.Thread(target=self.client_receive)
                gui_thread.start()
                receive_thread.start()
                window.mainloop()
            else:
                messagebox.showwarning("WARNING !", "Username is Required")

    def GuiClient(self):

        self.ui = tkinter.Tk()
        #  welcome msg
        self.ui.title("Welcome : " + self.username)
        self.ui.resizable(width=False, height=False)
        self.ui.configure(width=470, height=550, bg="#b3ffff")

        #  Time
        self.t_label = tkinter.Label(self.ui)
        self.t_label = datetime.now().strftime('%H:%M %p')

        #List box for online users
        #self.clients_list = tkinter.Listbox(self.ui, height=10, width=50)
        #self.clients_list.pack()

        # create a Label widget to display the number of connected clients
        #self.num_clients_label = tkinter.Label(self.win, text="Number of clients: 0")
        #self.num_clients_label.pack()


        self.chatlabel = tkinter.Label(self.ui, text=" WELCOME TO THE CHATAPP ", bg="lightgray")
        self.chatlabel.config(font=("Arial", 12))
        self.chatlabel.pack(padx=20, pady=5)

        self.textarea = tkinter.scrolledtext.ScrolledText(self.ui, bg="#ffffff")
        self.textarea.pack(padx=20, pady=5)
        self.textarea.config(state='disabled')

        self.msglabel = tkinter.Label(self.ui, text="Type Your Message ", bg="lightgray")
        self.msglabel.config(font=("Arial", 12))
        self.msglabel.pack(padx=20, pady=5)

        self.inputarea = tkinter.Text(self.ui, height=5, bg="#ffffff")
        self.inputarea.config(font=("Arial", 12))
        self.inputarea.pack(padx=20, pady=5)

        self.connectButton = tkinter.Button(self.ui, bg="#ffff80", text="Send", command=self.client_send)
        self.connectButton.config(font=("Arial", 12))
        self.connectButton.pack(padx=20, pady=5)


        self.gui_done = True
        # to terminate the window
        self.ui.protocol("WM_DELETE_WINDOW", self.stop)
        self.ui.mainloop()

    def stop(self):
        self.running = False
        self.ui.destroy()
        self.sock.close()
        exit(0)

    def client_send(self):

        #  get msg
        message = f"\n{self.t_label}\n{self.username}: {self.inputarea.get('1.0', 'end')}"

        # Empty Message handling
        if not len(self.inputarea.get('0.0', 'end')) == 1:
            #  send msg
            self.sock.send(message.encode('utf-8'))
            self.inputarea.delete('1.0', 'end')
        else:
            #  show error
            messagebox.showwarning("Message", "Please Enter a Message")

    def client_receive(self):

        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'username?':
                    self.sock.send(self.username.encode('utf-8'))

                #elif message.startswith("[") and message.endswith("]"):
                    #clients = eval(message)
                    #self.clients_list.delete(0, tkinter.END)
                    #for client in clients:
                        #self.clients_list.insert(tkinter.END, client)

                    #num_clients = len(clients)
                    #self.num_clients_label.config(text=f"Number of clients: {num_clients}")

                else:
                    if self.gui_done:
                        self.textarea.config(state='normal')
                        self.textarea.insert('end', message)
                        self.textarea.yview('end')
                        self.textarea.config(state='disabled')

            except:
                self.sock.close()
                exit(0)


client = client()