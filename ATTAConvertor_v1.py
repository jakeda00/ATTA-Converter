import tkMessageBox
from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename




#START -- function definitions:

def cross():

    if tkMessageBox.askokcancel(u"Quit ATTA Convertor ?", "Are you sure you want to close the program ?"):
        mainwin.quit()


def idrirast():
    outputname = asksaveasfilename(parent=mainwin, filetypes=[('Idrisi Raster Format', '*.rst')], defaultextension=".rst")
    try_convert(outputname,'RST',"r")

def ascirast():
    outputname = asksaveasfilename(parent=mainwin, filetypes=[('ARC/INFO ASCII GRID', '*.asc')], defaultextension=".asc")
    try_convert(outputname,'AAIGrid',"r")

def tifrast():
    outputname = asksaveasfilename(parent=mainwin, filetypes=[('GeoTIFF', '*.tif')], defaultextension=".tif")
    try_convert(outputname,'GTiff',"r")

def shpvect():
    outputname = asksaveasfilename(parent=mainwin, filetypes=[('Esri Shapefile', '*.shp')], defaultextension=".shp")
    try_convert(outputname,'ESRI Shapefile',"v")

def gmlvect():
    outputname = asksaveasfilename(parent=mainwin, filetypes=[('Geography Markup Language', '*.gml')], defaultextension=".gml")
    try_convert(outputname,'GML',"v")


def try_convert(outputname,driver,data):
    try:
        if data == 'r':
            status = convert_raster(outputname,driver)
        elif data == 'v':
            import ogr2ogr
            global inputname
            status = ogr2ogr.main(["", "-f", driver, outputname, inputname])
    except Exception, error:
        print(error.message)
    finally:
        if 'status' in locals():
            if (status == None or status == True):
                tkMessageBox.showinfo("Done!","The file has been converted.")
                print "File been converted ... "
            else:
                tkMessageBox.showwarning("Failed!", "The file hasn't been converted. (for more info check console")
                print "File hasn't been converted ... "
        else:
            tkMessageBox.showwarning("Failed!", "The file hasn't been converted. (for more info check console")
            print "File hasn't been converted ... "


def convert_raster(outputname,format):
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






def openfile():
    global inputname, lfilename, bopenfile
    if(inputname == ""):
        inputname = askopenfilename(parent=mainwin,**FILEOPENOPTIONS)
        if (inputname != ""):
            print "opening file..."
            filetype = inputname.split(".")
            filename = inputname.split("/")
            ftype = filetype[len(filetype) - 1]
            fname = filename[len(filename) - 1]
            bopenfile.config(state=DISABLED)
            lfilename.config(text=fname)
            lfilename.config(bg = "PeachPuff3")
            lpath.config(text=inputname)
            lpath.config(bg = "PeachPuff3")
            if ftype=='asc':
                lfileformat.config(text="ARC/INFO ASCII GRID",bg = "PeachPuff3")
                outformat1.config(text="Idrisi Raster")
                outformat1popis.config(text="raster format used by \nGIS software - TerrSet \n(formerly Idrisi)\n")
                b_conv1.config(state=ACTIVE,bg="PeachPuff3",text="Convert\n to \nIdrisi Raster",command=idrirast)
                outformat2.config(text="GeoTIFF")
                outformat2popis.config(text="represents an effort to estabilish a TIFF based interchange format for georeferenced raster imaginery\n")
                b_conv2.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nGeoTIFF", command=tifrast)
            elif ftype=='rst':
                lfileformat.config(text="Idrisi Raster Format", bg="PeachPuff3")
                outformat1.config(text="ARC/INFO ASCII GRID",font="Helvetica 12 bold")
                outformat1popis.config(text="raster GIS file format developed by Esri and used by GIS software ArcGIS ")
                b_conv1.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nASCII GRID", command=ascirast)
                outformat2.config(text="GeoTIFF")
                outformat2popis.config(text="represents an effort to estabilish a TIFF based interchange format for georeferenced raster imaginery\n")
                b_conv2.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nGeoTIFF", command=tifrast)
            elif ftype=='tif':
                lfileformat.config(text="GeoTIFF", bg="PeachPuff3")
                outformat1.config(text="ARC/INFO ASCII GRID",font="Helvetica 12 bold")
                outformat1popis.config(text="raster GIS file format developed by Esri and used by GIS software ArcGIS ")
                b_conv1.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nASCII GRID", command=ascirast)
                outformat2.config(text="Idrisi Raster")
                outformat2popis.config(text="raster format used by \nGIS software - TerrSet \n(formerly Idrisi)\n")
                b_conv2.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nIdrisi Raster", command=idrirast)
            elif ftype=='shp':
                lfileformat.config(text="Esri Shapefile",bg = "PeachPuff3")
                outformat1.config(text="Idrisi Vector")
                outformat1popis.config(text="vector format used by \nGIS software - TerrSet \n(formerly Idrisi)\n")
                b_conv1.config(bg="SystemButtonFace",text="UNAVIALABLE")
                outformat2.config(text="Geography Markup Language",font="Helvetica 10 bold")
                outformat2popis.config(text="GML is the XML grammar defined by the Open Geospatial Consortium (OGC) to express geographical features")
                b_conv2.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nGML", command=gmlvect)
            elif ftype == 'vct':
                lfileformat.config(text="Idrisi Vector Format", bg="PeachPuff3")
                outformat1.config(text="Esri Shapefile")
                outformat1popis.config(text="a popular geospatial vector data format for GIS software. It is developed and regulated by Esri and used by ArcGIS")
                b_conv1.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nEsri Shapefile", command=shpvect)
                outformat2.config(text="Geography Markup Language", font="Helvetica 10 bold")
                outformat2popis.config(text="GML is the XML grammar defined by the Open Geospatial Consortium (OGC) to express geographical features")
                b_conv2.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nGML", command=gmlvect)
            elif ftype == 'gml':
                lfileformat.config(text="Geography Markup Language", bg="PeachPuff3")
                outformat1.config(text="Esri Shapefile")
                outformat1popis.config(text="a popular geospatial vector data format for GIS software. It is developed and regulated by Esri and used by ArcGIS")
                b_conv1.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nEsri Shapefile", command=shpvect)
                outformat2.config(text="Idrisi Vector")
                outformat2popis.config(text="vector format used by \nGIS software - TerrSet \n(formerly Idrisi)\n")
                b_conv2.config(bg="SystemButtonFace",text="UNAVIALABLE")
            print inputname
            print "file open!"



