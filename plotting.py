import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from loading import load_patchmaster_file

def detect_spikes(time_ms, voltage_mv, threshold=0):
    peaks, peak_properties = find_peaks(voltage_mv, height=threshold)
    return time_ms[peaks], voltage_mv[peaks]

def plot_all_sweeps(directory, file_name, show_plots=False, save_folder=None):

    # load file the is to be plotted
    bundle = load_patchmaster_file(directory, file_name)

    for group_index, group in enumerate(bundle.pul):
        print(f"Group {group_index + 1}")
        for series_index, series in enumerate(group):
            print(f"  Series {series_index + 1}")
            for sweep_index, sweep in enumerate(series):
                print(f"    Sweep {sweep_index + 1}")

                # get trace objects
                trace0, trace1 = sweep[0], sweep[1]

                # get corresponding data
                data0 = bundle.data[group_index, series_index, sweep_index, 0]
                data1 = bundle.data[group_index, series_index, sweep_index, 1]

                # decide which is current and which is voltage
                if trace0.YUnit == "A":
                    current_trace, current_data = trace0, data0
                    voltage_trace, voltage_data = trace1, data1
                else:
                    current_trace, current_data = trace1, data1
                    voltage_trace, voltage_data = trace0, data0
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
                axs[0].set_ylabel("Current [pA]")

                # plot voltage on bottom
                axs[1].plot(plot_time, voltage_data_mv)
                axs[1].set_ylabel("Voltage [mV]")
                axs[1].set_xlabel("Time [ms]")

                # detect and mark spikes
                spike_times, spike_amplitudes = detect_spikes(plot_time, voltage_data_mv)
                axs[1].plot(spike_times, spike_amplitudes, 'x', label='spikes')
                axs[1].legend()


                # fixed axis limits
                axs[0].set_ylim(-100, 400)
                axs[1].set_ylim(-100, 60)

                # plt.tight_layout()
                fig.suptitle(f"{file_name}\nGroup {group_index + 1}, Series {series_index + 1}, Sweep {sweep_index + 1}")

                # save figure
                os.makedirs(save_folder, exist_ok=True)
                save_name = f"{file_name}_G{group_index+1}_S{series_index+1}_W{sweep_index+1}.png"
                fig.savefig(os.path.join(save_folder, save_name))

                # show or close the plot
                if show_plots:
                    plt.show()
                else:
                    plt.close(fig)