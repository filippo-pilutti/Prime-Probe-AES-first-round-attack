from dataclasses import dataclass
from lib.const import SETS, FIRST_POSSIBLE_BITS, TTABLE_OFFSET, PLAINTEXT_BYTES
from lib.parser import AESData
from collections import defaultdict, Counter
import statistics

@dataclass
class GroupAvg(object):
    plaintext_hex: str
    averages: list[float]

# Calculate the average value for each CL position across all sample
def compute_cache_line_averages(samples: list[AESData]) -> list[float]:
    
    # Create a list representing the CL values along each cache line and initialize empty
    cache_line_values: list[list[int]] = [[] for _ in range(SETS)]
    
    # Group values in the same line for all samples
    for sample in samples:
        for i, val in enumerate(sample.cl_values):
            cache_line_values[i].append(val)

    # Calculate the average of each cache line
    line_averages: list[float] = [statistics.mean(cl_val) for cl_val in cache_line_values]

    return line_averages

# Group AES samples by the 4 MSBs of a given byte of the plaintext and compute the cache line averages for each group
# Return a list of averages, one for each group of 4 MSBs. I will have 16 groups at the end
def compute_averages_for_plaintext_group(samples: list[AESData], byte_index: int) -> list[GroupAvg]:
    # Group samples by the 4 MSBs of the target byte
    grouped_samples = defaultdict(list)
    for sample in samples:
        byte_value = bytes.fromhex(sample.plaintext)[byte_index] # Convert hex plaintext string to bytes
        msb = f"0x{byte_value >> 4:X}" # Extract and format the 4 MSBs
        grouped_samples[msb].append(sample)
    
    # Compute averages for each MSB group
    msb_averages = [0] * len(FIRST_POSSIBLE_BITS)
    for hex_msb in FIRST_POSSIBLE_BITS:
        samples = grouped_samples.get(hex_msb, [])
        averages = compute_cache_line_averages(samples)
        index = int(hex_msb, 16)
        msb_averages[index] = GroupAvg(
            plaintext_hex = hex_msb, averages = averages
        )

    return msb_averages

# Apply correction to clean the data
# For each group 4 MSBs of the plaintext, subtract from the average of the cache line the average of all the samples
def averages_correction(msb_averages: list[GroupAvg], line_averages: list[float]) -> list[GroupAvg]:
    msb_averages_copy = [
        GroupAvg(sample.plaintext_hex, sample.averages)
        for sample in msb_averages
    ]
    for sample_averages in msb_averages_copy:
        for cache_line_num, cache_line_average in enumerate(sample_averages.averages):
            sample_averages.averages[cache_line_num] = (
                cache_line_average - line_averages[cache_line_num]
            )
    return msb_averages_copy

# Identify the cache miss set for each 4-bit plaintext MSBs by finding the index of the maximum timing
# measurement in the corrected averages
def extract_cache_misses(corr_averages: list[GroupAvg]) -> list[int]:
    cache_miss_sets = []
    for bits, avg in enumerate(corr_averages):
        max_index = avg.averages.index(max(avg.averages))
        cache_miss_sets.append(max_index)
    return cache_miss_sets

# Recover most significant 4 bits of a key byte using cache misses
def recover_4msb_key_for_byte(cache_misses: list[int], byte_index: int) -> str:
    # Find which table is being used and compute its base table
    # T0:02-17, T1:18-33, T2:34-49, T3:50-01 (with wrap-around)
    table_number = (byte_index % 4)
    base_table = ((table_number + TTABLE_OFFSET) % 4) * 16 + TTABLE_OFFSET

    candidates = []

    for plaintext_msb in range(PLAINTEXT_BYTES):
        cache_miss_set = cache_misses[plaintext_msb]

        # Calculate the set index within the table
        table_set_index = (cache_miss_set - base_table) % SETS # Handle wrap-around

        candidate_key_msb = table_set_index ^ plaintext_msb
        candidates.append(candidate_key_msb)
    
    # Identify most frequent candidate
    key_msb = Counter(candidates).most_common(1)[0][0]

    return f"0x{key_msb:X}"
