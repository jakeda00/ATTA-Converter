import tkMessageBox
from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename, askdirectory
from pathlib import Path
import os
from PIL import ImageTk


# START -- function definitions:

def cross():

    # own definition of cross button

    if tkMessageBox.askokcancel(u"Quit ATTA Convertor ?", "Are you sure you want to close the program ?"):
        mainwin.quit()

def workwin_open():

    # initialization "conversion in progress" window

    global workwin
    workwin = Toplevel(mainwin)
    workwin.resizable(0, 0)
    workwin.overrideredirect(True)  # can not see a toolbar

    w = 250
    h = 200

    # get screen width and height
    ws = mainwin.winfo_screenwidth()  # width of the screen
    hs = mainwin.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the "conversion in progress" window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    # locate "conversion in progress" window to center of screen
    workwin.geometry('+%d+%d' % (x, y))

    # create and layout all of the "conversion in progress" window containers
    sep_frame = Frame(workwin, bg='saddle brown', width=250, height=10)
    work_frame = Frame(workwin, width=200, height=180)
    sep2_frame = Frame(workwin, bg='saddle brown', width=250, height=10)
    sep_frame.grid(row=0)
    work_frame.grid(row=1)
    sep2_frame.grid(row=2)

    # lists the "Conversion in progress ..."
    Label(work_frame, text="Conversion in progress ...",padx=25,pady=35,bg='PeachPuff3',font="Helvetica 12 bold").grid(row=0, column=0)

def endofconv():

    # function at the end of the conversion ("conversion in progress" window destroy, ask to the next file)

    global workwin
    workwin.destroy()
    if tkMessageBox.askyesno(u"Convert another file?", "Are you want to convert some another file?"):
        new()




# work on this

def try_print_xml_to_csv(outputname):
    global inputname
    xmlfile=""
    xmlfile1 = Path(inputname+".aux.xml")
    xmlfile2 = Path(inputname+".xml")
    if xmlfile1.is_file():
        xmlfile = inputname+".aux.xml"
    elif xmlfile2.is_file():
        xmlfile = inputname+".xml"
    if xmlfile != "":

        #print "yes"
        import xml.etree.ElementTree as ET
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        #print root.tag

        level = 0

        for child in root:
            if level < 1:
                level = 1
            for child2 in child:
                if level < 2:
                    level = 2
                for child3 in child2:
                    if level < 3:
                        level = 3
                    for child4 in child3:
                        if level < 4:
                            level = 4
                        for child5 in child4:
                            if level < 5:
                                level = 5

        hlavicka = "root;"

        for i in range(1, level + 1):
            hlavicka = hlavicka + "level " + str(i) + ";"

        #print hlavicka

        csvfile = outputname + ".csv"
        csv = open(csvfile, "w")
        csv.write(hlavicka + "\n")
        csv.write(root.tag)
        if len(root.attrib) > 0:
            csv.write(str(root.attrib))
        if root.text != None:
            roottext = ''.join(root.text.split())
            #print roottext
            if len(roottext) > 0:
                rtext = roottext.replace(";", ",")
                csv.write(rtext)

        for i in range(0, level + 1):
            csv.write(";")
        csv.write("\n")

        for child in root:
            #print child.tag, child.attrib, child.text
            csv.write(";" + child.tag)
            if len(child.attrib) > 0:
                csv.write(": " + str(child.attrib))
            if child.text != None:
                childtext = ''.join(child.text.split())
                if len(childtext) > 0:
                    text = childtext.replace(";", ",")
                    csv.write(": " + text)

            for i in range(1, level + 1):
                csv.write(";")
            csv.write("\n")
            for child2 in child:
                #print child2.tag, child2.attrib, child2.text
                csv.write(";;" + child2.tag)
                if len(child2.attrib) > 0:
                    csv.write(": " + str(child2.attrib))
                if child2.text != None:
                    child2text = ''.join(child2.text.split())
                    if len(child2text) > 0:
                        text2 = child2text.replace(";", ",")
                        csv.write(": " + text2)
                for i in range(2, level + 1):
                    csv.write(";")
                csv.write("\n")
                for child3 in child2:
                    #print child3.attrib, child3.tag, child3.text
                    csv.write(";;;" + child3.tag)
                    if len(child3.attrib) > 0:
                        csv.write(": " + str(child3.attrib))
                    if child3.text != None:
                        child3text = ''.join(child3.text.split())
                        if len(child3text) > 0:
                            text3 = child3text.replace(";", ",")
                            csv.write(": " + text3)
                    for i in range(3, level + 1):
                        csv.write(";")
                    csv.write("\n")
                    for child4 in child3:
                        #print child4.attrib, child4.tag, child4.text
                        csv.write(";;;;" + child4.tag)
                        if len(child4.attrib) > 0:
                            csv.write(": " + str(child4.attrib))
                        if child4.text != None:
                            child4text = ''.join(child4.text.split())
                            if len(child4text) > 0:
                                text4 = child4text.replace(";", ",")
                                csv.write(": " + text4)
                        for i in range(4, level + 1):
                            csv.write(";")
                        csv.write("\n")
                        for child5 in child4:

                            csv.write(";;;;;" + child5.tag)
                            if len(child5.attrib) > 0:
                                csv.write(": " + str(child5.attrib))
                            if child5.text != None:
                                child5text = ''.join(child5.text.split())
                                if len(child5text) > 0:
                                    text5 = child5text.replace(";", ",")
                                    csv.write(": " + text5)
                            for i in range(5, level + 1):
                                csv.write(";")
                            csv.write("\n")

