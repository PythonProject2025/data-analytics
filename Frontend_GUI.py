from tkinter import Tk, Canvas, Button, PhotoImage, filedialog, messagebox
from pathlib import Path
import customtkinter
import pandas as pd
import requests
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import time
from threading import Timer

# Define the assets path
ASSETS_PATH_PAGE1 = Path(r"C:\Users\RAJAVEL MS\myproject\TestAPI\assets\frame0")
ASSETS_PATH_PAGE2 = Path(r"C:\Users\RAJAVEL MS\myproject\TestAPI\assets\frame1")
ASSETS_PATH_PAGE3 = Path(r"C:\Users\RAJAVEL MS\myproject\TestAPI\assets\frame2")




def relative_to_assets_page1(path: str) -> Path:
    return ASSETS_PATH_PAGE1 / Path(path)


def relative_to_assets_page2(path: str) -> Path:
    return ASSETS_PATH_PAGE2 / Path(path)


def relative_to_assets_page3(path: str) -> Path:
    return ASSETS_PATH_PAGE3 / Path(path)


class BasePage:
    def __init__(self, app):
        self.app = app
        self.canvas = app.canvas
        self.page_widgets = []

    def create_common_elements(self):
        image_3 = PhotoImage(file=relative_to_assets_page1("image_3.png"))
        img_3 = self.canvas.create_image(814.0, 34.0, image=image_3)
        self.page_widgets.append((img_3, image_3))

        image_5 = PhotoImage(file=relative_to_assets_page1("image_5.png"))
        img_5 = self.canvas.create_image(35, 384, image=image_5 )
        self.page_widgets.append((img_5, image_5))

    def Slidebar(self):

        image_4 = PhotoImage(file=relative_to_assets_page1("image_4.png"))
        img_4 = self.canvas.create_image(165, 384, image=image_4)
        self.page_widgets.append((img_4, image_4))

        image_da = PhotoImage(file=relative_to_assets_page1("button_1.png"))
        img_da = self.canvas.create_image(164.0, 87, image=image_da)
        self.page_widgets.append((img_da, image_da))

        self.app.create_button_with_hover(
            relative_to_assets_page1("Help_Button.png"),
            relative_to_assets_page1("Help_button_hover.png"),
            (95.0, 125.0, 137.0, 45.0),
             lambda: self.app.show_page(Help_Page),
        )
 
        #Help Text
        text_1 = self.canvas.create_text(
            154.0, 145.0, anchor="nw", text="Help", fill="#87888C", font=("Inter Medium", 12 * -1)
        )
        self.page_widgets.append((text_1, None))

        text_2 = self.canvas.create_text(
            154.0, 200.0, anchor="nw", text="Mode", fill="#87888C", font=("Inter Medium", 12 * -1)
        )
        self.page_widgets.append((text_2, None))

        mode_button = PhotoImage(file=relative_to_assets_page1("button_3.png"))
        button_3 = Button(
            image=mode_button,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("Mode Button clicked"),
            relief="flat",
        )
        button_3.place(x=120.0, y=195.0, width=26.0, height=23.0)
        self.page_widgets.append((button_3, mode_button))

    def clear_canvas(self):
        """Clear all widgets and canvas elements from the page."""
        for widget, ref in self.page_widgets:
            if isinstance(widget, int):  # Canvas item
                self.canvas.delete(widget)
            else:  # Tkinter widget
                widget.destroy()
        self.page_widgets.clear()


class FirstPage(BasePage):
    def display(self):
        self.clear_canvas()
        self.create_common_elements()
        self.Slidebar()

        # Add First Page Specific Elements
        image_1 = PhotoImage(file=relative_to_assets_page1("image_1.png"))
        img_1 = self.canvas.create_image(751.0, 391.0, image=image_1)
        self.page_widgets.append((img_1, image_1))

        image_2 = PhotoImage(file=relative_to_assets_page1("image_2.png"))
        img_2 = self.canvas.create_image(746.0, 387.0, image=image_2)
        self.page_widgets.append((img_2, image_2))

        text_3 = self.canvas.create_text(
            599.0,
            432.0,
            anchor="nw",
            text="Upload Files Here (.csv or .zip)",
            fill="#FFFFFF",
            font=("Inter Bold", 20 * -1),
        )
        self.page_widgets.append((text_3, None))

        self.app.create_button_with_hover(
            relative_to_assets_page1("button_4.png"),
            relative_to_assets_page1("button_hover_2.png"),
            (673.0, 322.0, 122.0, 99.0),
            self.app.upload_file,
        )


