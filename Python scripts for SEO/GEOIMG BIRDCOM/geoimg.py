import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image

class ImageMetadataEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Metadata Editor")
        self.image_path = ""
        self.tags = ""
        self.location = ""

        # Create UI elements
        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()

        self.image_label = tk.Label(root, text="")
        self.image_label.pack()

        self.tags_label = tk.Label(root, text="Enter Tags:")
        self.tags_label.pack()
        self.tags_entry = tk.Entry(root)
        self.tags_entry.pack()

        self.location_label = tk.Label(root, text="Enter Location:")
        self.location_label.pack()
        self.location_entry = tk.Entry(root)
        self.location_entry.pack()

        self.process_button = tk.Button(root, text="Process Image", command=self.process_image)
        self.process_button.pack()

        self.download_button = tk.Button(root, text="Download Image", command=self.download_image)
        self.download_button.pack()

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp")])
        self.image_label.config(text="Image: " + self.image_path)

    def process_image(self):
        if self.image_path:
            self.tags = self.tags_entry.get()
            self.location = self.location_entry.get()
            print("Tags:", self.tags)
            print("Location:", self.location)

            image = Image.open(self.image_path)
            # Here you can modify the image metadata using PIL's functionalities
            # For example, you can use the `PIL.ExifTags` module to modify EXIF metadata

    def download_image(self):
        if self.image_path:
            image = Image.open(self.image_path)
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
            if save_path:
                image.save(save_path)
                messagebox.showinfo("Success", "Image downloaded successfully.")
            else:
                messagebox.showwarning("Warning", "No save location selected.")

# Create the main Tkinter window
root = tk.Tk()

# Create the ImageMetadataEditor instance
editor = ImageMetadataEditor(root)

# Start the Tkinter event loop
root.mainloop()
