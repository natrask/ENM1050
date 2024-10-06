import tkinter as tk
import numpy as np
import random
import PIL 
import PIL.Image 
import PIL.ImageTk 
from PIL import Image

class BouncyImage:
    def __init__(self, initx, inity, canvas, image_path):
        self.random_u = 0*random.randint(1,3)*(-1)**random.randint(0,1)
        self.random_v = 0*random.randint(-3,3)*(-1)**random.randint(0,1)
        self.canvas = canvas
        self.image = tk.PhotoImage(file=image_path)
        self.image = self.image.subsample(9,9)
        self.image_item = canvas.create_image(initx,inity, anchor=tk.NW, image=self.image)

        # Initialize the velocity of the image
        self.dx = self.random_u
        self.dy = self.random_v
        # Initialize the force
        self.fx = 0.0
        self.fy = 0.0

    def get_position(self):
        # Assuming image_item has a method called get_position()
        return self.canvas.coords(self.image_item)
    
    def get_size(self):
        return [self.image.width(), self.image.height()]
    def zero_force(self):
        self.fx = 0.0
        self.fy = 0.0

    def move(self,dt):
        # implement a single step of explicit euler to update velocity
        self.dx += dt*self.fx
        self.dy += dt*self.fy
        #implement a single step of explicit euler to update position on canvas
        self.canvas.move(self.image_item, dt*self.dx, dt*self.dy)
        pos = self.canvas.coords(self.image_item)
        
        # Bounce off the walls
        if pos[0] + self.image.width() >= self.canvas.winfo_width() or pos[0] <= 0:
            self.dx = -self.dx
        if pos[1] + self.image.height() >= self.canvas.winfo_height() or pos[1] <= 0:
            self.dy = -self.dy

class AnimationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock paper scissors")
        
        self.canvas = tk.Canvas(root, width=800, height=400, bg="white")
        self.canvas.pack()
        
        #timestep for simulation
        self.dt = 0.1

        # Create a BouncyImage instance
        self.bouncy_list = []
        self.Nbouncies = 20 # be careful not to jam too many images into the canvas
        for i in range(self.Nbouncies):
            canvaswidth = self.canvas.winfo_reqwidth()
            canvasheight = self.canvas.winfo_reqheight()
            xpos = int(i*(canvaswidth-50)/(self.Nbouncies-1))
            ypos = random.randint(1,canvasheight-int(0.5*canvasheight))
            self.bouncy_list.append(BouncyImage(xpos,ypos,self.canvas, "dvd.png"))    

        
        self.animate()

    def animate(self):
        
        # loop over every pair of images and check for collision
        for image1_ind in range(self.Nbouncies):
            for image2_ind in range(image1_ind):
                if image1_ind != image2_ind:
                    image1 = self.bouncy_list[image1_ind]
                    image2 = self.bouncy_list[image2_ind]
                    #get position and sizes of images
                    pos1 = image1.get_position()
                    pos2 = image2.get_position()
                    size1 = image1.get_size()
                    size2 = image2.get_size()

                    # check overlap conditions
                    overlapx = pos1[0] + size1[0] >= pos2[0] and pos1[0] <= pos2[0] + size2[0]
                    overlapy = pos1[1] + size1[1] >= pos2[1] and pos1[1] <= pos2[1] + size2[1]

                    # if overlap is detected, do something
                    # if overlapx and overlapy:
                    #    #do something

        # calculate forces on all images
        # first zero out all forces
        for image in self.bouncy_list:
            image.zero_force()
            # add a tiny bit of friction to slow down the images
            image.fx = -0.1*image.dx
            image.fy = -0.1*image.dy

        # loop over every pair of images and accumulate the pairwise force
        for image1_ind in range(self.Nbouncies):
            for image2_ind in range(image1_ind):
                if image1_ind != image2_ind:
                    image1 = self.bouncy_list[image1_ind]
                    image2 = self.bouncy_list[image2_ind]
                    
                    #get position and sizes of images
                    pos1 = image1.get_position()
                    pos2 = image2.get_position()
                    relative_pos_magnitude = np.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
                    # generate envelope to make interaction local
                    length_interact = 100
                    W = 1.0#np.exp(-relative_pos_magnitude**2/length_interact**2)
                    force = -3000.*W/(relative_pos_magnitude**2 + 5**2) # add small number to avoid division by zero
                    #if relative_pos_magnitude < 100:
                     #   force += 100000.*W/(relative_pos_magnitude**4 + 1e-1)
                    # calculate the force direction
                    force_direction = np.array([pos1[0]-pos2[0], pos1[1]-pos2[1]])
                    force_direction = force_direction/np.linalg.norm(force_direction)
                    # apply the force to the images. note that forces are equal and opposite
                    image1.fx += force*force_direction[0]
                    image1.fy += force*force_direction[1]
                    image2.fx -= force*force_direction[0]
                    image2.fy -= force*force_direction[1]

        print(self.bouncy_list[0].fx, self.bouncy_list[0].fy)

        #push images forward
        for image in self.bouncy_list:
            image.move(self.dt)
        self.root.after(20, self.animate)

if __name__ == "__main__":
    # main function to open window and start executing the canvas animation loop
    root = tk.Tk()
    app = AnimationApp(root)
    root.mainloop()