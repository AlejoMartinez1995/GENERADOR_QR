'''Un generador de códigos QR en Python.'''

import qrcode
try:
    from PIL import Image
except ImportError:
    print("Error: PIL/Pillow no está instalado. Instálalo con: pip install Pillow")
import tkinter as tk
from tkinter import filedialog, messagebox

class QRCodeGenerator:
 
    def __init__(self, master):
        self.master = master
        self.master.title("Generador de Códigos QR")
        self.master.geometry("600x400")

        # Etiqueta y entrada para el texto del código QR
        self.label = tk.Label(master, text="Texto para el código QR:")
        self.label.pack(pady=10)

        self.text_entry = tk.Entry(master, width=50)
        self.text_entry.pack(pady=5)

        # Botón para generar el código QR
        self.generate_button = tk.Button(master, text="Generar Código QR", command=self.generate_qr)
        self.generate_button.pack(pady=20)

    def generate_qr(self):
        text = self.text_entry.get()
        if not text:
            messagebox.showerror("Error", "Por favor, ingresa un texto para generar el código QR.")
            return

        # Generar el código QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Guardar la imagen del código QR
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            img.save(file_path)
            messagebox.showinfo("Éxito", f"Código QR guardado en: {file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()