def new():
    global inputname
    if (inputname != ""):
        inputname = ""
        bopenfile.config(state=ACTIVE)
        lfilename.config(text="",bg="SystemButtonFace")
        lpath.config(text="",bg="SystemButtonFace")
        lfileformat.config(text="",bg="SystemButtonFace")
        outformat1.config(text="",font="Helvetica 14")
        outformat1popis.config(text="\n\n\n")
        b_conv1.config(state=DISABLED, bg="PeachPuff3", text="Convert", command=NONE)
        outformat2.config(text="",font="Helvetica 14")
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
        print "about"
        subwin = Toplevel(mainwin)
        subwin.title("About ATTA Convertor")
        subwin.resizable(0, 0)
        subwin.geometry("200x200+650+200")
        subwin.protocol("WM_DELETE_WINDOW", crosss)
        aboutopen = 1

        sep_frame = Frame(subwin, bg='saddle brown', width=200, height=10)
        about_frame = Frame(subwin, width=200, height=180,bg='PeachPuff3')
        sep2_frame = Frame(subwin, bg='saddle brown', width=200, height=10)
        sep_frame.grid(row=0)
        about_frame.grid(row=1)
        sep2_frame.grid(row=2)




def formats():
    print "formats"

def manual():
    print "manual"


#END -- function definitions




# initialize window

mainwin = Tk()
mainwin.title("ATTA Convertor")
mainwin.resizable(0,0)
mainwin.geometry("545x645+500+50")
mainwin.protocol("WM_DELETE_WINDOW", cross)



#create menu
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
mainMenu.add_command(label="about...", command=about)

# dispaly menu
mainwin.config(menu=mainMenu)







global inputname, lfilename, bopenfile, aboutopen
inputname = ""
aboutopen=0
FILEOPENOPTIONS = dict(defaultextension='.shp',
                  filetypes=[ ('ATTA Convertor supported formats','*.asc;*.rst;*.tif;*.shp;*.vct;*.gml')])



# create all of the main containers

separator1_frame = Frame(mainwin, bg='saddle brown', width=550, height=10)
buton_frame = Frame(mainwin, width= 150, height=150)
input_frame = Frame(mainwin, width= 400, height=150)
separator2_frame = Frame(mainwin, bg='saddle brown', width=550, height=10)

aviable_frame = Frame(mainwin, bg='PeachPuff3', width=550, height=40)
output_frame = Frame(mainwin, width=550, height=400)
footer_frame = Frame(mainwin, bg='saddle brown', width=550, height=60)



# layout all of the main containers

mainwin.grid_columnconfigure(1, weight=1)

separator1_frame.grid(row=0, columnspan=2)
buton_frame.grid(row=1, column=0, sticky='nw')
input_frame.grid(row=1, column=1, sticky='nw',pady=13,padx=0)
separator2_frame.grid(row=2, columnspan=2)

aviable_frame.grid(row=3, columnspan=2, sticky='nw')
output_frame.grid(row=4, columnspan=2, sticky='nw')
footer_frame.grid(row=5, columnspan=2, sticky='nw')



# buton_frame content

