Silhouette Series Driver Ver.1.20
for Microsoft Windows XP x64 Edition/Windows Vista x64 Edition/
    Windows 7 x64 Edition/Windows 8 x64 Edition

Thank you for choosing the Silhouette Series Driver.
The file provides instructions and notes on installation and operation as well
as other information.
Be sure to read through this file carefully before attempting to use this driver.


CONTENTS

  1. OVERVIEW

  2. CONFIGURING THE Silhouette Series DRIVER
     2-1  Selecting the Paper Size
     2-2  Use Carrier Sheet
     2-3  Selecting the Design Orientation
     2-4  Setting the Unit
     2-5  Ejecting the Medium
     2-6  Setting the Offset for the Origin Point
     2-7  Controller
     2-8  Cutline Settings
     2-9  Setting the Allowable Color Value Range
     2-10 Dashed Line Pattern Settings
     2-11 Saving the Settings to a File

  3. NOTES ON USE


1. OVERVIEW

This driver was designed for use with Silhouette America-specified
application software that supports Silhouette Series.
Correct performance of this driver is not guaranteed if application
software that is not specified by Silhouette America is used.


2. CONFIGURING THE PLOTTER DRIVER

 2-1 Selecting the Paper Size

 The Paper Size parameter determines the Silhouette Series effective plot (cutting) area
 according to the settings of the Paper Size and Margin parameters.

 The Paper Size can be set to ISO A4; Letter; 12 x 12 inch; 12 x 24 inch;
 User Size 1 to 6; or Specify Within Application.

 The resulting effective plot area will consist of the respectively specified
 paper size, minus the margins on all four sides of each page. The width of the
 margins will vary according to whether Standard or Expanded has been selected.


  Note: "Specify within application" uses the paper size specified within an
        application.
        Select this option when using an application that replaces the paper
        size set by the driver with one that is specified within the application.
        If no paper size is specified within an application while "Specify
        within application" is selected, the default value (210 mm x 297 mm) is
        assumed.

  Setting the Paper Size
     Either open the driver's [Properties] menu from the [Printers] menu under
     [Settings] or open the Silhouette Series dialog box by selecting <Print
     Setup...> from the <File> menu of the Windows application.
     You are now ready to select the paper size.
     The dimensions of the currently selected paper size appear in the Paper Size box.
     To select a different paper standard, open the Paper Size drop-down list
     box and click the desired size.

 2-2 Use Carrier Sheet

 When using the Carrier sheet for cut, check "Use Carrier Sheet".

 2-3 Selecting the Design Orientation

 To select the design orientation, click the dot preceding Portrait or Landscape.
 A black dot indicates the currently selected design orientation.

   Portrait  : The design is oriented vertically
   Landscape : The design is oriented horizontally

 Note: Be sure to set the design orientation before you generate plot data using
       a Windows application.
       With certain Windows applications, changing the design orientation may
       alter the orientation of previously defined plots.

 2-4 Setting the Unit

 The numerical value display unit can be set to mm or inch.

 2-5 Ejecting the Medium

 If the Eject Medium box is checked (by clicking on it), the medium is fed to the front when
 the cutting operation has been completed.

 2-6 Setting the Offset for the Origin Point

 The Offset parameter is used to offset the position of the coordinate system's origin point.
 The new origin position can be offset in 0.1-mm (0.01-inch) steps to any point within
 the effective plot area.

 Note: When the Offset setting causes the size of an image to exceed the effective plot area,
       its surplus area will be clipped prior to output.

 2-7 Cutline Settings

 This enables you to specify which color is to be used for the cutlines created
 in your software application.

 Procedure
 To add a new setting, click the "Add" button.

 To delete a setting, select the setting you want to delete from the list of cutline
 settings and then click the "Delete" button.

 If you select a cutline setting from the list and then click the "Modify Color" button,
 the "Color Settings" window appears. Specify your cutline color using a combination of
 the RGB elements. If you change the cutline combo box settings, the cutline setting that you
 selected from the list can be modified. If you select "Solid  Cut Line", the lines will be cut
 through. If you select "Dashed Line", the lines will be cut only at the specified intervals.

 2-8 Setting the Allowable Color Value Range

 This specifies the allowable range for the specified color for the cutline with respect to
 the RGB values.
 If the Allowable Color Value Range has been set to 32, for example, the RGB values of the specified
 color are set with a range of Å}32 on either side of that color. All colors that fall within that
 range are handled as Cutlines.

 2-9 Dashed Line Pattern Settings

 The length of both the cut line segments and uncut line segments can be specified in 0.1-mm
 (0.001-inch)increments. If the cutline has been specified as a dashed line, only the specified
 cut line segments will be cut. The cut line segments are combined with the uncut line segments
 to create a dashed line.

 2-10 Saving the Settings to a File

 All the settings made in the Silhouette Series driver, with the exception of the
 outport port setting, can be saved to a file.

 If a file is saved in this way is used with another computer and the Silhouette Series driver is loaded,
 the same settings can be made.

 Save to File Procedure

 1. Click the "Cutline Settings" tab.

 2. Click the "Save As/Load" button to display the "Save As/Load"window.

 3. Click the "Save As" button. A dialog box for entering the file name is displayed.
    Type in a file name, then click the "OK" button.

 4. Click the "Close" button to close the "Save As/Load" window.

 Load File Procedure

 1. Click the "Cutline Settings" tab.

 2. Click the Save As/Load" button to display the "Save As/Load"window.

 3. Click the "Load" button to display the dialog box for selecting a file name.
    Select the required file name, and then click the "OK" button.

 4. Click the Close button to close the "Save As/Load" window.


3. NOTES ON USE

 1. If the printer name is changed, all the settings are returned to their default values.

 2. Even if several pages are specified in the application, Silhouette Series will only cut
   the first page.


Registered trademarks

 Microsoft, Windows Vista, and Windows are either registered trademarks or trademarks of
 Microsoft Corporation in the United States and/or other countries.


END