def ref_syst_change_rst(outputname):
    global inputname
    rdcfile=""
    projfile=""
    prjfile1 = inputname.split(".")
    prjfile = Path(prjfile1[0] + ".prj")
    reffile1 = outputname.split(".")
    reffile = Path(reffile1[0] + ".rdc")

    if reffile.is_file():
        rdcfile= reffile1[0] + ".rdc"
    if prjfile.is_file():
        projfile = prjfile1[0] + ".prj"

    if rdcfile != "" and projfile != "":
        refsystem=""
        prjOpen = open(projfile, "r")

        chain = prjOpen.read()

        items = chain.split(",")

        for row in items:

            if '_UTM' in row or '_utm' in row:
                #print "JOJOJOJOJO"
                utmzone = row.split('Zone_')
                utmLower = utmzone[1].lower()
                refutm = utmLower.split('"')

                refsystem = 'utm-' + refutm[0]
            elif 'WGS' in row or 'wgs' in row:
                refsystem = "latlong"
            elif 'LAMBERT' in row or 'lambert' in row:
                refsystem = "spc83nc1"               # print refsystem

        rdcOpen = open(rdcfile, "r")

        file2 = rdcOpen.readlines()
        rdccreate = open("output2.rdc", "w")

        for row2 in file2:

            if 'ref. system' in row2:
                #print 'ref. system : ' + refsystem + '\n'
                rdccreate.write('ref. system : ' + refsystem + '\n')
            else:
               # print row2
                rdccreate.write(row2)

        rdccreate.close()
        prjOpen.close()
        rdcOpen.close()



        os.remove(rdcfile)
        os.rename("output2.rdc", rdcfile)

def change_nodata_value_asc(outputname):
    global inputname
    rdcfile = ""
    ascfile = ""
    inxmlfile = ""
    outxmlfile = ""
    rdcfile1 = inputname.split(".")
    rdcfile2 = Path(rdcfile1[0] + ".rdc")
    ascfile1 = outputname.split(".")
    ascfile2 = Path(ascfile1[0] + ".asc")
    inxmlfile1 = Path(inputname + ".xml")
    inxmlfile2 = Path(inputname + ".aux.xml")
    outxmlfile1 = Path(outputname + ".xml")
    outxmlfile2 = Path(outputname + ".aux.xml")
    if rdcfile2.is_file():
        rdcfile = rdcfile1[0] + ".rdc"
    if ascfile2.is_file():
        ascfile = ascfile1[0] + ".asc"
    if inxmlfile1.is_file():
        inxmlfile = inputname + ".xml"
    if inxmlfile2.is_file():
        inxmlfile = inputname + ".aux.xml"
    if outxmlfile1.is_file():
        outxmlfile = outputname + ".xml"
    if outxmlfile2.is_file():
        outxmlfile = outputname + ".aux.xml"

    if rdcfile != "" and ascfile != "" and inxmlfile != "" and outxmlfile != "":
        rdcopen = open(rdcfile, "r")

        chain = rdcopen.read()
        items = chain.split("\n")
        rdcopen.close()

        hlpfl = 0

        for row in items:
            if 'min. value' in row:
                minval = row.split(': ')

                if minval[1] == '0':
                    hlpfl = hlpfl + 1
            elif 'flag value' in row:
                flagval = row.split(': ')
                if flagval[1] == '0':
                    hlpfl = hlpfl + 1

        if hlpfl == 2:

            ascopen = open(ascfile, "r")

            chain2 = ascopen.read()
            items2 = chain2.split("\n")
            ascopen.close()

            asccreate = open("file.asc", "w")

            for row2 in items2:
                if 'NODATA_value 0' in row2:
                    asccreate.write('NODATA_value -9999\n')
                else:
                    asccreate.write(row2 + '\n')

            asccreate.close()

            import xml.etree.ElementTree as ET
            tree = ET.parse(outxmlfile)
            root = tree.getroot()
           # print root.tag

            for child in root:
                #print child.tag, child.attrib
                for child2 in child:
                    #print child2.tag, child2.attrib
                    for child3 in child2:
                        #print child3.attrib, child3.tag, child3.text

                        if 'STATISTICS_MINIMUM' in child3.attrib['key']:
                            child3.text = '0'

            newtree = ET.ElementTree(root)
            newtree.write("2file.xml")



            os.remove(ascfile)
            os.rename("file.asc", ascfile)
            os.remove(outxmlfile)
            os.rename("2file.xml", outxmlfile)

def try_acces_to_dbf(outputname):
    global inputname
    dbfile=""
    accessfile1 = inputname.split(".")
    accdbfile = Path(accessfile1[0] + ".accdb")
    mdbfile = Path(accessfile1[0] + ".mdb")

    if accdbfile.is_file():
        dbfile = accessfile1[0] + ".accdb"
    elif mdbfile.is_file():
        dbfile = accessfile1[0] + ".mdb"

    if dbfile != "":
        import pyodbc
        from dbfpy import dbf as dbfpy_dbf
        import string
        import dbf
        from glob import glob

        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ='+dbfile+';'
        )
        cnxn = pyodbc.connect(conn_str)
        crsr = cnxn.cursor()

        i = 0
        for table in crsr.tables(tableType='TABLE'):
            i = i + 1
            if i == 1:
                tname = table[2]

        cname = []
        if 'tname' in locals():
            for column in crsr.columns(table=tname):
                cname.append(column.column_name)

            rows = crsr.execute("select * from " + tname).fetchall()

            cnxn.close()

            array = []
            dbffile2 = outputname.split(".")
            dbffile3 = dbffile2[0] + ".dbf"
            for dbf_file in glob(dbffile3):
                with dbf.Table(dbf_file) as table:
                    for record in table:
                        #print record
                        strrec = str(record)
                        recsplit = strrec.split(":")
                        array.append(float(recsplit[1]))

            db = dbfpy_dbf.Dbf("dbfile.dbf", new=True)
            hlpfl = 0
            for col in cname:
                col = str(col)
                if hlpfl == 0:
                    db.addField((col, "N", 12, 0))
                    hlpfl = hlpfl + 1
                else:
                    #print type(rows[1][hlpfl])
                    if type(rows[1][hlpfl]).__name__ == 'unicode':
                        db.addField((col, "C", 64))
                        hlpfl = hlpfl + 1
                    elif type(rows[1][hlpfl]).__name__ == 'int':
                        db.addField((col, "N", 12, 0))
                        hlpfl = hlpfl + 1

            rec = db.newRecord()

            countinarray = 0

            for recs in array:
                rec = db.newRecord()

                data = array[countinarray]
                for row in rows:
                    hlpfl = 0
                    for colname in db.fieldNames:
                        if type(row[hlpfl]).__name__ == 'unicode':
                            printable = set(string.printable)
                            data3 = filter(lambda x: x in printable, row[hlpfl])

                            if data == row[hlpfl - 1]:
                                data2 = data3
                        hlpfl = hlpfl + 1

                rec[db.fieldNames[0]] = data
                rec[db.fieldNames[1]] = data2
                rec.store()
                countinarray = countinarray + 1


            db.close()


            os.remove(dbffile3)
            os.rename("dbfile.dbf", dbffile3)

