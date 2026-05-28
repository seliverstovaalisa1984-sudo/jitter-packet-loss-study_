import socket
import cv2
import numpy as np
import struct
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Использование: python receiver_final.py <output.mp4>")
        sys.exit(1)

    output_path = sys.argv[1]
    ip = "127.0.0.1"
    port = 5005

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen(1)
    print(f"Ожидание подключения на {ip}:{port}...")
    conn, _ = sock.accept()
    print("Подключение установлено")

    writer = None
    frames = 0

    while True:
        try:
            size_data = conn.recv(4)
            if not size_data:
                break
            size = struct.unpack('>I', size_data)[0]
            seq_data = conn.recv(4)
            seq = struct.unpack('>I', seq_data)[0]
            data = b''
            while len(data) < size:
                chunk = conn.recv(size - len(data))
                if not chunk:
                    break
                data += chunk
            frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
            if frame is not None:
                if writer is None:
                    h, w = frame.shape[:2]
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    writer = cv2.VideoWriter(output_path, fourcc, 30.0, (w, h))
                    print(f"Запись видео: {w}x{h}")
                writer.write(frame)
                frames += 1
        except:
            break

    conn.close()
    sock.close()
    if writer:
        writer.release()
    print(f"Сохранено кадров: {frames}")

if __name__ == "__main__":
    main()