class SecondPage(BasePage):
    def __init__(self, app, file_path):
        super().__init__(app)
        
        self.file_name = file_path.split("/")[-1]
        self.file_path = file_path

    def display(self):
        self.clear_canvas()
        self.create_common_elements()
        self.Slidebar()

        image_3 = PhotoImage(file=relative_to_assets_page1("image_3.png"))
        img_3 = self.canvas.create_image(814.0, 34.0, image=image_3)
        self.page_widgets.append((img_3, image_3))

        # Add Second Page Specific Elements
        image_5 = PhotoImage(file=relative_to_assets_page2("image_5.png"))
        img_5 = self.canvas.create_image(773.0, 120.0, image=image_5)
        self.page_widgets.append((img_5, image_5))

        text_3 = self.canvas.create_text(
            696.0,
            103.0,
            anchor="nw",
            text=self.file_name,
            fill="#FFFFFF",
            font=("Inter SemiBold", 20 * -1),
        )
        self.page_widgets.append((text_3, None))

        self.app.create_button_with_hover(
            relative_to_assets_page2("button_2.png"),
            relative_to_assets_page2("button_hover_1.png"),
            (938.0, 101.0, 30.0, 37.0),
            (lambda: self.app.show_page(FirstPage)),
        )
        image_6 = PhotoImage(file=relative_to_assets_page2("image_6.png"))
        img_6 = self.canvas.create_image(758.0, 190.0, image=image_6)
        self.page_widgets.append((img_6, image_6))


        # Buttons
        button_1 = PhotoImage(file=relative_to_assets_page2("button_1.png"))
        btn_1 = Button(
            image=button_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: (self.app.show_page(Data_Filtering,self.file_path),self.upload_csv()),
            relief="flat",
        )
        btn_1.place(x=387.0, y=210.0, width=871.0, height=133.0)
        self.page_widgets.append((btn_1, button_1))

        button_i = PhotoImage(file=relative_to_assets_page1("button_i.png"))
        btn_i = Button(
            image=button_i,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: (print("Button i clicked")),
            relief="flat",
        )
        btn_i.place(x=1080.0, y=255.0, width=50.0, height=50.0)  
        self.page_widgets.append((btn_i, button_i))



        image_6 = PhotoImage(file=relative_to_assets_page2("image_6.png"))
        img_6 = self.canvas.create_image(758.0, 376.0, image=image_6)
        self.page_widgets.append((img_6, image_6))

        button_5 = PhotoImage(file=relative_to_assets_page2("button_5.png"))
        btn_5 = Button(
            image=button_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("Button 1 clicked"),
            relief="flat",
        )
        btn_5.place(x=387.0, y=400.0, width=937.0, height=124.0)
        self.page_widgets.append((btn_5, button_5))

        button_i = PhotoImage(file=relative_to_assets_page1("button_i.png"))
        btn_i = Button(
            image=button_i,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: (print("Button i clicked")),
            relief="flat",
        )
        btn_i.place(x=1080.0, y=438.0, width=50.0, height=50.0)  
        self.page_widgets.append((btn_i, button_i))


        image_6 = PhotoImage(file=relative_to_assets_page2("image_6.png"))
        img_6 = self.canvas.create_image(758.0, 560.0, image=image_6)
        self.page_widgets.append((img_6, image_6))

        button_4 = PhotoImage(file=relative_to_assets_page2("button_4.png"))
        btn_4 = Button(
            image=button_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("Button 1 clicked"),
            relief="flat",
        )
        btn_4.place(x=387.0, y=587.0, width=906.0, height=123.0)

        self.page_widgets.append((btn_4, button_4))

        button_i = PhotoImage(file=relative_to_assets_page1("button_i.png"))
        btn_i = Button(
            image=button_i,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: (print("Button i clicked")),
            relief="flat",
        )
        btn_i.place(x=1080.0, y=625.0, width=50.0, height=50.0)  
        self.page_widgets.append((btn_i, button_i))

    def upload_csv(self):
        print("okup")
        """
        Upload the selected CSV file to the backend via API.
        """
        try:
            with open(self.file_path, 'rb') as file:
                response = requests.post(
                    'http://127.0.0.1:8000/api/datafiltering_file/',
                    files={'file': file}
                )
            if response.status_code == 200:
                print("ok")
                #pass
                #messagebox.showinfo("Success", "CSV file uploaded successfully!")
            else:
                messagebox.showerror(
                    "Error", response.json().get('error', 'File upload failed.')
                )
        except Exception as e:
            messagebox.showerror("Error", str(e))


