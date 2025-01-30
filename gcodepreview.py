#!/usr/bin/env python
#icon "C:\Program Files\PythonSCAD\bin\openscad.exe"  --trust-python
#Currently tested with PythonSCAD_nolibfive-2025.01.02-x86-64-Installer.exe and Python 3.11
#gcodepreview 0.8, for use with PythonSCAD,
#if using from PythonSCAD using OpenSCAD code, see gcodepreview.scad

import sys

# getting openscad functions into namespace
#https://github.com/gsohler/openscad/issues/39
try:
    from openscad import *
except ModuleNotFoundError as e:
    print("OpenSCAD module not loaded.")

# add math functions (using radians by default, convert to degrees where necessary)
import math

def pygcpversion():
    thegcpversion = 0.8
    return thegcpversion

class gcodepreview:

    def __init__(self, #basefilename = "export",
                 generatepaths = False,
                 generategcode = False,
                 generatedxf = False,
#                 stockXwidth = 25,
#                 stockYheight = 25,
#                 stockZthickness = 1,
#                 zeroheight = "Top",
#                 stockzero = "Lower-left" ,
#                 retractheight = 6,
#                 currenttoolnum = 102,
#                 toolradius = 3.175,
#                 plunge = 100,
#                 feed = 400,
#                 speed = 10000
                  ):
#        self.basefilename = basefilename
        if (generatepaths == 1):
            self.generatepaths = True
        if (generatepaths == 0):
            self.generatepaths = False
        else:
            self.generatepaths = generatepaths
        if (generategcode == 1):
            self.generategcode = True
        if (generategcode == 0):
            self.generategcode = False
        else:
            self.generategcode = generategcode
        if (generatedxf == 1):
            self.generatedxf = True
        if (generatedxf == 0):
            self.generatedxf = False
        else:
            self.generatedxf = generatedxf
#        self.stockXwidth = stockXwidth
#        self.stockYheight = stockYheight
#        self.stockZthickness = stockZthickness
#        self.zeroheight = zeroheight
#        self.stockzero = stockzero
#        self.retractheight = retractheight
#        self.currenttoolnum = currenttoolnum
#        self.toolradius = toolradius
#        self.plunge = plunge
#        self.feed = feed
#        self.speed = speed
#        global toolpaths
#        if (openscadloaded == True):
#            self.toolpaths = cylinder(0.1, 0.1)
        self.generatedxfs = False

    def checkgeneratepaths():
        return self.generatepaths

#    def myfunc(self, var):
#        self.vv = var * var
#        return self.vv
#
#    def getvv(self):
#        return self.vv
#
#    def checkint(self):
#        return self.mc
#
#    def makecube(self, xdim, ydim, zdim):
#        self.c=cube([xdim, ydim, zdim])
#
#    def placecube(self):
#        output(self.c)
#
#    def instantiatecube(self):
#        return self.c
#
    def xpos(self):
#        global mpx
        return self.mpx

    def ypos(self):
#        global mpy
        return self.mpy

    def zpos(self):
#        global mpz
        return self.mpz

#    def tpzinc(self):
#        global tpzinc
#        return self.tpzinc

    def setxpos(self, newxpos):
#        global mpx
        self.mpx = newxpos

    def setypos(self, newypos):
#        global mpy
        self.mpy = newypos

    def setzpos(self, newzpos):
#        global mpz
        self.mpz = newzpos

#    def settpzinc(self, newtpzinc):
#        global tpzinc
#        self.tpzinc = newtpzinc

    def setupstock(self, stockXwidth,
                 stockYheight,
                 stockZthickness,
                 zeroheight,
                 stockzero,
                 retractheight):
        self.stockXwidth = stockXwidth
        self.stockYheight = stockYheight
        self.stockZthickness = stockZthickness
        self.zeroheight = zeroheight
        self.stockzero = stockzero
        self.retractheight = retractheight
#        global mpx
        self.mpx = float(0)
#        global mpy
        self.mpy = float(0)
#        global mpz
        self.mpz = float(0)
#        global tpz
#        self.tpzinc = float(0)
#        global currenttoolnum
        self.currenttoolnum = 102
#        global currenttoolshape
        self.currenttoolshape = cylinder(12.7, 1.5875)
        self.rapids = self.currenttoolshape
#        global stock
        self.stock = cube([stockXwidth, stockYheight, stockZthickness])
#%WRITEGC        if self.generategcode == True:
#%WRITEGC            self.writegc("(Design File: " + self.basefilename + ")")
        self.toolpaths = cylinder(0.1, 0.1)
        if self.zeroheight == "Top":
            if self.stockzero == "Lower-Left":
                self.stock = stock.translate([0,0,-self.stockZthickness])
                if self.generategcode == True:
                    self.writegc("(stockMin:0.00mm, 0.00mm, -",str(self.stockZthickness),"mm)")
                    self.writegc("(stockMax:",str(self.stockXwidth),"mm, ",str(stockYheight),"mm, 0.00mm)")
                    self.writegc("(STOCK/BLOCK, ",str(self.stockXwidth),", ",str(self.stockYheight),", ",str(self.stockZthickness),", 0.00, 0.00, ",str(self.stockZthickness),")")
            if self.stockzero == "Center-Left":
                self.stock = self.stock.translate([0,-stockYheight / 2,-stockZthickness])
                if self.generategcode == True:
                    self.writegc("(stockMin:0.00mm, -",str(self.stockYheight/2),"mm, -",str(self.stockZthickness),"mm)")
                    self.writegc("(stockMax:",str(self.stockXwidth),"mm, ",str(self.stockYheight/2),"mm, 0.00mm)")
                    self.writegc("(STOCK/BLOCK, ",str(self.stockXwidth),", ",str(self.stockYheight),", ",str(self.stockZthickness),", 0.00, ",str(self.stockYheight/2),", ",str(self.stockZthickness),")");
            if self.stockzero == "Top-Left":
                self.stock = self.stock.translate([0,-self.stockYheight,-self.stockZthickness])
                if self.generategcode == True:
                    self.writegc("(stockMin:0.00mm, -",str(self.stockYheight),"mm, -",str(self.stockZthickness),"mm)")
                    self.writegc("(stockMax:",str(self.stockXwidth),"mm, 0.00mm, 0.00mm)")
                    self.writegc("(STOCK/BLOCK, ",str(self.stockXwidth),", ",str(self.stockYheight),", ",str(self.stockZthickness),", 0.00, ",str(self.stockYheight),", ",str(self.stockZthickness),")")
            if self.stockzero == "Center":
                self.stock = self.stock.translate([-self.stockXwidth / 2,-self.stockYheight / 2,-self.stockZthickness])
                if self.generategcode == True:
                    self.writegc("(stockMin: -",str(self.stockXwidth/2),", -",str(self.stockYheight/2),"mm, -",str(self.stockZthickness),"mm)")
                    self.writegc("(stockMax:",str(self.stockXwidth/2),"mm, ",str(self.stockYheight/2),"mm, 0.00mm)")
                    self.writegc("(STOCK/BLOCK, ",str(self.stockXwidth),", ",str(self.stockYheight),", ",str(self.stockZthickness),", ",str(self.stockXwidth/2),", ", str(self.stockYheight/2),", ",str(self.stockZthickness),")")
        if self.zeroheight == "Bottom":
            if self.stockzero == "Lower-Left":
                 self.stock = self.stock.translate([0,0,0])
                 if self.generategcode == True:
                     self.writegc("(stockMin:0.00mm, 0.00mm, 0.00mm)")
                     self.writegc("(stockMax:",str(self.stockXwidth),"mm, ",str(self.stockYheight),"mm,  ",str(self.stockZthickness),"mm)")
                     self.writegc("(STOCK/BLOCK, ",str(self.stockXwidth),", ",str(self.stockYheight),", ",str(self.stockZthickness),", 0.00, 0.00, 0.00)")
            if self.stockzero == "Center-Left":
                self.stock = self.stock.translate([0,-self.stockYheight / 2,0])
                if self.generategcode == True:
                    self.writegc("(stockMin:0.00mm, -",str(self.stockYheight/2),"mm, 0.00mm)")
                    self.writegc("(stockMax:",str(self.stockXwidth),"mm, ",str(self.stockYheight/2),"mm, -",str(self.stockZthickness),"mm)")
                    self.writegc("(STOCK/BLOCK, ",str(self.stockXwidth),", ",str(self.stockYheight),", ",str(self.stockZthickness),", 0.00, ",str(self.stockYheight/2),", 0.00mm)");
            if self.stockzero == "Top-Left":
                self.stock = self.stock.translate([0,-self.stockYheight,0])
                if self.generategcode == True:
                    self.writegc("(stockMin:0.00mm, -",str(self.stockYheight),"mm, 0.00mm)")
                    self.writegc("(stockMax:",str(self.stockXwidth),"mm, 0.00mm, ",str(self.stockZthickness),"mm)")
                    self.writegc("(STOCK/BLOCK, ",str(self.stockXwidth),", ",str(self.stockYheight),", ",str(self.stockZthickness),", 0.00, ",str(self.stockYheight),", 0.00)")
            if self.stockzero == "Center":
                self.stock = self.stock.translate([-self.stockXwidth / 2,-self.stockYheight / 2,0])
                if self.generategcode == True:
                    self.writegc("(stockMin: -",str(self.stockXwidth/2),", -",str(self.stockYheight/2),"mm, 0.00mm)")
                    self.writegc("(stockMax:",str(self.stockXwidth/2),"mm, ",str(self.stockYheight/2),"mm, ",str(self.stockZthickness),"mm)")
                    self.writegc("(STOCK/BLOCK, ",str(self.stockXwidth),", ",str(self.stockYheight),", ",str(self.stockZthickness),", ",str(self.stockXwidth/2),", ", str(self.stockYheight/2),", 0.00)")
        if self.generategcode == True:
            self.writegc("G90");
            self.writegc("G21");

    def settool(self,tn):