# edn work part




def idrirast():

    # function to convert into a RST format file

    global workwin
    # call "conversion in progress" window
    workwin_open()
    outputname = asksaveasfilename(parent=workwin, filetypes=[('Idrisi Raster Format', '*.rst')], defaultextension=".rst")
    if (outputname != ""):
        status = try_convert_raster(outputname, 'RST')
        if status[0] == "Done!":
            ref_syst_change_rst(outputname)
            tkMessageBox.showinfo(status[0],status[1])
        else:
            tkMessageBox.showwarning(status[0],status[1])
    endofconv()

def ascirast():

    # function to convert into a ASCII raster format file

    global workwin
    workwin_open()
    outputname = asksaveasfilename(parent=workwin, filetypes=[('ARC/INFO ASCII GRID', '*.asc')], defaultextension=".asc")
    if (outputname != ""):
        status = try_convert_raster(outputname, 'AAIGrid')
        if status[0] == "Done!":
            change_nodata_value_asc(outputname)
            try_print_xml_to_csv(outputname)
            tkMessageBox.showinfo(status[0],status[1])
        else:
            tkMessageBox.showwarning(status[0],status[1])
    endofconv()

def tifrast():

    # function to convert into a GeoTIFF format file

    global workwin
    workwin_open()
    outputname = asksaveasfilename(parent=workwin, filetypes=[('GeoTIFF', '*.tif')], defaultextension=".tif")
    if (outputname != ""):
        status = try_convert_raster(outputname, 'GTiff')
        if status[0] == "Done!":
            try_print_xml_to_csv(outputname)
            tkMessageBox.showinfo(status[0],status[1])
        else:
            tkMessageBox.showwarning(status[0],status[1])
    endofconv()


def try_convert_raster(outputname,driver):

    # function to try convert raster

    try:
        convert_raster(outputname, driver)
    except Exception, error:
        errmes = error.message
    finally:
        if 'errmes' in locals():
            #print errmes
            text = ["Error!", "The raster file hasn't been converted.\n\n"+errmes]
        else:
            if driver == 'AAIGrid':
                driver= 'ASCII Grid'
            elif driver == 'Gtiff':
                driver= 'GeoTIFF'
            text = ["Done!", "The raster file has been converted. \n\nNew "+driver+" file is saved as:\n\n"+outputname]
        return text

def convert_raster(outputname, format):

    # function to convert raster with GDAL

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

    # function to convert into a Shapefile format

    global workwin
    workwin_open()
    outputname = asksaveasfilename(parent=workwin, filetypes=[('Esri Shapefile', '*.shp')], defaultextension=".shp")
    if (outputname != ""):
        status = try_convert_vector(outputname, 'ESRI Shapefile')
        if status[0] == "Done!":
            try_acces_to_dbf(outputname)
            tkMessageBox.showinfo(status[0],status[1])
        else:
            tkMessageBox.showwarning(status[0],status[1])
    endofconv()

def gmlvect():

    # function to convert into a GML format file

    global workwin
    workwin_open()
    outputname = asksaveasfilename(parent=workwin, filetypes=[('Geography Markup Language', '*.gml')], defaultextension=".gml")
    if (outputname != ""):
        status = try_convert_vector(outputname, 'GML')
        if status[0] == "Done!":
            try_print_xml_to_csv(outputname)
            tkMessageBox.showinfo(status[0],status[1])
        else:
            tkMessageBox.showwarning(status[0],status[1])
    endofconv()

def jsonvect():

    # function to convert into a GeoJSON format file

    global workwin
    workwin_open()
    outputname = asksaveasfilename(parent=workwin, filetypes=[('GeoJSON files', '*.geojson')],
                                   defaultextension=".geojson")
    if (outputname != ""):
        status = try_convert_vector(outputname, 'GeoJSON')
        if status[0] == "Done!":

            tkMessageBox.showinfo(status[0], status[1])
        else:
            tkMessageBox.showwarning(status[0], status[1])
    endofconv()


def try_convert_vector(outputname, driver):

    # function to try convert vectors with ogr2ogr

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
            text = ["Done!", "The vector file has been converted. \n\nNew "+driver+" is saved as:\n\n"+outputname]
        else:
            if 'errmes' in locals():
                text = ["Error!", "The vector file hasn't been converted.\n\n" + errmes]
            else:
                text = ["Error!", "The vector file hasn't been converted.\n\nSome unknown error."]
        return text






