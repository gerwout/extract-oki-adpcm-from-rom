import subprocess
import time
import os
from pathlib import Path
import argparse

def read_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")
def get_adpcm_addresses(content):
    # Define the chunk size
    chunk_size = 4
    addresses = []
    # Iterate over the bytes object in chunks
    # skip the first 3 bytes, the MST3736 does not seem to use these
    for i in range(3, len(content), chunk_size):
        chunk = content[i:i + chunk_size]
        if chunk == b'\x00\x00\x00\x00':
            break
            break
            # the first 3 bytes are not used as the address
        addresses.append(''.join(map('{:02x}'.format, chunk))[3:])

    # MST3736, orders the samples from low to high, lets check if this is the case
    for i in range(len(addresses) - 1):
        if addresses[i] > addresses[i + 1]:
            print("This does not seem to be a MST3736 rom file.")
            exit(0)

    return addresses

def get_sample(content, dec_address):
    length = content[dec_address]
    # bit 8 is not used, so we cap it to 127 max
    length &= 127
    data = content[dec_address + 1:dec_address + 1 + length]

    while length != 0:
        # length of the "length byte" + 1 for the block marker
        dec_address += length + 1
        try:
            length = content[dec_address]
            length &= 127
        except IndexError:
            print("The sample location is not inside this rom file. This typically happens when there are multiple seperate rom files that need to be combined in a single file.")
            exit(0)
        data += content[dec_address + 1:dec_address + 1 + length]

    return data

def main():
    parser = argparse.ArgumentParser(description='Extract samples from Oki MSM6376 sound rom files')

    parser.add_argument('--file', dest='file', type=str, required=True, help='The input file path')
    parser.add_argument('--khz', dest='khz', type=float, default=32, help='The sampling rate in kHz (default: 32)')
    args = parser.parse_args()

    content = read_file(args.file)
    addresses = get_adpcm_addresses(content)

    rom_path = Path(args.file)
    pcm_dir = "output/" + rom_path.name + "/pcm/"
    wav_dir = "output/" + rom_path.name + "/wav/"
    if not os.path.exists(pcm_dir):
        os.makedirs(pcm_dir)
    if not os.path.exists(wav_dir):
        os.makedirs(wav_dir)
    print("There are " + str(len(addresses)) + " samples found")

    for address in addresses:
        dec_address = int("0x" + address, 16)

        file_name = pcm_dir +  hex(dec_address) + ".pcm"
        wav_file = wav_dir + hex(dec_address) + ".wav"
        sample = get_sample(content, dec_address)
        print("Saving " + file_name)
        with open(file_name, 'w+b') as f:
            f.write(sample)
        f.close()
        print("Converting to " + wav_file)
        command = "ffmpeg -y -f u8 -c adpcm_ima_oki -ar " + str(args.khz) + "k -ac 1 -i " + file_name + " " + wav_file
        print(command)
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE)
            process.wait()
            output, error = process.communicate()
        except FileNotFoundError:
            print("Warning! ffmpeg is not installed or the executable is not defined in the PATH environment variable!")

if __name__ == "__main__":
  main()