import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os

class MenuApp:
  def __init__(self):
    self.root = ctk.CTk()
    ctk.set_appearance_mode("Dark") # Modos: "System", "Dark", "Light"
    ctk.set_default_color_theme("blue")
    self.root.title("Interfaz de OCR con CustomTkinter")
    self.root.geometry("600x600")
    self.all_img_paths = []


  def destroyCurrentMenu(self):
      for widget in self.root.winfo_children():
          widget.destroy()
  
  def showMainMenu(self):
    self.destroyCurrentMenu()
    selectFile = ctk.CTkButton(
            master=self.root,
            text="Select One Image File",
            command=self.select_one_file,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=15,
            hover_color="#1F75FE"
        )
    selectFile.pack(pady=40, padx=40)
    selectFolder = ctk.CTkButton(
            master=self.root,
            text="Select Image Folder",
            command=self.select_folder,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=15,
            hover_color="#1F75FE"
        )
    selectFolder.pack(pady=40, padx=40)

  def showSelectModeMenu(self):
    self.destroyCurrentMenu()
    fastOCRButton = ctk.CTkButton(
            master=self.root,
            text="Fast OCR (Tesseract)",
            command=lambda: print("Fast OCR Selected"),
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=15,
            hover_color="#1F75FE"
        )
    fastOCRButton.pack(pady=20, padx=20)
    accurateOCRButton = ctk.CTkButton(
            master=self.root,
            text="Accurate OCR (PaddleOCR)",
            command=lambda: print("Accurate OCR Selected"),
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=15,
            hover_color="#1F75FE"
        )
    accurateOCRButton.pack(pady=20, padx=20)

  def select_one_file(self):
    file_format = [
        ("Images", "*.png *.jpg *.jpeg *.tif *.tiff"),
        ("PNG Images", "*.png"),
        ("JPEG Images", "*.jpg *.jpeg")
    ]
    ruta_archivo = filedialog.askopenfilename(
            title="Selecciona un archivo de imagen para OCR",
            initialdir=os.getcwd(),
            filetypes=file_format
        )
    if ruta_archivo:
        self.all_img_paths = [ruta_archivo]
    self.showSelectModeMenu()
        

  def select_folder(self):
    folder_path = filedialog.askdirectory(
        title="Selecciona una carpeta que contenga imágenes",
        initialdir=os.getcwd()
    )
    if folder_path:
        self.all_img_paths = [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".tif", ".tiff"))
        ]
    self.showSelectModeMenu()

  def mainloop(self):
      self.root.mainloop()

  # getter for root
  def getRoot(self):
      return self.root

  def getAllImgPaths(self):
      return self.all_img_paths