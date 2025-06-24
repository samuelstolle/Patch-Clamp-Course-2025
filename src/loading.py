import os.path
import src.heka_reader

def load_file(directory, file_name):
    """
    Load .dat file from HEKA's PATCHMASTER software

    Parameters
    ----------
    directory : str
        Path to the directory, where the .dat file is stored

    file_name : str
        Name of the .dat file that is to be analyzed

    Returns
    -------
    bundle : heka_reader.Bundle
        A data bundle containing the loaded data, including raw traces, metadata, and protocol information.
    """
    path = os.path.join(directory, file_name)
    return src.heka_reader.Bundle(path)