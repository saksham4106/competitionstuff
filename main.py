import tkinter as tk
from tkinter.ttk import *
from tkcalendar import DateEntry
import csv
from tkinter.constants import *



class Table:
     
    def __init__(self,root, total_rows, total_columns, lst):
         
        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                 
                self.e = Entry(root, width=15)
                self.e.config(state = "normal")
                 
                self.e.grid(row=i, column=j)
                self.e.insert(tk.END, lst[i][j])

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)




def storeData(data):
    with open('data.csv','r')as file:
        filecontent=csv.reader(file)
        n = True
        for row in filecontent:
            if(n):
                pass
            else:
                 data.append(row)
            n = False

data = []
storeData(data)
                
win = tk.Tk()
win.tk.call("source", "azure.tcl")
win.tk.call("set_theme", "dark")
style = Style()
#win.geometry("800x600+0+0")
w, h = win.winfo_screenwidth(), win.winfo_screenheight()
win.geometry("%dx%d+0+0" % (w, h))

shouldFilterDates = True
selectDateLabel = Label(win, text= "Select Date")
selectDateLabel.place(x = 10, y = 15)
cal = DateEntry(win, day=1, month=4, year=2018)
cal.place(x=110, y=10)
style.configure("Toggle.TButton", font = (None, 6))

def shouldFilterDates():
    global shouldFilterDates
    shouldFilterDates = not shouldFilterDates

enableAllDates = Checkbutton(win, text = "Toggle Date filtering", style= 'Toggle.TButton', command = shouldFilterDates)
enableAllDates.place(x = 250, y = 10)

daysVar = tk.StringVar(win)
selectDayLabel = Label(win, text= "Select Day")
selectDayLabel.place(x = 10, y = 60)
daysOption = OptionMenu(win, daysVar, *["All", "All", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"] )
daysOption.place(x = 110, y = 55)

pressureBox = Label(win , text="Pressure(at sea) Min:-:Max")
pressureBox.place(x= 10,y=100)
pressureInputMinBox = Entry(win, width = 5)
pressureInputMinBox.place(x=200,y=95)
pressureInputMaxBox = Entry(win, width = 5)
pressureInputMaxBox.place(x=260 ,y=95)


tempratureBox = Label(win , text="Temperature (Min:-:Max)")
tempratureBox.place(x=10,y=150)
tempratureInputMinBox = Entry(win, width = 5)
tempratureInputMinBox.place(x=200,y=145)
tempratureInputMaxBox = Entry(win, width = 5)
tempratureInputMaxBox.place(x=260,y=145)


humidityBox = Label(win , text="Rel Humidity (Min:-:Max)")
humidityBox.place(x=10,y=200)
humidityInputMinBox = Entry(win, width = 5)
humidityInputMinBox.place(x=200,y=195)
humidityInputMaxBox = Entry(win, width = 5)
humidityInputMaxBox.place(x=260,y=195)



visibilityBox = Label(win , text="Visibilty (Min:-:Max)")
visibilityBox.place(x=10,y=250)
visibilityInputMinBox = Entry(win, width = 5)
visibilityInputMinBox.place(x=200,y=245)
visibilityInputMaxBox = Entry(win, width = 5)
visibilityInputMaxBox.place(x=260,y=245)



windSpeedBox = Label(win , text="Wind Speed (Min:-:Max)")
windSpeedBox.place(x=10,y=300)
windSpeedInputMinBox = Entry(win, width = 5)
windSpeedInputMinBox.place(x=200,y=295)
windSpeedInputMaxBox = Entry(win, width = 5)
windSpeedInputMaxBox.place(x=260,y=295)


PMBox = Label(win , text="PM 2.5 (Min:-:Max)")
PMBox.place(x=10,y=350)
PMInputMinBox = Entry(win, width = 5)
PMInputMinBox.place(x=200,y=345)
PMInputMaxBox = Entry(win, width = 5)
PMInputMaxBox.place(x=260,y=345)





lst = []


def updateData():
    date = cal.get_date().strftime("%d/%m/%Y")
    day = daysVar.get()
    print(day)
    lst.clear()
    lst.append(("Date",'Day','Avg. Temp',"Max Temp", "Min Temp", "ATM", "rel. humidity", "Avg. visibilty", "Max wind Speed", "AQI"))
    n = 0
    for entry in data:
        filteredDate = False
        if(shouldFilterDates):
            if(date in entry[0]):
                filteredDate = True
        else:
            filteredDate = True


        if(filteredDate):
            if(day.lower() == entry[1].lower() or day == "All"):
                if(pressureInputMaxBox.get() == "" or pressureInputMinBox == ""):
                    if(n < 20):
                        lst.append(entry)
                        n += 1
                elif float(entry[5]) > float(pressureInputMinBox.get()) and float(entry[5]) < float(pressureInputMaxBox.get()):
                    if(n < 20):
                        lst.append(entry)
                        n += 1
                    
                    

                
        # n += 1
        # if n < 20: lst.append(entry)

    frame = VerticalScrolledFrame(win)
    frame.place(x = 0, y = 400)
    t = Table(frame.interior, len(lst), len(lst[0]), lst)

submitButton = Button(win, text="Get Filtered Data", command= updateData)
submitButton.place(x = 700, y = 200)

win.mainloop()