class Data_Filtering(BasePage):

    def __init__(self, app, file_path):
        super().__init__(app)
        self.file_name = file_path.split("/")[-1]
        self.file_path=file_path
        self.column_names = self.get_column_names()
        self.Slider_update_coord = False
        self.Out_update_once = False
        self.Iso_Update_once = False
        self.Fl_update_once = False
        
        

    
    def display_graph(self,cleaned_data=None ,Raw_data=None):

        
        if (cleaned_data is None or (isinstance(cleaned_data, pd.DataFrame) and cleaned_data.empty)) and \
        (Raw_data is None or (isinstance(Raw_data, pd.DataFrame) and Raw_data.empty)):
            messagebox.showwarning("Warning", "No data to display.")
            return
        
        def plot_graph(data, title, x_offset):

    
            df = pd.DataFrame(data)
            if self.choice_col not in df.columns:
                messagebox.showerror("Error", "Column  not found in the cleaned data.")
                return

            fig, ax = plt.subplots(figsize=(6, 4))
            fig.patch.set_facecolor("#171821")
            
            ax.set_facecolor("#171821")
            ax.plot(df.index, df[self.choice_col], label= self.choice_col)  # Replace with your column
            ax.set_title ( f"{title} Output",{'color':"#FFFFFF"})
            ax.set_xlabel("Index",{'color':"#FFFFFF"})
            ax.set_ylabel(self.choice_col,{'color':"#FFFFFF"})

            ax.tick_params(axis='both', colors='#FFFFFF') 
            ax.legend(edgecolor="#FFFFFF", labelcolor='black')

            for spine in ax.spines.values():
                spine.set_edgecolor("#FFFFFF")
            
        
            # Create a FigureCanvasTkAgg widget
            canvas_widget = FigureCanvasTkAgg(fig, master=self.app.window)
            canvas_tk_widget = canvas_widget.get_tk_widget()

            # Place the graph on the canvas at x=100, y=100
            canvas_tk_widget.place(x=100+x_offset, y=330)

            # Draw the canvas
            canvas_widget.draw()

            # Keep track of the widget for cleanup (if needed)
            self.page_widgets.append((canvas_tk_widget, None))

         
        plot_graph(cleaned_data, "Cleaned Data", x_offset=650)
        plot_graph(Raw_data, "Raw Data", x_offset=50)

    def get_column_names(self):

        try:
            # Read the CSV file to get column names
            df = pd.read_csv(self.file_path, nrows=0)  # Only read the header
            column_names = df.columns.tolist()  # Convert to a Python list
            return column_names
        except Exception as e:
            # Handle any errors (e.g., file not found or invalid format)
            messagebox.showerror("Error", f"Failed to retrieve column names: {e}")
            return []
        

    def display(self):
        self.clear_canvas()
        self.create_common_elements()

        

        image_5 = PhotoImage(file=relative_to_assets_page3("image_3.png"))   #Slidebar 
        img_5 = self.canvas.create_image(35, 380, image=image_5)
        self.page_widgets.append((img_5, image_5))

        DF_Header = PhotoImage(file=relative_to_assets_page3("DF_Header.png"))
        DF_Header_img = self.canvas.create_image(705.0, 34.0, image=DF_Header)
        self.page_widgets.append((DF_Header_img,DF_Header))

        image_5 = PhotoImage(file=relative_to_assets_page2("image_5.png"))
        img_5 = self.canvas.create_image(743.0, 120.0, image=image_5)
        self.page_widgets.append((img_5, image_5))

        button_home = PhotoImage(file=relative_to_assets_page3("Home_Icon.png"))   #Home_icon 
        btn_home = Button(
            image=button_home,
            borderwidth=0,
            highlightthickness=0,
            command=(lambda: self.app.show_page(FirstPage)),
            relief="flat",
        )
        btn_home.place(x=15.0, y=80.0, width=40.0, height=40.0)  
        self.page_widgets.append((btn_home, button_home))

        button_help = PhotoImage(file=relative_to_assets_page3("Help_Icon.png"))   #Home_icon 
        btn_help = Button(
            image=button_help,
            borderwidth=0,
            highlightthickness=0,
            command=(lambda: self.app.show_page(Help_Page)),
            relief="flat",
        )
        btn_help.place(x=15.0, y=140.0, width=40.0, height=40.0)  
        self.page_widgets.append((btn_help, button_help))

        

         # File name display
        text_3 = self.canvas.create_text(
            666.0,
            103.0,
            anchor="nw",
            text=self.file_name,
            fill="#FFFFFF",
            font=("Inter SemiBold", 20 * -1),
        )
        self.page_widgets.append((text_3, None))

        self.app.create_button_with_hover(
            relative_to_assets_page2("button_2.png"),
            relative_to_assets_page2("button_hover_1.png"),
            (908.0, 101.0, 30.0, 37.0),
            (lambda: self.app.show_page(FirstPage)),
        
        )

       

        image_6 = PhotoImage(file=relative_to_assets_page2("image_6.png"))
        img_6 = self.canvas.create_image(758.0, 180.0, image=image_6)
        self.page_widgets.append((img_6, image_6))

        

        self.image_8 = PhotoImage(file=relative_to_assets_page3("image_9.png"))
        self.img_8 = self.canvas.create_image(758.0, 260.0, image=self.image_8)
        self.page_widgets.append((self.img_8, self.image_8))

        
        FlOption =["Outlier Detection", "Interpolation" , "smoothing"]
        
        self.Flm_combobox,self.Fl_Method = self.app.create_combobox(FlOption, 747, 247,self.combobox_callback_Fl)

    def combobox_callback_Fl(self, choice_Fl):

       if not self.Fl_update_once:

            self.choice_Fl = choice_Fl

            
            
            if choice_Fl == "Outlier Detection":
                self.canvas.move(self.img_8,-168.0,10) #758 -168
                self.Flm_combobox.place (x=580,y=255)
                self.Outlier_detection()
            self.Fl_update_once = True

              

    def Outlier_detection(self):

        if not self.Out_update_once:
        
       

            self.image_9 = PhotoImage(file=relative_to_assets_page3("image_8.png"))
            self.img_9 = self.canvas.create_image(900.0, 275.0, image= self.image_9)
            self.page_widgets.append((self.img_9, self.image_9))

            OD_Option =["Isolation Forest", "IQR"]
            self.Out_update_once = True
        self.OD_Combobox,self.OD_Method = self.app.create_combobox(OD_Option, 880, 255,self.combobox_callback_Od)


    def combobox_callback_Od(self, choice_Od):
        #print(choice_2)
         self.choice_Od = choice_Od
            
         if choice_Od == "Isolation Forest" :

            if not self.Iso_Update_once :

                self.canvas.move(self.img_8,-110.0,0.00)
                self.Flm_combobox.place (x=470,y=255)
                self.canvas.move(self.img_9,-110.0,0)
                self.OD_Combobox.place (x=780,y=255)


        
                self.image_10 = PhotoImage(file=relative_to_assets_page3("image_10.png"))
                self.img_10 = self.canvas.create_image(1110.0, 275.0, image=self.image_10)
                self.page_widgets.append((self.img_10, self.image_10))

                self.Iso_Update_once = True

                self.app.Create_Slider(0.00,0.50,1010,265,self.on_slider_movement,1095,290)
            

    def Slider_Update(self):
         

        if not self.Slider_update_coord :
            self.canvas.move(self.img_8,-210.0,0.00)
            self.Flm_combobox.place (x=260,y=255)

            self.canvas.move(self.img_9,-210.0,0)
            self.OD_Combobox.place (x=570,y=255)

            self.canvas.move(self.img_10,-220.0,0.00)
            self.app.slider.place (x=795,y=265)
            self.app.slider_label.place(x=875, y=290)

            self.Col_img = PhotoImage(file=relative_to_assets_page3("Col_name.png"))
            self.column_img = self.canvas.create_image(1200.0, 275.0, image=self.Col_img)
            self.page_widgets.append((self.column_img, self.Col_img))

            self.Slider_update_coord = True   #only_once apply

            

        self.OD_Combobox,self.OD_Method = self.app.create_combobox(self.column_names, 1180, 255,self.combobox_callback_col)

    def combobox_callback_col(self, choice_col):
        #print(choice_2)
         self.choice_col = choice_col   
            
         if self.choice_col != " ":
             
           self.check_and_submit()
            
        
    def on_slider_movement(self, value):

       
        self.app.slider_label.configure(text=f"{float(value):.2f}")

        # Reset the debounce timer
        if self.app.update_timer:
            self.app.update_timer.cancel()

        # Set a new timer to trigger after movement stops
        self.app.update_timer = Timer(0.5, self.Slider_Update)
        self.app.update_timer.start()

    # def send_slider_data(self, value):
    #     #"""Handle slider value change and update label."""
    #    return float(value)
    
    def check_and_submit(self):
        
       
        filter_method = self.choice_Fl
        outlier_method = self.choice_Od
        slider_value = self.app.slider.get() 
        column_name= self.choice_col

        print(f"Filter Method: {filter_method}")
        print(f"Outlier Method: {outlier_method}")
        print(f"Slider Value: {slider_value}")
        print(f"column_name: {column_name}")

    # Check if all conditions are met
        if filter_method and outlier_method and slider_value > 0 and column_name:

             self.app.create_button_with_hover(
            relative_to_assets_page3("Submit.png"),
            relative_to_assets_page3("Submit_Hover.png"),
            (710, 330, 55, 70),
            lambda:  self.submit_parameters(filter_method,outlier_method,slider_value,column_name )
            )
           

  
    def submit_parameters(self,filter_method,outlier_method,slider_value,column_name):
        """
        Submit selected parameters to the backend API.
        """  
        #print("oksu")
 
        FIlter_method = filter_method
        outlier_method= outlier_method
        column_name = column_name
        contamination = slider_value if FIlter_method == "Outlier Detection" else None

        print(column_name)
        data = pd.read_csv(self.file_path)
        # Raw_data = data[[column_name]].copy()
        # #Raw_data["index"] = Raw_data.index
        # Raw_data = Raw_data[column_name]
        # print(Raw_data)

        # Payload for API
        payload = {
            "Filter_method":  FIlter_method,
            "Outlier_method": outlier_method,
            "contamination" : contamination,
            "column_name": column_name,
            
             # File path from earlier
        }
        # if contamination is not None:
        #     payload["contamination"] = contamination

        try:
            response = requests.post(
                'http://127.0.0.1:8000/api/datafiltering_params/',
                json=payload,
            )
            if response.status_code == 200:
                cleaned_data = response.json().get('cleaned_data',[])
                #print (cleaned_data)
                #Raw_data = response.json().get('Raw_data', [])
                #self.display_graph(Raw_data)
                self.display_graph(cleaned_data,data)
                print("ok")
            else:
                messagebox.showerror(
                    "Error", response.json().get('error', 'Parameter submission failed.')
                )
        except Exception as e:
            messagebox.showerror("Error", str(e))



         
    def clear_canvas(self):
        """Clear all widgets and canvas elements from the page."""
        for widget, ref in self.page_widgets:
            if isinstance(widget, int):  # Canvas item
                self.canvas.delete(widget)
            else:  # Tkinter widget
                widget.destroy()
        self.page_widgets.clear()

