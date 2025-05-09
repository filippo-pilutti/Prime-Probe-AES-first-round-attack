from lib.parser import  parse_aes_file
from lib.average_utils import compute_cache_line_averages, compute_averages_for_plaintext_group, averages_correction

aes_file_path = "output.txt"

if __name__ == "__main__":

    # Parse the data from the file and save it in a data structure
    aes_data = parse_aes_file(aes_file_path)
    
    # Compute averages of all samples
    #line_averages = compute_cache_line_averages(aes_data)

    #msb_averages = compute_averages_for_plaintext_group(aes_data, 0)

    avg = averages_correction(compute_averages_for_plaintext_group(aes_data, 0), compute_cache_line_averages(aes_data))

    print(f"First entry: {aes_data[0]}" )
    print(f"Averages: {avg}")
    