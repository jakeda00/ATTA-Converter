import tkMessageBox
from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename


# START -- function definitions:

def cross():
    if tkMessageBox.askokcancel(u"Quit ATTA Convertor ?", "Are you sure you want to close the program ?"):
        mainwin.quit()

def workwin_open():
    global workwin
    workwin = Toplevel(mainwin)
    workwin.resizable(0, 0)
    workwin.overrideredirect(True)  # nejde videt lista
    w = 250  # width for the Tk root
    h = 200  # height for the Tk root

    # get screen width and height
    ws = mainwin.winfo_screenwidth()  # width of the screen
    hs = mainwin.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    workwin.geometry('+%d+%d' % (x, y))


    sep_frame = Frame(workwin, bg='saddle brown', width=250, height=10)
    work_frame = Frame(workwin, width=200, height=180)
    sep2_frame = Frame(workwin, bg='saddle brown', width=250, height=10)
    sep_frame.grid(row=0)
    work_frame.grid(row=1)
    sep2_frame.grid(row=2)

    Label(work_frame, text="Conversion in progress ...",padx=25,pady=35,bg='PeachPuff3',font="Helvetica 12 bold").grid(row=0, column=0)

def endofconv():
    global workwin
    workwin.destroy()
    if tkMessageBox.askyesno(u"Convert another file?", "Are you want to convert some another file?"):
        new()



def idrirast():
    global workwin
    workwin_open()
    outputname = asksaveasfilename(parent=workwin, filetypes=[('Idrisi Raster Format', '*.rst')], defaultextension=".rst")
    if (outputname != ""):
        try_convert_raster(outputname, 'RST')
    endofconv()

def ascirast():
    global workwin
    workwin_open()
    outputname = asksaveasfilename(parent=workwin, filetypes=[('ARC/INFO ASCII GRID', '*.asc')], defaultextension=".asc")
    if (outputname != ""):
        try_convert_raster(outputname, 'AAIGrid')
    endofconv()

def tifrast():
    global workwin
    workwin_open()
    outputname = asksaveasfilename(parent=workwin, filetypes=[('GeoTIFF', '*.tif')], defaultextension=".tif")
    if (outputname != ""):
        try_convert_raster(outputname, 'GTiff')
    endofconv()


def try_convert_raster(outputname,driver):
    try:
        convert_raster(outputname, driver)
    except Exception, error:
        errmes = error.message
    finally:
        if 'errmes' in locals():
            print errmes
            tkMessageBox.showwarning("Error!", "The raster file hasn't been converted.\n\n"+errmes)
        else:
            if driver == 'AAIGrid':
                driver= 'ASCII Grid'
            elif driver == 'Gtiff':
                driver= 'GeoTIFF'
            tkMessageBox.showinfo("Done!", "The raster file has been converted. \n\nNew "+driver+" file is saved as:\n\n"+outputname)

def convert_raster(outputname, format):
    # Import gdal
    global inputname
    from osgeo import gdal

    # Open existing dataset
    src_ds = gdal.Open(inputname)

    # Open output format driver, see gdal_translate --formats for list
    driver = gdal.GetDriverByName(format)

    # Output to new format
    dst_ds = driver.CreateCopy(outputname, src_ds, 0)

    # Properly close the datasets to flush to disk
    dst_ds = None
    src_ds = None



def shpvect():
    global workwin
    workwin_open()
    outputname = asksaveasfilename(parent=workwin, filetypes=[('Esri Shapefile', '*.shp')], defaultextension=".shp")
    if (outputname != ""):
        try_convert_vector(outputname, 'ESRI Shapefile')
    endofconv()

def gmlvect():
    global workwin
    workwin_open()
    outputname = asksaveasfilename(parent=workwin, filetypes=[('Geography Markup Language', '*.gml')], defaultextension=".gml")
    if (outputname != ""):
        try_convert_vector(outputname, 'GML')
    endofconv()



def try_convert_vector(outputname, driver):
    import ogr2ogr
    global inputname
    try:
        status = ogr2ogr.main(["", "-f", driver, outputname, inputname])
    except Exception, error:
        errmes = error.message
    finally:
        if status == True:
            if driver=='GML':
                driver = 'GML file'
            tkMessageBox.showinfo("Done!", "The vector file has been converted. \n\nNew "+driver+" is saved as:\n\n"+outputname)
        else:
            if 'errmes' in locals():
                tkMessageBox.showwarning("Error!", "The vector file hasn't been converted.\n\n" + errmes)
            else:
                tkMessageBox.showwarning("Error!", "The vector file hasn't been converted.\n\nSome unknown error.")






