import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw

class AnnotationTool:
    def __init__(self, root):
        self.root = root
        self.image = None
        self.photo = None
        self.annotation = None
        self.bounding_box = None

        self.open_image_button = tk.Button(root, text="Open Image", command=self.open_image)
        self.open_image_button.pack()

        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

        self.canvas.bind("<Button-1>", self.start_annotation)
        self.canvas.bind("<B1-Motion>", self.update_annotation)
        self.canvas.bind("<ButtonRelease-1>", self.end_annotation)

    def open_image(self):
        file_path = filedialog.askopenfilename()
        self.image = Image.open(file_path)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

    def start_annotation(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.annotation = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def update_annotation(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.canvas.coords(self.annotation, self.start_x, self.start_y, self.end_x, self.end_y)

    def end_annotation(self, event):
        self.bounding_box = (self.start_x, self.start_y, self.end_x, self.end_y)
        print("Bounding Box:", self.bounding_box)

root = tk.Tk()
tool = AnnotationTool(root)
root.mainloop()