import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Demos to add widgets onto a canvas")
        
        # Create a canvas
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()
        
        # Precompute the width and depth to help us place widgets on the canvas
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()
        
        # Draw things on the canvas
        self.canvas.pack()
        self.circle_id = self.draw_circle(int(0.25*canvas_width), int(0.25*canvas_height))
        self.plot_id = self.add_plot((0.45*canvas_width), (0.45*canvas_height))
        self.text_id = self.add_text((0.75*canvas_width), (0.25*canvas_height), "Hello ENGR1050!")
        self.button1_id = self.add_button((0.25*canvas_width), (0.65*canvas_height), "Click Me 1", self.on_button_click_1)
        self.button2_id = self.add_button((0.25*canvas_width), (0.85*canvas_height), "Click Me 2", self.on_button_click_2)
        
   
    def draw_circle(self,xc,yc,fillcolor="blue"):

        radius = 50
        x0 = xc - radius
        y0 = yc - radius
        x1 = xc + radius
        y1 = yc + radius
        self.canvas.create_oval(x0, y0, x1, y1, fill=fillcolor)

    def add_text(self, x, y, text):
            self.canvas.create_text(x, y, text=text, fill="black", font=("Helvetica", 16))

    def add_plot(self,xc,yc):
        # Create a Matplotlib figure
        fig = Figure(figsize=(2, 2))
        ax = fig.add_subplot(111)
        t = np.arange(0, 3, .01)
        ax.plot(t, 2 * np.sin(2 * np.pi * t))

        # Create a canvas for the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()

        # Place the Matplotlib canvas on the Tkinter canvas
        canvas.get_tk_widget().place(x=xc,y=yc)
 
    def add_button(self, x, y, text, command):
        button = tk.Button(self.root, text=text, command=command)
        self.canvas.create_window(x, y, window=button)

    def on_button_click_1(self):
        print("Button 1 clicked!")

    def on_button_click_2(self):
        print("Button 2 clicked!")
        self.canvas.delete(self.circle_id)

        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()
        def random_color():
            #return a random color in hexidecimal format
            r = lambda: random.randint(0, 255)
            return f'#{r():02x}{r():02x}{r():02x}'
        
        self.circle_id = self.draw_circle(int(0.25*canvas_width), int(0.25*canvas_height),random_color())


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
    