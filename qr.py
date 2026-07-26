'''Un generador de códigos QR en Python adaptado para entorno Web Premium (Render).'''

from flask import Flask, request, jsonify, render_template_string
import qrcode
import io
import base64

app = Flask(__name__)

# Interfaz Web Premium (Tema Oscuro con Glassmorphism)
INTERFAZ_HTML = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generador de Códigos QR Premium</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #030712;
            --card-bg: rgba(17, 25, 40, 0.7);
            --border-color: rgba(255, 255, 255, 0.08);
            --primary-color: #00f2fe;
            --primary-hover: #4facfe;
            --text-color: #f3f4f6;
            --text-muted: #9ca3af;
        }

        body { 
            font-family: 'Outfit', sans-serif; 
            background: radial-gradient(circle at 50% 50%, #064e3b 0%, #022c22 100%);
            color: var(--text-color);
            margin: 0;
            padding: 40px 20px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            box-sizing: border-box;
        }

        .contenedor {
            background: var(--card-bg);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border: 1px solid var(--border-color);
            padding: 40px; 
            border-radius: 20px; 
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
            max-width: 800px;
            width: 100%;
            display: flex;
            gap: 30px;
            flex-direction: row;
        }

        @media (max-width: 768px) {
            .contenedor {
                flex-direction: column;
                padding: 30px 20px;
            }
        }

        .panel-form {
            flex: 1.2;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .panel-preview {
            flex: 0.8;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-left: 1px solid var(--border-color);
            padding-left: 30px;
        }

        @media (max-width: 768px) {
            .panel-preview {
                border-left: none;
                border-top: 1px solid var(--border-color);
                padding-left: 0;
                padding-top: 30px;
            }
        }

        h2 { 
            font-size: 2rem;
            font-weight: 700;
            margin-top: 0;
            margin-bottom: 8px;
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-hover) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .sub {
            color: var(--text-muted);
            margin-bottom: 25px;
            font-size: 0.95rem;
        }

        .control-group {
            margin-bottom: 20px;
            text-align: left;
        }

        label { 
            display: block; 
            margin-bottom: 8px; 
            font-weight: 600; 
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
        }

        input[type="text"] { 
            width: 100%; 
            padding: 14px; 
            background: rgba(10, 15, 26, 0.6);
            color: var(--text-color);
            border: 1px solid var(--border-color); 
            border-radius: 8px;
            box-sizing: border-box;
            font-size: 1rem;
            outline: none;
            transition: all 0.3s;
        }
        
        input[type="text"]:focus { 
            border-color: var(--primary-color); 
            box-shadow: 0 0 10px rgba(0, 242, 254, 0.2);
        }

        .color-row {
            display: flex;
            gap: 15px;
        }

        .color-field {
            flex: 1;
        }

        .color-picker-wrapper {
            display: flex;
            align-items: center;
            background: rgba(10, 15, 26, 0.6);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 8px 12px;
            box-sizing: border-box;
        }

        input[type="color"] {
            border: none;
            background: none;
            width: 32px;
            height: 32px;
            cursor: pointer;
            padding: 0;
            margin-right: 10px;
        }

        .color-val-text {
            font-family: monospace;
            font-size: 0.95rem;
            text-transform: uppercase;
            color: var(--text-color);
        }

        select {
            width: 100%;
            padding: 14px;
            background: rgba(10, 15, 26, 0.6);
            color: var(--text-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            font-size: 1rem;
            outline: none;
            cursor: pointer;
            appearance: none;
            background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
            background-repeat: no-repeat;
            background-position: right 14px center;
            background-size: 16px;
        }

        button { 
            width: 100%;
            padding: 14px; 
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-hover) 100%); 
            color: #022c22; 
            border: none; 
            border-radius: 8px; 
            font-size: 16px;
            cursor: pointer; 
            font-weight: 700;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(0, 242, 254, 0.25);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        button:hover { 
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 242, 254, 0.4);
            filter: brightness(1.1);
        }

        /* Preview box stylings */
        .preview-box {
            width: 250px;
            height: 250px;
            border: 2px dashed rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            display: flex;
            justify-content: center;
            align-items: center;
            background: rgba(0, 0, 0, 0.2);
            position: relative;
            overflow: hidden;
            transition: all 0.3s;
        }

        .preview-box img {
            max-width: 100%;
            max-height: 100%;
            display: none;
            animation: fadeIn 0.5s ease-out forwards;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }

        .placeholder-text {
            color: var(--text-muted);
            font-size: 0.9rem;
            text-align: center;
            padding: 20px;
        }

        .btn-descargar {
            margin-top: 20px;
            display: none;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.25);
        }

        .btn-descargar:hover {
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
            background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
        }

        .status {
            margin-top: 15px;
            font-weight: 600;
            font-size: 0.9rem;
            min-height: 20px;
            color: #10b981;
        }

        .status.error {
            color: #ef4444;
        }
    </style>