class Help_Page(BasePage):

    def display (self):
        self.clear_canvas()
        self.create_common_elements()
        #self.Slidebar()

        image_4 = PhotoImage(file=relative_to_assets_page1("image_4.png"))
        img_4 = self.canvas.create_image(165, 384, image=image_4)
        self.page_widgets.append((img_4, image_4))

         #dashboard utton
        self.app.create_button_with_hover(
            relative_to_assets_page1("Dashboard.png"),
            relative_to_assets_page1("Dashboard_Hover.png"),
            (90.0, 65.0, 137.0, 45.0),
            (lambda: self.app.show_page(FirstPage))
           ,
        )

        image_da = PhotoImage(file=relative_to_assets_page1("Help_button_b.png"))
        img_da = self.canvas.create_image(164.0, 155, image=image_da)
        self.page_widgets.append((img_da, image_da))

        Help_text = self.canvas.create_text(
            780.0, 325.0, anchor="center", text="STUCK ON WHAT TO DO ? ", fill="#FFFFFF", font=("Inter Medium", 26 * -1)
        )
        self.page_widgets.append((Help_text, None))

        Help_text1 = self.canvas.create_text(
            780.0, 365.0, anchor="center", text= "THIS PAGE IS HERE TO HELP YOU  GET UNSTUCK IN NO TIME ", fill="#FFFFFF", font=("Inter Medium", 20 * -1)
        )
        self.page_widgets.append((Help_text1, None))

