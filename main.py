import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image

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

        self.setup_screens()
        self.show_screen(MAIN_SCREEN)

    def setup_screens(self):
        self.screens = {}

        self.screens[MAIN_SCREEN] = self.create_main_screen()
        self.screens[SELECT_IMAGE_SCREEN] = self.create_select_image_screen()
        self.screens[EDIT_SCREEN] = self.create_edit_screen()
        self.screens[COMPLETE_SCREEN] = self.create_complete_screen()
        self.screens[DCT_SCREEN] = self.create_dct_screen()

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
        #select_button.place(x=50, y=50, width=150, height=60)
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
        title_label.pack(pady=30)

        tools_frame = tk.Frame(frame, bg=GRAY, width=300, height=150)
        tools_frame.pack(pady=20)
        tools_frame.pack_propagate(False)

        tools_label = tk.Label(tools_frame, text="Edit tools will\nappear here",
                               bg=GRAY, fg=LIGHT_GREEN, font=self.button_font)
        tools_label.pack(expand=True)

        button_frame = ttk.Frame(frame, style='Black.TFrame')
        button_frame.pack(pady=20)

        back_button = tk.Button(button_frame, text="Back", font=self.button_font,
                                bg=LIGHT_GREEN, fg=BLACK, width=10,
                                command=lambda: self.show_screen(SELECT_IMAGE_SCREEN))
        back_button.pack(side=tk.LEFT, padx=10)

        complete_button = tk.Button(button_frame, text="Complete", font=self.button_font,
                                    bg=LIGHT_GREEN, fg=BLACK, width=10,
                                    command=lambda: self.show_screen(COMPLETE_SCREEN))
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
        #text_entry.configure("")

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
        for screen in self.screens.values():
            screen.pack_forget()

        self.current_screen = screen_name
        self.screens[screen_name].pack(fill=tk.BOTH, expand=True)

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

            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {e}")

    def proceed_to_next(self):
        if not self.selected_image:
            messagebox.showwarning("Warning", "Please select an image first")
            return

        if self.skip_edit_flag:
            self.skip_edit_flag = False
            self.show_screen(DCT_SCREEN)
        else: self.show_screen(EDIT_SCREEN)

    def apply_watermark(self):
        if not self.selected_image:
            messagebox.showwarning("Warning", "Please select an image first")
            return

        try:
            # Apply DCT watermark placeholder
            watermarked_image = self.dct_watermark(
                self.selected_image,
                self.watermark_text.get(),
                self.watermark_strength.get()
            )

            self.edited_image = watermarked_image
            self.selected_image = watermarked_image

            messagebox.showinfo("Success", "Invisible watermark applied successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Could not apply watermark: {e}")

    # DCT watermark function placeholder
    def dct_watermark(self, image, watermark_text, strength):
        return image.copy()

    def download_image(self):
        if self.edited_image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )

            if file_path:
                try:
                    self.edited_image.save(file_path)
                    messagebox.showinfo("Success", f"Image saved to {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not save image: {e}")
        else: messagebox.showwarning("Warning", "No edited image to download")

    def run(self): self.root.mainloop()


if __name__ == "__main__":
    app = DnGstalApp()
    app.run()