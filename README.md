# AES Prime+Probe Side-Channel Attack

This project demonstrates a **cache timing side-channel attack** on the first round of AES using the **Prime+Probe** technique. By analyzing the victim’s memory access patterns through cache probe timings, we recover the **4 most significant bits (MSBs)** of each AES key byte, and optionally extend this to full key recovery.

## Repository Structure

```
project_root/
│
├── program/                  # Core codebase
│   ├── extract.py            # Main key extraction pipeline
│   ├── utils.py              # Averaging, grouping, key recovery logic
│   ├── parser.py             # Trace file parser
│   ├── heatmap_generator.py  # Heatmap PDF generation
│   ├── const.py              # Constants (T-table offsets, etc.)
│
├── output.txt                # Input trace file (plaintext, ciphertext, cache timings)
├── key.txt                   # Recovered MSBs of AES key (hex list)
├── heatmaps.pdf              # Heatmaps of cache set timings
├── approach.pdf              # Full technical explanation of the method
└── heatmap.pdf               # Visual-only PDF with heatmaps
```

## Usage

### Run the key recovery pipeline

```bash
cd program
python extract.py
```

Or specify a custom trace file:

```bash
python extract.py ../output.txt
```

### Output Files

- `key.txt`: 16 MSB key nibbles (as hex strings)
- `heatmaps.pdf`: Visual representation of cache access timings

## How It Works

- The AES implementation uses **lookup tables** (T-tables) for fast encryption.
- Cache accesses during round 1 depend on `plaintext_byte ⊕ key_byte`, which leaks via the cache set accessed.
- By grouping and averaging access times by the 4 MSBs of the plaintext byte, and observing evicted cache sets, we recover the upper nibble of each key byte.

## Heatmaps

Heatmaps are automatically generated per key byte index. Each one shows which cache sets were evicted for each group of 4 MSBs of the plaintext byte, making the cache leak visually interpretable.

## Requirements

- Python 3.8+
- [`matplotlib`](https://matplotlib.org/)

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Related Files

- `approach.pdf`: Describes the methodology, key schedule usage, statistical techniques, and attack extension for full key recovery.
- `heatmap.pdf`: Contains only heatmaps for visual support.

## Notes

- The AES traces were collected using an instrumented implementation in `aesrun.c`, compiled and run on a Linux system with cache probing support.
- This attack assumes the victim shares the L1 cache and does not use constant-time T-table masking.

## License

This project is intended for **educational and academic purposes only**. Do not use this attack on systems you do not own or have explicit permission to test.

---

**Author**: *Filippo Pilutti*  
