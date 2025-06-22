from loading import load_patchmaster_file
from plotting import plot_all_sweeps

def main():
    directory = "measurements"
    file_name = "2025-06-18_1_cultured-cells.dat"

    load_patchmaster_file(directory, file_name)
    plot_all_sweeps(directory, file_name)

if __name__ == '__main__':
    main()