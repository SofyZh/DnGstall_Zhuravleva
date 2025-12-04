import tkinter as tk
import numpy as np
from tkinter import ttk, filedialog, messagebox
from scipy.fftpack import dct, idct
from PIL import Image, ImageTk
import hashlib

# Tokens
SCREEN_WIDTH = 525
SCREEN_HEIGHT = 630
WHITE = "#FFFFFF"
BLACK = "#000000"
GRAY = "#5A5A5C"
LIGHT_GREEN = "#2AFF71"
DARK_GREEN = "#2C9B71"

MAIN_SCREEN = 0
SELECT_IMAGE_SCREEN = 1
EDIT_SCREEN = 2
COMPLETE_SCREEN = 3
DCT_SCREEN = 4



class DnGstalApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("D&Gstal")
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.configure(bg=BLACK)

        self.current_screen = MAIN_SCREEN
        self.selected_image, self.original_image, self.edited_image = None, None, None
        self.watermark_text = tk.StringVar(value="RandomWatermark2006")
        self.watermark_strength = tk.DoubleVar(value=0.1)
        self.skip_edit_flag = False

        self.title_font = ("Text me one", 60)
        self.lesser_title_font = ("Text me one", 40)
        self.button_font = ("Rubik", 20)
        self.info_font = ("Rubik", 10)

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.configure(style='Black.TFrame')

        style = ttk.Style()
        style.configure('Black.TFrame', background=BLACK)
        style.configure("Black.Horizontal.TScale", background=BLACK, troughcolor=GRAY, bordercolor=BLACK)
        style.configure("Black.TEntry", background=BLACK, foreground=BLACK)

        self.screens = {MAIN_SCREEN: self.create_main_screen()}
        self.show_screen(MAIN_SCREEN)

    # Пришлось изменить setup_screens на get_screen тк загрузка всех экранов сразу приводила к очень долгой инициализации
    def get_screen(self, screen_name):
        if screen_name not in self.screens:
            if screen_name == MAIN_SCREEN: self.screens[MAIN_SCREEN] = self.create_main_screen()
            elif screen_name == SELECT_IMAGE_SCREEN: self.screens[SELECT_IMAGE_SCREEN] = self.create_select_image_screen()
            elif screen_name == EDIT_SCREEN: self.screens[EDIT_SCREEN] = self.create_edit_screen()
            elif screen_name == COMPLETE_SCREEN: self.screens[COMPLETE_SCREEN] = self.create_complete_screen()
            elif screen_name == DCT_SCREEN: self.screens[DCT_SCREEN] = self.create_dct_screen()
        return self.screens[screen_name]

    def create_main_screen(self):
        frame = ttk.Frame(self.main_frame, style='Black.TFrame')

        title_label = ttk.Label(frame, text="D&Gstal", font=self.title_font, foreground=LIGHT_GREEN, background=BLACK)
        title_label.pack(pady=50)

        edit_button = tk.Button(frame, text="Edit Mode", font=self.button_font,
                                bg=LIGHT_GREEN, fg=BLACK, width=17, height=1,
                                command=lambda: self.show_screen(SELECT_IMAGE_SCREEN))
        edit_button.pack(pady=15)

        watermark_button = tk.Button(frame, text="Invisible Watermark", font=self.button_font,
                                     bg=LIGHT_GREEN, fg=BLACK, width=17, height=1,
                                     command=self.start_watermark_flow)
        watermark_button.pack(pady=15)

        return frame

    def create_select_image_screen(self):
        frame = ttk.Frame(self.main_frame, style='Black.TFrame')

        title_label = ttk.Label(frame, text="Select Image", font=self.lesser_title_font,
                                foreground=LIGHT_GREEN, background=BLACK)
        title_label.pack(pady=30)

        file_frame = tk.Frame(frame, bg=GRAY, width=300, height=150)
        file_frame.pack(pady=20)
        file_frame.pack_propagate(False)

        file_label = tk.Label(file_frame, text="No image selected", bg=GRAY, fg=LIGHT_GREEN,
                              font=self.button_font)
        file_label.pack(expand=True)

        select_button = tk.Button(frame, text="Select Image", font=self.button_font,
                                  bg=LIGHT_GREEN, fg=BLACK,
                                  command=lambda: self.select_image(file_label))
        select_button.pack(pady=10)

        button_frame = ttk.Frame(frame, style='Black.TFrame')
        button_frame.pack(pady=20)

        back_button = tk.Button(button_frame, text="Back", font=self.button_font,
                                bg=LIGHT_GREEN, fg=BLACK, width=10, height=1,
                                command=lambda: self.show_screen(MAIN_SCREEN))
        back_button.pack(side=tk.LEFT, padx=10)

        proceed_button = tk.Button(button_frame, text="Proceed", font=self.button_font,
                                   bg=LIGHT_GREEN, fg=BLACK, width=10, height=1,
                                   command=self.proceed_to_next)
        proceed_button.pack(side=tk.LEFT, padx=10)


        return frame

    def create_edit_screen(self):
        frame = ttk.Frame(self.main_frame, style='Black.TFrame')

        title_label = ttk.Label(frame, text="Edit Mode", font=self.lesser_title_font,
                                foreground=LIGHT_GREEN, background=BLACK)
        title_label.pack(pady=10)

        content_frame = ttk.Frame(frame, style='Black.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        preview_container = ttk.Frame(content_frame, style='Black.TFrame')
        preview_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        preview_label = ttk.Label(preview_container, text="Preview",
                                  font=self.button_font,
                                  foreground=LIGHT_GREEN, background=BLACK)
        preview_label.pack(anchor=tk.W)
        preview_frame = ttk.Frame(preview_container, style='Black.TFrame', relief=tk.FLAT)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        self.preview_canvas = tk.Canvas(preview_frame, bg=BLACK, width=250, height=250)
        self.preview_canvas.pack(pady=10, padx=10)
        self.preview_label = ttk.Label(preview_frame, text="No image loaded",
                                            foreground=LIGHT_GREEN, background=BLACK)
        self.preview_label.pack()

        self.update_image_preview()

        controls_frame = ttk.Frame(content_frame, style='Black.TFrame')
        controls_frame.pack(side=tk.RIGHT, fill=tk.Y)

        filters_container = ttk.Frame(controls_frame, style='Black.TFrame')
        filters_container.pack(fill=tk.X, pady=(0, 10))
        filters_label = ttk.Label(filters_container, text="Filters",
                                  font=self.button_font,
                                  foreground=LIGHT_GREEN, background=BLACK)
        filters_label.pack(anchor=tk.W)
        filters_frame = ttk.Frame(filters_container, style='Black.TFrame', relief=tk.FLAT)
        filters_frame.pack(fill=tk.X, pady=(5, 0))

        brightness_frame = ttk.Frame(filters_frame, style='Black.TFrame')
        brightness_frame.pack(fill=tk.X, pady=5)

        ttk.Label(brightness_frame, text="Brightness:",
                  foreground=LIGHT_GREEN, background=BLACK).pack(side=tk.LEFT)

        self.brightness_value = ttk.Label(brightness_frame, text="0",
                                          foreground=LIGHT_GREEN, background=BLACK)
        self.brightness_value.pack(side=tk.RIGHT)

        self.brightness_slider = ttk.Scale(brightness_frame, from_=-100, to=100,
                                           style="Black.Horizontal.TScale",
                                           command=lambda v: self.update_brightness(float(v)))
        self.brightness_slider.set(0)
        self.brightness_slider.pack(fill=tk.X, padx=5)

        # Contrast
        contrast_frame = ttk.Frame(filters_frame, style='Black.TFrame')
        contrast_frame.pack(fill=tk.X, pady=5)

        ttk.Label(contrast_frame, text="Contrast:",
                  foreground=LIGHT_GREEN, background=BLACK).pack(side=tk.LEFT)

        self.contrast_value = ttk.Label(contrast_frame, text="0",
                                        foreground=LIGHT_GREEN, background=BLACK)
        self.contrast_value.pack(side=tk.RIGHT)
        self.contrast_slider = ttk.Scale(contrast_frame, from_=-100, to=100,
                                         style="Black.Horizontal.TScale",
                                         command=lambda v: self.update_contrast(float(v)))
        self.contrast_slider.set(0)
        self.contrast_slider.pack(fill=tk.X, padx=5)

        # Saturation
        saturation_frame = ttk.Frame(filters_frame, style='Black.TFrame')
        saturation_frame.pack(fill=tk.X, pady=5)
        ttk.Label(saturation_frame, text="Saturation:",
                  foreground=LIGHT_GREEN, background=BLACK).pack(side=tk.LEFT)

        self.saturation_value = ttk.Label(saturation_frame, text="0",
                                          foreground=LIGHT_GREEN, background=BLACK)
        self.saturation_value.pack(side=tk.RIGHT)
        self.saturation_slider = ttk.Scale(saturation_frame, from_=-100, to=100,
                                           style="Black.Horizontal.TScale",
                                           command=lambda v: self.update_saturation(float(v)))
        self.saturation_slider.set(0)
        self.saturation_slider.pack(fill=tk.X, padx=5)

        # Crop tool
        crop_container = ttk.Frame(controls_frame, style='Black.TFrame')
        crop_container.pack(fill=tk.X, pady=(10, 10))
        crop_label = ttk.Label(crop_container, text="Crop Tool",
                               font=self.button_font,
                               foreground=LIGHT_GREEN, background=BLACK)
        crop_label.pack(anchor=tk.W)
        crop_frame = ttk.Frame(crop_container, style='Black.TFrame', relief=tk.FLAT)
        crop_frame.pack(fill=tk.X, pady=(5, 0))

        dim_frame = ttk.Frame(crop_frame, style='Black.TFrame')
        dim_frame.pack(fill=tk.X, pady=5)

        ttk.Label(dim_frame, text="Width:",
                  foreground=LIGHT_GREEN, background=BLACK).pack(side=tk.LEFT, padx=(0, 5))
        self.crop_width_var = tk.StringVar(value="200")
        crop_width_entry = ttk.Entry(dim_frame, textvariable=self.crop_width_var,
                                     width=8, style="Black.TEntry")
        crop_width_entry.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Label(dim_frame, text="Height:",
                  foreground=LIGHT_GREEN, background=BLACK).pack(side=tk.LEFT, padx=(0, 5))
        self.crop_height_var = tk.StringVar(value="200")
        crop_height_entry = ttk.Entry(dim_frame, textvariable=self.crop_height_var,
                                      width=8, style="Black.TEntry")
        crop_height_entry.pack(side=tk.LEFT)

        pos_frame = ttk.Frame(crop_frame, style='Black.TFrame')
        pos_frame.pack(fill=tk.X, pady=5)
        ttk.Label(pos_frame, text="X:",
                  foreground=LIGHT_GREEN, background=BLACK).pack(side=tk.LEFT, padx=(0, 5))
        self.crop_x_var = tk.StringVar(value="0")
        crop_x_entry = ttk.Entry(pos_frame, textvariable=self.crop_x_var,
                                 width=8, style="Black.TEntry")
        crop_x_entry.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Label(pos_frame, text="Y:",
                  foreground=LIGHT_GREEN, background=BLACK).pack(side=tk.LEFT, padx=(0, 5))
        self.crop_y_var = tk.StringVar(value="0")
        crop_y_entry = ttk.Entry(pos_frame, textvariable=self.crop_y_var,
                                 width=8, style="Black.TEntry")
        crop_y_entry.pack(side=tk.LEFT)

        crop_button = tk.Button(crop_frame, text="Apply Crop", font=self.info_font,
                                bg=LIGHT_GREEN, fg=BLACK,
                                command=self.apply_crop)
        crop_button.pack(pady=10)

        reset_frame = ttk.Frame(controls_frame, style='Black.TFrame')
        reset_frame.pack(fill=tk.X, pady=10)

        reset_button = tk.Button(reset_frame, text="Reset All Filters", font=self.info_font,
                                 bg=LIGHT_GREEN, fg=BLACK,
                                 command=self.reset_filters)
        reset_button.pack()

        button_frame = ttk.Frame(frame, style='Black.TFrame')
        button_frame.pack(pady=10)

        back_button = tk.Button(button_frame, text="Back", font=self.button_font,
                                bg=LIGHT_GREEN, fg=BLACK, width=10,
                                command=lambda: self.show_screen(SELECT_IMAGE_SCREEN))
        back_button.pack(side=tk.LEFT, padx=10)

        complete_button = tk.Button(button_frame, text="Complete", font=self.button_font,
                                    bg=LIGHT_GREEN, fg=BLACK, width=10,
                                    command=self.finish_editing)
        complete_button.pack(side=tk.LEFT, padx=10)

        return frame

    def create_complete_screen(self):
        frame = ttk.Frame(self.main_frame, style='Black.TFrame')

        title_label = ttk.Label(frame, text="Edit Complete", font=self.lesser_title_font,
                                foreground=LIGHT_GREEN, background=BLACK)
        title_label.pack(pady=30)

        preview_frame = tk.Frame(frame, bg=GRAY, width=300, height=150)
        preview_frame.pack(pady=20)
        preview_frame.pack_propagate(False)

        preview_label = tk.Label(preview_frame, text="Edited Image Preview",
                                 bg=GRAY, fg=LIGHT_GREEN, font=self.button_font)
        preview_label.pack(expand=True)

        button_frame = ttk.Frame(frame, style='Black.TFrame')
        button_frame.pack(pady=20)

        back_button = tk.Button(button_frame, text="Back", font=self.button_font,
                                bg=LIGHT_GREEN, fg=BLACK, width=10,
                                command=lambda: self.show_screen(MAIN_SCREEN))
        back_button.pack(side=tk.LEFT, padx=10)

        download_button = tk.Button(button_frame, text="Download", font=self.button_font,
                                    bg=LIGHT_GREEN, fg=BLACK, width=10,
                                    command=self.download_image)
        download_button.pack(side=tk.LEFT, padx=10)

        return frame

    def create_dct_screen(self):
        frame = ttk.Frame(self.main_frame, style='Black.TFrame')

        title_label = ttk.Label(frame, text="DCT Config", font=self.lesser_title_font,
                                foreground=LIGHT_GREEN, background=BLACK)
        title_label.pack(pady=20)

        text_frame = ttk.Frame(frame, style='Black.TFrame')
        text_frame.pack(pady=10, fill=tk.X, padx=20)

        text_label = ttk.Label(text_frame, text="Invisible Watermark:", foreground=LIGHT_GREEN, background=BLACK)
        text_label.pack(side=tk.LEFT)

        text_entry = ttk.Entry(text_frame, textvariable=self.watermark_text, font=self.info_font, style="Black.TEntry")
        text_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))

        strength_frame = ttk.Frame(frame, style='Black.TFrame')
        strength_frame.pack(pady=10, fill=tk.X, padx=20)

        strength_label = ttk.Label(strength_frame, text="Strength:", foreground=LIGHT_GREEN, background=BLACK)
        strength_label.pack(side=tk.LEFT)

        value_label = ttk.Label(strength_frame, text="0.10", foreground=LIGHT_GREEN, background=BLACK)
        value_label.pack(side=tk.RIGHT)

        strength_slider = ttk.Scale(strength_frame, from_=0.01, to=1.0, style="Black.Horizontal.TScale",
                                    orient=tk.HORIZONTAL, variable=self.watermark_strength,
                                    command=lambda v: value_label.config(text=f"{float(v):.2f}"))
        strength_slider.pack(fill=tk.X, padx=(10, 10))

        apply_button = tk.Button(frame, text="Apply Watermark", font=self.button_font,
                                 bg=LIGHT_GREEN, fg=BLACK, width=20,
                                 command=self.apply_watermark)
        apply_button.pack(pady=20)

        info_label = ttk.Label(frame, text="Add invisible watermark to your image",
                               foreground=LIGHT_GREEN, background=BLACK, font=self.info_font)
        info_label.pack(pady=10)

        button_frame = ttk.Frame(frame, style='Black.TFrame')
        button_frame.pack(pady=20)

        back_button = tk.Button(button_frame, text="Back", font=self.button_font,
                                bg=LIGHT_GREEN, fg=BLACK, width=10,
                                command=lambda: self.show_screen(MAIN_SCREEN))
        back_button.pack(side=tk.LEFT, padx=10)

        complete_button = tk.Button(button_frame, text="Complete", font=self.button_font,
                                    bg=LIGHT_GREEN, fg=BLACK, width=10,
                                    command=lambda: self.show_screen(COMPLETE_SCREEN))
        complete_button.pack(side=tk.LEFT, padx=10)

        return frame

    def show_screen(self, screen_name):
        for screen in self.screens.values():  screen.pack_forget()
        self.current_screen = screen_name
        screen = self.get_screen(screen_name)
        screen.pack(fill=tk.BOTH, expand=True)

    def start_watermark_flow(self):
        self.skip_edit_flag = True
        self.show_screen(SELECT_IMAGE_SCREEN)

    def select_image(self, file_label):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])

        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.selected_image = self.original_image.copy()
                file_label.config(text=file_path.split('/')[-1])

            except Exception as e: messagebox.showerror("Error", f"Could not load image: {e}")

    def proceed_to_next(self):
        if not self.selected_image:
            messagebox.showwarning("Warning", "Please select an image first")
            return

        if self.skip_edit_flag:
            self.skip_edit_flag = False
            self.show_screen(DCT_SCREEN)
        else: self.show_screen(EDIT_SCREEN)

    def apply_watermark(self):
        try:
            if self.original_image is None: self.original_image = self.selected_image.copy()

            watermarked_image = self.dct_watermark(
                self.selected_image,
                self.watermark_text.get(),
                self.watermark_strength.get()
            )

            self.edited_image, self.selected_image = watermarked_image, watermarked_image
            messagebox.showinfo("Success", "Invisible watermark applied successfully!")

        except Exception as e: messagebox.showerror("Error", f"Could not apply watermark: {e}")


    def dct_watermark(self, image, watermark_text, strength):
        try:
            if image.mode == 'RGBA': image = image.convert('RGB')

            img_array = np.array(image)
            # applying dct to colour channels
            watermarked_array = np.zeros_like(img_array, dtype=np.float32)
            for channel in range(3):
                watermarked_array[:, :, channel] = self.apply_dct_single_channel(
                    img_array[:, :, channel], watermark_text, strength, channel
                )

            watermarked_array = np.clip(watermarked_array, 0, 255).astype(np.uint8)
            return Image.fromarray(watermarked_array)

        except Exception as e: raise Exception(f"Watermarking error: {e}")

    def apply_dct_single_channel(self, channel, watermark_text, strength, channel_index):
        h, w = channel.shape
        watermark_sequence = self.generate_watermark_sequence(watermark_text, h, w, channel_index)
        block_size = 8
        watermarked_channel = channel.astype(np.float32).copy()

        # applying dct by blocks
        for i in range(0, h - block_size, block_size):
            for j in range(0, w - block_size, block_size):
                block = channel[i:i + block_size, j:j + block_size].astype(np.float32)
                dct_block = dct(dct(block, axis=0, norm='ortho'), axis=1, norm='ortho')
                self.embed_watermark_in_block(dct_block, watermark_sequence, i, j, strength)
                watermarked_block = idct(idct(dct_block, axis=0, norm='ortho'), axis=1, norm='ortho')
                watermarked_channel[i:i + block_size, j:j + block_size] = watermarked_block

        return watermarked_channel

    # Creating a unique sequence from the watermark text (acts as key cuz reproducible).
    # for now only the fist ~5 letters of watermark_text are used in the actual
    # sequence. to be improved
    def generate_watermark_sequence(self, watermark_text, height, width, channel_index):
        seed_text = f"{watermark_text}_channel_{channel_index}"
        seed = int(hashlib.md5(seed_text.encode()).hexdigest()[:8], 16)
        np.random.seed(seed)
        return np.random.randn(height, width)

    def embed_watermark_in_block(self, dct_block, watermark_sequence, i, j, strength):
        block_size = dct_block.shape[0]

        # standard mid-frequency coeffs that the program is gonna target and modify.
        # low frequencies dont work cuz they would be too visible to a human eye, high frequencies are too
        # susceptible to changes (they will disappear after basic editing of the image)
        embedding_positions = [(1, 2), (2, 1), (2, 2), (2, 3), (3, 2)]

        for pos_x, pos_y in embedding_positions:
            if pos_x < block_size and pos_y < block_size:
                wm_i = min(i + pos_x, watermark_sequence.shape[0] - 1)
                wm_j = min(j + pos_y, watermark_sequence.shape[1] - 1)
                dct_block[pos_x, pos_y] += strength * watermark_sequence[wm_i, wm_j] * abs(dct_block[pos_x, pos_y])


    def extract_bit_from_block(self, dct_block, original_dct_block, ref_sequence, i, j, strength):
        block_size = dct_block.shape[0]
        embedding_positions = [(1, 2), (2, 1), (2, 2), (2, 3), (3, 2)]

        correlation, count = 0, 0

        for pos_x, pos_y in embedding_positions:
            if pos_x < block_size and pos_y < block_size:
                diff = dct_block[pos_x, pos_y] - original_dct_block[pos_x, pos_y]

                wm_i = min(i + pos_x, ref_sequence.shape[0] - 1)
                wm_j = min(j + pos_y, ref_sequence.shape[1] - 1)

                correlation += diff * ref_sequence[wm_i, wm_j]
                count += 1

        return 1 if correlation > 0 else 0


    def update_image_preview(self):
        if self.selected_image:
            try:
                preview_size = (250, 250)
                preview_img = self.selected_image.copy()
                preview_img.thumbnail(preview_size, Image.Resampling.LANCZOS)

                photo = ImageTk.PhotoImage(preview_img)

                self.preview_canvas.delete("all")
                self.preview_canvas.create_image(125, 125, image=photo, anchor=tk.CENTER)
                self.preview_canvas.image = photo  # Keep reference

                self.preview_label.config(text=f"Size: {self.selected_image.size}")

            except Exception as e:
                print(f"Preview error: {e}")
                self.preview_label.config(text="Error loading preview")
        else:
            self.preview_canvas.delete("all")
            self.preview_label.config(text="No image loaded")

    def update_brightness(self, value):
        try:
            self.brightness_value.config(text=f"{int(value)}")

            if self.original_image:
                # convert to HSV for brightness adjustment
                img_array = np.array(self.original_image.convert('RGB')).astype(np.float32)

                factor = 1.0 + (value / 100.0)
                img_array = np.clip(img_array * factor, 0, 255)

                self.selected_image = Image.fromarray(img_array.astype(np.uint8))
                self.update_image_preview()

        except Exception as e: print(f"Brightness error: {e}")

    def update_contrast(self, value):
        try:
            self.contrast_value.config(text=f"{int(value)}")

            if self.original_image:
                img_array = np.array(self.original_image.convert('RGB')).astype(np.float32)

                factor = 1.0 + (value / 100.0)
                mean = img_array.mean()
                img_array = mean + factor * (img_array - mean)
                img_array = np.clip(img_array, 0, 255)

                self.selected_image = Image.fromarray(img_array.astype(np.uint8))
                self.update_image_preview()

        except Exception as e: print(f"Contrast error: {e}")

    def update_saturation(self, value):
        try:
            self.saturation_value.config(text=f"{int(value)}")

            if self.original_image:
                img = self.original_image.convert('RGB')
                hsv_img = img.convert('HSV')
                hsv_array = np.array(hsv_img).astype(np.float32)

                factor = 1.0 + (value / 100.0)
                hsv_array[:, :, 1] = np.clip(hsv_array[:, :, 1] * factor, 0, 255)

                hsv_array = hsv_array.astype(np.uint8)
                self.selected_image = Image.fromarray(hsv_array, mode='HSV').convert('RGB')
                self.update_image_preview()

        except Exception as e: print(f"Saturation error: {e}")

    def apply_crop(self):
        try:
            width = int(self.crop_width_var.get())
            height = int(self.crop_height_var.get())
            x = int(self.crop_x_var.get())
            y = int(self.crop_y_var.get())

            if (width <= 0 or height <= 0) or (x < 0 or y < 0):
                messagebox.showwarning("Warning", "Cannot be negative.")
                return

            img_width, img_height = self.selected_image.size
            if x + width > img_width: width = img_width - x
            if y + height > img_height: height = img_height - y

            cropped_image = self.selected_image.crop((x, y, x + width, y + height))
            self.selected_image = cropped_image
            self.update_image_preview()

        except ValueError:
            messagebox.showerror("Error", "Invalid crop values. Please enter numbers.")
        except Exception as e: messagebox.showerror("Error", f"Crop failed: {e}")

    def reset_filters(self):
        if self.original_image:
            self.selected_image = self.original_image.copy()

            self.brightness_slider.set(0)
            self.contrast_slider.set(0)
            self.saturation_slider.set(0)

            self.brightness_value.config(text="0")
            self.contrast_value.config(text="0")
            self.saturation_value.config(text="0")

            self.crop_width_var.set("200")
            self.crop_height_var.set("200")
            self.crop_x_var.set("0")
            self.crop_y_var.set("0")

            self.update_image_preview()
        else: messagebox.showwarning("Warning", "No original image to reset to")

    def finish_editing(self):
        self.edited_image = self.selected_image.copy()
        self.show_screen(COMPLETE_SCREEN)


    def download_image(self):
        file_path = filedialog.asksaveasfilename(
             defaultextension=".png",
             filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )

        if file_path:
            try: self.edited_image.save(file_path)
            except Exception as e: messagebox.showerror("Error", f"Could not save image: {e}")

    def run(self): self.root.mainloop()


if __name__ == "__main__":
    app = DnGstalApp()
    app.run()