#        global currenttoolnum
        self.currenttoolnum = tn

    def currenttoolnumber(self):
#        global currenttoolnum
        return self.currenttoolnum

#    def currentroundovertoolnumber(self):
#        global Roundover_tool_num
#        return self.Roundover_tool_num

    def endmill_square(self, es_diameter, es_flute_length):
        return cylinder(r1=(es_diameter / 2), r2=(es_diameter / 2), h=es_flute_length, center = False)

    def ballnose(self, es_diameter, es_flute_length):
        b = sphere(r=(es_diameter / 2))
        s = cylinder(r1=(es_diameter / 2), r2=(es_diameter / 2), h=es_flute_length, center=False)
        p = union(b,s)
        return p.translate([0, 0, (es_diameter / 2)])

    def endmill_v(self, es_v_angle, es_diameter):
        es_v_angle = math.radians(es_v_angle)
        v = cylinder(r1=0, r2=(es_diameter / 2), h=((es_diameter / 2) / math.tan((es_v_angle / 2))), center=False)
        s = cylinder(r1=(es_diameter / 2), r2=(es_diameter / 2), h=((es_diameter * 8) ), center=False)
        sh = s.translate([0, 0, ((es_diameter / 2) / math.tan((es_v_angle / 2)))])
        return union(v,sh)

    def keyhole(self, es_diameter, es_flute_length):
        return cylinder(r1=(es_diameter / 2), r2=(es_diameter / 2), h=es_flute_length, center=False)

    def keyhole_shaft(self, es_diameter, es_flute_length):
        return cylinder(r1=(es_diameter / 2), r2=(es_diameter / 2), h=es_flute_length, center=False)

    def threadmill(self, minor_diameter, major_diameter, cut_height):
        btm = cylinder(r1=(minor_diameter / 2), r2=(major_diameter / 2), h=cut_height, center = False)
        top = cylinder(r1=(major_diameter / 2), r2=(minor_diameter / 2), h=cut_height, center = False)
        top = top.translate([0, 0, cut_height/2])
        tm = btm.union(top)
        return tm

    def threadmill_shaft(self, diameter, cut_height, height):
        shaft = cylinder(r1=(diameter / 2), r2=(diameter / 2), h=height, center = False)
        shaft = shaft.translate([0, 0, cut_height/2])
        return shaft

    def dovetail(self, dt_bottomdiameter, dt_topdiameter, dt_height, dt_angle):
        return cylinder(r1=(dt_bottomdiameter / 2), r2=(dt_topdiameter / 2), h= dt_height, center=False)

    def currenttool(self):
#        global currenttoolshape
        return self.currenttoolshape

    def toolchange(self,tool_number,speed = 10000):
#        global currenttoolshape
        self.currenttoolshape = self.endmill_square(0.001, 0.001)

        self.settool(tool_number)
        if (self.generategcode == True):
            self.writegc("(Toolpath)")
            self.writegc("M05")
        if (tool_number == 201):
            self.writegc("(TOOL/MILL,6.35, 0.00, 0.00, 0.00)")
            self.currenttoolshape = self.endmill_square(6.35, 19.05)
        elif (tool_number == 102):
            self.writegc("(TOOL/MILL,3.175, 0.00, 0.00, 0.00)")
            self.currenttoolshape = self.endmill_square(3.175, 12.7)
        elif (tool_number == 112):
            self.writegc("(TOOL/MILL,1.5875, 0.00, 0.00, 0.00)")
            self.currenttoolshape = self.endmill_square(1.5875, 6.35)
        elif (tool_number == 122):
            self.writegc("(TOOL/MILL,0.79375, 0.00, 0.00, 0.00)")
            self.currenttoolshape = self.endmill_square(0.79375, 1.5875)
        elif (tool_number == 202):
            self.writegc("(TOOL/MILL,6.35, 3.175, 0.00, 0.00)")
            self.currenttoolshape = self.ballnose(6.35, 19.05)
        elif (tool_number == 101):
            self.writegc("(TOOL/MILL,3.175, 1.5875, 0.00, 0.00)")
            self.currenttoolshape = self.ballnose(3.175, 12.7)
        elif (tool_number == 111):
            self.writegc("(TOOL/MILL,1.5875, 0.79375, 0.00, 0.00)")
            self.currenttoolshape = self.ballnose(1.5875, 6.35)
        elif (tool_number == 121):
            self.writegc("(TOOL/MILL,3.175, 0.79375, 0.00, 0.00)")
            self.currenttoolshape = self.ballnose(0.79375, 1.5875)
        elif (tool_number == 327):
            self.writegc("(TOOL/MILL,0.03, 0.00, 13.4874, 30.00)")
            self.currenttoolshape = self.endmill_v(60, 26.9748)
        elif (tool_number == 301):
            self.writegc("(TOOL/MILL,0.03, 0.00, 6.35, 45.00)")
            self.currenttoolshape = self.endmill_v(90, 12.7)
        elif (tool_number == 302):
            self.writegc("(TOOL/MILL,0.03, 0.00, 10.998, 30.00)")
            self.currenttoolshape = self.endmill_v(60, 12.7)
        elif (tool_number == 390):
            self.writegc("(TOOL/MILL,0.03, 0.00, 1.5875, 45.00)")
            self.currenttoolshape = self.endmill_v(90, 3.175)
        elif (tool_number == 374):
            self.writegc("(TOOL/MILL,9.53, 0.00, 3.17, 0.00)")
        elif (tool_number == 375):
            self.writegc("(TOOL/MILL,9.53, 0.00, 3.17, 0.00)")
        elif (tool_number == 376):
            self.writegc("(TOOL/MILL,12.7, 0.00, 4.77, 0.00)")
        elif (tool_number == 378):
            self.writegc("(TOOL/MILL,12.7, 0.00, 4.77, 0.00)")
        elif (tool_number == 814):
            self.writegc("(TOOL/MILL,12.7, 6.367, 12.7, 0.00)")
            #dt_bottomdiameter, dt_topdiameter, dt_height, dt_angle)
            #https://www.leevalley.com/en-us/shop/tools/power-tool-accessories/router-bits/30172-dovetail-bits?item=18J1607
            self.currenttoolshape = self.dovetail(12.7, 6.367, 12.7, 14)
        elif (tool_number == 56125):#0.508/2, 1.531
            self.writegc("(TOOL/CRMILL, 0.508, 6.35, 3.175, 7.9375, 3.175)")
        elif (tool_number == 56142):#0.508/2, 2.921
            self.writegc("(TOOL/CRMILL, 0.508, 3.571875, 1.5875, 5.55625, 1.5875)")
#        elif (tool_number == 312):#1.524/2, 3.175
#            self.writegc("(TOOL/CRMILL, Diameter1, Diameter2,Radius, Height, Length)")
        elif (tool_number == 1570):#0.507/2, 4.509
            self.writegc("(TOOL/CRMILL, 0.17018, 9.525, 4.7625, 12.7, 4.7625)")
        self.writegc("M6T",str(tool_number))
        self.writegc("M03S",str(speed))

    def tool_diameter(self, ptd_tool, ptd_depth):
# Square 122,112,102,201
        if ptd_tool == 122:
            return 0.79375
        if ptd_tool == 112:
            return 1.5875
        if ptd_tool == 102:
            return 3.175
        if ptd_tool == 201:
            return 6.35
# Ball 121,111,101,202
        if ptd_tool == 122:
            if ptd_depth > 0.396875:
                return 0.79375
            else:
                return ptd_tool
        if ptd_tool == 112:
            if ptd_depth > 0.79375:
                return 1.5875
            else:
                return ptd_tool
        if ptd_tool == 101:
            if ptd_depth > 1.5875:
                return 3.175
            else:
                return ptd_tool
        if ptd_tool == 202:
            if ptd_depth > 3.175:
                return 6.35
            else:
                return ptd_tool
