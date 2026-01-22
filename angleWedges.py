# Generates 3d printable angle wedges to help measure angles in the real world.

import cadquery as cq  # as of 260121 cq is v2.6.1
import numpy as np
import os

def makeWedge(h,a,t=5, holeDiameter=3, dir=os.path.dirname(__file__)):
    """
    makeWedge(h,a, dir=os.path.dirname(__file__)):
    h = wedge hypotenuse length
    a = angle of the wedge tip
    t = wedge thickness
    dir = containing folder
    """
    x = h*np.cos(a/2) # half angle becuase we will mirror below
    y = h*np.sin(a/2)
    pts = [(h+x,0),(h,y),(-h-x,y),(-h,0)]
    tri = cq.Workplane("top").polyline(pts).close()
    drt = tri.mirrorX()
    res1 = drt.extrude(t)
    txt = "{:3.0f}°".format(np.rad2deg(a))
    res2 = res1.faces("<Y").workplane().center(10,0).text(txt,6,-1)

    holeDiameter = min(y*2+2, 3) # ensure the hole fits within the body
    res3 = res2.faces("<Y").workplane().center(-10,0).circle(holeDiameter/2).cutThruAll() #this +10, -10 doesn't show in the right-pane render, but does in the stl..
    # show_object(res3)
    cq.exporters.export(res3,dir+"/wedge{:3.3f}.step".format(np.rad2deg(a)))
    cq.exporters.export(res3,dir+"/wedge{:3.3f}.3mf".format(np.rad2deg(a)))
    cq.exporters.export(res3,dir+"/wedge{:3.3f}.stl".format(np.rad2deg(a)))

h = 20 # 20mm hypotenuse length
for a in np.deg2rad(np.arange(10,130,5)):
    makeWedge(h,a)

# MIT License
# Copyright 2026 Mechanomy LLC
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.