def openfile():
    global inputname, lfilename, bopenfile
    if (inputname == ""):
        inputname = askopenfilename(parent=mainwin, **FILEOPENOPTIONS)
        if (inputname != ""):
            print "opening file..."
            filetype = inputname.split(".")
            filename = inputname.split("/")
            ftype = filetype[len(filetype) - 1]
            fname = filename[len(filename) - 1]
            bopenfile.config(state=DISABLED)
            lfilename.config(text=fname)
            lfilename.config(bg="PeachPuff3")
            lpath.config(text=inputname)
            lpath.config(bg="PeachPuff3")
            if ftype == 'asc':
                lfileformat.config(text="ARC/INFO ASCII GRID", bg="PeachPuff3")
                outformat1.config(text="Idrisi Raster")
                outformat1popis.config(text="Raster format used by \nGIS software - TerrSet \n(formerly Idrisi).\n")
                b_conv1.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nIdrisi Raster", command=idrirast)
                outformat2.config(text="GeoTIFF")
                outformat2popis.config(
                    text="Represents an effort to estabilish a TIFF based interchange format for georeferenced raster imaginery.\n")
                b_conv2.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nGeoTIFF", command=tifrast)
            elif ftype == 'rst':
                lfileformat.config(text="Idrisi Raster Format", bg="PeachPuff3")
                outformat1.config(text="ARC/INFO ASCII GRID")
                outformat1popis.config(text="Raster GIS file format developed by Esri and used by GIS software ArcGIS. ")
                b_conv1.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nASCII GRID", command=ascirast)
                outformat2.config(text="GeoTIFF")
                outformat2popis.config(
                    text="Represents an effort to estabilish a TIFF based interchange format for georeferenced raster imaginery.\n")
                b_conv2.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nGeoTIFF", command=tifrast)
            elif ftype == 'tif':
                lfileformat.config(text="GeoTIFF", bg="PeachPuff3")
                outformat1.config(text="ARC/INFO ASCII GRID")
                outformat1popis.config(text="Raster GIS file format developed by Esri and used by GIS software ArcGIS. ")
                b_conv1.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nASCII GRID", command=ascirast)
                outformat2.config(text="Idrisi Raster")
                outformat2popis.config(text="Raster format used by \nGIS software - TerrSet \n(formerly Idrisi).\n")
                b_conv2.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nIdrisi Raster", command=idrirast)
            elif ftype == 'shp':
                lfileformat.config(text="Esri Shapefile", bg="PeachPuff3")
                outformat1.config(text="Idrisi Vector")
                outformat1popis.config(text="Vector format used by \nGIS software - TerrSet \n(formerly Idrisi).\n")
                b_conv1.config(bg="SystemButtonFace", text="UNAVIALABLE")
                outformat2.config(text="Geography Markup Language", font="Helvetica 10 bold")
                outformat2popis.config(
                    text="GML is the XML grammar defined by the Open Geospatial Consortium (OGC) to express geographical features.")
                b_conv2.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nGML", command=gmlvect)
            elif ftype == 'vct':
                lfileformat.config(text="Idrisi Vector Format", bg="PeachPuff3")
                outformat1.config(text="Esri Shapefile")
                outformat1popis.config(
                    text="A popular geospatial vector data format for GIS software. It is developed and regulated by Esri and used by ArcGIS.")
                b_conv1.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nEsri Shapefile", command=shpvect)
                outformat2.config(text="Geography Markup Language")
                outformat2popis.config(
                    text="GML is the XML grammar defined by the Open Geospatial Consortium (OGC) to express geographical features.")
                b_conv2.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nGML", command=gmlvect)
            elif ftype == 'gml':
                lfileformat.config(text="Geography Markup Language", bg="PeachPuff3")
                outformat1.config(text="Esri Shapefile")
                outformat1popis.config(
                    text="A popular geospatial vector data format for GIS software. It is developed and regulated by Esri and used by ArcGIS.")
                b_conv1.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nEsri Shapefile", command=shpvect)
                outformat2.config(text="Idrisi Vector")
                outformat2popis.config(text="Vector format used by \nGIS software - TerrSet \n(formerly Idrisi).\n")
                b_conv2.config(bg="SystemButtonFace", text="UNAVIALABLE")
            print inputname
            print "file open!"


