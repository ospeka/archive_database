from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from .main import perform_all

w = 800
h = 250

class MyFrame(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Input file creator")
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw / 2) - (w / 2)
        y = (sh / 2) - (h / 2)
        self.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.buttonGetDir = Button(self, text="Browse", command=self.getDir, width=10)
        self.buttonOk = Button(self, text="Ok", command=self.perf_grab, width=10)
        self.dirLabel = Label(text="Directory path:")
        self.buttonGetDir.pack(side=LEFT)
        self.dirLabel.pack(side=LEFT)
        self.buttonOk.pack(side=RIGHT)

    def getDir(self):
        dirname = filedialog.askdirectory()
        self.dirLabel['text'] = "Directory path:" + dirname

    def perf_grab(self):
        labelText = self.dirLabel['text']
        dirpath = labelText[labelText.find(':') + 1:]
        if (len(dirpath) == 0):
            messagebox.showinfo(title="Incorrect directory", message="Please choose right directory.")
            return
        perform_all(dirpath)

def main():
    root = MyFrame()
    root.mainloop()

if __name__ == '__main__':
    main()
