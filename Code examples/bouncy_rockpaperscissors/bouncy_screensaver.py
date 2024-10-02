import tkinter as tk
import numpy as np
import random
from PIL import Image
import PIL 
import PIL.Image 
import PIL.ImageTk 
from PIL import Image

class BouncyImage:
    def __init__(self, canvas, image_path):
        self.random_x = random.randint(1,canvas.winfo_reqwidth()-int(0.5*canvas.winfo_reqwidth()))
        self.random_y = random.randint(1,canvas.winfo_reqheight()-int(0.5*canvas.winfo_reqheight()))
        self.random_u = random.randint(-3,3)
        self.random_v = random.randint(-3,3)
        self.canvas = canvas
        self.image = tk.PhotoImage(file=image_path)
        self.image = self.image.subsample(3,3)
        self.image_item = canvas.create_image(self.random_x,self.random_y, anchor=tk.NW, image=self.image)

        # Replace the old image on the canvas
        # canvas.itemconfig(self.image_item, image=self.resized_img)
        self.dx = self.random_u
        self.dy = self.random_v

    def move(self):
        self.canvas.move(self.image_item, self.dx, self.dy)
        pos = self.canvas.coords(self.image_item)
        
        # Bounce off the walls
        if pos[0] + self.image.width() >= self.canvas.winfo_width() or pos[0] <= 0:
            self.dx = -self.dx
        if pos[1] + self.image.height() >= self.canvas.winfo_height() or pos[1] <= 0:
            self.dy = -self.dy

class AnimationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Animation Example")
        
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()
        
        # Create a BouncyImage instance
        self.bouncy_list = []
        self.Nbouncies = 30
        for i in range(self.Nbouncies):
            self.bouncy_list.append(BouncyImage(self.canvas, "dvd.png"))    

        
        self.animate()

    def animate(self):
        for image in self.bouncy_list:
            image.move()
        self.root.after(20, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimationApp(root)
    root.mainloop()