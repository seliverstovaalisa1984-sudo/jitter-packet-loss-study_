import subprocess
import time
import itertools
import sys
from pathlib import Path

REF_DIR = Path("reference")
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

VIDEOS = ["танцы_эталон", "интервью_эталон"]
JITTERS = [0, 10, 50, 75, 100, 300]      # 6 значений
LOSSES = [0, 0.5, 1, 3, 5, 10]            # 6 значений
REPEATS = 3

def run_test(video_name, jitter, loss, repeat, idx, total):
    video_path = REF_DIR / f"{video_name}.mp4"
    output_path = RESULTS_DIR / f"{video_name}_loss{loss}_jitter{jitter}_rep{repeat}.mp4"
    
    print(f"[{idx}/{total}] {video_name} | Loss={loss}% | Jitter={jitter}мс | rep={repeat}")
    
    recv = subprocess.Popen([sys.executable, "receiver_final.py", str(output_path)])
    time.sleep(1.5)
    send = subprocess.Popen([
        sys.executable, "sender_final.py",
        str(video_path), str(jitter), str(loss)
    ])
    send.wait()
    time.sleep(2)
    recv.terminate()
    recv.wait()
    
    return output_path.exists() and output_path.stat().st_size > 100000

def main():
    experiments = list(itertools.product(VIDEOS, JITTERS, LOSSES, range(1, REPEATS + 1)))
    total = len(experiments)
    print(f"🚀 Запись {total} видео...\n")
    
    for i, (video, jitter, loss, rep) in enumerate(experiments, 1):
        run_test(video, jitter, loss, rep, i, total)
    
    print(f"\n✅ Готово! Все видео записаны в {RESULTS_DIR}")

if __name__ == "__main__":
    main()