class ZipfilePage(BasePage):
    def __init__(self, app, file_path):
        super().__init__(app)
        
        self.file_name = file_path.split("/")[-1]
        self.file_path = file_path

    def display(self):
        self.clear_canvas()
        self.create_common_elements()
        self.Slidebar()

        image_3 = PhotoImage(file=relative_to_assets_page1("image_3.png"))
        img_3 = self.canvas.create_image(814.0, 34.0, image=image_3)
        self.page_widgets.append((img_3, image_3))

        # Add Second Page Specific Elements
        image_5 = PhotoImage(file=relative_to_assets_page2("image_5.png"))
        img_5 = self.canvas.create_image(773.0, 120.0, image=image_5)
        self.page_widgets.append((img_5, image_5))

        text_3 = self.canvas.create_text(
            696.0,
            103.0,
            anchor="nw",
            text=self.file_name,
            fill="#FFFFFF",
            font=("Inter SemiBold", 20 * -1),
        )
        self.page_widgets.append((text_3, None))

        self.app.create_button_with_hover(
            relative_to_assets_page2("button_2.png"),
            relative_to_assets_page2("button_hover_1.png"),
            (938.0, 101.0, 30.0, 37.0),
            lambda: self.app.show_page(FirstPage),
        )
        image_6 = PhotoImage(file=relative_to_assets_page2("image_6.png"))
        img_6 = self.canvas.create_image(758.0, 190.0, image=image_6)
        self.page_widgets.append((img_6, image_6))


        # Buttons
        button_1 = PhotoImage(file=relative_to_assets_page2("Button_im.png"))
        btn_1 = Button(
            image=button_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: (self.app.show_page(Image_Processing,self.file_path)),
            relief="flat",
        )
        btn_1.place(x=380.0, y=230.0, width=937.0, height=124.0)
        self.page_widgets.append((btn_1, button_1))

        button_i = PhotoImage(file=relative_to_assets_page1("button_i.png"))
        btn_i = Button(
            image=button_i,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: (print("Button i clicked")),
            relief="flat",
        )
        btn_i.place(x=1080.0, y=263.0, width=50.0, height=50.0)  
        self.page_widgets.append((btn_i, button_i))


