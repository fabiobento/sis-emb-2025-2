from flask import Flask, Response, render_template_string, request, redirect, url_for
from picamera2 import Picamera2
import io
import threading
import time
import os
import signal

app = Flask(__name__)

# Global variables
base_dir = "dataset"
picam2 = None
frame = None
frame_lock = threading.Lock()
capture_counts = {}
current_label = None
shutdown_event = threading.Event()

def initialize_camera():
    global picam2
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"size": (320, 240)})
    picam2.configure(config)
    picam2.start()
    time.sleep(2)  # Espere a câmera estabilizar

def get_frame():
    global frame
    while not shutdown_event.is_set():
        stream = io.BytesIO()
        picam2.capture_file(stream, format='jpeg')
        with frame_lock:
            frame = stream.getvalue()
        time.sleep(0.1)  # 

def generate_frames():
    while not shutdown_event.is_set():
        with frame_lock:
            if frame is not None:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.1)  # Ajuste conforme necessário para uma visualização suave

def shutdown_server():
    shutdown_event.set()
    if picam2:
        picam2.stop()
    # Dar algum tempo para que outros threads sejam concluídos.
    time.sleep(2)
    # Enviar SIGINT para o processo principal para encerrar o Flask
    os.kill(os.getpid(), signal.SIGINT)

@app.route('/', methods=['GET', 'POST'])
def index():
    global current_label
    if request.method == 'POST':
        current_label = request.form['label']
        if current_label not in capture_counts:
            capture_counts[current_label] = 0
        os.makedirs(os.path.join(base_dir, current_label), exist_ok=True)
        return redirect(url_for('capture_page'))
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Captura de conjunto de dados - Entrada de rótulo</title>
        </head>
        <body>
            <h1>Entre o rótulo para o conjunto de dados</h1>
            <form method="post">
                <input type="text" name="label" required>
                <input type="submit" value="Iniciar a captura">
            </form>
        </body>
        </html>
    ''')

@app.route('/capture')
def capture_page():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Captura de conjunto de dados - </title>
            <script>
                var shutdownInitiated = false;
                function checkShutdown() {
                    if (!shutdownInitiated) {
                        fetch('/check_shutdown')
                            .then(response => response.json())
                            .then(data => {
                                if (data.shutdown) {
                                    shutdownInitiated = true;
                                    document.getElementById('video-feed').src = '';
                                    document.getElementById('shutdown-message').style.display = 'block';
                                }
                            });
                    }
                }
                setInterval(checkShutdown, 1000);  // Check every second
            </script>
        </head>
        <body>
            <h1>Captura do Conjunto de Dados</h1>
            <p>Rótulo Atual: {{ label }}</p>
            <p>Imagens capturadas para esse rótulo: {{ capture_count }}</p>
            <img id="video-feed" src="{{ url_for('video_feed') }}" width="640" height="480" />
            <div id="shutdown-message" style="display: none; color: red;">
                Capture process has been stopped. You can close this window.
            </div>
            <form action="/capture_image" method="post">
                <input type="submit" value="Capturar Imagem">
            </form>
            <form action="/stop" method="post">
                <input type="submit" value="Parar a Captura" style="background-color: #ff6666;">
            </form>
            <form action="/" method="get">
                <input type="submit" value="Mudar o Rótulo" style="background-color: #ffff66;">
            </form>
        </body>
        </html>
    ''', label=current_label, capture_count=capture_counts.get(current_label, 0))

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture_image', methods=['POST'])
def capture_image():
    global capture_counts
    if current_label and not shutdown_event.is_set():
        capture_counts[current_label] += 1
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"image_{timestamp}.jpg"
        full_path = os.path.join(base_dir, current_label, filename)
        
        picam2.capture_file(full_path)
    
    return redirect(url_for('capture_page'))

@app.route('/stop', methods=['POST'])
def stop():
    summary = render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Captura de conjunto de dados - Parado</title>
        </head>
        <body>
            <h1>Captura de conjunto de dados interrompida</h1>
            <p>O processo de captura foi interrompido. Você pode fechar essa janela.</p>
            <p>Resumo de capturas:</p>
            <ul>
            {% for label, count in capture_counts.items() %}
                <li>{{ label }}: {{ count }} images</li>
            {% endfor %}
            </ul>
        </body>
        </html>
    ''', capture_counts=capture_counts)
    
    # Start a new thread to shutdown the server
    threading.Thread(target=shutdown_server).start()
    
    return summary

@app.route('/check_shutdown')
def check_shutdown():
    return {'shutdown': shutdown_event.is_set()}

if __name__ == '__main__':
    initialize_camera()
    threading.Thread(target=get_frame, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, threaded=True)