# V 301, 302, 390
        if ptd_tool == 301:
            return ptd_tool
        if ptd_tool == 302:
            return ptd_tool
        if ptd_tool == 390:
            return ptd_tool
# Keyhole
        if ptd_tool == 374:
            if ptd_depth < 3.175:
                return 9.525
            else:
                return 6.35
        if ptd_tool == 375:
            if ptd_depth < 3.175:
                return 9.525
            else:
                return 8
        if ptd_tool == 376:
            if ptd_depth < 4.7625:
                return 12.7
            else:
                return 6.35
        if ptd_tool == 378:
            if ptd_depth < 4.7625:
                return 12.7
            else:
                return 8
# Dovetail
        if ptd_tool == 814:
            if ptd_depth > 12.7:
                return 6.35
            else:
                return 12.7

    def tool_radius(self, ptd_tool, ptd_depth):
        tr = self.tool_diameter(ptd_tool, ptd_depth)/2
        return tr

    def rcs(self,ex, ey, ez, shape):
        start = shape
        end = shape
        toolpath = hull(start.translate([self.xpos(), self.ypos(), self.zpos()]),
                        end.translate([ex,ey,ez]))
        return toolpath

    def rapid(self,ex, ey, ez):
        cts = self.currenttoolshape
        toolpath = self.rcs(ex, ey, ez, cts)
        self.setxpos(ex)
        self.setypos(ey)
        self.setzpos(ez)
        if self.generatepaths == True:
            self.rapids = self.rapids.union(toolpath)
#            return cylinder(0.01, 0, 0.01, center = False, fn = 3)
            return cube([0.001,0.001,0.001])
        else:
            return toolpath

    def cutshape(self,ex, ey, ez):
        cts = self.currenttoolshape
        toolpath = self.rcs(ex, ey, ez, cts)
        if self.generatepaths == True:
            self.toolpaths = self.toolpaths.union(toolpath)
            return cube([0.001,0.001,0.001])
        else:
            return toolpath

    def movetosafeZ(self):
        rapid = self.rapid(self.xpos(),self.ypos(),self.retractheight)
#        if self.generatepaths == True:
#            rapid = self.rapid(self.xpos(),self.ypos(),self.retractheight)
#            self.rapids = self.rapids.union(rapid)
#        else:
#  if (generategcode == true) {
#  //    writecomment("PREPOSITION FOR RAPID PLUNGE");Z25.650
#  //G1Z24.663F381.0 ,"F",str(plunge)
        if self.generatepaths == False:
            return rapid
        else:
            return cube([0.001,0.001,0.001])

    def rapidXY(self, ex, ey):
        rapid = self.rapid(ex,ey,self.zpos())
#        if self.generatepaths == True:
#            self.rapids = self.rapids.union(rapid)
#        else:
        if self.generatepaths == False:
            return rapid

    def rapidZ(self, ez):
        rapid = self.rapid(self.xpos(),self.ypos(),ez)
#        if self.generatepaths == True:
#            self.rapids = self.rapids.union(rapid)
#        else:
        if self.generatepaths == False:
            return rapid

    def cutline(self,ex, ey, ez):\
#below will need to be integrated into if/then structure not yet copied
#        cts = self.currenttoolshape
        if (self.currenttoolnumber() == 374):
#            self.writegc("(TOOL/MILL,9.53, 0.00, 3.17, 0.00)")
            self.currenttoolshape = self.keyhole(9.53/2, 3.175)
            toolpath = self.cutshape(ex, ey, ez)
            self.currenttoolshape = self.keyhole_shaft(6.35/2, 12.7)
            toolpath = toolpath.union(self.cutshape(ex, ey, ez))
#        elif (self.currenttoolnumber() == 375):
#            self.writegc("(TOOL/MILL,9.53, 0.00, 3.17, 0.00)")
#        elif (self.currenttoolnumber() == 376):
#            self.writegc("(TOOL/MILL,12.7, 0.00, 4.77, 0.00)")
#        elif (self.currenttoolnumber() == 378):
#            self.writegc("(TOOL/MILL,12.7, 0.00, 4.77, 0.00)")
#        elif (self.currenttoolnumber() == 56125):#0.508/2, 1.531
#            self.writegc("(TOOL/CRMILL, 0.508, 6.35, 3.175, 7.9375, 3.175)")
        elif (self.currenttoolnumber() == 56142):#0.508/2, 2.921
#            self.writegc("(TOOL/CRMILL, 0.508, 3.571875, 1.5875, 5.55625, 1.5875)")
            toolpath = self.cutroundovertool(self.xpos(), self.ypos(), self.zpos(), ex, ey, ez, 0.508/2, 1.531)
#        elif (self.currenttoolnumber() == 1570):#0.507/2, 4.509
#            self.writegc("(TOOL/CRMILL, 0.17018, 9.525, 4.7625, 12.7, 4.7625)")
        else:
            toolpath = self.cutshape(ex, ey, ez)
        self.setxpos(ex)
        self.setypos(ey)
        self.setzpos(ez)
#        if self.generatepaths == True:
#            self.toolpaths = union([self.toolpaths, toolpath])
#        else:
        if self.generatepaths == False:
            return toolpath
        else:
            return cube([0.001,0.001,0.001])

    def cutlinedxfgc(self,ex, ey, ez):
        self.dxfline(self.currenttoolnumber(), self.xpos(), self.ypos(), ex, ey)
        self.writegc("G01 X", str(ex), " Y", str(ey), " Z", str(ez))
#        if self.generatepaths == False:
        return self.cutline(ex, ey, ez)

    def cutroundovertool(self, bx, by, bz, ex, ey, ez, tool_radius_tip, tool_radius_width):
#        n = 90 + fn*3
#        print("Tool dimensions", tool_radius_tip, tool_radius_width, "begin ",bx, by, bz,"end ", ex, ey, ez)
        step = 4 #360/n
        shaft = cylinder(step,tool_radius_tip,tool_radius_tip)
        toolpath = hull(shaft.translate([bx,by,bz]), shaft.translate([ex,ey,ez]))
        shaft = cylinder(tool_radius_width*2,tool_radius_tip+tool_radius_width,tool_radius_tip+tool_radius_width)
        toolpath = toolpath.union(hull(shaft.translate([bx,by,bz+tool_radius_width]), shaft.translate([ex,ey,ez+tool_radius_width])))
        for i in range(1, 90, 1):
            angle = i
            dx = tool_radius_width*math.cos(math.radians(angle))
            dxx = tool_radius_width*math.cos(math.radians(angle+1))
            dzz = tool_radius_width*math.sin(math.radians(angle))
            dz = tool_radius_width*math.sin(math.radians(angle+1))
            dh = abs(dzz-dz)+0.0001
            slice = cylinder(dh,tool_radius_tip+tool_radius_width-dx,tool_radius_tip+tool_radius_width-dxx)
            toolpath = toolpath.union(hull(slice.translate([bx,by,bz+dz]), slice.translate([ex,ey,ez+dz])))
        if self.generatepaths == True:
            self.toolpaths = self.toolpaths.union(toolpath)
        else:
            return toolpath

    def cutarcCC(self, barc, earc, xcenter, ycenter, radius, tpzreldim, steps=1):
#        tpzinc = ez - self.zpos() / (earc - barc)
        tpzinc = tpzreldim / (earc - barc)
        cts = self.currenttoolshape
        toolpath = cts
        toolpath = toolpath.translate([self.xpos(),self.ypos(),self.zpos()])
        i = barc
        while i < earc:
            toolpath = toolpath.union(self.cutline(xcenter + radius * math.cos(math.radians(i)), ycenter + radius * math.sin(math.radians(i)), self.zpos()+tpzinc))
            i += steps
        if self.generatepaths == False:
            return toolpath
        else:
            return cube([0.01,0.01,0.01])

    def cutarcCW(self, barc,earc, xcenter, ycenter, radius, tpzreldim, steps=1):
#        print(str(self.zpos()))
#        print(str(ez))
#        print(str(barc - earc))
#        tpzinc = ez - self.zpos() / (barc - earc)
#        print(str(tzinc))
#        global toolpath
#        print("Entering n toolpath")
        tpzinc = tpzreldim / (barc - earc)
        cts = self.currenttoolshape
        toolpath = cts
        toolpath = toolpath.translate([self.xpos(),self.ypos(),self.zpos()])
        i = barc
        while i > earc:
            toolpath = toolpath.union(self.cutline(xcenter + radius * math.cos(math.radians(i)), ycenter + radius * math.sin(math.radians(i)), self.zpos()+tpzinc))
