import os
import threading
import json
import tempfile
import smtplib
import winreg
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from PIL import Image, ImageEnhance, ImageOps, ImageTk, ImageFilter, ImageDraw, ImageFont, ImageChops
import pytesseract
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Scale, HORIZONTAL, VERTICAL, ttk, simpledialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4, letter, landscape, portrait
from reportlab.lib.units import inch
import uuid
import qrcode
import datetime
import subprocess
from tkcalendar import Calendar
import numpy as np
import cv2
import sys
import urllib.parse
from docx import Document
from docx.shared import Inches
import time  # Added for camera scanning stability
import pypdf # For PDF encryption
import fitz # PyMuPDF for PDF to image conversion
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from scan_settings_window import ScanSettingsWindow # JAUNS IMPORTS
import random  # Pievienots random modulis

def show_loading_screen(root):
    """Parāda premium ielādes logu ar modernu dizainu"""
    loading_window = tk.Toplevel(root)
    loading_window.title("Ielādē...")
    loading_window.geometry("600x400")
    loading_window.resizable(False, False)
    loading_window.configure(bg="#222831")
    loading_window.overrideredirect(True)  # Noņemam borderus un title bar

    # Centrēšana
    loading_window.update_idletasks()
    width = loading_window.winfo_width()
    height = loading_window.winfo_height()
    x = (loading_window.winfo_screenwidth() // 2) - (width // 2)
    y = (loading_window.winfo_screenheight() // 2) - (height // 2)
    loading_window.geometry(f"+{x}+{y}")

    # Padara neaizveramu
    loading_window.grab_set()
    loading_window.protocol("WM_DELETE_WINDOW", lambda: None)  # Atspējo aizvēršanu

    # Dizaina elementi
    bg_frame = tk.Frame(loading_window, bg="#393E46")
    bg_frame.pack(fill='both', expand=True, padx=50, pady=50)

    # Logo/tituls
    logo_frame = tk.Frame(bg_frame, bg="#393E46")
    logo_frame.pack(pady=(20, 10))
    tk.Label(logo_frame,
             text="PDF Vision Pro",
             font=("Helvetica", 24, "bold"),
             fg="#00ADB5", bg="#393E46").pack()
    tk.Label(logo_frame,
             text="Profesionāls OCR un PDF apstrādes rīks",
             font=("Helvetica", 10),
             fg="#EEEEEE", bg="#393E46").pack(pady=(0, 20))

    # Progress bars
    progress_container = tk.Frame(bg_frame, bg="#393E46")
    progress_container.pack(fill='x', padx=50, pady=20)

    # Pamata progress bars
    main_progress = ttk.Progressbar(progress_container,
                                    orient="horizontal",
                                    length=400,
                                    mode="determinate")
    main_progress.pack()

    # Animēta veidņa progress bars (dekors)
    style = ttk.Style()
    style.configure("Striped.Horizontal.TProgressbar",
                    background='#00ADB5',
                    troughcolor='#393E46',
                    lightcolor='#00ADB5',
                    darkcolor='#00848B',
                    relief='flat')

    deco_progress = ttk.Progressbar(progress_container,
                                    style="Striped.Horizontal.TProgressbar",
                                    orient="horizontal",
                                    length=400,
                                    mode="determinate")
    deco_progress.pack(pady=(10, 0))

    # Statusa teksts
    status_text = tk.Label(bg_frame,
                           text="Inicializē sistēmas komponentes...",
                           font=("Helvetica", 9),
                           fg="#EEEEEE", bg="#393E46")
    status_text.pack(pady=(10, 0))

    # Progress animācija
    def update_progress():
        current = main_progress['value']
        if current < 100:
            increment = random.uniform(0.5, 3)
            main_progress['value'] = current + increment
            deco_progress['value'] = current + increment

            phases = [
                "Ielādē OCR dzinēju...",
                "Inicializē dokumenta pārvaldnieku...",
                "Konfigurē lietotāja saskarni...",
                "Gatavojas darbam...",
                "Gandrīz gatavs..."
            ]
            if current % 25 == 0 and current <= 80:
                status_text.config(text=random.choice(phases))

            loading_window.after(100, update_progress)
        else:
            # Saglabājam loading loga pozīciju
            loading_x = loading_window.winfo_x()
            loading_y = loading_window.winfo_y()

            loading_window.destroy()

            # Atver galveno logu
            root.deiconify()

            # Maksimizējam logu bez pilnekrāna (lai ir redzamas ikonas)
            root.state('zoomed')  # Maina no fullscreen uz maximizētu

            # Pārvieto uz loading loga pozīciju
            root.geometry(f"+{loading_x}+{loading_y}")

    # Sākam animāciju
    loading_window.after(2000, update_progress)  # 1 sekunde delay pirms sākas

    return loading_window


    # Centrēšana
    loading_window.update_idletasks()
    width = loading_window.winfo_width()
    height = loading_window.winfo_height()
    x = (loading_window.winfo_screenwidth() // 2) - (width // 2)
    y = (loading_window.winfo_screenheight() // 2) - (height // 2)
    loading_window.geometry(f"+{x}+{y}")

    # Padara neaizveramu
    loading_window.grab_set()
    loading_window.protocol("WM_DELETE_WINDOW", lambda: None)  # Atspējo aizvēršanu

    # Dizaina elementi
    bg_frame = tk.Frame(loading_window, bg="#393E46")
    bg_frame.pack(fill='both', expand=True, padx=50, pady=50)

    # Logo/tituls
    logo_frame = tk.Frame(bg_frame, bg="#393E46")
    logo_frame.pack(pady=(20, 10))
    tk.Label(logo_frame,
             text="PDF Vision Pro",
             font=("Helvetica", 24, "bold"),
             fg="#00ADB5", bg="#393E46").pack()
    tk.Label(logo_frame,
             text="Profesionāls OCR un PDF apstrādes rīks",
             font=("Helvetica", 10),
             fg="#EEEEEE", bg="#393E46").pack(pady=(0, 20))

    # Progress bars
    progress_container = tk.Frame(bg_frame, bg="#393E46")
    progress_container.pack(fill='x', padx=50, pady=20)

    # Pamata progress bars
    main_progress = ttk.Progressbar(progress_container,
                                    orient="horizontal",
                                    length=400,
                                    mode="determinate")
    main_progress.pack()

    # Animēta veidņa progress bars (dekors)
    style = ttk.Style()
    style.configure("Striped.Horizontal.TProgressbar",
                    background='#00ADB5',
                    troughcolor='#393E46',
                    lightcolor='#00ADB5',
                    darkcolor='#00848B',
                    relief='flat')

    deco_progress = ttk.Progressbar(progress_container,
                                    style="Striped.Horizontal.TProgressbar",
                                    orient="horizontal",
                                    length=400,
                                    mode="determinate")
    deco_progress.pack(pady=(10, 0))

    # Statusa teksts
    status_text = tk.Label(bg_frame,
                           text="Inicializē sistēmas komponentes...",
                           font=("Helvetica", 9),
                           fg="#EEEEEE", bg="#393E46")
    status_text.pack(pady=(10, 0))

    # Progress animācija
    def update_progress():
        current = main_progress['value']
        if current < 100:
            increment = random.uniform(0.5, 3)  # Nejaušs solis
            main_progress['value'] = current + increment
            deco_progress['value'] = current + increment

            # Mainam statusa tekstu
            phases = [
                "Ielādē OCR dzinēju...",
                "Inicializē dokumenta pārvaldnieku...",
                "Konfigurē lietotāja saskarni...",
                "Gatavojas darbam...",
                "Gandrīz gatavs..."
            ]
            if current % 25 == 0 and current <= 80:
                status_text.config(text=random.choice(phases))

            loading_window.after(100, update_progress)  # Atjaunina ik pēc 100ms
        else:
            loading_window.destroy()

    # Sākam animāciju
    loading_window.after(2000, update_progress)  # 1 sekunde delay pirms sākas

    return loading_window



def register_file_association():
    """Reģistrē .pdf failu asociāciju ar šo programmu"""
    try:
        app_name = "MyPDFEditor"  # Nomainiet uz jūsu programmas nosaukumu
        exe_path = sys.executable

        # Reģistrējam paplašinājumu
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, ".pdf") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, f"{app_name}.pdf")

        # Reģistrējam komandu
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{app_name}.pdf\\shell\\open\\command") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, f'"{exe_path}" "%1"')

        # Atjauninām lietotāja iestatījumus
        subprocess.run(['assoc', '.pdf={app_name}.pdf'], shell=True)
        subprocess.run(['ftype', f'{app_name}.pdf="{exe_path}" "%1"'], shell=True)

        messagebox.showinfo("Sekmēs", "PDF asociācijas veiksmīgi iestatītas")
    except Exception as e:
        messagebox.showerror("Kļūda", f"Neizdevās reģistrēt asociācijas:\n{e}")

# Pārbauda un importē OpenCV un NumPy slīpuma korekcijai
OPENCV_AVAILABLE = False
try:
    import numpy as np
    import cv2

    OPENCV_AVAILABLE = True
except ImportError:
    print(
        "OpenCV and NumPy not found. Deskew, HSV conversion, stitching, inpainting, face detection, and camera scanning functionality will be disabled.")

# Tesseract ceļš - pielāgo savam datoram
DEFAULT_TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = DEFAULT_TESSERACT_CMD

# Definējiet ceļu uz iestatījumu failu
APP_SETTINGS_FILE = "app_settings.json"  # Varat mainīt uz citu ceļu, ja nepieciešams

# Noklusējuma kameras indekss
DEFAULT_CAMERA_INDEX = 1



class SettingsWindow(Toplevel):
    """Paplašināta iestatījumu klase ar e-pasta iestatījumiem un skenēšanas iestatījumiem"""

    def __init__(self, master, app_instance):
        super().__init__(master)
        self.app = app_instance
        self.title("Vispārīgie Iestatījumi") # MAINĪTS TEKSTS
        # Pielāgo iestatījumu loga izmēru, lai tas labāk ietilptu mazākos ekrānos
        # Var izmantot arī relatīvus izmērus, piemēram, 80% no galvenā loga izmēra
        self.geometry("1000x900")  # Palielināts iestatījumu loga izmērs
        self.minsize(800, 800)  # Pievienots minimālais izmērs iestatījumu logam
        self.transient(master)
        self.grab_set()

        self.create_widgets()
        self.load_current_settings()

    def toggle_id_code_options(self):
        """Ieslēdz/izslēdz ID koda opciju rāmi atkarībā no izvēles rūtiņas stāvokļa."""
        if self.add_id_code_var.get():
            self.id_code_options_frame.grid()
        else:
            self.id_code_options_frame.grid_remove()

    def create_widgets(self):
        """Izveido iestatījumu loga elementus"""
        main_frame = ttk.Frame(self, padding=(10, 10))
        main_frame.pack(fill=BOTH, expand=True)

        # Izveido notebook ar vairākām cilnēm
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Galvenie iestatījumi
        general_frame = ttk.Frame(notebook, padding=10)
        notebook.add(general_frame, text="Vispārīgi")

        # OCR iestatījumi
        ocr_frame = ttk.Frame(notebook, padding=10)
        notebook.add(ocr_frame, text="OCR")

        # PDF iestatījumi
        pdf_frame = ttk.Frame(notebook, padding=10)
        notebook.add(pdf_frame, text="PDF")

        # E-pasta iestatījumi
        email_frame = ttk.Frame(notebook, padding=10)
        notebook.add(email_frame, text="E-pasts")

        # Aizpilda iestatījumu rāmjus
        self.create_general_settings(general_frame)
        self.create_ocr_settings(ocr_frame)
        self.create_pdf_settings(pdf_frame)
        self.create_email_settings(email_frame)
        # self.create_scan_settings(scan_frame) # IZDZĒSTS: Skenēšanas iestatījumu cilne

        # Pogu rāmis
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=X, pady=(10, 0))

        ttk.Button(button_frame, text="Saglabāt", command=self.save_settings,
                   bootstyle=PRIMARY).pack(side=RIGHT, padx=5)
        ttk.Button(button_frame, text="Atcelt", command=self.destroy,
                   bootstyle=SECONDARY).pack(side=RIGHT, padx=5)


    def create_general_settings(self, frame):
        """Izveido vispārīgos iestatījumus"""
        ttk.Label(frame, text="Programmas tēma:").grid(row=0, column=0, sticky=W, pady=2)
        self.theme_var = tk.StringVar()
        theme_combo = ttk.Combobox(frame, textvariable=self.theme_var,
                                   values=self.app.style.theme_names())
        theme_combo.grid(row=0, column=1, sticky=EW, padx=5, pady=2)
        theme_combo.bind("<<ComboboxSelected>>", self.change_app_theme)

        ttk.Label(frame, text="Noklusējuma saglabāšanas mape:").grid(row=1, column=0, sticky=W, pady=2)
        self.save_path_var = tk.StringVar()
        save_path_entry = ttk.Entry(frame, textvariable=self.save_path_var, width=40)
        save_path_entry.grid(row=1, column=1, sticky=EW, padx=5, pady=2)
        ttk.Button(frame, text="Pārlūkot...", command=self.browse_save_path).grid(row=1, column=2, padx=5)

        ttk.Label(frame, text="Programmas tēma:").grid(row=0, column=0, sticky=W, pady=2)
        self.theme_var = tk.StringVar()
        theme_combo = ttk.Combobox(frame, textvariable=self.theme_var,
                                   values=self.app.style.theme_names())
        theme_combo.grid(row=0, column=1, sticky=EW, padx=5, pady=2)
        theme_combo.bind("<<ComboboxSelected>>", self.change_app_theme)
        # Pievienojiet jaunu iestatījumu par autentifikāciju
        ttk.Label(frame, text="Iespējot autentifikāciju:").grid(row=1, column=0, sticky=W, pady=2)
        self.enable_auth_var = tk.BooleanVar(value=True)  # Noklusējuma vērtība
        ttk.Checkbutton(frame, variable=self.enable_auth_var).grid(row=1, column=1, sticky=W, padx=5)

        # Piešķir visiem elementiem vienādu svaru
        frame.columnconfigure(1, weight=1)

    def create_ocr_settings(self, frame):
        """Izveido OCR iestatījumus"""
        ttk.Label(frame, text="Tesseract ceļš:").grid(row=0, column=0, sticky=W, pady=2)
        self.tesseract_var = tk.StringVar()
        tesseract_entry = ttk.Entry(frame, textvariable=self.tesseract_var, width=40)
        tesseract_entry.grid(row=0, column=1, sticky=EW, padx=5, pady=2)
        ttk.Button(frame, text="Pārlūkot...", command=self.browse_tesseract_path).grid(row=0, column=2, padx=5)

        ttk.Label(frame, text="OCR valodas:").grid(row=1, column=0, sticky=NW, pady=5)
        lang_frame = ttk.Frame(frame)
        lang_frame.grid(row=1, column=1, columnspan=2, sticky=EW, pady=2)

        self.lang_vars = {}
        col = 0
        for lang, code in self.app.lang_options.items():
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(lang_frame, text=lang, variable=var)
            cb.grid(row=0, column=col, sticky=W, padx=5)
            self.lang_vars[lang] = var
            col += 1

        ttk.Label(frame, text="Pārējie OCR parametri:").grid(row=2, column=0, sticky=W, pady=5)

        param_frame = ttk.Frame(frame)
        param_frame.grid(row=3, column=0, columnspan=3, sticky=EW)

        ttk.Label(param_frame, text="DPI:").grid(row=0, column=0, sticky=W)
        self.dpi_var = tk.IntVar()
        ttk.Spinbox(param_frame, from_=70, to=600, increment=10, textvariable=self.dpi_var, width=5).grid(row=0,
                                                                                                          column=1,
                                                                                                          padx=5)

        ttk.Label(param_frame, text="Confidence:").grid(row=0, column=2, sticky=W)
        self.conf_var = tk.IntVar()
        ttk.Spinbox(param_frame, from_=0, to=100, increment=5, textvariable=self.conf_var, width=5).grid(row=0,
                                                                                                         column=3,
                                                                                                         padx=5)

        frame.columnconfigure(1, weight=1)

    def create_pdf_settings(self, frame):
        """Izveido PDF iestatījumus"""
        ttk.Label(frame, text="PDF izvades kvalitāte:").grid(row=0, column=0, sticky=W, pady=2)
        self.pdf_qual_var = tk.StringVar()
        pdf_qual_combo = ttk.Combobox(frame, textvariable=self.pdf_qual_var,
                                      values=["Zema (60)", "Vidēja (85)", "Augsta (95)"])
        pdf_qual_combo.grid(row=0, column=1, sticky=EW, padx=5, pady=2)

        ttk.Label(frame, text="Lapas izmērs:").grid(row=1, column=0, sticky=W, pady=2)
        self.page_size_var = tk.StringVar()
        page_size_combo = ttk.Combobox(frame, textvariable=self.page_size_var,
                                       values=self.app.orientation_options)
        page_size_combo.grid(row=1, column=1, sticky=EW, padx=5, pady=2)

        ttk.Label(frame, text="Fonta izmērs:").grid(row=2, column=0, sticky=W, pady=2)
        self.font_size_var = tk.IntVar()
        ttk.Spinbox(frame, from_=5, to=20, increment=1, textvariable=self.font_size_var, width=5).grid(row=2, column=1,
                                                                                                       sticky=W, padx=5)

        ttk.Checkbutton(frame, text="Iekļaut meklējamo tekstu PDF", variable=tk.BooleanVar(value=True)).grid(row=3,
                                                                                                             column=0,
                                                                                                             columnspan=2,
                                                                                                             sticky=W,
                                                                                                             pady=5)

        # JAUNS: QR koda/Svītrkoda iestatījumi
        ttk.Label(frame, text="Pievienot ID kodu PDF:").grid(row=4, column=0, sticky=W, pady=2)
        self.add_id_code_var = tk.BooleanVar()
        ttk.Checkbutton(frame, variable=self.add_id_code_var, command=self.toggle_id_code_options).grid(row=4, column=1,
                                                                                                        sticky=W,
                                                                                                        padx=5, pady=2)

        self.id_code_options_frame = ttk.Frame(frame)
        self.id_code_options_frame.grid(row=5, column=0, columnspan=2, sticky=EW, padx=5, pady=2)

        ttk.Label(self.id_code_options_frame, text="Koda tips:").grid(row=0, column=0, sticky=W, pady=2)
        self.id_code_type_var = tk.StringVar()
        ttk.Radiobutton(self.id_code_options_frame, text="QR kods", variable=self.id_code_type_var, value="QR").grid(
            row=0, column=1, sticky=W, padx=5)
        ttk.Radiobutton(self.id_code_options_frame, text="Svītrkods (Code 128)", variable=self.id_code_type_var,
                        value="Barcode").grid(row=0, column=2, sticky=W, padx=5)
        ttk.Radiobutton(self.id_code_options_frame, text="Svītrkods (Code 39)", variable=self.id_code_type_var,
                        value="Code39").grid(row=0, column=3, sticky=W, padx=5)
        ttk.Radiobutton(self.id_code_options_frame, text="Svītrkods (EAN-13)", variable=self.id_code_type_var,
                        value="EAN13").grid(row=0, column=4, sticky=W, padx=5)

        ttk.Label(self.id_code_options_frame, text="Koda pozīcija:").grid(row=1, column=0, sticky=W, pady=2)
        self.id_code_position_var = tk.StringVar()
        ttk.Radiobutton(self.id_code_options_frame, text="Augšā pa labi", variable=self.id_code_position_var,
                        value="top_right").grid(row=1, column=1, sticky=W, padx=5)
        ttk.Radiobutton(self.id_code_options_frame, text="Apakšā pa labi", variable=self.id_code_position_var,
                        value="bottom_right").grid(row=1, column=2, sticky=W, padx=5)
        ttk.Radiobutton(self.id_code_options_frame, text="Apakšā pa kreisi", variable=self.id_code_position_var,
                        value="bottom_left").grid(row=1, column=3, sticky=W, padx=5)
        ttk.Radiobutton(self.id_code_options_frame, text="Augšā pa kreisi", variable=self.id_code_position_var,
                        value="top_left").grid(row=1, column=4, sticky=W, padx=5)

        frame.columnconfigure(1, weight=1)
        self.toggle_id_code_options()  # Sākotnējā stāvokļa iestatīšana

    def create_email_settings(self, frame):
        """Izveido e-pasta iestatījumus"""
        ttk.Label(frame, text="SMTP serveris:").grid(row=0, column=0, sticky=W, pady=2)
        self.smtp_server_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.smtp_server_var).grid(row=0, column=1, sticky=EW, padx=5, pady=2)

        ttk.Label(frame, text="SMTP ports:").grid(row=1, column=0, sticky=W, pady=2)
        self.smtp_port_var = tk.IntVar()
        ttk.Entry(frame, textvariable=self.smtp_port_var).grid(row=1, column=1, sticky=EW, padx=5, pady=2)

        ttk.Label(frame, text="Lietotājvārds:").grid(row=2, column=0, sticky=W, pady=2)
        self.email_user_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.email_user_var).grid(row=2, column=1, sticky=EW, padx=5, pady=2)

        ttk.Label(frame, text="Parole:").grid(row=3, column=0, sticky=W, pady=2)
        self.email_pass_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.email_pass_var, show="*").grid(row=3, column=1, sticky=EW, padx=5, pady=2)

        ttk.Label(frame, text="No adreses:").grid(row=4, column=0, sticky=W, pady=2)
        self.from_email_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.from_email_var).grid(row=4, column=1, sticky=EW, padx=5, pady=2)

        ttk.Label(frame, text="Uz adresi (noklusējums):").grid(row=5, column=0, sticky=W, pady=2)
        self.to_email_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.to_email_var).grid(row=5, column=1, sticky=EW, padx=5, pady=2)

        self.use_ssl_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="Izmantot SSL", variable=self.use_ssl_var).grid(row=6, column=0,
                                                                                    columnspan=2, sticky=W,
                                                                                    pady=5)

        ttk.Label(frame, text="E-pasta tēma:").grid(row=7, column=0, sticky=W, pady=2)
        self.email_subject_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.email_subject_var).grid(row=7, column=1, sticky=EW, padx=5, pady=2)

        ttk.Label(frame, text="E-pasta teksts (Plain):").grid(row=8, column=0, sticky=NW, pady=2)
        self.email_body_plain_text = tk.Text(frame, height=5, width=40, wrap="word")
        self.email_body_plain_text.grid(row=8, column=1, sticky=EW, padx=5, pady=2)

        ttk.Label(frame, text="E-pasta teksts (HTML):").grid(row=9, column=0, sticky=NW, pady=2)
        self.email_body_html_text = tk.Text(frame, height=5, width=40, wrap="word")
        self.email_body_html_text.grid(row=9, column=1, sticky=EW, padx=5, pady=2)

        # Pārbaudes poga
        ttk.Button(frame, text="Pārbaudīt savienojumu", command=self.test_email_settings,
                   bootstyle=INFO).grid(row=10, column=0, columnspan=2, pady=10)

        frame.columnconfigure(1, weight=1)


    def test_email_settings(self):
        """Pārbauda e-pasta savienojumu ar norādītajiem iestatījumiem"""
        try:
            server = self.smtp_server_var.get()
            port = self.smtp_port_var.get()
            username = self.email_user_var.get()
            password = self.email_pass_var.get()
            use_ssl = self.use_ssl_var.get()

            if not server or not port or not username or not password:
                messagebox.showwarning("Trūkst datu", "Lūdzu, aizpildiet visus laukus!")
                return

            if use_ssl:
                smtp = smtplib.SMTP_SSL(server, port)
            else:
                smtp = smtplib.SMTP(server, port)
                smtp.starttls()

            smtp.login(username, password)
            smtp.quit()
            messagebox.showinfo("Pārbaude", "Savienojums ar SMTP serveri veiksmīgs!")
        except Exception as e:
            messagebox.showerror("Kļūda", f"Neizdevās pieslēgties SMTP serverim:\n{str(e)}")

    def browse_save_path(self):
        """Atver dialogu, lai izvēlētos saglabāšanas ceļu"""
        path = filedialog.askdirectory(title="Izvēlieties noklusējuma saglabāšanas mapi")
        if path:
            self.save_path_var.set(path)

    def browse_tesseract_path(self):
        """Atver dialogu, lai izvēlētos Tesseract ceļu"""
        path = filedialog.askopenfilename(title="Izvēlieties Tesseract.exe",
                                          filetypes=[("Executable files", "*.exe")])
        if path:
            self.tesseract_var.set(path)

    def change_app_theme(self, event=None):
        """Maina lietotnes tēmu"""
        selected_theme = self.theme_var.get()
        self.app.style.theme_use(selected_theme)
        if hasattr(self.app, 'current_image_index') and self.app.current_image_index != -1:
            self.app.on_file_select()

    def load_current_settings(self):
        """Ielādē pašreizējos iestatījumus"""
        self.theme_var.set(self.app.style.theme_use())
        self.save_path_var.set(self.app.default_save_path)
        self.tesseract_var.set(pytesseract.pytesseract.tesseract_cmd)
        self.pdf_qual_var.set(self.app.pdf_quality)
        self.page_size_var.set(self.app.orientation_var.get())
        self.font_size_var.set(self.app.fontsize_var.get())
        self.dpi_var.set(self.app.dpi_var.get())
        self.conf_var.set(self.app.confidence_var.get())

        # E-pasta iestatījumi
        self.smtp_server_var.set(self.app.settings.get("smtp_server", ""))
        self.smtp_port_var.set(self.app.settings.get("smtp_port", 465))
        self.email_user_var.set(self.app.settings.get("email_user", ""))
        self.email_pass_var.set(self.app.settings.get("email_pass", ""))
        self.from_email_var.set(self.app.settings.get("from_email", ""))
        self.to_email_var.set(self.app.settings.get("to_email", ""))
        self.use_ssl_var.set(self.app.settings.get("use_ssl", True))
        self.email_subject_var.set(self.app.settings.get("email_subject", "OCR PDF dokumenti"))
        self.email_body_plain_text.delete("1.0", tk.END)
        self.email_body_plain_text.insert(tk.END, self.app.settings.get("email_body_plain",
                                                                        "Sveiki,\n\nPielikumā atradīsiet OCR apstrādātos PDF dokumentus.\n\nAr cieņu,\nJūsu OCR PDF App"))
        self.email_body_html_text.delete("1.0", tk.END)
        self.email_body_html_text.insert(tk.END, self.app.settings.get("email_body_html",
                                                                       "<html><body><p>Sveiki,</p><p>Pielikumā atradīsiet OCR apstrādātos PDF dokumentus.</p><p>Ar cieņu,<br/>Jūsu OCR PDF App</p></body></html>"))

        # Valodu atzīmēšana
        # JAUNS: ID koda iestatījumi
        self.add_id_code_var.set(self.app.settings.get("add_id_code_to_pdf", False))
        self.id_code_type_var.set(self.app.settings.get("id_code_type", "QR"))
        self.id_code_position_var.set(self.app.settings.get("id_code_position", "bottom_right"))
        self.toggle_id_code_options() # Atjaunina redzamību

        for lang_name, var in self.lang_vars.items():
            if lang_name in self.app.lang_vars:
                var.set(self.app.lang_vars[lang_name].get())

    def save_settings(self):
        """Saglabā iestatījumus"""
        # Galvenie iestatījumi
        self.app.style.theme_use(self.theme_var.get())
        self.app.default_save_path = self.save_path_var.get()

        # OCR iestatījumi
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_var.get()
        self.app.dpi_var.set(self.dpi_var.get())
        self.app.confidence_var.set(self.conf_var.get())

        # PDF iestatījumi
        self.app.pdf_quality = self.pdf_qual_var.get()
        self.app.orientation_var.set(self.page_size_var.get())
        self.app.fontsize_var.set(self.font_size_var.get())

        # E-pasta iestatījumi
        self.app.settings["smtp_server"] = self.smtp_server_var.get()
        self.app.settings["smtp_port"] = self.smtp_port_var.get()
        self.app.settings["email_user"] = self.email_user_var.get()
        self.app.settings["email_pass"] = self.email_pass_var.get()
        self.app.settings["from_email"] = self.from_email_var.get()
        self.app.settings["to_email"] = self.to_email_var.get()
        self.app.settings["use_ssl"] = self.use_ssl_var.get()
        self.app.settings["email_subject"] = self.email_subject_var.get()
        self.app.settings["email_body_plain"] = self.email_body_plain_text.get("1.0", tk.END).strip()
        self.app.settings["email_body_html"] = self.email_body_html_text.get("1.0", tk.END).strip()

        # JAUNS: ID koda iestatījumi
        self.app.settings["add_id_code_to_pdf"] = self.add_id_code_var.get()
        self.app.settings["id_code_type"] = self.id_code_type_var.get()
        self.app.settings["id_code_position"] = self.id_code_position_var.get()

        # Valodu atzīmēšana

        for lang_name, var in self.lang_vars.items():
            if lang_name in self.app.lang_vars:
                self.app.lang_vars[lang_name].set(var.get())

        self.app.save_app_settings()
        messagebox.showinfo("Iestatījumi", "Iestatījumi veiksmīgi saglabāti!")
        self.destroy()

    def create_image_processing_widgets(self, parent):
        """Izveido attēlu apstrādes komponentus."""
        params_frame = ttk.Frame(parent)
        params_frame.grid(row=0, column=0, padx=10, pady=10)
        # DPI iestatījums
        self.dpi_var = tk.IntVar(value=300)  # Noklusējuma DPI
        ttk.Label(params_frame, text="DPI:").grid(row=0, column=0, sticky=tk.W)
        ttk.Spinbox(params_frame, from_=70, to=600, increment=10, textvariable=self.dpi_var, width=4).grid(row=0,
                                                                                                           column=1)
        # Pievienojiet citus komponentus šeit


class PDFEditor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.document = None
        self.open()

    def open(self):
        if self.document is None:
            self.document = fitz.open(self.filepath)

    def close(self):
        if self.document:
            self.document.close()
            self.document = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_page_count(self):
        return len(self.document)

    def get_page_image(self, page_num, dpi=72):
        page = self.document.load_page(page_num)
        pix = page.get_pixmap(dpi=dpi)
        return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Pievienojiet citas metodes šeit...


class FullscreenImageViewer(Toplevel):
    """Pilnekrāna attēlu skatītājs ar tālummaiņas un pārvietošanas funkcijām."""

    def __init__(self, master, image_pil):
        super().__init__(master)
        self.title("Attēla priekšskatījums")
        # Sākotnējais izmērs kā galvenajam logam, maksimizē logu
        self.geometry(f"{master.winfo_width()}x{master.winfo_height()}+0+0")
        self.state('zoomed')
        self.transient(master)
        self.grab_set()

        self.image_pil = image_pil
        self.zoom_factor = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.start_pan_x = 0
        self.start_pan_y = 0

        self.canvas = tk.Canvas(self, bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)  # Windows/Linux
        self.canvas.bind("<Button-4>", self.on_mouse_wheel)  # MacOS
        self.canvas.bind("<Button-5>", self.on_mouse_wheel)  # MacOS
        self.canvas.bind("<ButtonPress-2>", self.on_pan_start)  # Middle mouse button
        self.canvas.bind("<B2-Motion>", self.on_pan_drag)
        self.canvas.bind("<ButtonRelease-2>", self.on_pan_end)

        self.canvas.bind("<ButtonPress-1>", self.on_selection_start)
        self.canvas.bind("<B1-Motion>", self.on_selection_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_selection_end)
        self.selection_rect = None
        self.selection_start_x = None
        self.selection_start_y = None

        self.file_listbox = tk.Listbox(self)  # Inicializē file_listbox
        self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)

        # Konfigurē krāsas
        self.file_listbox.configure(
            selectbackground='#d4edda',  # Zaļa atlases krāsa
            selectforeground='white'
        )

        self.display_image()

    def display_image(self):
        """Attēlo attēlu uz kanvasa, pielāgojot tālummaiņu un pārvietošanu."""
        if not hasattr(self, 'canvas') or not self.canvas.winfo_exists():
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            return

        img_width, img_height = self.image_pil.size
        scaled_width = int(img_width * self.zoom_factor)
        scaled_height = int(img_height * self.zoom_factor)

        # Pārmēro attēlu
        display_img = self.image_pil.resize((scaled_width, scaled_height), Image.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(display_img)

        self.canvas.delete("all")

        # Aprēķina attēla pozīciju ar pārvietošanu
        x = (canvas_width - scaled_width) / 2 + self.pan_x
        y = (canvas_height - scaled_height) / 2 + self.pan_y

        self.canvas.create_image(x, y, anchor="nw", image=self.photo_image)
        self.canvas.image = self.photo_image  # Saglabā atsauci

    def on_canvas_resize(self, event):
        """Pielāgo attēla attēlošanu, ja kanvasa izmērs mainās."""
        self.display_image()

    def on_mouse_wheel(self, event):
        """Apstrādā peles rullīša notikumus tālummaiņai."""
        if event.num == 5 or event.delta == -120:  # Tuvināt
            self.zoom_factor = max(0.1, self.zoom_factor - 0.1)
        if event.num == 4 or event.delta == 120:  # Attālināt
            self.zoom_factor = min(5.0, self.zoom_factor + 0.1)
        self.display_image()

    def on_pan_start(self, event):
        """Sāk attēla pārvietošanu (pan)."""
        self.start_pan_x = event.x - self.pan_x
        self.start_pan_y = event.y - self.pan_y
        self.canvas.config(cursor="fleur")

    def on_pan_drag(self, event):
        """Pārvieto attēlu, velkot peli."""
        self.pan_x = event.x - self.start_pan_x
        self.pan_y = event.y - self.start_pan_y
        self.display_image()

    def on_pan_end(self, event):
        """Beidz attēla pārvietošanu."""
        self.canvas.config(cursor="arrow")

    def on_selection_start(self, event):
        """Sāk atlases taisnstūra zīmēšanu."""
        self.selection_start_x = self.canvas.canvasx(event.x)
        self.selection_start_y = self.canvas.canvasy(event.y)
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)
        self.selection_rect = self.canvas.create_rectangle(self.selection_start_x, self.selection_start_y,
                                                           self.selection_start_x, self.selection_start_y,
                                                           outline="blue", width=2, dash=(5, 2))

    def on_selection_drag(self, event):
        """Atjaunina atlases taisnstūra izmērus, velkot peli."""
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.selection_rect, self.selection_start_x, self.selection_start_y, cur_x, cur_y)

    def on_selection_end(self, event):
        """Beidz atlases taisnstūra zīmēšanu (šeit varētu apstrādāt iezīmēto apgabalu)."""
        pass