def openfile():

    # functions to retrieve the input file

    global inputname, lfilename, bopenfile
    if (inputname == ""):
        inputname = askopenfilename(parent=mainwin, **FILEOPENOPTIONS)
        if (inputname != ""):
            #print "opening file..."
            filetype = inputname.split(".")
            filename = inputname.split("/")
            ftype = filetype[len(filetype) - 1]
            fname = filename[len(filename) - 1]
            bopenfile.config(state=DISABLED)
            lfilename.config(text=fname)
            lfilename.config(bg="PeachPuff3")
            lpath.config(text=inputname)
            lpath.config(bg="PeachPuff3")


            # filling options in the GUI form by input file
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
                outformat1.config(text="GeoJSON")
                outformat1popis.config(text="GeoJSON is an open standard format designed for representing simple geographical features.")
                b_conv1.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nGeoJSON", command=jsonvect)
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
                outformat2.config(text="GeoJSON")
                outformat2popis.config(
                    text="GeoJSON is an open standard format designed for representing simple geographical features.")
                b_conv2.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nGeoJSON", command=jsonvect)
            elif ftype == 'gml':
                lfileformat.config(text="Geography Markup Language", bg="PeachPuff3")
                outformat1.config(text="Esri Shapefile")
                outformat1popis.config(
                    text="A popular geospatial vector data format for GIS software. It is developed and regulated by Esri and used by ArcGIS.")
                b_conv1.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nEsri Shapefile", command=shpvect)
                outformat2.config(text="GeoJSON")
                outformat2popis.config(text="GeoJSON is an open standard format designed for representing simple geographical features.")
                b_conv2.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nGeoJSON", command=jsonvect)
            elif ftype == 'geojson' or ftype == 'json':
                lfileformat.config(text="GeoJson", bg="PeachPuff3")
                outformat1.config(text="Esri Shapefile")
                outformat1popis.config(
                    text="A popular geospatial vector data format for GIS software. It is developed and regulated by Esri and used by ArcGIS.")
                b_conv1.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nEsri Shapefile", command=shpvect)
                outformat2.config(text="Geography Markup Language")
                outformat2popis.config(
                    text="GML is the XML grammar defined by the Open Geospatial Consortium (OGC) to express geographical features.")
                b_conv2.config(state=ACTIVE, bg="PeachPuff3", text="Convert\n to \nGML", command=gmlvect)

            #print "file open!"


def new():

    # fnc for open new file
    # cleanup variables, changing GUI form to default settings

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
        #print "new file..."


