import os.path
import heka_reader  

def load_patchmaster_file(directory, file_name):
    path = os.path.join(directory, file_name)
    return heka_reader.Bundle(path)