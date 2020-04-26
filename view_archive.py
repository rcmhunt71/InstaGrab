import os
import pickle
import sys


def get_inv_from_file(filename):
    inv = {}
    if os.path.exists(filename):
        with open(filename, "rb") as ARCHIVE:
            inv = pickle.load(ARCHIVE)
        print(f"Read archived inventory from {filename}")
    else:
        print(f"\nERROR:\n\tUnable to open archive filename: '{filename}'")
    return inv


if __name__ == "__main__":
    archive_file = sys.argv[1] if len(sys.argv) > 1 else "inventory.dat"
    for index, (name, data) in enumerate(get_inv_from_file(archive_file).items()):
        print(f"({index}) {name} --> {str(data)}")
