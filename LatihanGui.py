from tkinter import *
from tkinter import ttk, filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import pandas as pd
from random import choice

FILE_LOCATION = "./csv files"
BUTTON_FONT = ("Arial", 13, "bold")
LABEL_FONT = ("Arial", 20, "bold")
USER_FONT = ("Arial", 14, "bold")
INFO_FONT = ("Arial", 12, "bold")
SMALL_FONT = ("Arial", 12, "normal")
COLORS = ['green', 'red', 'purple', 'brown', 'blue']

class Visualization:
    def __init__(self,window):
        self.window = window
        self.window.title('GUI Data Visualization')
        self.window.geometry('1250x720')
        self.window.config(bg='black')
        
        self.df= pd.DataFrame()
        # persiapan variabel untuk histogram
        self.hist_name         = StringVar()        
        # persiapan variabel untuk Scaterplot
        self.scatter_x_name    = StringVar()
        self.scatter_y_name    = StringVar()
         # persiapan variabel untuk pieplot
        self.pie_x_name        = StringVar()
        self.pie_y_name        = StringVar()        
        # persiapan variabel untuk boxplot
        self.box_name          = StringVar()

        # ========================================= LEFT FRAME ======================================== #
        # Button Load Csv
        my_menu = Menu(self.window)
        self.window.config(menu = my_menu)
        self.file_menu = Menu(my_menu, tearoff = False)
        my_menu.add_cascade(label = "Load CSV", menu = self.file_menu)
        self.file_menu.add_command(label = "Open File", command = self.file_open)

        self.left_frame = Frame(self.window, bg = "darkgreen", relief = RIDGE, bd = 1)
        self.left_frame.place(x = 5, y = 20, relwidth= 0.32, relheight= 0.95 )

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background      = "silver",
                        foreground      = "black",
                        rowheight       = 20,
                        fieldbackground = "silver")
        style.map("Treeview", background = [("selected", "medium sea green")])
        style.configure("Treeview.Heading", background = "light steel blue", font = ("Arial", 10, "bold"))

        self.my_table  = ttk.Treeview(self.left_frame)
        scroll_x_label = ttk.Scrollbar(self.left_frame, orient = HORIZONTAL, command = self.my_table.xview)
        scroll_y_label = ttk.Scrollbar(self.left_frame, orient = VERTICAL,   command = self.my_table.yview )
        scroll_x_label.pack(side = BOTTOM, fill = X)
        scroll_y_label.pack(side = RIGHT, fill = Y) 

        # ========================================= Right Frame ========================================#
        # Top Left Canva:--------------------------------------------------------------------------------->

        # Heading and Frame:
        self.hist_heading = Label(self.window, font = SMALL_FONT , text = "Histogram Chart", bg = "green" )
        self.hist_heading.place(x = 415, y = 20, relwidth = 0.32, relheight = 0.04 )

        self.hist_info = Frame(self.window, bg = "green")
        self.hist_info.place(x = 415, y = 50, relwidth = 0.32, relheight = 0.42 )

        # Select option/Combobox and label:
        self.hist_x_label = Label(self.hist_info, font = SMALL_FONT, text = "XLabel", bg = "green", bd = 1)
        self.hist_x_label.grid(row = 0, column = 0, padx = 10)

        self.hist_box = ttk.Combobox(self.hist_info, font = SMALL_FONT, justify = "center", state = "readonly",
                                       textvariable = self.hist_name)
        self.hist_box.grid(row = 0, column = 1)

        # Button:
        self.hist_draw_button = Button(self.hist_info, font = INFO_FONT, text = "draw", justify = "center",
                                       relief = RIDGE, bd = 2, bg = "grey", cursor = "hand2", width = 5,
                                       command = self.draw_hist_chart)
        self.hist_draw_button.grid(row= 0, column = 2, padx = 10)

        self.hist_clean_button = Button(self.hist_info, font = INFO_FONT, text = "clean", justify = "center",
                                        relief = RIDGE, bd = 2, bg = "grey", cursor = "hand2", width = 5,
                                        command = self.clean_hist)
        self.hist_clean_button.grid(row = 1, column = 2, padx = 10)

        #bar diagram replacement:
        self.top_left = Frame(self.window, bg="ivory")
        self.top_left.place(x=425, y=120, width=380, height=225)
        self.canvas_1 = Canvas(self.top_left, width=370, height=250, bg="ivory", relief=RIDGE)
        self.canvas_1.pack()
        self.fig_1 = None
        self.output_1 = None

        # Top Right Canva:--------------------------------------------------------------------------------->

        # Heading and Frame:
        self.box_heading = Label(self.window, font = SMALL_FONT, text = "Boxplot - Detect Outliers", bg = "green")
        self.box_heading.place(x = 852, y = 20, relwidth = 0.32, relheight=0.04)

        self.box_info = Frame(self.window, bg = "green")
        self.box_info.place(x = 852, y = 50, relwidth = 0.32, relheight = 0.42)

        # Select option/Combobox and label:
        self.box_x_label = Label(self.box_info, font = SMALL_FONT, text = "XLabel", bg = "green", bd = 1)
        self.box_x_label.grid(row = 0, column = 0, padx = 10) 

        self.box_box = ttk.Combobox(self.box_info, font = SMALL_FONT, justify = "center", state = "readonly",
                                    textvariable = self.box_name)
        self.box_box.grid(row = 0, column = 1)

        # Button:
        self.box_draw_button = Button(self.box_info, font = INFO_FONT,  text = "Draw", justify = "center",
                                     relief = RIDGE, bd = 2, bg = "grey", cursor = "hand2", width = 5,
                                     command = self.draw_boxplot)
        self.box_draw_button.grid(row = 0, column = 2, padx = 10)

        self.box_clean_button = Button(self.box_info, font = INFO_FONT, text = "Clean", justify = "center",
                                       relief = RIDGE,bd = 2, bg = "grey", cursor = "hand2", width = 5,
                                       command = self.clean_box)
        self.box_clean_button.grid(row = 1, column = 2, padx =10)

        # Bar diagram replacement
        self.top_right = Frame(self.window, bg = "ivory")
        self.top_right.place(x = 862, y = 120, width=380, height=225)
        self.canvas_2 = Canvas(self.top_right, width=380, height=225, bg="ivory", relief=RIDGE)
        self.canvas_2.pack()
        self.fig_2 = None
        self.output_2 = None

        # Bottom Right:---------------------------------------------------------------------------------->
        # Heading and Frame:
        self.scatter_heading = Label(self.window, font = SMALL_FONT, text = "Scatter plot", bg = "green")
        self.scatter_heading.place(x = 415, y = 360, relwidth = 0.32, relheight=0.04)

        self.scatter_info = Frame(self.window, bg = "green")
        self.scatter_info.place(x = 415, y = 390, relwidth = 0.32, relheight = 0.42)

        # Select option/Combobox and label:
        self.scatter_x_label = Label(self.scatter_info, font = SMALL_FONT, text = "XLabel", bg = "green", bd = 1)
        self.scatter_x_label.grid(row = 0, column = 0, padx = 10) 

        self.scatter_y_label = Label(self.scatter_info, font = SMALL_FONT, text = "YLabel", bg = "green", bd = 1)
        self.scatter_y_label.grid(row = 1, column = 0, padx = 10) 

        self.scatter_x_box = ttk.Combobox(self.scatter_info, font = SMALL_FONT, justify = "center", state = "readonly",
                                    textvariable = self.scatter_x_name)
        self.scatter_x_box.grid(row = 0, column = 1)

        self.scatter_y_box = ttk.Combobox(self.scatter_info, font = SMALL_FONT, justify = "center", state = "readonly",
                                          textvariable = self.scatter_y_name)
        self.scatter_y_box.grid(row = 1, column = 1)

        # Button:
        self.scatter_draw_button = Button(self.scatter_info, font = INFO_FONT, text = "Draw", justify = "center",
                                         relief = RIDGE, bd = 2, bg = "grey", cursor = "hand2", width = 5,
                                         command = self.draw_scatter)
        self.scatter_draw_button.grid(row = 0, column = 2, padx = 10)

        self.scatter_clean_button = Button(self.scatter_info, font = INFO_FONT, text = "Clean", justify = "center",
                                           relief = RIDGE, bd = 2, bg = "grey", cursor = "hand2", width = 5,
                                           command = self.clean_scatter)
        self.scatter_clean_button.grid(row = 1, column = 2, padx = 10)
        
        # Bar Diagram Replacement:
        self.bottom_left = Frame(self.window, bg = "ivory")
        self.bottom_left.place(x = 425, y = 460, width = 380, height = 225)
        self.canvas_3 = Canvas(self.bottom_left, width = 380, height = 225, bg = "ivory", relief = RIDGE)
        self.canvas_3.pack()
        self.fig_3 = None
        self.output_3 = None

        # ========================================= FUNCTIONAL ======================================== #
    def file_open(self):
        file_name = filedialog.askopenfilename(
            initialdir = FILE_LOCATION,
            title = "Open A File",
            filetypes = (("csv files", "*.csv" ), ("All Files", "*.*"))
        )
        if file_name:
            try:
                file_name = f"{file_name}"
                self.df = pd.read_csv(file_name)
            except ValueError:
                self.error_info.config(text = "file cannot be opened!")
            except FileNotFoundError:
                self.error_info.config(text = "file cannot be found!")
    
        # clean existing data
        self.clear_table_data()
        # from csv into dataframe:
        self.my_table["column"] = list(self.df.columns)
        self.my_table['show'] = "headings"

        for column in self.my_table['column']:
            self.my_table.heading(column, text = column)
        # resize columns:
        for column_name in self.my_table["column"]:
            self.my_table.column(column_name, width = 60)
        # fill rows with data:
        df_rows_old = self.df.to_numpy()
        df_rows_refreshed = [list(item) for item in df_rows_old]
        for row in df_rows_refreshed:
            self.my_table.insert("", "end", values = row)
        self.my_table.place(x = 5, y = 5, relwidth = 1, relheight = 1 )
        try:
            self.fill_hist_box()
        except TclError:
            pass
        try:
            self.fill_box_box()
        except TclError:
            pass
        try:
            self.fill_scatter_box()
        except TclError:
            pass
        # try:
        #     self.fill_pie_box()
        # except TclError:
        #     pass

    def clear_table_data(self):
        self.my_table.delete(*self.my_table.get_children())

    # ================================ FILL COMBOBOX METHODS ============================= #
        
    def fill_hist_box(self):
        columns = [item for item in self.df]
        x_labels = []
        for column in columns:
            if self.df[column].dtype == "int64" or self.df[column].dtype == "float64":
                x_labels.append(column)
        self.hist_box["values"] = tuple(x_labels)
        self.hist_box.current(0)

    def fill_box_box(self):
        columns = [item for item in self.df]
        x_labels = []
        for column in columns:
            if self.df[column].dtype == "int64" or self.df[column].dtype == "float64":
                x_labels.append(column)
        self.box_box["values"] = tuple(x_labels)
        self.box_box.current(0)

    def fill_scatter_box(self):
        columns = [item for item in self.df]
        x_labels = []
        y_labels = []
        for column in columns:
            if self.df[column].dtype == "int64" or self.df[column].dtype == "float64":
                x_labels.append(column)
                y_labels.append(column)
        self.scatter_x_box["values"] = tuple(x_labels)
        self.scatter_x_box.current(0)
        self.scatter_y_box["values"] = tuple(y_labels)
        self.scatter_y_box.current(0)

     # ===================================== DRAW CHART ================================= #
    # Draw hist:-------------------------------------------------------------------->
    def draw_hist_chart(self):
        self.fig_1 = Figure(figsize=(4, 2), dpi=100)
        axes = self.fig_1.add_subplot(111)
        
        # Get the selected column name from the Combobox
        selected_column = self.hist_box.get()

        # Plot histogram with a random color
        axes.hist(self.df[selected_column], color=choice(COLORS), bins=10)  # Adjust the number of bins as needed

        # Set labels and title
        axes.set_xlabel(selected_column)
        axes.set_ylabel("Frequency")
        axes.set_title("Histogram")

        # Create FigureCanvasTkAgg instance
        self.output_1 = FigureCanvasTkAgg(self.fig_1, master=self.canvas_1)
        self.output_1.draw()
        self.output_1.get_tk_widget().pack()
    
    # Clean hist:
    def clean_hist(self):
        if self.output_1:
            for child in self.canvas_1.winfo_children():
                child.destroy()
        self.output_1 = None

    # Draw boxplot:------------------------------------------------------------------------------->
    def draw_boxplot(self):
        self.fig_2 = Figure(figsize = (4,2), dpi = 100)
        axes = self.fig_2.add_subplot(111)

        selected_column = self.box_box.get()
        
        # plot boxplot with a random color
        # box_color = choice(COLORS)
        axes.boxplot(self.df[selected_column], vert = False)

        # Set Labels and Title
        axes.set_xlabel(selected_column)
        axes.set_ylabel("Frequency")
        axes.set_title("Boxplot")

        # Create FigureCanvasTkAgg instance
        self.output_2 = FigureCanvasTkAgg(self.fig_2, master = self.canvas_2)
        self.output_2.draw()
        self.output_2.get_tk_widget().pack()

    # clean bocplot:
    def clean_box(self):
        if self.output_2:
            for child in self.canvas_2.winfo_children():
                child.destroy()
        self.output_2 = None

    # Draw Scatterplot:--------------------------------------------------------------------------------------->
    def draw_scatter(self):
        self.fig_3 = Figure(figsize = (4,2), dpi =100)
        axes = self.fig_3.add_subplot(111)

        married_column = self.df["Married"]

        # Buat daftar warna sesuai kondisi
        colors = ['red' if status == 'Yes' else 'blue' for status in married_column]

        selected_x_column = self.scatter_x_box.get()
        selected_y_column = self.scatter_y_box.get()

        axes.scatter(x = self.df[selected_x_column], y = self.df[selected_y_column], c = colors)
        self.output_3 = FigureCanvasTkAgg(self.fig_3, master=self.canvas_3)
        self.output_3.draw()
        self.output_3.get_tk_widget().pack()

    def clean_scatter(self):
        if self.output_3:
            for child in self.canvas_3.winfo_children():
                child.destroy()
        self.output_3 = None
        

def LaunchProgram():
    app = Tk()
    Visualization(app)
    app.mainloop()
if __name__ == "__main__":
    LaunchProgram()