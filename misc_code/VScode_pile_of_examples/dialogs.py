import tkinter as tk
from tkinter import ttk

class UserInputDialog(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("User Input Dialog")
        self.geometry("400x300")
        self.configure(bg="#f0f0f0")

        # Style configuration
        style = ttk.Style(self)
        style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0")
        style.configure("TButton", font=("Helvetica", 12))
        style.configure("TEntry", font=("Helvetica", 12))
        style.configure("TScale", background="#f0f0f0")

        # Textbox
        self.label_textbox = ttk.Label(self, text="Enter some text:")
        self.label_textbox.pack(pady=10)
        self.textbox = ttk.Entry(self, width=30)
        self.textbox.pack(pady=10)

        # Slider
        self.label_slider = ttk.Label(self, text="Select a value:")
        self.label_slider.pack(pady=10)
        self.slider = ttk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=200)
        self.slider.pack(pady=10)

        # Buttons
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=20)

        self.ok_button = ttk.Button(self.button_frame, text="OK", command=self.on_ok)
        self.ok_button.pack(side=tk.LEFT, padx=10)

        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", command=self.on_cancel)
        self.cancel_button.pack(side=tk.LEFT, padx=10)

        # Result variables
        self.text_result = None
        self.slider_result = None

    def on_ok(self):
        self.text_result = self.textbox.get()
        self.slider_result = self.slider.get()
        self.destroy()

    def on_cancel(self):
        self.text_result = None
        self.slider_result = None
        self.destroy()

def get_user_input():
    dialog = UserInputDialog()
    dialog.mainloop()
    return dialog.text_result, dialog.slider_result

# Example usage
if __name__ == "__main__":
    text, slider_value = get_user_input()
    print("Text entered:", text)
    print("Slider value:", slider_value)