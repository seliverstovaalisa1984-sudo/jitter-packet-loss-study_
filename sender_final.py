import socket
import cv2
import time
import random
import struct
import sys
import numpy as np

def add_artifacts(frame, loss_prob):
    """Добавляет артефакты — частота зависит от loss_prob"""
    h, w = frame.shape[:2]
    corrupted = frame.copy()
    
    artifact_freq = min(loss_prob * 3, 0.5)
    if loss_prob < 0.005 or random.random() > artifact_freq:
        return corrupted
    
    max_blocks = max(1, int(loss_prob * 20))
    num_blocks = random.randint(1, min(max_blocks, 4))
    block_size = 32
    
    for _ in range(num_blocks):
        x = random.randint(0, max(0, (w - block_size) // block_size)) * block_size
        y = random.randint(0, max(0, (h - block_size) // block_size)) * block_size
        x_end = min(x + block_size, w)
        y_end = min(y + block_size, h)
        corrupted[y:y_end, x:x_end] = np.random.randint(0, 255, (y_end - y, x_end - x, 3), dtype=np.uint8)
    
    return corrupted

def get_freeze_duration(loss_prob):
    """Возвращает длительность фриза в кадрах в зависимости от вероятности потерь"""
    if loss_prob < 0.005:   # < 0.5%
        return 0
    elif loss_prob < 0.01:  # 0.5-1%
        return random.randint(1, 2)
    elif loss_prob < 0.03:  # 1-3%
        return random.randint(2, 3)
    elif loss_prob < 0.05:  # 3-5%
        return random.randint(2, 4)
    else:                   # 5-10%
        return random.randint(3, 6)

def main():
    if len(sys.argv) < 4:
        print("Использование: python sender_final.py <video> <jitter_ms> <loss_percent>")
        sys.exit(1)

    video_path = sys.argv[1]
    jitter_ms = float(sys.argv[2])
    loss_percent = float(sys.argv[3])
    ip = "127.0.0.1"
    port = 5005

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Ошибка: не удалось открыть {video_path}")
        sys.exit(1)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    loss_prob = loss_percent / 100.0
    max_jitter = jitter_ms / 1000.0

    seq = 0
    sent = 0
    last_frame = None
    freeze_counter = 0

    print(f"Отправка {video_path} | Loss={loss_percent}% | Jitter={jitter_ms}мс")
    print("Режим: фризы зависят от % потерь + артефакты")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 1. ФРИЗЫ (длительность зависит от loss_prob)
        if freeze_counter > 0:
            frame = last_frame.copy() if last_frame is not None else frame
            freeze_counter -= 1
        elif random.random() < loss_prob:
            freeze_duration = get_freeze_duration(loss_prob)
            freeze_counter = freeze_duration
            if last_frame is not None:
                frame = last_frame.copy()

        # 2. ДЖИТТЕР
        if max_jitter > 0:
            time.sleep(random.uniform(0, max_jitter))

        # 3. АРТЕФАКТЫ
        frame = add_artifacts(frame, loss_prob)

        ok, buf = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        if not ok:
            continue

        packet = struct.pack('>I', len(buf)) + struct.pack('>I', seq) + buf.tobytes()
        sock.sendall(packet)
        seq += 1
        sent += 1
        last_frame = frame.copy()

    cap.release()
    sock.close()
    print(f"Отправлено кадров: {sent}")

if __name__ == "__main__":
    main()