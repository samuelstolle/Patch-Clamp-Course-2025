import os
from matplotlib import pyplot as plt
from analysis import detect_spikes, prepare_sweep
from loading import load_file

def plot_single_sweep(
        time_ms,
        current_trace,
        current_data_pa,
        voltage_trace,
        voltage_data_mv,
        title,
        show_spikes=True
):
    """
    Generate a two-panel Current/Voltage plot for one sweep, optionally marking detected spikes.

    Parameters
    ----------
    time_ms : numpy.ndarray
        Time points in milliseconds
    current_trace : object
        Metadata object for the current trace (e.g., label, units)
    current_data_pa : numpy.ndarray
        Current values in picoamperes
    voltage_trace : object
        Metadata object for the voltage trace
    voltage_data_mv : numpy.ndarray
        Voltage values in millivolts
    title : str
        Figure title to display at the top
    show_spikes : bool, optional
        Whether to detect and mark spikes on the voltage trace (default is True)

    Returns
    -------
    fig : matplotlib.figure.Figure
        The generated Figure containing the two subplots.
    """

    # create plot for pairs of current and voltage
    fig, axs = plt.subplots(2, 1, sharex=True, layout=None)

    # plot current on top
    axs[0].plot(time_ms, current_data_pa)
    axs[0].set_ylabel("Current [pA]")
    axs[0].set_ylim(-100, 400)

    # plot voltage on bottom
    axs[1].plot(time_ms, voltage_data_mv)
    if show_spikes:
        spike_times, spike_voltages = detect_spikes(time_ms, voltage_data_mv)
        axs[1].plot(spike_times, spike_voltages, 'x', label=f'spikes ({len(spike_times)})')
        axs[1].legend()
    axs[1].set_ylabel("Membrane Potential [mV]")
    axs[1].set_xlabel("Time [ms]")
    axs[1].set_ylim(-100, 60)

    fig.suptitle(title)
    return fig

def plot_sweeps(
        directory,
        file_name,
        save_folder=None,
        show_plots=False
):
    bundle = load_file(directory, file_name)
    os.makedirs(save_folder, exist_ok=True) # if necessary, create a folder to save the plots

    for group_index, group in enumerate(bundle.pul):
        print(f"Group {group_index + 1}")
        for series_index, series in enumerate(group):
            print(f"  Series {series_index + 1}")
            for sweep_index, sweep in enumerate(series):
                print(f"    Sweep {sweep_index + 1}")

                time_ms, current_trace, current_data_pa, voltage_trace, voltage_data_mv = prepare_sweep(bundle, group_index, series_index, sweep_index)

                title = f"{file_name}\nGroup{group_index + 1}-Series{series_index + 1}-Sweep{sweep_index + 1}"
                fig = plot_single_sweep(time_ms, current_trace, current_data_pa, voltage_trace, voltage_data_mv, title)

                # save figure
                save_name = f"{file_name}_{group_index+1}_{series_index+1}_{sweep_index+1}.png"
                fig.savefig(os.path.join(save_folder, save_name))

                # show or close the plot
                if show_plots:
                    plt.show()
                else:
                    plt.close(fig)