#            self.setxpos(xcenter + radius * math.cos(math.radians(i)))
#            self.setypos(ycenter + radius * math.sin(math.radians(i)))
#            print(str(self.xpos()), str(self.ypos(), str(self.zpos())))
#            self.setzpos(self.zpos()+tpzinc)
            i += abs(steps) * -1
#        self.dxfarc(self.currenttoolnumber(), xcenter, ycenter, radius, barc, earc)
#        if self.generatepaths == True:
#            print("Unioning n toolpath")
#            self.toolpaths = self.toolpaths.union(toolpath)
#        else:
        if self.generatepaths == False:
            return toolpath
        else:
            return cube([0.01,0.01,0.01])

    def dxfcircle(self, tool_num, xcenter, ycenter, radius):
        self.dxfarc(tool_num, xcenter, ycenter, radius,   0,  90)
        self.dxfarc(tool_num, xcenter, ycenter, radius,  90, 180)
        self.dxfarc(tool_num, xcenter, ycenter, radius, 180, 270)
        self.dxfarc(tool_num, xcenter, ycenter, radius, 270, 360)

    def dxfrectangle(self, tool_num, xorigin, yorigin, xwidth, yheight, corners = "Square", radius = 6):
        if corners == "Square":
            self.dxfline(tool_num, xorigin, yorigin, xorigin + xwidth, yorigin)
            self.dxfline(tool_num, xorigin + xwidth, yorigin, xorigin + xwidth, yorigin + yheight)
            self.dxfline(tool_num, xorigin + xwidth, yorigin + yheight, xorigin, yorigin + yheight)
            self.dxfline(tool_num, xorigin, yorigin + yheight, xorigin, yorigin)
        elif corners == "Fillet":
            self.dxfrectangleround(tool_num, xorigin, yorigin, xwidth, yheight, radius)
        elif corners == "Chamfer":
            self.dxfrectanglechamfer(tool_num, xorigin, yorigin, xwidth, yheight, radius)
        elif corners == "Flipped Fillet":
            self.dxfrectangleflippedfillet(tool_num, xorigin, yorigin, xwidth, yheight, radius)

    def dxfrectangleround(self, tool_num, xorigin, yorigin, xwidth, yheight, radius):
        self.dxfarc(tool_num, xorigin + xwidth - radius, yorigin + yheight - radius, radius,   0,  90)
        self.dxfarc(tool_num, xorigin + radius, yorigin + yheight - radius, radius,  90, 180)
        self.dxfarc(tool_num, xorigin + radius, yorigin + radius, radius, 180, 270)
        self.dxfarc(tool_num, xorigin + xwidth - radius, yorigin + radius, radius, 270, 360)

        self.dxfline(tool_num, xorigin + radius, yorigin, xorigin + xwidth - radius, yorigin)
        self.dxfline(tool_num, xorigin + xwidth, yorigin + radius, xorigin + xwidth, yorigin + yheight - radius)
        self.dxfline(tool_num, xorigin + xwidth - radius, yorigin + yheight, xorigin + radius, yorigin + yheight)
        self.dxfline(tool_num, xorigin, yorigin + yheight - radius, xorigin, yorigin + radius)

    def dxfrectanglechamfer(self, tool_num, xorigin, yorigin, xwidth, yheight, radius):
        self.dxfline(tool_num, xorigin + radius, yorigin, xorigin, yorigin + radius)
        self.dxfline(tool_num, xorigin, yorigin + yheight - radius, xorigin + radius, yorigin + yheight)
        self.dxfline(tool_num, xorigin + xwidth - radius, yorigin + yheight, xorigin + xwidth, yorigin + yheight - radius)
        self.dxfline(tool_num, xorigin + xwidth - radius, yorigin, xorigin + xwidth, yorigin + radius)

        self.dxfline(tool_num, xorigin + radius, yorigin, xorigin + xwidth - radius, yorigin)
        self.dxfline(tool_num, xorigin + xwidth, yorigin + radius, xorigin + xwidth, yorigin + yheight - radius)
        self.dxfline(tool_num, xorigin + xwidth - radius, yorigin + yheight, xorigin + radius, yorigin + yheight)
        self.dxfline(tool_num, xorigin, yorigin + yheight - radius, xorigin, yorigin + radius)

    def dxfrectangleflippedfillet(self, tool_num, xorigin, yorigin, xwidth, yheight, radius):
        self.dxfarc(tool_num, xorigin, yorigin, radius,   0,  90)
        self.dxfarc(tool_num, xorigin + xwidth, yorigin, radius,  90, 180)
        self.dxfarc(tool_num, xorigin + xwidth, yorigin + yheight, radius, 180, 270)
        self.dxfarc(tool_num, xorigin, yorigin + yheight, radius, 270, 360)

        self.dxfline(tool_num, xorigin + radius, yorigin, xorigin + xwidth - radius, yorigin)
        self.dxfline(tool_num, xorigin + xwidth, yorigin + radius, xorigin + xwidth, yorigin + yheight - radius)
        self.dxfline(tool_num, xorigin + xwidth - radius, yorigin + yheight, xorigin + radius, yorigin + yheight)
        self.dxfline(tool_num, xorigin, yorigin + yheight - radius, xorigin, yorigin + radius)

    def cutkeyholegcdxf(self, kh_tool_num, kh_start_depth, kh_max_depth, kht_direction, kh_distance):
        if (kht_direction == "N"):
            toolpath = self.cutKHgcdxf(kh_tool_num, kh_start_depth, kh_max_depth, 90, kh_distance)
        elif (kht_direction == "S"):
            toolpath = self.cutKHgcdxf(kh_tool_num, kh_start_depth, kh_max_depth, 270, kh_distance)
        elif (kht_direction == "E"):
            toolpath = self.cutKHgcdxf(kh_tool_num, kh_start_depth, kh_max_depth, 0, kh_distance)
        elif (kht_direction == "W"):
            toolpath = self.cutKHgcdxf(kh_tool_num, kh_start_depth, kh_max_depth, 180, kh_distance)
        if self.generatepaths == True:
            self.toolpaths = union([self.toolpaths, toolpath])
            return toolpath
        else:
            return cube([0.01,0.01,0.01])

    def cutKHgcdxf(self, kh_tool_num, kh_start_depth, kh_max_depth, kh_angle, kh_distance):
        oXpos = self.xpos()
        oYpos = self.ypos()
        self.dxfKH(kh_tool_num, self.xpos(), self.ypos(), kh_start_depth, kh_max_depth, kh_angle, kh_distance)
        toolpath = self.cutline(self.xpos(), self.ypos(), -kh_max_depth)
        self.setxpos(oXpos)
        self.setypos(oYpos)
        if self.generatepaths == False:
            return toolpath
        else:
            return cube([0.001,0.001,0.001])

    def dxfKH(self, kh_tool_num, oXpos, oYpos, kh_start_depth, kh_max_depth, kh_angle, kh_distance):
#        oXpos = self.xpos()
#        oYpos = self.ypos()
#Circle at entry hole
        self.dxfarc(kh_tool_num, oXpos,oYpos,self.tool_radius(kh_tool_num, 7),  0, 90)
        self.dxfarc(kh_tool_num, oXpos,oYpos,self.tool_radius(kh_tool_num, 7), 90,180)
        self.dxfarc(kh_tool_num, oXpos,oYpos,self.tool_radius(kh_tool_num, 7),180,270)
        self.dxfarc(kh_tool_num, oXpos,oYpos,self.tool_radius(kh_tool_num, 7),270,360)

#pre-calculate needed values
        r = self.tool_radius(kh_tool_num, 7)
#        print(r)
        rt = self.tool_radius(kh_tool_num, 1)
#        print(rt)
        ro = math.sqrt((self.tool_radius(kh_tool_num, 1))**2-(self.tool_radius(kh_tool_num, 7))**2)
#        print(ro)
        angle = math.degrees(math.acos(ro/rt))
#Outlines of entry hole and slot
        if (kh_angle == 0):
#Lower left of entry hole
            self.dxfarc(kh_tool_num, self.xpos(),self.ypos(),self.tool_radius(kh_tool_num, 1),180,270)
#Upper left of entry hole
            self.dxfarc(kh_tool_num, self.xpos(),self.ypos(),self.tool_radius(kh_tool_num, 1),90,180)
#Upper right of entry hole
#            self.dxfarc(kh_tool_num, self.xpos(), self.ypos(), rt, 41.810, 90)
            self.dxfarc(kh_tool_num, self.xpos(), self.ypos(), rt, angle, 90)
#Lower right of entry hole
            self.dxfarc(kh_tool_num, self.xpos(), self.ypos(), rt, 270, 360-angle)
