import numpy as np
#import matplotlib.pyplot as plt
from scipy import integrate
import wx
import os

# normalizes spectra to 1
def normspec(datain):
    out = datain
    out[:,1] = datain[:,1]/datain[:,1].max(0)
    return out

# converts filters spectra to 0-1 range
def normspec_filter(datain):
    out = datain
    maxvalue = datain[:,1].max(0)
    #print 'maxvalue: ', maxvalue
    if (maxvalue > 1):
        decdigits = np.floor(np.log(maxvalue)/np.log(10)) + 1
        out[:,1] = datain[:,1]/10**(decdigits)
        print 'maxvalue: ', maxvalue
        print 'Filter Normalized by division: ', 10**(decdigits)
    return out
    
def LoadFilter(caption, datatype, norm): # Load Spectral or Filter Data
    
    dlg = wx.FileDialog(None, caption, os.getcwd(), '', datatype, wx.OPEN)
    rows2skip = 0    
    if dlg.ShowModal() == wx.ID_OK:
        pathdata = dlg.GetPath()
        datatitle = os.path.basename(pathdata)
        #data = np.loadtxt(pathdata)
        
        for i in range(0,10,1):
    
            try:
                data = np.loadtxt(pathdata, skiprows = rows2skip)
                break
            except:
                rows2skip = rows2skip + 1
                #print rows2skip

        print 'Rows skipped during data import:',rows2skip        
        
        if (norm == 'dye'):
            data= normspec(data)
        elif (norm == 'filter'):
            data = normspec_filter(data)
        elif (norm == 'misc'):
            data = data
    
    dlg.Destroy()
    
    return data, datatitle, pathdata

def calcfilter(data,filter):

    # determine range of wavelengths
    wlrange_data = data[:,0]
    wlrange_filter = filter[:,0]
    # begining wavelengths
    wlstart_data = data[0,0]
    wlend_data = data[-1,0]
    wlstart_filter = filter[0,0]
    wlend_filter = filter[-1,0]
    
    # determine biggest value for start
    start = np.round(max(wlstart_data,wlstart_filter))
    
    # determine smallest value for end
    end = np.floor(min(wlend_data,wlend_filter))
    
    # find indicies for start & end inside the wavelength vector
    sdata = (wlrange_data == start).nonzero()
    edata = (wlrange_data == end).nonzero()
    sfilter = (wlrange_filter == start).nonzero()
    efilter = (wlrange_filter == end).nonzero()
    
    # and convert to normal arrays
    sdata = sdata[0]
    edata = edata[0]
    sfilter = sfilter[0]
    efilter = efilter[0]
    
    # extract data for the overlapping wavelength range
    exdata = data[sdata:edata,:]
    exfilter = filter[sfilter:efilter,:]
    
    # create equally spaced wavelength vector
    r = np.arange(start,end,step=1)
    
    # interpolate input data & filter data for that range
    dataintp = np.interp(r,exdata[:,0],exdata[:,1])
    filterintp = np.interp(r,exfilter[:,0],exfilter[:,1])
    
    # do the filtering via simple matrix mutiplication
    res = dataintp * filterintp # new y-data

    area_data = integrate.trapz(dataintp[:])
    area_result = integrate.trapz(res[:])

    return area_data, area_result, res, r, dataintp, filterintp
    
def calc_raman_water(wl):
    # calculation for Raman lines for water
    raman_water = np.zeros( (wl.shape[0], 4))
    raman_water[:,0] = wl
    for i in range (0,wl.shape[0],1):
        raman1_water = 1.0 /(1.0/wl[i]-1595/1E7)
        raman2_water = 1.0 /(1.0/wl[i]-3652/1E7)
        raman3_water = 1.0 /(1.0/wl[i]-3756/1E7)
        raman_water[i,1]  = raman1_water
        raman_water[i,2]  = raman2_water
        raman_water[i,3]  = raman3_water
        
    return raman_water

def calc_raman_glas(wl):
    # calculation for Raman lines for glas
    raman_glas = np.zeros( (wl.shape[0], 4))
    raman_glas[:,0] = wl
    glas_raman_wn = 1200.0 # wave number for raman glas spectrum
    glas_raman_wl = 1000 * 1/(glas_raman_wn/10000) # cooresponding wavelength [nm]
    for i in range (0,wl.shape[0],1):
        raman1_glas = 1.0 /(1.0/wl[i]-glas_raman_wn/1E7)
        raman2_glas = 1.0 /(1.0/wl[i]+glas_raman_wn/1E7)
        raman_glas[i,1]  = raman1_glas
        raman_glas[i,2]  = raman2_glas
        
    return raman_glas

