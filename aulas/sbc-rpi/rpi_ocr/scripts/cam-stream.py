import cv2
from picamera2 import Picamera2
from flask import Flask, Response
import time

# --- Configuração do Servidor Flask ---
app = Flask(__name__)

# --- Configuração da Câmera ---
camera = Picamera2()
config = camera.create_video_configuration(main={"size": (640, 480), "format": "RGB888"})
camera.configure(config)
camera.start()
time.sleep(1.0)  # Tempo para a câmera inicializar

def generate_frames():
    """Gera frames de vídeo para o stream MJPEG."""
    print("Iniciando geração de frames...")
    while True:
        try:
            # 1. Captura o frame (formato RGB)
            img_rgb = camera.capture_array()
            
            # 2. Converte de RGB (Picamera2) para BGR (OpenCV)
            img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
            
            # 3. Codifica o frame BGR para o formato JPEG
            ret, buffer = cv2.imencode('.jpg', img_bgr)
            
            if not ret:
                print("Erro ao codificar frame")
                continue
            
            # 4. Converte o buffer para bytes
            frame_bytes = buffer.tobytes()
            
            # 5. "Entrega" (yield) o frame no formato MJPEG
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                   
        except Exception as e:
            # Se o cliente desconectar (ex: fechar o navegador), 
            # uma exceção pode ocorrer aqui. O break garante que o loop pare.
            # print(f"Erro no loop de geração de frames: {e}") 
            break
    print("Geração de frames parada.")

# --- Rotas do Servidor Web ---

@app.route('/')
def index():
    """Página principal que exibe o stream de vídeo."""
    return """
    <html>
    <head>
        <title>RPi - Video Stream</title>
        <style>
            body { font-family: sans-serif; text-align: center; padding-top: 20px; }
            img { border: 2px solid #333; }
        </style>
    </head>
    <body>
        <h1>Streaming de Vídeo(RPi)</h1>
        <img src="/video_feed" width="640" height="480">
    </body>
    </html>
    """

@app.route('/video_feed')
def video_feed():
    """A rota que fornece o stream de vídeo MJPEG."""
    return Response(generate_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# --- Ponto de Entrada Principal (MODIFICADO) ---
if __name__ == "__main__":
    print("Iniciando servidor web...")
    print("Pressione Ctrl+C para sair.")
    
    try:
        # Inicia o servidor Flask
        app.run(host='0.0.0.0', port=5000, threaded=True)
        
    except KeyboardInterrupt:
        # Captura o Ctrl+C para uma saída limpa
        print("\nServidor interrompido pelo usuário.")
        
    finally:
        # Este bloco é EXECUTADO SEMPRE, garantindo que a câmera seja liberada
        print("Limpando recursos... Parando a câmera.")
        camera.stop()
        camera.close()
        print("Recursos liberados. Saindo.")
