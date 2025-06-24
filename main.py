from src.plotting import plot_sweeps

def main():
    directory = "raw_data" # Where are your .dat files stored?
    file_name = "2025-06-18_1_cultured-cells.dat" # Which .dat file you want to analyze?
    save_folder = "plots" # Where do you want to save the plots?
    show_plots = False # Do you want to see the plots while they're being created?

    plot_sweeps(
        directory=directory,
        file_name=file_name,
        save_folder=save_folder,
        show_plots=show_plots
    )

if __name__ == '__main__':
    main()