#            self.dxfarc(kh_tool_num, self.xpos(),self.ypos(),self.tool_radius(kh_tool_num, 1),270, 270+math.acos(math.radians(self.tool_diameter(kh_tool_num, 5)/self.tool_diameter(kh_tool_num, 1))))
#Actual line of cut
#            self.dxfline(kh_tool_num, self.xpos(),self.ypos(),self.xpos()+kh_distance,self.ypos())
#upper right of end of slot (kh_max_depth+4.36))/2
            self.dxfarc(kh_tool_num, self.xpos()+kh_distance,self.ypos(),self.tool_diameter(kh_tool_num, (kh_max_depth+4.36))/2,0,90)
#lower right of end of slot
            self.dxfarc(kh_tool_num, self.xpos()+kh_distance,self.ypos(),self.tool_diameter(kh_tool_num, (kh_max_depth+4.36))/2,270,360)
#upper right slot
            self.dxfline(kh_tool_num, self.xpos()+ro, self.ypos()-(self.tool_diameter(kh_tool_num,7)/2), self.xpos()+kh_distance, self.ypos()-(self.tool_diameter(kh_tool_num,7)/2))
#            self.dxfline(kh_tool_num, self.xpos()+(sqrt((self.tool_diameter(kh_tool_num,1)^2)-(self.tool_diameter(kh_tool_num,5)^2))/2), self.ypos()+self.tool_diameter(kh_tool_num, (kh_max_depth))/2, ( (kh_max_depth-6.34))/2)^2-(self.tool_diameter(kh_tool_num, (kh_max_depth-6.34))/2)^2, self.xpos()+kh_distance, self.ypos()+self.tool_diameter(kh_tool_num, (kh_max_depth))/2, kh_tool_num)
#end position at top of slot
#lower right slot
            self.dxfline(kh_tool_num, self.xpos()+ro, self.ypos()+(self.tool_diameter(kh_tool_num,7)/2), self.xpos()+kh_distance, self.ypos()+(self.tool_diameter(kh_tool_num,7)/2))
#        dxfline(kh_tool_num, self.xpos()+(sqrt((self.tool_diameter(kh_tool_num,1)^2)-(self.tool_diameter(kh_tool_num,5)^2))/2), self.ypos()-self.tool_diameter(kh_tool_num, (kh_max_depth))/2, ( (kh_max_depth-6.34))/2)^2-(self.tool_diameter(kh_tool_num, (kh_max_depth-6.34))/2)^2, self.xpos()+kh_distance, self.ypos()-self.tool_diameter(kh_tool_num, (kh_max_depth))/2, KH_tool_num)
#end position at top of slot
#    hull(){
#      translate([xpos(), ypos(), zpos()]){
#        keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#    }
#    hull(){
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos()+kh_distance, ypos(), zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#    }
#    cutwithfeed(getxpos(),getypos(),-kh_max_depth,feed);
#    cutwithfeed(getxpos()+kh_distance,getypos(),-kh_max_depth,feed);
#    setxpos(getxpos()-kh_distance);
#  } else if (kh_angle > 0 && kh_angle < 90) {
#//echo(kh_angle);
#  dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_num, (kh_max_depth))/2,90+kh_angle,180+kh_angle, KH_tool_num);
#  dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_num, (kh_max_depth))/2,180+kh_angle,270+kh_angle, KH_tool_num);
#dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_num, (kh_max_depth))/2,kh_angle+asin((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_num, (kh_max_depth))/2)),90+kh_angle, KH_tool_num);
#dxfarc(getxpos(),getypos(),tool_diameter(KH_tool_num, (kh_max_depth))/2,270+kh_angle,360+kh_angle-asin((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_num, (kh_max_depth))/2)), KH_tool_num);
#dxfarc(getxpos()+(kh_distance*cos(kh_angle)),
#  getypos()+(kh_distance*sin(kh_angle)),tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2,0+kh_angle,90+kh_angle, KH_tool_num);
#dxfarc(getxpos()+(kh_distance*cos(kh_angle)),getypos()+(kh_distance*sin(kh_angle)),tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2,270+kh_angle,360+kh_angle, KH_tool_num);
#dxfline( getxpos()+tool_diameter(KH_tool_num, (kh_max_depth))/2*cos(kh_angle+asin((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_num, (kh_max_depth))/2))),
# getypos()+tool_diameter(KH_tool_num, (kh_max_depth))/2*sin(kh_angle+asin((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_num, (kh_max_depth))/2))),
# getxpos()+(kh_distance*cos(kh_angle))-((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)*sin(kh_angle)),
# getypos()+(kh_distance*sin(kh_angle))+((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)*cos(kh_angle)), KH_tool_num);
#//echo("a",tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2);
#//echo("c",tool_diameter(KH_tool_num, (kh_max_depth))/2);
#echo("Aangle",asin((tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2)/(tool_diameter(KH_tool_num, (kh_max_depth))/2)));
#//echo(kh_angle);
# cutwithfeed(getxpos()+(kh_distance*cos(kh_angle)),getypos()+(kh_distance*sin(kh_angle)),-kh_max_depth,feed);
#            toolpath = toolpath.union(self.cutline(self.xpos()+kh_distance, self.ypos(), -kh_max_depth))
        elif (kh_angle == 90):
#Lower left of entry hole
            self.dxfarc(kh_tool_num, oXpos,oYpos,self.tool_radius(kh_tool_num, 1),180,270)
#Lower right of entry hole
            self.dxfarc(kh_tool_num, oXpos,oYpos,self.tool_radius(kh_tool_num, 1),270,360)
#left slot
            self.dxfline(kh_tool_num, oXpos-r, oYpos+ro, oXpos-r, oYpos+kh_distance)
#right slot
            self.dxfline(kh_tool_num, oXpos+r, oYpos+ro, oXpos+r, oYpos+kh_distance)
#upper left of end of slot
            self.dxfarc(kh_tool_num, oXpos,oYpos+kh_distance,r,90,180)
#upper right of end of slot
            self.dxfarc(kh_tool_num, oXpos,oYpos+kh_distance,r,0,90)
#Upper right of entry hole
            self.dxfarc(kh_tool_num, oXpos, oYpos, rt, 0, 90-angle)
#Upper left of entry hole
            self.dxfarc(kh_tool_num, oXpos, oYpos, rt, 90+angle, 180)
#            toolpath = toolpath.union(self.cutline(oXpos, oYpos+kh_distance, -kh_max_depth))
        elif (kh_angle == 180):
#Lower right of entry hole
            self.dxfarc(kh_tool_num, oXpos,oYpos,self.tool_radius(kh_tool_num, 1),270,360)
#Upper right of entry hole
            self.dxfarc(kh_tool_num, oXpos,oYpos,self.tool_radius(kh_tool_num, 1),0,90)
#Upper left of entry hole
            self.dxfarc(kh_tool_num, oXpos, oYpos, rt, 90, 180-angle)
#Lower left of entry hole
            self.dxfarc(kh_tool_num, oXpos, oYpos, rt, 180+angle, 270)
#upper slot
            self.dxfline(kh_tool_num, oXpos-ro, oYpos-r, oXpos-kh_distance, oYpos-r)
#lower slot
            self.dxfline(kh_tool_num, oXpos-ro, oYpos+r, oXpos-kh_distance, oYpos+r)
#upper left of end of slot
            self.dxfarc(kh_tool_num, oXpos-kh_distance,oYpos,r,90,180)
#lower left of end of slot
            self.dxfarc(kh_tool_num, oXpos-kh_distance,oYpos,r,180,270)
#            toolpath = toolpath.union(self.cutline(oXpos-kh_distance, oYpos, -kh_max_depth))
        elif (kh_angle == 270):
#Upper left of entry hole
            self.dxfarc(kh_tool_num, oXpos,oYpos,self.tool_radius(kh_tool_num, 1),90,180)
#Upper right of entry hole
            self.dxfarc(kh_tool_num, oXpos,oYpos,self.tool_radius(kh_tool_num, 1),0,90)
#left slot
            self.dxfline(kh_tool_num, oXpos-r, oYpos-ro, oXpos-r, oYpos-kh_distance)
#right slot
            self.dxfline(kh_tool_num, oXpos+r, oYpos-ro, oXpos+r, oYpos-kh_distance)
#lower left of end of slot
            self.dxfarc(kh_tool_num, oXpos,oYpos-kh_distance,r,180,270)
#lower right of end of slot
            self.dxfarc(kh_tool_num, oXpos,oYpos-kh_distance,r,270,360)
#lower right of entry hole
            self.dxfarc(kh_tool_num, oXpos, oYpos, rt, 180, 270-angle)
#lower left of entry hole
            self.dxfarc(kh_tool_num, oXpos, oYpos, rt, 270+angle, 360)
#            toolpath = toolpath.union(self.cutline(oXpos, oYpos-kh_distance, -kh_max_depth))
#        print(self.zpos())
#        self.setxpos(oXpos)
#        self.setypos(oYpos)
#        if self.generatepaths == False:
#            return toolpath