def new():
    global inputname
    if (inputname != ""):
        inputname = ""
        bopenfile.config(state=ACTIVE)
        lfilename.config(text="", bg="SystemButtonFace")
        lpath.config(text="", bg="SystemButtonFace")
        lfileformat.config(text="", bg="SystemButtonFace")
        outformat1.config(text="")
        outformat1popis.config(text="\n\n\n")
        b_conv1.config(state=DISABLED, bg="PeachPuff3", text="Convert", command=NONE)
        outformat2.config(text="")
        outformat2popis.config(text="\n\n\n")
        b_conv2.config(state=DISABLED, bg="PeachPuff3", text="Convert", command=NONE)
        print "new file..."


def about():
    global aboutopen

    def crosss():
        global aboutopen
        aboutopen = 0
        subwin.destroy()

    if aboutopen == 0:
        subwin = Toplevel(mainwin)
        subwin.title("About ATTA Convertor")
        subwin.resizable(0, 0)

        w = 426  # width for the Tk root
        h = 570  # height for the Tk root

        # get screen width and height
        ws = mainwin.winfo_screenwidth()  # width of the screen
        hs = mainwin.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        subwin.geometry('+%d+%d' % (x, y))
        subwin.iconbitmap('Icon.ico')
        subwin.protocol("WM_DELETE_WINDOW", crosss)

        aboutopen = 1

        sep_frame = Frame(subwin, bg='saddle brown', width=426, height=10)
        leftsep_frame = Frame(subwin, bg='saddle brown', width=6, height=159)
        about_frame = Frame(subwin, width=430, height=180, bg='PeachPuff3')
        rightsep_frame = Frame(subwin, bg='saddle brown', width=6, height=159)
        centersep_frame = Frame(subwin, bg='saddle brown', width=426, height=5)
        about_frame2 = Frame(subwin, width=430, height=180, bg='PeachPuff3')
        sep2_frame = Frame(subwin, bg='saddle brown', width=426, height=10)
        sep_frame.grid(row=0,columnspan=3)
        leftsep_frame.grid(row=1,column=0)
        about_frame.grid(row=1,column=1)
        rightsep_frame.grid(row=1,column=2)
        centersep_frame.grid(row=2,columnspan=3)
        about_frame2.grid(row=3,columnspan=3)
        sep2_frame.grid(row=4,columnspan=3)

        Label(about_frame, text="", font="Helvetica 4", bg='PeachPuff3').grid(row=0, column=0)

        Label(about_frame, text="Author:",font='Helvetica 12 bold', bg='PeachPuff3').grid(row=1, column=0, sticky=E)
        Label(about_frame, text="David Jakes",font='Helvetica 12', bg='PeachPuff3').grid(row=1, column=1, sticky=W)
        Label(about_frame, text="\n", font="Helvetica 4", bg='PeachPuff3').grid(row=2, column=0)
        Message(about_frame, text="Program was developed within the bachelor thesis on Palacky University Olomouc.",font='Helvetica 8',width=300, bg='PeachPuff3').grid(row=3,columnspan=2)
        Label(about_frame, text="", font="Helvetica 4", bg='PeachPuff3').grid(row=4, column=0)
        Label(about_frame, text="Name of bachelor thesis:", font='Helvetica 8 bold', bg='PeachPuff3').grid(row=5, columnspan=2)
        Label(about_frame, text="Program for reversible data conversion between ArcGIS a TerrSet", font='Helvetica 8', bg='PeachPuff3',width=68).grid(row=6, columnspan=2)
        Label(about_frame, text="\n", font="Helvetica 4", bg='PeachPuff3').grid(row=7, column=0)




        Label(about_frame2, text="", font="Helvetica 4", bg='PeachPuff3').grid(row=0, column=0)
        Label(about_frame2, text="License:", font='Helvetica 12 bold', bg='PeachPuff3').grid(row=1, column=0, sticky=E)
        Label(about_frame2, text="X/MIT", font='Helvetica 12', bg='PeachPuff3').grid(row=1, column=1, sticky=W)
        Label(about_frame2, text="\n", font="Helvetica 4", bg='PeachPuff3').grid(row=2, column=0)
        Label(about_frame2, text="Copyright (c) 2017 David Jakes", font='Helvetica 8 bold', bg='PeachPuff3',width=60).grid(row=3, columnspan=2)
        Label(about_frame2, text="", font="Helvetica 4", bg='PeachPuff3').grid(row=4, column=0)
        Message(about_frame2, text="Permission is hereby granted, free of charge, to any person\nobtaining a copy of this software and associated documentation\nfiles (the \"Software\"), to deal in the Software without\nrestriction, including without limitation the rights to use,\ncopy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the\nSoftware is furnished to do so, subject to the following\nconditions:", font='Helvetica 8',width=400, bg='PeachPuff3').grid(row=5, columnspan=2)
        Label(about_frame2, text="", font="Helvetica 4", bg='PeachPuff3').grid(row=6, column=0)
        Message(about_frame2, text="The above copyright notice and this permission notice shall be\nincluded in all copies or substantial portions of the Software.", font='Helvetica 8',width=400, bg='PeachPuff3').grid(row=7, columnspan=2)
        Label(about_frame2, text="", font="Helvetica 4", bg='PeachPuff3').grid(row=8, column=0)
        Message(about_frame2, text="THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND,\nEXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES\nOF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND\nNONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT\nHOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,\nWHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING\nFROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR\nOTHER DEALINGS IN THE SOFTWARE.", font='Helvetica 8',width=400, bg='PeachPuff3').grid(row=9, columnspan=2)
        Label(about_frame2, text="", font="Helvetica 4", bg='PeachPuff3').grid(row=10, column=0)

        subwin.focus_set()

