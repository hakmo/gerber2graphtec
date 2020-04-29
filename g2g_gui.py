#!/usr/bin/env python
import Tkinter
import tkMessageBox
import tkFileDialog
import sys
import os
import string

from Tkinter import *
from os import path, access, R_OK, W_OK

top = Tkinter.Tk()
top.title("Gerber to Graphtec")

Gerber_name = StringVar()
Output_name = StringVar()
gerbv_path = StringVar()
pstoedit_path  = StringVar()
offset_str  = StringVar()
border_str  = StringVar()
matrix_str  = StringVar()
speed_str  = StringVar()
force_str  = StringVar()
cut_mode_str  = StringVar()
merge_str  = StringVar()
merge_threshold_str  = StringVar()
cutter_shared_name_str  = StringVar()
CONFPATH='./g2g_gui.cnf'

help_text = 'Help:\n\nGerber File \n- input Gerber (gbr,gtp,gbp) file\n\nOutput File \n- Graphtec / Silhouette (*.gpgl) file to send to the plotter\n\nOffset \n- translate to device coordinates x,y (inches)\n\nBorder \n- cut a border around the bounding box of the gerber file; 0,0 to disable\n\nMatrix \n- transform coordinates by [a b;c d]\n\nSpeed \n- use speed s in device units; s2,s3 for multiple passes\n\nForce \n- use force f in device units; f2,f3 for multiple passes\n\nMerge \n- Merge small SMD Pads\n\nMerge Threshold\n- Min Size, Min Distance\n\nCut Mode \n- 0 for highest accuracy (fine pitch), 1 for highest speed\n\nCutter Device/Share Name \n- device file or network share of the plotter, e.g. /dev/usb/lp0 or \\\Computer\\printer'

input_filename = ''
output_filename = ''
gerbv_filename = ''
pstoedit_filename = ''
offset_text = ''
border_text = ''
matrix_text = ''
speed_text = ''
force_text = ''
cut_mode_text = ''
merge_text = ''
merge_threshold_text = ''
cutter_shared_name_text = ''

offset = (4,0.5)
border = (1,1)
matrix = (1,0,0,1)
speed = [2,2]
force = [8,30]
cut_mode = 0
merge = 0
merge_threshold = [0.012, 0.01]  # min_size, min_distance in inch

def floats(s):
  return map(float,string.split(s,','))

def main_program():
  #
  # convert file to pic format
  #

  if not os.path.exists(Gerber_name.get()):
    get_input_filename()
  if not os.path.exists(Gerber_name.get()):
    tkMessageBox.showerror("G2G_GUI ERROR", "The path provided for the input Gerber file is invalid.")
    return

  head, tail = os.path.split(Gerber_name.get())

  if os.name=='nt':
    temp_pdf = os.path.normpath("%s\_tmp_gerber.pdf" % (head))
    temp_pic = os.path.normpath("%s\_tmp_gerber.pic" % (head))
    temp_bat = os.path.normpath("%s\_tmp_gerber.bat" % (head))
  else:
    temp_pdf = "_tmp_gerber.pdf"
    temp_pic = "_tmp_gerber.pic"

  if os.name=='nt':
    if not os.path.exists(gerbv_path.get()):
      tkMessageBox.showerror("G2G_GUI ERROR", "The path provided for gerbv is invalid.")
      return

    if not os.path.exists(pstoedit_path.get()):
      tkMessageBox.showerror("G2G_GUI ERROR", "The path provided for pstoedit is invalid.")
      return
  
  if os.name=='nt':
    os.system("echo \"%s\" --export=pdf --output=%s --border=0 \"%s\" > \"%s\"" % (os.path.normpath(gerbv_path.get()),temp_pdf,os.path.normpath(Gerber_name.get()),temp_bat))
    os.system("echo \"%s\" -q -f pic \"%s\" \"%s\" >> \"%s\"" % (os.path.normpath(pstoedit_path.get()),temp_pdf,temp_pic, temp_bat))
    os.system("\"%s\"" % temp_bat)
  else:
    os.system("%s --export=pdf --output=%s --border=0 \"%s\"" % (os.path.normpath(gerbv_path.get()),temp_pdf,os.path.normpath(Gerber_name.get())))
    os.system("%s -q -f pic \"%s\" \"%s\"" % (os.path.normpath(pstoedit_path.get()),temp_pdf,temp_pic))

  original_stdout = sys.stdout  # keep a reference to STDOUT

  if Output_name.get():
    sys.stdout = open(Output_name.get(), 'w')

  if not offset_str.get():
    default_offset_str()
  if not border_str.get():
    default_border_str()
  if not matrix_str.get():
    default_matrix_str()
  if not speed_str.get():
    default_speed_str()
  if not force_str.get():
    default_force_str()
  if not cut_mode_str.get():
    default_cut_mode_str()
  if not merge_str.get():
    default_merge_str()
  if not merge_threshold_str.get():
    default_merge_threshold_str()
    
  offset = floats(offset_str.get())
  border = floats(border_str.get())
  matrix = floats(matrix_str.get())
  speed = floats(speed_str.get())
  force = floats(force_str.get())
  cut_mode = int(cut_mode_str.get())
  merge = int(merge_str.get())
  merge_threshold = floats(merge_threshold_str.get())

  #
  # main program
  #

  import graphtec
  import pic
  import optimize
  import mergepads
  import svgwriter

  g = graphtec.graphtec()

  g.start()

  g.set(offset=(offset[0]+border[0]+0.5,offset[1]+border[1]+0.5), matrix=matrix)
  strokes = pic.read_pic(temp_pic)

  if not merge==0:
  # merge multiple smaller pads to bigger pads spanning the same area; gracefully handle errors
    try:
      strokes = mergepads.fix_small_geometry(strokes, merge_threshold[0], merge_threshold[1])
    except Exception as err:
      sys.stdout = original_stdout  # restore STDOUT back to its original value
      tkMessageBox.showerror("G2G_GUI ERROR", err)
      return

  max_x,max_y = optimize.max_extent(strokes)

  tx,ty = 0.5,0.5

  border_path = [
    (-border[0], -border[1]),
    (max_x+border[0], -border[1]),
    (max_x+border[0], max_y+border[1]),
    (-border[0], max_y+border[1])
  ]

  if cut_mode==0:
    lines = optimize.optimize(strokes, border)
    for (s,f) in zip(speed,force):
      g.set(speed=s, force=f)
      for x in lines:
        g.line(*x)