#  } else if (kh_angle == 90) {
#    //Lower left of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2,180,270, KH_tool_num);
#    //Lower right of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2,270,360, KH_tool_num);
#    //Upper right of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2,0,acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), KH_tool_num);
#    //Upper left of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2,180-acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), 180,KH_tool_num);
#    //Actual line of cut
#    dxfline(getxpos(),getypos(),getxpos(),getypos()+kh_distance);
#    //upper right of slot
#    dxfarc(getxpos(),getypos()+kh_distance,tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2,0,90, KH_tool_num);
#    //upper left of slot
#    dxfarc(getxpos(),getypos()+kh_distance,tool_diameter(KH_tool_num, (kh_max_depth+6.35))/2,90,180, KH_tool_num);
#    //right of slot
#    dxfline(
#        getxpos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,
#        getypos()+(sqrt((tool_diameter(KH_tool_num,1)^2)-(tool_diameter(KH_tool_num,5)^2))/2),//( (kh_max_depth-6.34))/2)^2-(tool_diameter(KH_tool_num, (kh_max_depth-6.34))/2)^2,
#        getxpos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,
#    //end position at top of slot
#        getypos()+kh_distance,
#        KH_tool_num);
#    dxfline(getxpos()-tool_diameter(KH_tool_num, (kh_max_depth))/2, getypos()+(sqrt((tool_diameter(KH_tool_num,1)^2)-(tool_diameter(KH_tool_num,5)^2))/2), getxpos()-tool_diameter(KH_tool_num, (kh_max_depth+6.35))/2,getypos()+kh_distance, KH_tool_num);
#    hull(){
#      translate([xpos(), ypos(), zpos()]){
#        keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#    }
#    hull(){
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos(), ypos()+kh_distance, zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#    }
#    cutwithfeed(getxpos(),getypos(),-kh_max_depth,feed);
#    cutwithfeed(getxpos(),getypos()+kh_distance,-kh_max_depth,feed);
#    setypos(getypos()-kh_distance);
#  } else if (kh_angle == 180) {
#    //Lower right of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2,270,360, KH_tool_num);
#    //Upper right of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2,0,90, KH_tool_num);
#    //Upper left of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2,90, 90+acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), KH_tool_num);
#    //Lower left of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2, 270-acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), 270, KH_tool_num);
#    //upper left of slot
#    dxfarc(getxpos()-kh_distance,getypos(),tool_diameter(KH_tool_num, (kh_max_depth+6.35))/2,90,180, KH_tool_num);
#    //lower left of slot
#    dxfarc(getxpos()-kh_distance,getypos(),tool_diameter(KH_tool_num, (kh_max_depth+6.35))/2,180,270, KH_tool_num);
#    //Actual line of cut
#    dxfline(getxpos(),getypos(),getxpos()-kh_distance,getypos());
#    //upper left slot
#    dxfline(
#        getxpos()-(sqrt((tool_diameter(KH_tool_num,1)^2)-(tool_diameter(KH_tool_num,5)^2))/2),
#        getypos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,//( (kh_max_depth-6.34))/2)^2-(tool_diameter(KH_tool_num, (kh_max_depth-6.34))/2)^2,
#        getxpos()-kh_distance,
#    //end position at top of slot
#        getypos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,
#        KH_tool_num);
#    //lower right slot
#    dxfline(
#        getxpos()-(sqrt((tool_diameter(KH_tool_num,1)^2)-(tool_diameter(KH_tool_num,5)^2))/2),
#        getypos()-tool_diameter(KH_tool_num, (kh_max_depth))/2,//( (kh_max_depth-6.34))/2)^2-(tool_diameter(KH_tool_num, (kh_max_depth-6.34))/2)^2,
#        getxpos()-kh_distance,
#    //end position at top of slot
#        getypos()-tool_diameter(KH_tool_num, (kh_max_depth))/2,
#        KH_tool_num);
#    hull(){
#      translate([xpos(), ypos(), zpos()]){
#        keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#    }
#    hull(){
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos()-kh_distance, ypos(), zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#    }
#    cutwithfeed(getxpos(),getypos(),-kh_max_depth,feed);
#    cutwithfeed(getxpos()-kh_distance,getypos(),-kh_max_depth,feed);
#    setxpos(getxpos()+kh_distance);
#  } else if (kh_angle == 270) {
#    //Upper right of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2,0,90, KH_tool_num);
#    //Upper left of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2,90,180, KH_tool_num);
#    //lower right of slot
#    dxfarc(getxpos(),getypos()-kh_distance,tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2,270,360, KH_tool_num);
#    //lower left of slot
#    dxfarc(getxpos(),getypos()-kh_distance,tool_diameter(KH_tool_num, (kh_max_depth+4.36))/2,180,270, KH_tool_num);
#    //Actual line of cut
#    dxfline(getxpos(),getypos(),getxpos(),getypos()-kh_distance);
#    //right of slot
#    dxfline(
#        getxpos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,
#        getypos()-(sqrt((tool_diameter(KH_tool_num,1)^2)-(tool_diameter(KH_tool_num,5)^2))/2),//( (kh_max_depth-6.34))/2)^2-(tool_diameter(KH_tool_num, (kh_max_depth-6.34))/2)^2,
#        getxpos()+tool_diameter(KH_tool_num, (kh_max_depth))/2,
#    //end position at top of slot
#        getypos()-kh_distance,
#        KH_tool_num);
#    //left of slot
#    dxfline(
#        getxpos()-tool_diameter(KH_tool_num, (kh_max_depth))/2,
#        getypos()-(sqrt((tool_diameter(KH_tool_num,1)^2)-(tool_diameter(KH_tool_num,5)^2))/2),//( (kh_max_depth-6.34))/2)^2-(tool_diameter(KH_tool_num, (kh_max_depth-6.34))/2)^2,
#        getxpos()-tool_diameter(KH_tool_num, (kh_max_depth))/2,
#    //end position at top of slot
#        getypos()-kh_distance,
#        KH_tool_num);
#    //Lower right of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2,360-acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), 360, KH_tool_num);
#    //Lower left of entry hole
#    dxfarc(getxpos(),getypos(),9.525/2,180, 180+acos(tool_diameter(KH_tool_num, 5)/tool_diameter(KH_tool_num, 1)), KH_tool_num);
#    hull(){
#      translate([xpos(), ypos(), zpos()]){
#        keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#    }
#    hull(){
#      translate([xpos(), ypos(), zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#      translate([xpos(), ypos()-kh_distance, zpos()-kh_max_depth]){
#        keyhole_shaft(6.35, 9.525);
#      }
#    }
#    cutwithfeed(getxpos(),getypos(),-kh_max_depth,feed);
#    cutwithfeed(getxpos(),getypos()-kh_distance,-kh_max_depth,feed);
#    setypos(getypos()+kh_distance);
#  }
#}

    def stockandtoolpaths(self, option = "stockandtoolpaths"):
        if option == "stock":
            if self.generatepaths == False:
                output(self.stock)
#                print("Outputting stock")
            else:
                return self.stock
        elif option == "toolpaths":
            if self.generatepaths == False:
                output(self.toolpaths)
            else:
                return self.toolpaths
        elif option == "rapids":
            if self.generatepaths == False:
                output(self.rapids)
            else:
                return self.rapids
        else:
            part = self.stock.difference(self.toolpaths)
            if self.generatepaths == False:
                output(part)
            else:
                return part

    def writegc(self, *arguments):
        if self.generategcode == True:
            line_to_write = ""
            for element in arguments:
                line_to_write += element
            self.gc.write(line_to_write)
            self.gc.write("\n")

    def writedxf(self, toolnumber, *arguments):
#        global dxfclosed
        line_to_write = ""
        for element in arguments:
            line_to_write += element
        if self.generatedxf == True:
            if self.dxfclosed == False:
                self.dxf.write(line_to_write)
                self.dxf.write("\n")
        if self.generatedxfs == True:
            self.writedxfs(toolnumber, line_to_write)

    def writedxfs(self, toolnumber, line_to_write):