def formats():
    print "formats"


def manual():
    print "manual"


# END -- function definitions




# initialize window

mainwin = Tk()

mainwin.title("ATTA Convertor")
mainwin.resizable(0, 0)
mainwin.protocol("WM_DELETE_WINDOW", cross)

w = 555 # width for the Tk root
h = 570 # height for the Tk root

# get screen width and height
ws = mainwin.winfo_screenwidth() # width of the screen
hs = mainwin.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

mainwin.geometry('+%d+%d' % ( x, y))
mainwin.iconbitmap('Icon.ico')

# create menu
mainMenu = Menu(mainwin)

# create cascade menu for menu items (File)
menuFile = Menu(mainMenu, tearoff=0)
menuFile.add_command(label="New", command=new)
menuFile.add_separator()
menuFile.add_command(label="Quit", command=cross)
mainMenu.add_cascade(label="File", menu=menuFile)

# create cascade menu for menu items (Help)
menuHelp = Menu(mainMenu, tearoff=0)
menuHelp.add_command(label="Supported formats", command=formats)
menuHelp.add_command(label="User's Manual", command=manual)
mainMenu.add_cascade(label="Help", menu=menuHelp)

# create menu item (about...)
mainMenu.add_command(label="About...", command=about)

# dispaly menu
mainwin.config(menu=mainMenu)

global inputname, lfilename, bopenfile, aboutopen, workwin
inputname = ""
aboutopen = 0
FILEOPENOPTIONS = dict(defaultextension='.shp',
                       filetypes=[('ATTA Convertor supported formats', '*.asc;*.rst;*.tif;*.shp;*.vct;*.gml')])

# create all of the main containers

separator1_frame = Frame(mainwin, bg='saddle brown', width=556, height=10)
buton_frame = Frame(mainwin, width=150, height=150)
input_frame = Frame(mainwin, width=400, height=150)
separator2_frame = Frame(mainwin, bg='saddle brown', width=556, height=10)

aviable_frame = Frame(mainwin, bg='PeachPuff3', width=556, height=40)
output_frame = Frame(mainwin, width=550, height=400)
footer_frame = Frame(mainwin, bg='saddle brown', width=556, height=15)

# layout all of the main containers

mainwin.grid_columnconfigure(1, weight=1)

separator1_frame.grid(row=0, columnspan=2)
buton_frame.grid(row=1, column=0, sticky='nw')
input_frame.grid(row=1, column=1, sticky='nw', pady=13, padx=0)
separator2_frame.grid(row=2, columnspan=2)

aviable_frame.grid(row=3, columnspan=2, sticky='nw')
output_frame.grid(row=4, columnspan=2, sticky='nw')
footer_frame.grid(row=5, columnspan=2, sticky='nw')

# buton_frame content

bopenfile = Button(buton_frame, text="Open File", command=openfile, height=5, width=10, bg="PeachPuff3")
bopenfile.grid(row=0, pady=30, padx=30)

# input_frame content

Label(input_frame, text="", font="Helvetica 1").grid(row=0, column=0)





Label(input_frame, text="File name:  ", font="Helvetica 10 bold").grid(row=1, column=0, sticky=W)
lfilename = Message(input_frame, text="", font="Helvetica 10 bold", padx=10,width=290,pady=5)
lfilename.grid(row=1, column=1, sticky=W)

