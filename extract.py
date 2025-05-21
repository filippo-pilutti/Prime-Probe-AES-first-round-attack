import argparse
import os
from lib.parser import  parse_aes_file
from lib.utils import (
    compute_cache_line_averages, compute_averages_for_plaintext_group,
    averages_correction, extract_cache_misses, recover_4msb_key_for_byte
    )
from lib.heatmap_generator import generate_heatmap
from lib.const import PLAINTEXT_BYTES

pdf_out_path = "heatmaps.pdf"

if __name__ == "__main__":

    p = argparse.ArgumentParser(description="extract.py [<input-trace>]")
    p.add_argument("trace_file", nargs='?', help="Optional path for AES attack output file (defaults to 'output.txt')")
    args = p.parse_args()

    if args.trace_file:
        path = args.trace_file
    else:
        path = "output.txt"

    if not os.path.isfile(path):
        raise FileNotFoundError(f"Trace file not found: {path}")

    print("Recovering key... ")

    # Parse the data from the file and save it in a data structure
    aes_data = parse_aes_file(path)
    
    # Compute averages of all samples
    line_averages = compute_cache_line_averages(aes_data)

    # Key recovery 
    # For each byte of the plaintext, calculate corrected averages for the 4 MSBs and generate heatmap to find cache misses
    recovered_key: list[str] = []
    for byte_index in range(PLAINTEXT_BYTES):
        
        # Mean cache access values grouped by the 16 possible 4 MSBs of the current plaintext byte
        msb_averages = compute_averages_for_plaintext_group(aes_data, byte_index)
       
        # Apply correction to averages for the current byte
        corr_msb_averages = averages_correction(msb_averages, line_averages)

        # Generate heatmap on the corrected averages
        generate_heatmap(corr_msb_averages, byte_index)

        # Recover key
        cache_misses = extract_cache_misses(corr_msb_averages)
        key_byte = recover_4msb_key_for_byte(cache_misses, byte_index)
        print(f"Key for byte {byte_index}: {key_byte}")
        recovered_key.append(key_byte)

    # Output recovered partial key to a file key.txt
    with open("key.txt", 'w') as key_file:
        key_file.write(str(recovered_key))
    