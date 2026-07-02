'''Un generador de códigos QR en Python adaptado para entorno Web (Render).'''

from flask import Flask, request, send_file, render_template_string
import qrcode
import io

app = Flask(__name__)

# Interfaz Web que reemplaza las ventanas de Tkinter
INTERFAZ_HTML = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generador de Códigos QR</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            text-align: center; 
            margin-top: 60px; 
            background-color: #f4f7f6; 
            color: #333;
        }
        .contenedor {
            background: white; 
            padding: 30px; 
            display: inline-block; 
            border-radius: 8px; 
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
            max-width: 500px;
            width: 90%;
        }
        h2 { margin-bottom: 20px; color: #028090; }
        label { display: block; margin-bottom: 8px; font-weight: bold; }
        input[type="text"] { 
            width: 100%; 
            padding: 12px; 
            margin-bottom: 20px; 
            border: 1px solid #ccc; 
            border-radius: 4px;
            box-sizing: border-box;
        }
        button { 
            width: 100%;
            padding: 12px; 
            background-color: #00a896; 
            color: white; 
            border: none; 
            border-radius: 4px; 
            font-size: 16px;
            cursor: pointer; 
            font-weight: bold;
        }
        button:hover { background-color: #028090; }
    </style>
</head>
<body>
    <div class="contenedor">
        <h2>Generador de Códigos QR</h2>
        <form action="/generar" method="POST">
            <label for="texto">Texto para el código QR:</label>
            <input type="text" id="texto" name="texto" placeholder="Ingresá el texto o enlace aquí..." required>
            <button type="submit">Generar Código QR</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    # Devuelve la interfaz de entrada
    return render_template_string(INTERFAZ_HTML)

@app.route('/generar', methods=['POST'])
def generate_qr():
    # Reemplaza a self.text_entry.get()
    text = request.form.get('texto')
    
    if not text:
        return "Por favor, ingresa un texto válido.", 400

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Guardar en memoria (BytesIO) en lugar de pedir una ruta física con filedialog
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    # Envía el archivo para que el navegador lo descargue automáticamente como 'codigo_qr.png'
    return send_file(
        img_buffer, 
        mimetype='image/png', 
        as_attachment=True, 
        download_name='codigo_qr.png'
    )

if __name__ == '__main__':
    # Para pruebas locales en tu PC
    app.run(debug=True)