bopenfile = Button(buton_frame, text="Open File", command=openfile,height=5, width=10, bg="PeachPuff3")
bopenfile.grid(row=0,pady=30,padx=30)





# input_frame content

Label(input_frame, text="").grid(row=0, column=0)


Label(input_frame, text="File name:",font="Helvetica 12").grid(row=1, column=0,sticky=W)
lfilename = Label(input_frame, text="",font="Helvetica 12 bold",padx=20)
lfilename.grid(row=1, column=1,sticky=W)



Label(input_frame, text="Format:",font="Helvetica 11").grid(row=2,column=0,sticky=E)
lfileformat = Label(input_frame, text="",font="Helvetica 11",padx=20)
lfileformat.grid(row=2,column=1,sticky=W)


Label(input_frame, text="Path:",font="Helvetica 10").grid(row=3,column=0,sticky=E)
lpath = Label(input_frame, text="",font="Helvetica 7",padx=20)
lpath.grid(row=3,column=1,sticky=W)



Label(input_frame, text="").grid(row=4, column=0)





# aviable_frame content
Label(aviable_frame, text="Available conversion :",width=45,bg='PeachPuff3',height=2,font="Helvetica 14 bold").grid(row=0, column=0)



#output frame content

# column layout
Label(output_frame, text="",width=15).grid(row=0,column=0)
Label(output_frame, text="",width=30).grid(row=0,column=1)
Label(output_frame, text="",width=30).grid(row=0,column=2)




# first descriptive column
Label(output_frame, text="Format:",font="Helvetica 10 bold").grid(row=1,column=0,sticky=E)
Label(output_frame, text="").grid(row=2,column=0)
Label(output_frame, text="Desription:",font="Helvetica 10 bold").grid(row=3,column=0,sticky=E)
Label(output_frame, text="").grid(row=4,column=0)
Label(output_frame, text="Convert with:",font="Helvetica 10 bold").grid(row=5,column=0,sticky=E)


# second convert column
outformat1 = Label(output_frame, text="",font="Helvetica 14")
outformat1.grid(row=1,column=1)

Label(output_frame, text="").grid(row=2,column=1)

outformat1popis  = Message(output_frame, text="\n\n\n",width=180)
outformat1popis.grid(row=3,column=1)

Label(output_frame, text="").grid(row=4,column=1)

ch_atrib1= IntVar()
check1_atr = Checkbutton(output_frame, text="attribut table  ", variable=ch_atrib1,state=DISABLED)
check1_atr.grid(row=5,column=1)

ch_color1= IntVar()
check1_col = Checkbutton(output_frame, text="color table      ", variable=ch_color1,state=DISABLED)
check1_col.grid(row=6,column=1)

ch_proj1= IntVar()
check1_proj = Checkbutton(output_frame, text="projection file", variable=ch_proj1,state=DISABLED)
check1_proj.grid(row=7,column=1)

ch_meta1= IntVar()
check1_meta = Checkbutton(output_frame, text="metadata       ", variable=ch_meta1,state=DISABLED)
check1_meta.grid(row=8,column=1)

Label(output_frame, text="").grid(row=9,column=1)

b_conv1 = Button(output_frame, text="Convert",height=5,width=12,state=DISABLED,bg="PeachPuff3")
b_conv1.grid(row=10,column=1)

Label(output_frame, text="").grid(row=11,column=1)
#end column 2



# third convert column
outformat2 = Label(output_frame, text="",font="Helvetica 14")
outformat2.grid(row=1,column=2)

Label(output_frame, text="").grid(row=2,column=2)

outformat2popis  = Message(output_frame, text="\n\n\n",width=200)
outformat2popis.grid(row=3,column=2)

Label(output_frame, text="").grid(row=4,column=2)

ch_atrib2= IntVar()
check2_atr = Checkbutton(output_frame, text="attribut table  ", variable=ch_atrib2,state=DISABLED)
check2_atr.grid(row=5,column=2)

ch_color2= IntVar()
check2_col = Checkbutton(output_frame, text="color table      ", variable=ch_color2,state=DISABLED)
check2_col.grid(row=6,column=2)

ch_proj2= IntVar()
check2_proj = Checkbutton(output_frame, text="projection file", variable=ch_proj2,state=DISABLED)
check2_proj.grid(row=7,column=2)

ch_meta2= IntVar()
check2_meta = Checkbutton(output_frame, text="metadata       ", variable=ch_meta2,state=DISABLED)
check2_meta.grid(row=8,column=2)

Label(output_frame, text="").grid(row=9,column=2)

b_conv2 = Button(output_frame, text="Convert",height=5,width=12,state=DISABLED,bg="PeachPuff3")
b_conv2.grid(row=10,column=2)

Label(output_frame, text="").grid(row=11,column=2)
Label(output_frame, text="").grid(row=12,column=2)
#end third column




mainwin.mainloop()