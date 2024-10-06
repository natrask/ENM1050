import numpy as np
import tkinter as tk
import random

class Circle:
    def __init__(self, xc, yc, radius, fillcolor="blue"):
        self.xc = xc
        self.yc = yc
        self.radius = radius
        self.fillcolor = fillcolor

    def draw(self, canvas):
        x0 = self.xc - self.radius
        y0 = self.yc - self.radius
        x1 = self.xc + self.radius
        y1 = self.yc + self.radius
        canvas.create_oval(x0, y0, x1, y1, fill=self.fillcolor)

class Square:
    def __init__(self, xc, yc, side_length, fillcolor="blue"):
        self.xc = xc
        self.yc = yc
        self.side_length = side_length
        self.fillcolor = fillcolor

    def draw(self, canvas):
        x0 = self.xc - self.side_length
        y0 = self.yc - self.side_length
        x1 = self.xc + self.side_length
        y1 = self.yc + self.side_length
        canvas.create_rectangle(x0, y0, x1, y1, fill=self.fillcolor)

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

        # Initialize variables to store click coordinates
        self.first_click = None
        self.second_click = None

        # Bind the mouse click event to the canvas
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)
        self.canvas.bind("<Control-Button-1>", self.on_canvas_right_click)
        self.canvas.bind("<Shift-Button-1>", self.on_canvas_shift_click)

    def on_canvas_click(self, event):
        # Print the coordinates of the click
        print(f"Clicked at: ({event.x}, {event.y})")
        
        def random_color():
            #return a random color in hexidecimal format
            r = lambda: random.randint(0, 255)
            return f'#{r():02x}{r():02x}{r():02x}'
    
        
        # Create a circle at the click location
        circle = Circle(event.x, event.y, 50, random_color())
        circle.draw(self.canvas)

    def on_canvas_right_click(self, event):
        # Print the coordinates of the click
        print(f"Right clicked at: ({event.x}, {event.y})")
        
        def random_color():
            #return a random color in hexidecimal format
            r = lambda: random.randint(0, 255)
            return f'#{r():02x}{r():02x}{r():02x}'
        
        # Create a square at the click location
        square = Square(event.x, event.y, 50, random_color())
        square.draw(self.canvas)

    def on_canvas_shift_click(self, event):
        if self.first_click is None:
            # Store the coordinates of the first click
            self.first_click = (event.x, event.y)
            print(f"First click at: ({event.x}, {event.y})")
        else:
            # Store the coordinates of the second click
            self.second_click = (event.x, event.y)
            print(f"Second click at: ({event.x}, {event.y})")
            
            # Draw a line between the first and second click
            self.canvas.create_line(self.first_click[0], self.first_click[1], 
                                    self.second_click[0], self.second_click[1], 
                                    fill="black", width=4)
            
            # Reset the click coordinates
            self.first_click = None
            self.second_click = None

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
    