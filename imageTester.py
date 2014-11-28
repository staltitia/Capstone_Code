#!/usr/bin/env python

# example helloworld.py

import pygtk
pygtk.require('2.0')
import gtk
import numpy

class HelloWorld:

    # This is a callback function. The data arguments are ignored
    # in this example. More on callbacks below.
    def hello(self, widget, data=None):
		print "Hello World"

    def delete_event(self, widget, event, data=None):
		# If you return FALSE in the "delete_event" signal handler,
		# GTK will emit the "destroy" signal. Returning TRUE means
		# you don't want the window to be destroyed.
		# This is useful for popping up 'are you sure you want to quit?'
		# type dialogs.
		print "delete event occurred"

		# Change FALSE to TRUE and the main window will not be destroyed
		# with a "delete_event".
		return False

    def destroy(self, widget, data=None):
		print "destroy signal occurred"
		gtk.main_quit()

    def __init__(self):
		# create a new window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		print "initialising"
		# When the window is given the "delete_event" signal (this is given
		# by the window manager, usually by the "close" option, or on the
		# titlebar), we ask it to call the delete_event () function
		# as defined above. The data passed to the callback
		# function is NULL and is ignored in the callback function.
		self.window.connect("delete_event", self.delete_event)
		
		# Here we connect the "destroy" event to a signal handler.  
		# This event occurs when we call gtk_widget_destroy() on the window,
		# or if we return FALSE in the "delete_event" callback.
		self.window.connect("destroy", self.destroy)
			
		# Sets the border width of the window.
		self.window.set_border_width(10)
		
		pixbuf = makePixbuff()
		pixbuf.save("tester file.jpg", 'jpeg')
    
		mainBox = gtk.VBox()
		
		image = gtk.Image()
		image.set_from_file("tester file.jpg")
		mainBox.pack_start(image, expand=True, fill = True)
		
		self.window.add(mainBox)
			
		# The final step is to display this newly created widget.
		#self.button.show()
		image.show()
		# and the window
		self.window.show()

    def main(self):
		# All PyGTK applications must have a gtk.main(). Control ends here
		# and waits for an event to occur (like a key press or mouse event).
		gtk.main()

def makePixbuff():
	width = 640
	height = 480
	dataType = numpy.dtype('b')
	imageList = []
	print "begin"
	for i in range(height):
		row = range(width)
		row = [ [chr(x%256), chr(x%256), chr(x%256)] for x in row ]
		row = [ item for sublist in row for item in sublist ]
		imageList.append(row)
	image = [ item for sublist in imageList for item in sublist ]
	pixbuff = gtk.gdk.pixbuf_new_from_data(''.join(image), gtk.gdk.COLORSPACE_RGB, False, 8, width, height, 3*width)
	return pixbuff


# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
    hello = HelloWorld()
    hello.main()