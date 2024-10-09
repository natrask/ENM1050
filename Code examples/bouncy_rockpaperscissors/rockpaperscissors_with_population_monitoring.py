import tkinter as tk
import numpy as np
import random
import PIL 
import PIL.Image 
import PIL.ImageTk 
from PIL import Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BouncyImage:


    def __init__(self, initx, inity, canvas, hand_type):
        # set up canvas and images
        self.canvas = canvas

        self.rockImage = tk.PhotoImage(file='rock.png').subsample(3,3)  
        self.paperImage = tk.PhotoImage(file='paper.png').subsample(3,3)
        self.scissorsImage = tk.PhotoImage(file='scissors.png').subsample(3,3)

        # Uncomment these to get different pictures
        # self.rockImage = tk.PhotoImage(file='rock2.png').subsample(12,12)  
        # self.paperImage = tk.PhotoImage(file='paper2.png').subsample(12,12)
        # self.scissorsImage = tk.PhotoImage(file='scissors2.png').subsample(12,12)
 

        # Initialize the image at a random or zero velocity
        self.init_u = 0
        self.init_v = 0
        # self.init_u = random.randint(1,3)*(-1)**random.randint(0,1)
        # self.init_v = random.randint(-3,3)*(-1)**random.randint(0,1)

        # Initialize the image based on the hand type
        self.hand_type = hand_type
        if self.hand_type == 'rock':
            self.image = self.rockImage
        elif self.hand_type == 'paper':
            self.image = self.paperImage
        elif self.hand_type == 'scissors':
            self.image = self.scissorsImage
        self.image_item = canvas.create_image(initx,inity, anchor=tk.NW, image=self.image)
        
        # Initialize the velocity of the image
        self.dx = self.init_u
        self.dy = self.init_v

        # Initialize the force to zero - this will be updated in the main loop
        self.fx = 0.0
        self.fy = 0.0


    def get_position(self):
        # Grab the current position from the canvas
        # Note that the position is the top left corner of the image
        #    and that the canvas is where the actual position is stored
        return self.canvas.coords(self.image_item)
    
    def get_size(self):
        # Return the width and height of the image
        return [self.image.width(), self.image.height()]
    
    def zero_force(self):
        # Zero out the force - this is done at the beginning of each loop before aggregating all of the neighbor forces
        self.fx = 0.0
        self.fy = 0.0

    def move(self,dt):
        # implement a single step of explicit euler to update velocity
        self.dx += dt*self.fx
        self.dy += dt*self.fy

        # implement a single step of explicit euler to update position on canvas
        self.canvas.move(self.image_item, dt*self.dx, dt*self.dy)
        pos = self.canvas.coords(self.image_item)
        
        # Bounce off the walls, bumping up by safeyfactor to avoid getting stuck on the walls
        safetyfactor = 2
        if pos[0] + self.image.width() >= self.canvas.winfo_width():
            self.dx = -0.5*self.dx
            self.canvas.move(self.image_item, -safetyfactor,0)
        if pos[0] <= 0:
            self.dx = -0.5*self.dx
            self.canvas.move(self.image_item, safetyfactor,0)
        if pos[1] + self.image.height() >= self.canvas.winfo_height():
            self.dy = -0.5*self.dy
            self.canvas.move(self.image_item, 0.0, -safetyfactor)
        if pos[1] <= 0:
            self.dy = -0.5*self.dy
            self.canvas.move(self.image_item, 0.0, safetyfactor)

        # Update the image to match the current state
        if self.hand_type == 'rock':
            self.image = self.rockImage
        if self.hand_type == 'paper':
            self.image = self.paperImage
        if self.hand_type == 'scissors':
            self.image = self.scissorsImage
        self.canvas.itemconfig(self.image_item, image=self.image)

class AnimationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock paper scissors")
        
        self.canvas = tk.Canvas(root, width=800, height=800, bg="white")
        self.canvas.pack()
        
        #timestep for simulation
        self.dt = 0.1
        self.time = 0.0
        self.Nsteps = 0

        # Create a BouncyImage instance
        canvaswidth = self.canvas.winfo_reqwidth()
        canvasheight = self.canvas.winfo_reqheight()
        self.bouncy_list = []
        self.Nbouncies = 30 # be careful not to jam too many images into the canvas
        for i in range(self.Nbouncies):
            # xpos = int(i*(canvaswidth-50)/(self.Nbouncies-1))
            xpos = random.randint(1,canvaswidth-int(0.05*canvaswidth))
            ypos = random.randint(1,canvasheight-int(0.05*canvasheight))
            # randomly choose between rock, paper, and scissors
            choice = random.randint(0,2)
            if choice == 0: #rock
                self.bouncy_list.append(BouncyImage(xpos,ypos,self.canvas, 'rock'))
            elif choice == 1: #paper
                self.bouncy_list.append(BouncyImage(xpos,ypos,self.canvas, 'paper'))
            elif choice == 2: #scissors
                self.bouncy_list.append(BouncyImage(xpos,ypos,self.canvas, 'scissors'))
            # self.bouncy_list.append(BouncyImage(xpos,ypos,self.canvas, "dvd.png"))    

        # store total population
        self.pop_list = []
        self.pop_list.append(self.calculate_population())

        # render a matplotlib plot in the corner
        self.plot_id = self.add_plot((0.75*canvaswidth), (0.75*canvasheight),self.pop_list)

        self.animate()

    def calculate_population(self):
        # calculate the population of each type of image
        rock_pop = 0
        paper_pop = 0
        scissors_pop = 0
        for image in self.bouncy_list:
            if image.hand_type == 'rock':
                rock_pop += 1
            if image.hand_type == 'paper':
                paper_pop += 1
            if image.hand_type == 'scissors':
                scissors_pop += 1
        total_pop = rock_pop + paper_pop + scissors_pop
        return np.array([rock_pop, paper_pop, scissors_pop])/total_pop
    
    def add_plot(self,xc,yc,population_list):
        # Create a Matplotlib figure
        fig = Figure(figsize=(2, 2))
        ax = fig.add_subplot(111)
        t = np.arange(0, 3, .01)
        # ax.plot(t, 2 * np.sin(2 * np.pi * t))
        ax.plot(np.array(population_list).T[0,:], 'r')
        ax.plot(np.array(population_list).T[1,:], 'g')
        ax.plot(np.array(population_list).T[2,:], 'b')
        ax.set_ylim([0,1])
        # ax.set_xlim([0,len(population_list)])
        ax.set_title('Population')
        ax.set_xlabel('Time')
        ax.set_ylabel('Population fraction')
        ax.legend(['rock', 'paper', 'scissors'])

        # Create a canvas for the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        canvas.draw()

        # Place the Matplotlib canvas on the Tkinter canvas
        plot_widget = canvas.get_tk_widget()
        plot_widget.place(x=xc,y=yc)
        return plot_widget

    def animate(self):
        
        # loop over every pair of images and check for collision
        for image1_ind in range(self.Nbouncies):
            for image2_ind in range(self.Nbouncies):
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
                    if overlapx and overlapy:
                        # if rock/scissors, make them both rock
                        if image1.hand_type == 'rock' and image2.hand_type == 'scissors':
                            image1.hand_type = 'rock'
                            image2.hand_type = 'rock'
                        # if rock/paper, make them both paper
                        elif image1.hand_type == 'rock' and image2.hand_type == 'paper':
                            image1.hand_type = 'paper'
                            image2.hand_type = 'paper'
                        # if scissors/paper, make them both scissors
                        elif image1.hand_type == 'scissors' and image1.hand_type == 'paper':
                            image1.hand_type = 'scissors'
                            image2.hand_type = 'scissors'
                        # if rock/scissors, make them both rock
                        elif image2.hand_type == 'rock' and image1.hand_type == 'scissors':
                            image1.hand_type = 'rock'
                            image2.hand_type = 'rock'
                        # if rock/paper, make them both paper
                        elif image2.hand_type == 'rock' and image1.hand_type == 'paper':
                            image1.hand_type = 'paper'
                            image2.hand_type = 'paper'
                        # if scissors/paper, make them both scissors
                        elif image2.hand_type == 'scissors' and image1.hand_type == 'paper':
                            image1.hand_type = 'scissors'
                            image2.hand_type = 'scissors'
                    

        # calculate forces on all images
        # first zero out all forces
        for image in self.bouncy_list:
            image.zero_force()
            # add friction to slow down the images
            image.fx = -1.0*image.dx
            image.fy = -1.0*image.dy

        # loop over every pair of images and accumulate the pairwise force
        for image1_ind in range(self.Nbouncies):
            for image2_ind in range(self.Nbouncies):
                if image1_ind != image2_ind:
                    image1 = self.bouncy_list[image1_ind]
                    image2 = self.bouncy_list[image2_ind]
                    
                    # figure out if interaction is predator, prey or neutral
                    interact = -0.5 #light repulsions from neutral images
                    if image1.hand_type == 'rock' and image2.hand_type == 'scissors':
                        interact = 1 #rock beats scissors
                    if image1.hand_type == 'rock' and image2.hand_type == 'paper':
                        interact = -2 #paper beats rock
                    if image1.hand_type == 'scissors' and image2.hand_type == 'rock':
                        interact = -2
                    if image1.hand_type == 'scissors' and image2.hand_type == 'paper':
                        interact = 1
                    if image1.hand_type == 'paper' and image2.hand_type == 'rock':
                        interact = 1
                    if image1.hand_type == 'paper' and image2.hand_type == 'scissors':
                        interact = -2

                    #get position and sizes of images
                    pos1 = image1.get_position()
                    pos2 = image2.get_position()
                    relative_pos_magnitude = np.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
                    # calculate the force magnitude, incorporating whether to chase predators or not
                    force = -60000.*interact/(relative_pos_magnitude**2 + 15**2) # add small number to avoid division by zero
                    # calculate the force direction
                    force_direction = np.array([pos1[0]-pos2[0], pos1[1]-pos2[1]])
                    force_direction = force_direction/(np.linalg.norm(force_direction)) # add small number to avoid division by zero
                    # apply the force to the image
                    image1.fx += force*force_direction[0]
                    image1.fy += force*force_direction[1]


        #collect data
        if self.Nsteps % 10 == 0:
            self.pop_list.append(self.calculate_population())

        #delete plot and redraw
        if self.Nsteps % 1000 == 0:
            # self.canvas.delete(self.plot_id)
            self.plot_id.destroy()
            self.plot_id = self.add_plot((0.75*self.canvas.winfo_reqwidth()), (0.75*self.canvas.winfo_reqheight()),self.pop_list)

        #push images forward
        for image in self.bouncy_list:
            self.time += self.dt
            self.Nsteps += 1
            image.move(self.dt)
        self.root.after(5, self.animate)

# The main loop that is executed to start the code.
if __name__ == "__main__":
    # main function to open window and start executing the canvas animation loop
    root = tk.Tk()
    app = AnimationApp(root)
    root.mainloop()