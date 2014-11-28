#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

class MainWindow:

	def destroyWindow(self, widget, window):
		window.destroy()

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
	
	def functionA(self, widget, data=None):
		print "function 1"
		#make a new window
		screenshotWindow = gtk.Window(gtk.WINDOW_POPUP)
		#screenshotWindow.set_default_size(800,600)
		screenshotWindow.set_gravity(gtk.gdk.GRAVITY_CENTER)
		print screenshotWindow.get_position()
		screenshotWindow.set_border_width(10)
		
		screenshotWindow.set_title("Screenshot")
		mainBox = gtk.VBox()
		doneButton = gtk.Button("Done")
		doneButton.connect("clicked", self.destroyWindow, screenshotWindow)
		
		mainBox.pack_end(doneButton, expand=True, fill = False)
		
		screenshotWindow.add(mainBox)
		
		doneButton.show()
		mainBox.show()
		screenshotWindow.show()
		
	def functionB(self, widget, data=None):
		print "function 2"
	
	def functionC(self, widget, data=None):
		print "function 3"
	
	def __init__(self):
		# create a new window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title("SEM Control Panel")
		#self.window.set_default_size(800,600)
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
		#self.window.set_border_width(10)
		
		self.mainBox = gtk.HBox()
		
		self.textBox = gtk.VBox()
		self.buttonBox = gtk.VBox()
		
		self.mainBox.pack_start(self.textBox, fill=False)
		self.mainBox.pack_start(self.buttonBox, fill=False)
		
		self.textFirst = gtk.Label("First Button")
		self.textSecond = gtk.Label("Second Button")
		self.textThird = gtk.Label("Third Button")
		self.buttonFirst = gtk.Button("One")
		self.buttonSecond = gtk.Button("Two")
		self.buttonThird = gtk.Button("Three")

		self.buttonFirst.connect("clicked", self.functionA, None)
		self.buttonSecond.connect("clicked", self.functionB, None)
		self.buttonThird.connect("clicked", self.functionC, None)
		
		self.textBox.pack_start(self.textFirst, fill=False)
		self.textBox.pack_start(self.textSecond, fill=False)
		self.textBox.pack_start(self.textThird, fill=False)
		
		self.buttonBox.pack_start(self.buttonFirst, fill=False)
		self.buttonBox.pack_start(self.buttonSecond, fill=False)
		self.buttonBox.pack_start(self.buttonThird, fill=False)
		
		self.window.add(self.mainBox)
		
		# The final step is to display this newly created widget.

		self.textFirst.show()
		self.textSecond.show()
		self.textThird.show()

		self.buttonFirst.show()
		self.buttonSecond.show()
		self.buttonThird.show()
		
		self.textBox.show()
		self.buttonBox.show()
		self.mainBox.show()
		
		# and the window
		self.window.show()
		
	def main(self):
		# All PyGTK applications must have a gtk.main(). Control ends here
		# and waits for an event to occur (like a key press or mouse event).
		gtk.main()

if __name__ == "__main__":
	pool = MainWindow()
	pool.main()