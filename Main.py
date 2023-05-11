import tkinter as tk
import time
import pyki2


def tick():
    app.label1.after(1000, tick)
    app.entry1.delete(0, 10)
    app.entry1.insert(1, time.strftime('%H:%M:%S'))


def command1():
    print(pyki2.test())
    message = (pyki2.test())
    app.entry2.delete(0, 10)
    string1 = str(message[1]) + ' ' + str(message[3])
    app.entry2.insert(1, string1)
    app.entry3.delete(0, 10)
    string2 = str(message[4]) + ' ' + str(message[10])
    app.entry3.insert(1, string2)


def command3():
    print(pyki2.test())
    message = (pyki2.test())
    app.entry2.delete(0, 10)
    string1 = str(message[11]) + ' ' + str(message[6])
    app.entry2.insert(1, string1)
    app.entry3.delete(0, 10)
    string2 = str(message[2]) + ' ' + str(message[11])
    app.entry3.insert(1, string2)


def command2():
    app.entry2.delete(0, 10)
    app.entry3.delete(0, 10)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Frame 1
        self.frame1 = tk.Frame(self, bd=2, padx=5, pady=5, relief='groove')
        self.label1 = tk.Label(self.frame1, text=time.strftime('%H:%M:%S'))

        self.label1.pack()
        self.button1 = tk.Button(self.frame1, text="START", command=command1)
        self.button1.pack(expand=1, padx=5, pady=5, fill='x')

        self.entry1 = tk.Entry(self.frame1)
        self.entry1.pack(expand=1, padx=5, pady=5)

        self.frame1.pack()

        # Frame 2
        self.frame2 = tk.Frame(self, bd=2, padx=5, pady=5, relief='groove')

        self.button2 = tk.Button(self.frame2, text="STOP", command=command3)
        self.button2.pack(expand=1, padx=5, pady=5, fill='x')

        self.entry2 = tk.Entry(self.frame2)
        self.entry2.pack(expand=1, padx=5, pady=5)

        self.frame2.pack()

        # Frame 3
        self.frame3 = tk.Frame(self, bd=2, padx=5, pady=5, relief='groove')

        self.button3 = tk.Button(self.frame3, text="CLEAR", command=command2)
        self.button3.pack(expand=1, padx=5, pady=5, fill='x')

        self.entry3 = tk.Entry(self.frame3)
        self.entry3.pack(expand=1, padx=5, pady=5)

        self.frame3.pack()

        # EXIT Button
        self.quit = tk.Button(self, text="QUIT", command=self.master.destroy)
        self.quit.pack(expand=1, padx=5, pady=5, fill='x')


root = tk.Tk()
app = Application(master=root)
app.label1.after_idle(tick)
app.mainloop()
