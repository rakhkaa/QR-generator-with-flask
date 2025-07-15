from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    text = request.form.get('text', '')
    
    if not text:
        return render_template('index.html', error="Mohon masukkan text untuk di-generate!")
    
    # Membuat QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    
    # Membuat image QR code
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert ke base64 untuk ditampilkan di HTML
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    
    return render_template('index.html', 
                         qr_code=img_base64, 
                         text=text,
                         success=True)

@app.route('/download/<text>')
def download_qr(text):
    # Membuat QR code untuk download
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save ke BytesIO untuk download
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    return send_file(img_buffer, 
                     mimetype='image/png',
                     as_attachment=True,
                     download_name=f'qr_code_{text[:20]}.png')

if __name__ == '__main__':
    app.run(debug=True)
