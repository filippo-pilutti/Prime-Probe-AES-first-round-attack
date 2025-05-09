import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os
from lib.average_utils import GroupAvg
from lib.const import FIRST_POSSIBLE_BITS

y_labels = ["0", "1", "2", "3",
            "4", "5", "6", "7",
            "8", "9", "A", "B",
            "C", "D", "E", "F"]

def generate_heatmap(averages: list[GroupAvg], byte_index: int):
    os.makedirs("heatmaps", exist_ok=True)
    output_file_path = f"heatmaps/byte_{byte_index}.png"
    heatmap_data = np.array([p.averages for p in averages])

    plt.figure(figsize=(10, 4))
    plt.imshow(heatmap_data, cmap='hot', aspect='auto')
    plt.colorbar(label="Corrected Average")

    plt.xlabel('Cache Set')
    plt.ylabel('Plaintext MSB (4 bits)')
    plt.yticks(ticks=range(len(y_labels)), labels=y_labels)
    plt.title(f'AES Cache Access Heatmap - Byte {byte_index}')

    plt.tight_layout()
    plt.savefig(output_file_path)
    plt.close()
