### GUI for Kaskad2P Validating station
### Use with pyki2.py library
### 

import tkinter as tk
import pyki2
import time

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def tick(self):
        app.entry1.after(2000, app.tick)
        app.entry1.delete(0, 10)
        app.entry1.insert(0, time.strftime('%H:%M:%S'))
        app.entry2.delete(0, 100)
        app.entry2.insert(0, pyki2.SpprCmdGet())

    def create_widgets(self):
        #Frame 1
        self.frame1 = tk.Frame(self, bd=2, padx=5, pady=5, relief='groove')
        # self.label1 = tk.Label(self.frame1, text=time.strftime('%H:%M:%S'))
        # self.label1.pack()
        
        # self.button1 = tk.Button(self.frame1, text="Button1", command=self.command1)
        # self.button1.pack(expand=1, padx=5, pady=5, fill='x')

        self.entry1 = tk.Entry(self.frame1)
        self.entry1.pack(expand=1, padx=5, pady=5)
        
        self.frame1.pack()

        #Frame 2
        self.frame2 = tk.Frame(self, bd=2, padx=5, pady=5, relief='groove')

        self.entry2 = tk.Entry(self.frame2)
        self.entry2.pack(expand=1, padx=5, pady=5)

        self.entry3 = tk.Entry(self.frame2)
        self.entry3.pack(expand=1, padx=5, pady=5)

        self.frame2.pack()

        #Frame 3
        self.frame3 = tk.Frame(self, bd=2, padx=5, pady=5, relief='groove')
                
        self.button2 = tk.Button(self.frame3, text="Старт", command=self.mesure)
        self.button2.pack(expand=1, padx=5, pady=5, fill='x')
        
        self.button3 = tk.Button(self.frame3, text="Стоп", command=self.stopmesure)
        self.button3.pack(expand=1, padx=5, pady=5, fill='x')

        self.frame3.pack(fill='x')

        #EXIT Button
        self.quit = tk.Button(self, text="QUIT", command=self.master.destroy)
        self.quit.pack(expand=1, padx=5, pady=5, fill='x')

    def command1(self):
        print(time.strftime('%H:%M:%S'))

    def mesure(self):
        print("Start")
        pyki2.SpprCmdTMeasure(600)
        
    def stopmesure(self):
        print("Stop")
        app.entry2.insert(0, pyki2.SpprCmdGetAndReset())
        app.entry2.delete(0, -1)
        app.entry3.insert(0, app.entry2.get())


root = tk.Tk()
app = Application(master=root)
app.entry1.after_idle(app.tick)
pyki2.preparation()
app.mainloop()