Tool for cutting accurate SMT stencils on a Graphtec cutter (e.g. Silhouette Cameo or Portrait) from gerber files.  Techniques include separately drawn line segments (no complex paths), antibacklash, drag-knife-angle "training", and multiple passes.  This produces stencils usable down to approximately 0.5 mm pitch (QFP/QFN) and 0201 discrete components, or perhaps even slightly better; but it is slower than normal cutting.

**Ubuntu TLDR:**
Standard edition:
sudo apt install git build-essential python-dev python-setuptools python-pip python-smbus -y
sudo apt install gerbv pstoedit python-tk -y

Merge edition:
sudo apt install python-numpy python-scipy python-svgwrite -y

**Windows TLDR:**
From the deps folder install ghostscript and pstoedit
Gerbv will run without installation
Get the necessary python modules using pymodules.bat
Install Cameo drivers in Win7 compatibility mode, reboot Windows, and ensure the Cameo shows up in Devices and Printers as a printer. From the Sharing tab of the Printer Properties for the Cameo, share it and give it a name.

**Note:** This is currently terrible at handling round/rounded pads. They will cause merge to fail with an error about non-closed polygons. Anything that's not at a multiple of 45* will be bad; basically don't do them.  Planning on a fix when I get around to it.

**Usage:**

A solderpaste gerber file, paste.gbr, and default settings:

  *gerber2graphtec paste.gbr >/dev/usb/lp0*

A more elaborate command line with linear map (to correct spatial miscalibration) and multiple passes with different speeds and forces:

  *gerber2graphtec --offset 3,4 --matrix 1.001,0,-0.0005,0.9985 --speed 2,1 --force 5,25 paste.gbr >/dev/usb/lp0*
  
with merge:

  *gerber2graphtec --offset 0.5,0.5 --matrix 1.001,0,-0.0005,0.9985 --speed 2,1 --force 8,30 --merge 1 paste.gbr >/dev/usb/lp0*
  
**Note:** the offset start from top right (0, 0)

You may want to have your CAM tool shrink the paste features by about 2 mils before exporting to gerber.  The craft-cutter knife, when cutting thin mylar, seems to spread out the geometry by about this amount.  I'd suggest using mylar with thickness between about 3 and 5 mils; the IPC-recommended thicknesses for fine-pitch stencils are approximately in this range.  (Typical inexpensive laser-transparency sheets happen to be just right, being somewhere between 3.5 and 4.3 mils.)  You may have to experiment with the cutting speeds and forces for best quality with your materials.

With Mac OS X or Windows, the file2graphtec script can take the place of /dev/usb/lp0.  Write gerber2graphtec's output to a temporary file (gerber2graphtec ... >foo), then send it to the cutter (file2graphtec foo).  I've tested file2graphtec on Mac OS X but not on Windows.  For Mac OS X, install XCode and macports, then install the dependencies with

port install gerbv
port install pstoedit
port install libusb

These will take some time to build.

To run file2graphtec, you will also need the Python bindings for libusb-1.0.  Download and install this package:

http://pypi.python.org/pypi/libusb1

with the usual "python setup.py install" installation method (as the root user).  If you don't need file2graphtec (perhaps you're on Linux and can just use the device node directly), this Python package isn't needed.

Ubuntu users may need to check their version of gerbv.  Several users have reported that versions prior to 2.6.0 (such as 2.5.0) apparently have a bug related to omitting small apertures/pads.  If your Linux distribution still has the old gerbv-2.5.0, please delete the package and instead build from source for the latest stable version:

http://gerbv.geda-project.org/

Fedora 17 has gerbv-2.6.0 in its supplied package list, so no issue there.  For Fedora-like systems, "yum install gerbv pstoedit tkinter".

On some Linux distributions, permissions on /dev/usb/lp0 are restricted by default.  To fix this, add yourself to the lp group and then log out and log back in:

sudo usermod -a --group lp your_userid


Links:

These pages have hints on usage (e.g. on Windows), materials, performance, calibration, etc:

http://pmonta.com/blog/2012/12/25/smt-stencil-cutting/
http://dangerousprototypes.com/forum/viewtopic.php?f=68&t=5341
http://hackeda.com/blog/start-printing-pcb-stencils-for-about-200/
http://hackaday.com/2012/12/27/diy-smd-stencils-made-with-a-craft-cutter/


GUI:

An optional GUI has been provided by jesuscf (see the dangerousprototypes.com thread linked above).  It allows interactive selection of the input Gerber file, parameters, and cutting operations.  To use it, run the file g2g_gui.py.


Dependencies:

gerbv (>= 2.6.0)
pstoedit
Tkinter (when using g2g_gui)

Credits:

Thanks to the authors of robocut and graphtecprint for protocol documentation:

http://gitorious.org/robocut
http://vidar.botfu.org/graphtecprint
https://github.com/jnweiger/graphtecprint

Also thanks to this web page (Cathy Sexton) for inspiration:

http://www.idleloop.com/robotics/cutter/index.php

Her cutter seems to be quite a bit better than mine was out of the box.  With Silhouette's default software my 0.5 mm pitch pads were distorted to the point of unusability.
