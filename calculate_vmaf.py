import subprocess
import re
import csv
from pathlib import Path

RESULTS_DIR = Path("results")
REF_DIR = Path("reference")
OUTPUT_CSV = Path("vmaf_scores.csv")

def calculate_vmaf(ref_path, dist_path):
    """Рассчитывает VMAF через прямой вызов FFmpeg и парсит вывод в реальном времени."""
    try:
        cmd = [
            "ffmpeg", "-i", str(ref_path), "-i", str(dist_path),
            "-lavfi", "libvmaf",
            "-f", "null", "-"
        ]
        
        # Запускаем FFmpeg и захватываем вывод stderr (туда пишется VMAF)
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Ищем VMAF score в выводе
        # Пример строки: "[libvmaf] VMAF score: 93.456789"
        match = re.search(r"VMAF score:\s*([\d\.]+)", result.stderr)
        if match:
            vmaf = float(match.group(1))
            return round(vmaf, 2)
        
        # Альтернативный поиск в stdout
        match = re.search(r"VMAF score:\s*([\d\.]+)", result.stdout)
        if match:
            vmaf = float(match.group(1))
            return round(vmaf, 2)
        
        return None
    except Exception as e:
        print(f"    Ошибка: {e}")
        return None

def main():
    distorted_videos = list(RESULTS_DIR.glob("*.mp4"))
    print(f"🔍 Найдено видео для анализа: {len(distorted_videos)}")
    
    results = []
    for i, dist_path in enumerate(distorted_videos, 1):
        # Извлекаем имя эталона из имени файла (часть до "_loss")
        video_name = dist_path.stem.split("_loss")[0]
        ref_path = REF_DIR / f"{video_name}.mp4"
        
        if not ref_path.exists():
            print(f"[{i}/{len(distorted_videos)}] ❌ Эталон для {video_name} не найден")
            continue
        
        print(f"[{i}/{len(distorted_videos)}] 📊 {dist_path.name}")
        vmaf = calculate_vmaf(ref_path, dist_path)
        
        if vmaf is not None:
            # Парсим параметры из имени файла
            parts = dist_path.stem.split("_")
            loss = None
            jitter = None
            for part in parts:
                if part.startswith("loss"):
                    loss = float(part.replace("loss", ""))
                if part.startswith("jitter"):
                    jitter = int(part.replace("jitter", ""))
            repeat = int(parts[-1].replace("rep", ""))
            
            results.append({
                "video": video_name,
                "loss": loss,
                "jitter": jitter,
                "repeat": repeat,
                "vmaf": vmaf
            })
            print(f"    ✅ VMAF = {vmaf}")
        else:
            print(f"    ❌ VMAF не рассчитан")
    
    if results:
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["video", "loss", "jitter", "repeat", "vmaf"])
            writer.writeheader()
            writer.writerows(results)
        print(f"\n✅ Результаты сохранены в {OUTPUT_CSV}")
        print(f"   Успешно обработано: {len(results)} из {len(distorted_videos)} файлов")
    else:
        print("\n❌ Не удалось рассчитать VMAF ни для одного файла")

if __name__ == "__main__":
    main()