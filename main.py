import sys
import os

def process_arc_file(input_file_path, output_directory):
    with open(input_file_path, "rb") as file:
        data = file.read()

    sector = 0
    fileId = 0
    ms = bytearray(data)
    offset = 0
    sector = int.from_bytes(ms[offset:offset + 3], byteorder='little')

    while sector != 0:
        size = int.from_bytes(ms[offset + 4:offset + 7], byteorder='little')
        backup = offset

        arc_size = int.from_bytes(data[sector * 0x800 + 4:sector * 0x800 + 7], byteorder='little')

        if arc_size < 0x4:
            print("ERROR: Invalid File Size")
            return
        elif arc_size != size:
            file_name = f"ARC_{fileId:X}.BIN"
        else:
            file_name = f"ARC_{fileId:X}.ARC"

        offset = sector * 0x800
        file_data = ms[offset:offset + size]

        output_file_path = os.path.join(output_directory, file_name)

        with open(output_file_path, "wb") as output_file:
            output_file.write(file_data)

        offset = backup
        offset += 8
        fileId += 1
        if fileId > 512:
            print("Max File Id exceeded")
            return
        sector = int.from_bytes(ms[offset:offset + 3], byteorder='little')
    #=========
    print("Program Completed, " + str(fileId) + " Files were created.")

#Start of Program
if len(sys.argv) != 3:
    print("Made by PogChampGuy AKA Kuumba")
    print("This Program is used for extracting MegaMan X5/X6 DAT files into ARC/BIN files")
    print("Usage: python main.py <input_file> <output_directory>")
else:
    input_file_path = sys.argv[1]
    output_directory = sys.argv[2]

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    process_arc_file(input_file_path, output_directory)