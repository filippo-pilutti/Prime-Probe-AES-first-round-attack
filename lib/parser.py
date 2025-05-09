from dataclasses import dataclass

@dataclass
class AESData(object):
    plaintext: str
    ciphertext: str
    cl_values: list[int]


def parse_aes_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            entry = AESData(
                plaintext = parts[0],
                ciphertext = parts[1],
                cl_values = [int(val) for val in parts[2:]]
            )
            data.append(entry)
    return data