Label(input_frame, text="", font="Helvetica 1").grid(row=2, column=0)
#outformat2popis = Message(output_frame, text="\n\n\n", width=200)




Label(input_frame, text="Format:  ", font="Helvetica 10 bold").grid(row=3, column=0, sticky=E)
lfileformat = Label(input_frame, text="", font="Helvetica 10", padx=10,pady=5)
lfileformat.grid(row=3, column=1, sticky=W)

Label(input_frame, text="", font="Helvetica 1").grid(row=4, column=0)

Label(input_frame, text="Path:  ", font="Helvetica 10 bold").grid(row=5, column=0, sticky=E)
lpath = Message(input_frame, text="", font="Helvetica 8", padx=10,width=290,pady=5)
lpath.grid(row=5, column=1, sticky=W)





Label(input_frame, text="", font="Helvetica 1").grid(row=6, column=0)

# aviable_frame content
Label(aviable_frame, text="Available conversion", width=55, bg='PeachPuff3', height=2, font="Helvetica 13 bold").grid(
    row=0, column=0)

# output frame content

# column layout
Label(output_frame, text="", width=15).grid(row=0, column=0)
Label(output_frame, text="", width=30).grid(row=0, column=1)
Label(output_frame, text="", width=30).grid(row=0, column=2)

# first descriptive column
Label(output_frame, text="Format:", font="Helvetica 10 bold").grid(row=1, column=0, sticky=E)
Label(output_frame, text="").grid(row=2, column=0)
Label(output_frame, text="Desription:", font="Helvetica 10 bold").grid(row=3, column=0, sticky=E)
Label(output_frame, text="").grid(row=4, column=0)
Label(output_frame, text="     Convert with:", font="Helvetica 10 bold").grid(row=5, column=0, sticky=E)

# second convert column
outformat1 = Label(output_frame, text="", font="Helvetica 10 bold")
outformat1.grid(row=1, column=1)

Label(output_frame, text="").grid(row=2, column=1)

outformat1popis = Message(output_frame, text="\n\n\n", width=180)
outformat1popis.grid(row=3, column=1)

Label(output_frame, text="").grid(row=4, column=1)

ch_atrib1 = IntVar()
check1_atr = Checkbutton(output_frame, text="attribut table", variable=ch_atrib1, state=DISABLED,padx=50)
check1_atr.grid(row=5, column=1, sticky=W)


ch_proj1 = IntVar()
check1_proj = Checkbutton(output_frame, text="projection file", variable=ch_proj1, state=DISABLED,padx=50)
check1_proj.grid(row=6, column=1, sticky=W)

ch_meta1 = IntVar()
check1_meta = Checkbutton(output_frame, text="metadata", variable=ch_meta1, state=DISABLED,padx=50)
check1_meta.grid(row=7, column=1, sticky=W)

Label(output_frame, text="").grid(row=8, column=1)

b_conv1 = Button(output_frame, text="Convert", height=5, width=12, state=DISABLED, bg="PeachPuff3")
b_conv1.grid(row=9, column=1)

Label(output_frame, text="").grid(row=10, column=1)
# end column 2



# third convert column
outformat2 = Label(output_frame, text="", font="Helvetica 10 bold")
outformat2.grid(row=1, column=2)

Label(output_frame, text="").grid(row=2, column=2)

outformat2popis = Message(output_frame, text="\n\n\n", width=200)
outformat2popis.grid(row=3, column=2)

Label(output_frame, text="").grid(row=4, column=2)

ch_atrib2 = IntVar()
check2_atr = Checkbutton(output_frame, text="attribut table  ", variable=ch_atrib2, state=DISABLED,padx=50)
check2_atr.grid(row=5, column=2, sticky=W)


ch_proj2 = IntVar()
check2_proj = Checkbutton(output_frame, text="projection file", variable=ch_proj2, state=DISABLED,padx=50)
check2_proj.grid(row=6, column=2, sticky=W)

ch_meta2 = IntVar()
check2_meta = Checkbutton(output_frame, text="metadata       ", variable=ch_meta2, state=DISABLED,padx=50)
check2_meta.grid(row=7, column=2, sticky=W)

Label(output_frame, text="").grid(row=8, column=2)

b_conv2 = Button(output_frame, text="Convert", height=5, width=12, state=DISABLED, bg="PeachPuff3")
b_conv2.grid(row=9, column=2)

Label(output_frame, text="").grid(row=10, column=2)
Label(output_frame, text="").grid(row=11, column=2)
# end third column




mainwin.mainloop()
