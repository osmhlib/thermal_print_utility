import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
from escpos.printer import Usb
from usb.backend import libusb1
import json
import os

CONFIG_FILE = "printer_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"vid": "0000", "pid": "0000"}


def save_config(vid, pid):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"vid": vid, "pid": pid}, f)

def center_window(root, width=430, height=450):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

class PrintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("XPrinter Image Print")
        center_window(self.root)

        self.image_path = None
        self.img_original = None

        config = load_config()

        config_frame = tk.Frame(root)
        config_frame.pack(pady=5)

        tk.Label(config_frame, text="VID:").pack(side=tk.LEFT, padx=2)
        self.vid_entry = tk.Entry(config_frame, width=8)
        self.vid_entry.insert(0, config["vid"])
        self.vid_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(config_frame, text="PID:").pack(side=tk.LEFT, padx=2)
        self.pid_entry = tk.Entry(config_frame, width=8)
        self.pid_entry.insert(0, config["pid"])
        self.pid_entry.pack(side=tk.LEFT, padx=5)

        control_frame = tk.Frame(root)
        control_frame.pack(pady=5)

        self.choose_btn = tk.Button(control_frame, text="🖼️ Select image", command=self.select_image)
        self.choose_btn.pack(side=tk.LEFT, padx=5)

        self.print_btn = tk.Button(control_frame, text="🖨️ Print", command=self.print_image)
        self.print_btn.pack(side=tk.LEFT, padx=5)

        self.contrast_label = tk.Label(control_frame, text="Contrast")
        self.contrast_label.pack(side=tk.LEFT, padx=5)

        self.contrast_slider = tk.Scale(
            control_frame, from_=0.5, to=2.0, resolution=0.1,
            orient=tk.HORIZONTAL, command=self.update_contrast
        )
        self.contrast_slider.set(1.0)
        self.contrast_slider.pack(side=tk.LEFT, padx=5)

        copies_frame = tk.Frame(root)
        copies_frame.pack(pady=5)

        self.copies_label = tk.Label(copies_frame, text="Number of copies:")
        self.copies_label.pack(side=tk.LEFT, padx=5)

        self.copies_spinbox = tk.Spinbox(copies_frame, from_=1, to=20, width=5)
        self.copies_spinbox.pack(side=tk.LEFT, padx=5)

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

    def select_image(self):
        filetypes = (("Image files", "*.png *.bmp *.jpg *.jpeg"),)
        filepath = filedialog.askopenfilename(title="Select image", filetypes=filetypes)
        if filepath:
            self.image_path = filepath
            img = Image.open(filepath).convert("L")

            max_width = 384
            aspect_ratio = img.width / img.height
            max_height = int(max_width / aspect_ratio)
            img_resized = img.resize((max_width, max_height), Image.LANCZOS)

            self.img_original = img_resized
            self.update_contrast()

    def update_contrast(self, event=None):
        if self.img_original is not None:
            contrast_value = self.contrast_slider.get()
            enhancer = ImageEnhance.Contrast(self.img_original)
            self.img_contrast = enhancer.enhance(contrast_value)

            img_bw = self.img_contrast.convert("L")
            threshold = 180
            img_bw = img_bw.point(lambda p: p > threshold and 255)

            img_sharpened = img_bw.filter(ImageFilter.SHARPEN)

            img_thumbnail = img_sharpened.copy()
            img_thumbnail.thumbnail((384, 300))

            img_tk = ImageTk.PhotoImage(img_thumbnail)
            self.image_label.configure(image=img_tk)
            self.image_label.image = img_tk

    def print_image(self):
        if not self.img_original:
            messagebox.showwarning("Attention", "First select an image.")
            return
        try:
            vid_text = self.vid_entry.get().strip()
            pid_text = self.pid_entry.get().strip()
            vid = int(vid_text, 16)
            pid = int(pid_text, 16)

            save_config(vid_text, pid_text)

            backend = libusb1.get_backend()
            printer = Usb(vid, pid, backend=backend)

            contrast_value = self.contrast_slider.get()
            enhancer = ImageEnhance.Contrast(self.img_original)
            img_to_print = enhancer.enhance(contrast_value)
            img_bw = img_to_print.convert("1")

            copies = int(self.copies_spinbox.get())
            for _ in range(copies):
                printer.image(img_bw)
                printer.cut()

            printer.close()
            messagebox.showinfo("Success", f"Printed {copies} copies.")
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PrintApp(root)
    root.mainloop()

