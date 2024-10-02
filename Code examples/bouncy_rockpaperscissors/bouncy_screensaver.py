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
        
        #loop over every pair of images and check for collision
        for image1 in self.bouncy_list:
            for image2 in self.bouncy_list:
                if image1 != image2 and self.is_collision(image1, image2):
                    image1.dx = -image1.dx
                    image1.dy = -image1.dy
                    image2.dx = -image2.dx
                    image2.dy = -image2.dy
        
        
        #push images forward
        for image in self.bouncy_list:
            image.move()
        self.root.after(20, self.animate)
    
    def is_collision(self, img1, img2):
        # check whether two images overlap
        pos1 = img1.get_position()
        pos2 = img2.get_position()
        size1 = img1.get_size()
        size2 = img2.get_size()

        return not (pos1[0] + size1[0] < pos2[0] or
                    pos1[0] > pos2[0] + size2[0] or
                    pos1[1] + size1[1] < pos2[1] or
                    pos1[1] > pos2[1] + size2[1])

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimationApp(root)
    root.mainloop()