def about():

    # display "about" window

    global aboutopen

    def crosss():

        # own definition of cross button

        global aboutopen, abouttext
        global subwin2
        aboutopen = 0
        subwin.destroy()
        if 'subwin2' in globals():
            abouttext = 0
            subwin2.destroy()

    def viewxmittext():

        # display X/MIT full licence text

        global abouttext
        global subwin2

        if abouttext == 0:

            subwin2 = Toplevel(mainwin)
            subwin2.title("X/MIT License text")
            subwin2.resizable(0, 0)


            w = 430
            h = 425

            # get screen width and height
            ws = mainwin.winfo_screenwidth()  # width of the screen
            hs = mainwin.winfo_screenheight()  # height of the screen

            # calculate x and y coordinates for the Tk root window
            x = (ws / 2) - (w / 2)
            y = (hs / 2) - (h / 2)

            # locate "about" window to center of screen
            subwin2.geometry('+%d+%d' % (x, y))
            subwin2.iconbitmap('Icon.ico')

            abouttext = 1

            sep_frame = Frame(subwin2, bg='saddle brown', width=438, height=10)
            leftsep_frame = Frame(subwin2, bg='saddle brown', width=6, height=393)
            about_frame = Frame(subwin2, width=430, height=180, bg='PeachPuff3')
            rightsep_frame = Frame(subwin2, bg='saddle brown', width=6, height=393)
            sep2_frame = Frame(subwin2, bg='saddle brown', width=438, height=10)
            sep_frame.grid(row=0, columnspan=3)
            leftsep_frame.grid(row=1, column=0)
            about_frame.grid(row=1, column=1)
            rightsep_frame.grid(row=1, column=2)
            sep2_frame.grid(row=2, columnspan=3)

            Label(about_frame, text="", font="Helvetica 4", bg='PeachPuff3').grid(row=0, column=0)
            Label(about_frame, text="License:", font='Helvetica 12 bold', bg='PeachPuff3').grid(row=1, column=0, sticky=E)
            Label(about_frame, text="X/MIT", font='Helvetica 12', bg='PeachPuff3').grid(row=1, column=1, sticky=W)
            Label(about_frame, text="\n", font="Helvetica 4", bg='PeachPuff3').grid(row=2, column=0)
            Label(about_frame, text="Copyright (c) 2017 David Jakes", font='Helvetica 8 bold', width=60, bg='PeachPuff3').grid(row=3,
                                                                                                               columnspan=2)
            Label(about_frame, text="", font="Helvetica 4", bg='PeachPuff3').grid(row=4, column=0)

            Message(about_frame,
                    text="Permission is hereby granted, free of charge, to any person\nobtaining a copy of this software and associated documentation\nfiles (the \"Software\"), to deal in the Software without\nrestriction, including without limitation the rights to use,\ncopy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the\nSoftware is furnished to do so, subject to the following\nconditions:",
                    font='Helvetica 8', width=400, bg='PeachPuff3').grid(row=5, columnspan=2)
            Label(about_frame, text="", font="Helvetica 4", bg='PeachPuff3').grid(row=6, column=0)
            Message(about_frame,
                    text="The above copyright notice and this permission notice shall be\nincluded in all copies or substantial portions of the Software.",
                    font='Helvetica 8', width=400, bg='PeachPuff3').grid(row=7, columnspan=2)
            Label(about_frame, text="", font="Helvetica 4", bg='PeachPuff3').grid(row=8, column=0)
            Message(about_frame,
                    text="THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND,\nEXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES\nOF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND\nNONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT\nHOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,\nWHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING\nFROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR\nOTHER DEALINGS IN THE SOFTWARE.",
                    font='Helvetica 8', width=400, bg='PeachPuff3').grid(row=9, columnspan=2)
            Label(about_frame, text="", font="Helvetica 4", bg='PeachPuff3').grid(row=10, column=0)

            def on_focus_out(event):

                # call when subwin2 lost focus

                global abouttext
                abouttext = 0
                subwin2.destroy()

            # set focus
            subwin2.focus_set()
            # call on_focus_out, when Button 1 is pressed on subwin2
            subwin2.bind('<Button-1>', on_focus_out)
            # call on_focus_out, when subwin2 lost focus
            subwin2.bind('<FocusOut>', on_focus_out)


    if aboutopen == 0:
        subwin = Toplevel(mainwin)
        subwin.title("About ATTA Convertor")
        subwin.resizable(0, 0)

        w = 426
        h = 470

        # get screen width and height
        ws = mainwin.winfo_screenwidth()  # width of the screen
        hs = mainwin.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # locate "about" window to center of screen
        subwin.geometry('+%d+%d' % (x, y))

        #set window icon
        subwin.iconbitmap('Icon.ico')

        #set what happens when pressing the cross
        subwin.protocol("WM_DELETE_WINDOW", crosss)

        aboutopen = 1

        # create and layout all of the "about" window containers
        sep_frame = Frame(subwin, bg='saddle brown', width=426, height=10)
        leftsep_frame = Frame(subwin, bg='saddle brown', width=6, height=267)
        about_frame = Frame(subwin, width=430, height=180, bg='PeachPuff3')
        rightsep_frame = Frame(subwin, bg='saddle brown', width=6, height=267)
        centersep_frame = Frame(subwin, bg='saddle brown', width=426, height=5)
        about_frame2 = Frame(subwin, width=430, height=180)
        sep2_frame = Frame(subwin, bg='saddle brown', width=426, height=10)
        sep_frame.grid(row=0,columnspan=3)
        leftsep_frame.grid(row=1,column=0)
        about_frame.grid(row=1,column=1)
        rightsep_frame.grid(row=1,column=2)
        centersep_frame.grid(row=2,columnspan=3)
        about_frame2.grid(row=3,columnspan=3)
        sep2_frame.grid(row=4,columnspan=3)


        # set texts in "about" window
        Label(about_frame, text="", font="Helvetica 4", bg='PeachPuff3').grid(row=0, column=0)

        Label(about_frame, text="Author:",font='Helvetica 12 bold', bg='PeachPuff3').grid(row=1, column=0, sticky=E)
        Label(about_frame, text="David Jakes",font='Helvetica 12', bg='PeachPuff3').grid(row=1, column=1, sticky=W)
        Label(about_frame, text="\n", font="Helvetica 4", bg='PeachPuff3').grid(row=2, column=0)
        Message(about_frame, text="Program was developed within the bachelor thesis on Palacky University Olomouc.",font='Helvetica 8',width=300, bg='PeachPuff3').grid(row=3,columnspan=2)
        Label(about_frame, text="", font="Helvetica 4", bg='PeachPuff3').grid(row=4, column=0)
        Label(about_frame, text="Name of bachelor thesis:", font='Helvetica 8 bold', bg='PeachPuff3').grid(row=5, columnspan=2)
        Label(about_frame, text="Program for reversible data conversion between ArcGIS a TerrSet", font='Helvetica 8', bg='PeachPuff3',width=68).grid(row=6, columnspan=2)
        Label(about_frame, text="\n", font="Helvetica 4", bg='PeachPuff3').grid(row=7, column=0)
        Label(about_frame, text="TerrSet and IDRISI are trademarks and registered trademarks\n respectively of Clark University.Windows and Access are trademarks \nof Microsoft Corporation. ArcGIS and its related components\n are trademarks of Esri, Inc. Other companies and products or services\n mentioned herein may be tradearks, service marks, or registered marks \nof their respective marks owner.", font='Helvetica 8', bg='PeachPuff3', width=68).grid(row=8, columnspan=2)
        Label(about_frame, text="\n", font="Helvetica 4", bg='PeachPuff3').grid(row=9, column=0)

        Label(about_frame2, text="", font="Helvetica 4").grid(row=0, column=0)
        Label(about_frame2, text="License:", font='Helvetica 12 bold').grid(row=1, column=0, sticky=E)
        Label(about_frame2, text="X/MIT", font='Helvetica 12').grid(row=1, column=1, sticky=W)
        Label(about_frame2, text="\n", font="Helvetica 4").grid(row=2, column=0)
        Label(about_frame2, text="Copyright (c) 2017 David Jakes", font='Helvetica 8 bold',width=60).grid(row=3, columnspan=2)
        Label(about_frame2, text="", font="Helvetica 4").grid(row=4, column=0)
        Button(about_frame2, text="View X/MIT licension text",command=viewxmittext, bg="PeachPuff3").grid(row=5, columnspan=2)
        Label(about_frame2, text="", font="Helvetica 4").grid(row=6, column=0)

        subwin.focus_set()

def formats():
    print "formats"


def manual():
    print "manual"


def radio():
    global rad1,rad2
    selection = inputdriver.get()
    for item in rad2:
        item.config(state=DISABLED)
    if selection == 'asc':
        rad2[1].config(state=NORMAL)
        rad2[2].config(state=NORMAL)
        rad2[1].select()
    elif selection == "rst":
        rad2[0].config(state=NORMAL)
        rad2[2].config(state=NORMAL)
        rad2[0].select()
    elif selection == "tif":
        rad2[0].config(state=NORMAL)
        rad2[1].config(state=NORMAL)
        rad2[0].select()
    elif selection == "shp":
        rad2[4].config(state=NORMAL)
        rad2[5].config(state=NORMAL)
        rad2[4].select()
    elif selection == "vct":
        rad2[3].config(state=NORMAL)
        rad2[4].config(state=NORMAL)
        rad2[5].config(state=NORMAL)
        rad2[3].select()
    elif selection == "gml":
        rad2[3].config(state=NORMAL)
        rad2[4].config(state=NORMAL)
        rad2[3].select()
    elif selection == "json":
        rad2[3].config(state=NORMAL)
        rad2[5].config(state=NORMAL)
        rad2[3].select()



