import matplotlib as plt
from loading import load_patchmaster_file

def plot_all_sweeps(directory, file_name):
    bundle = load_patchmaster_file(directory, file_name)
    for group_index, group in enumerate(bundle.pul):
        print(f"Group {group_index + 1}")
        for series_index, series in enumerate(group):
            print(f"  Series {series_index + 1}")
            for sweep_index, sweep in enumerate(series):
                print(f"    Sweep {sweep_index + 1}")

                # get trace objects (metadata)
                current_trace = sweep[0]  # first trace: current
                voltage_trace = sweep[1]  # second trace: voltage

                # get trace data arrays
                current_data = bundle.data[group_index, series_index, sweep_index, 0]  # actual current values
                voltage_data = bundle.data[group_index, series_index, sweep_index, 1]  # actual voltage values

                # define time dimension
                start = voltage_trace.XStart
                interval = voltage_trace.XInterval
                data_points = len(voltage_data)

                time = np.linspace(start, start + interval * (data_points - 1), data_points)
                plot_time = time * 1000  # time in ms

                # data conversions
                current_data_pa = current_data * 1e12  # convert Ampere to Picoampere
                voltage_data_mv = voltage_data * 1e3  # convert Volts to Milivolts

                # create plot for pairs of current and voltage
                fig, axs = plt.subplots(2, 1, sharex=True, layout=None)

                # plot current on top
                axs[0].plot(plot_time, current_data_pa)  # time in ms
                axs[0].set_ylabel(f"{current_trace.Label} [pA]")

                # plot voltage on bottom
                axs[1].plot(plot_time, voltage_data_mv)
                axs[1].set_ylabel(f"{voltage_trace.Label} [mV]")
                axs[1].set_xlabel("Time [ms]")

                # plt.tight_layout()
                fig.suptitle(f"Group {group_index + 1}, Series {series_index + 1}, Sweep {sweep_index + 1}")
                plt.show()