#        print("Processing writing toolnumber", toolnumber)
#        line_to_write = ""
#        for element in arguments:
#            line_to_write += element
        if (toolnumber == 0):
            return
        elif self.generatedxfs == True:
            if (self.large_square_tool_num == toolnumber):
                self.dxflgsq.write(line_to_write)
                self.dxflgsq.write("\n")
            if (self.small_square_tool_num == toolnumber):
                self.dxfsmsq.write(line_to_write)
                self.dxfsmsq.write("\n")
            if (self.large_ball_tool_num == toolnumber):
                self.dxflgbl.write(line_to_write)
                self.dxflgbl.write("\n")
            if (self.small_ball_tool_num == toolnumber):
                self.dxfsmbl.write(line_to_write)
                self.dxfsmbl.write("\n")
            if (self.large_V_tool_num == toolnumber):
                self.dxflgV.write(line_to_write)
                self.dxflgV.write("\n")
            if (self.small_V_tool_num == toolnumber):
                self.dxfsmV.write(line_to_write)
                self.dxfsmV.write("\n")
            if (self.DT_tool_num == toolnumber):
                self.dxfDT.write(line_to_write)
                self.dxfDT.write("\n")
            if (self.KH_tool_num == toolnumber):
                self.dxfKH.write(line_to_write)
                self.dxfKH.write("\n")
            if (self.Roundover_tool_num == toolnumber):
                self.dxfRt.write(line_to_write)
                self.dxfRt.write("\n")
            if (self.MISC_tool_num == toolnumber):
                self.dxfMt.write(line_to_write)
                self.dxfMt.write("\n")

    def opengcodefile(self, basefilename = "export",
                      currenttoolnum = 102,
                      toolradius = 3.175,
                      plunge = 400,
                      feed = 1600,
                      speed = 10000
                      ):
        self.basefilename = basefilename
        self.currenttoolnum = currenttoolnum
        self.toolradius = toolradius
        self.plunge = plunge
        self.feed = feed
        self.speed = speed
        if self.generategcode == True:
            self.gcodefilename = basefilename + ".nc"
            self.gc = open(self.gcodefilename, "w")

    def opendxffile(self, basefilename = "export"):
        self.basefilename = basefilename
#        global generatedxfs
#        global dxfclosed
        self.dxfclosed = False
        if self.generatedxf == True:
            self.generatedxfs = False
            self.dxffilename = basefilename + ".dxf"
            self.dxf = open(self.dxffilename, "w")
            self.dxfpreamble(-1)

    def opendxffiles(self, basefilename = "export",
                     large_square_tool_num = 0,
                     small_square_tool_num = 0,
                     large_ball_tool_num = 0,
                     small_ball_tool_num = 0,
                     large_V_tool_num = 0,
                     small_V_tool_num = 0,
                     DT_tool_num = 0,
                     KH_tool_num = 0,
                     Roundover_tool_num = 0,
                     MISC_tool_num = 0):
#        global generatedxfs
        self.basefilename = basefilename
        self.generatedxfs = True
        self.large_square_tool_num = large_square_tool_num
        self.small_square_tool_num = small_square_tool_num
        self.large_ball_tool_num = large_ball_tool_num
        self.small_ball_tool_num = small_ball_tool_num
        self.large_V_tool_num = large_V_tool_num
        self.small_V_tool_num = small_V_tool_num
        self.DT_tool_num = DT_tool_num
        self.KH_tool_num = KH_tool_num
        self.Roundover_tool_num = Roundover_tool_num
        self.MISC_tool_num = MISC_tool_num
        if self.generatedxf == True:
            if (large_square_tool_num > 0):
                self.dxflgsqfilename = basefilename + str(large_square_tool_num) + ".dxf"
#                print("Opening ", str(self.dxflgsqfilename))
                self.dxflgsq = open(self.dxflgsqfilename, "w")
            if (small_square_tool_num > 0):
#                print("Opening small square")
                self.dxfsmsqfilename = basefilename + str(small_square_tool_num) + ".dxf"
                self.dxfsmsq = open(self.dxfsmsqfilename, "w")
            if (large_ball_tool_num > 0):
#                print("Opening large ball")
                self.dxflgblfilename = basefilename + str(large_ball_tool_num) + ".dxf"
                self.dxflgbl = open(self.dxflgblfilename, "w")
            if (small_ball_tool_num > 0):
#                print("Opening small ball")
                self.dxfsmblfilename = basefilename + str(small_ball_tool_num) + ".dxf"
                self.dxfsmbl = open(self.dxfsmblfilename, "w")
            if (large_V_tool_num > 0):
#                print("Opening large V")
                self.dxflgVfilename = basefilename + str(large_V_tool_num) + ".dxf"
                self.dxflgV = open(self.dxflgVfilename, "w")
            if (small_V_tool_num > 0):
#                print("Opening small V")
                self.dxfsmVfilename = basefilename + str(small_V_tool_num) + ".dxf"
                self.dxfsmV = open(self.dxfsmVfilename, "w")
            if (DT_tool_num > 0):
#                print("Opening DT")
                self.dxfDTfilename = basefilename + str(DT_tool_num) + ".dxf"
                self.dxfDT = open(self.dxfDTfilename, "w")
            if (KH_tool_num > 0):
#                print("Opening KH")
                self.dxfKHfilename = basefilename + str(KH_tool_num) + ".dxf"
                self.dxfKH = open(self.dxfKHfilename, "w")
            if (Roundover_tool_num > 0):
#                print("Opening Rt")
                self.dxfRtfilename = basefilename + str(Roundover_tool_num) + ".dxf"
                self.dxfRt = open(self.dxfRtfilename, "w")
            if (MISC_tool_num > 0):
#                print("Opening Mt")
                self.dxfMtfilename = basefilename + str(MISC_tool_num) + ".dxf"
                self.dxfMt = open(self.dxfMtfilename, "w")
            if (large_square_tool_num > 0):
                self.dxfpreamble(large_square_tool_num)
            if (small_square_tool_num > 0):
                self.dxfpreamble(small_square_tool_num)
            if (large_ball_tool_num > 0):
                self.dxfpreamble(large_ball_tool_num)
            if (small_ball_tool_num > 0):
                self.dxfpreamble(small_ball_tool_num)
            if (large_V_tool_num > 0):
                self.dxfpreamble(large_V_tool_num)
            if (small_V_tool_num > 0):
                self.dxfpreamble(small_V_tool_num)
            if (DT_tool_num > 0):
                self.dxfpreamble(DT_tool_num)
            if (KH_tool_num > 0):
                self.dxfpreamble(KH_tool_num)
            if (Roundover_tool_num > 0):
                self.dxfpreamble(Roundover_tool_num)
            if (MISC_tool_num > 0):
                self.dxfpreamble(MISC_tool_num)

    def dxfpreamble(self, tn):
#        self.writedxf(tn,str(tn))
        self.writedxf(tn,"0")
        self.writedxf(tn,"SECTION")
        self.writedxf(tn,"2")
        self.writedxf(tn,"ENTITIES")

    def dxfline(self, tn, xbegin,ybegin,xend,yend):
        self.writedxf(tn,"0")
        self.writedxf(tn,"LWPOLYLINE")
        self.writedxf(tn,"90")
        self.writedxf(tn,"2")
        self.writedxf(tn,"70")
        self.writedxf(tn,"0")
        self.writedxf(tn,"43")
        self.writedxf(tn,"0")
        self.writedxf(tn,"10")
        self.writedxf(tn,str(xbegin))
        self.writedxf(tn,"20")
        self.writedxf(tn,str(ybegin))
        self.writedxf(tn,"10")
        self.writedxf(tn,str(xend))
        self.writedxf(tn,"20")
        self.writedxf(tn,str(yend))

    def dxfarc(self, tn, xcenter, ycenter, radius, anglebegin, endangle):
        if (self.generatedxf == True):
            self.writedxf(tn, "0")
            self.writedxf(tn, "ARC")
            self.writedxf(tn, "10")
            self.writedxf(tn, str(xcenter))
            self.writedxf(tn, "20")
            self.writedxf(tn, str(ycenter))
            self.writedxf(tn, "40")
            self.writedxf(tn, str(radius))
            self.writedxf(tn, "50")
            self.writedxf(tn, str(anglebegin))
            self.writedxf(tn, "51")
            self.writedxf(tn, str(endangle))

    def gcodearc(self, tn, xcenter, ycenter, radius, anglebegin, endangle):
        if (self.generategcode == True):
            self.writegc(tn, "(0)")

    def cutarcNECCdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
#        toolpath = self.currenttool()
#        toolpath = toolpath.translate([self.xpos(),self.ypos(),self.zpos()])
        self.dxfarc(self.currenttoolnumber(), xcenter,ycenter,radius,0,90)
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
#        self.setxpos(ex)
#        self.setypos(ey)
#        self.setzpos(ez)
        if self.generatepaths == True:
            print("Unioning cutarcNECCdxf toolpath")
            self.arcloop(1,90, xcenter, ycenter, radius)
#            self.toolpaths = self.toolpaths.union(toolpath)
        else:
            toolpath = self.arcloop(1,90, xcenter, ycenter, radius)
#            print("Returning cutarcNECCdxf toolpath")
            return toolpath

    def cutarcNWCCdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
#        toolpath = self.currenttool()
#        toolpath = toolpath.translate([self.xpos(),self.ypos(),self.zpos()])
        self.dxfarc(self.currenttoolnumber(), xcenter,ycenter,radius,90,180)
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
#        self.setxpos(ex)
#        self.setypos(ey)
#        self.setzpos(ez)
        if self.generatepaths == True:
            self.arcloop(91,180, xcenter, ycenter, radius)