#      if border[0]!=0 or border[1]!=0:    # Only draw border if non-zero
        g.closed_path(border_path)
  else:
    for (s,f) in zip(speed,force):
      g.set(speed=s, force=f)
      for s in strokes:
        g.closed_path(s)
 #     if border[0]!=0 or border[1]!=0:    # Only draw border if non-zero
        g.closed_path(border_path)

  svgwriter.svg_strokes("_tmp_gerber.svg", [[strokes, 'black']])

  g.end()

  if Output_name.get():
    sys.stdout = original_stdout  # restore STDOUT back to its original value
    tkMessageBox.showinfo("G2G_GUI Message", "File '%s' created"  % (Output_name.get()) )

def Save_Configuration():
    f = open(CONFPATH,'w')
    f.write(Gerber_name.get() + '\n')
    f.write(Output_name.get() + '\n')
    f.write(gerbv_path.get() + '\n')
    f.write(pstoedit_path.get() + '\n')
    f.write(offset_str.get() + '\n')
    f.write(border_str.get() + '\n')
    f.write(matrix_str.get() + '\n')
    f.write(speed_str.get() + '\n')
    f.write(force_str.get() + '\n')
    f.write(cut_mode_str.get() + '\n')
    f.write(merge_str.get() + '\n')
    f.write(merge_threshold_str.get() + '\n')
    f.write(cutter_shared_name_str.get() + '\n')
    f.close()

def Just_Exit():
    top.destroy()

def Send_to_Cutter():
    if not Output_name.get():
      get_output_filename()
    if not Output_name.get():
      return
    src=os.path.normpath(Output_name.get())
    
    if not cutter_shared_name_str.get():
      tkMessageBox.showerror("G2G_GUI ERROR", "The name of the cutter (as a shared printer) was not provided.")
      return

    #if not os.path.exists(cutter_shared_name_str.get()):
    #  tkMessageBox.showerror("G2G_GUI ERROR", "The name of the cutter (as a shared printer) does not exist.")
    #  return
    
    dst=os.path.normpath(cutter_shared_name_str.get())
    if os.name=='nt':
      os.system("copy /B \"%s\" \"%s\"" % (src, dst))
    else:
      if sys.platform=='darwin':
        os.system("./file2graphtec %s &" % (src))
      else:
        os.system("cat %s > %s" % (src, dst))

def show_in_gerbv():
    src=os.path.normpath(Gerber_name.get())
    if os.name=='nt':
      os.system("\"%s\" %s &" % (os.path.normpath(gerbv_path.get()), src))
    else:
      os.system("gerbv %s &" % (src))

def show_help():
    tkMessageBox.showinfo("Help", help_text)

