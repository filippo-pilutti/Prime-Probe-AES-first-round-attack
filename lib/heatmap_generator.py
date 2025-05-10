import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os
from lib.utils import GroupAvg

y_labels = [f"{i:X}0" for i in range(16)]

def generate_heatmap(averages: list[GroupAvg], byte_index: int):
    os.makedirs("heatmaps", exist_ok=True)
    output_file_path = f"heatmaps/byte_{byte_index}.png"
    heatmap_data = np.array([p.averages for p in averages])

    plt.figure(figsize=(14, 5))
    plt.imshow(heatmap_data, cmap='hot', aspect='auto')

    plt.xlabel('Cache Set')
    plt.ylabel('Plaintext MSB (4 bits)')
    plt.yticks(ticks=range(len(y_labels)), labels=y_labels)
    plt.xticks(ticks=range(64))
    plt.title(f'AES Cache Access Heatmap - Byte {byte_index}')

    plt.tight_layout()
    plt.savefig(output_file_path)
    plt.close()