def create_batch_win():

    global batchopen, batchwin, rad1, rad2, b_conv_batch, outputdriver, inputdriver, b_folder, folder1, convico

    def crosss():
    # own definition of cross button

        global batchopen, batchwin, rad1, rad2, inputdir, inputname, b_conv_batch
        batchopen = 0

        rad1 = []

        rad2 = []
        inputdir = ""
        inputname = ""
        b_conv_batch.config(state=DISABLED)
        batchwin.destroy()
        print "destroy"


    if batchopen == 0:
        batchwin = Toplevel(mainwin)
        batchwin.title("Batch - Convert multiple files - ATTA Convertor")
        batchwin.resizable(0, 0)

        w = 560
        h = 630

        # get screen width and height
        ws = mainwin.winfo_screenwidth()  # width of the screen
        hs = mainwin.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # locate "about" window to center of screen
        batchwin.geometry('+%d+%d' % (x, y))



        # set what happens when pressing the cross
        batchwin.protocol("WM_DELETE_WINDOW", crosss)

        # set window icon
        batchwin.iconbitmap('Icon.ico')

        batchopen = 1

        # create and layout all of the "about" window containers
        sep_frame = Frame(batchwin, bg='saddle brown', width=558, height=10)
        leftsep_frame = Frame(batchwin, bg='saddle brown', width=6, height=575)
        head_frame= Frame(batchwin, width=563, height=40)
        folder_frame = Frame(batchwin, width=563, height=50)
        sep3_frame = Frame(batchwin, bg='saddle brown', width=510, height=2)
        batch_frame = Frame(batchwin, width=350, height=50, bg='PeachPuff3')
        rightsep_frame = Frame(batchwin, bg='saddle brown', width=6, height=575)
        sep2_frame = Frame(batchwin, bg='saddle brown', width=558, height=10)

        sep_frame.grid(row=0, columnspan=3)
        leftsep_frame.grid(row=1, column=0,rowspan=4,sticky=W)
        head_frame.grid(row=1, column=1)
        rightsep_frame.grid(row=1, column=2,rowspan=4,sticky=E)
        folder_frame.grid( column=1, row=2, sticky=W,padx=15)
        sep3_frame.grid(row=3, columnspan=3)
        batch_frame.grid( column=1, row=4)

        sep2_frame.grid(row=5, columnspan=3)



        Label(head_frame, text="Convert batch / multiple files", width=55, bg='PeachPuff3', font="Helvetica 11 bold").grid(row=0)



        Label(folder_frame, text="", font="Helvetica 10").grid(row=0, column=0)

        global ficon, arrowico
        #img3 = ImageTk.PhotoImage(Image.open("./images/close.gif"))

        #img1 = ImageTk.PhotoImage(...)
       # c1 = Button(...)
        #c1.image = img1




        b_folder = Button(folder_frame, text="Choose directory", height=90, width=90, command=choosedir, bg="PeachPuff3", image=ficon, compound=TOP)
        b_folder.grid(row=1, column=0,sticky=W,padx=10)
        Label(folder_frame, text="Folder path:  ", font="Helvetica 10 bold",pady=10,padx=10).grid(row=1, column=1,sticky=W)
        folder1 = Message(folder_frame, text="", font="Helvetica 9", padx=10, width=270, pady=5)
        folder1.grid(row=1, column=2, sticky=W)

        Label(folder_frame, text="", font="Helvetica 10").grid(row=2, column=0)
        Label(folder_frame, text="", font="Helvetica 10").grid(row=2, column=0)






        Label(batch_frame, text="", font="Helvetica 10", bg="PeachPuff3").grid(row=0, column=0)
        Label(batch_frame, text="Original file type", font="Helvetica 10 bold", bg="PeachPuff3").grid(row=1, column=0)
        Label(batch_frame, text="", font="Helvetica 20 bold", bg="PeachPuff3", image=arrowico).grid(row=1, column=1, rowspan=10)
        Label(batch_frame, text="New file type", font="Helvetica 10 bold", bg="PeachPuff3").grid(row=1, column=2)
        Label(batch_frame, text="", font="Helvetica 10", bg="PeachPuff3").grid(row=2, column=0)


        inputdriver = StringVar()

        rad1.append(Radiobutton(batch_frame, text="ASCII grid (*.asc)", variable=inputdriver, value="asc", state=DISABLED,command=radio, bg="PeachPuff3",padx=20,pady=5))
        rad1[0].grid(row=3,column=0,sticky=W)
        rad1.append(Radiobutton(batch_frame, text="Idrisi Raster file (*.rst)", variable=inputdriver, value="rst", state=DISABLED,command=radio, bg="PeachPuff3",padx=20,pady=5))
        rad1[1].grid(row=4,column=0,sticky=W)
        rad1.append(Radiobutton(batch_frame, text="GeoTIFF (*.tif)", variable=inputdriver, value="tif", state=DISABLED,command=radio, bg="PeachPuff3",padx=20,pady=5))
        rad1[2].grid(row=5,column=0,sticky=W)
        rad1.append(Radiobutton(batch_frame, text="Esri Shapefile (*.shp)", variable=inputdriver, value="shp", state=DISABLED,command=radio, bg="PeachPuff3",padx=20,pady=5))
        rad1[3].grid(row=6,column=0,sticky=W)
        rad1.append(Radiobutton(batch_frame, text="Idrisi Vector file (*.vct)", variable=inputdriver, value="vct", state=DISABLED,command=radio, bg="PeachPuff3",padx=20,pady=5))
        rad1[4].grid(row=7,column=0,sticky=W)
        rad1.append(Radiobutton(batch_frame, text="GeoJSON (*.json, *.geojson)", variable=inputdriver, value="json", state=DISABLED,command=radio, bg="PeachPuff3",padx=20,pady=5))
        rad1[5].grid(row=8,column=0,sticky=W)
        rad1.append(Radiobutton(batch_frame, text="Geography Markup Language (*.gml)", variable=inputdriver, value="gml", state=DISABLED,command=radio, bg="PeachPuff3",padx=20,pady=5))
        rad1[6].grid(row=9,column=0,sticky=W)

        outputdriver = StringVar()

        rad2.append(Radiobutton(batch_frame, text="ASCII grid (*.asc)", variable=outputdriver, value="AAIGrid", state=DISABLED, bg="PeachPuff3",padx=20,pady=5))
        rad2[0].grid(row=3, column=2,sticky=W)
        rad2.append(Radiobutton(batch_frame, text="Idrisi Raster file (*.rst)", variable=outputdriver, value="RST",state=DISABLED, bg="PeachPuff3",padx=20,pady=5))
        rad2[1].grid(row=4, column=2,sticky=W)
        rad2.append(Radiobutton(batch_frame, text="GeoTIFF (*.tif)", variable=outputdriver, value="GTiff", state=DISABLED, bg="PeachPuff3",padx=20,pady=5))
        rad2[2].grid(row=5, column=2,sticky=W)

        rad2.append(Radiobutton(batch_frame, text="Esri Shapefile (*.shp)", variable=outputdriver, value="Esri Shapefile",
                    state=DISABLED, bg="PeachPuff3",padx=20,pady=5))
        rad2[3].grid(row=6, column=2,sticky=W)
        rad2.append(Radiobutton(batch_frame, text="GeoJSON (*.json, *.geojson)", variable=outputdriver, value="GeoJSON",
                    state=DISABLED, bg="PeachPuff3",padx=20,pady=5))
        rad2[4].grid(row=7, column=2,sticky=W)
        rad2.append(Radiobutton(batch_frame, text="Geography Markup Language (*.gml)", variable=outputdriver, value="GML",
                    state=DISABLED, bg="PeachPuff3",padx=20,pady=5))
        rad2[5].grid(row=8, column=2,sticky=W)

        Label(batch_frame, text="", font="Helvetica 10", bg="PeachPuff3").grid(row=9, column=0)
        Label(batch_frame, text="", font="Helvetica 10", bg="PeachPuff3").grid(row=10, column=0)

        b_conv_batch = Button(batch_frame, text="Convert multiple files", command=convert_batch, state=DISABLED, pady=10,padx=10, image=convico,compound=TOP)
        b_conv_batch.grid(row=11, columnspan=3)
        Label(batch_frame, text="", font="Helvetica 10", bg="PeachPuff3").grid(row=12, column=0)


