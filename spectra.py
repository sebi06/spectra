#!/usr/bin/env python

# Author: Sebastian Rhode
# Email:  sebrhode at googlemail.com
# Created: 2009-11-03
# Version: 2.6 - 2012-01-24
#
# Feel free to improve it!

import wx
import os
import numpy as np
import wx.grid
import filtertools as ft
import time

# Matplotlib Figure object
from matplotlib.figure import Figure
# import the WxAgg FigureCanvas object, that binds Figure to
# WxAgg backend --> a wxPanel
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
# import the NavigationToolbar WxAgg widget
from matplotlib.backends.backend_wx import NavigationToolbar2Wx

# ------------------------------------------------------------------------------------
# global variables
# defaults for figure size
sizex = 15
sizey = 10
res = 100
# array with used laser wavelengths
wl  = np.array([405, 445, 473, 488, 491, 515, 532, 561, 594, 640])    # wavelengths of Lasers
# corresponding colors in HEX-RGB code
colors = ['#8700ff', '#5600ff', '#00baff', '#00f6ff', '#00fffc', '#00ffa0', '#00ff64', '#c1ff00', '#ff8900', '#ff001f']
# line width for displaying the laser lines
linew = 2
# size of legend
legsize = "x-small"
# title for main application window
apptitle = 'Spectra 2.6 - by Sebastian Rhode'
# -------------------------------------------------------------------------------------------------------------

# adjust the display and display the legends
def AdjustDisplay(self, idnum):
    # idnum = 1 --> graph page
    # idnum = 2 --> filter efficiency page    
    if (idnum == 1):
        self.page_graph.axes.axis([self.xmin, self.xmax, self.ymin, self.ymax])
        self.page_graph.axes.legend(loc=4)
        leg1 = self.page_graph.axes.legend(loc='lower right')
        # matplotlib.text.Text instances
        try:
            for t1 in leg1.get_texts():
                t1.set_fontsize(legsize)    # the legend text fontsize
        except:
            test=1
        self.page_graph.figure.canvas.draw()
    
    if (idnum == 2):
        self.page_filterinterp.axes.axis([self.xmin, self.xmax, self.ymin, self.ymax])
        self.page_filterinterp.axes.legend(loc=4)
        leg2 = self.page_filterinterp.axes.legend(loc='upper left')
        try:
            for t2 in leg2.get_texts():
                t2.set_fontsize(legsize)    # the legend text fontsize
        except:
            test=1
        self.page_filterinterp.figure.canvas.draw()

