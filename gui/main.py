from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import shapefile as shp
import os
import sys
sys.path.append("../")

from forecast_appending.with_owm_past import with_owm_past
from forecast_appending.from_past_year import from_past_year
from write_swat_from_db import write_swat_from_db

from shape_files_plot.plot_output import plot_output
from parse_output.parse_output import get_vals, parse_output

w = 800
h = 600
swat_path = ""


class MyFrame(Tk):
    """Class for main window"""
    def __init__(self):
        Tk.__init__(self)
        self.title("Desna SWAT tool")
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw / 2) - (w / 2)
        y = (sh / 2) - (h / 2)
        self.geometry("%dx%d+%d+%d" % (w, h, x, y))
        upd_db_fr = Frame(self, bg='cyan', height=120, pady=3)
        select_dir_fr = Frame(self, bg='gray', height=120, pady=3)
        select_inp_type_fr = Frame(self, bg='green', height=120, pady=3)
        start_modeling_fr = Frame(self, bg='red', height=120, pady=3)
        go_to_viz_fr = Frame(self, bg='yellow', height=120, pady=3)

        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)

        upd_db_fr.grid(row=0, sticky='ew')
        select_dir_fr.grid(row=1, sticky='ew')
        select_inp_type_fr.grid(row=2, sticky='ew')
        start_modeling_fr.grid(row=3, sticky='ew')
        go_to_viz_fr.grid(row=4, sticky='ew')

        upd_db_butt = Button(upd_db_fr, text="check db update", width=20,
                            command=lambda: update_db(upd_db_fr))
        upd_label = Label(upd_db_fr, text="Update status: nothing to update.")
        upd_db_butt.grid(row=0, column=0, pady=45)
        upd_label.grid(row=0, column=1, padx=50)

        swat_dir_label = Label(select_dir_fr, text="SWAT Directory path:")
        select_swat_dir = Button(select_dir_fr, text="Select SWAT project path", width=20,
                                command= lambda: self.getDir(swat_dir_label))
        select_swat_dir.grid(row=0, column=0, pady=45)
        swat_dir_label.grid(row=0, column=1, padx=50)

        variable = StringVar(select_inp_type_fr)
        variable.set("Select type of input file")
        select_type_of_inp_files = OptionMenu(select_inp_type_fr, variable,
            "from past year", "with owm past")
        select_type_of_inp_files.grid(row=0, column=0, padx=300, pady=45)

        start_modeling_butt = Button(start_modeling_fr, text="Start modeling", width=20,
                                    command=lambda: perform_modeling(variable.get()))
        modeling_status_label = Label(start_modeling_fr,
            text="Modeling status: modeling didn't started.")
        start_modeling_butt.grid(row=0, column=0, pady=45)
        modeling_status_label.grid(row=0, column=1, padx=50)

        go_to_viz_butt = Button(go_to_viz_fr, text="Go to output vizualization", width=30,
            command=self.plot_output
            )
        go_to_viz_butt.grid(padx=275, pady=45)

    def plot_output(self):
        dir_content = os.listdir(swat_path)
        shp_file = ""
        for el in dir_content:
            if el.endswith('.shp'):
                shp_file = el
        sf = shp.Reader(swat_path + '/' + shp_file)
        



    def getDir(self, swat_dir_label):
        dirname = filedialog.askdirectory()
        global swat_path
        swat_path = dirname
        swat_dir_label['text'] = "SWAT Directory path:" + dirname


def update_db(upd_db_fr):
    print(upd_db_fr)
    print("updating db")


def perform_modeling(option):
    print(option)
    if option == "from past year":
        print(swat_path)
        write_swat_from_db(swat_path)
        print("from past year")
        from_past_year(swat_path)
        return

    if option == "with owm past":
        print(swat_path)
        write_swat_from_db(swat_path)
        print("write_swat_from_db done")
        with_owm_past(swat_path)
        print("with owm path done")
        return



def main():
    root = MyFrame()
    root.mainloop()



if __name__ == '__main__':
    main()