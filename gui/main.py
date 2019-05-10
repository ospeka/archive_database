from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import shapefile as shp
import os
import sys
import matplotlib
import sqlite3
import datetime as dt
from dateutil import parser
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.path import Path
import matplotlib.colors as mcolors
import matplotlib.cm as cm

sys.path.append("../")

from forecast_appending.with_owm_past import with_owm_past
from forecast_appending.from_past_year import from_past_year
from write_swat_from_db import write_swat_from_db

from shape_files_plot.plot_output import plot_output
from parse_output.parse_output import get_vals, parse_output
import update_db
from ua_stations.ua_st_update import ua_st_update
import update_db as upd_ru_db

w = 800
h = 600
swat_path = ""
swate_exe_name = "rev670_64rel.exe"
db_path = "../db.sqlite"
ua_ids = "../ua_stations/ua_ids.json"
city_ids_path = "../city_ids.json"
update_data_dir = "../update_data/"

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

        upd_db_butt = Button(upd_db_fr, text="Update database", width=20,
                            command=lambda: update_db(upd_db_fr))
        update_status = get_update_status()
        upd_label = Label(upd_db_fr, text=update_status)
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
        plot_window = Toplevel(self)
        plot_window.title("Visualization window")
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw / 2) - (w / 2) + 100
        y = (sh / 2) - (h / 2) + 100
        plot_window.geometry("%dx%d+%d+%d" % (w, h, x, y))
        sf = self._get_shapefile()
        
        parsed_output = parse_output(swat_path + '/output.sub')
        col_names = list(parsed_output[0].keys())

        variable = StringVar(plot_window)
        variable.set("Select column of output file")
        select_column = OptionMenu(plot_window, variable,
            *col_names)
        select_column.pack(anchor="w")

        value_box_var = StringVar()
        value_box = Entry(plot_window, textvariable=value_box_var)
        value_box.insert(0, "Here will be value.")
        value_box.configure(state='readonly')


        fig = Figure(figsize=(8, 8))
        ax = fig.add_subplot(111)
        ax.set_facecolor((1.0, 0.47, 0.42))
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        plot_button = Button(plot_window, text="Plot graph",
        command=lambda: self.plot_graph(fig, ax, plot_window,
            variable, parsed_output, sf, canvas, value_box, value_box_var))
        plot_button.pack()
        value_box.pack()
        canvas.get_tk_widget().pack()
        

        # canvas = FigureCanvasTkAgg(fig, master=plot_window)
        # canvas.get_tk_widget().pack()
        # canvas.draw()


    def plot_graph(self, fig, ax, plot_window, variable, parsed_output, sf, canvas, value_box, value_box_var):
        shapes = sf.shapes()
        col_name = variable.get()
        if col_name == 'Select column of output file':
            return
        ax.set_title(col_name)
        vals = get_vals(col_name, parsed_output, day=1)

        pols = []
        colors_cm = []
        diff = max(vals) - min(vals)
        if diff == 0:
            messagebox.showerror("Error", "min and max value of column are equal\n or all values are equal")
            return
        norm_values = [(val - min(vals)) / diff for val in vals]
        for shape, val in zip(shapes, norm_values):
            points = shape.points
            x = [el[0] for el in points]
            y = [el[1] for el in points]
            color_val = 1 - val
            rgb = color_val, color_val, 0.9
            colors_cm.append(rgb)
            ax.fill(x, y, color=rgb)
            ax.plot(x, y, color=(1.0, 0.47, 0.42), linewidth=0.5)
            path_inp = [[xi, yi] for xi, yi in zip(x, y)]
            pols.append(path_inp)
        pathes = [Path(el) for el in pols]
        colors_cm = sort_colors(colors_cm)
        mycmp = mcolors.LinearSegmentedColormap.from_list(name='custom',
        colors=colors_cm, N=10)
        normalize = mcolors.Normalize(vmin=min(vals), vmax=max(vals))
        scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=mycmp)
        scalarmappaple.set_array(vals)

        flag = 0
        try:
            cb_axes = fig.axes[1]
        except IndexError:
            flag = 1
        if flag == 0:
            cb = fig.colorbar(scalarmappaple, cax=fig.axes[1])
        else:
            cb = fig.colorbar(scalarmappaple)

        fig.canvas.mpl_connect('button_press_event',
            lambda event: self.onclick(event, fig, ax, pathes, vals, value_box, value_box_var))

        canvas.draw()

    def onclick(self, event, fig, ax, pathes, values, value_box, value_box_var):
        if event.inaxes == ax:
            x, y = round(event.xdata, 1), round(event.ydata, 1)
            text = ''
            index = -1
            for path, i in zip(pathes, range(1, 117)):
                if path.contains_point([x, y]):
                    text += str(i)
                    index = pathes.index(path)
            text += ": " + str(values[index])
            if index == -1:
                text = "Not a subbasin."
            value_box_var.set(text)
            value_box.insert(0, text)


    def _get_shapefile(self):
        dir_content = os.listdir(swat_path)
        shp_file = ""
        for el in dir_content:
            if el.endswith('.shp'):
                shp_file = el
        sf = shp.Reader(swat_path + '/' + shp_file)
        return sf
        

    def getDir(self, swat_dir_label):
        dirname = filedialog.askdirectory()
        global swat_path
        swat_path = dirname
        swat_dir_label['text'] = "SWAT Directory path:" + dirname


def get_update_status():
    con = sqlite3.connect('../db.sqlite')
    cursor = con.cursor()
    table_names_res = cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table';
    """).fetchall()
    table_names = [el[0] for el in table_names_res]
    tommorow = dt.date.today() - dt.timedelta(days=1)
    for name in table_names:
        res = cursor.execute("""
            SELECT max(dt) FROM {}
            """.format(name)).fetchall()
        max_dt = parser.parse(res[0][0]).date()
        if tommorow != max_dt:
            return "Update needed!"
    return "Update doesn't needed."
    


def update_db(upd_db_fr):
    # ua_st_update(db_path, ua_ids)
    upd_ru_db.update_db(db_path, city_ids_path, update_data_dir)
    


def perform_modeling(option):
    print(option)
    if option == "from past year":
        print(swat_path)
        write_swat_from_db(swat_path)
        print("from past year")
        from_past_year(swat_path)
        execute_swat(swat_path)
        return

    if option == "with owm past":
        print(swat_path)
        write_swat_from_db(swat_path)
        print("write_swat_from_db done")
        with_owm_past(swat_path)
        print("with owm path done")
        execute_swat(swat_path)
        return

def execute_swat(path):
    swat_exe_path = path + "/" + swate_exe_name
    print(swat_exe_path)
    print("swat execution ...")
    # os.system(swat_exe_path)

def sort_colors(colors):
    # super hard to understand function that sort colors
    # for my own colorbar
    d = {k: v for k, v in zip(colors, range(len(colors)))}
    d_sums = {sum(k): v for k, v in d.items()}
    sorted_sums = list(d_sums.keys())
    sorted_sums = sorted(sorted_sums)
    good_order = [d_sums[el] for el in sorted_sums]
    ret = []
    d_reversed = {v: k for k, v in d.items()}
    for ind in good_order:
        ret.append(d_reversed[ind])
    return ret[::-1]

def main():
    root = MyFrame()
    root.mainloop()



if __name__ == '__main__':
    main()