def choosedir():
    global inputdir,batchwin,rad1,rad2, b_conv_batch, b_folder, folder1
    if (inputdir == ""):
        inputdir = askdirectory(parent=batchwin)
        if (inputdir != ""):
            for item in rad1:
                item.config(state=NORMAL)
            rad1[0].select()
            rad2[1].config(state=NORMAL)
            rad2[1].select()
            rad2[2].config(state=NORMAL)
            b_folder.config(state=DISABLED)
            folder1.config(text=inputdir,bg="PeachPuff3")

            b_conv_batch.config(state=NORMAL)



           # rad1.config(state=ACTIVE)


def convert_batch():
    global workwin
    workwin_open()


    def crosss():
    # own definition of cross button

        global batchopen,batchwin,rad1,rad2,inputdir,inputname,b_conv_batch
        batchopen = 0


        rad1 = []

        rad2 = []
        inputdir = ""
        inputname= ""
        b_conv_batch.config(state=DISABLED)
        batchwin.destroy()
        print "destroy"

    global outputdriver, inputdriver, inputdir, batchwin, inputname, workwin
    
    #workwin.attributes("-topmost",True)

    if outputdriver == inputdriver:
        tkMessageBox.showwarning("Wrong choice !!!","Cant choose two same formats")
        batchwin.focus_set()
    else:
        countok = 0
        countfail = 0

        okarray = []
        failarray = []
        selection1 = inputdriver.get()
        selection2 = outputdriver.get()
        workwin_open()

        for filename in os.listdir(inputdir):
            if "." in filename:
                filetype = filename.split(".")

                if filetype [len(filetype)-1] == selection1:
                    inputname = inputdir +"/"+filename


                    if selection2 == "AAIGrid":
                        outputname = inputdir + "/" + filetype[0] + ".asc"
                        status = try_convert_raster(outputname, selection2)
                        if status[0] == "Done!":
                            change_nodata_value_asc(outputname)
                            try_print_xml_to_csv(outputname)
                            countok += 1
                            okarray.append(outputname)
                        else:
                            countfail += 1
                            failarray.append(outputname)

                    elif selection2 == "RST":
                        outputname = inputdir + "/" + filetype[0] + ".rst"
                        status = try_convert_raster(outputname, selection2)
                        if status[0] == "Done!":
                            ref_syst_change_rst(outputname)
                            countok += 1
                            okarray.append(outputname)
                        else:
                            countfail += 1
                            failarray.append(outputname)

                    elif selection2 == "GTiff":
                        outputname = inputdir + "/" + filetype[0] + ".tif"
                        status = try_convert_raster(outputname, selection2)
                        if status[0] == "Done!":
                            try_print_xml_to_csv(outputname)
                            countok += 1
                            okarray.append(outputname)
                        else:
                            countfail += 1
                            failarray.append(outputname)

                    elif selection2 == "Esri Shapefile":
                        outputname = inputdir + "/" + filetype[0] + ".shp"
                        status = try_convert_vector(outputname, selection2)
                        if status[0] == "Done!":
                            try_acces_to_dbf(outputname)
                            countok += 1
                            okarray.append(outputname)
                        else:
                            countfail += 1
                            failarray.append(outputname)

                    elif selection2 == "GeoJSON":
                        outputname = inputdir + "/" + filetype[0] + ".geojson"
                        status = try_convert_vector(outputname, selection2)
                        if status[0] == "Done!":

                            countok += 1
                            okarray.append(outputname)
                        else:
                            countfail += 1
                            failarray.append(outputname)

                    elif selection2 == "GML":
                        outputname = inputdir + "/" + filetype[0] + ".gml"
                        status = try_convert_vector(outputname, selection2)
                        if status[0] == "Done!":
                            try_print_xml_to_csv(outputname)
                            countok += 1
                            okarray.append(outputname)
                        else:
                            countfail += 1
                            failarray.append(outputname)

        convfiles = ""
        for one in okarray:
            convfiles = convfiles + one+"\n"
        nonconvfiles = ""
        for one in failarray:
            nonconvfiles = nonconvfiles + one + "\n"

        text = "Batch accomplished.\n\nSuccessufully converted files: "+str(countok)+"\n\n"
        if convfiles != "":
            text = text + "List of converted files:\n"+convfiles+"\n\n"
        text = text + "Unsuccessufully converted files: "+str(countfail)+"\n"
        if nonconvfiles != "":
            text = text + "List of non converted files:\n"+ nonconvfiles+"\n"

        crosss()

        tkMessageBox.showinfo("Conversions done", text)










