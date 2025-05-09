from lib.parser import  parse_aes_file
from lib.average_utils import compute_cache_line_averages, compute_averages_for_plaintext_group, averages_correction
from lib.heatmap_generator import generate_heatmap
from lib.const import PLAINTEXT_BYTES

aes_file_path = "output.txt"

if __name__ == "__main__":

    # Parse the data from the file and save it in a data structure
    aes_data = parse_aes_file(aes_file_path)
    
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

        # (TODO) Recover key


    print(f"First entry: {aes_data[0]}" )
    #print(f"Averages: {avg}")
    