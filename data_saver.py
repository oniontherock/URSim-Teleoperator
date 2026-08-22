# this file is responsible for tracking data live while the program is running. It writes down data but on it's own it does nothing to preserve data outside of the current program
# if this file was the only one, no data would be preserved outside of the current instance of the program.
import numpy as np
from numpy.typing import NDArray
from datetime import datetime

def data_save_singular(file_name, formatted_data, data_format, data_header):

    date = datetime.now()

    formatted_date = date.strftime("%Y_%m_%d__%Hh%Mm%Ss")

    file_name_with_date = file_name + "__" + formatted_date

    formatted_name = file_name_with_date + ".txt"
    
    np.savetxt(
        "Data/" + formatted_name,
        formatted_data, 
        fmt=data_format, 
        delimiter=', ', 
        header=data_header, 
        comments=''
    )