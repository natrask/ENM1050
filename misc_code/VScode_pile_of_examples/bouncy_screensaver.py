import tkinter as tk
import numpy as np
import random
from PIL import Image
import PIL 
import PIL.Image 
import PIL.ImageTk 
from PIL import Image

class BouncyImage:
    def __init__(self, canvas, xpos, ypos, image_path):
        self.random_u = random.randint(-3,3)
        self.random_v = random.randint(-3,3)
        self.canvas = canvas
        self.image = tk.PhotoImage(file=image_path)
        self.image = self.image.subsample(3,3) #shrink image by 3x
        self.image_item = canvas.create_image(xpos,ypos, anchor=tk.NW, image=self.image)
        self.width = self.image.width()
        self.height = self.image.height()
        self.dx = self.random_u
        self.dy = self.random_v
        
    def getpos(self):
        return self.canvas.coords(self.image_item)

    def flip(self):
        self.dx = -self.dx
        self.dy = -self.dy  
        
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
        self.Nbouncies = 8
        for i in range(self.Nbouncies):
            xi = int((i/self.Nbouncies)*self.canvas.winfo_reqwidth())
            yi = random.randint(1,self.canvas.winfo_reqheight()-int(0.5*self.canvas.winfo_reqheight()))
            self.bouncy_list.append(BouncyImage(self.canvas, xi,yi,"dvd.png"))    

        
        self.animate()

    def animate(self):
        
        #loop over every unique pair of images and check for collisions
        for imgi1 in range(self.Nbouncies):
            image1 = self.bouncy_list[imgi1]
            for imgi2 in range(imgi1+1,self.Nbouncies):
                image2 = self.bouncy_list[imgi2]
                if self.is_collision(image1, image2):
                    image1.flip()
                    image2.flip()

        #push images forward
        for image in self.bouncy_list:
            image.move()
        self.root.after(20, self.animate)
        

    def is_collision(self, img1, img2):
        # check whether two images overlap
        pos1 = img1.getpos()
        pos2 = img2.getpos()
        size1 = [img1.width,img1.height]
        size2 = [img2.width,img2.height]

        return  not ((pos1[0] + size1[0] < pos2[0]) or
                    (pos1[0] > pos2[0] + size2[0]) or
                    (pos1[1] + size1[1] < pos2[1]) or
                    (pos1[1] > pos2[1] + size2[1]))
        
        

if __name__ == "__main__":
    import os
    print("Current working directory:", os.getcwd())
    files = os.listdir('.')
    print("Files in directory:", '.')
    for file in files:
        print(file)
    root = tk.Tk()
    app = AnimationApp(root)
    root.mainloop()