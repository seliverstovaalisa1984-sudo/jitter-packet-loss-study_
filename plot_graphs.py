import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# === ВАШИ ДАННЫЕ ===
interview_data = [
    [0, 93.34], [0.5, 93.06], [1, 92.19], [3, 86.55], [5, 81.75], [10, 71.37],
]
dance_data = [
    [0, 97.28], [0.5, 96.69], [1, 92.79], [3, 88.12], [5, 79.01], [10, 64.48],
]

# Данные для разных Jitter (Интервью)
interview_jitter = {
    0: [93.34, 93.06, 92.19, 86.55, 81.75, 71.37],
    10: [93.34, 93.03, 91.78, 86.41, 79.95, 70.57],
    50: [93.33, 93.00, 91.63, 86.51, 78.89, 70.39],
    75: [93.31, 92.17, 91.06, 85.77, 77.89, 70.30],
    100: [93.30, 92.33, 90.72, 85.33, 76.79, 69.06],
    300: [93.29, 92.03, 90.45, 84.80, 75.63, 68.01],
}

# Данные для разных Jitter (Танцы)
dance_jitter = {
    0: [97.28, 96.69, 92.79, 88.12, 79.01, 64.48],
    10: [97.28, 96.33, 92.41, 88.37, 76.88, 64.00],
    50: [97.25, 95.48, 92.03, 88.34, 75.45, 61.83],
    75: [97.24, 94.83, 91.36, 87.38, 75.39, 61.24],
    100: [97.23, 94.38, 90.71, 86.74, 74.15, 60.96],
    300: [97.20, 94.20, 90.44, 85.73, 73.74, 59.03],
}

losses = [0, 0.5, 1, 3, 5, 10]
jitter_values = [0, 10, 50, 75, 100, 300]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

output_dir = Path("plots")
output_dir.mkdir(exist_ok=True)

def setup_ax(ax, title, ylabel=True):
    """Настройка стиля как на скриншоте"""
    ax.set_facecolor('#E0E0E0')  # светло-серая заливка
    ax.grid(True, linestyle='-', linewidth=0.5, color='white', alpha=1)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(direction='out', length=4, width=1, colors='black')
    ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
    ax.set_xlabel('Loss, %', fontsize=10, fontweight='bold')
    if ylabel:
        ax.set_ylabel('VMAF, баллы', fontsize=10, fontweight='bold')
    ax.set_xticks([0, 2, 4, 6, 8, 10])
    ax.set_xticklabels(['0', '2', '4', '6', '8', '10'])
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(50, 100)

# === ГРАФИК 1: ИНТЕРВЬЮ (VMAF vs Loss) ===
fig, ax = plt.subplots(figsize=(9, 6))
setup_ax(ax, "Интервью", ylabel=True)

for i, jitter in enumerate(jitter_values):
    ax.plot(losses, interview_jitter[jitter], 'o-', 
            color=colors[i], linewidth=2.5, markersize=6, 
            label=f'jitter = {jitter} ms')

ax.legend(loc='upper right', frameon=True, fancybox=False, edgecolor='black', fontsize=9)
plt.tight_layout()
plt.savefig(output_dir / 'intervyu_vmaf_loss.png', dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'intervyu_vmaf_loss.pdf', bbox_inches='tight')
plt.close()
print("✅ 1. Интервью график сохранён")

# === ГРАФИК 2: ТАНЦЫ (VMAF vs Loss) ===
fig, ax = plt.subplots(figsize=(9, 6))
setup_ax(ax, "Танцы", ylabel=True)

for i, jitter in enumerate(jitter_values):
    ax.plot(losses, dance_jitter[jitter], 'o-', 
            color=colors[i], linewidth=2.5, markersize=6, 
            label=f'jitter = {jitter} ms')

ax.legend(loc='upper right', frameon=True, fancybox=False, edgecolor='black', fontsize=9)
plt.tight_layout()
plt.savefig(output_dir / 'dance_vmaf_loss.png', dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'dance_vmaf_loss.pdf', bbox_inches='tight')
plt.close()
print("✅ 2. Танцы график сохранён")

# === ГРАФИК 3: СРАВНЕНИЕ (оба видео, Jitter=0) ===
fig, ax = plt.subplots(figsize=(9, 6))
setup_ax(ax, "Сравнение видео (jitter = 0 мс)", ylabel=True)

ax.plot(losses, interview_jitter[0], 'o-', color='#1f77b4', linewidth=2.5, markersize=6, label='Интервью')
ax.plot(losses, dance_jitter[0], 's-', color='#ff7f0e', linewidth=2.5, markersize=6, label='Танцы')

ax.legend(loc='upper right', frameon=True, fancybox=False, edgecolor='black', fontsize=10)
plt.tight_layout()
plt.savefig(output_dir / 'comparison_jitter0.png', dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'comparison_jitter0.pdf', bbox_inches='tight')
plt.close()
print("✅ 3. Сравнительный график сохранён")

# === ГРАФИК 4: VMAF vs JITTER (для разных Loss) ===
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_facecolor('#E0E0E0')
ax.grid(True, linestyle='-', linewidth=0.5, color='white', alpha=1)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.set_title('Зависимость VMAF от джиттера', fontsize=12, fontweight='bold', pad=10)
ax.set_xlabel('Джиттер, мс', fontsize=10, fontweight='bold')
ax.set_ylabel('VMAF, баллы', fontsize=10, fontweight='bold')
ax.set_ylim(50, 100)

loss_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
loss_labels = ['Loss 0%', 'Loss 0.5%', 'Loss 1%', 'Loss 3%', 'Loss 5%', 'Loss 10%']

for i, loss in enumerate(losses):
    values = []
    for jitter in jitter_values:
        if loss == 0:
            val = interview_jitter[jitter][0]
        elif loss == 0.5:
            val = interview_jitter[jitter][1]
        elif loss == 1:
            val = interview_jitter[jitter][2]
        elif loss == 3:
            val = interview_jitter[jitter][3]
        elif loss == 5:
            val = interview_jitter[jitter][4]
        else:
            val = interview_jitter[jitter][5]
        values.append(val)
    ax.plot(jitter_values, values, 'o-', color=loss_colors[i], linewidth=2, markersize=6, label=loss_labels[i])

ax.legend(loc='lower left', frameon=True, fancybox=False, edgecolor='black', fontsize=8)
plt.tight_layout()
plt.savefig(output_dir / 'vmaf_vs_jitter.png', dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'vmaf_vs_jitter.pdf', bbox_inches='tight')
plt.close()
print("✅ 4. График VMAF vs Jitter сохранён")

print(f"\n✅ Все графики сохранены в папку: {output_dir.absolute()}")
print("   Форматы: PNG и PDF")