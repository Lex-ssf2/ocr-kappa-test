import customtkinter as ctk
import tkinter as tk
import threading
from PIL import Image
from tkinter import filedialog
from tkinter import ttk
import os
from fastOCR import fast_ocr_simple
from safeOCR import AccurateOCRResult

class MenuApp:

  def __init__(self):
    self.root = ctk.CTk()
    ctk.set_appearance_mode("Dark") # Modos: "System", "Dark", "Light"
    ctk.set_default_color_theme("blue")
    self.root.title("Interfaz de OCR con CustomTkinter")
    self.root.geometry(f"{1100}x{580}")
    self.all_img_paths = []
    self.MAX_COLUMNS = 7
    self.accurate_ocr = None

  def destroyCurrentMenu(self):
      for widget in self.root.winfo_children():
          widget.destroy()
  
  def showMainMenu(self):
    self.destroyCurrentMenu()
    self.root.grid_columnconfigure(1, weight=1)
    self.root.grid_columnconfigure((2, 3), weight=0)
    self.root.grid_rowconfigure(1, weight=1)
    # both side bar and top bar frames are created
    self.root.sidebar_frame = ctk.CTkFrame(self.root, width=140, corner_radius=0)
    self.root.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
    self.root.sidebar_frame.grid_rowconfigure(4, weight=1)
    self.root.topbar_frame = ctk.CTkFrame(self.root, height=10, corner_radius=0)
    self.root.topbar_frame.grid(row=0, column=1, sticky="nsew")

    # Side bar elements
    self.root.name_label = ctk.CTkLabel(self.root.sidebar_frame, text="OCR App", fg_color="transparent")
    self.root.name_label.grid(row=0, column=0, padx=20, pady=20)
    self.root.clearAllImages = ctk.CTkButton(
        master=self.root.sidebar_frame,
        text="Clear all Images",
        command=self.clear_image_list,
        font=ctk.CTkFont(size=10, weight="bold"),
        corner_radius=15,
        hover_color="#1F75FE"
    )
    self.root.saveAllImagesFast = ctk.CTkButton(
        master=self.root.sidebar_frame,
        text="Save all Images (Fast Mode)",
        command=self.save_all_images_fast,
        font=ctk.CTkFont(size=10, weight="bold"),
        corner_radius=15,
        hover_color="#1F75FE"
    )
    self.root.saveAllImagesAccurate = ctk.CTkButton(
        master=self.root.sidebar_frame,
        text="Save all Images (Accurate Mode)",
        command=self.save_all_images_accurate,
        font=ctk.CTkFont(size=10, weight="bold"),
        corner_radius=15,
        hover_color="#1F75FE"
    )
    self.root.clearAllImages.grid(row=1, column=0, padx=20, pady=10)
    self.root.saveAllImagesFast.grid(row=2, column=0, padx=20, pady=10)
    self.root.saveAllImagesAccurate.grid(row=3, column=0, padx=20, pady=10)
    # Top bar elements
    self.root.addOneImageButton = ctk.CTkButton(
            master=self.root.topbar_frame,
            text="Select One Image File",
            command=self.select_one_file,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=15,
            hover_color="#1F75FE"
        )
    self.root.addOneImageButton.grid(row=0, column=0, padx=20, pady=10)
    self.root.addFolderButton = ctk.CTkButton(
            master=self.root.topbar_frame,
            text="Select Image Folder",
            command=self.select_folder,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=15,
            hover_color="#1F75FE"
        )
    self.root.addFolderButton.grid(row=0, column=1, padx=20, pady=10)
    # Main view frame with an scrollbar
    self.root.main_view_frame = ctk.CTkScrollableFrame(
        self.root, 
        label_text="Images Selected",
    )
    self.root.main_view_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew") 
    self.root.main_view_frame.grid_columnconfigure(self.MAX_COLUMNS, weight=1)

  def showSelectModeMenu(self):
    self.destroyCurrentMenu()

  def select_one_file(self):
    file_format = [
        ("Images", "*.png *.jpg *.jpeg *.tif *.tiff"),
        ("PNG Images", "*.png"),
        ("JPEG Images", "*.jpg *.jpeg")
    ]
    ruta_archivo = filedialog.askopenfilename(
            title="Select an image file for OCR",
            initialdir=os.getcwd(),
            filetypes=file_format
        )
    if ruta_archivo:
        self.all_img_paths.append(ruta_archivo)
        self.update_listbox()

  def clear_image_list(self):
    self.all_img_paths = []
    self.update_listbox()

  def select_folder(self):
    folder_path = filedialog.askdirectory(
        title="Select a folder containing images",
        initialdir=os.getcwd()
    )
    if folder_path:
      self.all_img_paths += [
          os.path.join(folder_path, f)
          for f in os.listdir(folder_path)
          if f.lower().endswith((".png", ".jpg", ".jpeg", ".tif", ".tiff"))
      ]
      self.update_listbox()

  def remove_image(self, index):
    if 0 <= index < len(self.all_img_paths):
        del self.all_img_paths[index]
        self.update_listbox()

  def save_all_images_fast(self):
    if not self.all_img_paths:
        return
    processing_window = ctk.CTkFrame(self.root)
    processing_window.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    processing_label = ctk.CTkLabel(
            master=processing_window,
            text=f"Processing 0/{len(self.all_img_paths)} images in Fast Mode...",
            font=ctk.CTkFont(size=12, weight="bold")
    )
    processing_label.pack(pady=20)

    # Worker runs in background thread; GUI updates are scheduled with .after
    def worker():
        total = len(self.all_img_paths)
        for i, img_path in enumerate(self.all_img_paths, start=1):
            try:
                fast_ocr_simple(img_path)
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
            self.root.after(0, lambda i=i, total=total: processing_label.configure(text=f"Processing {i}/{total} images in Fast Mode..."))
        def finish():
            processing_window.destroy()
            self.set_ui_enabled(True)
        self.root.after(0, finish)

    self.set_ui_enabled(False)
    t = threading.Thread(target=worker, daemon=True)
    t.start()
  
  def save_all_images_accurate(self):
    if not self.all_img_paths:
        return
    self.set_ui_enabled(False)
    self.root.update()
    self.root.update_idletasks()
    if self.accurate_ocr is None:
        self.accurate_ocr = AccurateOCRResult()
        print("Accurate OCR model initialized for batch processing.")
    processing_window = ctk.CTkFrame(self.root)
    processing_window.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    processing_label = ctk.CTkLabel(
            master=processing_window,
            text=f"Processing 0/{len(self.all_img_paths)} images in Accuracy Mode...",
            font=ctk.CTkFont(size=12, weight="bold")
    )
    processing_label.pack(pady=20)

    # Doesnt uses multithreading due to paddle ocr issues with it because it is already multithreaded internally
    for i, img_path in enumerate(self.all_img_paths, start=1):
        try:
            self.accurate_ocr.accurate_ocr_simple(img_path)
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
        processing_label.configure(text=f"Processing {i}/{len(self.all_img_paths)} images in Accuracy Mode...")
        self.root.update_idletasks()
    processing_window.destroy()
    self.set_ui_enabled(True)
  
  def set_ui_enabled(self,enabled: bool):
    state = "normal" if enabled else "disabled"
    if enabled == False:
      self.overlay_frame = ctk.CTkFrame(self.root, fg_color="transparent", corner_radius=0)
      self.overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
      self.overlay_frame.lift() 
      self.root.update()
    else:
      if hasattr(self, 'overlay_frame'):
          self.overlay_frame.destroy()
                
  def create_options_menu(self, path):
    optionsFrame = ctk.CTkFrame(self.root)
    optionsFrame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    def close_options():
        optionsFrame.destroy()
        self.set_ui_enabled(True)

    def accuracy_mode():
        if self.accurate_ocr is None:
            self.accurate_ocr = AccurateOCRResult()
        self.accurate_ocr.accurate_ocr_simple(path)
        self.set_ui_enabled(False)
        close_options()

    def fast_mode():
        fast_ocr_simple(path)
        self.set_ui_enabled(False)
        close_options()

    fast_button = ctk.CTkButton(
        master=optionsFrame,
        text="Save this Image (Fast Mode)",
        command=fast_mode
    )
    fast_button.pack(side=tk.LEFT, padx=5, pady=5)

    accuracy_button = ctk.CTkButton(
        master=optionsFrame,
        text="Save this Image (Accuracy Mode)",
        command=accuracy_mode
    )
    accuracy_button.pack(side=tk.LEFT, padx=5, pady=5)


  def update_listbox(self):
    for widget in self.root.main_view_frame.winfo_children():
            widget.destroy()
    MAX_WIDTH = 100
    MAX_HEIGHT = 100
    self.MAX_COLUMNS = self.root.main_view_frame.winfo_width() // (MAX_WIDTH * 2)
    for index, img_path in enumerate(self.all_img_paths):
        try:
            img_pil = Image.open(img_path)
            img_pil_resized = img_pil.resize((MAX_WIDTH, MAX_HEIGHT))

            img_tk = ctk.CTkImage(light_image=img_pil_resized, size=(MAX_WIDTH, MAX_HEIGHT))
            item_frame = ctk.CTkFrame(
                master=self.root.main_view_frame, 
                fg_color="transparent"
            )
            img_label = ctk.CTkButton(
                master=item_frame,
                image=img_tk,
                text=os.path.basename(img_path)[:15],
                compound="top",
                command=lambda path=img_path: self.create_options_menu(path),
                font=ctk.CTkFont(size=12, weight="bold"),
                bg_color="transparent",
                fg_color="transparent"
            )
            item_frame.grid(
                row=index // self.MAX_COLUMNS,
                column=index % self.MAX_COLUMNS,
                pady=10,
                padx=10,
                sticky="ew"
            )
            img_label.img_ref = img_tk
            img_label.grid(row=0, column=0, padx=0, pady=0, sticky="ew")
            delete_button = ctk.CTkButton(
                master=item_frame,
                text="X",
                command=lambda index=index: self.remove_image(index),
                width=20,
                height=20,
                fg_color="red",
                hover_color="#AA0000"
            )
            delete_button.grid(row=0, column=1, padx=2, pady=2, sticky="ne")
            
        except Exception as e:
            print(f"Couldn't read the image: {img_path}: {e}")

  def mainloop(self):
      self.root.mainloop()

  # getter for root
  def getRoot(self):
      return self.root

  def getAllImgPaths(self):
      return self.all_img_paths