def get_input_filename():
    input_filename=tkFileDialog.askopenfilename(title='Select paste mask Gerber file', initialdir= os.path.dirname(Gerber_name.get()), filetypes=[('Gerber File', '*.gbr;*.gtp;*.gbp'),("All files", "*.*")] )
    if input_filename:
        Gerber_name.set(input_filename)

def get_output_filename():
    output_filename=tkFileDialog.asksaveasfilename(title='Select output filename', initialfile=Gerber_name.get().rsplit( ".", 1 )[0], defaultextension='.gpgl', filetypes=[('Output files', '*.gpgl'),("All files", "*.*")] )
    if output_filename:
        Output_name.set(output_filename)

def get_gerbv_path():
    gerbv_filename=tkFileDialog.askopenfilename(title='Select gerbv program', initialdir= os.path.dirname(gerbv_path.get()), initialfile='gerbv.exe', filetypes=[('Programs', '*.exe')] )
    if gerbv_filename:
        gerbv_path.set(gerbv_filename)

def get_pstoedit_path():
    pstoedit_filename=tkFileDialog.askopenfilename(title='Select pstoedit program', initialdir= os.path.dirname(pstoedit_path.get()), initialfile='pstoedit.exe', filetypes=[('Programs', '*.exe')] )
    if pstoedit_filename:
        pstoedit_path.set(pstoedit_filename)

def default_offset_str():
    offset_str.set("4.0,0.5")
    
def default_border_str():
    border_str.set("1,1")
    
def default_matrix_str():
    matrix_str.set("1,0,0,1")

def default_speed_str():
    speed_str.set("2,2")

def default_force_str():
    force_str.set("8,30")
    
def default_cut_mode_str():
    cut_mode_str.set("0")

def default_merge_str():
    merge_str.set("0")

def default_merge_threshold_str():
    merge_threshold_str.set("0.012,0.01")

Label(top, text="Gerber File ").grid(row=1, column=0, sticky=W)
Entry(top, bd =1, width=60, textvariable=Gerber_name).grid(row=1, column=1)
Tkinter.Button(top, width=9, text = "Browse", command = get_input_filename).grid(row=1, column=2)

Label(top, text="Output File ").grid(row=2, column=0, sticky=W)
Entry(top, bd =1, width=60, textvariable=Output_name).grid(row=2, column=1)
Tkinter.Button(top, width=9, text = "Browse", command = get_output_filename).grid(row=2, column=2)

if os.name=='nt':
  Label(top, text="gerbv path ").grid(row=3, column=0, sticky=W)
  Entry(top, bd =1, width=60, textvariable=gerbv_path).grid(row=3, column=1)
  Tkinter.Button(top, width=9, text = "Browse", command = get_gerbv_path).grid(row=3, column=2)

  Label(top, text="pstoedit path ").grid(row=4, column=0, sticky=W)
  Entry(top, bd =1, width=60, textvariable=pstoedit_path).grid(row=4, column=1)
  Tkinter.Button(top, width=9, text = "Browse", command = get_pstoedit_path).grid(row=4, column=2)

Label(top, text="Offset ").grid(row=5, column=0, sticky=W)
Entry(top, bd =1, width=60, textvariable=offset_str).grid(row=5, column=1)
Tkinter.Button(top, width=9, text = "Default", command = default_offset_str).grid(row=5, column=2)

Label(top, text="Border ").grid(row=6, column=0, sticky=W)
Entry(top, bd =1, width=60, textvariable=border_str).grid(row=6, column=1)
Tkinter.Button(top, width=9, text = "Default", command = default_border_str).grid(row=6, column=2)

Label(top, text="Matrix ").grid(row=7, column=0, sticky=W)
Entry(top, bd =1, width=60, textvariable=matrix_str).grid(row=7, column=1)
Tkinter.Button(top, width=9, text = "Default", command = default_matrix_str).grid(row=7, column=2)

Label(top, text="Speed ").grid(row=8, column=0, sticky=W)
Entry(top, bd =1, width=60, textvariable=speed_str).grid(row=8, column=1)
Tkinter.Button(top, width=9, text = "Default", command = default_speed_str).grid(row=8, column=2)

Label(top, text="Force ").grid(row=9, column=0, sticky=W)
Entry(top, bd =1, width=60, textvariable=force_str).grid(row=9, column=1)
Tkinter.Button(top, width=9, text = "Default", command = default_force_str).grid(row=9, column=2)

Label(top, text="Cut Mode ").grid(row=10, column=0, sticky=W)
Entry(top, bd =1, width=60, textvariable=cut_mode_str).grid(row=10, column=1)
Tkinter.Button(top, width=9, text = "Default", command = default_cut_mode_str).grid(row=10, column=2)