# defines classes for displaying data
class Page_Abs1(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
class Page_Abs2(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

class Page_Flu1(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
class Page_Flu2(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
    
class Page_Ex1(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
class Page_Ex2(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
       
class Page_Di1(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
class Page_Di2(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

class Page_Em1(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

class Page_Em2(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
    
class Page_Ls(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

class Page_Misc(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
class MplPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        wx.Panel.__init__(self, *args, **kwds)

        self.__set_properties()
        self.__do_layout()
        
        # default x/y scaling values
        self.xmin = 320
        self.xmax = 700
        self.ymin = 0
        self.ymax = 1.05
        self.xmin_limit = 200
        self.xmax_limit = 1500
        
        self.figure = Figure(figsize=(sizex, sizey), dpi=res)
        self.axes = self.figure.add_subplot(111)
        self.axes.set_xticks(np.arange(self.xmin_limit, self.xmax_limit,  50))
        self.axes.set_yticks(np.arange(self.ymin, self.ymax, 0.1));
        self.axes.axis([self.xmin, self.xmax, self.ymin, self.ymax])
        self.axes.grid(True)
        self.axes.set_xlabel('Wavelength [nm]',fontsize=14)
        self.axes.set_ylabel('Transmission [%] or Intensity [a.u.]',fontsize=14)
        self.figure.subplots_adjust(left=0.07, bottom=0.09, right=0.97, top=0.94,wspace=0.20, hspace=0.20)

        # bind the figure to the FigureCanvas, so that it will be drawn using the specific backend 
        self.canvas = FigureCanvas(self, wx.ID_ANY, self.figure)
        # create an BoxSizer, to define the layout of our window
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        # add the figure canvas
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.EXPAND)
        # instantiate the Navigation Toolbar
        self.toolbar = NavigationToolbar2Wx(self.canvas)
        # needed to support Windows systems
        self.toolbar.Realize()
        # add it to the sizer
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        # explicitly show the toolbar
        self.toolbar.Show()
        # sets the window to have the given layout sizer
        self.SetSizer(self.sizer)
        # adapt sub-widget sizes to fit the window size following sizer specification
        self.Fit()
        
    def __set_properties(self):
        # begin wxGlade: MplPanel.__set_properties
        pass
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MplPanel.__do_layout
        pass
        # end wxGlade

# dialog for calculating the spectral efficiency
class FilterEffDlg(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: FilterEffDlg.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        self.button_flu = wx.Button(self, -1, "Load Fluorescence Emission")
        self.label_flu = wx.StaticText(self, -1, "     *.flu")
        self.button_di1 = wx.Button(self, -1, "Load Dichroic Mirror 1")
        self.label_di1 = wx.StaticText(self, -1, "     *.di")
        self.button_di2 = wx.Button(self, -1, "Load Dichroic Mirror 2")
        self.label_di2 = wx.StaticText(self, -1, "     *.di")
        self.button_em = wx.Button(self, -1, "Load Emission Filter")
        self.label_em = wx.StaticText(self, -1, "     *.em")
        self.button_calceff = wx.Button(self, -1, "Calculate")
        self.hint1 = wx.StaticText(self, -1, "Use X to close the dialog after\npressing 'Calculate'\nto display the results")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnLoadFluData, self.button_flu)
        self.Bind(wx.EVT_BUTTON, self.OnLoadDiData1, self.button_di1)
        self.Bind(wx.EVT_BUTTON, self.OnLoadDiData2, self.button_di2)
        self.Bind(wx.EVT_BUTTON, self.OnLoadEmData, self.button_em)
        self.Bind(wx.EVT_BUTTON, self.OnCalcEff, self.button_calceff)
        # end wxGlade

        self.flu_loaded = False
        self.di1_loaded = False
        self.di2_loaded = False
        self.em_loaded = False         
        self.calcdone = False

    def __set_properties(self):
        # begin wxGlade: FilterEffDlg.__set_properties
        self.SetTitle("Calculate Filter Efficiency")
        self.SetSize((350, 140))
        self.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        
        self.label_flu.SetBackgroundColour(wx.Colour(255, 255, 255))
        
        self.button_di1.SetBackgroundColour(wx.Colour(0, 255, 0))
        self.label_di1.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.button_di1.Enable(False)
        
        self.button_di2.SetBackgroundColour(wx.Colour(0, 255, 0))
        self.button_di2.Enable(False)
        self.label_di2.SetBackgroundColour(wx.Colour(255, 255, 255))
        
        self.button_em.SetBackgroundColour(wx.Colour(255, 0, 0))
        self.label_em.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.button_em.Enable(False)        
        
        self.button_calceff.SetBackgroundColour(wx.Colour(159, 159, 95))
        
        self.hint1.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: FilterEffDlg.__do_layout
        grid_sizer_1 = wx.FlexGridSizer(4, 2, 0, 0)
        grid_sizer_1.Add(self.button_flu, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_flu, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.button_di1, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_di1, 0,  wx.EXPAND, 0)
        grid_sizer_1.Add(self.button_di2, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_di2, 0,  wx.EXPAND, 0)
        grid_sizer_1.Add(self.button_em, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_em, 0,  wx.EXPAND, 0)
        grid_sizer_1.Add(self.button_calceff, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        grid_sizer_1.Add(self.hint1, 0, wx.EXPAND, 0)
        self.SetSizer(grid_sizer_1)
        grid_sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

    # load Data for filter efficiency calculation
    def OnLoadFluData(self, event): # wxGlade: FilterEffDialog.<event_handler>
        [self.flu, self.flutitle, self.flupath] = ft.LoadFilter('Load Fluorescence Spectra','*.flu', 'dye') # load spectral data
        self.flu = ft.normspec(self.flu)
        self.label_flu.SetLabel(self.flutitle)
        self.flu_loaded = True
        self.button_di1.Enable(True)

    def OnLoadDiData1(self, event): # wxGlade: FilterEffDialog.<event_handler>
        [self.filter1, self.filtertitle1, self.filterpath1] = ft.LoadFilter('Load Dichroic 1','*.di', 'filter')
        self.filter1 = ft.normspec_filter(self.filter1)
        self.label_di1.SetLabel(self.filtertitle1)
        self.di1_loaded = True
        self.button_di2.Enable(True)
        self.button_em.Enable(True)
    
    def OnLoadDiData2(self, event): # wxGlade: FilterEffDialog.<event_handler>
        [self.filter2, self.filtertitle2, self.filterpath2] = ft.LoadFilter('Load Dichroic 2','*.di', 'filter')
        self.filter2 = ft.normspec_filter(self.filter2)
        self.label_di2.SetLabel(self.filtertitle2)
        self.di2_loaded = True

    def OnLoadEmData(self, event): # wxGlade: FilterEffDialog.<event_handler>
        [self.filter3, self.filtertitle3, self.filterpath3] = ft.LoadFilter('Load Emission Filter Data','*.em', filter)
        self.filter3 = ft.normspec_filter(self.filter3)
        self.label_em.SetLabel(self.filtertitle3)
        self.em_loaded = True

    def OnCalcEff(self, event): # wxGlade: FilterEffDialog.<event_handler>
        
        if((self.flu_loaded and (self.di1_loaded or self.di2_loaded) and self.em_loaded) == True):        
        
            self.button_calceff.SetLabel('Done !!!')
            time.sleep(1)
            self.button_calceff.SetLabel('Calculate')
            
            # a1_1 = area of data
            # a2_1 = area of data after filtering
            # self.result = resulting y-data after filtering --> intensity values
            # self.rewave = resulting x-data after filtering --> wavelength values
            
            # apply filter number 1            
            [a1_1, a2_1, self.result1, self.reswave1, fintp1, eintp1] = ft.calcfilter(self.flu,self.filter1)
            # create new XY-data 1 --> wavelength [nm] - intensity [a.u.]            
            self.output_spec1 = np.column_stack((self.reswave1,self.result1)) # create matrix [wavelength,transmission]
            
            # apply 2nd filer only if something was loaded
            if (self.di2_loaded == True):            
              
                [a1_2, a2_2, self.result2, self.reswave2, fintp2, eintp2] = ft.calcfilter(self.output_spec1,self.filter2) 
                # create new XY-data 2 --> wavelength [nm] - intensity [a.u.]            
                self.output_spec2 = np.column_stack((self.reswave2,self.result2)) # create matrix [wavelength,transmission]
            
            # if nothing was loaded for dichroic 2--> results from first dichroic and continue
            elif(self.di2_loaded == False):
                self.output_spec2 = self.output_spec1
                
            
            # apply filter number 3   
            [a1_3, a2_3, self.result3, self.reswave3, fintp3, eintp3] = ft.calcfilter(self.output_spec2,self.filter3) 
            
            # calc efficiency of dichroic 1
            self.df1 = a2_1/a1_1
            
            # calc efficiency of dichroic 2            
            if (self.di2_loaded == True):           
                self.df2 = a2_2/a1_2 # efficiency of filter 2
            elif (self.di2_loaded == False):
                self.df2 = 1.0

            
            self.df3 = a2_3/a1_3 # efficiency of filter 3
            # resulting overall efficiency after filter 1 & 2
            #self.df_all = (a2_1/a1_1) * (a2_2/a1_2)
            #self.df_all = self.df1 * self.df2
            
            
            self.df_all = self.df1 * self.df2 * self.df3
            self.calcdone = True
        
        else:
            dial = wx.MessageDialog(None, 'Spectral Data are not complete !',
                                    'Efficiency calculation not possible', wx.OK | wx.ICON_ERROR)           
            dial.ShowModal()
        
# end of class FilterEffDialog

class MplFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds['style'] = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.MAXIMIZE|wx.MAXIMIZE_BOX|wx.SYSTEM_MENU|wx.RESIZE_BORDER|wx.FULL_REPAINT_ON_RESIZE|wx.CLIP_CHILDREN
        wx.Frame.__init__(self, *args, **kwds)

        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        self.nb = wx.Notebook(p)
        
        # create the page windows as children of the notebook
        self.page_graph = MplPanel(self.nb)
        self.page_abs1 = Page_Abs1(self.nb)
        self.page_abs2 = Page_Abs2(self.nb)
        self.page_flu1 = Page_Flu1(self.nb)
        self.page_flu2 = Page_Flu2(self.nb)
        self.page_ex1 = Page_Ex1(self.nb)      
        self.page_ex2 = Page_Ex2(self.nb)
        self.page_di1 = Page_Di1(self.nb)
        self.page_di2 = Page_Di2(self.nb)
        self.page_em1 = Page_Em1(self.nb)
        self.page_em2 = Page_Em2(self.nb)
        self.page_ls = Page_Ls(self.nb)
        self.page_misc = Page_Misc(self.nb)
        self.page_filterinterp = MplPanel(self.nb)

        # add the pages to the notebook with the label to show on the tab
        self.nb.AddPage(self.page_graph, 'Graph')
        self.nb.AddPage(self.page_abs1, 'Abs 1')
        self.nb.AddPage(self.page_abs2, 'Abs 2')
        self.nb.AddPage(self.page_flu1, 'Flu 1')
        self.nb.AddPage(self.page_flu2, 'Flu 2')
        self.nb.AddPage(self.page_ex1, 'Ex 1')
        self.nb.AddPage(self.page_ex2, 'Ex 2')
        self.nb.AddPage(self.page_di1, 'Di 1')
        self.nb.AddPage(self.page_di2, 'Di 2')
        self.nb.AddPage(self.page_em1, 'Em 1')
        self.nb.AddPage(self.page_em2, 'Em 2')
        self.nb.AddPage(self.page_ls, 'Ls')
        self.nb.AddPage(self.page_misc, 'Misc')
        self.nb.AddPage(self.page_filterinterp, 'Efficiency Graph')
        self.createMenuBar()
        self.MplFrame_statusbar = self.CreateStatusBar(1, 0)

        self.__set_properties()
        self.__do_layout()
        
        # toggle visibility of laser lines within the legend
        self.laseronoff = False
        self.ramanonoff = False
        
        # calculate the raman lines for glas & water
        self.raman_water = ft.calc_raman_water(wl)
        self.raman_glas = ft.calc_raman_glas(wl)
        
        # default x/y scaling values
        self.xmin = 320
        self.xmax = 700
        self.ymin = 0
        self.ymax = 1.05
        self.xmin_limit = 200
        self.xmax_limit = 1500
        self.bp_center_last = 500
        self.bp_width_last = 30
        
    def menuData(self):
        return (('File',
#                    ('Save Graph As...', '', self.OnSaveAs, wx.ITEM_NORMAL, True),
#                    ('Save Efficieny Graph As...', '', self.OnSaveAsEff, wx.ITEM_NORMAL, True),
#                    ('', '', '', '', ''), # separator
                    ('Set Working Directory', '', self.OnSetDir, wx.ITEM_NORMAL, True),
                    ('', '', '', '', ''), # separator
                    ('Quit', '', self.OnQuit, wx.ITEM_NORMAL,  True)),
                ('Dyes', 
                    ('Load Dye Absorption 1', '', self.OnLoadAbs1, wx.ITEM_NORMAL,  True),
                    ('Load Dye Emission 1', '', self.OnLoadFlu1, wx.ITEM_NORMAL,  True),
                    ('', '', '', '', ''),
                    ('Delete Absorption 1', '', self.OnDelAbs1, wx.ITEM_NORMAL,  False),
                    ('Delete Emission 1', '', self.OnDelFlu1, wx.ITEM_NORMAL,  False),
                    ('', '', '', '', ''),
                    ('', '', '', '', ''),
                    ('Load Dye Absorption 2', '', self.OnLoadAbs2, wx.ITEM_NORMAL,  True),
                    ('Load Dye Emission 2', '', self.OnLoadFlu2, wx.ITEM_NORMAL,  True),
                    ('', '', '', '',  ''),
                    ('Delete Absorption 2', '', self.OnDelAbs2, wx.ITEM_NORMAL,  False),
                    ('Delete Emission 2', '', self.OnDelFlu2, wx.ITEM_NORMAL,  False)),
                ('Filter', 
                    ('Load Excitation Filter 1', '', self.OnLoadEx1, wx.ITEM_NORMAL,  True),
                    ('Load Dichroic Mirror 1', '', self.OnLoadDi1, wx.ITEM_NORMAL,  True),
                    ('Load Emission Filter 1', '', self.OnLoadEm1, wx.ITEM_NORMAL,  True),
                    ('', '', '', '', ''),
                    ('Delete Excitation Filter 1', '', self.OnDelEx1, wx.ITEM_NORMAL,  False),
                    ('Delete Dichroic Mirror 1', '', self.OnDelDi1, wx.ITEM_NORMAL,  False),
                    ('Delete Emission Filter 1', '', self.OnDelEm1, wx.ITEM_NORMAL,  False),
                    ('', '', '', '', ''),
                    ('', '', '', '', ''), 
                    ('Load Excitation Filter 2', '', self.OnLoadEx2, wx.ITEM_NORMAL,  True),
                    ('Load Dichroic Mirror 2', '', self.OnLoadDi2, wx.ITEM_NORMAL,  True),
                    ('Load Emission Filter 2', '', self.OnLoadEm2, wx.ITEM_NORMAL,  True),
                    ('', '', '', '', ''),
                    ('Delete Excitation Filter 2', '', self.OnDelEx2, wx.ITEM_NORMAL,  False),
                    ('Delete Dichroic Mirror 2', '', self.OnDelDi2, wx.ITEM_NORMAL,  False),
                    ('Delete Emission Filter 2', '', self.OnDelEm2, wx.ITEM_NORMAL,  False),
                    ('', '', '', '', ''),
                    ('Show/Hide Bandpass Filter', '', self.OnEnterBand, wx.ITEM_CHECK,  True)),
                ('Light Source', 
                    ('Load Light Source', '', self.OnLoadLs, wx.ITEM_NORMAL,  True),
                    ('', '', '', '', ''),
                    ('Delete Light Source', '', self.OnDelLs, wx.ITEM_NORMAL,  False)),
                ('Misc. Spectra', 
                    ('Load miscellaneous Spectra', '', self.OnLoadMisc, wx.ITEM_NORMAL,  True),
                    ('', '', '', '', ''),
                    ('Delete miscellaneous Spectra', '', self.OnDelMisc, wx.ITEM_NORMAL,  False)),
                ('Fura Excitation',
                    ('Fura 340nm', '', self.OnShowFura340, wx.ITEM_CHECK,  True),
                    ('Fura 380nm', '', self.OnShowFura380, wx.ITEM_CHECK,  True)),
                ('Laser Lines',
                    ('405nm', '', self.OnShow405, wx.ITEM_CHECK,  True),
                    ('445nm', '', self.OnShow445, wx.ITEM_CHECK,  True),
                    ('473nm', '', self.OnShow473, wx.ITEM_CHECK,  True),
                    ('488nm', '', self.OnShow488, wx.ITEM_CHECK,  True),
                    ('491nm', '', self.OnShow491, wx.ITEM_CHECK,  True),
                    ('515nm', '', self.OnShow515, wx.ITEM_CHECK,  True),
                    ('532nm', '', self.OnShow532, wx.ITEM_CHECK,  True),
                    ('561nm', '', self.OnShow561, wx.ITEM_CHECK,  True),
                    ('594nm', '', self.OnShow594, wx.ITEM_CHECK,  True),
                    ('640nm', '', self.OnShow640, wx.ITEM_CHECK,  True),
                    ('', '', '', '', ''),
                    ('Custom Laser', '', self.OnShowCustomLaser, wx.ITEM_CHECK,  True),
                    ('', '', '', '', ''),
                    ('Show Laser Lines in Legend', '', self.OnShowLaserLines, wx.ITEM_CHECK,  True)),
                ('Raman Lines',
                    ('Raman 405nm', '', self.OnShowRaman405, wx.ITEM_CHECK,  True),
                    ('Raman 445nm', '', self.OnShowRaman445, wx.ITEM_CHECK,  True),
                    ('Raman 473nm', '', self.OnShowRaman473, wx.ITEM_CHECK,  True),
                    ('Raman 488nm', '', self.OnShowRaman488, wx.ITEM_CHECK,  True),
                    ('Raman 491nm', '', self.OnShowRaman491, wx.ITEM_CHECK,  True),
                    ('Raman 515nm', '', self.OnShowRaman515, wx.ITEM_CHECK,  True),
                    ('Raman 532nm', '', self.OnShowRaman532, wx.ITEM_CHECK,  True),
                    ('Raman 561nm', '', self.OnShowRaman561, wx.ITEM_CHECK,  True),
                    ('Raman 594nm', '', self.OnShowRaman594, wx.ITEM_CHECK,  True),
                    ('Raman 640nm', '', self.OnShowRaman640, wx.ITEM_CHECK,  True),
                    ('', '', '', '', ''),
                    ('Custom Raman Laser', '', self.OnShowCustomRaman, wx.ITEM_CHECK,  True),
                    ('', '', '', '', ''),
                    ('Show Raman Lines in Legend', '', self.OnShowRamanLines, wx.ITEM_CHECK,  True)), 
                ('Filter Efficiency', 
                    ('Simulate Filter Efficiency', '',  self.OnInterpolateFilter,  wx.ITEM_NORMAL,  True), 
                    ('', '', '', '', ''),
                    ('Delete Efficiency Simulation', '',  self.OnDelInterpolation,  wx.ITEM_NORMAL,  False)),  
                ('Scaling Options', 
                    ('Set X-Min Value', '',  self.OnSetXMin,  wx.ITEM_NORMAL,  True),
                    ('Set X-Max Value', '',  self.OnSetXMax,  wx.ITEM_NORMAL,  True)),
                ('Legend Size', 
                    ('X-Small', '',  self.OnSetLegendSize,  wx.ITEM_RADIO,  True),
                    ('Small', '',  self.OnSetLegendSize,  wx.ITEM_RADIO,  True),
                    ('Medium', '',  self.OnSetLegendSize,  wx.ITEM_RADIO,  True))) 

    def createMenuBar(self):
        menuBar = wx.MenuBar()
        for eachMenuData in self.menuData():
            menuLabel = eachMenuData[0]
            menuItems = eachMenuData[1:]
            menuBar.Append(self.createMenu(menuItems), menuLabel)
        self.SetMenuBar(menuBar)

    def createMenu(self, menuData):
        menu = wx.Menu()
        for eachLabel, eachStatus, eachHandler,  eachKind,  eachEnable in menuData:
            if not eachLabel:
                menu.AppendSeparator()
                continue
            menuItem = menu.Append(-1, eachLabel, eachStatus,  eachKind)
            menuItem.Enable(eachEnable)
            self.Bind(wx.EVT_MENU, eachHandler, menuItem)
        return menu

    def __set_properties(self):
        self.SetTitle(apptitle)
        self.SetSize((sizex*res, sizey*res))
        self.MplFrame_statusbar.SetStatusWidths([-1])
        # statusbar fields
        MplFrame_statusbar_fields = ['MplFrame_statusbar']
        for i in range(len(MplFrame_statusbar_fields)):
            self.MplFrame_statusbar.SetStatusText(MplFrame_statusbar_fields[i], i)

    def __do_layout(self):
        mplsizer1 = wx.BoxSizer(wx.VERTICAL)
        mplsizer1.Add(self.nb, 1, wx.ALL|wx.EXPAND, 0)
        self.SetSizer(mplsizer1)
        self.Layout()

    def ToggleItem(self, event,  IDjump):
        item1 = self.GetMenuBar().FindItemById(event.GetId()) # get the corresponding item
        item2 = self.GetMenuBar().FindItemById(event.GetId() + IDjump) # get the cooresponding item to switch Enalbled status
        enabled1 = item1.IsEnabled()
        enabled2 = item2.IsEnabled()
        item1.Enable(not enabled1) # toggle status
        item2.Enable(not enabled2) # toggle status

    def ShowSpectralData(self,  event, dat, kind,  fc):
        colLabels = ['Wavelength',  'Trans / Int']
        sizex = 300
        sizey = 580
        
        if (kind == 'abs1'):
            grid = wx.grid.Grid(self.page_abs1, size = (sizex, sizey))
        elif (kind == 'abs2'):
            grid = wx.grid.Grid(self.page_abs2, size = (sizex, sizey))
        elif (kind == 'flu1'):
            grid = wx.grid.Grid(self.page_flu1, size = (sizex, sizey))
        elif (kind == 'flu2'):
            grid = wx.grid.Grid(self.page_flu2, size = (sizex, sizey))
        elif (kind == 'ex1'):
            grid = wx.grid.Grid(self.page_ex1, size = (sizex, sizey))
        elif (kind == 'ex2'):
            grid = wx.grid.Grid(self.page_ex2, size = (sizex, sizey))
        elif (kind == 'di1'):
            grid = wx.grid.Grid(self.page_di1, size = (sizex, sizey))
        elif (kind == 'di2'):
            grid = wx.grid.Grid(self.page_di2, size = (sizex, sizey))
        elif (kind== 'em1'):
            grid = wx.grid.Grid(self.page_em1, size = (sizex, sizey))
        elif (kind== 'em2'):
            grid = wx.grid.Grid(self.page_em2, size = (sizex, sizey))
        elif (kind == 'ls'):
            grid = wx.grid.Grid(self.page_ls, size = (sizex, sizey))
        elif (kind == 'misc'):
            grid = wx.grid.Grid(self.page_misc, size = (sizex, sizey))
            colLabels = ['X [a.u.]',  'Y [a.u.]']
        
        grid.CreateGrid(dat.shape[0],dat.shape[1])
        grid.SelectAll()
        grid.ClearSelection()
        for row in range(dat.shape[0]):
            for col in range(dat.shape[1]):
                grid.SetCellValue(row, col, str(dat[row,col]))
                grid.SetCellTextColour(row,  col, fc)
        for col in range(dat.shape[1]):
            grid.SetColLabelValue(col,  colLabels[col])

    def OnSaveAs(self, event):
        dlg = wx.FileDialog(self, 'Choose a Filename', os.getcwd(), '', '*.png*',
            wx.SAVE | wx.OVERWRITE_PROMPT)

        if dlg.ShowModal() == wx.ID_OK:
            savename = dlg.GetPath()
            self.page_graph.figure.savefig(savename)
        
        dlg.Destroy()
        
    def OnSaveAsEff(self, event):
        dlg = wx.FileDialog(self, 'Choose a Filename', os.getcwd(), '', '*.png*',
            wx.SAVE | wx.OVERWRITE_PROMPT)

        if dlg.ShowModal() == wx.ID_OK:
            savename = dlg.GetPath()
            self.page_filterinterp.figure.savefig(savename)
        
        dlg.Destroy()
        
    def OnSetDir(self, event):
        dlg = wx.DirDialog(self, 'Choose a working directory:',
           style = wx.wx.DD_DIR_MUST_EXIST)
        
        if dlg.ShowModal() == wx.ID_OK:
            workingdir = dlg.GetPath()
            os.chdir(workingdir)
            self.SetStatusText('Selected default directory: %s' % workingdir)
        
        dlg.Destroy()

    def OnQuit(self, event):
        self.Close(True)

    def OnLoadAbs1(self, event):
        [abs1, mypathabs1, pathabs1] = ft.LoadFilter('Choose Dye Absorption Spectra','*.abs', 'dye') # load spectral data
        self.SetStatusText('Selected Absorption Spectra: %s' % mypathabs1)              
        self.gabs1, = self.page_graph.axes.plot(abs1[:,0],abs1[:,1],'k-', lw=2,label = mypathabs1 +' (1)')        
        self.gabs1c = self.page_graph.axes.fill_between(abs1[:,0],abs1[:,1],abs1[:,1]*0, facecolor='blue', alpha = 0.3)
        AdjustDisplay(self,1)
        self.ToggleItem(event, 2)
        fc = 'black'
        kind = 'abs1'
        self.ShowSpectralData(event, abs1, kind,  fc)
        
    def OnLoadAbs2(self, event):
        [abs2, mypathabs2, pathabs2] = ft.LoadFilter('Choose Dye Absorption Spectra','*.abs', 'dye') # load spectral data
        self.SetStatusText('Selected Absorption Spectra: %s' % mypathabs2)
        self.gabs2, = self.page_graph.axes.plot(abs2[:,0],abs2[:,1],'k-.', lw=2,label = mypathabs2 +' (2)')
        self.gabs2c = self.page_graph.axes.fill_between(abs2[:,0],abs2[:,1],abs2[:,1]*0, facecolor='blue', alpha = 0.3)        
        AdjustDisplay(self,1)
        self.ToggleItem(event, 2)
        fc = 'black'
        kind = 'abs2'
        self.ShowSpectralData(event, abs2, kind,  fc)

    def OnLoadFlu1(self, event):
        [flu1, mypathflu1, pathflu1] = ft.LoadFilter('Choose Dye Emission Spectra','*.flu', 'dye') # load spectral data
        self.SetStatusText('Selected Fluorescence Spectra: %s' % mypathflu1)
        self.gflu1, = self.page_graph.axes.plot(flu1[:,0],flu1[:,1],'k--', lw=2,label = mypathflu1 +' (1)')
        self.gflu1c = self.page_graph.axes.fill_between(flu1[:,0],flu1[:,1],flu1[:,1]*0, facecolor='red', alpha = 0.3)        
        AdjustDisplay(self,1)
        self.ToggleItem(event, 2)
        fc = 'black'
        kind = 'flu1'
        self.ShowSpectralData(event, flu1,  kind, fc)
        
    def OnLoadFlu2(self, event):
        [flu2, mypathflu2, pathflu2] = ft.LoadFilter('Choose Dye Emission Spectra','*.flu', 'dye') # load spectral data
        self.SetStatusText('Selected Fluorescence Spectra: %s' % mypathflu2)
        self.gflu2, = self.page_graph.axes.plot(flu2[:,0],flu2[:,1],'k:', lw=2,label = mypathflu2 +' (2)')
        self.gflu2c = self.page_graph.axes.fill_between(flu2[:,0],flu2[:,1],flu2[:,1]*0, facecolor='red', alpha = 0.3)             
        AdjustDisplay(self,1)
        self.ToggleItem(event, 2)
        fc = 'black'
        kind = 'flu2'
        self.ShowSpectralData(event, flu2,  kind, fc)

    def OnDelAbs1(self, event):
        self.gabs1.remove()
        self.gabs1c.remove()
        self.page_graph.axes.legend_= None
        AdjustDisplay(self,1)
        self.ToggleItem(event, -2)
        fc = 'black'
        kind = 'abs1'
        self.ShowSpectralData(event, np.zeros([1,1]), kind, fc) # delete grid table
            
    def OnDelAbs2(self, event):
        self.gabs2.remove()
        self.gabs2c.remove()
        self.page_graph.axes.legend_= None
        AdjustDisplay(self,1)
        self.ToggleItem(event, -2)
        fc = 'black'
        kind = 'abs2'
        self.ShowSpectralData(event, np.zeros([1,1]), kind, fc) # delete grid table
        
    def OnDelFlu1(self, event):
        self.gflu1.remove()
        self.gflu1c.remove()
        self.page_graph.axes.legend_= None
        AdjustDisplay(self,1)
        self.ToggleItem(event, -2)
        fc = 'black'
        kind = 'flu1'
        self.ShowSpectralData(event, np.zeros([1,1]), kind, fc)
            
    def OnDelFlu2(self, event):
        self.gflu2.remove()
        self.gflu2c.remove()
        self.page_graph.axes.legend_= None
        AdjustDisplay(self,1)
        self.ToggleItem(event, -2)
        fc = 'black'
        kind = 'flu2'
        self.ShowSpectralData(event, np.zeros([1,1]), kind, fc)

    def OnLoadEx1(self, event):
        [ex1, mypathex1, pathex1] = ft.LoadFilter('Choose an Excitation Filter','*.ex', 'filter') # load spectral data
        self.SetStatusText('Selected Excitation Filter: %s' % mypathex1)
        self.gex1, = self.page_graph.axes.plot(ex1[:,0],ex1[:,1],'b-', lw=2,label = mypathex1 +' (1)')
        AdjustDisplay(self,1)
        self.ToggleItem(event, 3) # 3 --> add to ID of current menu entry to get ID for OnDelEx
        fc = 'blue'
        kind = 'ex1'
        self.ShowSpectralData(event, ex1, kind, fc)
    
    def OnLoadEx2(self, event):
        [ex2, mypathex2, pathex2] = ft.LoadFilter('Choose an Excitation Filter','*.ex', 'filter') # load spectral data
        self.SetStatusText('Selected Excitation Filter: %s' % mypathex2)
        self.gex2, = self.page_graph.axes.plot(ex2[:,0],ex2[:,1],'b--', lw=2,label = mypathex2 +' (2)')
        AdjustDisplay(self,1)
        self.ToggleItem(event, 3) # 3 --> add to ID of current menu entry to get ID for OnDelEx
        fc = 'blue'
        kind = 'ex2'
        self.ShowSpectralData(event, ex2,  kind, fc)

    def OnLoadDi1(self, event):
        [di1, mypathdi1, pathdi1] = ft.LoadFilter('Choose a Dichroic Mirror','*.di', 'filter') # load spectral data
        self.SetStatusText('Selected Dichroic Mirror: %s' % mypathdi1)
        self.gdi1, = self.page_graph.axes.plot(di1[:,0],di1[:,1],'g-', lw=2,label = mypathdi1 +' (1)')
        AdjustDisplay(self,1)
        self.ToggleItem(event, 3)
        fc = 'green'
        kind = 'di1'
        self.ShowSpectralData(event, di1,  kind, fc)
        
    def OnLoadDi2(self, event):
        [di2, mypathdi2, pathdi2] = ft.LoadFilter('Choose a Dichroic Mirror','*.di', 'filter') # load spectral data
        self.SetStatusText('Selected Dichroic Mirror: %s' % mypathdi2)
        self.gdi2, = self.page_graph.axes.plot(di2[:,0],di2[:,1],'g--', lw=2,label = mypathdi2 +' (2)')
        AdjustDisplay(self,1)
        self.ToggleItem(event, 3)
        fc = 'green'
        kind = 'di2'
        self.ShowSpectralData(event, di2,  kind, fc)

    def OnLoadEm1(self, event):
        [em1, mypathem1, pathem1] = ft.LoadFilter('Choose an Emission Filter','*.em', 'filter') # load spectral data
        self.SetStatusText('Selected Emission Filter: %s' % mypathem1)
        self.gem1, = self.page_graph.axes.plot(em1[:,0],em1[:,1],'r-', lw=2,label = mypathem1 +' (1)')
        AdjustDisplay(self,1)
        self.ToggleItem(event, 3)
        fc = 'red'
        kind = 'em1'
        self.ShowSpectralData(event, em1,  kind, fc)
        
    def OnLoadEm2(self, event):
        [em2, mypathem2, pathem2] = ft.LoadFilter('Choose an Emission Filter','*.em', 'filter') # load spectral data
        self.SetStatusText('Selected Emission Filter: %s' % mypathem2)
        self.gem2, = self.page_graph.axes.plot(em2[:,0],em2[:,1],'r--', lw=2,label = mypathem2 +' (2)')
        AdjustDisplay(self,1)
        self.ToggleItem(event, 3)
        fc = 'red'
        kind = 'em2'
        self.ShowSpectralData(event, em2,  kind, fc)

    def OnDelEx1(self, event):
        self.gex1.remove()
        self.page_graph.axes.legend_= None
        AdjustDisplay(self,1)
        self.ToggleItem(event, -3) # -3 --> add to ID of current menu entry to get ID for OnLoadEx
        fc = 'blue'
        kind = 'ex1'
        self.ShowSpectralData(event, np.zeros([1,1]), kind, fc) 
            
    def OnDelEx2(self, event):
        self.gex2.remove()
        self.page_graph.axes.legend_= None
        AdjustDisplay(self,1)
        self.ToggleItem(event, -3) # -3 --> add to ID of current menu entry to get ID for OnLoadEx
        fc = 'blue'
        kind = 'ex2'
        self.ShowSpectralData(event, np.zeros([1,1]), kind, fc) 
            
    def OnDelDi1(self, event):
        self.gdi1.remove()
        self.page_graph.axes.legend_= None
        AdjustDisplay(self,1)
        self.ToggleItem(event, -3)
        fc = 'green'
        kind = 'di1'
        self.ShowSpectralData(event, np.zeros([1,1]), kind, fc)
            
    def OnDelDi2(self, event):
        self.gdi2.remove()
        self.page_graph.axes.legend_= None
        AdjustDisplay(self,1)
        self.ToggleItem(event, -3)
        fc = 'green'
        kind = 'di2'
        self.ShowSpectralData(event, np.zeros([1,1]), kind, fc)
        
    def OnDelEm1(self, event):
        self.gem1.remove()
        self.page_graph.axes.legend_= None
        AdjustDisplay(self,1)
        self.ToggleItem(event, -3)
        fc = 'red'
        kind = 'em1'
        self.ShowSpectralData(event, np.zeros([1,1]), kind, fc)
            
    def OnDelEm2(self, event):
        self.gem2.remove()
        self.page_graph.axes.legend_= None
        AdjustDisplay(self,1)
        self.ToggleItem(event, -3)
        fc = 'red'
        kind = 'em2'
        self.ShowSpectralData(event, np.zeros([1,1]), kind, fc)

    def OnLoadLs(self, event):
        [ls, mypathls, pathls] = ft.LoadFilter('Choose a Light Source Spectrum','*.ls', 'dye') # load spectral data
        self.SetStatusText('Selected Light Source: %s' % mypathls)
        self.gls, = self.page_graph.axes.plot(ls[:,0],ls[:,1],'m', lw=2,label = mypathls)
        AdjustDisplay(self,1)
        self.ToggleItem(event, 1)
        fc = 'magenta'
        kind = 'ls'
        self.ShowSpectralData(event,  pathls,  ls,  kind, fc)
         
    def OnDelLs(self, event):
        self.gls.remove()
        self.page_graph.axes.legend_= None
        AdjustDisplay(self,1)
        self.ToggleItem(event, -1)
        fc = 'mangenta'
        kind = 'ls'
        self.ShowSpectralData(event, np.zeros([1,1]), kind, fc)
            
    def OnLoadMisc(self, event):
        [misc, mypathmisc, pathmisc] = ft.LoadFilter('Choose a misc spectra','*.*', 'misc') # load spectral data
        self.SetStatusText('Selected Spectra: %s' % mypathmisc)
        fend = mypathmisc[-2:]
        if (fend == ('ex' or 'di' or 'em')):
            misc = ft.normspec_filter(misc)
        else:
            misc = ft.normspec(misc)
        self.gmisc, = self.page_graph.axes.plot(misc[:,0],misc[:,1],'m', lw=2,label = mypathmisc)
        AdjustDisplay(self,1)
        self.ToggleItem(event, 1)
        fc = 'k-.'
        kind = 'misc'
        self.ShowSpectralData(event, misc,  kind, fc)
         
    def OnDelMisc(self, event):
        self.gmisc.remove()
        self.page_graph.axes.legend_= None
        AdjustDisplay(self,1)
        self.ToggleItem(event, -1)
        fc = 'k-.'
        kind = 'misc'
        self.ShowSpectralData(event, np.zeros([1,1]), kind, fc)
        self.page_graph.figure.canvas.draw()

    def OnShow405(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        lnum = 0
        if item.IsChecked() == True:
            if self.laseronoff == True:
                self.laser405, = self.page_graph.axes.plot([wl[lnum],wl[lnum]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew, label=str(wl[lnum])+'nm')
            elif self.laseronoff == False:
                self.laser405, = self.page_graph.axes.plot([wl[lnum],wl[lnum]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew)
            
            self.SetStatusText('Switched On Laser Line: %s' % str(wl[lnum])+'nm' )
        else:
            self.laser405.remove()  # delete laser line
            self.page_graph.axes.legend_= None
            
        AdjustDisplay(self,1)
        
    def OnShow445(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        lnum = 1
        if item.IsChecked() == True:
            if self.laseronoff == True:
                self.laser445, = self.page_graph.axes.plot([wl[lnum],wl[lnum]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew, label=str(wl[lnum])+'nm')
            elif self.laseronoff == False:
                self.laser445, = self.page_graph.axes.plot([wl[lnum],wl[lnum]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew)
            
            self.SetStatusText('Switched On Laser Line: %s' % str(wl[lnum])+'nm' )
        else:
            self.laser445.remove()  # delete laser line
            self.page_graph.axes.legend_= None
            
        AdjustDisplay(self,1)
        
    def OnShow473(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        lnum = 2
        if item.IsChecked() == True:
            if self.laseronoff == True:
                self.laser473, = self.page_graph.axes.plot([wl[lnum],wl[lnum]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew, label=str(wl[lnum])+'nm')
            elif self.laseronoff == False:
                self.laser473, = self.page_graph.axes.plot([wl[lnum],wl[lnum]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew)
            
            self.SetStatusText('Switched On Laser Line: %s' % str(wl[lnum])+'nm' )
        else:
            self.laser473.remove()  # delete laser line
            self.page_graph.axes.legend_= None
            
        AdjustDisplay(self,1)
        
    def OnShow488(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        lnum = 3
        if item.IsChecked() == True:
            if self.laseronoff == True:
                self.laser488, = self.page_graph.axes.plot([wl[lnum],wl[lnum]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew, label=str(wl[lnum])+'nm')
            elif self.laseronoff == False:
                self.laser488, = self.page_graph.axes.plot([wl[lnum],wl[lnum]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew)
            
            self.SetStatusText('Switched On Laser Line: %s' % str(wl[lnum])+'nm' )
        else:
            self.laser488.remove()  # delete laser line
            self.page_graph.axes.legend_= None
            
        AdjustDisplay(self,1)
        
    def OnShow491(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        lnum = 4
        if item.IsChecked() == True:
            if self.laseronoff == True:
                self.laser491, = self.page_graph.axes.plot([wl[lnum],wl[lnum]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew, label=str(wl[lnum])+'nm')
            elif self.laseronoff == False:
                self.laser491, = self.page_graph.axes.plot([wl[lnum],wl[lnum]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew)
            
            self.SetStatusText('Switched On Laser Line: %s' % str(wl[lnum])+'nm' )
        else:
            self.laser491.remove()  # delete laser line
            self.page_graph.axes.legend_= None
           
        AdjustDisplay(self,1)
        
    def OnShow515(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        lnum = 5
        if item.IsChecked() == True:
            if self.laseronoff == True:
                self.laser515, = self.page_graph.axes.plot([wl[lnum],wl[lnum]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew, label=str(wl[lnum])+'nm')
            elif self.laseronoff == False:
                self.laser515, = self.page_graph.axes.plot([wl[lnum],wl[lnum]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew)
            
            self.SetStatusText('Switched On Laser Line: %s' % str(wl[lnum])+'nm' )
        else:
            self.laser515.remove()  # delete laser line
            self.page_graph.axes.legend_= None
            
        AdjustDisplay(self,1)
        
    def OnShow532(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        lnum = 6
        if item.IsChecked() == True:
            if self.laseronoff == True:
                self.laser532, = self.page_graph.axes.plot([wl[lnum],wl[lnum]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew, label=str(wl[lnum])+'nm')
            elif self.laseronoff == False:
                self.laser532, = self.page_graph.axes.plot([wl[lnum],wl[lnum]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew)
            
            self.SetStatusText('Switched On Laser Line: %s' % str(wl[lnum])+'nm' )
        else:
            self.laser532.remove()  # delete laser line
            self.page_graph.axes.legend_= None
            
        AdjustDisplay(self,1)
        
    def OnShow561(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        lnum = 7
        if item.IsChecked() == True:
            if self.laseronoff == True:
                self.laser561, = self.page_graph.axes.plot([wl[lnum],wl[lnum]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew, label=str(wl[lnum])+'nm')
            elif self.laseronoff == False:
                self.laser561, = self.page_graph.axes.plot([wl[lnum],wl[lnum]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew)
            
            self.SetStatusText('Switched On Laser Line: %s' % str(wl[lnum])+'nm' )
        else:
            self.laser561.remove()  # delete laser line
            self.page_graph.axes.legend_= None
            
        AdjustDisplay(self,1)
        
    def OnShow594(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        lnum = 8
        if item.IsChecked() == True:
            if self.laseronoff == True:
                self.laser594, = self.page_graph.axes.plot([wl[lnum],wl[lnum]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew, label=str(wl[lnum])+'nm')
            elif self.laseronoff == False:
                self.laser594, = self.page_graph.axes.plot([wl[lnum],wl[lnum]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew)
            
            self.SetStatusText('Switched On Laser Line: %s' % str(wl[lnum])+'nm' )
        else:
            self.laser594.remove()  # delete laser line
            self.page_graph.axes.legend_= None
            
        AdjustDisplay(self,1)
        
    def OnShow640(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        lnum = 9
        if item.IsChecked() == True:
            if self.laseronoff == True:
                self.laser640, = self.page_graph.axes.plot([wl[lnum],wl[lnum]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew, label=str(wl[lnum])+'nm')
            elif self.laseronoff == False:
                self.laser640, = self.page_graph.axes.plot([wl[lnum],wl[lnum]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew)
            
            self.SetStatusText('Switched On Laser Line: %s' % str(wl[lnum])+'nm' )
        else:
            self.laser640.remove()  # delete laser line
            self.page_graph.axes.legend_= None
            
        AdjustDisplay(self,1)
        
    def OnShowRaman405(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        lnum = 0       
        if item.IsChecked() == True:
            if self.ramanonoff == True:
                self.raman405_1, = self.page_graph.axes.plot([self.raman_water[lnum,1],self.raman_water[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--',
                        label='Raman Water '+str(wl[lnum])+'nm')
            elif self.ramanonoff == False:
                self.raman405_1, = self.page_graph.axes.plot([self.raman_water[lnum,1],self.raman_water[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            self.raman405_2, = self.page_graph.axes.plot([self.raman_water[lnum,2],self.raman_water[lnum,2]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            self.raman405_3, = self.page_graph.axes.plot([self.raman_water[lnum,3],self.raman_water[lnum,3]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            if self.ramanonoff == True:
                self.raman405_4, = self.page_graph.axes.plot([self.raman_glas[lnum,1],self.raman_glas[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.',
                        label='Raman Glass '+str(wl[lnum])+'nm')
            elif self.ramanonoff == False:
                self.raman405_4, = self.page_graph.axes.plot([self.raman_glas[lnum,1],self.raman_glas[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.')
            
            self.raman405_5, = self.page_graph.axes.plot([self.raman_glas[lnum,2],self.raman_glas[lnum,2]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.')
            
            self.SetStatusText('Switched On Raman Laser Lines: %s' % str(wl[lnum])+'nm' )
        else:
            self.raman405_1.remove()
            self.raman405_2.remove()
            self.raman405_3.remove()
            self.raman405_4.remove()
            self.raman405_5.remove()
            self.page_graph.axes.legend_= None
            
        AdjustDisplay(self,1)
                
    def OnShowRaman445(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        lnum = 1
        if item.IsChecked() == True:
            if self.ramanonoff == True:
                self.raman445_1, = self.page_graph.axes.plot([self.raman_water[lnum,1],self.raman_water[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--',
                        label='Raman Water '+str(wl[lnum])+'nm')
            elif self.ramanonoff == False:
                self.raman445_1, = self.page_graph.axes.plot([self.raman_water[lnum,1],self.raman_water[lnum,1]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            self.raman445_2, = self.page_graph.axes.plot([self.raman_water[lnum,2],self.raman_water[lnum,2]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            self.raman445_3, = self.page_graph.axes.plot([self.raman_water[lnum,3],self.raman_water[lnum,3]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            if self.ramanonoff == True:
                self.raman445_4, = self.page_graph.axes.plot([self.raman_glas[lnum,1],self.raman_glas[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.',
                        label='Raman Glass '+str(wl[lnum])+'nm')
            elif self.ramanonoff == False:
                self.raman445_4, = self.page_graph.axes.plot([self.raman_glas[lnum,1],self.raman_glas[lnum,1]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.')
            self.raman445_5, = self.page_graph.axes.plot([self.raman_glas[lnum,2],self.raman_glas[lnum,2]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.')
            self.SetStatusText('Switched On Raman Laser Lines: %s' % str(wl[lnum])+'nm' )
        else:
            self.raman445_1.remove()
            self.raman445_2.remove()
            self.raman445_3.remove()
            self.raman445_4.remove()
            self.raman445_5.remove()
            self.page_graph.axes.legend_= None
            
        AdjustDisplay(self,1)
                
    def OnShowRaman473(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        lnum = 2
        if item.IsChecked() == True:
            if self.ramanonoff == True:            
                self.raman473_1, = self.page_graph.axes.plot([self.raman_water[lnum,1],self.raman_water[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--',
                        label='Raman Water '+str(wl[lnum])+'nm')
            elif self.ramanonoff == False:
                self.raman473_1, = self.page_graph.axes.plot([self.raman_water[lnum,1],self.raman_water[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            self.raman473_2, = self.page_graph.axes.plot([self.raman_water[lnum,2],self.raman_water[lnum,2]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            self.raman473_3, = self.page_graph.axes.plot([self.raman_water[lnum,3],self.raman_water[lnum,3]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            if self.ramanonoff == True: 
                self.raman473_4, = self.page_graph.axes.plot([self.raman_glas[lnum,1],self.raman_glas[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.',
                        label='Raman Glass '+str(wl[lnum])+'nm')
            elif self.ramanonoff == False:
                self.raman473_4, = self.page_graph.axes.plot([self.raman_glas[lnum,1],self.raman_glas[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.') 
            self.raman473_5, = self.page_graph.axes.plot([self.raman_glas[lnum,2],self.raman_glas[lnum,2]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.')
            self.SetStatusText('Switched On Raman Laser Lines: %s' % str(wl[lnum])+'nm' )
        else:
            self.raman473_1.remove()
            self.raman473_2.remove()
            self.raman473_3.remove()
            self.raman473_4.remove()
            self.raman473_5.remove()
            self.page_graph.axes.legend_= None
            
        AdjustDisplay(self,1)
                
    def OnShowRaman488(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        lnum = 3
        if item.IsChecked() == True:
            if self.ramanonoff == True:            
                self.raman488_1, = self.page_graph.axes.plot([self.raman_water[lnum,1],self.raman_water[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--',
                        label='Raman Water '+str(wl[lnum])+'nm')
            elif self.ramanonoff == False:
                self.raman488_1, = self.page_graph.axes.plot([self.raman_water[lnum,1],self.raman_water[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            self.raman488_2, = self.page_graph.axes.plot([self.raman_water[lnum,2],self.raman_water[lnum,2]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            self.raman488_3, = self.page_graph.axes.plot([self.raman_water[lnum,3],self.raman_water[lnum,3]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            if self.ramanonoff == True: 
                self.raman488_4, = self.page_graph.axes.plot([self.raman_glas[lnum,1],self.raman_glas[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.',
                        label='Raman Glass '+str(wl[lnum])+'nm')
            elif self.ramanonoff == False:
                self.raman488_4, = self.page_graph.axes.plot([self.raman_glas[lnum,1],self.raman_glas[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.') 
            self.raman488_5, = self.page_graph.axes.plot([self.raman_glas[lnum,2],self.raman_glas[lnum,2]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.')
            self.SetStatusText('Switched On Raman Laser Lines: %s' % str(wl[lnum])+'nm' )
        else:
            self.raman488_1.remove()
            self.raman488_2.remove()
            self.raman488_3.remove()
            self.raman488_4.remove()
            self.raman488_5.remove()
            self.page_graph.axes.legend_= None
            
        AdjustDisplay(self,1)
                
    def OnShowRaman491(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        lnum = 4
        if item.IsChecked() == True:
            if self.ramanonoff == True:            
                self.raman491_1, = self.page_graph.axes.plot([self.raman_water[lnum,1],self.raman_water[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--',
                        label='Raman Water '+str(wl[lnum])+'nm')
            elif self.ramanonoff == False:
                self.raman491_1, = self.page_graph.axes.plot([self.raman_water[lnum,1],self.raman_water[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            self.raman491_2, = self.page_graph.axes.plot([self.raman_water[lnum,2],self.raman_water[lnum,2]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            self.raman491_3, = self.page_graph.axes.plot([self.raman_water[lnum,3],self.raman_water[lnum,3]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            if self.ramanonoff == True: 
                self.raman491_4, = self.page_graph.axes.plot([self.raman_glas[lnum,1],self.raman_glas[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.',
                        label='Raman Glass '+str(wl[lnum])+'nm')
            elif self.ramanonoff == False:
                self.raman491_4, = self.page_graph.axes.plot([self.raman_glas[lnum,1],self.raman_glas[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.') 
            self.raman491_5, = self.page_graph.axes.plot([self.raman_glas[lnum,2],self.raman_glas[lnum,2]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.')
            self.SetStatusText('Switched On Raman Laser Lines: %s' % str(wl[lnum])+'nm' )
        else:
            self.raman491_1.remove()
            self.raman491_2.remove()
            self.raman491_3.remove()
            self.raman491_4.remove()
            self.raman491_5.remove()
            self.page_graph.axes.legend_= None
            
        AdjustDisplay(self,1)
                
    def OnShowRaman515(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        lnum = 5
        if item.IsChecked() == True:
            if self.ramanonoff == True:            
                self.raman515_1, = self.page_graph.axes.plot([self.raman_water[lnum,1],self.raman_water[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--',
                        label='Raman Water '+str(wl[lnum])+'nm')
            elif self.ramanonoff == False:
                self.raman515_1, = self.page_graph.axes.plot([self.raman_water[lnum,1],self.raman_water[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            self.raman515_2, = self.page_graph.axes.plot([self.raman_water[lnum,2],self.raman_water[lnum,2]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            self.raman515_3, = self.page_graph.axes.plot([self.raman_water[lnum,3],self.raman_water[lnum,3]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            if self.ramanonoff == True: 
                self.raman515_4, = self.page_graph.axes.plot([self.raman_glas[lnum,1],self.raman_glas[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.',
                        label='Raman Glass '+str(wl[lnum])+'nm')
            elif self.ramanonoff == False:
                self.raman515_4, = self.page_graph.axes.plot([self.raman_glas[lnum,1],self.raman_glas[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.') 
            self.raman515_5, = self.page_graph.axes.plot([self.raman_glas[lnum,2],self.raman_glas[lnum,2]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.')
            self.SetStatusText('Switched On Raman Laser Lines: %s' % str(wl[lnum])+'nm' )
        else:
            self.raman515_1.remove()
            self.raman515_2.remove()
            self.raman515_3.remove()
            self.raman515_4.remove()
            self.raman515_5.remove()
            self.page_graph.axes.legend_= None

        AdjustDisplay(self,1)
                
    def OnShowRaman532(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        lnum = 6
        if item.IsChecked() == True:
            if self.ramanonoff == True:            
                self.raman532_1, = self.page_graph.axes.plot([self.raman_water[lnum,1],self.raman_water[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--',
                        label='Raman Water '+str(wl[lnum])+'nm')
            elif self.ramanonoff == False:
                self.raman532_1, = self.page_graph.axes.plot([self.raman_water[lnum,1],self.raman_water[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            self.raman532_2, = self.page_graph.axes.plot([self.raman_water[lnum,2],self.raman_water[lnum,2]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            self.raman532_3, = self.page_graph.axes.plot([self.raman_water[lnum,3],self.raman_water[lnum,3]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            if self.ramanonoff == True: 
                self.raman532_4, = self.page_graph.axes.plot([self.raman_glas[lnum,1],self.raman_glas[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.',
                        label='Raman Glass '+str(wl[lnum])+'nm')
            elif self.ramanonoff == False:
                self.raman532_4, = self.page_graph.axes.plot([self.raman_glas[lnum,1],self.raman_glas[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.') 
            self.raman532_5, = self.page_graph.axes.plot([self.raman_glas[lnum,2],self.raman_glas[lnum,2]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.')
            self.SetStatusText('Switched On Raman Laser Lines: %s' % str(wl[lnum])+'nm' )
        else:
            self.raman532_1.remove()
            self.raman532_2.remove()
            self.raman532_3.remove()
            self.raman532_4.remove()
            self.raman532_5.remove()
            self.page_graph.axes.legend_= None
            
        AdjustDisplay(self,1)    
        
    def OnShowRaman561(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        lnum = 7
        if item.IsChecked() == True:
            if self.ramanonoff == True:            
                self.raman561_1, = self.page_graph.axes.plot([self.raman_water[lnum,1],self.raman_water[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--',
                        label='Raman Water '+str(wl[lnum])+'nm')
            elif self.ramanonoff == False:
                self.raman561_1, = self.page_graph.axes.plot([self.raman_water[lnum,1],self.raman_water[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            self.raman561_2, = self.page_graph.axes.plot([self.raman_water[lnum,2],self.raman_water[lnum,2]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            self.raman561_3, = self.page_graph.axes.plot([self.raman_water[lnum,3],self.raman_water[lnum,3]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            if self.ramanonoff == True: 
                self.raman561_4, = self.page_graph.axes.plot([self.raman_glas[lnum,1],self.raman_glas[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.',
                        label='Raman Glass '+str(wl[lnum])+'nm')
            elif self.ramanonoff == False:
                self.raman561_4, = self.page_graph.axes.plot([self.raman_glas[lnum,1],self.raman_glas[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.') 
            self.raman561_5, = self.page_graph.axes.plot([self.raman_glas[lnum,2],self.raman_glas[lnum,2]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.')
            self.SetStatusText('Switched On Raman Laser Lines: %s' % str(wl[lnum])+'nm' )
        else:
            self.raman561_1.remove()
            self.raman561_2.remove()
            self.raman561_3.remove()
            self.raman561_4.remove()
            self.raman561_5.remove()
            self.page_graph.axes.legend_= None
            
        AdjustDisplay(self,1)
                
    def OnShowRaman594(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        lnum = 8
        if item.IsChecked() == True:
            if self.ramanonoff == True:            
                self.raman594_1, = self.page_graph.axes.plot([self.raman_water[lnum,1],self.raman_water[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--',
                        label='Raman Water '+str(wl[lnum])+'nm')
            elif self.ramanonoff == False:
                self.raman594_1, = self.page_graph.axes.plot([self.raman_water[lnum,1],self.raman_water[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            self.raman594_2, = self.page_graph.axes.plot([self.raman_water[lnum,2],self.raman_water[lnum,2]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            self.raman594_3, = self.page_graph.axes.plot([self.raman_water[lnum,3],self.raman_water[lnum,3]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            if self.ramanonoff == True: 
                self.raman594_4, = self.page_graph.axes.plot([self.raman_glas[lnum,1],self.raman_glas[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.',
                        label='Raman Glass '+str(wl[lnum])+'nm')
            elif self.ramanonoff == False:
                self.raman594_4, = self.page_graph.axes.plot([self.raman_glas[lnum,1],self.raman_glas[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.') 
            self.raman594_5, = self.page_graph.axes.plot([self.raman_glas[lnum,2],self.raman_glas[lnum,2]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.')
            self.SetStatusText('Switched On Raman Laser Lines: %s' % str(wl[lnum])+'nm' )
        else:
            self.raman594_1.remove()
            self.raman594_2.remove()
            self.raman594_3.remove()
            self.raman594_4.remove()
            self.raman594_5.remove()
            self.page_graph.axes.legend_= None

        AdjustDisplay(self,1)
                
    def OnShowRaman640(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        lnum = 9
        if item.IsChecked() == True:
            if self.ramanonoff == True:            
                self.raman640_1, = self.page_graph.axes.plot([self.raman_water[lnum,1],self.raman_water[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--',
                        label='Raman Water '+str(wl[lnum])+'nm')
            elif self.ramanonoff == False:
                self.raman640_1, = self.page_graph.axes.plot([self.raman_water[lnum,1],self.raman_water[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            self.raman640_2, = self.page_graph.axes.plot([self.raman_water[lnum,2],self.raman_water[lnum,2]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            self.raman640_3, = self.page_graph.axes.plot([self.raman_water[lnum,3],self.raman_water[lnum,3]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '--')
            if self.ramanonoff == True: 
                self.raman640_4, = self.page_graph.axes.plot([self.raman_glas[lnum,1],self.raman_glas[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.',
                        label='Raman Glass '+str(wl[lnum])+'nm')
            elif self.ramanonoff == False:
                self.raman640_4, = self.page_graph.axes.plot([self.raman_glas[lnum,1],self.raman_glas[lnum,1]],
                    [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.') 
            self.raman640_5, = self.page_graph.axes.plot([self.raman_glas[lnum,2],self.raman_glas[lnum,2]],
                [self.ymin,self.ymax], color=colors[lnum], lw=linew-1, linestyle = '-.')
            self.SetStatusText('Switched On Raman Laser Lines: %s' % str(wl[lnum])+'nm' )
        else:
            self.raman640_1.remove()
            self.raman640_2.remove()
            self.raman640_3.remove()
            self.raman640_4.remove()
            self.raman640_5.remove()
            self.page_graph.axes.legend_= None

        AdjustDisplay(self,1)

    def OnShowFura340(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        if item.IsChecked() == True:
            self.fura340, = self.page_graph.axes.bar([330], [self.ymax], label='Ex340 +/-20nm',
			    color='#8800ff', width = 20, alpha = 0.5)
            self.SetStatusText('Switched On Fura Excitation 340nm +/-20' )
        else:
            self.fura340.remove()
            self.page_graph.axes.legend_= None
            
        AdjustDisplay(self,1)
        
    def OnShowFura380(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        if item.IsChecked() == True:
            self.fura380, = self.page_graph.axes.bar([370], [self.ymax],  label='Ex380 +/-20nm',
			    color='#8800ff', width = 20, alpha = 0.5)
            self.SetStatusText('Switched On Fura Excitation 380nm +/-20' )
        else:
            self.fura380.remove()
            self.page_graph.axes.legend_= None
            
        AdjustDisplay(self,1)
        
    def OnShowCustomLaser(self,  event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        if item.IsChecked() == True:
            dlg = wx.NumberEntryDialog(None, 'Enter Laser Wavelength',
            'WL [nm]', 'Custom Laser Line',  355,  self.xmin_limit, self.xmax_limit)
            if dlg.ShowModal() == wx.ID_OK:
                cwl = dlg.GetValue() # get entered value for custom laser wavelength
                if self.laseronoff == True:
                    self.claser, = self.page_graph.axes.plot([cwl,cwl],
                        [self.ymin,self.ymax], 'm-', lw=linew, label=str(cwl)+'nm')
                elif self.laseronoff == False:
                    self.claser, = self.page_graph.axes.plot([cwl,cwl],
                        [self.ymin,self.ymax], 'm-', lw=linew)
                        
                self.SetStatusText('Switched On Custom Laser Line: %s' % str(cwl)+'nm' )
            
            dlg.Destroy()
            
        else:
            self.claser.remove()  # delete custom laser line
            self.page_graph.axes.legend_= None
            
        AdjustDisplay(self,1)
        
    def OnShowCustomRaman(self,  event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        if item.IsChecked() == True:
            dlg = wx.NumberEntryDialog(None, 'Enter Laser Wavelength',
            'WL [nm]', 'Custom Raman Lines ',  355,  self.xmin_limit, self.xmax_limit)
            if dlg.ShowModal() == wx.ID_OK:
                crwl = dlg.GetValue() # get entered value for custom laser wavelength
                cr1 = 1.0 /(1.0/crwl - 1595/1E7)
                cr2 = 1.0 /(1.0/crwl - 3652/1E7)
                cr3 = 1.0 /(1.0/crwl - 3756/1E7)
                glas_raman_wn = 1200.0 # wave number for raman glas spectrum
                #glas_raman_wl = 1000 * 1/(glas_raman_wn/10000) # cooresponding wavelength [nm]
                cr4 = 1.0 /(1.0/crwl-glas_raman_wn/1E7)
                cr5 = 1.0 /(1.0/crwl+glas_raman_wn/1E7)
                if self.ramanonoff == True:
                    self.craman1, = self.page_graph.axes.plot([cr1, cr1], [self.ymin,self.ymax], 'm--',
                                                              label='Raman Water '+str(crwl)+'nm')
                elif self.ramanonoff == False:
                    self.craman1, = self.page_graph.axes.plot([cr1, cr1], [self.ymin,self.ymax], 'm--')
                self.craman2, = self.page_graph.axes.plot([cr2, cr2], [self.ymin,self.ymax], 'm--')
                self.craman3, = self.page_graph.axes.plot([cr3, cr3], [self.ymin,self.ymax], 'm--',)
                if self.ramanonoff == True:
                    self.craman4, = self.page_graph.axes.plot([cr4, cr4], [self.ymin,self.ymax], 'm-.',
                                                              label='Raman Glas '+str(crwl)+'nm')
                elif self.ramanonoff == False:
                    self.craman4, = self.page_graph.axes.plot([cr4, cr4], [self.ymin,self.ymax], 'm-.')
                self.craman5, = self.page_graph.axes.plot([cr5, cr5], [self.ymin,self.ymax], 'm-.')
                self.SetStatusText('Switched On Custom Raman Laser Lines: %s' % str(crwl)+'nm' )
            
            dlg.Destroy()
            
        else:
            self.craman1.remove()  # delete custom raman laser lines
            self.craman2.remove()
            self.craman3.remove()
            self.craman4.remove()
            self.craman5.remove()
            self.page_graph.axes.legend_= None
            
        AdjustDisplay(self,1)
    
    def OnShowLaserLines(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        self.laseronoff = item.IsChecked()

    def OnShowRamanLines(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        self.ramanonoff = item.IsChecked()        
    
    def OnInterpolateFilter(self,  event):
        
        # fontsize
        fsz = 11        
        
        fedlg = FilterEffDlg(None, -1, 'Calculate Filter Efficiency')
        fedlg.ShowModal()
        if (fedlg.calcdone == True):
            
            # plot fluorescence spectra            
            self.gfintp1, = self.page_filterinterp.axes.plot(fedlg.flu[:, 0],fedlg.flu[:, 1], 'k-', lw=2, label=fedlg.flutitle)
            # fill area under curve
            self.gfintp1c = self.page_filterinterp.axes.fill_between(fedlg.flu[:, 0],fedlg.flu[:, 1],fedlg.flu[:, 1]*0, facecolor='blue', alpha = 0.4)               
            
            # plot dichroic1 1
            self.gfintp2, = self.page_filterinterp.axes.plot(fedlg.filter1[:, 0], fedlg.filter1[:, 1], 'g-', lw=2, label=fedlg.filtertitle1)
            
            # dichroic 2 - if loaded            
            try:
                # plot dichroic2                 
                self.gfintp3, = self.page_filterinterp.axes.plot(fedlg.filter2[:, 0], fedlg.filter2[:, 1], 'g--', lw=2, label=fedlg.filtertitle2)
                # plot result after dichroic 2   
                #self.gfintp4, = self.page_filterinterp.axes.plot(fedlg.reswave2,fedlg.result2, 'k.-',lw=4, label='Filtered 2')
                #self.txt3  = self.page_filterinterp.axes.text(self.xmax-100, 0.80, 'Eff. after Dichroic 2  : %.2f' %fedlg.df2)
            
            except:
                print '2nd dichroic was not loaded.'
            
            #plot emission filter                                                
            self.gfintp5, = self.page_filterinterp.axes.plot(fedlg.filter3[:, 0], fedlg.filter3[:, 1], 'r-', lw=2, label=fedlg.filtertitle3)                                                         
            
            # plot result after dichroic 1
            self.gfintp6, = self.page_filterinterp.axes.plot(fedlg.reswave1,fedlg.result1, 'k--', lw=2, label='Filtered 1')
            
            try:
                # plot result after dichroic 2   
                self.gfintp4, = self.page_filterinterp.axes.plot(fedlg.reswave2,fedlg.result2, 'k.',lw=4, label='Filtered 2')
                self.txt2  = self.page_filterinterp.axes.text(self.xmax-100, 0.75, 'Eff. of Dichroic 2  : %.2f' %fedlg.df2, fontsize = fsz)
            except:
                print '2nd dichroic was not loaded.'
            
            
            # plot result after emission filter           
            self.gfintp7, = self.page_filterinterp.axes.plot(fedlg.reswave3,fedlg.result3, 'b-',lw=4, label='Filtered 3')
            
            self.gfintp7c = self.page_filterinterp.axes.fill_between(fedlg.reswave3,fedlg.result3,fedlg.result3*0, facecolor='red', alpha = 0.4)            
            
            self.txt1  = self.page_filterinterp.axes.text(self.xmax-100, 0.80, 'Eff. of Dichroic 1 : %.2f' %fedlg.df1, fontsize = fsz)
            #self.txt2  = self.page_filterinterp.axes.text(self.xmax-100, 0.75, 'Eff. of Dichroic 2 : %.2f' %fedlg.df2)
            self.txt3  = self.page_filterinterp.axes.text(self.xmax-100, 0.70, 'Eff. of EM-Filter  : %.2f' %fedlg.df3, fontsize = fsz)
            self.txt4  = self.page_filterinterp.axes.text(self.xmax-100, 0.65, 'Efficiency Overall : %.2f' %fedlg.df_all, fontsize = fsz)
            AdjustDisplay(self,2)
            self.ToggleItem(event, 1)
            fedlg.Destroy()
        
    def OnDelInterpolation(self,  event):
        self.gfintp1.remove()
        self.gfintp1c.remove()
        self.gfintp2.remove()
        #self.gfintp3.remove()
        #self.gfintp4.remove()
        self.gfintp5.remove()
        self.gfintp6.remove()
        self.gfintp7.remove()
        self.gfintp7c.remove()
        self.txt1.remove()
        self.txt3.remove()
        self.txt4.remove()
        try:        
            self.gfintp3.remove()
            self.gfintp4.remove()            
            self.txt2.remove()
        except:
            print 'Nothing to remove since dichroic 2 was not loaded.'
        
        self.page_filterinterp.axes.legend_= None
        AdjustDisplay(self,2)
        self.ToggleItem(event, -1)       
        self.page_filterinterp.figure.canvas.draw()

    def OnSetXMin(self,  event):
        dlg = wx.NumberEntryDialog(None, 'Enter Value for X-Min',
            'X-Min [nm]', 'X-Min Adjustment',  self.xmin,  self.xmin_limit, self.xmax_limit)
        if dlg.ShowModal() == wx.ID_OK:
            self.xmin = dlg.GetValue() # get entered value
            # check values
            if self.xmin < self.xmin_limit:
                self.xmin = self.xmin_limit
            if self.xmin > self.xmax-100:
                self.xmin = self.xmax-100
            self.page_graph.axes.axis([self.xmin, self.xmax, self.ymin, self.ymax]) # do the scaling
            self.page_graph.figure.canvas.draw() # display graph
            self.page_filterinterp.axes.axis([self.xmin, self.xmax, self.ymin, self.ymax]) # do the scaling
            self.page_filterinterp.figure.canvas.draw() # display graph for filter interpolation
        dlg.Destroy()
        
    def OnSetXMax(self, event):
        dlg = wx.NumberEntryDialog(None, 'Enter Value for X-Min',
            'X-Max [nm]', 'X-Max Adjustment',  self.xmax,  self.xmin_limit, self.xmax_limit)
        if dlg.ShowModal() == wx.ID_OK:
            self.xmax = dlg.GetValue()
            if self.xmax > self.xmax_limit:
                self.xmax = self.xmax_limit
            if self.xmax < self.xmin+100:
                self.xmax = self.xmin+100
            self.page_graph.axes.axis([self.xmin, self.xmax, self.ymin, self.ymax])
            self.page_graph.figure.canvas.draw()
            self.page_filterinterp.axes.axis([self.xmin, self.xmax, self.ymin, self.ymax]) # do the scaling
            self.page_filterinterp.figure.canvas.draw() # display graph for filter interpolation
        dlg.Destroy()
        
    def OnEnterBand(self,  event):
            item = self.GetMenuBar().FindItemById(event.GetId())
            if item.IsChecked() == True:            
                # enter center wavelength in [nm]                
                dlg = wx.NumberEntryDialog(None, 'Enter Center Wavelength for Bandpass Filter',
                    'Center [nm]', 'Center Adjustment',  self.bp_center_last,  100, 2000)
                if dlg.ShowModal() == wx.ID_OK:
                    self.bp_center_last = dlg.GetValue() # get band filter center wavelength
                dlg.Destroy()
                # enter bandwith in [nm]
                dlg = wx.NumberEntryDialog(None, 'Enter Bandpass Width Filter',
                    'Bandpass [nm]', 'Bandpass Adjustment',  self.bp_width_last,  2, 200)
                if dlg.ShowModal() == wx.ID_OK:
                    self.bp_width_last = dlg.GetValue() # get bandpass width
                dlg.Destroy()
                # create label string
                bp_label = 'BP '+ str(self.bp_center_last) + ' / ' + str(self.bp_width_last)
                # draw bandpass filter
                self.bp, = self.page_graph.axes.bar(self.bp_center_last - self.bp_width_last/2, self.ymax, label=bp_label,
    			    color='grey', width = self.bp_width_last, alpha = 0.5)
                self.SetStatusText('Switched On Bandpass Filter : ' + bp_label )
            else:
                self.bp.remove()
                self.page_graph.axes.legend_= None
                
            AdjustDisplay(self,1)
        
    def OnSetLegendSize(self, event):
        idfirst = 183        
        legsize_selected =  event.GetId()
        if (legsize_selected == idfirst):
            legsize = 'x-small'
        if (legsize_selected == idfirst+1):
            legsize = 'small'
        if (legsize_selected == idfirst+2):
            legsize = 'medium' 

# end of class MplFrame

if __name__ == '__main__':
    app = wx.PySimpleApp()
    wx.InitAllImageHandlers()
    MplFrame = MplFrame(parent=None, id = -1)
    app.SetTopWindow(MplFrame)
    MplFrame.Show()
    app.MainLoop()