#            self.toolpaths = self.toolpaths.union(toolpath)
        else:
            toolpath = self.arcloop(91,180, xcenter, ycenter, radius)
            return toolpath

    def cutarcSWCCdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
#        toolpath = self.currenttool()
#        toolpath = toolpath.translate([self.xpos(),self.ypos(),self.zpos()])
        self.dxfarc(self.currenttoolnumber(), xcenter,ycenter,radius,180,270)
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
#        self.setxpos(ex)
#        self.setypos(ey)
#        self.setzpos(ez)
        if self.generatepaths == True:
            self.arcloop(181,270, xcenter, ycenter, radius)
#            self.toolpaths = self.toolpaths.union(toolpath)
        else:
            toolpath = self.arcloop(181,270, xcenter, ycenter, radius)
            return toolpath

    def cutarcSECCdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
#        toolpath = self.currenttool()
#        toolpath = toolpath.translate([self.xpos(),self.ypos(),self.zpos()])
        self.dxfarc(self.currenttoolnumber(), xcenter,ycenter,radius,270,360)
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
#        self.setxpos(ex)
#        self.setypos(ey)
#        self.setzpos(ez)
        if self.generatepaths == True:
            self.arcloop(271,360, xcenter, ycenter, radius)
#            self.toolpaths = self.toolpaths.union(toolpath)
        else:
            toolpath = self.arcloop(271,360, xcenter, ycenter, radius)
            return toolpath

    def cutarcNECWdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
#        toolpath = self.currenttool()
#        toolpath = toolpath.translate([self.xpos(),self.ypos(),self.zpos()])
        self.dxfarc(self.currenttoolnumber(), xcenter,ycenter,radius,0,90)
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
#        self.setxpos(ex)
#        self.setypos(ey)
#        self.setzpos(ez)
        if self.generatepaths == True:
            self.narcloop(89,0, xcenter, ycenter, radius)
#            self.toolpaths = self.toolpaths.union(toolpath)
        else:
            toolpath = self.narcloop(89,0, xcenter, ycenter, radius)
            return toolpath

    def cutarcSECWdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
#        toolpath = self.currenttool()
#        toolpath = toolpath.translate([self.xpos(),self.ypos(),self.zpos()])
        self.dxfarc(self.currenttoolnumber(), xcenter,ycenter,radius,270,360)
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
#        self.setxpos(ex)
#        self.setypos(ey)
#        self.setzpos(ez)
        if self.generatepaths == True:
            self.narcloop(359,270, xcenter, ycenter, radius)
#            self.toolpaths = self.toolpaths.union(toolpath)
        else:
            toolpath = self.narcloop(359,270, xcenter, ycenter, radius)
            return toolpath

    def cutarcSWCWdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
#        toolpath = self.currenttool()
#        toolpath = toolpath.translate([self.xpos(),self.ypos(),self.zpos()])
        self.dxfarc(self.currenttoolnumber(), xcenter,ycenter,radius,180,270)
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
#        self.setxpos(ex)
#        self.setypos(ey)
#        self.setzpos(ez)
        if self.generatepaths == True:
            self.narcloop(269,180, xcenter, ycenter, radius)
#            self.toolpaths = self.toolpaths.union(toolpath)
        else:
            toolpath = self.narcloop(269,180, xcenter, ycenter, radius)
            return toolpath

    def cutarcNWCWdxf(self, ex, ey, ez, xcenter, ycenter, radius):
#        global toolpath
#        toolpath = self.currenttool()
#        toolpath = toolpath.translate([self.xpos(),self.ypos(),self.zpos()])
        self.dxfarc(self.currenttoolnumber(), xcenter,ycenter,radius,90,180)
        if (self.zpos == ez):
            self.settzpos(0)
        else:
            self.settzpos((self.zpos()-ez)/90)
#        self.setxpos(ex)
#        self.setypos(ey)
#        self.setzpos(ez)
        if self.generatepaths == True:
            self.narcloop(179,90, xcenter, ycenter, radius)
#            self.toolpaths = self.toolpaths.union(toolpath)
        else:
            toolpath = self.narcloop(179,90, xcenter, ycenter, radius)
            return toolpath

    def arcCCgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.writegc("G03 X", str(ex), " Y", str(ey), " Z", str(ez), " R", str(radius))

    def arcCWgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.writegc("G02 X", str(ex), " Y", str(ey), " Z", str(ez), " R", str(radius))

    def cutarcNECCdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCCgc(ex, ey, ez, xcenter, ycenter, radius)
        if self.generatepaths == True:
            self.cutarcNECCdxf(ex, ey, ez, xcenter, ycenter, radius)
        else:
            return self.cutarcNECCdxf(ex, ey, ez, xcenter, ycenter, radius)

    def cutarcNWCCdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCCgc(ex, ey, ez, xcenter, ycenter, radius)
        if self.generatepaths == False:
            return self.cutarcNWCCdxf(ex, ey, ez, xcenter, ycenter, radius)

    def cutarcSWCCdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCCgc(ex, ey, ez, xcenter, ycenter, radius)
        if self.generatepaths == False:
            return self.cutarcSWCCdxf(ex, ey, ez, xcenter, ycenter, radius)

    def cutarcSECCdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCCgc(ex, ey, ez, xcenter, ycenter, radius)
        if self.generatepaths == False:
            return self.cutarcSECCdxf(ex, ey, ez, xcenter, ycenter, radius)

    def cutarcNECWdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCWgc(ex, ey, ez, xcenter, ycenter, radius)
        if self.generatepaths == False:
            return self.cutarcNECWdxf(ex, ey, ez, xcenter, ycenter, radius)

    def cutarcSECWdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCWgc(ex, ey, ez, xcenter, ycenter, radius)
        if self.generatepaths == False:
            return self.cutarcSECWdxf(ex, ey, ez, xcenter, ycenter, radius)

    def cutarcSWCWdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCWgc(ex, ey, ez, xcenter, ycenter, radius)
        if self.generatepaths == False:
            return self.cutarcSWCWdxf(ex, ey, ez, xcenter, ycenter, radius)

    def cutarcNWCWdxfgc(self, ex, ey, ez, xcenter, ycenter, radius):
        self.arcCWgc(ex, ey, ez, xcenter, ycenter, radius)
        if self.generatepaths == False:
            return self.cutarcNWCWdxf(ex, ey, ez, xcenter, ycenter, radius)

    def dxfpostamble(self,tn):
#        self.writedxf(tn,str(tn))
        self.writedxf(tn,"0")
        self.writedxf(tn,"ENDSEC")
        self.writedxf(tn,"0")
        self.writedxf(tn,"EOF")

    def gcodepostamble(self):
        self.writegc("Z12.700")
        self.writegc("M05")
        self.writegc("M02")

    def closegcodefile(self):
        self.gcodepostamble()
        self.gc.close()

    def closedxffile(self):
        if self.generatedxf == True:
#            global dxfclosed
            self.dxfpostamble(-1)
#            self.dxfclosed = True
            self.dxf.close()

    def closedxffiles(self):
        if self.generatedxfs == True:
            if (self.large_square_tool_num > 0):
                self.dxfpostamble(self.large_square_tool_num)
            if (self.small_square_tool_num > 0):
                self.dxfpostamble(self.small_square_tool_num)
            if (self.large_ball_tool_num > 0):
                self.dxfpostamble(self.large_ball_tool_num)
            if (self.small_ball_tool_num > 0):
                self.dxfpostamble(self.small_ball_tool_num)
            if (self.large_V_tool_num > 0):
                self.dxfpostamble(self.large_V_tool_num)
            if (self.small_V_tool_num > 0):
                self.dxfpostamble(self.small_V_tool_num)
            if (self.DT_tool_num > 0):
                self.dxfpostamble(self.DT_tool_num)
            if (self.KH_tool_num > 0):
                self.dxfpostamble(self.KH_tool_num)
            if (self.Roundover_tool_num > 0):
                self.dxfpostamble(self.Roundover_tool_num)
            if (self.MISC_tool_num > 0):
                self.dxfpostamble(self.MISC_tool_num)

            if (self.large_square_tool_num > 0):
                self.dxflgsq.close()
            if (self.small_square_tool_num > 0):
                self.dxfsmsq.close()
            if (self.large_ball_tool_num > 0):
                self.dxflgbl.close()
            if (self.small_ball_tool_num > 0):
                self.dxfsmbl.close()
            if (self.large_V_tool_num > 0):
                self.dxflgV.close()
            if (self.small_V_tool_num > 0):
                self.dxfsmV.close()
            if (self.DT_tool_num > 0):
                self.dxfDT.close()
            if (self.KH_tool_num > 0):
                self.dxfKH.close()
            if (self.Roundover_tool_num > 0):
                self.dxfRt.close()
            if (self.MISC_tool_num > 0):
                self.dxfMt.close()