Label(top, text="Merge ").grid(row=11, column=0, sticky=W)
Entry(top, bd =1, width=60, textvariable=merge_str).grid(row=11, column=1)
Tkinter.Button(top, width=9, text = "Default", command = default_merge_str).grid(row=11, column=2)

Label(top, text="Merge Threshold").grid(row=12, column=0, sticky=W)
Entry(top, bd =1, width=60, textvariable=merge_threshold_str).grid(row=12, column=1)
Tkinter.Button(top, width=9, text = "Default", command = default_merge_threshold_str).grid(row=12, column=2)

if os.name=='nt':
  Label(top, text="Cutter Shared Name").grid(row=13, column=0, sticky=W)
else:
  if not sys.platform=='darwin':
    Label(top, text="Cutter Device Name").grid(row=13, column=0, sticky=W)
Entry(top, bd =1, width=60, textvariable=cutter_shared_name_str).grid(row=13, column=1, sticky=E)

Tkinter.Button(top, width=40, text = "View Gerber file in gerbv", command = show_in_gerbv).grid(row=14, column=1)
Tkinter.Button(top, width=40, text = "Create Graphtec File", command = main_program).grid(row=15, column=1)
Tkinter.Button(top, width=40, text = "Send Graphtec File to Silhouette Cutter", command = Send_to_Cutter).grid(row=16, column=1)
Tkinter.Button(top, width=40, text = "Save Configuration", command = Save_Configuration).grid(row=17, column=1)
Tkinter.Button(top, width=40, text = "Help", command = show_help).grid(row=18, column=1)
Tkinter.Button(top, width=40, text = "Exit", command = Just_Exit).grid(row=19, column=1)

if path.isfile(CONFPATH) and access(CONFPATH, R_OK):
    f = open(CONFPATH,'r')
    input_filename = f.readline()
    input_filename = input_filename.strip()
    output_filename = f.readline()
    output_filename = output_filename.strip()
    gerbv_filename = f.readline()
    gerbv_filename = gerbv_filename.strip()
    pstoedit_filename = f.readline()
    pstoedit_filename = pstoedit_filename.strip()
    offset_text =  f.readline()
    offset_text = offset_text.strip()
    border_text =  f.readline()
    border_text = border_text.strip()
    matrix_text =  f.readline()
    matrix_text = matrix_text.strip()
    speed_text =  f.readline()
    speed_text = speed_text.strip()
    force_text =  f.readline()
    force_text = force_text.strip()
    cut_mode_text =  f.readline()
    cut_mode_text = cut_mode_text.strip()
    merge_text =  f.readline()
    merge_text = merge_text.strip()
    merge_threshold_text =  f.readline()
    merge_threshold_text = merge_threshold_text.strip()
    cutter_shared_name_text =  f.readline()
    cutter_shared_name_text = cutter_shared_name_text.strip()
    f.close()

if not input_filename:
    input_filename=""
if not output_filename:
    output_filename="result.gpgl"
if not gerbv_filename:
    if os.name=='nt':
        gerbv_filename="C:/Program Files (x86)/gerbv-2.6.0/bin/gerbv.exe"
    else:
        gerbv_filename="gerbv"
if not pstoedit_filename:
    if os.name=='nt':
        pstoedit_filename="C:/Program Files/pstoedit/pstoedit.exe"
    else:
        pstoedit_filename="pstoedit"
if not offset_text:
    offset_text="4.0,0.5"
if not border_text:
    border_text="1,1"
if not matrix_text:
    matrix_text="1,0,0,1"
if not speed_text:
    speed_text="2,2"
if not force_text:
    force_text="8,30"
if not cut_mode_text:
    cut_mode_text="0"
if not merge_text:
    merge_text="0"
if not merge_threshold_text:
    merge_threshold="0.012,0.01"
if not cutter_shared_name_text:
    if os.name=='nt':
        cutter_shared_name_text="\\\\[Computer Name]\\[Shared Name]"
    else:
        cutter_shared_name_text="/dev/usb/lp0"

Gerber_name.set(input_filename)
Output_name.set(output_filename)
gerbv_path.set(gerbv_filename)
pstoedit_path.set(pstoedit_filename)
offset_str.set(offset_text)
border_str.set(border_text)
matrix_str.set(matrix_text)
speed_str.set(speed_text)
force_str.set(force_text)
cut_mode_str.set(cut_mode_text)
merge_str.set(merge_text)
merge_threshold_str.set(merge_threshold_text)
cutter_shared_name_str.set(cutter_shared_name_text)

top.mainloop()
