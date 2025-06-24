import numpy as np
from scipy.signal import find_peaks

def detect_spikes(time_points,
                  voltage_values,
                  threshold=0
):

    """
    Find spike times & amplitudes in a voltage trace

    Parameters
    ----------
    time_points : array-like
        Time points (ms) for each sample
    voltage_values : array-like
        Voltage values (mV) at these time points
    threshold : float, optional
        Only count peaks taller than this (mV)

    Returns
    -------
    spike_times : ndarray
        Time point (ms) of each detected peak
    spike_amplitudes : ndarray
        Voltage (mV) of each detected peak

    """

    peaks, peak_properties = find_peaks(voltage_values, height=threshold, prominence=1) #TODO calculate suitable prominence
    spike_times, spike_amplitudes = time_points[peaks], voltage_values[peaks]
    return spike_times, spike_amplitudes

def prepare_sweep(
        bundle,
        group_index,
        series_index,
        sweep_index
):
    """
    Extract and convert one Current/Voltage sweep from the loaded data bundle.

    Parameters
    ----------
    bundle : heka_reader.Bundle
        The loaded data bundle
    group_index : int
        Group index within the bundle
    series_index : int
        Series index within that group
    sweep_index : int
        Sweep index within that series

    Returns
    -------
    time_ms : numpy.ndarray
        1D array of time points in milliseconds.
    current_trace : object
        Metadata object for the current (I) trace.
    current_data_pa : numpy.ndarray
        Current data in picoamperes.
    voltage_trace : object
        Metadata object for the voltage (V) trace.
    voltage_data_mv : numpy.ndarray
        Voltage data in millivolts.
    """
    sweep = bundle.pul[group_index][series_index][sweep_index]

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

    # data conversions
    time_ms = time * 1000  # convert time from s to ms
    current_data_pa = current_data * 1e12  # convert Ampere to Picoampere
    voltage_data_mv = voltage_data * 1e3  # convert Volts to Milivolts

    return time_ms, current_trace, current_data_pa, voltage_trace, voltage_data_mv