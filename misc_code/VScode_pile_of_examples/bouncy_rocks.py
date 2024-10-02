# %%
import tkinter as tk
from tkinter import simpledialog
import math

# %%
class TableInputGUI:
    def __init__(self, root, rows, cols):
        self.root = root
        # Add a label at the top
        label = tk.Label(root, text="Enter your data below:")
        label.grid(row=0, columnspan=cols)
        
        self.entries = []
        for i in range(rows):
            row_entries = []
            for j in range(cols):
                # Add a label in front of each entry
                entry_label = tk.Label(root, text=f"R{i+1}C{j+1}")
                entry_label.grid(row=i+1, column=j*2)  # Adjust column index to account for the labels
                
                entry = tk.Entry(root, width=10)
                entry.grid(row=i+1, column=j*2+1)  # Adjust column index to account for the labels
                row_entries.append(entry)
            self.entries.append(row_entries)

        submit_button = tk.Button(root, text="Submit", command=self.submit)
        submit_button.grid(row=rows+1, columnspan=cols)
        
        close_button = tk.Button(root, text="Close", command=self.close)
        close_button.grid(row=rows+2, columnspan=cols)
    def submit(self):
        data = []
        for row_entries in self.entries:
            row_data = [entry.get() for entry in row_entries]
            data.append(row_data)
        print(data)  # You can replace this with any other action you want to perform with the data

    def close(self):
        self.root.destroy()

import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk  # Import Pillow modules
import os

class TrajectoryAnimation:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()

        # Print the current directory
        print("Current Directory:", os.getcwd())

        # Initial position and velocity
        self.x = 50
        self.y = 300
        self.vx = 5  # Velocity in x direction
        self.vy = -10  # Initial velocity in y direction
        self.gravity = 0.5  # Gravity effect
        self.isJetpack = False # Jetpack effect
        self.jetPack_time = 0.0 # Jetpack time
        
        # Add text that will follow the object
        self.text = self.canvas.create_text(self.x, self.y-40, text="Bouncy Rock", font=("Arial", 16), fill='black')

        # Add text that will act like the ground
        self.ground_text = self.canvas.create_text(400, 592, text=40*str('*')+" Icy ground "+40*str('*'), font=("Arial", 16), fill='blue')

        # Load and resize the image using Pillow
        pil_image = Image.open("hw2fig0.png")  # Ensure the path is correct
        resized_image = pil_image.resize((50, 50))  # Resize the image to 20x20 pixels
        self.image = ImageTk.PhotoImage(resized_image)

        # Load and resize the image to be used during firing
        new_pil_image = Image.open("granite.png")  # E        nsure the path is correct
        new_resized_image = new_pil_image.resize((50, 50))  # Resize the image to 50x50 pixels
        self.new_image = ImageTk.PhotoImage(new_resized_image)  

        # Create a circle to represent the object
        self.object = self.canvas.create_oval(self.x-10, self.y-10, self.x+10, self.y+10, fill="blue")

        # Create an image on the canvas
        self.image_id = self.canvas.create_image(self.x, self.y, image=self.image)

        # Bind the left mouse button click event to the on_click method
        self.root.bind("<Button-1>", self.on_click)
        # Bind the key press event to the on_key_press method
        
        # Bind the key press event to the on_key_press method
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
        
        # Start the animation
        self.animate()

    def on_key_press(self, event):
        # Function to execute when a key is pressed
        print(f"Key pressed: {event.keysym}")
        # Turn on jetpack
        self.fire_jetpack()
        
    def on_key_release(self, event):
        # Function to execute when a key is released
        print(f"Key released: {event.keysym}")  
        
    def on_click(self, event):
        # Function to execute when the user clicks on the window
        print(f"Mouse clicked at ({event.x}, {event.y}) while the object is at ({self.x}, {self.y})")
        # Turn on jetpack
        self.fire_jetpack()

    def fire_jetpack(self):
        self.isJetpack = True
        self.jetPack_time = 2.0
        # Switch to the jetpack image
        self.canvas.itemconfig(self.image_id, image=self.new_image)
        # Update the text to indicate jetpack is on
        self.canvas.itemconfig(self.text, text="Jetpack Activated!")
        
    def animate(self):
        # Update position
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity  # Apply gravity to y velocity

        # if the jetpack is on, fire it and decrement
        if self.isJetpack:
            self.vy -= 1.5*self.gravity
            self.jetPack_time -= 0.1
            # if we're out of back, revert back to original state
            if self.jetPack_time <= 0.0:
                self.isJetpack = False
                # Switch to the jetpack image
                self.canvas.itemconfig(self.image_id, image=self.image)
                # Update the text to indicate jetpack is on
                self.canvas.itemconfig(self.text, text="Bouncy Rock")

        # Update the position of the object on the canvas
        self.canvas.coords(self.object, self.x-10, self.y-10, self.x+10, self.y+10)
        self.canvas.coords(self.text, self.x, self.y-40)
        self.canvas.coords(self.image_id, self.x, self.y)

        # Bounce back when the object hits the ground or walls
        if self.y > 550:  
            self.vy = -0.8 * self.vy
            self.y = 550
        if self.x > 700 or self.x < 0:  
            self.vx = -1.0 * self.vx

        if self.x < 900:  # Stop the animation if the object goes out of the canvas
            self.root.after(50, self.animate)

def main():
    root = tk.Tk()
    root.title("Trajectory Animation")
    app = TrajectoryAnimation(root)
    root.mainloop()


# %%
import os
print("Current directory:", os.getcwd())
main()

# %%