class Image_Processing (BasePage):

    def __init__(self, app, file_path):
        super().__init__(app)
        self.file_name = file_path.split("/")[-1]
        self.file_path=file_path
    
    def display(self):
        self.clear_canvas()
        self.create_common_elements()

        

        image_5 = PhotoImage(file=relative_to_assets_page3("image_3.png"))   #Slidebar 
        img_5 = self.canvas.create_image(35, 380, image=image_5)
        self.page_widgets.append((img_5, image_5))

        DF_Header = PhotoImage(file=relative_to_assets_page3("Img_Header.png"))
        DF_Header_img = self.canvas.create_image(705.0, 34.0, image=DF_Header)
        self.page_widgets.append((DF_Header_img,DF_Header))

        image_5 = PhotoImage(file=relative_to_assets_page2("image_5.png"))
        img_5 = self.canvas.create_image(743.0, 120.0, image=image_5)
        self.page_widgets.append((img_5, image_5))

         # File name display
        text_3 = self.canvas.create_text(
            666.0,
            103.0,
            anchor="nw",
            text=self.file_name,
            fill="#FFFFFF",
            font=("Inter SemiBold", 20 * -1),
        )
        self.page_widgets.append((text_3, None))

        self.app.create_button_with_hover(
            relative_to_assets_page2("button_2.png"),
            relative_to_assets_page2("button_hover_1.png"),
            (908.0, 101.0, 30.0, 37.0),
            (lambda: self.app.show_page(FirstPage)),
        
        )

       

        image_6 = PhotoImage(file=relative_to_assets_page2("image_6.png"))
        img_6 = self.canvas.create_image(758.0, 180.0, image=image_6)
        self.page_widgets.append((img_6, image_6))

        button_home = PhotoImage(file=relative_to_assets_page3("Home_Icon.png"))   #Home_icon 
        btn_home = Button(
            image=button_home,
            borderwidth=0,
            highlightthickness=0,
            command=(lambda: self.app.show_page(FirstPage)),
            relief="flat",
        )
        btn_home.place(x=15.0, y=80.0, width=40.0, height=40.0)  
        self.page_widgets.append((btn_home, button_home))

        button_help = PhotoImage(file=relative_to_assets_page3("Help_Icon.png"))   #Home_icon 
        btn_help = Button(
            image=button_help,
            borderwidth=0,
            highlightthickness=0,
            command=(lambda: self.app.show_page(Help_Page)),
            relief="flat",
        )
        btn_help.place(x=15.0, y=140.0, width=40.0, height=40.0)  
        self.page_widgets.append((btn_help, button_help))