# END -- function definitions



# definitions of globals variables
global inputname, lfilename, bopenfile, aboutopen, abouttext, workwin, batchopen,inputdir, rad1, rad2, b_conv_batch, outputdriver, inputdriver, ficon, arrowico, b_folder, folder1, convico

rad1=[]
rad2=[]



inputdir = ""
inputname = ""
aboutopen = 0
abouttext = 0
batchopen = 0

#definition of filetypes in askfile dialog
FILEOPENOPTIONS = dict(defaultextension='.shp',
                       filetypes=[('ATTA Convertor supported formats', '*.asc;*.rst;*.tif;*.shp;*.vct;*.gml;*.geojson;*.json')])


# initialize window
mainwin = Tk()

mainwin.title("ATTA Convertor")
mainwin.resizable(0, 0)

#set what happens when pressing the cross
mainwin.protocol("WM_DELETE_WINDOW", cross)

w = 555
h = 570

# get screen width and height
ws = mainwin.winfo_screenwidth() # width of the screen
hs = mainwin.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# locate main window to center of screen
mainwin.geometry('+%d+%d' % ( x, y))

#set window icon
mainwin.iconbitmap('Icon.ico')

# create menu
mainMenu = Menu(mainwin)

# create cascade menu for menu items (File)
menuFile = Menu(mainMenu, tearoff=0)
menuFile.add_command(label="New", command=new)
menuFile.add_command(label="Batch ...", command=create_batch_win)
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


#load icons
fileicon = ImageTk.PhotoImage(file="file.png")
ficon = ImageTk.PhotoImage(file="folder.png")
arrowico = ImageTk.PhotoImage(file="arrow24.png")
convico = ImageTk.PhotoImage(file="convert3.png")

# buton_frame content
bopenfile = Button(buton_frame, text="Open File", command=openfile, height=80, width=80, bg="PeachPuff3",image=fileicon,compound=TOP)
bopenfile.grid(row=0, pady=30, padx=30)


# input_frame content

Label(input_frame, text="", font="Helvetica 1").grid(row=0, column=0)

Label(input_frame, text="File name:  ", font="Helvetica 10 bold").grid(row=1, column=0, sticky=W)
lfilename = Message(input_frame, text="", font="Helvetica 10 bold", padx=10, width=290, pady=5)
lfilename.grid(row=1, column=1, sticky=W)

Label(input_frame, text="", font="Helvetica 1").grid(row=2, column=0)

Label(input_frame, text="Format:  ", font="Helvetica 10 bold").grid(row=3, column=0, sticky=E)
lfileformat = Label(input_frame, text="", font="Helvetica 10", padx=10, pady=5)
lfileformat.grid(row=3, column=1, sticky=W)

Label(input_frame, text="", font="Helvetica 1").grid(row=4, column=0)

Label(input_frame, text="Path:  ", font="Helvetica 10 bold").grid(row=5, column=0, sticky=E)
lpath = Message(input_frame, text="", font="Helvetica 8", padx=10, width=290, pady=5)
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



# second convert column

outformat1 = Label(output_frame, text="", font="Helvetica 10 bold")
outformat1.grid(row=1, column=1)

Label(output_frame, text="").grid(row=2, column=1)

outformat1popis = Message(output_frame, text="\n\n\n", width=180)
outformat1popis.grid(row=3, column=1)

Label(output_frame, text="").grid(row=4, column=1)
Label(output_frame, text="").grid(row=5, column=1)

b_conv1 = Button(output_frame, text="Convert", height=80, width=80, state=DISABLED, bg="PeachPuff3",image=convico, compound=TOP)
b_conv1.grid(row=6, column=1)

Label(output_frame, text="").grid(row=7, column=1)
# end column 2



# third convert column

outformat2 = Label(output_frame, text="", font="Helvetica 10 bold")
outformat2.grid(row=1, column=2)

Label(output_frame, text="").grid(row=2, column=2)

outformat2popis = Message(output_frame, text="\n\n\n", width=200)
outformat2popis.grid(row=3, column=2)

Label(output_frame, text="").grid(row=4, column=2)
Label(output_frame, text="").grid(row=5, column=2)

b_conv2 = Button(output_frame, text="Convert", height=80, width=80, state=DISABLED, bg="PeachPuff3",image=convico, compound=TOP)
b_conv2.grid(row=6, column=2)

Label(output_frame, text="").grid(row=7, column=2)
Label(output_frame, text="").grid(row=8, column=2)

# end third column




mainwin.mainloop()