</head>
<body>
    <div class="contenedor">
        <div class="panel-form">
            <h2>Generador de QR</h2>
            <div class="sub">Personalizá y creá tu código QR al instante.</div>

            <div class="control-group">
                <label for="texto">Contenido del QR</label>
                <input type="text" id="texto" placeholder="Ingresá texto o un enlace (URL)..." required>
            </div>

            <div class="color-row">
                <div class="control-group color-field">
                    <label for="color_fg">Color QR</label>
                    <div class="color-picker-wrapper">
                        <input type="color" id="color_fg" value="#000000" onchange="updateColorText('color_fg', 'fg_text')">
                        <span id="fg_text" class="color-val-text">#000000</span>
                    </div>
                </div>
                <div class="control-group color-field">
                    <label for="color_bg">Color Fondo</label>
                    <div class="color-picker-wrapper">
                        <input type="color" id="color_bg" value="#FFFFFF" onchange="updateColorText('color_bg', 'bg_text')">
                        <span id="bg_text" class="color-val-text">#FFFFFF</span>
                    </div>
                </div>
            </div>

            <div class="control-group">
                <label for="error_correction">Corrección de Errores</label>
                <select id="error_correction">
                    <option value="L">Bajo (L - 7%)</option>
                    <option value="M">Medio (M - 15%)</option>
                    <option value="Q">Alto (Q - 25%)</option>
                    <option value="H">Máximo (H - 30%)</option>
                </select>
            </div>

            <button onclick="generarQR()">Generar QR</button>
            <div id="status" class="status"></div>
        </div>

        <div class="panel-preview">
            <div class="preview-box" id="preview-box">
                <div class="placeholder-text" id="placeholder-text">Ingresá los datos y generá el código para previsualizarlo acá.</div>
                <img id="qr-img" src="" alt="Código QR Generado">
            </div>
            <button class="btn-descargar" id="btn-descargar" onclick="descargarQR()">Descargar Imagen</button>
        </div>
    </div>

    <script>
        let qrBase64 = "";

        function updateColorText(pickerId, spanId) {
            const picker = document.getElementById(pickerId);
            const textSpan = document.getElementById(spanId);
            textSpan.innerText = picker.value.toUpperCase();
        }

        function generarQR() {
            const texto = document.getElementById('texto').value.trim();
            const colorFg = document.getElementById('color_fg').value;
            const colorBg = document.getElementById('color_bg').value;
            const ec = document.getElementById('error_correction').value;
            const statusDiv = document.getElementById('status');

            if (!texto) {
                statusDiv.className = "status error";
                statusDiv.innerText = "Por favor, ingresá un contenido válido.";
                return;
            }

            statusDiv.className = "status";
            statusDiv.innerText = "Generando código QR...";

            fetch('/generar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    texto: texto,
                    color_fg: colorFg,
                    color_bg: colorBg,
                    error_correction: ec
                })
            })
            .then(res => {
                if (!res.ok) throw new Error("Error al generar el QR.");
                return res.json();
            })
            .then(data => {
                if (data.exito) {
                    qrBase64 = data.qr_base64;
                    const img = document.getElementById('qr-img');
                    img.src = "data:image/png;base64," + qrBase64;
                    img.style.display = "block";
                    
                    document.getElementById('placeholder-text').style.display = "none";
                    document.getElementById('preview-box').style.border = "1px solid var(--border-color)";
                    document.getElementById('btn-descargar').style.display = "block";
                    
                    statusDiv.innerText = "¡QR generado con éxito!";
                    setTimeout(() => { statusDiv.innerText = ""; }, 3000);
                } else {
                    throw new Error("No se pudo completar la generación.");
                }
            })
            .catch(err => {
                statusDiv.className = "status error";
                statusDiv.innerText = err.message;
            });
        }

        function descargarQR() {
            if (!qrBase64) return;
            const link = document.createElement('a');
            link.href = 'data:image/png;base64,' + qrBase64;
            link.download = 'codigo_qr.png';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(INTERFAZ_HTML)

@app.route('/generar', methods=['POST'])
def generate_qr():
    # Permitir lectura tanto de JSON (asíncrono) como de Form tradicional (retrocompatibilidad)
    if request.is_json:
        data = request.get_json()
        text = data.get('texto')
        color_fg = data.get('color_fg', '#000000')
        color_bg = data.get('color_bg', '#FFFFFF')
        ec = data.get('error_correction', 'L')
    else:
        text = request.form.get('texto')
        color_fg = '#000000'
        color_bg = '#FFFFFF'
        ec = 'L'
    
    if not text:
        return jsonify({"exito": False, "error": "Por favor, ingresa un texto válido."}), 400

    # Configuración de nivel de corrección de errores
    err_level = qrcode.constants.ERROR_CORRECT_L
    if ec == 'M':
        err_level = qrcode.constants.ERROR_CORRECT_M
    elif ec == 'Q':
        err_level = qrcode.constants.ERROR_CORRECT_Q
    elif ec == 'H':
        err_level = qrcode.constants.ERROR_CORRECT_H

    qr = qrcode.QRCode(
        version=1,
        error_correction=err_level,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color=color_fg, back_color=color_bg)

    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    if request.is_json:
        # Devuelve en formato JSON Base64 para mostrarlo directamente
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        return jsonify({"exito": True, "qr_base64": img_base64})
    else:
        # Devuelve descarga tradicional si se envía por formulario plano
        return send_file(
            img_buffer, 
            mimetype='image/png', 
            as_attachment=True, 
            download_name='codigo_qr.png'
        )

if __name__ == '__main__':
    app.run(debug=True)
