import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

# Quadtree Node
class Node:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_leaf = True
        self.color = None
        self.children = []

# Compress Image using Quadtree
def compress(image, node, threshold):
    region = image[node.y:node.y+node.height, node.x:node.x+node.width]
    mean_color = np.mean(region, axis=(0, 1))
    diff = np.max(np.abs(region - mean_color))
    
    if diff < threshold or node.width <= 1 or node.height <= 1:
        node.color = mean_color
        return [node]
    
    node.is_leaf = False
    half_width = node.width // 2
    half_height = node.height // 2
    
    nodes = [
        Node(node.x, node.y, half_width, half_height),
        Node(node.x + half_width, node.y, half_width, half_height),
        Node(node.x, node.y + half_height, half_width, half_height),
        Node(node.x + half_width, node.y + half_height, half_width, half_height),
    ]
    
    compressed_nodes = []
    for n in nodes:
        compressed_nodes.extend(compress(image, n, threshold))
    
    node.children = nodes
    return compressed_nodes

# Reconstruct Image from Quadtree
def reconstruct(image, node):
    if node.is_leaf:
        image[node.y:node.y+node.height, node.x:node.x+node.width] = node.color
        return
    
    for child in node.children:
        reconstruct(image, child)

# GUI
class QuadtreeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Compression Using Quadtrees")
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        
        self.canvas = tk.Canvas(self.frame, width=600, height=400)
        self.canvas.pack()
        
        self.select_button = tk.Button(self.frame, text="Select Image", command=self.select_image)
        self.select_button.pack()
        
        self.threshold_label = tk.Label(self.frame, text="Compression Threshold")
        self.threshold_label.pack()
        
        self.threshold = tk.IntVar(value=20)
        self.threshold_slider = tk.Scale(self.frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.threshold)
        self.threshold_slider.pack()
        
        self.compress_button = tk.Button(self.frame, text="Compress Image", command=self.compress_image)
        self.compress_button.pack()
        
        self.save_button = tk.Button(self.frame, text="Save Image", command=self.save_image)
        self.save_button.pack()
        
        self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset)
        self.reset_button.pack()
        
        self.image = None
        self.compressed_image = None
        self.nodes = []
    
    def select_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path).convert('RGB')
            self.display_image(self.image)
    
    def display_image(self, img):
        img.thumbnail((600, 400))
        self.img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(300, 200, image=self.img_tk)
    
    def compress_image(self):
        if self.image:
            img_array = np.array(self.image)
            root_node = Node(0, 0, img_array.shape[1], img_array.shape[0])
            self.nodes = compress(img_array, root_node, self.threshold.get())
            self.compressed_image = np.zeros_like(img_array)
            reconstruct(self.compressed_image, root_node)
            self.display_image(Image.fromarray(np.uint8(self.compressed_image)))
    
    def reset(self):
        self.canvas.delete("all")
        self.image = None
        self.compressed_image = None
        self.nodes = []
    
    def save_image(self):
        if self.compressed_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                Image.fromarray(np.uint8(self.compressed_image)).save(file_path)

# Run the App
root = tk.Tk()
app = QuadtreeApp(root)
root.mainloop()