class App:
    def __init__(self, window):
        self.window = window
        self.window.geometry("1366x768")
        self.window.configure(bg="#171821")
        self.window.resizable(True, True)

        self.last_update_time = time.time()
        self.update_timer = None

        # Initialize canvas
        self.canvas = Canvas(
            self.window,
            bg="#171821",
            height=768,
            width=1366,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.place(x=0, y=0)

        self.current_page = None
        self.page_widgets = []

        # Start with the first page
        self.show_page(FirstPage)

    def show_page(self, page_class, *args):
        self.clear_page_widgets()
        
        if self.current_page:
            self.current_page.clear_canvas()
        self.current_page = page_class(self, *args)
        self.current_page.display()

    def create_button_with_hover(self, image, hover_image, position, command):
        """Create a button with hover effects."""
        default_image = PhotoImage(file=image)
        hover_image_file = PhotoImage(file=hover_image)

        button = Button(
            self.window,
            image=default_image,
            borderwidth=0,
            highlightthickness=0,
            command=command,
            relief="flat",
        )
        button.place(x=position[0], y=position[1], width=position[2], height=position[3])

        def on_hover(e):
            button.config(image=hover_image_file)

        def on_leave(e):
            button.config(image=default_image)

        button.bind("<Enter>", on_hover)
        button.bind("<Leave>", on_leave)

        button.image = (default_image, hover_image_file)

        # Track the button for this page
        self.page_widgets.append(button)

    def clear_page_widgets(self):
        """Destroy all widgets tracked for the current page."""
        for widget in self.page_widgets:
            widget.destroy()
        self.page_widgets.clear()

    def create_combobox(self, options, x, y,cmd):
        
        selected_value = customtkinter.StringVar(value=" ")  # Set default value
        combobox = customtkinter.CTkComboBox(
            master=self.window,
            fg_color="#343743",
            text_color="#FFFFFF",
            dropdown_hover_color="#D9D9D9",
            values=options,
            command=cmd,
            variable=selected_value,
        )
        combobox.place(x=x, y=y)
        self.page_widgets.append((combobox))
        return combobox, selected_value
    
    def Create_Slider(self,from_value,to_value,x,y,cmd,Lx,Ly):
        self.slider = customtkinter.CTkSlider(
            master=self.window,
            from_=from_value,
            to=to_value,
            command=cmd,
            orientation="horizontal",
            number_of_steps=20,
            width=200,
            height=25,
            fg_color=None,
            bg_color="#343743",
            progress_color="#FFFFFF",
            button_color="White",
            button_hover_color="orange",
            state="normal",
            hover=False,

    )
        self.slider.place(x=x, y=y)  # Adjust position as needed
        self.page_widgets.append((self.slider, None))

    
        self.slider_label = customtkinter.CTkLabel(
            master=self.window,
            text=f"{self.slider.get():.2f}",
            font=("Helvetica", 14),text_color="#FFFFFF",fg_color="#343743",bg_color="transparent"
        )
        self.slider_label.place(x=Lx, y=Ly)  # Position below the slider
        self.page_widgets.append((self.slider_label, None))

        # Set slider starting point
        self.slider.set(0.00)

    def button_dashboard_clicked(self):
        """Handle the dashboard button click."""
        print("Dashboard button clicked")

    def upload_file(self):
        """Handle file upload."""
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("Zip Files", "*.zip"),("All Files", "*.*")]
        )
        if file_path.endswith(".csv"):
            self.show_page(SecondPage, file_path)

        elif file_path.endswith(".zip"):
            self.show_page(ZipfilePage, file_path)
        else:
            messagebox.showerror("Error", "Please upload a valid .csv file.")


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
