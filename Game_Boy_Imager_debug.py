import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

def bayer_dither(image):
    bayer_matrix = np.array([
        [0, 8, 2, 10],
        [12, 4, 14, 6],
        [3, 11, 1, 9],
        [15, 7, 13, 5]
    ]) / 16.0

    bayer_matrix = np.tile(bayer_matrix, (image.size[1] // 4 + 1, image.size[0] // 4 + 1))
    bayer_matrix = bayer_matrix[:image.size[1], :image.size[0]]

    image = np.array(image) / 255.0

    dithered_image = (image > bayer_matrix).astype(np.uint8) * 255

    return Image.fromarray(dithered_image)

def gameboy_camera_filter(image_path):
    print(f"Applying Gameboy Camera filter to {image_path}")
    # Load the image
    img = Image.open(image_path)

    # Convert to grayscale
    img = img.convert("L")

    # Resize the image to Gameboy Camera resolution (128x112)
    img = img.resize((128, 112), Image.LANCZOS)

    # Apply Bayer dithering
    img = bayer_dither(img)

    return img

class GameboyCameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gameboy Camera Filter")

        # Set window size for landscape orientation
        self.root.geometry("800x400")

        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.load_button = tk.Button(self.frame, text="Load Image", command=self.load_image)
        self.load_button.grid(row=0, column=0, padx=10, pady=10)

        self.convert_button = tk.Button(self.frame, text="Convert Image", command=self.convert_image)
        self.convert_button.grid(row=0, column=1, padx=10, pady=10)
        self.convert_button.config(state=tk.DISABLED)

        self.export_button = tk.Button(self.frame, text="Export Image", command=self.export_image)
        self.export_button.grid(row=0, column=2, padx=10, pady=10)
        self.export_button.config(state=tk.DISABLED)

        self.original_image_label = tk.Label(self.frame, text="Original Image:")
        self.original_image_label.grid(row=1, column=0, pady=5)

        self.original_image_display = tk.Label(self.frame)
        self.original_image_display.grid(row=2, column=0, pady=10)

        self.converted_image_label = tk.Label(self.frame, text="Converted Image:")
        self.converted_image_label.grid(row=1, column=1, pady=5)

        self.converted_image_display = tk.Label(self.frame)
        self.converted_image_display.grid(row=2, column=1, pady=10)

    def load_image(self):
        try:
            self.image_path = filedialog.askopenfilename(filetypes=[])
            if self.image_path:
                self.original_image = Image.open(self.image_path)
                self.display_original_image()
                self.convert_button.config(state=tk.NORMAL)
                print("Image loaded and displayed successfully.")
            else:
                print("No file selected.")
        except Exception as e:
            messagebox.showerror("Error", f"Unable to load image: {e}")
            print(f"Error loading image: {e}")
            self.image_path = None

    def display_original_image(self):
        if self.original_image:
            img = self.original_image
            img.thumbnail((256, 256))
            self.original_img_display = ImageTk.PhotoImage(img)
            self.original_image_display.config(image=self.original_img_display)

    def convert_image(self):
        if self.image_path:
            try:
                self.converted_image = gameboy_camera_filter(self.image_path)
                self.display_converted_image()
                self.export_button.config(state=tk.NORMAL)
                print("Image converted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Unable to convert image: {e}")
                print(f"Error converting image: {e}")

    def display_converted_image(self):
        if self.converted_image:
            img = self.converted_image
            img.thumbnail((256, 256))
            self.converted_img_display = ImageTk.PhotoImage(img)
            self.converted_image_display.config(image=self.converted_img_display)
            print("Converted image displayed successfully.")

    def export_image(self):
        if self.converted_image:
            output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")])
            if output_path:
                try:
                    self.converted_image.save(output_path)
                    messagebox.showinfo("Success", f"Image saved to {output_path}")
                    print(f"Image saved to {output_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Unable to save image: {e}")
                    print(f"Error saving image: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GameboyCameraApp(root)
    root.mainloop()