class OCRPDFApp(ttk.Window):
    """Galvenā lietojumprogrammas klase OCR un PDF ģenerēšanai."""

    def __init__(self):
        super().__init__(themename="darkly")

        # Paslēpt galveno logu
        self.withdraw()

        # Ielādes logs
        loading_window = show_loading_screen(self)
        self.wait_window(loading_window)



        # Rādīt galveno logu
        self.deiconify()

        # MAINĪTS: Izdarīta maksimizācija (nevis pilnekrāns)
        self.state('zoomed')  # Logs aizņems visu darba laukumu, bet saglabā kontroljoslas

        self.title("Advanced OCR uz PDF")
        # Sākotnējais izmērs un minimālais izmērs, kas labāk piemērots mazākiem ekrāniem
        self.geometry("1024x768")  # Samazināts noklusējuma izmērs
        self.minsize(800, 500)  # Samazināts minimālais izmērs
        self.settings = {}  # Inicializējiet settings kā tukšu vārdnīcu
        self.scan_settings = {}  # JAUNS: Inicializējiet skenēšanas iestatījumus
        self.settings_file = os.path.join(os.path.expanduser("~"), "ocr_pdf_settings.json")
        self.scan_settings_file = os.path.join(os.path.expanduser("~"),
                                               "ocr_scan_settings.json")  # JAUNS: Skenēšanas iestatījumu fails
        self.pdf_archive_file = os.path.join(os.path.expanduser("~"), "ocr_pdf_archive.json")
        self.scan_folder_path = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "ScannedDocuments")) # JAUNS: Skenēšanas mapes ceļš
        self.auto_scan_enabled = tk.BooleanVar(value=False) # JAUNS: Automātiskās skenēšanas ieslēgšana/izslēgšana
        self.observer = None # JAUNS: Watchdog observers


        self.title("Advanced OCR uz PDF")
        # Sākotnējais izmērs un minimālais izmērs, kas labāk piemērots mazākiem ekrāniem
        self.geometry("1024x768")  # Samazināts noklusējuma izmērs
        self.minsize(800, 500)  # Samazināts minimālais izmērs
        self.settings = {}  # Inicializējiet settings kā tukšu vārdnīcu
        self.scan_settings = {}  # JAUNS: Inicializējiet skenēšanas iestatījumus
        self.settings_file = os.path.join(os.path.expanduser("~"), "ocr_pdf_settings.json")
        self.scan_settings_file = os.path.join(os.path.expanduser("~"),
                                               "ocr_scan_settings.json")  # JAUNS: Skenēšanas iestatījumu fails
        self.pdf_archive_file = os.path.join(os.path.expanduser("~"), "ocr_pdf_archive.json")
        self.scan_folder_path = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "ScannedDocuments")) # JAUNS: Skenēšanas mapes ceļš
        self.auto_scan_enabled = tk.BooleanVar(value=False) # JAUNS: Automātiskās skenēšanas ieslēgšana/izslēgšana
        self.observer = None # JAUNS: Watchdog observers


        # JAUNS: Attālinātās glabāšanas iestatījumi
        self.remote_storage_type = tk.StringVar(value=self.settings.get("remote_storage_type", "Local"))
        self.ftp_host = tk.StringVar(value=self.settings.get("ftp_host", ""))
        self.ftp_port = tk.IntVar(value=self.settings.get("ftp_port", 21))
        self.ftp_user = tk.StringVar(value=self.settings.get("ftp_user", ""))
        self.ftp_pass = tk.StringVar(value=self.settings.get("ftp_pass", ""))
        self.ftp_remote_path = tk.StringVar(value=self.settings.get("ftp_remote_path", "/"))
        self.ftp_use_sftp = tk.BooleanVar(value=self.settings.get("ftp_use_sftp", False))

        self.file_paths_to_open = []
        if len(sys.argv) > 1:
            self.file_paths_to_open = [arg for arg in sys.argv[1:] if arg.lower().endswith('.pdf')]

        # Iestatam callback pēc pilnīgas inicializācijas
        self.after(100, self.check_files_to_open)


        self.google_drive_folder_id = tk.StringVar(value=self.settings.get("google_drive_folder_id", ""))
        self.google_drive_credentials_path = tk.StringVar(value=self.settings.get("google_drive_credentials_path", "credentials.json"))
        self.google_drive_token_path = tk.StringVar(value=self.settings.get("google_drive_token_path", "token.json"))

        self.auto_upload_enabled = tk.BooleanVar(value=self.settings.get("auto_upload_enabled", False))
        self.auto_upload_target = tk.StringVar(value=self.settings.get("auto_upload_target", "Local")) # Local, FTP, GoogleDrive


        self.file_listbox = tk.Listbox(self)  # Inicializē file_listbox
        self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)

        # Konfigurē krāsas
        self.file_listbox.configure(
            selectbackground='#d4edda',  # Zaļa atlases krāsa
            selectforeground='white'
        )

        self.load_app_settings()  # Ielādējiet galvenos iestatījumus
        self.load_scan_settings()  # JAUNS: Ielādējiet skenēšanas iestatījumus
        # JAUNS: Inicializējiet gaussian_blur_kernel_var
        self.gaussian_blur_kernel_var = tk.IntVar(value=self.scan_settings.get("scan_gaussian_blur_kernel", 5))
        # Pievienojiet šo rindu, lai apstrādātu loga aizvēršanu
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.images = []
        self.ocr_results = []
        self.stop_processing = False
        self.default_save_path = os.path.expanduser("~")
        self.current_image_index = -1
        self.pdf_quality = "Vidēja"
        self.document_keywords = {
            "id_card": ["id karte", "personas apliecība", "identity card", "passport", "pase", "vadītāja apliecība", "driver's license", "bankas karte", "credit card", "debit card"],
            # Pievienojiet citus atslēgvārdus, ja nepieciešams
        }


        self.internal_file_system = {"type": "folder", "name": "Sakne", "contents": []}
        self.current_folder = self.internal_file_system
        self.load_internal_file_system()

        self.lang_options = {
            "Latviešu (lav)": "lav", "Angļu (eng)": "eng", "Krievu (rus)": "rus",
            "Vācu (deu)": "deu", "Franču (fra)": "fra", "Spāņu (spa)": "spa",
            "Itāļu (ita)": "ita", "Lietuviešu (lit)": "lit", "Igauņu (est)": "est"
        }

        self.orientation_options = [
            "Auto", "Portrets", "Ainava", "A4 Portrets", "A4 Ainava",
            "Letter Portrets", "Letter Ainava", "Tāds pats kā attēls"
        ]

        self.lang_vars = {}
        for lang_name in self.lang_options.keys():
            self.lang_vars[lang_name] = tk.BooleanVar(value=(lang_name == "Angļu (eng)"))

        self.language_var = tk.StringVar(value="eng")
        self.output_dir_var = tk.StringVar(value=os.path.expanduser("~"))
        self.output_format_var = tk.StringVar(value=self.settings.get("output_format", "pdf"))
        self.psm_var = tk.IntVar(value=self.settings.get("psm", 3))
        self.oem_var = tk.IntVar(value=self.settings.get("oem", 3))

        self.brightness_var = tk.DoubleVar(value=1.0)
        self.contrast_var = tk.DoubleVar(value=1.0)
        self.sharpness_var = tk.DoubleVar(value=1.0)
        self.rotate_var = tk.IntVar(value=0)
        self.grayscale_var = tk.BooleanVar(value=True)
        self.deskew_var = tk.BooleanVar(value=False)
        self.remove_noise_var = tk.BooleanVar(value=False)
        self.invert_colors_var = tk.BooleanVar(value=False)
        self.edge_detection_var = tk.BooleanVar(value=False)
        self.binarize_var = tk.BooleanVar(value=False)

        # JAUNS: Skenēšanas iestatījumu mainīgie tagad tiek inicializēti no self.scan_settings
        self.scan_camera_index = tk.IntVar(value=self.scan_settings.get("scan_camera_index", DEFAULT_CAMERA_INDEX))
        self.scan_camera_width = tk.IntVar(value=self.scan_settings.get("scan_camera_width", 1280))
        self.scan_camera_height = tk.IntVar(value=self.scan_settings.get("scan_camera_height", 720))
        self.scan_min_contour_area = tk.IntVar(value=self.scan_settings.get("scan_min_contour_area", 10000))
        self.scan_stable_threshold = tk.DoubleVar(value=self.scan_settings.get("scan_stable_threshold", 1.5))
        self.scan_stability_tolerance = tk.DoubleVar(value=self.scan_settings.get("scan_stability_tolerance", 0.02))
        self.scan_aspect_ratio_min = tk.DoubleVar(value=self.scan_settings.get("scan_aspect_ratio_min", 0.5))
        self.scan_aspect_ratio_max = tk.DoubleVar(value=self.scan_settings.get("scan_aspect_ratio_max", 2.0))
        self.scan_gaussian_blur_kernel = tk.IntVar(value=self.scan_settings.get("scan_gaussian_blur_kernel", 5))
        self.scan_adaptive_thresh_block_size = tk.IntVar(value=self.scan_settings.get("scan_adaptive_thresh_block_size", 11))
        self.scan_adaptive_thresh_c = tk.IntVar(value=self.scan_settings.get("scan_adaptive_thresh_c", 2))
        self.scan_canny_thresh1 = tk.IntVar(value=self.scan_settings.get("scan_canny_thresh1", 75))
        self.scan_canny_thresh2 = tk.IntVar(value=self.scan_settings.get("scan_canny_thresh2", 200))

        self.create_widgets()
        self.configure_grid()
        self.create_menu()

        # Pielāgo iestatījumus no ielādētajām vērtībām
        self.orientation_var.set(self.settings.get("default_pdf_page_size"))
        self.fontsize_var.set(self.settings.get("default_pdf_font_size"))
        self.pdf_quality = self.settings.get("pdf_quality")
        pytesseract.pytesseract.tesseract_cmd = self.settings.get("tesseract_path")
        self.default_save_path = self.settings.get("default_save_path")

        # JAUNS: Skenēšanas iestatījumu mainīgo atjaunināšana vairs nav nepieciešama šeit, jo tie tiek ielādēti no `load_scan_settings`
        # un tiek atjaunināti caur `ScanSettingsWindow`

        # Atjaunina OCR valodu mainīgos
        for lang_name in self.lang_options.keys():
            if lang_name in self.settings.get("selected_ocr_languages"):
                self.lang_vars[lang_name].set(True)
            else:
                self.lang_vars[lang_name].set(False)

        # Atjaunina arī citus mainīgos, ja tie tiek ielādēti no settings
        self.output_format_var.set(self.settings.get("output_format"))
        self.psm_var.set(self.settings.get("psm"))
        self.oem_var.set(self.settings.get("oem"))
        self.language_var.set(self.settings.get("language"))
        self.output_dir_var.set(self.settings.get("output_dir"))

        # Atjaunina loga izmērus un pozīciju, nodrošinot, ka tas ir ekrāna robežās
        try:
            # Ielādē saglabātos izmērus
            saved_width = self.settings.get('window_width', 1024)
            saved_height = self.settings.get('window_height', 768)
            saved_x = self.settings.get('window_x', 0)
            saved_y = self.settings.get('window_y', 0)

            # Pārbauda ekrāna izmērus
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()

            # Pielāgo loga pozīciju, ja tas ir ārpus ekrāna
            if saved_x + saved_width > screen_width or saved_x < 0:
                saved_x = (screen_width - saved_width) // 2
            if saved_y + saved_height > screen_height or saved_y < 0:
                saved_y = (screen_height - saved_height) // 2

            # Nodrošina, ka loga izmēri nav mazāki par minimālajiem
            saved_width = max(saved_width,
                              self.winfo_reqwidth())  # winfo_reqwidth() atgriež minimālo nepieciešamo platumu
            saved_height = max(saved_height,
                               self.winfo_reqheight())  # winfo_reqheight() atgriež minimālo nepieciešamo augstumu

            self.geometry(f"{saved_width}x{saved_height}+{saved_x}+{saved_y}")
        except Exception as e:
            print(f"Nevarēja atjaunot loga izmērus/pozīciju: {e}")
            # Ja rodas kļūda, atiestata uz noklusējuma izmēriem un centrē
            self.geometry("1024x768")
            self.update_idletasks()  # Atjaunina, lai iegūtu pareizus izmērus centrēšanai
            x = (self.winfo_screenwidth() - self.winfo_width()) // 2
            y = (self.winfo_screenheight() - self.winfo_height()) // 2
            self.geometry(f"+{x}+{y}")

    def _get_physical_path_from_node(self, node):
        """Atgriež pilnu fizisko ceļu uz mapi no mezgla struktūras."""
        path_parts = []
        temp = node
        while temp and temp != self.internal_file_system:
            path_parts.insert(0, temp["name"])
            temp = temp.get("parent")
        return os.path.join(self.default_save_path, *path_parts)

    def check_files_to_open(self):
        """Atver failus no komandrindas argumentiem"""
        if self.file_paths_to_open:
            for filepath in self.file_paths_to_open:
                if os.path.exists(filepath):
                    self.open_files(filepath)

    def load_app_settings(self):
        """Ielādē lietotnes iestatījumus no JSON faila"""
        # Sākumā iestata noklusējuma vērtības visiem iestatījumiem
        self.settings.setdefault("output_format", "pdf")
        self.settings.setdefault("psm", 3)
        self.settings.setdefault("oem", 3)
        self.settings.setdefault("default_pdf_page_size", "Auto")
        self.settings.setdefault("default_pdf_font_size", 7)
        self.settings.setdefault("pdf_quality", "Vidēja")
        self.settings.setdefault("tesseract_path", DEFAULT_TESSERACT_CMD)
        self.settings.setdefault("default_save_path", os.path.expanduser("~"))
        self.settings.setdefault("selected_ocr_languages", ["Angļu (eng)"])  # Noklusējums

        # E-pasta iestatījumu noklusējuma vērtības
        self.settings.setdefault("smtp_server", "")
        self.settings.setdefault("smtp_port", 465)
        self.settings.setdefault("email_user", "")
        self.settings.setdefault("email_pass", "")
        self.settings.setdefault("from_email", "")
        self.settings.setdefault("to_email", "")
        self.settings.setdefault("use_ssl", True)
        self.settings.setdefault("email_subject", "OCR PDF dokumenti")
        self.settings.setdefault("email_body_plain",
                                 "Sveiki,\n\nPielikumā atradīsiet OCR apstrādātos PDF dokumentus.\n\nAr cieņu,\nJūsu OCR PDF App")
        self.settings.setdefault("email_body_html",
                                 "<html><body><p>Sveiki,</p><p>Pielikumā atradīsiet OCR apstrādātos PDF dokumentus.</p><p>Ar cieņu,<br/>Jūsu OCR PDF App</p></body></html>")

        # Pārējie iestatījumi (logu izmēri utt.)
        self.settings.setdefault("window_width", 1024)  # Jaunais noklusējuma platums
        self.settings.setdefault("window_height", 768)  # Jaunais noklusējuma augstums
        self.settings.setdefault("window_x", 0)
        self.settings.setdefault("window_y", 0)
        self.settings.setdefault("scan_folder_path", os.path.join(os.path.expanduser("~"), "ScannedDocuments")) # JAUNS
        self.settings.setdefault("auto_scan_enabled", False) # JAUNS
        # JAUNS: Attālinātās glabāšanas noklusējuma vērtības
        self.settings.setdefault("remote_storage_type", "Local")
        self.settings.setdefault("ftp_host", "")
        self.settings.setdefault("ftp_port", 21)
        self.settings.setdefault("ftp_user", "")
        self.settings.setdefault("ftp_pass", "")
        self.settings.setdefault("ftp_remote_path", "/")
        self.settings.setdefault("ftp_use_sftp", False)
        self.settings.setdefault("google_drive_folder_id", "")
        self.settings.setdefault("google_drive_credentials_path", "credentials.json")
        self.settings.setdefault("google_drive_token_path", "token.json")
        self.settings.setdefault("auto_upload_enabled", False)
        self.settings.setdefault("auto_upload_target", "Local")
        # JAUNS: ID koda iestatījumu noklusējuma vērtības
        self.settings.setdefault("add_id_code_to_pdf", False)
        self.settings.setdefault("id_code_type", "QR")
        self.settings.setdefault("id_code_position", "bottom_right")

        # JAUNS: ID koda iestatījumi
        self.settings.setdefault("add_id_code_to_pdf", False)
        self.settings.setdefault("id_code_type", "QR") # "QR" vai "Barcode"
        self.settings.setdefault("id_code_position", "bottom_right") # "top_right", "bottom_right", "bottom_left", "top_left"




        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
                return True
            except Exception as e:
                print(f"Nevarēja ielādēt iestatījumus: {e}")
                return False
        return False


    def load_scan_settings(self):
        """JAUNS: Ielādē skenēšanas iestatījumus no JSON faila."""
        # Noklusējuma vērtības skenēšanas iestatījumiem
        self.scan_settings.setdefault("scan_camera_index", DEFAULT_CAMERA_INDEX)
        self.scan_settings.setdefault("scan_camera_width", 1280)
        self.scan_settings.setdefault("scan_camera_height", 720)
        self.scan_settings.setdefault("scan_min_contour_area", 10000)
        self.scan_settings.setdefault("scan_stable_threshold", 1.5)
        self.scan_settings.setdefault("scan_stability_tolerance", 0.02)
        self.scan_settings.setdefault("scan_aspect_ratio_min", 0.5)
        self.scan_settings.setdefault("scan_aspect_ratio_max", 2.0)
        self.scan_settings.setdefault("scan_gaussian_blur_kernel", 5)
        self.scan_settings.setdefault("scan_adaptive_thresh_block_size", 11)
        self.scan_settings.setdefault("scan_adaptive_thresh_c", 2)
        self.scan_settings.setdefault("scan_canny_thresh1", 75)
        self.scan_settings.setdefault("scan_canny_thresh2", 200)

        if os.path.exists(self.scan_settings_file):
            try:
                with open(self.scan_settings_file, 'r', encoding='utf-8') as f:
                    loaded_scan_settings = json.load(f)
                    self.scan_settings.update(loaded_scan_settings)
                return True
            except Exception as e:
                print(f"Nevarēja ielādēt skenēšanas iestatījumus: {e}")
                return False
        return False

    def save_app_settings(self):
        """Saglabā lietotnes iestatījumus JSON failā"""
        # Pārējie iestatījumi
        self.settings["output_format"] = self.output_format_var.get()
        self.settings["psm"] = self.psm_var.get()
        self.settings["oem"] = self.oem_var.get()
        self.settings["language"] = self.language_var.get()
        self.settings["output_dir"] = self.output_dir_var.get()
        self.settings["window_width"] = self.winfo_width()
        self.settings["window_height"] = self.winfo_height()
        self.settings["window_x"] = self.winfo_x()
        self.settings["window_y"] = self.winfo_y()
        self.settings["scan_folder_path"] = self.scan_folder_path.get() # JAUNS
        self.settings["auto_scan_enabled"] = self.auto_scan_enabled.get() # JAUNS
        # JAUNS: Attālinātās glabāšanas iestatījumi
        self.settings["remote_storage_type"] = self.remote_storage_type.get()
        self.settings["ftp_host"] = self.ftp_host.get()
        self.settings["ftp_port"] = self.ftp_port.get()
        self.settings["ftp_user"] = self.ftp_user.get()
        self.settings["ftp_pass"] = self.ftp_pass.get()
        self.settings["ftp_remote_path"] = self.ftp_remote_path.get()
        self.settings["ftp_use_sftp"] = self.ftp_use_sftp.get()
        self.settings["google_drive_folder_id"] = self.google_drive_folder_id.get()
        self.settings["google_drive_credentials_path"] = self.google_drive_credentials_path.get()
        self.settings["google_drive_token_path"] = self.google_drive_token_path.get()
        self.settings["auto_upload_enabled"] = self.auto_upload_enabled.get()
        self.settings["auto_upload_target"] = self.auto_upload_target.get()
        # JAUNS: ID koda iestatījumi
        self.settings["add_id_code_to_pdf"] = self.settings.get("add_id_code_to_pdf", False) # Jāpārliecinās, ka vērtība ir iestatīta
        self.settings["id_code_type"] = self.settings.get("id_code_type", "QR")
        self.settings["id_code_position"] = self.settings.get("id_code_position", "bottom_right")




        # Saglabā arī citus iestatījumus, kas tiek mainīti SettingsWindow
        self.settings["default_save_path"] = self.default_save_path
        self.settings["pdf_quality"] = self.pdf_quality
        self.settings["default_pdf_page_size"] = self.orientation_var.get()
        self.settings["default_pdf_font_size"] = self.fontsize_var.get()
        self.settings["tesseract_path"] = pytesseract.pytesseract.tesseract_cmd

        # Saglabā atlasītās OCR valodas
        selected_langs_codes = []
        for lang_name, var in self.lang_vars.items():
            if var.get():
                selected_langs_codes.append(lang_name)  # Saglabājam nosaukumu, nevis kodu
        self.settings["selected_ocr_languages"] = selected_langs_codes

        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
            print("Iestatījumi veiksmīgi saglabāti")  # Konsolei
            return True
        except Exception as e:
            print(f"Nevarēja saglabāt iestatījumus: {e}")
            return False

    def save_scan_settings(self):
        """JAUNS: Saglabā skenēšanas iestatījumus JSON failā."""
        self.scan_settings["scan_camera_index"] = self.scan_camera_index.get()
        self.scan_settings["scan_camera_width"] = self.scan_camera_width.get()
        self.scan_settings["scan_camera_height"] = self.scan_camera_height.get()
        self.scan_settings["scan_min_contour_area"] = self.scan_min_contour_area.get()
        self.scan_settings["scan_stable_threshold"] = self.scan_stable_threshold.get()
        self.scan_settings["scan_stability_tolerance"] = self.scan_stability_tolerance.get()
        self.scan_settings["scan_aspect_ratio_min"] = self.scan_aspect_ratio_min.get()
        self.scan_settings["scan_aspect_ratio_max"] = self.scan_aspect_ratio_max.get()
        self.scan_settings["scan_gaussian_blur_kernel"] = self.scan_gaussian_blur_kernel.get()
        self.scan_settings["scan_adaptive_thresh_block_size"] = self.scan_adaptive_thresh_block_size.get()
        self.scan_settings["scan_adaptive_thresh_c"] = self.scan_adaptive_thresh_c.get()
        self.scan_settings["scan_canny_thresh1"] = self.scan_canny_thresh1.get()
        self.scan_settings["scan_canny_thresh2"] = self.scan_canny_thresh2.get()

        try:
            with open(self.scan_settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.scan_settings, f, indent=4)
            print("Skenēšanas iestatījumi veiksmīgi saglabāti")
            return True
        except Exception as e:
            print(f"Nevarēja saglabāt skenēšanas iestatījumus: {e}")
            return False


    def _flatten_file_system(self, node):
        """Rekursīvi pārveido koka struktūru par sarakstu, lai to varētu serializēt."""
        flat_list = []
        if node["type"] == "file":
            # Noņem 'parent' atsauci, jo tā ir ciklisks objekts un nevar tikt serializēta
            temp_node = node.copy()
            temp_node.pop("parent", None)
            flat_list.append(temp_node)
        elif node["type"] == "folder":
            # Noņem 'parent' atsauci no mapes objekta
            temp_node = node.copy()
            temp_node.pop("parent", None)
            temp_node["contents"] = [self._flatten_file_system(item) for item in node["contents"]]
            flat_list.append(temp_node)
        return flat_list[0] if len(flat_list) == 1 else flat_list  # Atgriež vienu objektu, ja sarakstā ir tikai viens

    def _unflatten_file_system(self, flat_node, parent=None):
        """Rekursīvi pārveido sarakstu atpakaļ par koka struktūru."""
        if flat_node["type"] == "file":
            node = flat_node.copy()
            node["parent"] = parent
            return node
        elif flat_node["type"] == "folder":
            node = flat_node.copy()
            node["parent"] = parent
            node["contents"] = [self._unflatten_file_system(item, node) for item in flat_node["contents"]]
            return node

    def detect_and_decode_barcodes(self, img):
        """Atpazīst un atšifrē QR kodus un svītrkodus attēlā."""
        if not OPENCV_AVAILABLE:
            messagebox.showwarning("Trūkst bibliotēkas",
                                   "QR kodu un svītrkodu atpazīšanai nepieciešams 'opencv-python' un 'pyzbar'.")
            return []

        from pyzbar.pyzbar import decode  # Pārliecinās, ka pyzbar ir pieejams

        img_cv = np.array(img)
        decoded_objects = decode(img_cv)

        decoded_texts = []
        for obj in decoded_objects:
            decoded_texts.append(obj.data.decode('utf-8'))  # Atšifrē QR kodu vai svītrkodu

        return decoded_texts

    def load_internal_file_system(self):
        """Ielādē iekšējo failu sistēmu no arhīva JSON faila."""
        self.internal_file_system = {"type": "folder", "name": "Sakne", "contents": []}
        self.current_folder = self.internal_file_system

        if os.path.exists(self.pdf_archive_file):
            try:
                with open(self.pdf_archive_file, 'r') as f:
                    flat_data = json.load(f)
                if flat_data:
                    # Pārliecināmies, ka ielādējam saknes mapi
                    self.internal_file_system = self._unflatten_file_system(flat_data)
                    self.current_folder = self.internal_file_system  # Sākumā vienmēr saknes mapē
            except json.JSONDecodeError:
                messagebox.showwarning("Arhīva kļūda", "Neizdevās ielādēt PDF arhīvu. Fails ir bojāts.")
            except Exception as e:
                messagebox.showerror("Arhīva ielādes kļūda", f"Neizdevās ielādēt PDF arhīvu: {e}")

    def save_pdf_archive(self):
        """Saglabā PDF arhīva datus JSON failā."""
        try:
            # Pārveido koka struktūru par serializējamu sarakstu
            flat_data = self._flatten_file_system(self.internal_file_system)
            with open(self.pdf_archive_file, 'w') as f:
                json.dump(flat_data, f, indent=4)
        except Exception as e:
            messagebox.showerror("Arhīva saglabāšanas kļūda", f"Neizdevās saglabāt PDF arhīvu: {e}")

    def add_password_to_pdf(self, pdf_path):
        """Pievieno paroli PDF dokumentam"""
        try:
            # Iegūst paroli no lietotāja
            password = simpledialog.askstring("Parole", "Ievadiet jauno paroli:", show='*')
            if not password:
                return  # Lietotājs atcēla

            reader = pypdf.PdfReader(pdf_path)

            # Ja fails jau ir šifrēts, mēģinam to atšifrēt
            if reader.is_encrypted:
                try:
                    if not reader.decrypt(""):  # Mēģinam atšifrēt bez paroles
                        # Ja neizdodas, prasam esošo paroli
                        old_pass = simpledialog.askstring("Esošā parole",
                                                          "Dokuments jau ir aizsargāts. Ievadiet esošo paroli:",
                                                          show='*')
                        if not old_pass or not reader.decrypt(old_pass):
                            messagebox.showerror("Kļūda", "Nepareiza parole vai neizdevās atšifrēt!")
                            return
                except Exception as e:
                    messagebox.showerror("Kļūda", f"Atšifrēšanas kļūda: {e}")
                    return

            writer = pypdf.PdfWriter()

            # Pārkopējam visas lapas
            for page in reader.pages:
                writer.add_page(page)

            # Šifrējam ar jauno paroli
            writer.encrypt(password)

            # Saglabājam izmaiņas
            with open(pdf_path, "wb") as f:
                writer.write(f)

            messagebox.showinfo("Veiksmīgi", f"Parole veiksmīgi pievienota dokumentam!")

        except Exception as e:
            messagebox.showerror("Kļūda", f"Neizdevās pievienot paroli: {e}")

    def remove_password_from_pdf(self, pdf_path):
        """Noņem paroli no PDF dokumenta"""
        try:
            reader = pypdf.PdfReader(pdf_path)

            if not reader.is_encrypted:
                messagebox.showinfo("Info", "Dokuments jau nav aizsargāts ar paroli!")
                return

            # Mēģinam atšifrēt bez paroles
            if not reader.decrypt(""):
                # Ja neizdodas, prasam paroli
                password = simpledialog.askstring("Parole",
                                                  "Ievadiet dokumenta paroli:",
                                                  show='*')
                if not password or not reader.decrypt(password):
                    messagebox.showerror("Kļūda", "Nepareiza parole!")
                    return

            writer = pypdf.PdfWriter()

            # Pārkopējam visas lapas
            for page in reader.pages:
                writer.add_page(page)

            # Saglabājam bez paroles
            with open(pdf_path, "wb") as f:
                writer.write(f)

            messagebox.showinfo("Veiksmīgi", "Parole veiksmīgi noņemta!")

        except Exception as e:
            messagebox.showerror("Kļūda", f"Neizdevās noņemt paroli: {e}")

    def change_password_of_pdf(self, pdf_path):
        """Maina PDF dokumenta paroli"""
        try:
            reader = pypdf.PdfReader(pdf_path)

            if not reader.is_encrypted:
                messagebox.showinfo("Info", "Dokuments nav aizsargāts ar paroli!")
                return self.add_password_to_pdf(pdf_path)  # Pārslēdzam uz paroles pievienošanu

            # Mēģinam atšifrēt bez paroles
            if not reader.decrypt(""):
                # Ja neizdodas, prasam esošo paroli
                old_pass = simpledialog.askstring("Esošā parole",
                                                  "Ievadiet pašreizējo paroli:",
                                                  show='*')
                if not old_pass or not reader.decrypt(old_pass):
                    messagebox.showerror("Kļūda", "Nepareiza parole!")
                    return

            # Iegūstam jauno paroli
            new_pass = simpledialog.askstring("Jaunā parole",
                                              "Ievadiet jauno paroli:",
                                              show='*')
            if not new_pass:
                return  # Lietotājs atcēla

            writer = pypdf.PdfWriter()

            # Pārkopējam visas lapas
            for page in reader.pages:
                writer.add_page(page)

            # Šifrējam ar jauno paroli
            writer.encrypt(new_pass)

            # Saglabājam izmaiņas
            with open(pdf_path, "wb") as f:
                writer.write(f)

            messagebox.showinfo("Veiksmīgi", "Parole veiksmīgi nomainīta!")

        except Exception as e:
            messagebox.showerror("Kļūda", f"Neizdevās mainīt paroli: {e}")

    def create_widgets(self):
        """Izveido galvenās lietotnes logrīkus un cilnes."""
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # --- Attēlu apstrādes cilne ---
        self.image_processing_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.image_processing_tab, text="Attēlu apstrāde")
        self.create_image_processing_widgets(self.image_processing_tab)

        # --- Failu pārvaldības cilne ---
        self.file_management_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.file_management_tab, text="Failu pārvaldība")
        self.create_file_management_widgets(self.file_management_tab)

        # --- Papildu rīku cilne ---
        self.additional_tools_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.additional_tools_tab, text="Papildu rīki")
        self.create_additional_tools_widgets(self.additional_tools_tab)
        # --- Automatizācijas cilne ---
        self.automation_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.automation_tab, text="Automatizācija")
        self.create_automation_widgets(self.automation_tab)

    def create_image_processing_widgets(self, parent_frame):
        """Izveido logrīkus attēlu apstrādes cilnei."""

        # Augšējā rīkjosla ar ritjoslu (labots augstums)
        top_toolbar_container = ttk.Frame(parent_frame)
        top_toolbar_container.pack(fill="x", padx=5, pady=5)

        # Izveido kanvasu ar fiksētu augstumu (~40px, var pielāgot)
        self.top_toolbar_canvas = tk.Canvas(
            top_toolbar_container,
            highlightthickness=0,
            height=40  # Šo vērtību varat pielāgot pēc saviem vajadzībām
        )
        self.top_toolbar_canvas.pack(side=tk.TOP, fill=tk.X)

        # Lietojiet pack bez expand=True, lai novērstu nevēlamu augstuma pieaugumu

        # Izveido horizontālo ritjoslu kanvasam
        self.top_toolbar_scrollbar = ttk.Scrollbar(top_toolbar_container, orient=tk.HORIZONTAL,
                                                   command=self.top_toolbar_canvas.xview)
        self.top_toolbar_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Konfigurē kanvasu, lai tas izmantotu ritjoslu
        self.top_toolbar_canvas.configure(xscrollcommand=self.top_toolbar_scrollbar.set)
        self.top_toolbar_canvas.bind('<Configure>', lambda e: self.top_toolbar_canvas.configure(
            scrollregion=self.top_toolbar_canvas.bbox("all")))

        # Izveido rāmi, kurā tiks ievietotas visas pogas un citi elementi
        # Šis rāmis tiks ievietots kanvasā
        top_frame = ttk.Frame(self.top_toolbar_canvas, padding=1)
        self.top_toolbar_canvas.create_window((0, 0), window=top_frame, anchor="nw")

        # Svarīgi: Pārliecinieties, ka top_frame izmērs tiek atjaunināts, kad tā saturs mainās
        top_frame.bind("<Configure>",
                       lambda e: self.top_toolbar_canvas.configure(scrollregion=self.top_toolbar_canvas.bbox("all")))

        self.btn_open = ttk.Button(top_frame, text="Atvērt attēlus/PDF", command=self.open_files, bootstyle="primary")
        self.btn_open.pack(side=tk.LEFT, padx=2)


        # Pievienota poga kameras skenēšanai
        self.btn_scan_camera = ttk.Button(top_frame, text="Skenēt ar kameru", command=self.scan_document_with_camera,
                                          bootstyle="info", state=tk.NORMAL if OPENCV_AVAILABLE else tk.DISABLED)
        self.btn_scan_camera.pack(side=tk.LEFT, padx=2)

        self.btn_settings = ttk.Button(top_frame, text="Vispārīgie Iestatījumi",
                                       command=self.show_settings)  # MAINĪTS TEKSTS
        self.btn_settings.pack(side=tk.LEFT, padx=2)

        self.btn_scan_settings = ttk.Button(top_frame, text="Skenēšanas Iestatījumi",
                                            command=self.show_scan_settings)  # JAUNA POGA
        self.btn_scan_settings.pack(side=tk.LEFT, padx=2)

        self.btn_check_langs = ttk.Button(top_frame, text="Pārbaudīt valodas", command=self.check_ocr_languages)
        self.btn_check_langs.pack(side=tk.LEFT, padx=2)

        # OCR parametri
        params_frame = ttk.Frame(top_frame)
        params_frame.pack(side=tk.LEFT, padx=10)  # Šis rāmis joprojām izmanto pack, jo tas ir tiešais bērns top_frame

        ttk.Label(params_frame, text="DPI:").grid(row=0, column=0)
        self.dpi_var = tk.IntVar(value=300)
        ttk.Spinbox(params_frame, from_=70, to=600, increment=10, textvariable=self.dpi_var, width=4).grid(row=0,
                                                                                                           column=1,
                                                                                                           padx=2)

        ttk.Label(params_frame, text="Fonts:").grid(row=0, column=2)
        self.fontsize_var = tk.IntVar(value=7)
        ttk.Spinbox(params_frame, from_=5, to=20, increment=1, textvariable=self.fontsize_var, width=3).grid(row=0,
                                                                                                             column=3,
                                                                                                             padx=2)

        ttk.Label(params_frame, text="Konfidence:").grid(row=0, column=4)
        self.confidence_var = tk.IntVar(value=60)
        ttk.Spinbox(params_frame, from_=0, to=100, increment=5, textvariable=self.confidence_var, width=3).grid(row=0,
                                                                                                                column=5,
                                                                                                            padx=2)

        ttk.Label(params_frame, text="PSM:").grid(row=0, column=6)
        # self.psm_var = tk.IntVar(value=3) # Šī rinda vairs nav nepieciešama, jo definēta __init__
        ttk.Spinbox(params_frame, from_=0, to=13, increment=1, textvariable=self.psm_var, width=3).grid(row=0, column=7,
                                                                                                        padx=2)

        ttk.Label(params_frame, text="OEM:").grid(row=0, column=8)
        # self.oem_var = tk.IntVar(value=3) # Šī rinda vairs nav nepieciešama, jo definēta __init__
        ttk.Spinbox(params_frame, from_=0, to=3, increment=1, textvariable=self.oem_var, width=3).grid(row=0, column=9,
                                                                                                       padx=2)

        self.orientation_var = tk.StringVar(value="Auto")
        self.orientation_combo = ttk.Combobox(top_frame, values=self.orientation_options, state="readonly", width=15,
                                              textvariable=self.orientation_var)
        self.orientation_combo.pack(side=tk.LEFT, padx=5)

        self.include_text_var = tk.BooleanVar(value=tk.FALSE)
        ttk.Checkbutton(top_frame, text="Iekļaut meklējamo tekstu", variable=self.include_text_var).pack(side=tk.LEFT,
                                                                                                         padx=5)

        # Galvenā darba zona - izmantojam PanedWindow, lai nodrošinātu izmēru pielāgošanu
        main_paned_window = ttk.PanedWindow(parent_frame, orient=tk.HORIZONTAL)
        main_paned_window.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        # Kreiso pusi (failu saraksts) ievietojam atsevišķā rāmī
        file_list_pane = ttk.Frame(main_paned_window)
        main_paned_window.add(file_list_pane,
                              weight=2)  # Piešķir nelielu svaru, lai sākumā būtu platāks

        # Labo pusi (attēla priekšskatījums un OCR teksts) ievietojam atsevišķā rāmī
        image_ocr_pane = ttk.Frame(main_paned_window)
        main_paned_window.add(image_ocr_pane, weight=1)  # Ļaujam tam izstiepties

        # Konfigurējam labās puses rāmi, lai tas izstieptos
        image_ocr_pane.columnconfigure(0, weight=1)
        image_ocr_pane.rowconfigure(0, weight=1)  # Rinda attēla priekšskatījumam
        image_ocr_pane.rowconfigure(1, weight=1)  # Rinda OCR tekstam

        # Failu saraksta rāmis
        file_list_container = ttk.Frame(file_list_pane)  # MAINĪTS: Vecāks tagad ir file_list_pane
        file_list_container.pack(fill="both", expand=True, padx=(0, 5))  # MAINĪTS: Izmantojam pack
        file_list_container.pack_propagate(False)  # Novērš rāmja izmēra maiņu
        file_list_container.rowconfigure(1, weight=1)  # Nodrošina, ka listbox izstiepjas

        ttk.Label(file_list_container, text="Atlasītie faili:").pack(fill="x")

        # Ritjosla failu sarakstam
        file_list_frame_with_scrollbar = ttk.Frame(file_list_container)
        file_list_frame_with_scrollbar.pack(fill="both", expand=True)  # Šis ir pareizi, jo ir iekš file_list_container

        self.file_listbox = tk.Listbox(file_list_frame_with_scrollbar, selectmode=tk.EXTENDED, exportselection=False)
        self.file_listbox.pack(side=tk.LEFT, fill="both", expand=True)

        file_list_scrollbar = ttk.Scrollbar(file_list_frame_with_scrollbar, orient=tk.VERTICAL,
                                            command=self.file_listbox.yview)
        file_list_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.file_listbox.config(yscrollcommand=file_list_scrollbar.set)

        self.file_listbox.bind("<Button-1>", self.file_list_drag_start)  # Kreisais klikšķis sāk vilkšanu
        self.file_listbox.bind("<B1-Motion>", self.file_list_drag_motion)  # Vilkšanas kustība
        self.file_listbox.bind("<ButtonRelease-1>", self.file_list_drag_drop)  # Nomešana
        self.file_listbox.bind("<Button-3>", self.show_file_context_menu)  # Labais klikšķis
        self.file_listbox.bind("<Button-1>", self.on_file_click)  # Pievienojam jaunu bind, lai apstrādātu vienu klikšķi
        self.file_listbox.bind("<<ListboxSelect>>",
                               lambda e: self.after(1, self.on_file_select_deferred))  # Aizkavēta atlase
        # Inicializējam vilkšanas datus attēlu sarakstam
        self.file_drag_data = {"item_index": None, "start_y": 0}


        # JAUNS: OCR pogas un progresa josla failu saraksta rāmī
        ocr_controls_frame = ttk.Frame(file_list_container)
        ocr_controls_frame.pack(fill="x", pady=5)

        self.progress = ttk.Progressbar(ocr_controls_frame, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", expand=True, padx=(0, 5))

        ocr_buttons_inner_frame = ttk.Frame(ocr_controls_frame)
        ocr_buttons_inner_frame.pack(fill="x", pady=(5,0)) # Neliela atstarpe starp progress bar un pogām

        self.btn_start = ttk.Button(ocr_buttons_inner_frame, text="Sākt OCR", command=self.start_processing, bootstyle="success")
        self.btn_start.pack(side=tk.LEFT, expand=True, padx=2)

        self.btn_stop = ttk.Button(ocr_buttons_inner_frame, text="Apturēt", command=self.stop_processing_func, state=tk.DISABLED,
                                   bootstyle="danger")
        self.btn_stop.pack(side=tk.LEFT, expand=True, padx=2)

        # Pogas failu kārtošanai
        move_buttons_frame = ttk.Frame(file_list_container)  # Izmantojam file_list_container kā vecāku
        move_buttons_frame.pack(fill="x", pady=5)

        ttk.Button(move_buttons_frame, text="↑ Uz augšu", command=self.move_file_up).pack(side=tk.LEFT, padx=2)
        ttk.Button(move_buttons_frame, text="↓ Uz leju", command=self.move_file_down).pack(side=tk.LEFT, padx=2)

        # Attēla priekšskatījuma rāmis
        preview_frame = ttk.Frame(image_ocr_pane)  # MAINĪTS: Vecāks tagad ir image_ocr_pane
        preview_frame.grid(row=0, column=0, sticky="nsew")  # MAINĪTS: Izmantojam grid iekš image_ocr_pane
        preview_frame.rowconfigure(1, weight=1)  # Nodrošina, ka canvas izstiepjas

        ttk.Label(preview_frame, text="Attēla priekšskatījums:").pack(fill="x")
        self.canvas = tk.Canvas(preview_frame, background="#222222")
        self.canvas.pack(fill="both", expand=True)  # Šis ir pareizi, jo ir iekš preview_frame
        self.canvas.bind("<Configure>", self.resize_canvas)
        self.canvas.bind("<MouseWheel>", self.on_canvas_mouse_wheel)  # Zoom
        self.canvas.bind("<Button-4>", self.on_canvas_mouse_wheel)  # MacOS
        self.canvas.bind("<Button-5>", self.on_canvas_mouse_wheel)  # MacOS
        self.canvas.bind("<ButtonPress-2>", self.on_canvas_pan_start)  # Pan
        self.canvas.bind("<B2-Motion>", self.on_canvas_pan_drag)
        self.canvas.bind("<ButtonRelease-2>", self.on_canvas_pan_end)
        self.canvas.bind("<ButtonPress-1>", self.on_canvas_selection_start)  # Selection
        self.canvas.bind("<B1-Motion>", self.on_canvas_selection_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_selection_end)
        self.canvas_selection_rect = None
        self.canvas_selection_start_x = None
        self.canvas_selection_start_y = None
        self.canvas_zoom_factor = 1.0
        self.canvas_pan_x = 0
        self.canvas_pan_y = 0
        self.canvas_start_pan_x = 0
        self.canvas_start_pan_y = 0

        # Attēlu apstrādes rīki (ar ritjoslu)
        # Izveido rāmi ar ritjoslu ap attēlu apstrādes rīkiem
        processing_tools_outer_frame = ttk.Frame(preview_frame)
        processing_tools_outer_frame.pack(fill="x", pady=5)  # Šis ir pareizi, jo ir iekš preview_frame

        processing_tools_canvas = tk.Canvas(processing_tools_outer_frame, highlightthickness=0)
        processing_tools_canvas.pack(side=tk.LEFT, fill="both", expand=True)

        processing_tools_scrollbar = ttk.Scrollbar(processing_tools_outer_frame, orient=tk.VERTICAL,
                                                   command=processing_tools_canvas.yview)
        processing_tools_scrollbar.pack(side=tk.RIGHT, fill="y")

        processing_tools_canvas.configure(yscrollcommand=processing_tools_scrollbar.set)
        processing_tools_canvas.bind('<Configure>', lambda e: processing_tools_canvas.configure(
            scrollregion=processing_tools_canvas.bbox("all")))

        image_processing_tools_frame = ttk.LabelFrame(processing_tools_canvas, text="Attēlu apstrāde", padding=5)
        processing_tools_canvas.create_window((0, 0), window=image_processing_tools_frame, anchor="nw")

        # Izveido rāmi slīdņiem un pogām
        processing_inner_frame = ttk.Frame(image_processing_tools_frame)
        processing_inner_frame.pack(fill="both", expand=True)  # Šis ir pareizi, jo ir iekš image_processing_tools_frame

        # Slīdņi
        sliders_frame = ttk.Frame(processing_inner_frame)
        sliders_frame.grid(row=0, column=0, sticky="nsew", padx=5,
                           pady=5)  # Šis ir pareizi, jo ir iekš processing_inner_frame

        ttk.Label(sliders_frame, text="Spilgtums:").grid(row=0, column=0, sticky="w")
        self.brightness_slider = tk.Scale(sliders_frame, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL,
                                          variable=self.brightness_var, command=self.apply_image_filters)
        self.brightness_slider.grid(row=0, column=1, sticky="ew", padx=5)

        ttk.Label(sliders_frame, text="Kontrasts:").grid(row=1, column=0, sticky="w")
        self.contrast_slider = tk.Scale(sliders_frame, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL,
                                        variable=self.contrast_var, command=self.apply_image_filters)
        self.contrast_slider.grid(row=1, column=1, sticky="ew", padx=5)

        ttk.Label(sliders_frame, text="Asums:").grid(row=2, column=0, sticky="w")
        self.sharpness_slider = tk.Scale(sliders_frame, from_=2.0, to=3.5, resolution=0.1, orient=tk.HORIZONTAL,
                                         variable=self.sharpness_var, command=self.apply_image_filters)
        self.sharpness_slider.grid(row=2, column=1, sticky="ew", padx=5)

        ttk.Label(sliders_frame, text="Rotācija:").grid(row=3, column=0, sticky="w")
        self.rotate_spinbox = ttk.Spinbox(sliders_frame, from_=-360, to=360, increment=90, textvariable=self.rotate_var,
                                          width=5, command=lambda: self.apply_image_filters(None))
        self.rotate_spinbox.grid(row=3, column=1, sticky="ew", padx=5)
        sliders_frame.columnconfigure(1, weight=1)

        # Papildu attēlu apstrādes pogas un čekboksi
        processing_buttons_frame = ttk.Frame(processing_inner_frame)
        processing_buttons_frame.grid(row=0, column=1, sticky="nsew", padx=10,
                                      pady=5)  # Šis ir pareizi, jo ir iekš processing_inner_frame

        ttk.Checkbutton(processing_buttons_frame, text="Pelēktoņi", variable=self.grayscale_var,
                        command=lambda: self.apply_image_filters(None)).pack(anchor="w", pady=2)
        ttk.Checkbutton(processing_buttons_frame, text="Slīpuma korekcija", variable=self.deskew_var,
                        command=lambda: self.apply_image_filters(None),
                        state=tk.NORMAL if OPENCV_AVAILABLE else tk.DISABLED).pack(anchor="w", pady=2)
        ttk.Checkbutton(processing_buttons_frame, text="Trokšņu samazināšana", variable=self.remove_noise_var,
                        command=lambda: self.apply_image_filters(None)).pack(anchor="w", pady=2)
        ttk.Checkbutton(processing_buttons_frame, text="Attēla negatīvs", variable=self.invert_colors_var,
                        command=lambda: self.apply_image_filters(None)).pack(anchor="w", pady=2)
        ttk.Checkbutton(processing_buttons_frame, text="Malu noteikšana", variable=self.edge_detection_var,
                        command=lambda: self.apply_image_filters(None)).pack(anchor="w", pady=2)
        ttk.Checkbutton(processing_buttons_frame, text="Binārizācija", variable=self.binarize_var,
                        command=lambda: self.apply_image_filters(None)).pack(anchor="w", pady=2)

        ttk.Button(processing_buttons_frame, text="Apgriezt attēlu", command=self.crop_image).pack(anchor="w", pady=2)
        ttk.Button(processing_buttons_frame, text="Pagriezt par 90°", command=self.rotate_90_degrees).pack(anchor="w",
                                                                                                           pady=2)
        ttk.Button(processing_buttons_frame, text="Spoguļot (Horiz.)",
                   command=lambda: self.flip_image(Image.FLIP_LEFT_RIGHT)).pack(anchor="w", pady=2)
        ttk.Button(processing_buttons_frame, text="Spoguļot (Vert.)",
                   command=lambda: self.flip_image(Image.FLIP_TOP_BOTTOM)).pack(anchor="w", pady=2)
        ttk.Button(processing_buttons_frame, text="Mainīt izmērus", command=self.resize_image_dialog).pack(anchor="w",
                                                                                                           pady=2)
        ttk.Button(processing_buttons_frame, text="Auto uzlabošana", command=self.auto_enhance_image).pack(anchor="w",
                                                                                                           pady=2)
        ttk.Button(processing_buttons_frame, text="Rādīt histogrammu", command=self.show_image_histogram).pack(
            anchor="w", pady=2)
        ttk.Button(processing_buttons_frame, text="Rādīt metadatus", command=self.show_image_metadata).pack(anchor="w",
                                                                                                            pady=2)
        ttk.Button(processing_buttons_frame, text="Rādīt krāsu paleti", command=self.show_color_palette).pack(
            anchor="w", pady=2)
        ttk.Button(processing_buttons_frame, text="Atvērt pilnekrāna priekšskatījumu",
                   command=self.open_fullscreen_preview).pack(anchor="w", pady=2)

        # OCR rezultātu rāmis
        text_frame = ttk.Frame(image_ocr_pane)  # MAINĪTS: Vecāks tagad ir image_ocr_pane
        text_frame.grid(row=1, column=0, sticky="nsew", padx=5,
                        pady=(0, 5))  # MAINĪTS: Izmantojam grid iekš image_ocr_pane
        text_frame.rowconfigure(1, weight=1)  # Nodrošina, ka text_ocr izstiepjas

        ttk.Label(text_frame, text="OCR rezultāts (rediģējams):").pack(fill="x")

        # Ritjosla OCR tekstam
        text_ocr_frame_with_scrollbar = ttk.Frame(text_frame)
        text_ocr_frame_with_scrollbar.pack(fill="both", expand=True)  # Šis ir pareizi, jo ir iekš text_frame

        self.text_ocr = tk.Text(text_ocr_frame_with_scrollbar, wrap="word")
        self.text_ocr.pack(side=tk.LEFT, fill="both", expand=True)

        text_ocr_scrollbar = ttk.Scrollbar(text_ocr_frame_with_scrollbar, orient=tk.VERTICAL,
                                           command=self.text_ocr.yview)
        text_ocr_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.text_ocr.config(yscrollcommand=text_ocr_scrollbar.set)

        file_list_buttons_frame = ttk.Frame(file_list_container)
        file_list_buttons_frame.pack(fill="x", pady=5)  # Šis ir pareizi, jo ir iekš file_list_container
        ttk.Button(file_list_buttons_frame, text="Dzēst atlasīto", command=self.delete_selected_image,
                   bootstyle="danger").pack(fill="x")


    def create_file_management_widgets(self, parent_frame):
        """Izveido logrīkus failu pārvaldības cilnei."""
        # Izveido rāmi ar ritjoslu ap visu failu pārvaldības cilnes saturu
        file_management_outer_frame = ttk.Frame(parent_frame)
        file_management_outer_frame.pack(fill="both", expand=True)

        # Pārliecinieties, ka šis rāmis aizņem visu pieejamo vietu
        file_management_outer_frame.columnconfigure(0, weight=1)
        file_management_outer_frame.rowconfigure(0, weight=1)

        # Iekšējais rāmis, kurā atradīsies viss failu pārvaldības saturs
        inner_file_management_frame = ttk.Frame(file_management_outer_frame)
        inner_file_management_frame.grid(row=0, column=0, sticky="nsew")  # Izmanto grid, lai aizņemtu visu vietu

        # Meklēšanas un filtrēšanas rāmis
        filter_frame = ttk.LabelFrame(inner_file_management_frame, text="Meklēšana un filtrēšana", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        # Meklēšana
        ttk.Label(filter_frame, text="Meklēt:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=40)
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        self.search_entry.bind("<KeyRelease>", self.filter_pdf_list)

        # Datuma filtrēšana
        ttk.Label(filter_frame, text="No datuma:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.start_date_var = tk.StringVar()
        self.start_date_entry = ttk.Entry(filter_frame, textvariable=self.start_date_var, width=15)
        self.start_date_entry.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        ttk.Button(filter_frame, text="Kalendārs", command=self.open_start_date_calendar).grid(row=1, column=2,
                                                                                               sticky="w", padx=2)

        ttk.Label(filter_frame, text="Līdz datumam:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.end_date_var = tk.StringVar()
        self.end_date_entry = ttk.Entry(filter_frame, textvariable=self.end_date_var, width=15)
        self.end_date_entry.grid(row=2, column=1, sticky="w", padx=5, pady=2)
        ttk.Button(filter_frame, text="Kalendārs", command=self.open_end_date_calendar).grid(row=2, column=2,
                                                                                             sticky="w", padx=2)

        ttk.Button(filter_frame, text="Filtrēt", command=self.filter_pdf_list).grid(row=3, column=1, sticky="ew",
                                                                                    padx=5, pady=5)
        ttk.Button(filter_frame, text="Notīrīt filtrus", command=self.clear_pdf_filters).grid(row=3, column=2,
                                                                                              sticky="ew", padx=5,
                                                                                              pady=5)

        filter_frame.columnconfigure(1, weight=1)

        # PDF arhīva saraksts un mapju navigācija
        archive_frame = ttk.LabelFrame(inner_file_management_frame, text="Saglabātie PDF faili", padding=10)
        archive_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)  # Aizņem visu atlikušo vietu

        # Mapju navigācijas rīkjosla
        folder_nav_frame = ttk.Frame(archive_frame)
        folder_nav_frame.pack(fill="x", pady=(0, 5))

        self.back_button = ttk.Button(folder_nav_frame, text="Atpakaļ", command=self.go_back_folder, state=DISABLED)
        self.back_button.pack(side=LEFT, padx=2)

        self.current_path_label = ttk.Label(folder_nav_frame, text="/")
        self.current_path_label.pack(side=LEFT, padx=5)

        # Ritjosla PDF sarakstam
        pdf_list_frame_with_scrollbar = ttk.Frame(archive_frame)
        pdf_list_frame_with_scrollbar.pack(side=LEFT, fill="both", expand=True)

        self.pdf_listbox = tk.Listbox(pdf_list_frame_with_scrollbar, selectmode=tk.EXTENDED,
                                      exportselection=False)  # Atļauj vairāku failu atlasi
        self.pdf_listbox.pack(side=LEFT, fill="both", expand=True)

        pdf_list_scrollbar = ttk.Scrollbar(pdf_list_frame_with_scrollbar, orient="vertical",
                                           command=self.pdf_listbox.yview)
        pdf_list_scrollbar.pack(side=RIGHT, fill="y")
        self.pdf_listbox.config(yscrollcommand=pdf_list_scrollbar.set)

        self.pdf_listbox.bind("<<ListboxSelect>>", self.on_pdf_select)
        self.pdf_listbox.bind("<Double-Button-1>", self.open_selected_item)  # Dubultklikšķis atver PDF vai mapi
        self.pdf_listbox.bind("<Button-3>", self.show_pdf_context_menu)  # Labais klikšķis

        # Drag and Drop bindings
        self.pdf_listbox.bind("<Button-1>", self.drag_start)
        self.pdf_listbox.bind("<B1-Motion>", self.drag_motion)
        self.pdf_listbox.bind("<ButtonRelease-1>", self.drag_drop)
        self.drag_data = {"x": 0, "y": 0, "item": None, "index": None}

        # Pogas PDF arhīvam
        pdf_buttons_frame = ttk.Frame(archive_frame)
        pdf_buttons_frame.pack(side=RIGHT, fill="y", padx=10)

        ttk.Button(pdf_buttons_frame, text="Atvērt", command=self.open_selected_item).pack(fill="x", pady=5)
        ttk.Button(pdf_buttons_frame, text="Atvērt mapē (sistēmā)", command=self.open_pdf_location).pack(fill="x",
                                                                                                         pady=5)
        ttk.Button(pdf_buttons_frame, text="Dzēst", command=self.delete_selected_item,
                   bootstyle="danger").pack(fill="x", pady=5)
        ttk.Button(pdf_buttons_frame, text="Nosūtīt e-pastā", command=self.send_selected_pdfs_by_email,
                   bootstyle="info").pack(fill="x", pady=5)
        ttk.Button(pdf_buttons_frame, text="Izveidot mapi", command=self.create_new_folder_internal).pack(fill="x",
                                                                                                          pady=5)
        ttk.Button(pdf_buttons_frame, text="Pārvietot uz...", command=self.move_selected_items).pack(fill="x", pady=5)
        ttk.Button(pdf_buttons_frame, text="Pārdēvēt", command=self.rename_selected_item).pack(fill="x", pady=5)
        ttk.Button(pdf_buttons_frame, text="Saglabāt kā Word", command=self.save_as_word).pack(fill="x", pady=5)

        self.refresh_pdf_list()  # Tagad self.current_folder ir inicializēts

    def create_additional_tools_widgets(self, parent_frame):
        """Izveido logrīkus papildu rīku cilnei."""
        main_frame = ttk.Frame(parent_frame, padding=10)
        main_frame.pack(fill=BOTH, expand=True)

        # Ritjosla visam papildu rīku saturam
        tools_canvas = tk.Canvas(main_frame, highlightthickness=0)
        tools_canvas.pack(side=LEFT, fill="both", expand=True)

        tools_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tools_canvas.yview)
        tools_scrollbar.pack(side=RIGHT, fill="y")

        tools_canvas.configure(yscrollcommand=tools_scrollbar.set)
        tools_canvas.bind('<Configure>', lambda e: tools_canvas.configure(scrollregion=tools_canvas.bbox("all")))

        # Iekšējais rāmis, kurā atradīsies visi rīki
        inner_tools_frame = ttk.Frame(tools_canvas)
        tools_canvas.create_window((0, 0), window=inner_tools_frame, anchor="nw")

        # Attēlu analīzes rīki
        image_analysis_frame = ttk.LabelFrame(inner_tools_frame, text="Attēlu analīze", padding=10)
        image_analysis_frame.pack(fill=X, padx=5, pady=5)

        ttk.Button(image_analysis_frame, text="Rādīt histogrammu", command=self.show_image_histogram).pack(fill=X,
                                                                                                           pady=2)
        ttk.Button(image_analysis_frame, text="Rādīt metadatus", command=self.show_image_metadata).pack(fill=X, pady=2)
        ttk.Button(image_analysis_frame, text="Rādīt krāsu paleti", command=self.show_color_palette).pack(fill=X,
                                                                                                          pady=2)
        ttk.Button(image_analysis_frame, text="Attēla salīdzināšana", command=self.compare_images).pack(fill=X, pady=2)
        ttk.Button(image_analysis_frame, text="Attēla kvalitātes novērtēšana",
                   command=self.evaluate_image_quality).pack(fill=X, pady=2)
        ttk.Button(image_analysis_frame, text="Teksta izvilkšana no apgabala",
                   command=self.extract_text_from_region).pack(fill=X, pady=2)

        # QR koda ģenerators
        qr_generator_frame = ttk.LabelFrame(inner_tools_frame, text="QR koda ģenerators", padding=10)
        qr_generator_frame.pack(fill=X, padx=5, pady=5)

        ttk.Label(qr_generator_frame, text="Teksts QR kodam:").grid(row=0, column=0, sticky=W, pady=2)
        self.qr_text_var = tk.StringVar()
        ttk.Entry(qr_generator_frame, textvariable=self.qr_text_var, width=50).grid(row=0, column=1, sticky=EW, padx=5,
                                                                                    pady=2)

        ttk.Button(qr_generator_frame, text="Ģenerēt QR kodu", command=self.generate_qr_code).grid(row=1, column=0,
                                                                                                   columnspan=2, pady=5)

        self.qr_canvas = tk.Canvas(qr_generator_frame, width=200, height=200, bg="white")
        self.qr_canvas.grid(row=2, column=0, columnspan=2, pady=5)

        qr_generator_frame.columnconfigure(1, weight=1)

        # Papildu attēlu apstrādes rīki
        advanced_image_tools_frame = ttk.LabelFrame(inner_tools_frame, text="Papildu attēlu rīki", padding=10)
        advanced_image_tools_frame.pack(fill=X, padx=5, pady=5)

        ttk.Button(advanced_image_tools_frame, text="Krāsu konvertēšana", command=self.convert_color_space).pack(fill=X,
                                                                                                                 pady=2)
        ttk.Button(advanced_image_tools_frame, text="Ūdenszīmes pievienošana", command=self.add_watermark).pack(fill=X,
                                                                                                                pady=2)
        ttk.Button(advanced_image_tools_frame, text="Attēla mozaīka", command=self.create_image_mosaic).pack(fill=X,
                                                                                                             pady=2)
        ttk.Button(advanced_image_tools_frame, text="Attēla salikšana (stitch)", command=self.stitch_images).pack(
            fill=X, pady=2)
        ttk.Button(advanced_image_tools_frame, text="Attēla atjaunošana (inpainting)",
                   command=self.image_inpainting).pack(fill=X, pady=2)
        ttk.Button(advanced_image_tools_frame, text="Attēla stilizācija", command=self.stylize_image).pack(fill=X,
                                                                                                           pady=2)
        ttk.Button(advanced_image_tools_frame, text="Attēla ģeometriskās transformācijas",
                   command=self.geometric_transformations).pack(fill=X, pady=2)

        # Jaunās funkcijas
        ttk.Button(advanced_image_tools_frame, text="Konvertēt uz pelēktoņiem", command=self.convert_to_grayscale).pack(
            fill=X, pady=2)
        ttk.Button(advanced_image_tools_frame, text="Pielietot sliekšņošanu", command=self.apply_thresholding).pack(
            fill=X, pady=2)
        ttk.Button(advanced_image_tools_frame, text="Pielietot Gausa izplūšanu", command=self.apply_gaussian_blur).pack(
            fill=X, pady=2)
        ttk.Button(advanced_image_tools_frame, text="Pielietot mediānas filtru", command=self.apply_median_filter).pack(
            fill=X, pady=2)
        ttk.Button(advanced_image_tools_frame, text="Uzlabot asumu", command=self.sharpen_image).pack(fill=X, pady=2)
        ttk.Button(advanced_image_tools_frame, text="Pagriezt par leņķi", command=self.rotate_image_by_angle).pack(
            fill=X, pady=2)
        ttk.Button(advanced_image_tools_frame, text="Pievienot teksta pārklājumu", command=self.add_text_overlay).pack(
            fill=X, pady=2)
        ttk.Button(advanced_image_tools_frame, text="Zīmēt taisnstūri", command=self.draw_rectangle_on_image).pack(
            fill=X, pady=2)
        ttk.Button(advanced_image_tools_frame, text="Zīmēt apli", command=self.draw_circle_on_image).pack(fill=X,
                                                                                                          pady=2)
        ttk.Button(advanced_image_tools_frame, text="Izvilkt krāsu kanālus", command=self.extract_color_channels).pack(
            fill=X, pady=2)
        ttk.Button(advanced_image_tools_frame, text="Apvienot krāsu kanālus", command=self.merge_color_channels).pack(
            fill=X, pady=2)
        ttk.Button(advanced_image_tools_frame, text="Pielietot sēpijas filtru", command=self.apply_sepia_filter).pack(
            fill=X, pady=2)
        ttk.Button(advanced_image_tools_frame, text="Pielietot vinjetes efektu",
                   command=self.apply_vignette_effect).pack(fill=X, pady=2)
        ttk.Button(advanced_image_tools_frame, text="Pikselizēt attēlu", command=self.pixelate_image).pack(fill=X,
                                                                                                           pady=2)
        ttk.Button(advanced_image_tools_frame, text="Noteikt sejas", command=self.detect_faces).pack(fill=X, pady=2)

    def create_automation_widgets(self, parent_frame):
        """Izveido logrīkus automatizācijas cilnei."""
        main_frame = ttk.Frame(parent_frame, padding=10)
        main_frame.pack(fill=BOTH, expand=True)

        # Ritjosla visam automatizācijas saturam
        automation_canvas = tk.Canvas(main_frame, highlightthickness=0)
        automation_canvas.pack(side=LEFT, fill="both", expand=True)

        automation_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=automation_canvas.yview)
        automation_scrollbar.pack(side=RIGHT, fill="y")

        automation_canvas.configure(yscrollcommand=automation_scrollbar.set)
        automation_canvas.bind('<Configure>',
                               lambda e: automation_canvas.configure(scrollregion=automation_canvas.bbox("all")))

        # Iekšējais rāmis, kurā atradīsies visi automatizācijas rīki
        inner_automation_frame = ttk.Frame(automation_canvas)
        automation_canvas.create_window((0, 0), window=inner_automation_frame, anchor="nw")

        # --- Automātiskās skenēšanas uzraudzība ---
        scan_monitor_frame = ttk.LabelFrame(inner_automation_frame, text="Automātiskā skenēšanas mapes uzraudzība",
                                            padding=10)
        scan_monitor_frame.pack(fill=X, padx=5, pady=5)

        ttk.Label(scan_monitor_frame, text="Skenēšanas mapes ceļš:").grid(row=0, column=0, sticky=W, pady=2)
        self.scan_folder_entry = ttk.Entry(scan_monitor_frame, textvariable=self.scan_folder_path, width=50)
        self.scan_folder_entry.grid(row=0, column=1, sticky=EW, padx=5, pady=2)
        ttk.Button(scan_monitor_frame, text="Pārlūkot...", command=self.browse_scan_folder).grid(row=0, column=2,
                                                                                                 padx=5)

        ttk.Checkbutton(scan_monitor_frame, text="Iespējot automātisko skenēšanu", variable=self.auto_scan_enabled,
                        command=self.toggle_auto_scan).grid(row=1, column=0, columnspan=3, sticky=W, pady=5)

        self.auto_scan_status_label = ttk.Label(scan_monitor_frame, text="Statuss: Izslēgts", bootstyle="info")
        self.auto_scan_status_label.grid(row=2, column=0, columnspan=3, sticky=W, pady=5)

        scan_monitor_frame.columnconfigure(1, weight=1)

        # --- Attālinātās glabāšanas iestatījumi ---
        remote_storage_frame = ttk.LabelFrame(inner_automation_frame, text="Attālinātās glabāšanas iestatījumi",
                                              padding=10)
        remote_storage_frame.pack(fill=X, padx=5, pady=10)

        ttk.Label(remote_storage_frame, text="Glabāšanas veids:").grid(row=0, column=0, sticky=W, pady=2)
        self.remote_storage_type_combo = ttk.Combobox(remote_storage_frame, textvariable=self.remote_storage_type,
                                                      values=["Local", "FTP", "SFTP", "Google Drive"], state="readonly")
        self.remote_storage_type_combo.grid(row=0, column=1, sticky=EW, padx=5, pady=2)
        self.remote_storage_type_combo.bind("<<ComboboxSelected>>", self.update_remote_storage_fields)

        # FTP/SFTP iestatījumi
        self.ftp_settings_frame = ttk.LabelFrame(remote_storage_frame, text="FTP/SFTP iestatījumi", padding=5)
        self.ftp_settings_frame.grid(row=1, column=0, columnspan=2, sticky=EW, padx=5, pady=5)

        ttk.Label(self.ftp_settings_frame, text="Host:").grid(row=0, column=0, sticky=W, pady=2)
        ttk.Entry(self.ftp_settings_frame, textvariable=self.ftp_host).grid(row=0, column=1, sticky=EW, padx=5, pady=2)
        ttk.Label(self.ftp_settings_frame, text="Port:").grid(row=0, column=2, sticky=W, pady=2)
        ttk.Entry(self.ftp_settings_frame, textvariable=self.ftp_port).grid(row=0, column=3, sticky=EW, padx=5, pady=2)

        ttk.Label(self.ftp_settings_frame, text="Lietotājvārds:").grid(row=1, column=0, sticky=W, pady=2)
        ttk.Entry(self.ftp_settings_frame, textvariable=self.ftp_user).grid(row=1, column=1, sticky=EW, padx=5, pady=2)
        ttk.Label(self.ftp_settings_frame, text="Parole:").grid(row=1, column=2, sticky=W, pady=2)
        ttk.Entry(self.ftp_settings_frame, textvariable=self.ftp_pass, show="*").grid(row=1, column=3, sticky=EW,
                                                                                      padx=5, pady=2)

        ttk.Label(self.ftp_settings_frame, text="Attālā mape:").grid(row=2, column=0, sticky=W, pady=2)
        ttk.Entry(self.ftp_settings_frame, textvariable=self.ftp_remote_path).grid(row=2, column=1, columnspan=3,
                                                                                   sticky=EW, padx=5, pady=2)

        ttk.Checkbutton(self.ftp_settings_frame, text="Izmantot SFTP", variable=self.ftp_use_sftp).grid(row=3, column=0,
                                                                                                        columnspan=4,
                                                                                                        sticky=W,
                                                                                                        pady=5)
        ttk.Button(self.ftp_settings_frame, text="Pārbaudīt savienojumu", command=self.test_ftp_connection,
                   bootstyle=INFO).grid(row=4, column=0, columnspan=4, pady=5)
        self.ftp_settings_frame.columnconfigure(1, weight=1)
        self.ftp_settings_frame.columnconfigure(3, weight=1)

        # Google Drive iestatījumi
        self.google_drive_settings_frame = ttk.LabelFrame(remote_storage_frame, text="Google Drive iestatījumi",
                                                          padding=5)
        self.google_drive_settings_frame.grid(row=2, column=0, columnspan=2, sticky=EW, padx=5, pady=5)

        ttk.Label(self.google_drive_settings_frame, text="Mapes ID:").grid(row=0, column=0, sticky=W, pady=2)
        ttk.Entry(self.google_drive_settings_frame, textvariable=self.google_drive_folder_id).grid(row=0, column=1,
                                                                                                   sticky=EW, padx=5,
                                                                                                   pady=2)

        ttk.Label(self.google_drive_settings_frame, text="Akreditācijas fails:").grid(row=1, column=0, sticky=W, pady=2)
        ttk.Entry(self.google_drive_settings_frame, textvariable=self.google_drive_credentials_path).grid(row=1,
                                                                                                          column=1,
                                                                                                          sticky=EW,
                                                                                                          padx=5,
                                                                                                          pady=2)
        ttk.Button(self.google_drive_settings_frame, text="Pārlūkot...", command=self.browse_google_credentials).grid(
            row=1, column=2, padx=5)

        ttk.Label(self.google_drive_settings_frame, text="Token fails:").grid(row=2, column=0, sticky=W, pady=2)
        ttk.Entry(self.google_drive_settings_frame, textvariable=self.google_drive_token_path).grid(row=2, column=1,
                                                                                                    sticky=EW, padx=5,
                                                                                                    pady=2)
        ttk.Button(self.google_drive_settings_frame, text="Pārlūkot...", command=self.browse_google_token).grid(row=2,
                                                                                                                column=2,
                                                                                                                padx=5)

        ttk.Button(self.google_drive_settings_frame, text="Autorizēties", command=self.authorize_google_drive,
                   bootstyle=INFO).grid(row=3, column=0, columnspan=3, pady=5)
        self.google_drive_settings_frame.columnconfigure(1, weight=1)

        remote_storage_frame.columnconfigure(1, weight=1)

        # --- Automātiskās augšupielādes iestatījumi ---
        auto_upload_frame = ttk.LabelFrame(inner_automation_frame, text="Automātiskā augšupielāde", padding=10)
        auto_upload_frame.pack(fill=X, padx=5, pady=10)

        ttk.Checkbutton(auto_upload_frame, text="Iespējot automātisko augšupielādi pēc OCR",
                        variable=self.auto_upload_enabled,
                        command=self.toggle_auto_upload).grid(row=0, column=0, columnspan=2, sticky=W, pady=5)

        ttk.Label(auto_upload_frame, text="Augšupielādēt uz:").grid(row=1, column=0, sticky=W, pady=2)
        self.auto_upload_target_combo = ttk.Combobox(auto_upload_frame, textvariable=self.auto_upload_target,
                                                     values=["Local", "FTP", "SFTP", "Google Drive"], state="readonly")
        self.auto_upload_target_combo.grid(row=1, column=1, sticky=EW, padx=5, pady=2)

        auto_upload_frame.columnconfigure(1, weight=1)

        # --- Skenēto dokumentu saraksts (Automatizācijas cilnē) ---
        scanned_docs_frame = ttk.LabelFrame(inner_automation_frame, text="Skenētie dokumenti (uzraudzītā mapē)",
                                            padding=10)
        scanned_docs_frame.pack(fill=BOTH, expand=True, padx=5, pady=10)

        self.scanned_docs_listbox = tk.Listbox(scanned_docs_frame, selectmode=tk.SINGLE, exportselection=False)
        self.scanned_docs_listbox.pack(side=LEFT, fill="both", expand=True)

        scanned_docs_scrollbar = ttk.Scrollbar(scanned_docs_frame, orient="vertical",
                                               command=self.scanned_docs_listbox.yview)
        scanned_docs_scrollbar.pack(side=RIGHT, fill="y")
        self.scanned_docs_listbox.config(yscrollcommand=scanned_docs_scrollbar.set)

        self.scanned_docs_listbox.bind("<<ListboxSelect>>", self.on_scanned_doc_select)
        self.scanned_docs_listbox.bind("<Double-Button-1>", self.open_scanned_doc_location)

        # Ielādē saglabātos iestatījumus un atjaunina UI
        self.scan_folder_path.set(
            self.settings.get("scan_folder_path", os.path.join(os.path.expanduser("~"), "ScannedDocuments")))
        self.auto_scan_enabled.set(self.settings.get("auto_scan_enabled", False))
        self.remote_storage_type.set(self.settings.get("remote_storage_type", "Local"))
        self.ftp_host.set(self.settings.get("ftp_host", ""))
        self.ftp_port.set(self.settings.get("ftp_port", 21))
        self.ftp_user.set(self.settings.get("ftp_user", ""))
        self.ftp_pass.set(self.settings.get("ftp_pass", ""))
        self.ftp_remote_path.set(self.settings.get("ftp_remote_path", "/"))
        self.ftp_use_sftp.set(self.settings.get("ftp_use_sftp", False))
        self.google_drive_folder_id.set(self.settings.get("google_drive_folder_id", ""))
        self.google_drive_credentials_path.set(self.settings.get("google_drive_credentials_path", "credentials.json"))
        self.google_drive_token_path.set(self.settings.get("google_drive_token_path", "token.json"))
        self.auto_upload_enabled.set(self.settings.get("auto_upload_enabled", False))
        self.auto_upload_target.set(self.settings.get("auto_upload_target", "Local"))

        self.update_remote_storage_fields()  # Atjaunina redzamos laukus
        self.update_auto_scan_status()  # Atjaunina statusu pēc ielādes
        self.refresh_scanned_docs_list()  # Atjaunina skenēto dokumentu sarakstu

        if self.auto_scan_enabled.get():
            self.start_auto_scan()  # Sāk uzraudzību, ja bija ieslēgta

    def generate_qr_code(self):
        """Ģenerē QR kodu no ievadītā teksta un parāda to."""
        qr_text = self.qr_text_var.get()
        if not qr_text:
            messagebox.showwarning("Kļūda", "Lūdzu, ievadiet tekstu QR kodam.")
            return

        try:
            qr_img = qrcode.make(qr_text)
            qr_pil_img = qr_img.get_image()

            # Pielāgo izmēru, lai ietilptu kanvasā
            canvas_size = min(self.qr_canvas.winfo_width(), self.qr_canvas.winfo_height())
            if canvas_size == 1:  # Ja kanvass vēl nav inicializēts
                canvas_size = 200

            qr_pil_img = qr_pil_img.resize((canvas_size, canvas_size), Image.LANCZOS)
            self.qr_photo = ImageTk.PhotoImage(qr_pil_img)

            self.qr_canvas.delete("all")
            self.qr_canvas.create_image(0, 0, anchor="nw", image=self.qr_photo)
            self.qr_canvas.image = self.qr_photo  # Saglabā atsauci

            # Piedāvā saglabāt QR kodu
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG attēli", "*.png"), ("Visi faili", "*.*")],
                title="Saglabāt QR kodu kā"
            )
            if save_path:
                qr_img.save(save_path)
                messagebox.showinfo("QR kods", f"QR kods veiksmīgi saglabāts: {save_path}")

        except Exception as e:
            messagebox.showerror("Kļūda", f"Neizdevās ģenerēt QR kodu: {e}")

    def open_start_date_calendar(self):
        """Atver kalendāru sākuma datuma izvēlei."""
        self._open_calendar(self.start_date_var)

    def open_end_date_calendar(self):
        """Atver kalendāru beigu datuma izvēlei."""
        self._open_calendar(self.end_date_var)

    def _open_calendar(self, date_var):
        """Atver kalendāra logu un iestata izvēlēto datumu."""

        def set_date():
            date_var.set(cal.selection_get().strftime("%Y-%m-%d"))
            top.destroy()
            self.filter_pdf_list()  # Pēc datuma izvēles uzreiz filtrē

        top = Toplevel(self)
        top.title("Izvēlēties datumu")
        top.transient(self)
        top.grab_set()

        # Izmanto tkcalendar.Calendar tieši, lai izvairītos no ttkbootstrap savietojamības problēmām
        # Vai arī nodrošina, ka Calendar tiek inicializēts ar pareizo stilu
        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd',
                       font="TkDefaultFont", background="#222222",
                       normalbackground="#222222", foreground="white",
                       normalforeground="white", headersbackground="#333333",
                       headersforeground="white", selectbackground="#007bff",
                       selectforeground="white", bordercolor="#333333",
                       othermonthforeground="#666666", othermonthbackground="#1a1a1a",
                       othermonthweforeground="#999999", othermonthwebackground="#1a1a1a",
                       weekendbackground="#2a2a2a", weekendforeground="white",
                       tooltipbackground="#444444", tooltipforeground="white")
        cal.pack(padx=10, pady=10)

        ttk.Button(top, text="Apstiprināt", command=set_date).pack(pady=5)
        top.update_idletasks()  # Atjaunina loga izmērus
        top.geometry(
            f"+{self.winfo_x() + self.winfo_width() // 2 - top.winfo_width() // 2}+{self.winfo_y() + self.winfo_height() // 2 - top.winfo_height() // 2}")

    def filter_pdf_list(self, event=None):
        """Filtrē PDF sarakstu, pamatojoties uz meklēšanas terminu un datumu diapazonu."""
        search_term = self.search_var.get().lower()
        start_date_str = self.start_date_var.get()
        end_date_str = self.end_date_var.get()

        # Filtrē pašreizējās mapes saturu
        filtered_contents = []
        for item in self.current_folder["contents"]:
            match_search = True
            match_date = True

            # Meklēšana
            if search_term:
                if item["type"] == "file":
                    if search_term not in item['filepath'].lower() and search_term not in item[
                        'doc_id'].lower() and search_term not in item['name'].lower():
                        match_search = False
                elif item["type"] == "folder":
                    if search_term not in item['name'].lower():
                        match_search = False

            # Datuma filtrēšana (tikai failiem)
            if item["type"] == "file" and (start_date_str or end_date_str):
                try:
                    entry_date = datetime.datetime.strptime(item['date'].split(" ")[0], "%Y-%m-%d").date()
                    if start_date_str:
                        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
                        if entry_date < start_date:
                            match_date = False
                    if end_date_str:
                        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
                        if entry_date > end_date:
                            match_date = False
                except ValueError:
                    pass  # Ignorē nederīgus datuma formātus

            if match_search and match_date:
                filtered_contents.append(item)

        self.pdf_listbox.delete(0, tk.END)
        for item in filtered_contents:
            if item["type"] == "file":
                self.pdf_listbox.insert(tk.END, f"📄 {item['doc_id']} - {item['name']} ({item['date']})")
            elif item["type"] == "folder":
                self.pdf_listbox.insert(tk.END, f"📁 {item['name']}")

    def clear_pdf_filters(self):
        """Notīra visus PDF saraksta filtrus."""
        self.search_var.set("")
        self.start_date_var.set("")
        self.end_date_var.set("")
        self.refresh_pdf_list()

    def refresh_pdf_list(self):
        """Atjaunina PDF sarakstu, parādot pašreizējās mapes saturu."""
        self.pdf_listbox.delete(0, tk.END)
        for item in self.current_folder["contents"]:
            if item["type"] == "file":
                self.pdf_listbox.insert(tk.END, f"📄 {item['doc_id']} - {item['name']} ({item['date']})")
            elif item["type"] == "folder":
                self.pdf_listbox.insert(tk.END, f"📁 {item['name']}")
        self.update_path_label()
        self.update_back_button_state()
        self.save_pdf_archive()  # Saglabā izmaiņas failu sistēmā

    def update_path_label(self):
        """Atjaunina ceļa etiķeti, lai parādītu pašreizējo mapes ceļu."""
        path_parts = []
        temp_folder = self.current_folder
        # Pārliecināmies, ka mēs neejam tālāk par saknes mapi
        while temp_folder != self.internal_file_system and temp_folder.get("parent") is not None:
            path_parts.insert(0, temp_folder["name"])
            temp_folder = temp_folder["parent"]
        self.current_path_label.config(text="/".join([""] + path_parts) if path_parts else "/")

    def update_back_button_state(self):
        """Atjaunina pogas 'Atpakaļ' stāvokli."""
        if self.current_folder == self.internal_file_system:
            self.back_button.config(state=DISABLED)
        else:
            self.back_button.config(state=NORMAL)

    def go_back_folder(self):
        """Atgriežas uz iepriekšējo mapi."""
        if self.current_folder.get("parent"):
            self.current_folder = self.current_folder["parent"]
            self.refresh_pdf_list()

    def open_selected_item(self, event=None):
        """Atver atlasīto vienumu (failu vai mapi)."""
        selection = self.pdf_listbox.curselection()
        if not selection:
            messagebox.showwarning("Nav atlasīts", "Lūdzu, atlasiet vienumu no saraksta.")
            return

        index = selection[0]
        selected_item = self.current_folder["contents"][index]

        if selected_item["type"] == "file":
            filepath = selected_item['filepath']
            if os.path.exists(filepath):
                try:
                    os.startfile(filepath)  # Atver failu ar noklusējuma programmu
                except Exception as e:
                    messagebox.showerror("Kļūda", f"Neizdevās atvērt failu:\n{e}")
            else:
                messagebox.showwarning("Fails nav atrasts",
                                       "Fails nav atrasts norādītajā vietā. Iespējams, tas ir pārvietots vai dzēsts.")
        elif selected_item["type"] == "folder":
            self.current_folder = selected_item
            self.refresh_pdf_list()

    def on_pdf_select(self, event=None):
        """Apstrādā PDF faila atlasi sarakstā (pašlaik nedara neko)."""
        pass

    def open_pdf_location(self):
        """Atver mapes atrašanās vietu, kurā atrodas atlasītais PDF fails (sistēmā)."""
        selection = self.pdf_listbox.curselection()
        if not selection:
            messagebox.showwarning("Nav atlasīts", "Lūdzu, atlasiet failu no saraksta.")
            return

        index = selection[0]
        selected_item = self.current_folder["contents"][index]

        if selected_item["type"] == "file":
            filepath = selected_item['filepath']
            if os.path.exists(filepath):
                try:
                    # Atver mapi un iezīmē failu
                    if os.name == 'nt':  # Windows
                        os.startfile(os.path.dirname(filepath))
                    elif os.name == 'posix':  # macOS, Linux
                        import sys
                        if sys.platform == 'darwin':  # macOS
                            subprocess.Popen(['open', '-R', filepath])
                        else:  # Linux
                            subprocess.Popen(['xdg-open', os.path.dirname(filepath)])
                except Exception as e:
                    messagebox.showerror("Kļūda", f"Neizdevās atvērt faila atrašanās vietu:\n{e}")
            else:
                messagebox.showwarning("Fails nav atrasts", "Fails nav atrasts norādītajā vietā.")
        else:
            messagebox.showwarning("Nav fails", "Atlasītais vienums nav fails.")

    def delete_selected_item(self):
        """Dzēš atlasītos vienumus (failus vai mapes) no iekšējās failu sistēmas."""
        selection = self.pdf_listbox.curselection()
        if not selection:
            messagebox.showwarning("Nav atlasīts", "Lūdzu, atlasiet vienumu(s), ko dzēst.")
            return

        selected_indices = sorted(list(selection), reverse=True)
        items_to_delete = [self.current_folder["contents"][i] for i in selected_indices]

        confirm_msg = f"Vai tiešām vēlaties dzēst {len(items_to_delete)} atlasītos vienumus?\n"
        confirm_msg += "Ņemiet vērā, ka faili tiks dzēsti arī no diska!"

        if messagebox.askyesno("Dzēst vienumus", confirm_msg):
            for index in selected_indices:
                item = self.current_folder["contents"][index]
                if item["type"] == "file":
                    try:
                        if os.path.exists(item["filepath"]):
                            os.remove(item["filepath"])
                        # Noņem no saraksta tikai pēc veiksmīgas dzēšanas no diska
                        self.current_folder["contents"].pop(index)
                    except Exception as e:
                        messagebox.showerror("Kļūda", f"Neizdevās dzēst failu {item['name']}:\n{e}")
                elif item["type"] == "folder":
                    # Rekursīvi dzēš mapes saturu no diska
                    if self._delete_folder_contents_from_disk(item):
                        # Noņem no saraksta tikai pēc veiksmīgas dzēšanas no diska
                        self.current_folder["contents"].pop(index)
                    else:
                        messagebox.showwarning("Dzēšanas kļūda",
                                               f"Neizdevās pilnībā dzēst mapi {item['name']} no diska.")

            self.refresh_pdf_list()
            messagebox.showinfo("Dzēsts", "Atlasītie vienumi veiksmīgi dzēsti.")

    def _delete_folder_contents_from_disk(self, folder_node):
        """Rekursīvi dzēš mapes saturu no diska."""
        success = True
        for item in folder_node["contents"]:
            if item["type"] == "file":
                try:
                    if os.path.exists(item["filepath"]):
                        os.remove(item["filepath"])
                except Exception as e:
                    messagebox.showwarning("Dzēšanas kļūda", f"Neizdevās dzēst failu {item['name']} no diska: {e}")
                    success = False
            elif item["type"] == "folder":
                if not self._delete_folder_contents_from_disk(item):
                    success = False
        # Pēc satura dzēšanas mēģina dzēst pašu mapi, ja tā ir tukša
        try:
            # Pārbauda, vai mape ir tukša pirms dzēšanas
            if os.path.exists(os.path.join(self.default_save_path, folder_node["name"])):
                if not os.listdir(os.path.join(self.default_save_path, folder_node["name"])):
                    os.rmdir(os.path.join(self.default_save_path, folder_node["name"]))
        except Exception as e:
            messagebox.showwarning("Dzēšanas kļūda", f"Neizdevās dzēst mapi {folder_node['name']} no diska: {e}")
            success = False
        return success


    def send_selected_pdfs_by_email(self):
        """Nosūta atlasītos PDF failus, izmantojot SMTP iestatījumus."""
        selection = self.pdf_listbox.curselection()
        if not selection:
            messagebox.showwarning("Nav atlasīts", "Lūdzu, atlasiet PDF failu(s), ko nosūtīt e-pastā.")
            return

        selected_filepaths = []
        for index in selection:
            item = self.current_folder["contents"][index]
            if item["type"] == "file":
                filepath = item['filepath']
                if os.path.exists(filepath):
                    selected_filepaths.append(filepath)
                else:
                    messagebox.showwarning("Fails nav atrasts",
                                           f"Fails '{os.path.basename(filepath)}' nav atrasts un netiks pievienots.")
            else:
                messagebox.showwarning("Nav fails", f"Vienums '{item['name']}' nav fails un netiks pievienots.")

        if not selected_filepaths:
            messagebox.showwarning("Nav failu", "Neviens derīgs fails nav atlasīts sūtīšanai.")
            return

        # Dialogs e-pasta adresāta izvēlei
        to_email_dialog = Toplevel(self)
        to_email_dialog.title("Nosūtīt e-pastu")
        to_email_dialog.transient(self)
        to_email_dialog.grab_set()

        ttk.Label(to_email_dialog, text="Nosūtīt uz:").pack(padx=10, pady=5)

        default_to_email = self.settings.get("to_email", "")
        to_email_var_dialog = tk.StringVar(value=default_to_email)

        ttk.Entry(to_email_dialog, textvariable=to_email_var_dialog, width=50).pack(padx=10, pady=5)

        def confirm_send():
            to_address = to_email_var_dialog.get()
            if not to_address:
                messagebox.showwarning("Trūkst adresāta", "Lūdzu, ievadiet e-pasta adresātu.")
                return
            to_email_dialog.destroy()
            self._send_email_with_attachments(selected_filepaths, to_address)

        ttk.Button(to_email_dialog, text="Nosūtīt", command=confirm_send, bootstyle=PRIMARY).pack(pady=10)
        ttk.Button(to_email_dialog, text="Atcelt", command=to_email_dialog.destroy, bootstyle=SECONDARY).pack(pady=5)

    def on_select(event):
        global selected_item  # Padara mainīgo globālu
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            selected_item = event.widget.get(index)  # Iegūst izvēlēto elementu

    def _send_email_with_attachments(self, filepaths, to_address):
        """Faktiski nosūta e-pastu ar pielikumiem."""
        smtp_server = self.settings.get("smtp_server")
        smtp_port = self.settings.get("smtp_port")
        email_user = self.settings.get("email_user")
        email_pass = self.settings.get("email_pass")
        from_email = self.settings.get("from_email")
        use_ssl = self.settings.get("use_ssl", True)
        email_subject = self.settings.get("email_subject", "OCR PDF dokumenti")
        email_body_plain = self.settings.get("email_body_plain",
                                             "Sveiki,\n\nPielikumā atradīsiet OCR apstrādātos PDF dokumentus.\n\nAr cieņu,\nJūsu OCR PDF App")
        email_body_html = self.settings.get("email_body_html",
                                            "<html><body><p>Sveiki,</p><p>Pielikumā atradīsiet OCR apstrādātos PDF dokumentus.</p><p>Ar cieņu,<br/>Jūsu OCR PDF App</p></body></html>")

        if not all([smtp_server, smtp_port, email_user, email_pass, from_email, to_address]):
            messagebox.showwarning("E-pasta iestatījumi",
                                   "Lūdzu, konfigurējiet e-pasta iestatījumus (SMTP serveris, ports, lietotājvārds, parole, sūtītāja un saņēmēja adreses) Iestatījumu logā.")
            return

        msg = MIMEMultipart('alternative')
        msg['From'] = from_email
        msg['To'] = to_address
        msg['Subject'] = email_subject

        part1 = MIMEText(email_body_plain, 'plain')
        msg.attach(part1)

        part2 = MIMEText(email_body_html, 'html')
        msg.attach(part2)

        for filepath in filepaths:
            try:
                filename = os.path.basename(filepath)
                with open(filepath, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                # Labojums: Pareizi kodē faila nosaukumu Content-Disposition galvenē
                part.add_header("Content-Disposition", f"attachment; filename*=UTF-8''{urllib.parse.quote(filename)}")
                msg.attach(part)
            except Exception as e:
                messagebox.showwarning("Pielikuma kļūda", f"Neizdevās pievienot failu {filename}: {e}")
                continue

        try:
            if use_ssl:
                server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            else:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()

            server.login(email_user, email_pass)
            text = msg.as_string()
            server.sendmail(from_email, to_address, text)
            server.quit()
            messagebox.showinfo("E-pasts", "E-pasts veiksmīgi nosūtīts!")
        except Exception as e:
            messagebox.showerror("E-pasta sūtīšanas kļūda", f"Neizdevās nosūtīt e-pastu:\n{e}")

    def show_pdf_context_menu(self, event):
        """Parāda konteksta izvēlni PDF saraksta elementiem."""
        try:
            # Pārliecināmies, ka tiek atlasīts elements, uz kura uzklikšķināts
            self.pdf_listbox.selection_clear(0, tk.END)
            index = self.pdf_listbox.nearest(event.y)
            self.pdf_listbox.selection_set(index)
            self.pdf_listbox.activate(index)

            # Iegūst atlasīto vienumu
            selected_item = self.current_folder["contents"][index]

            context_menu = tk.Menu(self.pdf_listbox, tearoff=0)
            context_menu.add_command(label="Atvērt", command=lambda: self.open_selected_item())
            context_menu.add_command(label="Atvērt mapē (sistēmā)", command=lambda: self.open_pdf_location())
            context_menu.add_command(label="Nosūtīt e-pastā", command=lambda: self.send_selected_pdfs_by_email())
            context_menu.add_separator()
            context_menu.add_command(label="Dzēst", command=lambda: self.delete_selected_item())
            context_menu.add_command(label="Pārdēvēt", command=lambda: self.rename_selected_item())
            context_menu.add_command(label="Pārvietot uz...", command=lambda: self.move_selected_items())
            context_menu.add_command(label="Saglabāt kā Word", command=lambda: self.save_as_word())
            context_menu.add_command(label="Pievienot paroli",
                                     command=lambda: self.add_password_to_pdf(selected_item['filepath']))
            context_menu.add_command(label="Noņemt paroli",
                                     command=lambda: self.remove_password_from_pdf(selected_item['filepath']))
            context_menu.add_command(label="Mainīt paroli",
                                     command=lambda: self.change_password_of_pdf(selected_item['filepath']))

            context_menu.post(event.x_root, event.y_root)
        except Exception:
            pass  # Ja nav atlasīts nekas, ignorē

    def create_new_folder_internal(self):
        """Izveido jaunu mapi iekšējā failu sistēmā."""
        new_folder_name = simpledialog.askstring("Jauna mape", "Ievadiet jaunās mapes nosaukumu:", parent=self)
        if new_folder_name:
            # Pārbauda, vai mape ar šādu nosaukumu jau eksistē
            for item in self.current_folder["contents"]:
                if item["type"] == "folder" and item["name"] == new_folder_name:
                    messagebox.showwarning("Mape jau eksistē",
                                           f"Mape ar nosaukumu '{new_folder_name}' jau eksistē šajā mapē.")
                    return

            new_folder = {"type": "folder", "name": new_folder_name, "contents": [], "parent": self.current_folder}
            self.current_folder["contents"].append(new_folder)
            self.refresh_pdf_list()
            messagebox.showinfo("Mape izveidota", f"Mape '{new_folder_name}' veiksmīgi izveidota.")

    def move_selected_items(self):
        """Pārvieto atlasītos vienumus uz citu mapi iekšējā failu sistēmā."""
        selection = self.pdf_listbox.curselection()
        if not selection:
            messagebox.showwarning("Nav atlasīts", "Lūdzu, atlasiet vienumu(s), ko pārvietot.")
            return

        # Izveido mapju izvēles dialogu
        target_folder = self._select_folder_dialog(self.internal_file_system)

        if target_folder:
            moved_count = 0
            # Jāveido kopija, jo saraksts mainīsies dzēšot elementus
            items_to_move = [self.current_folder["contents"][i] for i in sorted(list(selection), reverse=True)]

            # Pārbauda, vai mērķa mape nav pati pašreizējā mape
            if target_folder == self.current_folder:
                messagebox.showinfo("Pārvietošana", "Vienumi jau atrodas izvēlētajā mapē.")
                return

            for item in items_to_move:
                # Pārbauda, vai mērķa mape nav pati vienums vai tās apakšmape
                if item["type"] == "folder" and self._is_descendant(target_folder, item):
                    messagebox.showwarning("Kļūda", f"Mapi '{item['name']}' nevar pārvietot uz tās paša apakšmapi.")
                    continue

                # Pārbauda, vai mērķa mapē jau nav vienums ar tādu pašu nosaukumu
                # Pārvietojot failus, jāpārliecinās, ka mērķa mapē nav faila ar tādu pašu nosaukumu
                # Ja ir, varētu piedāvāt pārdēvēt vai ignorēt
                name_exists = False
                for existing_item in target_folder["contents"]:
                    if existing_item["name"] == item["name"] and existing_item["type"] == item["type"]:
                        name_exists = True
                        break

                if name_exists:
                    response = messagebox.askyesno("Nosaukums jau eksistē",
                                                   f"Mērķa mapē jau eksistē vienums ar nosaukumu '{item['name']}'. Vai vēlaties to pārdēvēt?")
                    if response:
                        new_name = simpledialog.askstring("Pārdēvēt",
                                                          f"Ievadiet jauno nosaukumu vienumam '{item['name']}':",
                                                          parent=self)
                        if new_name:
                            item["name"] = new_name
                        else:
                            continue  # Atcelt pārvietošanu šim vienumam
                    else:
                        continue  # Atcelt pārvietošanu šim vienumam

                # Noņem vienumu no pašreizējās mapes
                self.current_folder["contents"].pop(self.drag_data["index"])
                # Pievieno vienumu mērķa mapei
                target_folder["contents"].append(item)
                item["parent"] = target_folder  # Atjaunina vecāka atsauci
                moved_count += 1

            if moved_count > 0:
                self.refresh_pdf_list()
                messagebox.showinfo("Pārvietots", f"Veiksmīgi pārvietoti {moved_count} vienumi.")
            else:
                messagebox.showinfo("Pārvietošana", "Neviens vienums netika pārvietots.")
        else:
            messagebox.showinfo("Pārvietošana", "Mērķa mape netika izvēlēta.")

    def _select_folder_dialog(self, root_folder):
        """Atver dialogu mapes izvēlei iekšējā failu sistēmā."""
        dialog = Toplevel(self)
        dialog.title("Izvēlēties mapi")
        dialog.transient(self)
        dialog.grab_set()

        tree = ttk.Treeview(dialog, selectmode="browse")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        selected_folder = None

        def on_select():
            nonlocal selected_folder
            item_id = tree.selection()
            if item_id:
                # Piekļūst mapes objektam, kas saglabāts kā vērtība
                # tree.item(item_id, "values") atgriež tuple, kurā pirmais elements ir mūsu saglabātais dict
                item_data = tree.item(item_id, "values")
                if item_data and isinstance(item_data[0], dict) and item_data[0].get("type") == "folder":
                    selected_folder = item_data[0]
                    dialog.destroy()
                else:
                    messagebox.showwarning("Nederīga atlase", "Lūdzu, atlasiet mapi, nevis failu.")
            else:
                messagebox.showwarning("Nav atlasīts", "Lūdzu, atlasiet mapi.")

        ttk.Button(dialog, text="Izvēlēties", command=on_select).pack(pady=5)
        ttk.Button(dialog, text="Atcelt", command=dialog.destroy).pack(pady=5)

        def populate_treeview_with_data(treeview, parent_node_id, folder_data):
            # Pievieno mapes objektu kā vērtību, lai to varētu atgūt on_select
            node_id = treeview.insert(parent_node_id, "end", text=folder_data["name"], open=False, tags=("folder",),
                                      values=(folder_data,))  # Šeit saglabājam visu mapes dict kā vērtību
            for item in folder_data["contents"]:
                if item["type"] == "folder":
                    populate_treeview_with_data(treeview, node_id, item)
                # Failus nepievienojam, jo dialogs ir paredzēts tikai mapju izvēlei

        # Ievieto saknes mapi un aizpilda to
        populate_treeview_with_data(tree, "", self.internal_file_system)

        self.wait_window(dialog)
        return selected_folder

    def _is_descendant(self, potential_descendant, potential_ancestor):
        """Pārbauda, vai potential_descendant ir potential_ancestor apakšmape."""
        current = potential_descendant
        while current.get("parent"):
            if current["parent"] == potential_ancestor:
                return True
            current = current["parent"]
        return False

    def rename_selected_item(self):
        """Pārdēvē atlasīto vienumu (failu vai mapi)."""
        selection = self.pdf_listbox.curselection()
        if not selection:
            messagebox.showwarning("Nav atlasīts", "Lūdzu, atlasiet vienumu, ko pārdēvēt.")
            return

        index = selection[0]
        item = self.current_folder["contents"][index]

        old_name = item["name"]
        new_name = simpledialog.askstring("Pārdēvēt", f"Ievadiet jauno nosaukumu vienumam '{old_name}':",
                                          initialvalue=old_name, parent=self)

        if new_name and new_name != old_name:
            # Pārbauda, vai jaunais nosaukums jau eksistē
            for existing_item in self.current_folder["contents"]:
                if existing_item["name"] == new_name and existing_item["type"] == item["type"]:
                    messagebox.showwarning("Nosaukums jau eksistē",
                                           f"Vienums ar nosaukumu '{new_name}' jau eksistē šajā mapē.")
                    return

            item["name"] = new_name
            # Ja tas ir fails, jāatjaunina arī filepath, ja tas ir atkarīgs no nosaukuma
            if item["type"] == "file":
                # Šeit varētu būt sarežģītāk, ja faili tiek saglabāti ar nosaukumu, kas ietver doc_id
                # Vienkāršības labad pieņemam, ka filepath paliek nemainīgs, ja vien nav nepieciešams pārdēvēt arī fizisko failu
                # Ja nepieciešams pārdēvēt arī fizisko failu, tad:
                # old_filepath = item["filepath"]
                # new_filepath = os.path.join(os.path.dirname(old_filepath), new_name)
                # try:
                #     os.rename(old_filepath, new_filepath)
                #     item["filepath"] = new_filepath
                # except Exception as e:
                #     messagebox.showerror("Kļūda", f"Neizdevās pārdēvēt fizisko failu: {e}")
                #     return
                pass  # Pašlaik fiziskais fails netiek pārdēvēts, tikai loģiskais nosaukums

            self.refresh_pdf_list()
            messagebox.showinfo("Pārdēvēts", f"Vienums veiksmīgi pārdēvēts uz '{new_name}'.")

    def save_as_word(self):
        """
        Saglabā atlasītos PDF failus kā Word dokumentus, izmantojot OCR tekstu.
        """
        selection = self.pdf_listbox.curselection()
        if not selection:
            messagebox.showwarning("Nav atlasīts", "Lūdzu, atlasiet PDF failu(s), ko saglabāt kā Word.")
            return

        selected_items = []
        for index in selection:
            item = self.current_folder["contents"][index]
            if item["type"] == "file":
                selected_items.append(item)
            else:
                messagebox.showwarning("Nav fails", f"Vienums '{item['name']}' nav fails un netiks apstrādāts.")

        if not selected_items:
            messagebox.showwarning("Nav failu", "Neviens derīgs fails nav atlasīts saglabāšanai.")
            return

        for item in selected_items:
            pdf_filepath = item['filepath']
            doc_id = item['doc_id']
            doc_name = item['name']

            # Atrod OCR rezultātus pēc doc_id
            ocr_text = ""
            # Pārbauda, vai OCR rezultāti jau ir atmiņā
            found_ocr_in_memory = False
            for ocr_res in self.ocr_results:
                if ocr_res and ocr_res.get("doc_id") == doc_id:
                    ocr_text = ocr_res["full_text"]
                    found_ocr_in_memory = True
                    break

            if not found_ocr_in_memory:
                # Ja OCR rezultāti nav pieejami atmiņā, mēģina veikt OCR no jauna
                try:
                    # PyPDF2 varētu būt nepieciešams, lai izvilktu tekstu no PDF
                    # Bet, ja PDF ir tikai attēls, tad jāizmanto pytesseract
                    # Vienkāršības labad pieņemam, ka varam veikt OCR tieši no attēla, ja PDF ir attēls
                    # Reālā situācijā varētu būt nepieciešams izmantot `pdf2image` bibliotēku, lai konvertētu PDF lapas uz attēliem
                    # vai `PyPDF2` (vai `pypdf`) lai izvilktu tekstu no teksta PDF.
                    # Šeit mēs pieņemam, ka PDF ir attēls vai ka varam veikt OCR no tā.
                    img = Image.open(pdf_filepath)
                    ocr_text = pytesseract.image_to_string(img, lang="lav+eng")  # Pieņemam latviešu un angļu
                except Exception as e:
                    messagebox.showwarning("OCR kļūda", f"Neizdevās iegūt tekstu no {doc_name} priekš Word: {e}")
                    continue

            if not ocr_text:
                messagebox.showwarning("Nav teksta", f"Nav atrasts teksts, ko saglabāt Word dokumentā no {doc_name}.")
                continue

            doc = Document()
            doc.add_heading(f"Dokuments: {doc_name}", level=1)
            doc.add_paragraph(f"Dokumenta ID: {doc_id}")
            doc.add_paragraph(f"Oriģinālais fails: {pdf_filepath}")
            doc.add_paragraph("\n" + ocr_text)

            default_word_filename = os.path.splitext(doc_name)[0] + ".docx"
            save_path = filedialog.asksaveasfilename(
                defaultextension=".docx",
                filetypes=[("Word dokumenti", "*.docx")],
                initialdir=os.path.dirname(pdf_filepath),
                initialfile=default_word_filename,
                title=f"Saglabāt {doc_name} kā Word"
            )

            if save_path:
                try:
                    doc.save(save_path)
                    messagebox.showinfo("Saglabāts", f"Dokuments veiksmīgi saglabāts kā Word: {save_path}")
                except Exception as e:
                    messagebox.showerror("Saglabāšanas kļūda", f"Neizdevās saglabāt Word dokumentu: {e}")

    def drag_start(self, event):
        """Sāk vilkšanas operāciju."""
        selection = self.pdf_listbox.curselection()
        if selection:
            self.drag_data["item"] = self.current_folder["contents"][selection[0]]
            self.drag_data["index"] = selection[0]
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
            # Pievieno vizuālu atgriezenisko saiti (piem., maina kursoru)
            self.pdf_listbox.config(cursor="fleur")

    def drag_motion(self, event):
        """Apstrādā vilkšanas kustību."""
        # Šeit varētu pievienot vizuālu vilkšanas indikatoru
        pass

    def drag_drop(self, event):
        """Apstrādā nomešanas operāciju."""
        self.pdf_listbox.config(cursor="arrow")  # Atjauno kursoru
        if self.drag_data["item"]:
            target_index = self.pdf_listbox.nearest(event.y)
            if target_index is not None:
                target_item = self.current_folder["contents"][target_index]

                if target_item["type"] == "folder":
                    # Mēģina pārvietot uz mapi
                    if self.drag_data["item"] == target_item:
                        messagebox.showwarning("Pārvietošana", "Nevar pārvietot vienumu uz pašu sevi.")
                        self.drag_data["item"] = None
                        return

                    if self.drag_data["item"]["type"] == "folder" and self._is_descendant(target_item,
                                                                                          self.drag_data["item"]):
                        messagebox.showwarning("Kļūda", "Mapi nevar pārvietot uz tās paša apakšmapi.")
                        self.drag_data["item"] = None
                        return

                    # Pārbauda, vai mērķa mapē jau nav vienums ar tādu pašu nosaukumu
                    name_exists = False
                    for existing_item in target_item["contents"]:
                        if existing_item["name"] == self.drag_data["item"]["name"] and existing_item["type"] == \
                                self.drag_data["item"]["type"]:
                            name_exists = True
                            break

                    if name_exists:
                        response = messagebox.askyesno("Nosaukums jau eksistē",
                                                       f"Mērķa mapē jau eksistē vienums ar nosaukumu '{self.drag_data['item']['name']}'. Vai vēlaties to pārdēvēt?")
                        if response:
                            new_name = simpledialog.askstring("Pārdēvēt",
                                                              f"Ievadiet jauno nosaukumu vienumam '{self.drag_data['item']['name']}':",
                                                              parent=self)
                            if new_name:
                                self.drag_data["item"]["name"] = new_name
                            else:
                                self.drag_data["item"] = None  # Atcelt pārvietošanu
                                return
                        else:
                            self.drag_data["item"] = None  # Atcelt pārvietošanu
                            return

                    # Noņem no pašreizējās mapes
                    self.current_folder["contents"].pop(self.drag_data["index"])
                    # Pievieno mērķa mapei
                    target_item["contents"].append(self.drag_data["item"])
                    self.drag_data["item"]["parent"] = target_item  # Atjaunina vecāka atsauci
                    messagebox.showinfo("Pārvietots",
                                        f"Vienums '{self.drag_data['item']['name']}' pārvietots uz '{target_item['name']}'.")
                    self.refresh_pdf_list()

                elif target_item["type"] == "file":
                    # Mēģina pārvietot starp failiem (pārvietošana tajā pašā mapē)
                    if self.drag_data["item"]["type"] == "file":
                        # Pārvieto failu sarakstā
                        current_item = self.current_folder["contents"].pop(self.drag_data["index"])
                        self.current_folder["contents"].insert(target_index, current_item)
                        messagebox.showinfo("Pārvietots", f"Vienums '{current_item['name']}' pārvietots sarakstā.")
                        self.refresh_pdf_list()
                    else:
                        messagebox.showwarning("Pārvietošana", "Mapi nevar pārvietot uz failu.")
            else:
                # Nomešana tukšā vietā vai ārpus saraksta (varētu nozīmēt pārvietošanu uz pašreizējo mapi)
                # Šis scenārijs jau ir apstrādāts, ja vienums tiek nomests uz mapi
                pass
            self.drag_data["item"] = None  # Notīra vilkšanas datus

    def configure_grid(self):
        """Konfigurē galvenā loga režģa izkārtojumu (pašlaik netiek izmantots, jo ir Notebook)."""
        # Galvenais logs tagad izmanto Notebook, tāpēc rindu/kolonnu konfigurācija ir mazāk svarīga šeit
        # Tā vietā, katra cilne konfigurē savu iekšējo izkārtojumu
        pass

    def _show_folder_selection_dialog(self, suggested_category):
        """
        Parāda dialoga logu, lai lietotājs varētu izvēlēties vai izveidot mapi
        pirms PDF saglabāšanas.
        """
        dialog = Toplevel(self)
        dialog.title("Izvēlēties saglabāšanas mapi")
        dialog.transient(self)
        dialog.grab_set()

        selected_node = None  # Šeit tiks saglabāts izvēlētais mapes mezgls

        # Pašreizējā ceļa attēlošana
        current_path_label = ttk.Label(dialog, text="Pašreizējā mape: /")
        current_path_label.pack(fill="x", padx=10, pady=5)

        # Mapju saraksts
        folder_list_frame = ttk.Frame(dialog)
        folder_list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        folder_listbox = tk.Listbox(folder_list_frame, selectmode=tk.SINGLE, exportselection=False)
        folder_listbox.pack(side=tk.LEFT, fill="both", expand=True)

        folder_scrollbar = ttk.Scrollbar(folder_list_frame, orient="vertical", command=folder_listbox.yview)
        folder_scrollbar.pack(side=tk.RIGHT, fill="y")
        folder_listbox.config(yscrollcommand=folder_scrollbar.set)

        # Iekšējā funkcija, lai atjauninātu sarakstu
        current_dialog_folder = self.internal_file_system  # Sāk ar saknes mapi dialogā

        def update_folder_listbox():
            folder_listbox.delete(0, tk.END)
            # Pievieno ".." opciju, ja nav saknes mapē
            if current_dialog_folder != self.internal_file_system:
                folder_listbox.insert(tk.END, "📁 .. (Atpakaļ)")

            # Pievieno mapes
            for item in current_dialog_folder["contents"]:
                if item["type"] == "folder":
                    folder_listbox.insert(tk.END, f"📁 {item['name']}")

            # Atjaunina ceļa etiķeti
            path_parts = []
            temp_folder = current_dialog_folder
            while temp_folder != self.internal_file_system:
                path_parts.insert(0, temp_folder["name"])
                temp_folder = temp_folder["parent"]
            current_path_label.config(text="Pašreizējā mape: /" + "/".join(path_parts))

        def on_folder_select(event):
            nonlocal current_dialog_folder
            selection = folder_listbox.curselection()
            if selection:
                index = selection[0]
                item_text = folder_listbox.get(index)

                if item_text.startswith("📁 .."):  # Atpakaļ
                    if current_dialog_folder.get("parent"):
                        current_dialog_folder = current_dialog_folder["parent"]
                        update_folder_listbox()
                else:  # Mape
                    folder_name = item_text[2:].strip()  # Noņem "📁 "
                    for item in current_dialog_folder["contents"]:
                        if item["type"] == "folder" and item["name"] == folder_name:
                            current_dialog_folder = item
                            update_folder_listbox()
                            break

        folder_listbox.bind("<Double-Button-1>", on_folder_select)

        # Ieteiktās kategorijas rāmis
        suggested_frame = ttk.LabelFrame(dialog, text="Ieteiktā kategorija", padding=5)
        suggested_frame.pack(fill="x", padx=10, pady=5)

        suggested_label = ttk.Label(suggested_frame, text=f"Programma iesaka: {suggested_category}")
        suggested_label.pack(side=tk.LEFT, padx=5)

        def use_suggested():
            nonlocal selected_node
            selected_node = self.get_or_create_folder(suggested_category)
            dialog.destroy()

        ttk.Button(suggested_frame, text="Izmantot ieteikto", command=use_suggested, bootstyle=SUCCESS).pack(
            side=tk.RIGHT, padx=5)

        # Pogas
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill="x", padx=10, pady=5)

        def create_new_folder_in_dialog():
            new_name = simpledialog.askstring("Jauna mape", "Ievadiet jaunās mapes nosaukumu:", parent=dialog)
            if new_name:
                # Pārbauda, vai mape ar šādu nosaukumu jau eksistē pašreizējā dialoga mapē
                for item in current_dialog_folder["contents"]:
                    if item["type"] == "folder" and item["name"] == new_name:
                        messagebox.showwarning("Mape jau eksistē",
                                               f"Mape ar nosaukumu '{new_name}' jau eksistē šajā mapē.", parent=dialog)
                        return
                new_folder = {"type": "folder", "name": new_name, "contents": [], "parent": current_dialog_folder}
                current_dialog_folder["contents"].append(new_folder)
                update_folder_listbox()
                self.save_pdf_archive()  # Saglabā izmaiņas arhīvā

        ttk.Button(button_frame, text="Izveidot jaunu mapi", command=create_new_folder_in_dialog).pack(side=tk.LEFT,
                                                                                                       padx=2)

        def confirm_selection():
            nonlocal selected_node
            selected_node = current_dialog_folder  # Izvēlētā mape ir pašreizējā dialoga mape
            dialog.destroy()

        ttk.Button(button_frame, text="Apstiprināt izvēli", command=confirm_selection).pack(side=tk.LEFT, padx=2)

        update_folder_listbox()  # Atjaunina sarakstu, kad logs tiek atvērts
        self.wait_window(dialog)
        return selected_node

        def update_folder_listbox():
            folder_listbox.delete(0, tk.END)
            # Pievieno ".." opciju, ja nav saknes mapē
            if current_dialog_folder != self.internal_file_system:
                folder_listbox.insert(tk.END, "📁 .. (Atpakaļ)")

            # Pievieno mapes
            for item in current_dialog_folder["contents"]:
                if item["type"] == "folder":
                    folder_listbox.insert(tk.END, f"📁 {item['name']}")

            # Atjaunina ceļa etiķeti
            path_parts = []
            temp_folder = current_dialog_folder
            while temp_folder != self.internal_file_system:
                path_parts.insert(0, temp_folder["name"])
                temp_folder = temp_folder["parent"]
            current_path_label.config(text="Pašreizējā mape: /" + "/".join(path_parts))

        def on_folder_select(event):
            nonlocal current_dialog_folder
            selection = folder_listbox.curselection()
            if selection:
                index = selection[0]
                item_text = folder_listbox.get(index)

                if item_text.startswith("📁 .."):  # Atpakaļ
                    if current_dialog_folder.get("parent"):
                        current_dialog_folder = current_dialog_folder["parent"]
                        update_folder_listbox()
                else:  # Mape
                    folder_name = item_text[2:].strip()  # Noņem "📁 "
                    for item in current_dialog_folder["contents"]:
                        if item["type"] == "folder" and item["name"] == folder_name:
                            current_dialog_folder = item
                            update_folder_listbox()
                            break

        folder_listbox.bind("<Double-Button-1>", on_folder_select)

        # Ieteiktās kategorijas rāmis
        suggested_frame = ttk.LabelFrame(dialog, text="Ieteiktā kategorija", padding=5)
        suggested_frame.pack(fill="x", padx=10, pady=5)

        suggested_label = ttk.Label(suggested_frame, text=f"Programma iesaka: {suggested_category}")
        suggested_label.pack(side=tk.LEFT, padx=5)

        def use_suggested():
            nonlocal selected_node
            selected_node = self.get_or_create_folder(suggested_category)
            dialog.destroy()

        ttk.Button(suggested_frame, text="Izmantot ieteikto", command=use_suggested, bootstyle=SUCCESS).pack(
            side=tk.RIGHT, padx=5)

        # Pogas
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill="x", padx=10, pady=5)

        def create_new_folder_in_dialog():
            new_name = simpledialog.askstring("Jauna mape", "Ievadiet jaunās mapes nosaukumu:", parent=dialog)
            if new_name:
                # Pārbauda, vai mape ar šādu nosaukumu jau eksistē pašreizējā dialoga mapē
                for item in current_dialog_folder["contents"]:
                    if item["type"] == "folder" and item["name"] == new_name:
                        messagebox.showwarning("Mape jau eksistē",
                                               f"Mape ar nosaukumu '{new_name}' jau eksistē šajā mapē.", parent=dialog)
                        return
                new_folder = {"type": "folder", "name": new_name, "contents": [], "parent": current_dialog_folder}
                current_dialog_folder["contents"].append(new_folder)
                update_folder_listbox()
                self.save_pdf_archive()  # Saglabā izmaiņas arhīvā

        ttk.Button(button_frame, text="Izveidot jaunu mapi", command=create_new_folder_in_dialog).pack(side=tk.LEFT,
                                                                                                       padx=2)

        def confirm_selection():
            nonlocal selected_node
            selected_node = current_dialog_folder  # Izvēlētā mape ir pašreizējā dialoga mape
            dialog.destroy()

        ttk.Button(button_frame, text="Apstiprināt izvēli", command=confirm_selection).pack(side=tk.LEFT, padx=2)
    def create_menu(self):
        """Izveido lietojumprogrammas izvēlni."""
        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Atvērt attēlus...", command=self.open_files)
        file_menu.add_command(label="Vispārīgie Iestatījumi...", command=self.show_settings)  # MAINĪTS TEKSTS
        file_menu.add_command(label="Skenēšanas Iestatījumi...", command=self.show_scan_settings)  # JAUNA IZVĒLNE
        file_menu.add_separator()
        file_menu.add_command(label="Iziet", command=self.quit)
        menu_bar.add_cascade(label="Fails", menu=file_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Par programmu", command=self.show_about)
        help_menu.add_command(label="Pārbaudīt OCR valodas", command=self.check_ocr_languages)
        menu_bar.add_cascade(label="Palīdzība", menu=help_menu)

        self.config(menu=menu_bar)

    def show_about(self):
        """Parāda informāciju par lietojumprogrammu."""
        messagebox.showinfo("Par programmu",
                            "Advanced OCR uz PDF\n\n"
                            "Versija: 2.3\n"
                            "Funkcijas:\n"
                            "- Augstas kvalitātes OCR teksts\n"
                            "- Meklējamais teksts PDF failos\n"
                            "- Vairāku valodu atbalsts\n"
                            "- Responsīvs lietotāja interfeiss ar cilnēm un ritjoslām\n"
                            "- Attēlu apstrādes rīki (spilgtums, kontrasts, asums, rotācija)\n"
                            "- Slīpuma korekcija (Deskew)\n"
                            "- Trokšņu samazināšana\n"
                            "- Attēla negatīvs, malu noteikšana, binārizācija\n"
                            "- Automātiska attēla uzlabošana\n"
                            "- Pielāgojami OCR parametri\n"
                            "- PDF lapas orientācijas un izmēra izvēle\n"
                            "- PDF izvades kvalitātes kontrole\n"
                            "- Iestatījumu saglabāšana un automātiska ielāde\n"
                            "- Attēlu dzēšana no saraksta\n"
                            "- Attēla priekšskatījuma tālummaiņa un pārvietošana\n"
                            "- Pilnekrāna attēla priekšskatījums\n"
                            "- Attēla histogramma, metadati, krāsu palete\n"
                            "- Unikāls dokumenta ID un QR kods PDF failos\n"
                            "- Integrēta PDF failu pārvaldības sistēma (arhīvs)\n"
                            "- Meklēšana un filtrēšana PDF arhīvā pēc datuma un teksta\n"
                            "- Iespēja nosūtīt PDF failus e-pastā, izmantojot noklusēto e-pasta klientu\n"
                            "- Mapju izveide un failu pārvietošana failu pārvaldības cilnē\n"
                            "- Automātiska dokumentu klasifikācija un saglabāšana atbilstošās mapēs")

    def show_settings(self):
        """Parāda vispārīgo iestatījumu logu."""
        if not hasattr(self, '_settings_window') or not self._settings_window.winfo_exists():
            self._settings_window = SettingsWindow(self, self)
        self._settings_window.lift()
    def show_scan_settings(self):
        """JAUNS: Parāda skenēšanas iestatījumu logu."""
        if not hasattr(self, '_scan_settings_window') or not self._scan_settings_window.winfo_exists():
            self._scan_settings_window = ScanSettingsWindow(self, self)
        self._scan_settings_window.lift()

    def open_files(self, filepath=None):
        """Galvenā metode failu atvēršanai"""
        if filepath is None:
            filepaths = filedialog.askopenfilenames(
                title="Izvēlieties failus",
                filetypes=[("PDF faili", "*.pdf"), ("Attēli", "*.png *.jpg *.jpeg")]
            )
        else:
            filepaths = [filepath]

        if not filepaths:
            return

        self.clear_files()

        for filepath in filepaths:
            if not os.path.exists(filepath):
                continue

            try:
                if filepath.lower().endswith('.pdf'):
                    with PDFEditor(filepath) as editor:
                        for page_num in range(editor.get_page_count()):
                            img = editor.get_page_image(page_num, self.dpi_var.get())
                            self.images.append({
                                "filepath": f"{filepath}||page{page_num}",
                                "original_img": img.copy(),
                                "processed_img": img.copy()
                            })
                            self.file_listbox.insert(tk.END, f"{os.path.basename(filepath)} (lapa {page_num + 1})")
                else:
                    img = Image.open(filepath)
                    self.images.append({
                        "filepath": filepath,
                        "original_img": img.copy(),
                        "processed_img": img.copy()
                    })
                    self.file_listbox.insert(tk.END, os.path.basename(filepath))

                # Saglabā failu lietotāja datu struktūrā
                save_user_file(self.username, filepath)  # Saglabā failu lietotāja datu struktūrā
            except Exception as e:
                print(f"Kļūda apstrādājot {filepath}: {e}")

        if self.images:
            self.file_listbox.select_set(0)
            self.on_file_select()

    def clear_files(self):
        """Notīra visus ielādētos attēlus un OCR rezultātus."""
        self.images.clear()
        self.file_listbox.delete(0, tk.END)
        self.ocr_results.clear()  # Notīra OCR rezultātus
        # Notīra visas iepriekšējās fona krāsas, ja tādas bija
        self.ocr_results.clear()
        self.text_ocr.delete("1.0", tk.END)
        self.canvas.delete("all")
        self.progress["value"] = 0
        self.current_image_index = -1
        self.reset_image_processing_vars()
        self.canvas_zoom_factor = 1.0
        self.canvas_pan_x = 0
        self.canvas_pan_y = 0

    def reset_image_processing_vars(self):
        """Atjauno attēlu apstrādes mainīgos uz noklusējuma vērtībām."""
        self.brightness_var.set(1.0)
        self.contrast_var.set(1.0)
        self.sharpness_var.set(1.0)
        self.rotate_var.set(0)
        self.grayscale_var.set(True)
        self.deskew_var.set(False)
        self.remove_noise_var.set(False)
        self.invert_colors_var.set(False)
        self.edge_detection_var.set(False)
        self.binarize_var.set(False)

    def delete_selected_image(self):
        """Dzēš atlasītos attēlus no saraksta."""
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showwarning("Nav atlasīts", "Lūdzu, atlasiet attēlu(s), ko dzēst.")
            return

        # Sakārto indeksus dilstošā secībā, lai dzēšot nemainītos atlikušo elementu indeksi
        selected_indices = sorted(list(selection), reverse=True)

        if messagebox.askyesno("Dzēst attēlus",
                               f"Vai tiešām vēlaties dzēst {len(selected_indices)} atlasītos attēlus no saraksta?"):
            for index in selected_indices:
                # Pārbauda, vai indekss joprojām ir derīgs (ja saraksts ir mainījies)
                if index < len(self.images):
                    # Nav nepieciešams dzēst fizisko failu, jo tie ir tikai ielādēti attēli
                    # no dažādām vietām, nevis arhīva faili.
                    del self.images[index]
                    if len(self.ocr_results) > index:
                        del self.ocr_results[index]
                    self.file_listbox.delete(index)  # Dzēš no Listbox
                    # Pēc dzēšanas no Listbox, atjaunojam atlikušo vienumu krāsas, ja nepieciešams
                    # Tas nodrošina, ka, ja dzēšam vienumu, kas nav pēdējais,
                    # tad nākamie vienumi saglabā savas krāsas vai atjaunojas uz noklusējumu.
                    # Šeit mēs vienkārši atjaunojam visu sarakstu, lai nodrošinātu konsekvenci.
                    for index in selected_indices:
                        # Pārbauda, vai indekss joprojām ir derīgs (ja saraksts ir mainījies)
                        if index < len(self.images):
                            # Nav nepieciešams dzēst fizisko failu, jo tie ir tikai ielādēti attēli
                            # no dažādām vietām, nevis arhīva faili.
                            del self.images[index]
                            # Pārbauda, vai ocr_results saraksts ir pietiekami garš
                            if index < len(self.ocr_results):
                                del self.ocr_results[index]
                            # Listbox vienumi tiks atjaunināti ar refresh_file_listbox() pēc cikla

                    # Pēc visu atlasīto vienumu dzēšanas no datu struktūrām, atjaunojam Listbox
                    self.refresh_file_listbox()

                    if self.images:
                        # Pēc dzēšanas mēģina atlasīt pirmo atlikušo attēlu, ja tāds ir
                        new_index = 0
                        if new_index < len(self.images):
                            self.file_listbox.select_set(new_index)
                            self.on_file_select()
                        else:
                            self.clear_files()  # Ja saraksts ir tukšs
                    else:
                        self.clear_files()
                    messagebox.showinfo("Dzēsts", "Atlasītie attēli veiksmīgi dzēsti no saraksta.")

            if self.images:
                # Pēc dzēšanas mēģina atlasīt pirmo atlikušo attēlu, ja tāds ir
                new_index = 0
                if new_index < len(self.images):
                    self.file_listbox.select_set(new_index)
                    self.on_file_select()
                else:
                    self.clear_files()  # Ja saraksts ir tukšs
            else:
                self.clear_files()
            messagebox.showinfo("Dzēsts", "Atlasītie attēli veiksmīgi dzēsti no saraksta.")

    def on_file_click(self, event):
        """Apstrādā vienu klikšķi uz faila, lai to apskatītu."""
        # Pārbauda, vai nav nospiests Ctrl vai Shift, kas norāda uz vairāku atlasi
        if event.state & 0x4 or event.state & 0x1:  # 0x4 ir Ctrl, 0x1 ir Shift
            return  # Ļauj Listbox apstrādāt vairāku atlasi

        # Notīra iepriekšējo atlasi un atlasa tikai noklikšķināto vienumu
        self.file_listbox.selection_clear(0, tk.END)
        index = self.file_listbox.nearest(event.y)
        if index != -1:
            self.file_listbox.selection_set(index)
            self.on_file_select()  # Izsauc faila atlases funkciju

    def on_file_select_deferred(self):
        """Aizkavēta faila atlases apstrāde, lai izvairītos no konfliktiem ar vilkšanu."""
        # Šī funkcija tiek izsaukta pēc <<ListboxSelect>> notikuma.
        # Ja ir aktīva vilkšanas operācija, mēs neko nedarām.
        if self.file_drag_data["item_index"] is not None:
            return

        # Ja nav aktīvas vilkšanas, tad izsaucam parasto atlases loģiku.
        # Tomēr, lai nodrošinātu, ka vienmēr tiek parādīts atlasītais fails,
        # mēs izmantosim on_file_click, kas jau apstrādā vienu atlasi.
        # Šis <<ListboxSelect>> notikums joprojām ir noderīgs, ja lietotājs izmanto
        # tastatūras bulttaustiņus, lai pārvietotos pa sarakstu.
        selection = self.file_listbox.curselection()
        if selection:
            self.current_image_index = selection[0]
            self.apply_image_filters(None)
            if len(self.ocr_results) > self.current_image_index and self.ocr_results[
                self.current_image_index] is not None:
                self.text_ocr.delete("1.0", tk.END)
                self.text_ocr.insert(tk.END, self.ocr_results[self.current_image_index]['full_text'])
            else:
                self.text_ocr.delete("1.0", tk.END)
                self.text_ocr.insert(tk.END, "OCR rezultāts vēl nav pieejams.")
        else:
            self.current_image_index = -1
            self.canvas.delete("all")
            self.text_ocr.delete("1.0", tk.END)


    def move_file_up(self):
        """Pārvieto atlasīto failu uz augšu sarakstā."""
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showwarning("Nav atlasīts", "Lūdzu, atlasiet failu.")
            return

        index = selection[0]
        if index > 0:
            # Maina vietām ar iepriekšējo
            self.images[index], self.images[index - 1] = self.images[index - 1], self.images[index]
            if len(self.ocr_results) > index:
                self.ocr_results[index], self.ocr_results[index - 1] = self.ocr_results[index - 1], self.ocr_results[
                    index]

            self.refresh_file_listbox()
            self.file_listbox.select_set(index - 1)
            self.current_image_index = index - 1
            self.on_file_select()

    def move_file_down(self):
        """Pārvieto atlasīto failu uz leju sarakstā."""
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showwarning("Nav atlasīts", "Lūdzu, atlasiet failu.")
            return

        index = selection[0]
        if index < len(self.images) - 1:
            # Maina vietām ar nākošo
            self.images[index], self.images[index + 1] = self.images[index + 1], self.images[index]
            if len(self.ocr_results) > index + 1:
                self.ocr_results[index], self.ocr_results[index + 1] = self.ocr_results[index + 1], self.ocr_results[
                    index]

            self.refresh_file_listbox()
            self.file_listbox.select_set(index + 1)
            self.current_image_index = index + 1
            self.on_file_select()

    def file_list_drag_start(self, event):
        """Sāk vilkšanas operāciju attēlu sarakstā."""
        index = self.file_listbox.nearest(event.y)
        if index != -1:
            # Pārbauda, vai noklikšķinātais vienums ir atlasīts.
            # Ja nav, tad notīra iepriekšējo atlasi un atlasa tikai šo vienumu.
            if index not in self.file_listbox.curselection():
                self.file_listbox.selection_clear(0, tk.END)
                self.file_listbox.selection_set(index)
                self.on_file_select()  # Atjauno priekšskatījumu uz atlasīto failu

            self.file_drag_data["item_index"] = index
            self.file_drag_data["start_y"] = event.y
            self.file_listbox.config(cursor="fleur")  # Maina kursoru uz pārvietošanas ikonu

    def file_list_drag_motion(self, event):
        """Apstrādā vilkšanas kustību attēlu sarakstā."""
        if self.file_drag_data["item_index"] is not None:
            # Šeit varētu pievienot vizuālu atgriezenisko saiti, piemēram, zīmēt līniju
            # vai mainīt fona krāsu, kur fails tiks nomests.
            pass

    def file_list_drag_drop(self, event):
        """Apstrādā nomešanas operāciju attēlu sarakstā."""
        self.file_listbox.config(cursor="arrow")  # Atjauno kursoru
        if self.file_drag_data["item_index"] is not None:
            current_index = self.file_drag_data["item_index"]
            target_index = self.file_listbox.nearest(event.y)

            if target_index != -1 and current_index != target_index:
                # Pārvieto atlasītos vienumus
                selected_indices = sorted([i for i in self.file_listbox.curselection()], reverse=True)

                # Izveido sarakstu ar pārvietojamiem attēliem un OCR rezultātiem
                moved_images = []
                moved_ocr_results = []
                for idx in selected_indices:
                    moved_images.insert(0, self.images.pop(idx))
                    if len(self.ocr_results) > idx:
                        moved_ocr_results.insert(0, self.ocr_results.pop(idx))
                    else:
                        moved_ocr_results.insert(0, None)  # Ja OCR rezultāts vēl nav

                # Ievieto pārvietotos vienumus jaunajā pozīcijā
                for i, img_data in enumerate(moved_images):
                    insert_idx = target_index if target_index < current_index else target_index - (
                                len(selected_indices) - 1) + i
                    self.images.insert(insert_idx, img_data)
                    self.ocr_results.insert(insert_idx, moved_ocr_results[i])

                self.refresh_file_listbox()  # Atjauno Listbox vizuāli

                # Atjauno atlasi uz pārvietotajiem vienumiem
                new_selection_start = min(current_index, target_index)
                new_selection_end = new_selection_start + len(selected_indices) - 1
                for i in range(new_selection_start, new_selection_end + 1):
                    self.file_listbox.selection_set(i)

                # Pārliecinās, ka pašreizējais attēls joprojām ir redzams, ja tas tika pārvietots
                if self.current_image_index != -1:
                    old_current_image_filepath = self.images[self.current_image_index]["filepath"]
                    # Atrod jauno indeksu pašreizējam attēlam
                    for i, img_data in enumerate(self.images):
                        if img_data["filepath"] == old_current_image_filepath:
                            self.current_image_index = i
                            break
                    self.on_file_select()  # Atjauno priekšskatījumu

                messagebox.showinfo("Pārvietots", "Atlasītie faili veiksmīgi pārvietoti sarakstā.")

            self.file_drag_data["item_index"] = None  # Notīra vilkšanas datus

        # Pilnībā aizvietojiet esošo refresh_file_listbox metodi ar šo:

        def refresh_file_listbox(self):
            """Atjauno failu saraksta izskatu"""
            current_selection = self.file_listbox.curselection()  # Saglabā aktuālo atlasi
            self.file_listbox.delete(0, tk.END)

            for i, img_data in enumerate(self.images):
                # Noteik faila nosaukumu
                if "Lapa" in img_data["filepath"]:
                    display_name = img_data["filepath"]
                else:
                    display_name = os.path.basename(img_data["filepath"])

                self.file_listbox.insert(tk.END, display_name)

                # Iestata fona krāsu, ja fails ir apstrādāts
                if i < len(self.ocr_results) and self.ocr_results[i] is not None:
                    self.file_listbox.itemconfig(i, {'bg': '#d4edda'})

            # Atjauno iepriekšējo atlasi
            if current_selection:
                for index in current_selection:
                    if index < self.file_listbox.size():
                        self.file_listbox.selection_set(index)

    def on_file_click(self, event):
        """Apstrādā vienu klikšķi uz faila, lai to apskatītu."""
        # Pārbauda, vai nav nospiests Ctrl vai Shift, kas norāda uz vairāku atlasi
        if event.state & 0x4 or event.state & 0x1:  # 0x4 ir Ctrl, 0x1 ir Shift
            return  # Ļauj Listbox apstrādāt vairāku atlasi

        # Notīra iepriekšējo atlasi un atlasa tikai noklikšķināto vienumu
        self.file_listbox.selection_clear(0, tk.END)
        index = self.file_listbox.nearest(event.y)
        if index != -1:
            self.file_listbox.selection_set(index)
            self.on_file_select()  # Izsauc faila atlases funkciju

    def on_file_select_deferred(self):
        """Aizkavēta faila atlases apstrāde, lai izvairītos no konfliktiem ar vilkšanu."""
        # Šī funkcija tiek izsaukta pēc <<ListboxSelect>> notikuma.
        # Ja ir aktīva vilkšanas operācija, mēs neko nedarām.
        if self.file_drag_data["item_index"] is not None:
            return

        # Ja nav aktīvas vilkšanas, tad izsaucam parasto atlases loģiku.
        # Tomēr, lai nodrošinātu, ka vienmēr tiek parādīts atlasītais fails,
        # mēs izmantosim on_file_click, kas jau apstrādā vienu atlasi.
        # Šis <<ListboxSelect>> notikums joprojām ir noderīgs, ja lietotājs izmanto
        # tastatūras bulttaustiņus, lai pārvietotos pa sarakstu.
        selection = self.file_listbox.curselection()
        if selection:
            self.current_image_index = selection[0]
            self.apply_image_filters(None)
            if len(self.ocr_results) > self.current_image_index and self.ocr_results[
                self.current_image_index] is not None:
                self.text_ocr.delete("1.0", tk.END)
                self.text_ocr.insert(tk.END, self.ocr_results[self.current_image_index]['full_text'])
            else:
                self.text_ocr.delete("1.0", tk.END)
                self.text_ocr.insert(tk.END, "OCR rezultāts vēl nav pieejams.")
        else:
            self.current_image_index = -1
            self.canvas.delete("all")
            self.text_ocr.delete("1.0", tk.END)

    def move_file_up(self):
        """Pārvieto atlasīto failu uz augšu sarakstā."""
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showwarning("Nav atlasīts", "Lūdzu, atlasiet failu.")
            return

        index = selection[0]
        if index > 0:
            # Maina vietām ar iepriekšējo
            self.images[index], self.images[index - 1] = self.images[index - 1], self.images[index]
            if len(self.ocr_results) > index:
                self.ocr_results[index], self.ocr_results[index - 1] = self.ocr_results[index - 1], self.ocr_results[
                    index]

            self.refresh_file_listbox()
            self.file_listbox.select_set(index - 1)
            self.current_image_index = index - 1
            self.on_file_select()

    def move_file_down(self):
        """Pārvieto atlasīto failu uz leju sarakstā."""
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showwarning("Nav atlasīts", "Lūdzu, atlasiet failu.")
            return

        index = selection[0]
        if index < len(self.images) - 1:
            # Maina vietām ar nākošo
            self.images[index], self.images[index + 1] = self.images[index + 1], self.images[index]
            if len(self.ocr_results) > index + 1:
                self.ocr_results[index], self.ocr_results[index + 1] = self.ocr_results[index + 1], self.ocr_results[
                    index]

            self.refresh_file_listbox()
            self.file_listbox.select_set(index + 1)
            self.current_image_index = index + 1
            self.on_file_select()

    def file_list_drag_start(self, event):
        """Sāk vilkšanas operāciju attēlu sarakstā."""
        index = self.file_listbox.nearest(event.y)
        if index != -1:
            # Pārbauda, vai noklikšķinātais vienums ir atlasīts.
            # Ja nav, tad notīra iepriekšējo atlasi un atlasa tikai šo vienumu.
            if index not in self.file_listbox.curselection():
                self.file_listbox.selection_clear(0, tk.END)
                self.file_listbox.selection_set(index)
                self.on_file_select()  # Atjauno priekšskatījumu uz atlasīto failu

            self.file_drag_data["item_index"] = index
            self.file_drag_data["start_y"] = event.y
            self.file_listbox.config(cursor="fleur")  # Maina kursoru uz pārvietošanas ikonu

    def file_list_drag_motion(self, event):
        """Apstrādā vilkšanas kustību attēlu sarakstā."""
        if self.file_drag_data["item_index"] is not None:
            # Šeit varētu pievienot vizuālu atgriezenisko saiti, piemēram, zīmēt līniju
            # vai mainīt fona krāsu, kur fails tiks nomests.
            pass

    def file_list_drag_drop(self, event):
        """Apstrādā nomešanas operāciju attēlu sarakstā."""
        self.file_listbox.config(cursor="arrow")  # Atjauno kursoru
        if self.file_drag_data["item_index"] is not None:
            current_index = self.file_drag_data["item_index"]
            target_index = self.file_listbox.nearest(event.y)

            if target_index != -1 and current_index != target_index:
                # Pārvieto atlasītos vienumus
                selected_indices = sorted([i for i in self.file_listbox.curselection()], reverse=True)

                # Izveido sarakstu ar pārvietojamiem attēliem un OCR rezultātiem
                moved_images = []
                moved_ocr_results = []
                for idx in selected_indices:
                    moved_images.insert(0, self.images.pop(idx))
                    if len(self.ocr_results) > idx:
                        moved_ocr_results.insert(0, self.ocr_results.pop(idx))
                    else:
                        moved_ocr_results.insert(0, None)  # Ja OCR rezultāts vēl nav

                # Ievieto pārvietotos vienumus jaunajā pozīcijā
                for i, img_data in enumerate(moved_images):
                    insert_idx = target_index if target_index < current_index else target_index - (
                                len(selected_indices) - 1) + i
                    self.images.insert(insert_idx, img_data)
                    self.ocr_results.insert(insert_idx, moved_ocr_results[i])

                self.refresh_file_listbox()  # Atjauno Listbox vizuāli

                # Atjauno atlasi uz pārvietotajiem vienumiem
                new_selection_start = min(current_index, target_index)
                new_selection_end = new_selection_start + len(selected_indices) - 1
                for i in range(new_selection_start, new_selection_end + 1):
                    self.file_listbox.selection_set(i)

                # Pārliecinās, ka pašreizējais attēls joprojām ir redzams, ja tas tika pārvietots
                if self.current_image_index != -1:
                    old_current_image_filepath = self.images[self.current_image_index]["filepath"]
                    # Atrod jauno indeksu pašreizējam attēlam
                    for i, img_data in enumerate(self.images):
                        if img_data["filepath"] == old_current_image_filepath:
                            self.current_image_index = i
                            break
                    self.on_file_select()  # Atjauno priekšskatījumu

                messagebox.showinfo("Pārvietots", "Atlasītie faili veiksmīgi pārvietoti sarakstā.")

            self.file_drag_data["item_index"] = None  # Notīra vilkšanas datus

    def refresh_file_listbox(self):
        """Atjauno failu saraksta Listbox vizuāli un atjaunina krāsas."""
        self.file_listbox.delete(0, tk.END)
        default_bg_color = self.style.colors.get("bg")  # Iegūst noklusējuma fona krāsu no tēmas

        for i, img_data in enumerate(self.images):
            display_name = ""
            # Pārbauda, vai tas ir PDF lapa vai atsevišķs attēls
            if "Lapa" in img_data["filepath"]:  # Vienkāršots veids, kā atpazīt PDF lapas
                display_name = img_data["filepath"]
            else:
                display_name = os.path.basename(img_data["filepath"])

            self.file_listbox.insert(tk.END, display_name)

            # Pārbauda, vai OCR ir pabeigts šim failam un iezīmē to zaļā krāsā
            # Pārliecinās, ka indekss ir derīgs ocr_results sarakstam
            if i < len(self.ocr_results) and self.ocr_results[i] is not None:
                self.file_listbox.itemconfig(i, {'bg': '#d4edda'})  # Gaiši zaļa krāsa
            else:
                # Atjauno noklusējuma krāsu, ja fails vēl nav apstrādāts
                self.file_listbox.itemconfig(i, {'bg': default_bg_color})

        # Atjauno iepriekšējo atlasi, ja tāda bija
        if self.current_image_index != -1 and self.current_image_index < len(self.images):
            self.file_listbox.select_set(self.current_image_index)
            self.file_listbox.activate(self.current_image_index)
            self.file_listbox.see(self.current_image_index)  # Pārvietojas uz atlasīto vienumu

    def show_file_context_menu(self, event):
        """Parāda konteksta izvēlni failu saraksta elementiem."""
        try:
            self.file_listbox.selection_clear(0, tk.END)
            self.file_listbox.selection_set(self.file_listbox.nearest(event.y))
            self.file_listbox.activate(self.file_listbox.nearest(event.y))

            context_menu = tk.Menu(self.file_listbox, tearoff=0)
            context_menu.add_command(label="Dzēst", command=self.delete_selected_image)
            context_menu.add_command(label="Atvērt faila atrašanās vietu", command=self.open_file_location)
            context_menu.post(event.x_root, event.y_root)
        except Exception:
            pass  # Ja nav atlasīts nekas, ignorē

    def open_file_location(self):
        """Atver mapes atrašanās vietu, kurā atrodas atlasītais attēla fails."""
        selection = self.file_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        filepath = self.images[index]['filepath']
        if os.path.exists(filepath):
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(os.path.dirname(filepath))
                elif os.name == 'posix':  # macOS, Linux
                    import subprocess
                    import sys
                    if sys.platform == 'darwin':  # macOS
                        subprocess.Popen(['open', '-R', filepath])
                    else:  # Linux
                        subprocess.Popen(['xdg-open', os.path.dirname(filepath)])
            except Exception as e:
                messagebox.showerror("Kļūda", f"Neizdevās atvērt faila atrašanās vietu:\n{e}")
        else:
            messagebox.showwarning("Fails nav atrasts", "Attēla fails nav atrasts norādītajā vietā.")

    def on_file_select(self):
        """Apstrādā faila atlasi sarakstā, atjauninot priekšskatījumu un OCR tekstu."""
        selection = self.file_listbox.curselection()
        if not selection or not self.images:
            self.current_image_index = -1
            self.canvas.delete("all")
            self.text_ocr.delete("1.0", tk.END)
            return

        index = selection[0]
        self.current_image_index = index
        self.apply_image_filters(None)

        if len(self.ocr_results) > index and self.ocr_results[index] is not None:
            self.text_ocr.delete("1.0", tk.END)
            self.text_ocr.insert(tk.END, self.ocr_results[index]['full_text'])
        else:
            self.text_ocr.delete("1.0", tk.END)
            self.text_ocr.insert(tk.END, "OCR rezultāts vēl nav pieejams.")

    def apply_image_filters(self, event):
        """Pielieto attēlu apstrādes filtrus pašreizējam attēlam."""
        if self.current_image_index == -1:
            return

        img_data = self.images[self.current_image_index]
        img = img_data["original_img"].copy()

        rotation_angle = self.rotate_var.get()
        if rotation_angle != 0:
            img = img.rotate(rotation_angle, expand=True, fillcolor=(255, 255, 255) if img.mode == 'RGB' else 255)

        if self.grayscale_var.get():
            img = img.convert("L")

        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(self.brightness_var.get())

        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(self.contrast_var.get())

        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(self.sharpness_var.get())

        if self.deskew_var.get() and OPENCV_AVAILABLE:
            try:
                img_cv = np.array(img)
                if len(img_cv.shape) == 3:
                    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
                img_cv = cv2.bitwise_not(img_cv)
                coords = np.column_stack(np.where(img_cv > 0))

                # Pārbaude, vai coords nav tukšs
                if coords.size > 0:
                    angle = cv2.minAreaRect(coords)[-1]
                    if angle < -45:
                        angle = -(90 + angle)
                    else:
                        angle = -angle
                    (h, w) = img_cv.shape[:2]
                    center = (w // 2, h // 2)
                    M = cv2.getRotationMatrix2D(center, angle, 1.0)
                    img_cv = cv2.warpAffine(img_cv, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
                    img_cv = cv2.bitwise_not(img_cv)
                    img = Image.fromarray(img_cv)
                else:
                    messagebox.showwarning("Slīpuma korekcija",
                                           "Netika atrasts pietiekami daudz teksta slīpuma korekcijai. Slīpuma korekcija netika veikta.")
                    self.deskew_var.set(False)  # Atspējo, ja nevar veikt
            except Exception as e:
                messagebox.showwarning("Slīpuma korekcijas kļūda", f"Neizdevās veikt slīpuma korekciju: {e}")
                self.deskew_var.set(False)
        elif self.deskew_var.get() and not OPENCV_AVAILABLE:
            messagebox.showwarning("Trūkst bibliotēkas",
                                   "Slīpuma korekcijai nepieciešams 'opencv-python' un 'numpy'. Lūdzu, instalējiet tās (pip install opencv-python numpy).")
            self.deskew_var.set(False)

        if self.remove_noise_var.get():
            if img.mode != 'L':
                img = img.convert("L")
            img = img.filter(ImageFilter.MedianFilter(size=3))

        if self.invert_colors_var.get():
            img = ImageOps.invert(img)

        if self.edge_detection_var.get():
            if img.mode != 'L':
                img = img.convert("L")
            img = img.filter(ImageFilter.FIND_EDGES)

        if self.binarize_var.get():
            if img.mode != 'L':
                img = img.convert("L")
            img = img.point(lambda x: 0 if x < 128 else 255, '1')

        img_data["processed_img"] = img
        self.show_image_preview(img)

    def show_image_preview(self, img):
        """Parāda attēla priekšskatījumu uz kanvasa."""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            return

        img_width, img_height = img.size
        scaled_width = int(img_width * self.canvas_zoom_factor)
        scaled_height = int(img_height * self.canvas_zoom_factor)

        display_img = img.resize((scaled_width, scaled_height), Image.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(display_img)

        self.canvas.delete("all")

        x = (canvas_width - scaled_width) / 2 + self.canvas_pan_x
        y = (canvas_height - scaled_height) / 2 + self.canvas_pan_y

        self.canvas.create_image(x, y, anchor="nw", image=self.photo_image)
        self.canvas.image = self.photo_image

    def resize_canvas(self, event):
        """Pielāgo kanvasa izmērus un atjaunina attēla priekšskatījumu."""
        if self.current_image_index != -1:
            img = self.images[self.current_image_index]["processed_img"]
            self.show_image_preview(img)

    def on_canvas_mouse_wheel(self, event):
        """Apstrādā peles rullīša notikumus kanvasa tālummaiņai."""
        if self.current_image_index == -1: return
        if event.num == 5 or event.delta == -120:  # Tuvināt
            self.canvas_zoom_factor = max(0.1, self.canvas_zoom_factor - 0.1)
        if event.num == 4 or event.delta == 120:  # Attālināt
            self.canvas_zoom_factor = min(5.0, self.canvas_zoom_factor + 0.1)
        self.show_image_preview(self.images[self.current_image_index]["processed_img"])

    def on_canvas_pan_start(self, event):
        """Sāk kanvasa attēla pārvietošanu (pan)."""
        if self.current_image_index == -1: return
        self.canvas_start_pan_x = event.x - self.canvas_pan_x
        self.canvas_start_pan_y = event.y - self.canvas_pan_y
        self.canvas.config(cursor="fleur")

    def on_canvas_pan_drag(self, event):
        """Pārvieto kanvasa attēlu, velkot peli."""
        if self.current_image_index == -1: return
        self.canvas_pan_x = event.x - self.canvas_start_pan_x
        self.canvas_pan_y = event.y - self.canvas_start_pan_y
        self.show_image_preview(self.images[self.current_image_index]["processed_img"])

    def on_canvas_pan_end(self, event):
        """Beidz kanvasa attēla pārvietošanu."""
        if self.current_image_index == -1: return
        self.canvas.config(cursor="arrow")

    def on_canvas_selection_start(self, event):
        """Sāk atlases taisnstūra zīmēšanu uz kanvasa."""
        if self.current_image_index == -1: return
        self.canvas_selection_start_x = self.canvas.canvasx(event.x)
        self.canvas_selection_start_y = self.canvas.canvasy(event.y)
        if self.canvas_selection_rect:
            self.canvas.delete(self.canvas_selection_rect)
        self.canvas_selection_rect = self.canvas.create_rectangle(self.canvas_selection_start_x,
                                                                  self.canvas_selection_start_y,
                                                                  self.canvas_selection_start_x,
                                                                  self.canvas_selection_start_y,
                                                                  outline="blue", width=2, dash=(5, 2))

    def on_canvas_selection_drag(self, event):
        """Atjaunina atlases taisnstūra izmērus uz kanvasa, velkot peli."""
        if self.current_image_index == -1: return
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.canvas_selection_rect, self.canvas_selection_start_x, self.canvas_selection_start_y,
                           cur_x, cur_y)

    def on_canvas_selection_end(self, event):
        """Beidz atlases taisnstūra zīmēšanu uz kanvasa (šeit varētu apstrādāt iezīmēto apgabalu)."""
        if self.current_image_index == -1: return
        # Šeit varētu apstrādāt iezīmēto apgabalu, piemēram, apgriezt vai veikt OCR uz iezīmētā apgabala
        pass

    def open_fullscreen_preview(self):
        """Atver pašreizējo attēlu pilnekrāna priekšskatījuma logā."""
        if self.current_image_index == -1:
            messagebox.showwarning("Nav attēla", "Lūdzu, vispirms atlasiet attēlu priekšskatījumam.")
            return
        img = self.images[self.current_image_index]["processed_img"]
        FullscreenImageViewer(self, img)

    def start_processing(self):
        """Sāk OCR apstrādes procesu atsevišķā pavedienā."""
        if not self.images:
            messagebox.showwarning("Nav attēlu", "Lūdzu, vispirms atlasiet attēlus!")
            return

        self.btn_start.config(state=DISABLED)
        self.btn_stop.config(state=NORMAL)
        self.progress.config(maximum=len(self.images))
        self.progress["value"] = 0
        self.ocr_results = [None] * len(self.images)
        self.stop_processing = False

        threading.Thread(target=self.process_images_thread, daemon=True).start()

    def stop_processing_func(self):
        """Aptur OCR apstrādes procesu."""
        self.stop_processing = True
        self.btn_stop.config(state=DISABLED)

    def process_images_thread(self):
        """OCR apstrādes loģika, kas darbojas atsevišķā pavedienā."""
        langs = []
        for lang_name, var in self.lang_vars.items():
            if var.get():
                langs.append(self.lang_options[lang_name])

        if not langs:
            langs = ["eng"]

        lang_param = "+".join(langs)
        tess_config = f"--psm {self.psm_var.get()} --oem {self.oem_var.get()}"
        confidence_threshold = self.confidence_var.get() / 100.0

        for i, img_data in enumerate(self.images):
            if self.stop_processing:
                messagebox.showinfo("Apstrāde apturēta", "OCR apstrāde tika apturēta pēc lietotāja pieprasījuma.")
                break

            filepath = img_data["filepath"]
            img_to_ocr = img_data["processed_img"]

            try:
                img_proc = self.preprocess_image_for_ocr(img_to_ocr, self.dpi_var.get())

                data = pytesseract.image_to_data(
                    img_proc,
                    lang=lang_param,
                    config=tess_config,
                    output_type=pytesseract.Output.DICT
                )

                processed_words = []
                full_text_lines = []
                current_line = []
                current_line_num = None

                for j in range(len(data["level"])):
                    if data["level"][j] == 5:
                        word = data["text"][j]
                        conf = float(data["conf"][j])

                        if word.strip() and conf >= confidence_threshold * 100:
                            x, y, w, h = data["left"][j], data["top"][j], data["width"][j], data["height"][j]
                            line_num = data["line_num"][j]

                            processed_words.append({
                                "text": word, "x": x, "y": y, "w": w, "h": h, "line_num": line_num
                            })

                            if current_line_num is None:
                                current_line_num = line_num
                            elif line_num != current_line_num:
                                full_text_lines.append(" ".join(current_line))
                                current_line = []
                                current_line_num = line_num
                            current_line.append(word)

                if current_line:
                    full_text_lines.append(" ".join(current_line))

                full_text = "\n".join(full_text_lines)
                self.ocr_results[i] = {
                    "full_text": full_text,
                    "word_data": processed_words,
                    "doc_id": str(uuid.uuid4())[:8].upper()  # Pievieno doc_id OCR rezultātiem
                }
                self.after(0, self.update_ocr_text, i)
                # Aizstāt ar šo kodu
                if hasattr(self, '_mark_file_as_processed'):
                    self.after(0, lambda: self._mark_file_as_processed(i))
                else:
                    print(f"Apstrādāts fails {i}")
                    # Šeit varat pievienot failu apstrādes loģiku



            except Exception as e:
                self.ocr_results[i] = {
                    "full_text": f"[OCR kļūda failā {os.path.basename(filepath)}] {str(e)}",
                    "word_data": [],
                    "doc_id": None
                }
                self.after(0, self.update_ocr_text, i)
                # Aizstāt ar šo kodu
                if hasattr(self, '_mark_file_as_processed'):
                    self.after(0, lambda: self._mark_file_as_processed(i))
                else:
                    print(f"Apstrādāts fails {i}")
                    # Šeit varat pievienot failu apstrādes loģiku

            self.after(0, lambda: self.progress.config(value=i + 1))

        if not self.stop_processing and any(res is not None for res in self.ocr_results):
            # Pārbauda, vai apstrāde tika sākta no kameras skenēšanas
            if hasattr(self, '_camera_scan_in_progress') and self._camera_scan_in_progress:
                self.after(0, self.save_pdf, True)  # Automātiski saglabā PDF
                self._camera_scan_in_progress = False
            else:
                self.after(0, self.save_pdf)  # Piedāvā saglabāt PDF
        else:
            if hasattr(self, '_camera_scan_in_progress') and self._camera_scan_in_progress:
                self._camera_scan_in_progress = False

        self.after(0, lambda: self.btn_start.config(state=NORMAL))
        self.after(0, lambda: self.btn_stop.config(state=DISABLED))

        # Pievieno šo kodu pēc OCR apstrādes
        decoded_barcodes = self.detect_and_decode_barcodes(img_to_ocr)
        if decoded_barcodes:
            self.ocr_results[i]["decoded_barcodes"] = decoded_barcodes  # Pievieno atšifrētos datus rezultātiem

    def preprocess_image_for_ocr(self, img, dpi=300):
        """Veic attēla priekšapstrādi OCR vajadzībām (pelēktoņi, automātiskais kontrasts, DPI pielāgošana)."""
        if img.mode != 'L':
            img = img.convert("L")
        img = ImageOps.autocontrast(img)
        original_dpi = img.info.get("dpi", (72, 72))[0]
        if original_dpi < dpi:
            scale_factor = dpi / original_dpi
            new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
            img = img.resize(new_size, Image.LANCZOS)
        return img

    def _mark_file_as_processed(self, index):
        """
        Iezīmē failu kā apstrādātu, mainot fona krāsu
        :param index: faila indekss sarakstā
        """
        try:
            if 0 <= index < self.file_listbox.size():  # Pārbauda derīgu indeksu
                self.file_listbox.itemconfig(index, {'bg': '#49be25'})  # Gaiši zaļa krāsa
                print(f"Fails ar indeksu {index} ir apstrādāts.")
        except Exception as e:
            print(f"Kļūda atzīmējot failu: {e}")

    def update_ocr_text(self, index):
        """Atjaunina OCR teksta lauku ar jaunākajiem rezultātiem."""
        selection = self.file_listbox.curselection()
        if selection and selection[0] == index and self.ocr_results[index]:
            self.text_ocr.delete("1.0", tk.END)
            self.text_ocr.insert(tk.END, self.ocr_results[index]["full_text"])

        # Atrodiet klases OCRPDFApp beigu daļu (pirms pēdējās "if __name__" rindas)
        # un ievietojiet šo jauno metodi:

        def _mark_file_as_processed(self, index):
            """Iezīmē failu kā apstrādātu, mainot fona krāsu"""
            if 0 <= index < self.file_listbox.size():  # Pārbauda derīgu indeksu
                self.file_listbox.itemconfig(index, {'bg': '#d4edda'})
                print(f"Fails ar indeksu {index} ir apstrādāts.")

    def classify_document(self, ocr_text):
        """Klasificē dokumentu, pamatojoties uz OCR tekstu un nosaka, vai tas ir sensitīvs."""
        ocr_text_lower = ocr_text.lower()

        # Pārbauda, vai dokuments ir sensitīvs
        is_sensitive = False
        for keyword in self.document_keywords["id_card"]:
            if keyword in ocr_text_lower:
                is_sensitive = True
                break

        if "pavadzīme" in ocr_text_lower or "delivery note" in ocr_text_lower or "shipping document" in ocr_text_lower:
            category = "Pavadzīmes"
        elif "rēķins" in ocr_text_lower or "invoice" in ocr_text_lower or "bill" in ocr_text_lower:
            category = "Rēķini"
        elif "līgums" in ocr_text_lower or "contract" in ocr_text_lower or "agreement" in ocr_text_lower:
            category = "Līgumi"
        elif "kvīts" in ocr_text_lower or "receipt" in ocr_text_lower or "payment confirmation" in ocr_text_lower:
            category = "Kvītis"
        elif "protokols" in ocr_text_lower or "minutes" in ocr_text_lower or "report" in ocr_text_lower:
            category = "Protokoli"
        elif "pasūtījums" in ocr_text_lower or "order" in ocr_text_lower or "purchase order" in ocr_text_lower:
            category = "Pasūtījumi"
        elif "darba laika uzskaite" in ocr_text_lower or "timesheet" in ocr_text_lower:
            category = "Darba laika uzskaite"
        elif "personāla dokuments" in ocr_text_lower or "personnel document" in ocr_text_lower or "employee record" in ocr_text_lower:
            category = "Personāla dokumenti"
        elif is_sensitive:  # Ja ir sensitīvs, bet nav citā kategorijā
            category = "Sensitīvi dokumenti"
        else:
            category = "Nekategorizēti"  # Ja nav atrasta neviena atbilstoša kategorija

        return category, is_sensitive

    def get_or_create_folder(self, folder_name):
        """Atgriež mapes objektu vai izveido jaunu, ja tā neeksistē."""
        for item in self.internal_file_system["contents"]:
            if item["type"] == "folder" and item["name"] == folder_name:
                return item
        # Ja mape neeksistē, izveido to saknes mapē
        new_folder = {"type": "folder", "name": folder_name, "contents": [], "parent": self.internal_file_system}
        self.internal_file_system["contents"].append(new_folder)
        return new_folder

    def save_pdf(self, auto_save=False):
        """Saglabā apstrādātos attēlus kā PDF failu ar meklējamu tekstu."""
        if not any(res is not None and res["word_data"] for res in self.ocr_results):
            messagebox.showwarning("Nav datu", "Nav neviens OCR rezultāts ar atpazītu tekstu saglabāšanai!")
            return

        # Ģenerē unikālu dokumenta ID
        doc_id = str(uuid.uuid4())[:8].upper()  # Īss, unikāls ID
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")

        # Klasificē dokumentu un iegūst ieteikto mapi
        first_ocr_text = self.ocr_results[0]["full_text"] if self.ocr_results and self.ocr_results[0] else ""
        document_category, is_sensitive = self.classify_document(first_ocr_text)

        # --- JAUNS KODS SĀKAS ŠEIT ---
        # Pirms saglabāšanas dialoga, piedāvā izvēlēties mapi
        selected_folder_node = None
        if not auto_save:
            # Atver mapes izvēles dialogu
            selected_folder_node = self._show_folder_selection_dialog(document_category)
            if selected_folder_node is None:  # Ja lietotājs atceļ mapes izvēli
                return

        # Ja lietotājs izvēlējās mapi, izmanto to, citādi izmanto klasificēto
        if selected_folder_node:
            target_folder_node = selected_folder_node
            # Atjaunina document_category, ja lietotājs izvēlējās citu mapi
            document_category = target_folder_node["name"]
        else:
            # Ja auto_save vai lietotājs neizvēlējās citu mapi, izmanto klasificēto
            target_folder_node = self.get_or_create_folder(document_category)

        # Izveido fizisko mapi, ja tā neeksistē
        # Šeit ir svarīgi izmantot `self.default_save_path` kā bāzes ceļu
        # un pievienot visu ceļu līdz izvēlētajai mapei iekšējā failu sistēmā.
        # Lai to izdarītu, mums ir jāizveido funkcija, kas atgriež pilnu fizisko ceļu no mapes mezgla.
        physical_category_path = self._get_physical_path_from_node(target_folder_node)
        os.makedirs(physical_category_path, exist_ok=True)

        default_filename = f"{document_category}_{current_date}_{doc_id}.pdf"
        full_save_path = os.path.join(physical_category_path, default_filename)

        out_path = full_save_path
        if not auto_save:
            out_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF faili", "*.pdf")],
                initialdir=physical_category_path,  # Sākotnējais direktorijs ir izvēlētā mape
                initialfile=default_filename,
                title="Saglabāt PDF kā"
            )

        if not out_path:
            return
        # --- JAUNS KODS BEIDZAS ŠEIT ---

        c = canvas.Canvas(out_path)
        fontsize = self.fontsize_var.get()

        jpeg_quality = 85
        if self.pdf_quality == "Zema (60)":
            jpeg_quality = 60
        elif self.pdf_quality == "Augsta (95)":
            jpeg_quality = 95

        for i, img_data in enumerate(self.images):
            if self.stop_processing or i >= len(self.ocr_results) or not self.ocr_results[i]:
                continue

            img_for_pdf = img_data["processed_img"]  # <--- Nomainīts uz processed_img
            img_width, img_height = img_for_pdf.size

            page_size = self.get_page_size(img_width, img_height)
            c.setPageSize(page_size)
            page_width, page_height = page_size

            img_ratio = img_width / img_height
            page_ratio = page_width / page_height

            if img_ratio > page_ratio:
                draw_width = page_width
                draw_height = page_width / img_ratio
            else:
                draw_height = page_height
                draw_width = page_height * img_ratio

            x_offset = (page_width - draw_width) / 2
            y_offset = (page_height - draw_height) / 2

            pil_img = img_for_pdf.convert("RGB")
            temp_img_path = "temp_image_for_pdf.jpg"
            pil_img.save(temp_img_path, "JPEG", quality=jpeg_quality)
            image_reader = ImageReader(temp_img_path)
            c.drawImage(image_reader, x_offset, y_offset, width=draw_width, height=draw_height)
            os.remove(temp_img_path)

            if self.include_text_var.get() and self.ocr_results[i]["word_data"]:
                word_data = self.ocr_results[i]["word_data"]
                processed_img_width, processed_img_height = img_data["processed_img"].size

                scale_x_ocr_to_pdf = draw_width / processed_img_width
                scale_y_ocr_to_pdf = draw_height / processed_img_height

                c.setFillColorRGB(0, 0, 0, 0)  # Caurspīdīgs teksts
                c.setFont("Helvetica", fontsize)

                for word in word_data:
                    x = x_offset + word["x"] * scale_x_ocr_to_pdf
                    y = y_offset + (processed_img_height - word["y"] - word["h"]) * scale_y_ocr_to_pdf

                    word_height_pdf = word["h"] * scale_y_ocr_to_pdf
                    actual_fontsize = max(fontsize, word_height_pdf * 0.8)  # Pielāgo fonta izmēru vārda augstumam
                    c.setFont("Helvetica", actual_fontsize)

                    text_obj = c.beginText(x, y)
                    text_obj.textLine(word["text"])
                    c.drawText(text_obj)

            # Pievieno QR kodu vai svītrkodu ar dokumenta ID, ja iestatīts
            if self.settings.get("add_id_code_to_pdf", False):
                id_code_type = self.settings.get("id_code_type", "QR")
                id_code_position = self.settings.get("id_code_position", "bottom_right")

                # Pārbauda, vai ir pieejams doc_id
                current_doc_id = self.ocr_results[i]["doc_id"] if self.ocr_results[i] else None
                if current_doc_id:
                    code_reader = None  # Inicializē code_reader
                    temp_code_path = None  # Inicializē temp_code_path

                    try:
                        if id_code_type == "QR":
                            qr_img = qrcode.make(current_doc_id)
                            qr_pil_img = qr_img.get_image()
                            temp_code_path = os.path.join(tempfile.gettempdir(),
                                                          "temp_qr_code.png")  # Izmanto temp direktoriju
                            qr_pil_img.save(temp_code_path)
                            code_reader = ImageReader(temp_code_path)
                        elif id_code_type == "Barcode":
                            try:
                                from barcode import Code128
                                from barcode.writer import ImageWriter

                                # Izveido pilnu faila ceļu pie temp direktorija, lai izvairītos no pieejas tiesību problēmām
                                temp_dir = tempfile.gettempdir()
                                temp_code_path = os.path.join(temp_dir, f"temp_barcode_{i}.png")

                                # Izveido barcode ar pilno ceļu un nodrošina, ka fails ir aizvērts pēc saglabāšanas
                                with open(temp_code_path, 'wb') as f:
                                    Code128(current_doc_id, writer=ImageWriter()).write(f)

                                # Pārliecinās, ka fails eksistē un ir nolasāms pirms mēģinājuma to lasīt
                                if os.path.exists(temp_code_path):
                                    code_reader = ImageReader(temp_code_path)
                                else:
                                    print(f"Nevarēja atrast ģenerēto svītrkoda failu: {temp_code_path}")
                                    continue  # Pārtrauc šī koda pievienošanu, ja fails nav atrasts
                            except Exception as e:
                                print(f"Svītrkoda ģenerēšanas kļūda: {e}")
                                continue  # Pārtrauc šī koda pievienošanu kļūdas gadījumā
                        elif id_code_type == "Code39":
                            try:
                                from barcode import Code39
                                from barcode.writer import ImageWriter
                                temp_dir = tempfile.gettempdir()
                                temp_code_path = os.path.join(temp_dir, f"temp_code39_{i}.png")
                                with open(temp_code_path, 'wb') as f:
                                    Code39(current_doc_id, writer=ImageWriter()).write(f)
                                if os.path.exists(temp_code_path):
                                    code_reader = ImageReader(temp_code_path)
                                else:
                                    print(f"Nevarēja atrast ģenerēto Code39 failu: {temp_code_path}")
                                    continue
                            except Exception as e:
                                print(f"Code39 ģenerēšanas kļūda: {e}")
                                continue
                        elif id_code_type == "EAN13":
                            try:
                                from barcode import EAN13
                                from barcode.writer import ImageWriter
                                temp_dir = tempfile.tempdir
                                temp_code_path = os.path.join(temp_dir, f"temp_ean13_{i}.png")
                                # EAN-13 prasa 12 ciparus, lai ģenerētu 13. pārbaudes ciparu
                                # Ja current_doc_id nav ciparu virkne vai nav pareizā garumā, tas var izraisīt kļūdu
                                # Šeit ir jābūt loģikai, kas nodrošina derīgu EAN-13 ievadi
                                # Vienkāršības labad pieņemam, ka current_doc_id ir derīgs 12 ciparu virkne
                                if len(current_doc_id) >= 12 and current_doc_id.isdigit():
                                    with open(temp_code_path, 'wb') as f:
                                        EAN13(current_doc_id[:12], writer=ImageWriter()).write(f)
                                    if os.path.exists(temp_code_path):
                                        code_reader = ImageReader(temp_code_path)
                                    else:
                                        print(f"Nevarēja atrast ģenerēto EAN-13 failu: {temp_code_path}")
                                        continue
                                else:
                                    print(f"Nederīgs ID EAN-13 ģenerēšanai: {current_doc_id}. Nepieciešami 12 cipari.")
                                    continue
                            except Exception as e:
                                print(f"EAN-13 ģenerēšanas kļūda: {e}")
                                continue

                        if code_reader:
                            # Dinamiski pielāgo koda izmēru, pamatojoties uz lapas izmēru
                            code_max_size = min(page_width, page_height) * 0.15  # Max 15% no mazākās lapas puses
                            code_size = min(0.75 * inch,
                                            code_max_size)  # Noklusējums 0.75 collas, bet ne lielāks par 15%

                            margin = 0.2 * inch  # Marža no malas

                            if id_code_position == "top_right":
                                code_x_pos = page_width - code_size - margin
                                code_y_pos = page_height - code_size - margin
                            elif id_code_position == "bottom_right":
                                code_x_pos = page_width - code_size - margin
                                code_y_pos = margin
                            elif id_code_position == "bottom_left":
                                code_x_pos = margin
                                code_y_pos = margin
                            elif id_code_position == "top_left":
                                code_x_pos = margin
                                code_y_pos = page_height - code_size - margin
                            else:  # Noklusējums
                                code_x_pos = page_width - code_size - margin
                                code_y_pos = margin

                            c.drawImage(code_reader, code_x_pos, code_y_pos, width=code_size, height=code_size)
                            os.remove(temp_code_path)  # Dzēš pagaidu failu
                    except ImportError:
                        messagebox.showwarning("Trūkst bibliotēkas",
                                               "Lai ģenerētu svītrkodus, lūdzu, instalējiet 'python-barcode' un 'Pillow' (pip install python-barcode Pillow).")
                    except Exception as code_e:
                        print(f"Koda ģenerēšanas kļūda: {code_e}")

            c.showPage()

        c.save()

        # Pievieno paroles aizsardzību, ja dokuments ir sensitīvs
        if is_sensitive:
            messagebox.showwarning("Datu aizsardzība",
                                   "Dokuments, iespējams, satur sensitīvus datus. Tiks pievienota paroles aizsardzība.")
            password = simpledialog.askstring("Paroles aizsardzība", "Ievadiet paroli PDF failam:", show='*',
                                              parent=self)
            if password:
                try:
                    reader = pypdf.PdfReader(out_path)
                    writer = pypdf.PdfWriter()

                    for page in reader.pages:
                        writer.add_page(page)

                    writer.encrypt(password)

                    # Pagaidu fails, lai saglabātu šifrēto PDF
                    encrypted_pdf_path = out_path.replace(".pdf", "_encrypted.pdf")
                    with open(encrypted_pdf_path, "wb") as f:
                        writer.write(f)

                    os.remove(out_path)  # Dzēš nešifrēto failu
                    os.rename(encrypted_pdf_path, out_path)  # Pārdēvē šifrēto failu uz oriģinālo nosaukumu
                    messagebox.showinfo("Gatavs", f"PDF veiksmīgi saglabāts un šifrēts:\n{out_path}")
                except Exception as e:
                    messagebox.showerror("Kļūda šifrēšanā", f"Neizdevās šifrēt PDF failu: {e}\n"
                                                            "PDF saglabāts bez paroles.")
                    messagebox.showinfo("Gatavs", f"PDF veiksmīgi saglabāts:\n{out_path}")
            else:
                messagebox.showinfo("Gatavs", f"PDF veiksmīgi saglabāts (bez paroles):\n{out_path}")
        else:
            messagebox.showinfo("Gatavs", f"PDF veiksmīgi saglabāts:\n{out_path}")

        # Pievieno failu iekšējai failu sistēmai atbilstošajā mapē
        target_folder_node["contents"].append({
            "type": "file",
            "name": os.path.basename(out_path),
            "filepath": out_path,
            "doc_id": doc_id,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "parent": target_folder_node  # Svarīgi atjaunināt parent atsauci
        })
        self.refresh_pdf_list()  # Atjauno failu sarakstu failu pārvaldības cilnē
        # JAUNS: Automātiskā augšupielāde
        if self.auto_upload_enabled.get():
            upload_target = self.auto_upload_target.get()
            # Izmanto dokumenta kategoriju kā attālo apakšmapi
            self.upload_file_to_remote(out_path, upload_target, document_category)

    def get_page_size(self, img_width, img_height):
        """Aprēķina PDF lapas izmēru, pamatojoties uz izvēlēto orientāciju un attēla izmēriem."""
        orientation = self.orientation_var.get()
        points_per_pixel = 72 / self.dpi_var.get()

        img_width_pt = img_width * points_per_pixel
        img_height_pt = img_height * points_per_pixel

        if orientation == "Tāds pats kā attēls":
            return (img_width_pt, img_height_pt)
        elif orientation == "Auto":
            return (img_width_pt, img_height_pt) if img_width_pt < img_height_pt else landscape(
                (img_width_pt, img_height_pt))
        elif orientation == "Portrets":
            return (min(img_width_pt, img_height_pt), max(img_width_pt, img_height_pt))
        elif orientation == "Ainava":
            return landscape((min(img_width_pt, img_height_pt), max(img_width_pt, img_height_pt)))
        elif orientation == "A4 Portrets":
            return A4
        elif orientation == "A4 Ainava":
            return landscape(A4)
        elif orientation == "Letter Portrets":
            return letter
        elif orientation == "Letter Ainava":
            return landscape(letter)
        else:
            return A4

    def crop_image(self):
        """Atver logu attēla apgriešanai."""
        if self.current_image_index == -1:
            messagebox.showwarning("Nav attēla", "Lūdzu, vispirms atlasiet attēlu, ko apgriezt.")
            return

        img_data = self.images[self.current_image_index]
        img = img_data["processed_img"].copy()

        crop_window = Toplevel(self)
        crop_window.title("Apgriezt attēlu")
        crop_window.geometry("800x600")
        crop_window.transient(self)
        crop_window.grab_set()

        crop_canvas = tk.Canvas(crop_window, bg="gray", cursor="cross")
        crop_canvas.pack(fill="both", expand=True)

        # Pārmēro attēlu, lai tas ietilptu kanvasā
        canvas_width = crop_canvas.winfo_width()
        canvas_height = crop_canvas.winfo_height()
        img_width, img_height = img.size

        # Pagaidām izmantojam fiksētu izmēru, lai iegūtu kanvasa izmērus
        # Pēc tam, kad logs ir parādīts, varam iegūt reālos izmērus
        crop_window.update_idletasks()
        canvas_width = crop_canvas.winfo_width()
        canvas_height = crop_canvas.winfo_height()

        if canvas_width == 0 or canvas_height == 0:  # Ja logs vēl nav pilnībā inicializēts
            canvas_width = 800  # Noklusējuma vērtības
            canvas_height = 600

        ratio = min(canvas_width / img_width, canvas_height / img_height)
        display_w = int(img_width * ratio)
        display_h = int(img_height * ratio)

        display_img = img.resize((display_w, display_h), Image.LANCZOS)
        original_img_tk = ImageTk.PhotoImage(display_img)
        crop_canvas.create_image(0, 0, anchor="nw", image=original_img_tk)
        crop_canvas.image = original_img_tk

        rect_id = None
        start_x = start_y = end_x = end_y = 0

        def on_button_press(event):
            nonlocal start_x, start_y, rect_id
            start_x = crop_canvas.canvasx(event.x)
            start_y = crop_canvas.canvasy(event.y)
            if rect_id:
                crop_canvas.delete(rect_id)
            rect_id = crop_canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="red", width=2)

        def on_mouse_drag(event):
            nonlocal end_x, end_y
            end_x = crop_canvas.canvasx(event.x)
            end_y = crop_canvas.canvasy(event.y)
            crop_canvas.coords(rect_id, start_x, start_y, end_x, end_y)

        def on_button_release(event):
            nonlocal end_x, end_y
            end_x = crop_canvas.canvasx(event.x)
            end_y = crop_canvas.canvasy(event.y)

            x1, y1 = min(start_x, end_x), min(start_y, end_y)
            x2, y2 = max(start_x, end_x), max(start_y, end_y)

            # Pārrēķina koordinātas uz oriģinālā attēla izmēriem
            # Ņem vērā mērogošanas koeficientu, ko izmantoja attēla parādīšanai kanvasā
            original_x1 = int(x1 / ratio)
            original_y1 = int(y1 / ratio)
            original_x2 = int(x2 / ratio)
            original_y2 = int(y2 / ratio)

            try:
                cropped_img = img.crop((original_x1, original_y1, original_x2, original_y2))
                img_data["processed_img"] = cropped_img
                self.show_image_preview(cropped_img)
                crop_window.destroy()
            except Exception as e:
                messagebox.showerror("Apgriešanas kļūda", f"Neizdevās apgriezt attēlu: {e}")

        crop_canvas.bind("<ButtonPress-1>", on_button_press)
        crop_canvas.bind("<B1-Motion>", on_mouse_drag)
        crop_canvas.bind("<ButtonRelease-1>", on_button_release)

        # Pielāgo kanvas izmēru, kad logs tiek parādīts
        crop_canvas.update_idletasks()
        crop_canvas.config(scrollregion=crop_canvas.bbox("all"))

    def rotate_90_degrees(self):
        """Pagriež pašreizējo attēlu par 90 grādiem pulksteņrādītāja virzienā."""
        if self.current_image_index == -1:
            messagebox.showwarning("Nav attēla", "Lūdzu, vispirms atlasiet attēlu.")
            return
        img_data = self.images[self.current_image_index]
        img = img_data["processed_img"]
        img = img.rotate(-90, expand=True, fillcolor=(255, 255, 255) if img.mode == 'RGB' else 255)
        img_data["processed_img"] = img
        self.show_image_preview(img)

    def flip_image(self, method):
        """Spoguļo pašreizējo attēlu (horizontāli vai vertikāli)."""
        if self.current_image_index == -1:
            messagebox.showwarning("Nav attēla", "Lūdzu, vispirms atlasiet attēlu.")
            return
        img_data = self.images[self.current_image_index]
        img = img_data["processed_img"]
        img = img.transpose(method)
        img_data["processed_img"] = img
        self.show_image_preview(img)

    def resize_image_dialog(self):
        """Atver dialoga logu attēla izmēru maiņai."""
        if self.current_image_index == -1:
            messagebox.showwarning("Nav attēla", "Lūdzu, vispirms atlasiet attēlu.")
            return

        img_data = self.images[self.current_image_index]
        img = img_data["processed_img"]

        resize_window = Toplevel(self)
        resize_window.title("Mainīt attēla izmērus")
        resize_window.transient(self)
        resize_window.grab_set()

        current_width, current_height = img.size

        ttk.Label(resize_window, text=f"Pašreizējie izmēri: {current_width}x{current_height} pikseļi").pack(pady=5)

        ttk.Label(resize_window, text="Jauns platums:").pack(pady=2)
        new_width_var = tk.IntVar(value=current_width)
        ttk.Entry(resize_window, textvariable=new_width_var).pack(pady=2)

        ttk.Label(resize_window, text="Jauns augstums:").pack(pady=2)
        new_height_var = tk.IntVar(value=current_height)
        ttk.Entry(resize_window, textvariable=new_height_var).pack(pady=2)

        keep_aspect_ratio_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(resize_window, text="Saglabāt proporcijas", variable=keep_aspect_ratio_var).pack(pady=5)

        def update_height(*args):
            if keep_aspect_ratio_var.get():
                try:
                    new_w = new_width_var.get()
                    if new_w > 0:
                        new_h = int(new_w * (current_height / current_width))
                        new_height_var.set(new_h)
                except:
                    pass

        def update_width(*args):
            if keep_aspect_ratio_var.get():
                try:
                    new_h = new_height_var.get()
                    if new_h > 0:
                        new_w = int(new_h * (current_width / current_height))
                        new_width_var.set(new_w)
                except:
                    pass

        new_width_var.trace_add("write", update_height)
        new_height_var.trace_add("write", update_width)

        def apply_resize():
            try:
                new_w = new_width_var.get()
                new_h = new_height_var.get()

                if new_w <= 0 or new_h <= 0:
                    messagebox.showwarning("Kļūda", "Platumam un augstumam jābūt pozitīviem skaitļiem.")
                    return

                resized_img = img.resize((new_w, new_h), Image.LANCZOS)
                img_data["processed_img"] = resized_img
                self.show_image_preview(resized_img)
                resize_window.destroy()

            except Exception as e:
                messagebox.showerror("Kļūda", f"Neizdevās mainīt izmērus: {e}")

        ttk.Button(resize_window, text="Mainīt izmērus", command=apply_resize).pack(pady=10)

    def auto_enhance_image(self):
        """Automātiski uzlabo pašreizējā attēla kontrastu un asumu."""
        if self.current_image_index == -1:
            messagebox.showwarning("Nav attēla", "Lūdzu, vispirms atlasiet attēlu.")
            return

        img_data = self.images[self.current_image_index]
        img = img_data["processed_img"].copy()

        img = ImageOps.autocontrast(img)
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.5)

        img_data["processed_img"] = img
        self.show_image_preview(img)
        messagebox.showinfo("Automātiska uzlabošana", "Attēls ir automātiski uzlabots (kontrasts un asums).")

    def show_image_histogram(self):
        """Parāda pašreizējā attēla krāsu histogrammu."""
        if self.current_image_index == -1:
            messagebox.showwarning("Nav attēla", "Lūdzu, vispirms atlasiet attēlu, lai rādītu histogrammu.")
            return

        img = self.images[self.current_image_index]["processed_img"]
        if img.mode != 'L' and img.mode != 'RGB':
            img = img.convert('RGB')  # Pārvērš uz RGB, ja nav atbalstīts režīms

        hist_window = Toplevel(self)
        hist_window.title("Attēla histogramma")
        hist_window.transient(self)
        hist_window.grab_set()

        canvas_hist = tk.Canvas(hist_window, width=300, height=200, bg="white")
        canvas_hist.pack(padx=10, pady=10)

        if img.mode == 'L':  # Pelēktoņi
            histogram = img.histogram()
            max_val = max(histogram)
            for i, val in enumerate(histogram):
                height = (val / max_val) * 180  # Mērogo augstumu
                canvas_hist.create_rectangle(i, 200 - height, i + 1, 200, fill="gray")
        elif img.mode == 'RGB':  # Krāsains attēls
            r, g, b = img.split()
            hist_r = r.histogram()
            hist_g = g.histogram()
            hist_b = b.histogram()
            max_val = max(max(hist_r), max(hist_g), max(hist_b))

            for i in range(256):
                height_r = (hist_r[i] / max_val) * 180
                height_g = (hist_g[i] / max_val) * 180
                height_b = (hist_b[i] / max_val) * 180
                canvas_hist.create_rectangle(i, 200 - height_r, i + 1, 200, fill="red", outline="red")
                canvas_hist.create_rectangle(i, 200 - height_g, i + 1, 200, fill="green", outline="green")
                canvas_hist.create_rectangle(i, 200 - height_b, i + 1, 200, fill="blue", outline="blue")
        else:
            messagebox.showwarning("Histogramma", "Histogramma nav pieejama šim attēla režīmam.")
            hist_window.destroy()

    def show_image_metadata(self):
        """Parāda pašreizējā attēla metadatus (EXIF utt.)."""
        if self.current_image_index == -1:
            messagebox.showwarning("Nav attēla", "Lūdzu, vispirms atlasiet attēlu, lai rādītu metadatus.")
            return

        img = self.images[self.current_image_index]["original_img"]
        metadata = img.info

        if not metadata:
            messagebox.showinfo("Metadati", "Šim attēlam nav pieejami metadati (EXIF utt.).")
            return

        meta_str = "Attēla metadati:\n"
        for key, value in metadata.items():
            meta_str += f"{key}: {value}\n"

        meta_window = Toplevel(self)
        meta_window.title("Attēla metadati")
        meta_window.transient(self)
        meta_window.grab_set()

        text_widget = tk.Text(meta_window, wrap="word", width=60, height=20)
        text_widget.pack(padx=10, pady=10)
        text_widget.insert(tk.END, meta_str)
        text_widget.config(state=DISABLED)  # Padara tekstu nelabojamu

    def show_color_palette(self):
        """Parāda pašreizējā attēla dominējošās krāsas."""
        if self.current_image_index == -1:
            messagebox.showwarning("Nav attēla", "Lūdzu, vispirms atlasiet attēlu, lai rādītu krāsu paleti.")
            return

        img = self.images[self.current_image_index]["processed_img"]
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Samazina attēlu, lai paātrinātu apstrādi
        img_small = img.resize((100, 100))
        colors = img_small.getcolors(img_small.size[0] * img_small.size[1])  # Iegūst visas krāsas un to skaitu

        if not colors:
            messagebox.showinfo("Krāsu palete", "Neizdevās iegūt krāsu informāciju.")
            return

        # Sakārto krāsas pēc biežuma (dominējošās krāsas)
        colors.sort(key=lambda x: x[0], reverse=True)
        top_colors = colors[:10]  # Top 10 dominējošās krāsas

        palette_window = Toplevel(self)
        palette_window.title("Attēla krāsu palete")
        palette_window.transient(self)
        palette_window.grab_set()

        canvas_palette = tk.Canvas(palette_window, width=300, height=150, bg="white")
        canvas_palette.pack(padx=10, pady=10)

        x_offset = 10
        y_offset = 10
        color_block_size = 30

        for count, (r, g, b) in top_colors:
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            canvas_palette.create_rectangle(x_offset, y_offset,
                                            x_offset + color_block_size, y_offset + color_block_size,
                                            fill=hex_color, outline="black")
            canvas_palette.create_text(x_offset + color_block_size + 5, y_offset + color_block_size / 2,
                                       anchor="w", text=f"{hex_color} (Count: {count})")
            y_offset += color_block_size + 5

    def compare_images(self):
        """Salīdzina divus attēlus un parāda atšķirības."""
        if self.current_image_index == -1:
            messagebox.showwarning("Nav attēla", "Lūdzu, vispirms atlasiet attēlu, ko salīdzināt.")
            return

        img1 = self.images[self.current_image_index]["processed_img"]

        filepaths = filedialog.askopenfilenames(
            title="Izvēlieties otru attēlu salīdzināšanai",
            filetypes=[("Attēlu faili", "*.png *.jpg *.jpeg *.tif *.tiff *.bmp"), ("Visi faili", "*.*")]
        )
        if not filepaths:
            return

        try:
            img2 = Image.open(filepaths[0])
            if img1.size != img2.size:
                messagebox.showwarning("Izmēru neatbilstība", "Attēliem jābūt vienāda izmēra salīdzināšanai.")
                return
            if img1.mode != img2.mode:
                img2 = img2.convert(img1.mode)

            diff_img = ImageChops.difference(img1, img2)

            # Parāda atšķirību attēlu
            diff_window = Toplevel(self)
            diff_window.title("Attēlu atšķirības")
            diff_window.transient(self)
            diff_window.grab_set()

            diff_canvas = tk.Canvas(diff_window, bg="black")
            diff_canvas.pack(fill="both", expand=True)

            # Pielāgo attēlu kanvasa izmēram
            diff_window.update_idletasks()  # Atjaunina loga izmērus, lai iegūtu pareizus canvas_width/height
            canvas_width = diff_canvas.winfo_width()
            canvas_height = diff_canvas.winfo_height()

            if canvas_width == 0 or canvas_height == 0:  # Fallback if window not yet rendered
                canvas_width = 600
                canvas_height = 400

            display_diff_img = diff_img.resize((canvas_width, canvas_height), Image.LANCZOS)
            self.diff_photo = ImageTk.PhotoImage(display_diff_img)
            diff_canvas.create_image(0, 0, anchor="nw", image=self.diff_photo)
            diff_canvas.image = self.diff_photo

            messagebox.showinfo("Attēlu salīdzināšana",
                                "Atšķirību attēls ir parādīts jaunā logā. Jo gaišāks pikselis, jo lielāka atšķirība.")

        except Exception as e:
            messagebox.showerror("Kļūda", f"Neizdevās salīdzināt attēlus: {e}")

    def evaluate_image_quality(self):
        """Novērtē pašreizējā attēla kvalitāti (piem., trokšņa līmeni, asumu)."""
        if self.current_image_index == -1:
            messagebox.showwarning("Nav attēla", "Lūdzu, vispirms atlasiet attēlu.")
            return

        img = self.images[self.current_image_index]["processed_img"]

        # Vienkāršota asuma un trokšņa novērtēšana
        # Asums: Augsta frekvence attēlā (Laplacian variants)
        if img.mode != 'L':
            img_gray = img.convert('L')
        else:
            img_gray = img

        img_np = np.array(img_gray)

        if OPENCV_AVAILABLE:
            # Asums, izmantojot Laplasiāna operatoru
            laplacian_var = cv2.Laplacian(img_np, cv2.CV_64F).var()

            # Trokšņa līmenis (vienkāršots: standarta novirze pelēktoņu attēlā)
            noise_level = np.std(img_np)

            quality_report = f"Attēla kvalitātes novērtējums:\n" \
                             f"Asums (Laplacian Variance): {laplacian_var:.2f}\n" \
                             f"Trokšņa līmenis (Standard Deviation): {noise_level:.2f}\n\n" \
                             f"Augstāka Laplasiāna variācija norāda uz lielāku asumu.\n" \
                             f"Augstāka standarta novirze var norādīt uz lielāku trokšņa līmeni."
        else:
            quality_report = "OpenCV nav pieejams, tāpēc kvalitātes novērtēšana ir ierobežota.\n" \
                             "Lūdzu, instalējiet 'opencv-python' un 'numpy', lai iegūtu pilnu funkcionalitāti."

        messagebox.showinfo("Attēla kvalitāte", quality_report)

    def extract_text_from_region(self):
        """Ļauj lietotājam atlasīt apgabalu attēlā un veikt OCR tikai šajā apgabalā."""
        if self.current_image_index == -1:
            messagebox.showwarning("Nav attēla", "Lūdzu, vispirms atlasiet attēlu.")
            return

        img = self.images[self.current_image_index]["processed_img"].copy()

        extract_window = Toplevel(self)
        extract_window.title("Izvilkt tekstu no apgabala")
        extract_window.geometry("800x600")
        extract_window.transient(self)
        extract_window.grab_set()

        extract_canvas = tk.Canvas(extract_window, bg="gray", cursor="cross")
        extract_canvas.pack(fill="both", expand=True)

        # Pārmēro attēlu, lai tas ietilptu kanvasā
        extract_window.update_idletasks()
        canvas_width = extract_canvas.winfo_width()
        canvas_height = extract_canvas.winfo_height()
        img_width, img_height = img.size

        ratio = min(canvas_width / img_width, canvas_height / img_height)
        display_w = int(img_width * ratio)
        display_h = int(img_height * ratio)

        display_img = img.resize((display_w, display_h), Image.LANCZOS)
        original_img_tk = ImageTk.PhotoImage(display_img)
        extract_canvas.create_image(0, 0, anchor="nw", image=original_img_tk)
        extract_canvas.image = original_img_tk

        rect_id = None
        start_x = start_y = end_x = end_y = 0

        def on_button_press(event):
            nonlocal start_x, start_y, rect_id
            start_x = extract_canvas.canvasx(event.x)
            start_y = extract_canvas.canvasy(event.y)
            if rect_id:
                extract_canvas.delete(rect_id)
            rect_id = extract_canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="blue", width=2)

        def on_mouse_drag(event):
            nonlocal end_x, end_y
            end_x = extract_canvas.canvasx(event.x)
            end_y = extract_canvas.canvasy(event.y)
            extract_canvas.coords(rect_id, start_x, start_y, end_x, end_y)

        def on_button_release(event):
            nonlocal end_x, end_y
            end_x = extract_canvas.canvasx(event.x)
            end_y = extract_canvas.canvasy(event.y)

            x1, y1 = min(start_x, end_x), min(start_y, end_y)
            x2, y2 = max(start_x, end_x), max(start_y, end_y)

            original_x1 = int(x1 / ratio)
            original_y1 = int(y1 / ratio)
            original_x2 = int(x2 / ratio)
            original_y2 = int(y2 / ratio)

            try:
                region_img = img.crop((original_x1, original_y1, original_x2, original_y2))
                extracted_text = pytesseract.image_to_string(region_img, lang="lav+eng")  # Pieņemam latviešu un angļu

                messagebox.showinfo("Izvilktais teksts", f"Teksts no atlasītā apgabala:\n\n{extracted_text}")
                extract_window.destroy()
            except Exception as e:
                messagebox.showerror("OCR kļūda", f"Neizdevās izvilkt tekstu no apgabala: {e}")

        extract_canvas.bind("<ButtonPress-1>", on_button_press)
        extract_canvas.bind("<B1-Motion>", on_mouse_drag)  # Changed from draw_mask to on_mouse_drag
        extract_canvas.bind("<ButtonRelease-1>", on_button_release)

    def convert_color_space(self):
        """Konvertē pašreizējā attēla krāsu telpu (piem., uz HSV, CMYK)."""
        if self.current_image_index == -1:
            messagebox.showwarning("Nav attēla", "Lūdzu, vispirms atlasiet attēlu.")
            return

        img_data = self.images[self.current_image_index]
        img = img_data["processed_img"].copy()

        color_space_window = Toplevel(self)
        color_space_window.title("Krāsu telpas konvertēšana")
        color_space_window.transient(self)
        color_space_window.grab_set()

        ttk.Label(color_space_window, text="Izvēlieties krāsu telpu:").pack(pady=5)
        color_space_var = tk.StringVar(value="RGB")
        color_space_options = ["RGB", "L (Grayscale)", "HSV (Requires OpenCV)", "CMYK"]
        color_space_combo = ttk.Combobox(color_space_window, textvariable=color_space_var, values=color_space_options,
                                         state="readonly")
        color_space_combo.pack(pady=5)

        def apply_conversion():
            selected_space = color_space_var.get()
            try:
                converted_img = None
                if selected_space == "RGB":
                    converted_img = img.convert("RGB")
                elif selected_space == "L (Grayscale)":
                    converted_img = img.convert("L")
                elif selected_space == "HSV (Requires OpenCV)":
                    if OPENCV_AVAILABLE:
                        img_np = np.array(img.convert('RGB'))
                        img_hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
                        converted_img = Image.fromarray(img_hsv)
                    else:
                        messagebox.showwarning("Trūkst bibliotēkas", "HSV konvertēšanai nepieciešams 'opencv-python'.")
                        return
                elif selected_space == "CMYK":
                    converted_img = img.convert("CMYK")
                else:
                    return

                if converted_img:
                    img_data["processed_img"] = converted_img
                    self.show_image_preview(converted_img)
                    color_space_window.destroy()
            except Exception as e:
                messagebox.showerror("Kļūda", f"Neizdevās konvertēt krāsu telpu: {e}")

        ttk.Button(color_space_window, text="Konvertēt", command=apply_conversion).pack(pady=10)

    def add_watermark(self):
        """Pievieno ūdenszīmi pašreizējam attēlam."""
        if self.current_image_index == -1:
            messagebox.showwarning("Nav attēla", "Lūdzu, vispirms atlasiet attēlu.")
            return

        img_data = self.images[self.current_image_index]
        img = img_data["processed_img"].copy()

        watermark_text = simpledialog.askstring("Ūdenszīme", "Ievadiet ūdenszīmes tekstu:", parent=self)
        if watermark_text:
            try:
                draw = ImageDraw.Draw(img)
                font_size = 40
                try:
                    # Mēģina ielādēt sistēmas fontu
                    font = ImageFont.truetype("arial.ttf", font_size)
                except IOError:
                    # Ja sistēmas fonts nav pieejams, izmanto noklusējuma fontu
                    font = ImageFont.load_default()

                # Aprēķina teksta izmērus
                bbox = draw.textbbox((0, 0), watermark_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                # Centra pozīcija
                x = (img.width - text_width) / 2
                y = (img.height - text_height) / 2

                # Pievieno tekstu ar caurspīdīgumu
                # Lai pievienotu caurspīdīgu tekstu, attēlam jābūt ar alfa kanālu (RGBA)
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')

                temp_draw = ImageDraw.Draw(img)
                temp_draw.text((x, y), watermark_text, font=font,
                               fill=(128, 128, 128, 128))  # Pelēka, daļēji caurspīdīga

                img_data["processed_img"] = img
                self.show_image_preview(img)
                messagebox.showinfo("Ūdenszīme", "Ūdenszīme veiksmīgi pievienota.")
            except Exception as e:
                messagebox.showerror("Kļūda", f"Neizdevās pievienot ūdenszīmi: {e}")
        else:
            messagebox.showinfo("Ūdenszīme", "Ūdenszīmes teksts netika ievadīts.")

    def create_image_mosaic(self):
        """Izveido attēla mozaīku no vairākiem attēliem."""
        filepaths = filedialog.askopenfilenames(
            title="Izvēlieties attēlus mozaīkai",
            filetypes=[("Attēlu faili", "*.png *.jpg *.jpeg *.tif *.tiff *.bmp"), ("Visi faili", "*.*")]
        )
        if not filepaths:
            return

        images_to_mosaic = []
        for fp in filepaths:
            try:
                images_to_mosaic.append(Image.open(fp))
            except Exception as e:
                messagebox.showwarning("Kļūda", f"Neizdevās ielādēt attēlu {fp}: {e}")
                continue

        if not images_to_mosaic:
            messagebox.showwarning("Nav attēlu", "Netika ielādēts neviens attēls mozaīkai.")
            return

        # Vienkāršota mozaīka: saliek attēlus vienā rindā
        widths, heights = zip(*(i.size for i in images_to_mosaic))
        max_height = max(heights)
        total_width = sum(widths)

        mosaic_img = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for img in images_to_mosaic:
            mosaic_img.paste(img, (x_offset, 0))
            x_offset += img.width

        # Parāda mozaīku
        mosaic_window = Toplevel(self)
        mosaic_window.title("Attēla mozaīka")
        mosaic_window.transient(self)
        mosaic_window.grab_set()

        mosaic_canvas = tk.Canvas(mosaic_window, bg="black")
        mosaic_canvas.pack(fill="both", expand=True)

        # Pielāgo attēlu kanvasa izmēram
        mosaic_window.update_idletasks()
        canvas_width = mosaic_canvas.winfo_width()
        canvas_height = mosaic_canvas.winfo_height()

        if canvas_width == 0 or canvas_height == 0:
            canvas_width = 600
            canvas_height = 400

        display_mosaic_img = mosaic_img.resize((canvas_width, canvas_height),
                                               Image.LANCZOS)
        self.mosaic_photo = ImageTk.PhotoImage(display_mosaic_img)
        mosaic_canvas.create_image(0, 0, anchor="nw", image=self.mosaic_photo)
        mosaic_canvas.image = self.mosaic_photo

        messagebox.showinfo("Attēla mozaīka", "Attēlu mozaīka izveidota un parādīta jaunā logā.")

    def stitch_images(self):
        """Saliek vairākus attēlus kopā, lai izveidotu panorāmu vai lielāku attēlu (vienkāršota versija)."""
        if not OPENCV_AVAILABLE:
            messagebox.showwarning("Trūkst bibliotēkas", "Attēlu salikšanai nepieciešams 'opencv-python'.")
            return

        filepaths = filedialog.askopenfilenames(
            title="Izvēlieties attēlus salikšanai (vismaz 2)",
            filetypes=[("Attēlu faili", "*.png *.jpg *.jpeg *.tif *.tiff *.bmp"), ("Visi faili", "*.*")]
        )
        if not filepaths or len(filepaths) < 2:
            messagebox.showwarning("Nav pietiekami daudz attēlu", "Lūdzu, atlasiet vismaz divus attēlus salikšanai.")
            return

        images_to_stitch = []
        for fp in filepaths:
            try:
                img_pil = Image.open(fp).convert('RGB')
                images_to_stitch.append(cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR))
            except Exception as e:
                messagebox.showwarning("Kļūda", f"Neizdevās ielādēt attēlu {fp}: {e}")
                continue

        if len(images_to_stitch) < 2:
            messagebox.showwarning("Nav pietiekami daudz attēlu", "Netika ielādēts pietiekami daudz attēlu salikšanai.")
            return

        try:
            # Izmanto OpenCV Sticher klasi
            stitcher = cv2.Stitcher_create()
            status, stitched_image = stitcher.stitch(images_to_stitch)

            if status == cv2.Stitcher.OK:
                stitched_image_pil = Image.fromarray(cv2.cvtColor(stitched_image, cv2.COLOR_BGR2RGB))

                # Parāda salikto attēlu
                stitch_window = Toplevel(self)
                stitch_window.title("Saliktais attēls")
                stitch_window.transient(self)
                stitch_window.grab_set()

                stitch_canvas = tk.Canvas(stitch_window, bg="black")
                stitch_canvas.pack(fill="both", expand=True)

                # Pielāgo attēlu kanvasa izmēram
                stitch_window.update_idletasks()
                canvas_width = stitch_canvas.winfo_width()
                canvas_height = stitch_canvas.winfo_height()

                if canvas_width == 0 or canvas_height == 0:
                    canvas_width = 600
                    canvas_height = 400

                display_stitched_img = stitched_image_pil.resize(
                    (canvas_width, canvas_height), Image.LANCZOS)
                self.stitch_photo = ImageTk.PhotoImage(display_stitched_img)
                stitch_canvas.create_image(0, 0, anchor="nw", image=self.stitch_photo)
                stitch_canvas.image = self.stitch_photo

                messagebox.showinfo("Attēlu salikšana", "Attēli veiksmīgi salikti un parādīti jaunā logā.")
            else:
                messagebox.showerror("Kļūda", f"Neizdevās salikt attēlus. Statuss: {status}")
        except Exception as e:
            messagebox.showerror("Kļūda", f"Kļūda attēlu salikšanas procesā: {e}")

    def image_inpainting(self):
        """Aizpilda trūkstošās vai bojātās attēla daļas (vienkāršota versija)."""
        if self.current_image_index == -1:
            messagebox.showwarning("Nav attēla", "Lūdzu, vispirms atlasiet attēlu.")
            return
        if not OPENCV_AVAILABLE:
            messagebox.showwarning("Trūkst bibliotēkas",
                                   "Attēla atjaunošanai (inpainting) nepieciešams 'opencv-python'.")
            return

        img_data = self.images[self.current_image_index]
        img = img_data["processed_img"].copy()

        inpainting_window = Toplevel(self)
        inpainting_window.title("Attēla atjaunošana (Inpainting)")
        inpainting_window.geometry("800x600")
        inpainting_window.transient(self)
        inpainting_window.grab_set()

        inpainting_canvas = tk.Canvas(inpainting_window, bg="gray")
        inpainting_canvas.pack(fill="both", expand=True)

        # Pārmēro attēlu, lai tas ietilptu kanvasā
        inpainting_window.update_idletasks()
        canvas_width = inpainting_canvas.winfo_width()
        canvas_height = inpainting_canvas.winfo_height()
        img_width, img_height = img.size

        ratio = min(canvas_width / img_width, canvas_height / img_height)
        display_w = int(img_width * ratio)
        display_h = int(img_height * ratio)

        display_img = img.resize((display_w, display_h), Image.LANCZOS)
        self.inpainting_photo = ImageTk.PhotoImage(display_img)
        inpainting_canvas.create_image(0, 0, anchor="nw", image=self.inpainting_photo)
        inpainting_canvas.image = self.inpainting_photo

        mask = np.zeros((img_height, img_width), dtype=np.uint8)  # Maska, kurā iezīmēs bojātās vietas
        drawing = False
        last_x, last_y = 0, 0

        def start_draw(event):
            nonlocal drawing, last_x, last_y
            drawing = True
            last_x, last_y = event.x, event.y

        def draw_mask(event):
            nonlocal last_x, last_y
            if drawing:
                inpainting_canvas.create_line(last_x, last_y, event.x, event.y,
                                              width=10, fill="red", capstyle=tk.ROUND, smooth=tk.TRUE)
                # Pārrēķina uz oriģinālā attēla koordinātām
                orig_x1, orig_y1 = int(last_x / ratio), int(last_y / ratio)
                orig_x2, orig_y2 = int(event.x / ratio), int(event.y / ratio)
                cv2.line(mask, (orig_x1, orig_y1), (orig_x2, orig_y2), 255, 10)  # Zīmē maskā
                last_x, last_y = event.x, event.y

        def stop_draw(event):
            nonlocal drawing
            drawing = False

        inpainting_canvas.bind("<Button-1>", start_draw)
        inpainting_canvas.bind("<B1-Motion>", draw_mask)
        inpainting_canvas.bind("<ButtonRelease-1>", stop_draw)

        def apply_inpainting():
            try:
                img_np = np.array(img.convert('RGB'))
                # Izmanto OpenCV inpainting funkciju
                # cv2.INPAINT_TELEA vai cv2.INPAINT_NS
                restored_img_np = cv2.inpaint(img_np, mask, 3, cv2.INPAINT_TELEA)
                restored_img_pil = Image.fromarray(cv2.cvtColor(restored_img_np, cv2.COLOR_BGR2RGB))

                img_data["processed_img"] = restored_img_pil
                self.show_image_preview(restored_img_pil)
                inpainting_window.destroy()
                messagebox.showinfo("Attēla atjaunošana", "Attēls veiksmīgi atjaunots.")
            except Exception as e:
                messagebox.showerror("Kļūda", f"Neizdevās veikt attēla atjaunošanu: {e}")

        ttk.Button(inpainting_window, text="Pielietot atjaunošanu", command=apply_inpainting).pack(pady=10)

    def stylize_image(self):
        """Pielieto mākslinieciskus stilus attēlam (vienkāršota versija ar filtriem)."""
        if self.current_image_index == -1:
            messagebox.showwarning("Nav attēla", "Lūdzu, vispirms atlasiet attēlu.")
            return

        img_data = self.images[self.current_image_index]
        img = img_data["processed_img"].copy()

        stylize_window = Toplevel(self)
        stylize_window.title("Attēla stilizācija")
        stylize_window.transient(self)
        stylize_window.grab_set()

        ttk.Label(stylize_window, text="Izvēlieties stilu:").pack(pady=5)
        style_var = tk.StringVar(value="Oriģināls")
        styles = ["Oriģināls", "Zīmējums (FIND_EDGES)", "Reljefs (EMBOSS)", "Kontūras (CONTOUR)", "Gausiāns (BLUR)"]
        style_combo = ttk.Combobox(stylize_window, textvariable=style_var, values=styles, state="readonly")
        style_combo.pack(pady=5)

        def apply_style():
            selected_style = style_var.get()
            styled_img = img.copy()
            try:
                if selected_style == "Zīmējums (FIND_EDGES)":
                    styled_img = styled_img.filter(ImageFilter.FIND_EDGES)
                elif selected_style == "Reljefs (EMBOSS)":
                    styled_img = styled_img.filter(ImageFilter.EMBOSS)
                elif selected_style == "Kontūras (CONTOUR)":
                    styled_img = styled_img.filter(ImageFilter.CONTOUR)
                elif selected_style == "Gausiāns (BLUR)":
                    styled_img = styled_img.filter(ImageFilter.GaussianBlur(radius=2))
                # "Oriģināls" neko nedara

                img_data["processed_img"] = styled_img
                self.show_image_preview(styled_img)
                stylize_window.destroy()
            except Exception as e:
                messagebox.showerror("Kļūda", f"Neizdevās pielietot stilu: {e}")

        ttk.Button(stylize_window, text="Pielietot stilu", command=apply_style).pack(pady=10)

    def geometric_transformations(self):
        """Veic ģeometriskās transformācijas attēlam (vienkāršota versija)."""
        if self.current_image_index == -1:
            messagebox.showwarning("Nav attēla", "Lūdzu, vispirms atlasiet attēlu.")
            return

        img_data = self.images[self.current_image_index]
        img = img_data["processed_img"].copy()

        transform_window = Toplevel(self)
        transform_window.title("Ģeometriskās transformācijas")
        transform_window.transient(self)
        transform_window.grab_set()

        ttk.Label(transform_window, text="Izvēlieties transformāciju:").pack(pady=5)
        transform_type_var = tk.StringVar(value="Nobīde")
        transform_types = ["Nobīde", "Mērogošana", "Bīde (Shear)"]
        transform_type_combo = ttk.Combobox(transform_window, textvariable=transform_type_var, values=transform_types,
                                            state="readonly")
        transform_type_combo.pack(pady=5)

        # Nobīdes parametri
        ttk.Label(transform_window, text="X nobīde (pikseļi):").pack(pady=2)
        offset_x_var = tk.IntVar(value=0)
        ttk.Entry(transform_window, textvariable=offset_x_var).pack(pady=2)

        ttk.Label(transform_window, text="Y nobīde (pikseļi):").pack(pady=2)
        offset_y_var = tk.IntVar(value=0)
        ttk.Entry(transform_window, textvariable=offset_y_var).pack(pady=2)

        # Mērogošanas parametri
        ttk.Label(transform_window, text="Mērogošanas faktors:").pack(pady=2)
        scale_factor_var = tk.DoubleVar(value=1.0)
        ttk.Entry(transform_window, textvariable=scale_factor_var).pack(pady=2)

        # Bīdes parametri
        ttk.Label(transform_window, text="X bīdes faktors:").pack(pady=2)
        shear_x_var = tk.DoubleVar(value=0.0)
        ttk.Entry(transform_window, textvariable=shear_x_var).pack(pady=2)

        ttk.Label(transform_window, text="Y bīdes faktors:").pack(pady=2)
        shear_y_var = tk.DoubleVar(value=0.0)
        ttk.Entry(transform_window, textvariable=shear_y_var).pack(pady=2)

        def apply_transform():
            selected_transform = transform_type_var.get()
            transformed_img = img.copy()
            try:
                if selected_transform == "Nobīde":
                    offset_x = offset_x_var.get()
                    offset_y = offset_y_var.get()
                    transformed_img = ImageChops.offset(transformed_img, offset_x, offset_y)
                elif selected_transform == "Mērogošana":
                    scale_factor = scale_factor_var.get()
                    new_width = int(img.width * scale_factor)
                    new_height = int(img.height * scale_factor)
                    transformed_img = transformed_img.resize((new_width, new_height), Image.LANCZOS)
                elif selected_transform == "Bīde (Shear)":
                    shear_x = shear_x_var.get()
                    shear_y = shear_y_var.get()
                    # Bīdes transformācija ar affine transformāciju
                    # Matrica: [[1, shear_x, 0], [shear_y, 1, 0]]
                    transformed_img = transformed_img.transform(
                        transformed_img.size, Image.AFFINE, (1, shear_x, 0, shear_y, 1, 0)
                    )

                img_data["processed_img"] = transformed_img
                self.show_image_preview(transformed_img)
                transform_window.destroy()
            except Exception as e:
                messagebox.showerror("Kļūda", f"Neizdevās veikt ģeometrisko transformāciju: {e}")

        ttk.Button(transform_window, text="Pielietot transformāciju", command=apply_transform).pack(pady=10)

    def check_ocr_languages(self):
        """Pārbauda, vai atlasītās OCR valodas ir pieejamas Tesseract instalācijā."""
        try:
            available_langs = pytesseract.get_languages(config='')
            selected_langs = []
            for lang_name, var in self.lang_vars.items():
                if var.get():
                    selected_langs.append(self.lang_options[lang_name])

            missing_langs = [lang for lang in selected_langs if lang not in available_langs]

            if not selected_langs:
                messagebox.showinfo("OCR valodu pārbaude", "Nav atlasīta neviena OCR valoda.")
            elif not missing_langs:
                messagebox.showinfo("OCR valodu pārbaude",
                                    "Visas atlasītās OCR valodas ir pieejamas Tesseract instalācijā.")
            else:
                messagebox.showwarning("OCR valodu pārbaude",
                                       f"Trūkst šādu atlasīto OCR valodu Tesseract instalācijā:\n{', '.join(missing_langs)}\n"
                                       "Lūdzu, instalējiet tās, lai nodrošinātu pareizu OCR darbību.")
        except pytesseract.TesseractNotFoundError:
            messagebox.showerror("Kļūda", "Tesseract nav atrasts. Lūdzu, pārbaudiet Tesseract ceļu iestatījumos.")
        except Exception as e:
            messagebox.showerror("Kļūda", f"Neizdevās pārbaudīt OCR valodas: {e}")

    def browse_scan_folder(self):
        """Atver dialogu, lai izvēlētos mapi automātiskai skenēšanai."""
        path = filedialog.askdirectory(title="Izvēlieties mapi automātiskai skenēšanai")
        if path:
            self.scan_folder_path.set(path)
            self.settings["scan_folder_path"] = path # Uzreiz saglabā iestatījumos
            self.save_app_settings()
            if self.auto_scan_enabled.get():
                self.stop_auto_scan()
                self.start_auto_scan() # Restartē uzraudzību ar jauno mapi

    def toggle_auto_scan(self):
        """Ieslēdz vai izslēdz automātisko skenēšanu."""
        if self.auto_scan_enabled.get():
            self.start_auto_scan()
        else:
            self.stop_auto_scan()
        self.update_auto_scan_status()
        self.settings["auto_scan_enabled"] = self.auto_scan_enabled.get() # Uzreiz saglabā iestatījumos
        self.save_app_settings()

    def update_remote_storage_fields(self, event=None):
        """Atjaunina attālinātās glabāšanas iestatījumu lauku redzamību."""
        storage_type = self.remote_storage_type.get()
        if storage_type == "FTP" or storage_type == "SFTP":
            self.ftp_settings_frame.grid()
            self.google_drive_settings_frame.grid_remove()
        elif storage_type == "Google Drive":
            self.ftp_settings_frame.grid_remove()
            self.google_drive_settings_frame.grid()
        else:  # Local
            self.ftp_settings_frame.grid_remove()
            self.google_drive_settings_frame.grid_remove()

    def test_ftp_connection(self):
        """Pārbauda FTP/SFTP savienojumu."""
        host = self.ftp_host.get()
        port = self.ftp_port.get()
        user = self.ftp_user.get()
        password = self.ftp_pass.get()
        use_sftp = self.ftp_use_sftp.get()

        if not host or not user or not password:
            messagebox.showwarning("Trūkst datu", "Lūdzu, ievadiet FTP/SFTP hostu, lietotājvārdu un paroli.")
            return

        try:
            if use_sftp:
                import paramiko
                transport = paramiko.Transport((host, port))
                transport.connect(username=user, password=password)
                sftp = paramiko.SFTPClient.from_transport(transport)
                sftp.close()
                transport.close()
                messagebox.showinfo("Savienojums", "SFTP savienojums veiksmīgs!")
            else:
                import ftplib
                ftp = ftplib.FTP()
                ftp.connect(host, port)
                ftp.login(user, password)
                ftp.quit()
                messagebox.showinfo("Savienojums", "FTP savienojums veiksmīgs!")
        except Exception as e:
            messagebox.showerror("Kļūda", f"Neizdevās izveidot savienojumu: {e}")

    def browse_google_credentials(self):
        """Atver dialogu Google Drive akreditācijas faila izvēlei."""
        path = filedialog.askopenfilename(title="Izvēlieties Google Drive credentials.json",
                                          filetypes=[("JSON faili", "*.json")])
        if path:
            self.google_drive_credentials_path.set(path)
            self.save_app_settings()

    def browse_google_token(self):
        """Atver dialogu Google Drive token faila izvēlei."""
        path = filedialog.askopenfilename(title="Izvēlieties Google Drive token.json",
                                          filetypes=[("JSON faili", "*.json")])
        if path:
            self.google_drive_token_path.set(path)
            self.save_app_settings()

    def authorize_google_drive(self):
        """Autorizējas Google Drive API."""
        try:
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials

            creds = None
            token_path = self.google_drive_token_path.get()
            credentials_path = self.google_drive_credentials_path.get()

            if os.path.exists(token_path):
                creds = Credentials.from_authorized_user_file(token_path,
                                                              ['https://www.googleapis.com/auth/drive.file'])

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not os.path.exists(credentials_path):
                        messagebox.showerror("Kļūda", f"Akreditācijas fails '{credentials_path}' nav atrasts.\n"
                                                      "Lūdzu, lejupielādējiet 'credentials.json' no Google Cloud Console.")
                        return

                    flow = InstalledAppFlow.from_client_secrets_file(
                        credentials_path, ['https://www.googleapis.com/auth/drive.file'])
                    creds = flow.run_local_server(port=0)

                with open(token_path, 'w') as token:
                    token.write(creds.to_json())

            messagebox.showinfo("Google Drive", "Google Drive autorizācija veiksmīga!")
            # Šeit varētu inicializēt Google Drive servisu, ja nepieciešams tūlītējai lietošanai
            # from googleapiclient.discovery import build
            # self.google_drive_service = build('drive', 'v3', credentials=creds)

        except Exception as e:
            messagebox.showerror("Kļūda", f"Google Drive autorizācijas kļūda: {e}")

    def toggle_auto_upload(self):
        """Ieslēdz vai izslēdz automātisko augšupielādi."""
        self.settings["auto_upload_enabled"] = self.auto_upload_enabled.get()
        self.settings["auto_upload_target"] = self.auto_upload_target.get()
        self.save_app_settings()
        messagebox.showinfo("Automātiskā augšupielāde",
                            f"Automātiskā augšupielāde ir {'ieslēgta' if self.auto_upload_enabled.get() else 'izslēgta'}.")

    def refresh_scanned_docs_list(self):
        """Atjaunina skenēto dokumentu sarakstu automatizācijas cilnē."""
        self.scanned_docs_listbox.delete(0, tk.END)
        scan_path = self.scan_folder_path.get()
        if not os.path.exists(scan_path):
            os.makedirs(scan_path, exist_ok=True)

        for filename in os.listdir(scan_path):
            filepath = os.path.join(scan_path, filename)
            if os.path.isfile(filepath) and filename.lower().endswith(
                    ('.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp', '.pdf')):
                # Pārbauda, vai dokuments ir apstrādāts (vienkāršots variants)
                # Reālā sistēmā varētu būt nepieciešams saglabāt apstrādāto failu sarakstu vai pievienot metadatus
                is_processed = False
                for item in self.internal_file_system["contents"]:
                    if item["type"] == "folder":
                        for doc in item["contents"]:
                            if doc["type"] == "file" and os.path.basename(doc["filepath"]) == filename:
                                is_processed = True
                                break
                        if is_processed: break

                status = "Skenēts un apstrādāts" if is_processed else "Gaida apstrādi"
                self.scanned_docs_listbox.insert(tk.END, f"{filename} - [{status}]")

    def on_scanned_doc_select(self, event=None):
        """Apstrādā skenēta dokumenta atlasi sarakstā."""
        pass  # Pašlaik nedara neko, var pievienot priekšskatījumu vai apstrādes opcijas

    def open_scanned_doc_location(self, event=None):
        """Atver skenētā dokumenta atrašanās vietu sistēmā."""
        selection = self.scanned_docs_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        filename_with_status = self.scanned_docs_listbox.get(index)
        filename = filename_with_status.split(" - ")[0]  # Iegūst tikai faila nosaukumu
        filepath = os.path.join(self.scan_folder_path.get(), filename)

        if os.path.exists(filepath):
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(os.path.dirname(filepath))
                elif os.name == 'posix':  # macOS, Linux
                    import subprocess
                    import sys
                    if sys.platform == 'darwin':  # macOS
                        subprocess.Popen(['open', '-R', filepath])
                    else:  # Linux
                        subprocess.Popen(['xdg-open', os.path.dirname(filepath)])
            except Exception as e:
                messagebox.showerror("Kļūda", f"Neizdevās atvērt faila atrašanās vietu:\n{e}")
        else:
            messagebox.showwarning("Fails nav atrasts", "Skenētais fails nav atrasts norādītajā vietā.")

    def upload_file_to_remote(self, local_filepath, remote_target, remote_path=None):
        """
        Augšupielādē failu uz attālinātu glabāšanas vietu.
        remote_target var būt "FTP", "SFTP", "Google Drive".
        remote_path ir attālā mape, kurā saglabāt.
        """
        if not self.auto_upload_enabled.get():
            return  # Ja automātiskā augšupielāde nav ieslēgta, neko nedara

        try:
            if remote_target == "FTP":
                import ftplib
                ftp = ftplib.FTP()
                ftp.connect(self.ftp_host.get(), self.ftp_port.get())
                ftp.login(self.ftp_user.get(), self.ftp_pass.get())

                # Pārliecinās, ka attālā mape eksistē vai izveido to
                current_dir = ftp.pwd()
                target_dir = os.path.join(self.ftp_remote_path.get(), remote_path).replace("\\",
                                                                                           "/") if remote_path else self.ftp_remote_path.get()

                # Mēģina mainīt direktoriju, ja neizdodas, mēģina izveidot
                try:
                    ftp.cwd(target_dir)
                except ftplib.error_perm:
                    # Mape neeksistē, mēģina izveidot
                    parts = target_dir.split('/')
                    for i in range(1, len(parts) + 1):
                        sub_dir = '/'.join(parts[:i])
                        try:
                            ftp.mkd(sub_dir)
                        except ftplib.error_perm:
                            pass  # Mape jau eksistē
                    ftp.cwd(target_dir)  # Pēc izveides ieiet mapē

                with open(local_filepath, 'rb') as f:
                    ftp.storbinary(f"STOR {os.path.basename(local_filepath)}", f)
                ftp.quit()
                messagebox.showinfo("Augšupielāde",
                                    f"Fails '{os.path.basename(local_filepath)}' veiksmīgi augšupielādēts uz FTP.")

            elif remote_target == "SFTP":
                import paramiko
                transport = paramiko.Transport((self.ftp_host.get(), self.ftp_port.get()))
                transport.connect(username=self.ftp_user.get(), password=self.ftp_pass.get())
                sftp = paramiko.SFTPClient.from_transport(transport)

                # Pārliecinās, ka attālā mape eksistē vai izveido to
                target_dir = os.path.join(self.ftp_remote_path.get(), remote_path).replace("\\",
                                                                                           "/") if remote_path else self.ftp_remote_path.get()

                # Rekursīvi izveido mapes
                parts = target_dir.split('/')
                current_path = ''
                for part in parts:
                    if part:  # Izvairās no tukšām daļām, ja ceļš sākas ar '/'
                        current_path = os.path.join(current_path, part).replace("\\", "/")
                        try:
                            sftp.stat(current_path)
                        except FileNotFoundError:
                            sftp.mkdir(current_path)

                sftp.put(local_filepath, os.path.join(target_dir, os.path.basename(local_filepath)).replace("\\", "/"))
                sftp.close()
                transport.close()
                messagebox.showinfo("Augšupielāde",
                                    f"Fails '{os.path.basename(local_filepath)}' veiksmīgi augšupielādēts uz SFTP.")

            elif remote_target == "Google Drive":
                from google_auth_oauthlib.flow import InstalledAppFlow
                from google.auth.transport.requests import Request
                from google.oauth2.credentials import Credentials
                from googleapiclient.discovery import build
                from googleapiclient.http import MediaFileUpload

                creds = None
                token_path = self.google_drive_token_path.get()
                credentials_path = self.google_drive_credentials_path.get()

                if os.path.exists(token_path):
                    creds = Credentials.from_authorized_user_file(token_path,
                                                                  ['https://www.googleapis.com/auth/drive.file'])

                if not creds or not creds.valid:
                    if creds and creds.expired and creds.refresh_token:
                        creds.refresh(Request())
                    else:
                        if not os.path.exists(credentials_path):
                            messagebox.showerror("Kļūda", f"Akreditācijas fails '{credentials_path}' nav atrasts.\n"
                                                          "Lūdzu, lejupielādējiet 'credentials.json' no Google Cloud Console.")
                            return
                        flow = InstalledAppFlow.from_client_secrets_file(
                            credentials_path, ['https://www.googleapis.com/auth/drive.file'])
                        creds = flow.run_local_server(port=0)
                    with open(token_path, 'w') as token:
                        token.write(creds.to_json())

                service = build('drive', 'v3', credentials=creds)

                # Pārbauda, vai mērķa mape eksistē, ja nē, izveido to
                target_folder_id = self.google_drive_folder_id.get()
                if not target_folder_id:
                    # Ja nav norādīts mapes ID, mēģina atrast vai izveidot saknes mapi
                    results = service.files().list(
                        q="name='OCR_Documents' and mimeType='application/vnd.google-apps.folder'",
                        fields="files(id, name)").execute()
                    items = results.get('files', [])
                    if not items:
                        file_metadata = {
                            'name': 'OCR_Documents',
                            'mimeType': 'application/vnd.google-apps.folder'
                        }
                        file = service.files().create(body=file_metadata, fields='id').execute()
                        target_folder_id = file.get('id')
                        self.google_drive_folder_id.set(target_folder_id)  # Saglabā jauno ID
                        self.save_app_settings()
                    else:
                        target_folder_id = items[0]['id']
                        self.google_drive_folder_id.set(target_folder_id)  # Saglabā atrasto ID
                        self.save_app_settings()

                # Izveido apakšmapi, ja remote_path ir norādīts (piem., dokumentu kategorija)
                if remote_path:
                    # Pārbauda, vai apakšmape jau eksistē
                    results = service.files().list(
                        q=f"'{target_folder_id}' in parents and name='{remote_path}' and mimeType='application/vnd.google-apps.folder'",
                        fields="files(id, name)").execute()
                    items = results.get('files', [])
                    if not items:
                        file_metadata = {
                            'name': remote_path,
                            'parents': [target_folder_id],
                            'mimeType': 'application/vnd.google-apps.folder'
                        }
                        file = service.files().create(body=file_metadata, fields='id').execute()
                        target_folder_id = file.get('id')  # Tagad mērķa ID ir apakšmapes ID
                    else:
                        target_folder_id = items[0]['id']

                file_metadata = {
                    'name': os.path.basename(local_filepath),
                    'parents': [target_folder_id]
                }
                media = MediaFileUpload(local_filepath, mimetype='application/pdf')  # Pieņemam, ka PDF
                file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                messagebox.showinfo("Augšupielāde",
                                    f"Fails '{os.path.basename(local_filepath)}' veiksmīgi augšupielādēts uz Google Drive (ID: {file.get('id')}).")

            else:
                messagebox.showwarning("Augšupielāde", "Nav izvēlēts derīgs attālinātās glabāšanas veids.")

        except Exception as e:
            messagebox.showerror("Augšupielādes kļūda", f"Neizdevās augšupielādēt failu: {e}")

    def update_auto_scan_status(self):
        """Atjaunina automātiskās skenēšanas statusa etiķeti."""
        if self.auto_scan_enabled.get():
            self.auto_scan_status_label.config(text=f"Statuss: Ieslēgts (Uzrauga: {self.scan_folder_path.get()})", bootstyle="success")
        else:
            self.auto_scan_status_label.config(text="Statuss: Izslēgts", bootstyle="info")

    def start_auto_scan(self):
        """Sāk failu sistēmas uzraudzību automātiskai skenēšanai."""
        scan_path = self.scan_folder_path.get()
        if not os.path.exists(scan_path):
            os.makedirs(scan_path, exist_ok=True)
            messagebox.showinfo("Mape izveidota", f"Izveidota skenēšanas mape: {scan_path}")

        if self.observer:
            self.observer.stop()
            self.observer.join()

        event_handler = ScanEventHandler(self)
        self.observer = Observer()
        self.observer.schedule(event_handler, scan_path, recursive=False) # Uzrauga tikai tiešos failus mapē
        self.observer.start()
        print(f"Automātiskā skenēšana sākta mapē: {scan_path}")
        self.update_auto_scan_status()

    def stop_auto_scan(self):
        """Aptur failu sistēmas uzraudzību."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            print("Automātiskā skenēšana apturēta.")
        self.update_auto_scan_status()

    def process_new_scanned_file(self, filepath):
        """Apstrādā jaunu skenētu failu (attēlu vai PDF)."""
        print(f"Jauns fails atrasts: {filepath}")
        if not os.path.exists(filepath):
            print(f"Fails {filepath} vairs neeksistē, ignorē.")
            return

        # Pagaida, kamēr fails ir pilnībā uzrakstīts (īpaši svarīgi lieliem failiem)
        size_before = -1
        for _ in range(10): # Mēģina 10 reizes ar 0.5s intervālu
            current_size = os.path.getsize(filepath)
            if current_size == size_before:
                break
            size_before = current_size
            time.sleep(0.5)
        else:
            print(f"Brīdinājums: Fails {filepath} varbūt nav pilnībā uzrakstīts.")

        # Pārbauda faila tipu
        file_extension = os.path.splitext(filepath)[1].lower()
        if file_extension in ['.pdf']:
            self.after(100, lambda: self._process_pdf_for_auto_scan(filepath))
        elif file_extension in ['.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp']:
            self.after(100, lambda: self._process_image_for_auto_scan(filepath))
        else:
            print(f"Neatbalstīts faila tips automātiskai apstrādei: {filepath}")
            self.after(100, lambda: messagebox.showwarning("Automātiskā skenēšana", f"Neatbalstīts faila tips: {os.path.basename(filepath)}"))
            self.after(0, self.refresh_scanned_docs_list)  # Atjaunina sarakstu pēc apstrādes


    def _process_image_for_auto_scan(self, filepath):
        """Ielādē un apstrādā attēlu automātiskai skenēšanai."""
        try:
            img = Image.open(filepath)
            self.clear_files() # Notīra iepriekšējos attēlus
            self.images.append({"filepath": filepath, "original_img": img.copy(), "processed_img": img.copy()})
            self.file_listbox.insert(tk.END, os.path.basename(filepath))
            self.file_listbox.select_set(0)
            self.on_file_select()
            self._camera_scan_in_progress = True # Izmanto to pašu karogu, lai automātiski saglabātu PDF
            self.start_processing()
        except Exception as e:
            messagebox.showerror("Automātiskā skenēšana", f"Neizdevās apstrādāt attēlu {os.path.basename(filepath)}: {e}")

    def _process_pdf_for_auto_scan(self, filepath):
        """Ielādē un apstrādā PDF automātiskai skenēšanai."""
        try:
            doc = PDFEditor.open(filepath)
            self.clear_files() # Notīra iepriekšējos attēlus
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(dpi=self.dpi_var.get()) # Izmanto iestatīto DPI
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                self.images.append({"filepath": filepath, "original_img": img.copy(), "processed_img": img.copy()})
                self.file_listbox.insert(tk.END, f"{os.path.basename(filepath)} (Lapa {page_num + 1})")
            doc.close()

            if self.images:
                self.file_listbox.select_set(0)
                self.on_file_select()
                self._camera_scan_in_progress = True # Izmanto to pašu karogu, lai automātiski saglabātu PDF
                self.start_processing()
            else:
                messagebox.showwarning("Automātiskā skenēšana", f"PDF dokuments {os.path.basename(filepath)} nesatur attēlus vai lapas.")
        except Exception as e:
            messagebox.showerror("Automātiskā skenēšana", f"Neizdevās apstrādāt PDF {os.path.basename(filepath)}: {e}")


    def on_closing(self):
        """Apstrādā loga aizvēršanas notikumu, saglabājot iestatījumus un arhīvu."""
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.save_app_settings()
        self.save_scan_settings()  # JAUNS: Saglabā skenēšanas iestatījumus
        self.stop_auto_scan() # Aptur watchdog observer
        self.save_pdf_archive()
        self.destroy()

    # --- JAUNAS FUNKCIJAS ---

    def _get_current_image(self):
        """Palīgfunkcija, lai iegūtu pašreizējo apstrādājamo attēlu."""
        if self.current_image_index == -1:
            messagebox.showwarning("Nav attēla", "Lūdzu, vispirms atlasiet attēlu.")
            return None
        return self.images[self.current_image_index]["processed_img"]

    def _update_current_image(self, new_img):
        """Palīgfunkcija, lai atjauninātu pašreizējo attēlu un priekšskatījumu."""
        if self.current_image_index != -1:
            self.images[self.current_image_index]["processed_img"] = new_img
            self.show_image_preview(new_img)

    def convert_to_grayscale(self):
        """Konvertē pašreizējo attēlu pelēktoņos."""
        img = self._get_current_image()
        if img:
            try:
                if img.mode != 'L':
                    img = img.convert('L')
                    self._update_current_image(img)
                    messagebox.showinfo("Konvertēšana", "Attēls konvertēts uz pelēktoņiem.")
                else:
                    messagebox.showinfo("Konvertēšana", "Attēls jau ir pelēktoņos.")
            except Exception as e:
                messagebox.showerror("Kļūda", f"Neizdevās konvertēt uz pelēktoņiem: {e}")

    def apply_thresholding(self):
        """Pielieto attēlam bināro sliekšņošanu."""
        img = self._get_current_image()
        if img:
            try:
                if img.mode != 'L':
                    img = img.convert('L')  # Sliekšņošanai nepieciešami pelēktoņi

                threshold_value = simpledialog.askinteger("Sliekšņošana", "Ievadiet sliekšņa vērtību (0-255):",
                                                          parent=self, minvalue=0, maxvalue=255, initialvalue=128)
                if threshold_value is not None:
                    img = img.point(lambda p: 255 if p > threshold_value else 0)
                    self._update_current_image(img)
                    messagebox.showinfo("Sliekšņošana", "Sliekšņošana veiksmīgi pielietota.")
            except Exception as e:
                messagebox.showerror("Kļūda", f"Neizdevās pielietot sliekšņošanu: {e}")

    def apply_gaussian_blur(self):
        """Pielieto Gausa izplūšanu attēlam."""
        img = self._get_current_image()
        if img:
            try:
                radius = simpledialog.askfloat("Gausa izplūšana", "Ievadiet izplūšanas rādiusu (piem., 2.0):",
                                               parent=self, minvalue=0.1, initialvalue=2.0)
                if radius is not None:
                    img = img.filter(ImageFilter.GaussianBlur(radius))
                    self._update_current_image(img)
                    messagebox.showinfo("Gausa izplūšana", "Gausa izplūšana veiksmīgi pielietota.")
            except Exception as e:
                messagebox.showerror("Kļūda", f"Neizdevās pielietot Gausa izplūšanu: {e}")

    def apply_median_filter(self):
        """Pielieto mediānas filtru trokšņu samazināšanai."""
        img = self._get_current_image()
        if img:
            try:
                size = simpledialog.askinteger("Mediānas filtrs", "Ievadiet filtra izmēru (nepāra skaitlis, piem., 3):",
                                               parent=self, minvalue=1, initialvalue=3)
                if size is not None and size % 2 == 1:
                    img = img.filter(ImageFilter.MedianFilter(size))
                    self._update_current_image(img)
                    messagebox.showinfo("Mediānas filtrs", "Mediānas filtrs veiksmīgi pielietots.")
                elif size is not None:
                    messagebox.showwarning("Mediānas filtrs", "Filtra izmēram jābūt nepāra skaitlim.")
            except Exception as e:
                messagebox.showerror("Kļūda", f"Neizdevās pielietot mediānas filtru: {e}")

    def sharpen_image(self):
        """Uzlabo attēla asumu."""
        img = self._get_current_image()
        if img:
            try:
                factor = simpledialog.askfloat("Asums", "Ievadiet asuma faktoru (1.0 - oriģināls, >1.0 - asāks):",
                                               parent=self, minvalue=0.1, initialvalue=1.5)
                if factor is not None:
                    enhancer = ImageEnhance.Sharpness(img)
                    img = enhancer.enhance(factor)
                    self._update_current_image(img)
                    messagebox.showinfo("Asums", "Attēla asums veiksmīgi uzlabots.")
            except Exception as e:
                messagebox.showerror("Kļūda", f"Neizdevās uzlabot asumu: {e}")

    def rotate_image_by_angle(self):
        """Pagriež attēlu par norādītu leņķi."""
        img = self._get_current_image()
        if img:
            try:
                angle = simpledialog.askfloat("Pagriezt attēlu", "Ievadiet pagriešanas leņķi (grādos):",
                                              parent=self, initialvalue=45.0)
                if angle is not None:
                    img = img.rotate(angle, expand=True, fillcolor=(255, 255, 255) if img.mode == 'RGB' else 255)
                    self._update_current_image(img)
                    messagebox.showinfo("Pagriešana", f"Attēls pagriezts par {angle}°.")
            except Exception as e:
                messagebox.showerror("Kļūda", f"Neizdevās pagriezt attēlu: {e}")

    def add_text_overlay(self):
        """Pievieno attēlam teksta pārklājumu."""
        img = self._get_current_image()
        if img:
            text = simpledialog.askstring("Teksta pārklājums", "Ievadiet tekstu:", parent=self)
            if text:
                try:
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')  # Nepieciešams caurspīdīgumam

                    draw = ImageDraw.Draw(img)
                    font_size = simpledialog.askinteger("Teksta pārklājums", "Ievadiet fonta izmēru:",
                                                        parent=self, minvalue=10, initialvalue=50)
                    if font_size is None: return

                    font_color = simpledialog.askstring("Teksta pārklājums",
                                                        "Ievadiet fonta krāsu (piem., 'red', '#FF0000'):",
                                                        parent=self, initialvalue="black")
                    if font_color is None: return

                    x_pos = simpledialog.askinteger("Teksta pārklājums", "Ievadiet X pozīciju:",
                                                    parent=self, initialvalue=50)
                    if x_pos is None: return

                    y_pos = simpledialog.askinteger("Teksta pārklājums", "Ievadiet Y pozīciju:",
                                                    parent=self, initialvalue=50)
                    if y_pos is None: return

                    try:
                        font = ImageFont.truetype("arial.ttf", font_size)
                    except IOError:
                        font = ImageFont.load_default()

                    draw.text((x_pos, y_pos), text, font=font, fill=font_color)
                    self._update_current_image(img)
                    messagebox.showinfo("Teksta pārklājums", "Teksts veiksmīgi pievienots.")
                except Exception as e:
                    messagebox.showerror("Kļūda", f"Neizdevās pievienot teksta pārklājumu: {e}")

    def draw_rectangle_on_image(self):
        """Zīmē taisnstūri uz attēla."""
        img = self._get_current_image()
        if img:
            try:
                x1 = simpledialog.askinteger("Zīmēt taisnstūri", "Ievadiet X1 koordinātu:", parent=self,
                                             initialvalue=50)
                y1 = simpledialog.askinteger("Zīmēt taisnstūri", "Ievadiet Y1 koordinātu:", parent=self,
                                             initialvalue=50)
                x2 = simpledialog.askinteger("Zīmēt taisnstūri", "Ievadiet X2 koordinātu:", parent=self,
                                             initialvalue=150)
                y2 = simpledialog.askinteger("Zīmēt taisnstūri", "Ievadiet Y2 koordinātu:", parent=self,
                                             initialvalue=150)
                if any(coord is None for coord in [x1, y1, x2, y2]): return

                color = simpledialog.askstring("Zīmēt taisnstūri", "Ievadiet krāsu (piem., 'red', '#FF0000'):",
                                               parent=self, initialvalue="red")
                if color is None: return

                width = simpledialog.askinteger("Zīmēt taisnstūri", "Ievadiet līnijas biezumu:",
                                                parent=self, minvalue=1, initialvalue=3)
                if width is None: return

                draw = ImageDraw.Draw(img)
                draw.rectangle([x1, y1, x2, y2], outline=color, width=width)
                self._update_current_image(img)
                messagebox.showinfo("Zīmēšana", "Taisnstūris veiksmīgi uzzīmēts.")
            except Exception as e:
                messagebox.showerror("Kļūda", f"Neizdevās uzzīmēt taisnstūri: {e}")

    def draw_circle_on_image(self):
        """Zīmē apli uz attēla."""
        img = self._get_current_image()
        if img:
            try:
                x = simpledialog.askinteger("Zīmēt apli", "Ievadiet centra X koordinātu:", parent=self,
                                            initialvalue=100)
                y = simpledialog.askinteger("Zīmēt apli", "Ievadiet centra Y koordinātu:", parent=self,
                                            initialvalue=100)
                radius = simpledialog.askinteger("Zīmēt apli", "Ievadiet rādiusu:", parent=self, minvalue=1,
                                                 initialvalue=50)
                if any(val is None for val in [x, y, radius]): return

                color = simpledialog.askstring("Zīmēt apli", "Ievadiet krāsu (piem., 'green', '#00FF00'):",
                                               parent=self, initialvalue="blue")
                if color is None: return

                width = simpledialog.askinteger("Zīmēt apli", "Ievadiet līnijas biezumu:",
                                                parent=self, minvalue=1, initialvalue=3)
                if width is None: return

                draw = ImageDraw.Draw(img)
                draw.ellipse([x - radius, y - radius, x + radius, y + radius], outline=color, width=width)
                self._update_current_image(img)
                messagebox.showinfo("Zīmēšana", "Aplis veiksmīgi uzzīmēts.")
            except Exception as e:
                messagebox.showerror("Kļūda", f"Neizdevās uzzīmēt apli: {e}")

    def extract_color_channels(self):
        """Izvelk atsevišķus krāsu kanālus (R, G, B) un parāda tos."""
        img = self._get_current_image()
        if img:
            try:
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                r, g, b = img.split()

                # Parāda katru kanālu atsevišķā logā
                for channel_img, channel_name in zip([r, g, b], ["Red", "Green", "Blue"]):
                    channel_window = Toplevel(self)
                    channel_window.title(f"Krāsu kanāls: {channel_name}")
                    channel_window.transient(self)
                    channel_window.grab_set()

                    canvas_channel = tk.Canvas(channel_window, bg="black")
                    canvas_channel.pack(fill="both", expand=True)

                    # Pielāgo attēlu kanvasa izmēram
                    channel_window.update_idletasks()
                    canvas_width = canvas_channel.winfo_width()
                    canvas_height = canvas_channel.winfo_height()

                    if canvas_width == 0 or canvas_height == 0:
                        canvas_width = 400
                        canvas_height = 300

                    display_channel_img = channel_img.resize(
                        (canvas_width, canvas_height), Image.LANCZOS)
                    photo_channel = ImageTk.PhotoImage(display_channel_img)
                    canvas_channel.create_image(0, 0, anchor="nw", image=photo_channel)
                    canvas_channel.image = photo_channel  # Saglabā atsauci

                messagebox.showinfo("Krāsu kanāli", "Krāsu kanāli veiksmīgi izvilkti un parādīti atsevišķos logos.")
            except Exception as e:
                messagebox.showerror("Kļūda", f"Neizdevās izvilkt krāsu kanālus: {e}")

    def merge_color_channels(self):
        """Apvieno krāsu kanālus (R, G, B) no atsevišķiem attēliem."""
        messagebox.showinfo("Apvienot krāsu kanālus",
                            "Lūdzu, atlasiet trīs pelēktoņu attēlus (sarkanajam, zaļajam un zilajam kanālam).")
        filepaths = filedialog.askopenfilenames(
            title="Izvēlieties 3 pelēktoņu attēlus (R, G, B)",
            filetypes=[("Attēlu faili", "*.png *.jpg *.jpeg *.tif *.tiff *.bmp"), ("Visi faili", "*.*")]
        )

        if len(filepaths) != 3:
            messagebox.showwarning("Kļūda", "Lūdzu, atlasiet tieši 3 attēlus (pa vienam katram kanālam).")
            return

        try:
            # Ielādē attēlus un pārliecinās, ka tie ir pelēktoņos
            r_img = Image.open(filepaths[0]).convert('L')
            g_img = Image.open(filepaths[1]).convert('L')
            b_img = Image.open(filepaths[2]).convert('L')

            # Pārliecinās, ka attēli ir vienāda izmēra
            if not (r_img.size == g_img.size == b_img.size):
                messagebox.showwarning("Kļūda", "Visiem kanālu attēliem jābūt vienāda izmēra.")
                return

            merged_img = Image.merge('RGB', (r_img, g_img, b_img))
            self._update_current_image(merged_img)
            messagebox.showinfo("Apvienošana", "Krāsu kanāli veiksmīgi apvienoti.")
        except Exception as e:
            messagebox.showerror("Kļūda", f"Neizdevās apvienot krāsu kanālus: {e}")

    def apply_sepia_filter(self):
        """Pielieto sēpijas filtru attēlam."""
        img = self._get_current_image()
        if img:
            try:
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                pixels = img.load()
                for y in range(img.size[1]):
                    for x in range(img.size[0]):
                        r, g, b = pixels[x, y]
                        tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                        tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                        tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                        pixels[x, y] = (min(255, tr), min(255, tg), min(255, tb))
                self._update_current_image(img)
                messagebox.showinfo("Sēpijas filtrs", "Sēpijas filtrs veiksmīgi pielietots.")
            except Exception as e:
                messagebox.showerror("Kļūda", f"Neizdevās pielietot sēpijas filtru: {e}")

    def apply_vignette_effect(self):
        """Pielieto vinjetes efektu attēlam."""
        img = self._get_current_image()
        if img:
            try:
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                width, height = img.size
                center_x, center_y = width // 2, height // 2
                max_dist = (center_x ** 2 + center_y ** 2) ** 0.5

                pixels = img.load()
                for y in range(height):
                    for x in range(width):
                        dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                        intensity = 1 - (dist / max_dist) * 0.7  # 0.7 ir vinjetes stiprums
                        r, g, b = pixels[x, y]
                        pixels[x, y] = (int(r * intensity), int(g * intensity), int(b * intensity))
                self._update_current_image(img)
                messagebox.showinfo("Vinjetes efekts", "Vinjetes efekts veiksmīgi pielietots.")
            except Exception as e:
                messagebox.showerror("Kļūda", f"Neizdevās pielietot vinjetes efektu: {e}")

    def pixelate_image(self):
        """Pikselizē attēlu."""
        img = self._get_current_image()
        if img:
            try:
                pixel_size = simpledialog.askinteger("Pikselizācija", "Ievadiet pikseļa bloka izmēru (piem., 10):",
                                                     parent=self, minvalue=1, initialvalue=10)
                if pixel_size is not None:
                    small_img = img.resize((img.width // pixel_size, img.height // pixel_size), Image.NEAREST)
                    pixelated_img = small_img.resize(img.size, Image.NEAREST)
                    self._update_current_image(pixelated_img)
                    messagebox.showinfo("Pikselizācija", "Attēls veiksmīgi pikselizēts.")
            except Exception as e:
                messagebox.showerror("Kļūda", f"Neizdevās pikselizēt attēlu: {e}")

    def detect_faces(self):
        """Noteikt sejas attēlā, izmantojot OpenCV."""
        if not OPENCV_AVAILABLE:
            messagebox.showwarning("Trūkst bibliotēkas", "Sejas noteikšanai nepieciešams 'opencv-python'.")
            return

        img = self._get_current_image()
        if img:
            try:
                # Pārvērš PIL attēlu uz OpenCV formātu
                img_cv = np.array(img.convert('RGB'))
                img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)
                gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

                # Ielādē sejas kaskādes klasifikatoru
                # Jums būs nepieciešams `haarcascade_frontalface_default.xml` fails.
                # To var atrast OpenCV repozitorijā:
                # https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
                # Ieteicams to novietot tajā pašā direktorijā, kur ir jūsu Python skripts,
                # vai norādīt pilnu ceļu uz failu.

                # Pārbauda, vai fails eksistē
                cascade_path = "haarcascade_frontalface_default.xml"
                if not os.path.exists(cascade_path):
                    messagebox.showerror("Kļūda", f"Haar kaskādes klasifikators '{cascade_path}' nav atrasts.\n"
                                                  "Lūdzu, lejupielādējiet to no OpenCV GitHub repozitorija un novietojiet blakus skriptam.")
                    return

                face_cascade = cv2.CascadeClassifier(cascade_path)

                if face_cascade.empty():
                    messagebox.showerror("Kļūda", f"Neizdevās ielādēt Haar kaskādes klasifikatoru no '{cascade_path}'.")
                    return

                faces = face_cascade.detectMultiScale(gray, 1.1, 4)

                if len(faces) == 0:
                    messagebox.showinfo("Sejas noteikšana", "Attēlā netika atrastas sejas.")
                    return

                # Zīmē taisnstūrus ap atrastajām sejām
                for (x, y, w, h) in faces:
                    cv2.rectangle(img_cv, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Zils taisnstūris

                # Pārvērš atpakaļ uz PIL attēlu un atjaunina
                result_img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
                self._update_current_image(result_img_pil)
                messagebox.showinfo("Sejas noteikšana", f"Attēlā atrastas {len(faces)} sejas.")

            except Exception as e:
                messagebox.showerror("Kļūda", f"Neizdevās veikt sejas noteikšanu: {e}")

    def scan_document_with_camera(self):
        """
        Automātiski skenē dokumentu, izmantojot kameru, un apstrādā to.
        Pirms kameras atvēršanas piedāvā izvēlēties kameru, ja pieejamas vairākas.
        Pievienota manuālās atlases iespēja.
        Uzlabota attēla apstrāde, lai labāk atpazītu dokumentus dažādos apgaismojuma apstākļos.
        """
        if not OPENCV_AVAILABLE:
            messagebox.showwarning("Trūkst bibliotēkas", "Kameras skenēšanai nepieciešams 'opencv-python'.")
            return

        # Pārbauda pieejamās kameras
        available_cameras = []
        for i in range(10):  # Pārbauda pirmās 10 kameras
            cap_test = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if cap_test.isOpened():
                available_cameras.append(i)
                cap_test.release()
            else:
                pass

        if not available_cameras:
            messagebox.showerror("Kļūda", "Netika atrasta neviena pieejama kamera.")
            return

        camera_index = self.scan_settings.get("scan_camera_index", DEFAULT_CAMERA_INDEX)

        if len(available_cameras) > 1:
            choice_dialog = Toplevel(self)
            choice_dialog.title("Izvēlēties kameru")
            choice_dialog.transient(self)
            choice_dialog.grab_set()

            ttk.Label(choice_dialog, text="Lūdzu, izvēlieties kameru:").pack(padx=10, pady=5)

            camera_options = [f"Kamera {idx}" for idx in available_cameras]
            selected_camera_var = tk.StringVar(
                value=f"Kamera {camera_index}" if camera_index in available_cameras else camera_options[0])
            camera_combo = ttk.Combobox(choice_dialog, textvariable=selected_camera_var, values=camera_options,
                                        state="readonly")
            camera_combo.pack(padx=10, pady=5)

            def confirm_camera_choice():
                nonlocal camera_index
                selected_text = selected_camera_var.get()
                camera_index = int(selected_text.split(" ")[1])
                choice_dialog.destroy()

            ttk.Button(choice_dialog, text="Apstiprināt", command=confirm_camera_choice, bootstyle=PRIMARY).pack(
                pady=10)
            self.wait_window(choice_dialog)

            if not choice_dialog.winfo_exists():
                if camera_index not in available_cameras:
                    camera_index = available_cameras[0]
            else:
                return

        cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        if not cap.isOpened():
            messagebox.showerror("Kļūda",
                                 f"Neizdevās atvērt kameru ar indeksu {camera_index}. Pārliecinieties, ka kamera ir pievienota un pieejama.")
            return

        # Ielādē skenēšanas iestatījumus
        camera_width = self.scan_settings.get("scan_camera_width", 1280)
        camera_height = self.scan_settings.get("scan_camera_height", 720)
        min_contour_area = self.scan_settings.get("scan_min_contour_area", 10000)
        stable_threshold = self.scan_settings.get("scan_stable_threshold", 1.5)
        stability_tolerance = self.scan_settings.get("scan_stability_tolerance", 0.02)
        aspect_ratio_min = self.scan_settings.get("scan_aspect_ratio_min", 0.5)
        aspect_ratio_max = self.scan_settings.get("scan_aspect_ratio_max", 2.0)
        gaussian_blur_kernel = self.scan_settings.get("scan_gaussian_blur_kernel", 5)
        adaptive_thresh_block_size = self.scan_settings.get("scan_adaptive_thresh_block_size", 11)
        adaptive_thresh_c = self.scan_settings.get("scan_adaptive_thresh_c", 2)
        canny_thresh1 = self.scan_settings.get("scan_canny_thresh1", 75)
        canny_thresh2 = self.scan_settings.get("scan_canny_thresh2", 200)

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)

        scan_window_name = "Dokumentu skenēšana (Nospiediet 'q', lai aizvērtu, 'm' - manuālai atlasei)"
        cv2.namedWindow(scan_window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(scan_window_name, 800, 600)

        document_found_time = None
        last_contour_area = 0
        self._camera_scan_in_progress = True

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    messagebox.showerror("Kļūda", "Neizdevās nolasīt kadru no kameras.")
                    break

                original_frame = frame.copy()

                # Uzlabota priekšapstrāde:
                # 1. Pārvērš uz HSV, lai labāk atdalītu krāsas un spilgtumu
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                # Izmantojam V (Value) kanālu, kas atspoguļo spilgtumu
                gray = hsv[:, :, 2]

                # 2. Pielieto Gausa izplūšanu, lai samazinātu troksni
                if gaussian_blur_kernel % 2 == 0:
                    gaussian_blur_kernel += 1  # Kernela izmēram jābūt nepāra
                blurred = cv2.GaussianBlur(gray, (gaussian_blur_kernel, gaussian_blur_kernel), 0)

                # 3. Pielieto adaptīvo sliekšņošanu, lai izceltu dokumentu neatkarīgi no fona
                # Šī metode ir robustāka pret apgaismojuma izmaiņām
                if adaptive_thresh_block_size % 2 == 0:
                    adaptive_thresh_block_size += 1  # Bloka izmēram jābūt nepāra
                if adaptive_thresh_block_size <= 1:
                    adaptive_thresh_block_size = 3  # Minimālais bloka izmērs

                # Izmantojam THRESH_BINARY_INV, lai dokuments būtu balts uz melna fona kontūru meklēšanai
                thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
                                               adaptive_thresh_block_size, adaptive_thresh_c)

                # 4. Morfoloģiskās operācijas, lai aizpildītu mazas atstarpes un savienotu kontūras
                kernel = np.ones((5, 5), np.uint8)  # Palielināts kernela izmērs
                morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel,
                                           iterations=3)  # Palielināts iterāciju skaits

                # 5. Canny malu noteikšana
                edged = cv2.Canny(morphed, canny_thresh1, canny_thresh2)

                contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                contours = sorted(contours, key=cv2.contourArea, reverse=True)

                document_contour = None
                status_text = "Meklē dokumentu..."

                for c in contours:
                    if cv2.contourArea(c) < min_contour_area:
                        continue

                    peri = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

                    # Pārbauda, vai kontūrai ir 4 stūri (dokuments)
                    if len(approx) == 4:
                        x, y, w, h = cv2.boundingRect(approx)
                        aspect_ratio = float(w) / h
                        # Pārbauda malu attiecību, lai filtrētu nedokumentu objektus
                        if aspect_ratio_min < aspect_ratio < aspect_ratio_max:
                            document_contour = approx
                            break

                display_frame = original_frame.copy()
                if document_contour is not None:
                    cv2.drawContours(display_frame, [document_contour], -1, (0, 255, 0), 2)  # Zaļa kontūra
                    current_contour_area = cv2.contourArea(document_contour)

                    if document_found_time is None:
                        document_found_time = time.time()
                        last_contour_area = current_contour_area
                        status_text = "Dokuments atrasts, gaida stabilitāti..."
                    else:
                        # Pārbauda kontūras stabilitāti
                        if abs(current_contour_area - last_contour_area) / last_contour_area < stability_tolerance:
                            if (time.time() - document_found_time) > stable_threshold:
                                status_text = "Dokuments stabils! Skenē..."
                                warped = self._four_point_transform(original_frame, document_contour.reshape(4, 2))

                                # Uzlabota pēcapstrāde skenētajam attēlam:
                                # Pārvērš uz pelēktoņiem
                                warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

                                # Pielieto adaptīvo sliekšņošanu ar lielāku bloka izmēru tīrākam rezultātam
                                # Šī ir galvenā apstrāde, lai iegūtu tīru, bināru attēlu
                                final_processed_img_cv = cv2.adaptiveThreshold(warped_gray, 255,
                                                                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                                               cv2.THRESH_BINARY, 21,
                                                                               # Lielāks bloka izmērs
                                                                               5)  # C vērtība

                                # Pārliecinās, ka fons ir balts un teksts melns (standarta OCR formāts)
                                # Pārbauda vidējo pikseļu vērtību. Ja tā ir zema, attēls ir tumšs (melns fons, balts teksts)
                                # un ir jāinvertē.
                                if np.mean(final_processed_img_cv) < 128:
                                    final_processed_img_cv = cv2.bitwise_not(final_processed_img_cv)

                                # Saglabā oriģinālo krāsu attēlu
                                original_scanned_pil_img = Image.fromarray(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))

                                # Apstrādā attēlu OCR vajadzībām (pelēktoņi, adaptīvā sliekšņošana)
                                warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
                                final_processed_img_cv = cv2.adaptiveThreshold(warped_gray, 255,
                                                                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                                               cv2.THRESH_BINARY, 21, 5)
                                if np.mean(final_processed_img_cv) < 128:
                                    final_processed_img_cv = cv2.bitwise_not(final_processed_img_cv)
                                ocr_processed_pil_img = Image.fromarray(final_processed_img_cv)

                                self.clear_files()
                                self.images.append(
                                    {"filepath": "camera_scan.png",
                                     "original_img": original_scanned_pil_img,
                                     # Šis ir krāsainais attēls PDF ģenerēšanai
                                     "processed_img": ocr_processed_pil_img})  # Šis ir apstrādātais attēls OCR veikšanai
                                self.file_listbox.insert(tk.END, "camera_scan.png")
                                self.file_listbox.select_set(0)
                                self.on_file_select()

                                self.start_processing()
                                break  # Iziet no kameras cilpas pēc veiksmīgas skenēšanas
                            else:
                                status_text = f"Dokuments stabils ({int(stable_threshold - (time.time() - document_found_time) + 1)}s)..."
                        else:
                            document_found_time = time.time()  # Atjauno laiku, ja dokuments kustas
                            last_contour_area = current_contour_area
                            status_text = "Dokuments kustas, gaida stabilitāti..."
                else:
                    document_found_time = None
                    status_text = "Meklē dokumentu..."

                cv2.putText(display_frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                cv2.putText(display_frame, "Nospiediet 'm' manuālai atlasei", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0, 255, 255), 2)

                cv2.imshow(scan_window_name, display_frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('m'):  # Manuālās atlases režīms
                    cv2.destroyWindow(scan_window_name)  # Aizver automātiskās skenēšanas logu
                    # Uztver abas atgrieztās vērtības
                    result_tuple = self._manual_document_selection(original_frame)
                    if result_tuple:  # Pārbauda, vai atlase netika atcelta
                        original_scanned_pil_img, ocr_processed_pil_img = result_tuple
                        self.clear_files()
                        self.images.append(
                            {"filepath": "manual_scan.png",
                             "original_img": original_scanned_pil_img,
                             "processed_img": ocr_processed_pil_img})
                        self.file_listbox.insert(tk.END, "manual_scan.png")
                        self.file_listbox.select_set(0)
                        self.on_file_select()
                        self.start_processing()
                    break  # Iziet no kameras cilpas pēc manuālās atlases

        except Exception as e:
            messagebox.showerror("Kļūda kameras skenēšanā", f"Radās kļūda: {e}")
        finally:
            cap.release()
            cv2.destroyAllWindows()  # Nodrošina visu OpenCV logu aizvēršanu
            self._camera_scan_in_progress = False

    def _manual_document_selection(self, frame):
        """
        Ļauj lietotājam manuāli atlasīt dokumenta stūrus.
        Atgriež apstrādātu PIL attēlu vai None, ja atlase atcelta.
        Uzlabota pēcapstrāde manuāli atlasītajam apgabalam.
        """
        points = []
        clone = frame.copy()
        window_name = "Manuāla atlase: Noklikšķiniet uz 4 stūriem (Esc, lai atceltu, Enter, lai apstiprinātu)"

        def mouse_callback(event, x, y, flags, param):
            nonlocal points, clone

            if event == cv2.EVENT_LBUTTONDOWN:
                if len(points) < 4:
                    points.append((x, y))
                    cv2.circle(clone, (x, y), 5, (0, 255, 0), -1)
                    cv2.imshow(window_name, clone)
                else:
                    messagebox.showwarning("Atlase",
                                           "Jau ir atlasīti 4 punkti. Nospiediet Enter, lai apstiprinātu, vai Esc, lai atceltu.")

        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 800, 600)
        cv2.setMouseCallback(window_name, mouse_callback)

        while True:
            cv2.imshow(window_name, clone)
            key = cv2.waitKey(1) & 0xFF

            if key == 27:  # Esc taustiņš
                messagebox.showinfo("Atlase atcelta", "Manuālā atlase atcelta.")
                cv2.destroyWindow(window_name)
                return None
            elif key == 13:  # Enter taustiņš
                if len(points) == 4:
                    break
                else:
                    messagebox.showwarning("Nepietiekami punkti", "Lūdzu, atlasiet visus 4 dokumenta stūrus.")

        cv2.destroyWindow(window_name)

        if len(points) == 4:
            try:
                # Veic perspektīvas transformāciju ar manuāli atlasītajiem punktiem
                warped = self._four_point_transform(frame, np.array(points, dtype="float32"))

                # Uzlabota pēcapstrāde skenētajam attēlam:
                # Pārvērš uz pelēktoņiem
                warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

                # Pielieto adaptīvo sliekšņošanu ar lielāku bloka izmēru tīrākam rezultātam
                final_processed_img_cv = cv2.adaptiveThreshold(warped_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                               cv2.THRESH_BINARY, 21, 5)

                # Pārliecinās, ka fons ir balts un teksts melns (standarta OCR formāts)
                if np.mean(final_processed_img_cv) < 128:
                    final_processed_img_cv = cv2.bitwise_not(final_processed_img_cv)

                # Saglabā oriģinālo krāsu attēlu
                original_scanned_pil_img = Image.fromarray(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))

                # Apstrādā attēlu OCR vajadzībām (pelēktoņi, adaptīvā sliekšņošana)
                warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
                final_processed_img_cv = cv2.adaptiveThreshold(warped_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                               cv2.THRESH_BINARY, 21, 5)
                if np.mean(final_processed_img_cv) < 128:
                    final_processed_img_cv = cv2.bitwise_not(final_processed_img_cv)
                ocr_processed_pil_img = Image.fromarray(final_processed_img_cv)

                messagebox.showinfo("Atlase veiksmīga", "Dokuments veiksmīgi skenēts ar manuālo atlasi.")
                # Atgriežam apstrādāto attēlu, kas tiks izmantots kā "processed_img"
                # "original_img" tiks iestatīts no `original_scanned_pil_img`
                return original_scanned_pil_img, ocr_processed_pil_img

            except Exception as e:
                messagebox.showerror("Kļūda", f"Neizdevās apstrādāt manuāli atlasīto apgabalu: {e}")
                return None
        return None

    def _order_points(self, pts):
        """Sakārto punktus: augšējais kreisais, augšējais labais, apakšējais labais, apakšējais kreisais."""
        rect = np.zeros((4, 2), dtype="float32")

        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]  # Augšējais kreisais (mazākā summa)
        rect[2] = pts[np.argmax(s)]  # Apakšējais labais (lielākā summa)

        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]  # Augšējais labais (mazākā starpība)
        rect[3] = pts[np.argmax(diff)]  # Apakšējais kreisais (lielākā starpība)

        return rect

    def _four_point_transform(self, image, pts):
        """Veic četru punktu perspektīvas transformāciju."""
        rect = self._order_points(pts)
        (tl, tr, br, bl) = rect

        # Aprēķina jaunā attēla platumu
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        # Aprēķina jaunā attēla augstumu
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        # Galamērķa punkti
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        # Aprēķina perspektīvas transformācijas matricu un pielieto to
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

        return warped

class ScanEventHandler(FileSystemEventHandler):
    """
    Apstrādā failu sistēmas notikumus, lai automātiski apstrādātu jaunus failus.
    """
    def __init__(self, app_instance):
        super().__init__()
        self.app = app_instance
        self.processed_files = set() # Lai izvairītos no dubultas apstrādes

    def on_created(self, event):
        """Apstrādā faila izveides notikumu."""
        if not event.is_directory:
            filepath = event.src_path
            # Pārbauda, vai fails ir attēls vai PDF un nav jau apstrādāts
            if filepath.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp', '.pdf')) and filepath not in self.processed_files:
                self.processed_files.add(filepath)
                # Izsauc galvenās lietotnes metodi, lai apstrādātu failu
                self.app.after(100, lambda: self.app.process_new_scanned_file(filepath))
                # Pēc apstrādes noņem failu no saraksta, lai to varētu apstrādāt vēlreiz, ja tas tiek modificēts/pārsūtīts
                # Pagaida ilgāku laiku, lai nodrošinātu, ka fails ir pilnībā apstrādāts un augšupielādēts
                self.app.after(10000, lambda: self.processed_files.discard(filepath))


if __name__ == "__main__":
    # Pārbauda, vai ir instalēti nepieciešamie moduļi
    try:
        from PIL import ImageFilter, ImageChops  # ImageChops priekš attēlu salīdzināšanas
        import urllib.parse  # Nepieciešams e-pasta pielikumiem
        from docx import Document  # Priekš Word dokumentiem
    except ImportError as e:
        messagebox.showwarning("Trūkst bibliotēku", f"Dažas nepieciešamās bibliotēkas nav instalētas: {str(e)}\n"
                                  "Lūdzu, instalējiet trūkstošās bibliotēkas (pip install pillow python-docx).")
    # Palaiž galveno lietotni
    app = OCRPDFApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()