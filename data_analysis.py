"""
This module contains data analysis functions for downloading and processing
temperature data from Brekeley Earth.
"""
# import only necessary modules (i.e. skip matplotlib)
import numpy as np
import requests  
import os

def generate_url(location):
    # using fairly modern python syntax call f-strings
    url = f'http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/{location.lower()}-TAVG-Trend.txt'
    return url

def download_data(location):
    data_fname = f'data-{location.lower()}.txt'
    # download data if have not already
    if ~os.path.isfile(data_fname):
        url = generate_url(location)
        # Download the content of the URL
        response = requests.get(url)
        # Save it to a file
        with open(data_fname, 'w') as open_file:
            open_file.write(response.text)
    
    # Parse data (skip the header records which are marked with a %)
    data = np.loadtxt(data_fname, comments="%")
    
    # *alternative approach: download directly to memory, don't save to disk
    #respone = requests.get(url)
    #data = np.loadtxt(response.iter_lines(), comments='%')
    
    return data

def moving_average(data, width):
    moving_avg = np.full(data.size, np.nan)
    for i in range(width, moving_avg.size - width):
        moving_avg[i] = np.mean(data[i - width:i + width])
        
    return moving_avg

# define tests here too 
def test_moving_avg():
    avg = moving_average(np.ones(1000), 2)
    assert np.all(np.isnan(avg[0:2]))
    assert np.all(np.isnan(avg[-2:]))
    assert np.allclose(avg[2:-2], 1)
