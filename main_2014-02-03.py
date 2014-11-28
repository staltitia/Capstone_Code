#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

class MainWindow:

	def destroyWindow(self, widget, window):
		window.destroy()

	def changeMode(self, widget, inVal):
		#print "mode changed"
		#how it should work
		self.currentMode.set_label(inVal)
		
	def inputModeChange(self, widget, inVal):
		if inVal == "Secondary Electron":
			self.SEButton.set_sensitive(False)
			self.xRayButton.set_sensitive(True)
			self.auxButton.set_sensitive(True)
		elif inVal == "X-Ray":
			self.SEButton.set_sensitive(True)
			self.xRayButton.set_sensitive(False)
			self.auxButton.set_sensitive(True)
		elif inVal == "Auxiliary":
			self.SEButton.set_sensitive(True)
			self.xRayButton.set_sensitive(True)
			self.auxButton.set_sensitive(False)
		
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
	
	def makeScreenshot(self, widget, data=None):
		#print "Make Screenshot"
		#make a new window
		screenshotWindow = gtk.Window(gtk.WINDOW_POPUP)
		pos = self.window.get_position()
		screenshotWindow.move(pos[0], pos[1])
		
		screenshotWindow.set_border_width(10)
		
		screenshotWindow.set_title("Screenshot")
		mainBox = gtk.VBox()
		doneButton = gtk.Button("Done")
		doneButton.connect("clicked", self.destroyWindow, screenshotWindow)
		
		mainBox.pack_end(doneButton, expand=True, fill = False)
		
		screenshotWindow.add(mainBox)
		
		self.image = gtk.Image()
		self.image.set_from_file("placeholder.bmp")
		mainBox.pack_start(self.image, expand=True, fill = True)
		
		updateButton = gtk.Button("Update Image")
		#saveButton.connect("clicked", self.saveImage, screenshotWindow)
		
		mainBox.pack_end(updateButton, expand=True, fill = False)
		
		self.image.show()
		doneButton.show()
		updateButton.show()
		mainBox.show()
		screenshotWindow.show()
	
	def __init__(self):
	
		# initialise the variables
		self.xShift = 0
		self.yShift = 0
		self.xStig = 0
		self.yStif = 0
		self.objLens = 0
		self.conLens = 0
		self.filament = 0
		
		#make an empty list of objects to show
		toShow = []
	
		# create a new window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		toShow.append(self.window)
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
		
		#next, we make the layout boxes of the window
		self.mainBox = gtk.VBox()
		toShow.append(self.mainBox)
		
		self.window.add(self.mainBox)
		
		self.bottomBox = gtk.HBox()
		toShow.append(self.bottomBox)
		
		self.mainBox.pack_end(self.bottomBox, fill=False)
		
		self.textFirst = gtk.Label("Get Screenshot")
		toShow.append(self.textFirst)
		self.buttonFirst = gtk.Button("Start")
		toShow.append(self.buttonFirst)

		self.buttonFirst.connect("clicked", self.makeScreenshot, None)
		
		self.bottomBox.pack_start(self.textFirst, fill=False)
		self.bottomBox.pack_end(self.buttonFirst, fill=False)
		
		#mode buttons
		
		self.modeButtonBox = gtk.HBox()
		toShow.append(self.modeButtonBox)
		self.mainBox.pack_start(self.modeButtonBox, fill=False)
		
		self.modeButtonSubBox1 = gtk.VBox()
		toShow.append(self.modeButtonSubBox1)
		self.modeButtonSubBox2 = gtk.VBox()
		toShow.append(self.modeButtonSubBox2)
		self.modeButtonBox.pack_start(self.modeButtonSubBox1, fill=False)
		self.modeButtonBox.pack_start(self.modeButtonSubBox2, fill=False)
		
		self.modeLabel = gtk.Label("Current mode :")
		toShow.append(self.modeLabel)
		self.currentMode = gtk.Label("Slow 1")
		toShow.append(self.currentMode)
		self.modeButtonSubBox1.pack_start(self.modeLabel, fill=False)
		self.modeButtonSubBox1.pack_start(self.currentMode, fill=False)
		
		self.modeButtonSubBox2Top = gtk.HBox()
		toShow.append(self.modeButtonSubBox2Top)
		self.modeButtonSubBox2Bot = gtk.HBox()
		toShow.append(self.modeButtonSubBox2Bot)
		self.modeButtonSubBox2.pack_start(self.modeButtonSubBox2Top, fill=False)
		self.modeButtonSubBox2.pack_start(self.modeButtonSubBox2Bot, fill=False)
		
		self.slowOneButton = gtk.Button("Slow 1")
		toShow.append(self.slowOneButton)
		self.slowTwoButton = gtk.Button("Slow 2")
		toShow.append(self.slowTwoButton)
		self.photoButton = gtk.Button("Photo")
		toShow.append(self.photoButton)
		self.fastButton = gtk.Button("Fast")
		toShow.append(self.fastButton)
		self.TVButton = gtk.Button("TV")
		toShow.append(self.TVButton)
		
		self.modeButtonSubBox2Top.pack_start(self.slowOneButton, fill=False)
		self.modeButtonSubBox2Top.pack_start(self.slowTwoButton, fill=False)
		self.modeButtonSubBox2Top.pack_start(self.photoButton, fill=False)
		self.modeButtonSubBox2Bot.pack_start(self.fastButton, fill=False)
		self.modeButtonSubBox2Bot.pack_start(self.TVButton, fill=False)
		
		self.slowOneButton.connect("clicked", self.changeMode, self.slowOneButton.get_label())
		self.slowTwoButton.connect("clicked", self.changeMode, self.slowTwoButton.get_label())
		self.photoButton.connect("clicked", self.changeMode, self.photoButton.get_label())
		self.fastButton.connect("clicked", self.changeMode, self.fastButton.get_label())
		self.TVButton.connect("clicked", self.changeMode, self.TVButton.get_label())
		
		# next, we set up buttons that choose input type
		# values are either secondary electrons, x-ray or auxillary
		
		self.collectionModeButtonBox = gtk.HBox()
		toShow.append(self.collectionModeButtonBox)
		self.mainBox.pack_start(self.collectionModeButtonBox, fill=False)
		
		self.inputTypeLabel = gtk.Label("Input type: ")
		toShow.append(self.inputTypeLabel)
		self.collectionModeButtonBox.pack_start(self.inputTypeLabel, fill=False)
		
		self.SEButton = gtk.Button("Secondary Electron")
		toShow.append(self.SEButton)
		self.collectionModeButtonBox.pack_start(self.SEButton, fill=False)
		self.xRayButton = gtk.Button("X-Ray")
		toShow.append(self.xRayButton)
		self.collectionModeButtonBox.pack_start(self.xRayButton, fill=False)
		self.auxButton = gtk.Button("Auxiliary")
		toShow.append(self.auxButton)
		self.collectionModeButtonBox.pack_start(self.auxButton, fill=False)
		
		self.SEButton.connect("clicked", self.inputModeChange, self.SEButton.get_label())
		self.xRayButton.connect("clicked", self.inputModeChange, self.xRayButton.get_label())
		self.auxButton.connect("clicked", self.inputModeChange, self.auxButton.get_label())
		
		# sliders/spinbuttons
		# format is: 
		# Name of variable; value in spinbutton; slider that is connected to the same variable
		
		#-------------------------------------------------------------------------------------------------
		
		self.shiftXBox = gtk.HBox()
		self.mainBox.pack_start(self.shiftXBox, fill=False)
		toShow.append(self.shiftXBox)
		self.shiftXLabel = gtk.Label("X Shift")
		toShow.append(self.shiftXLabel)
		self.shiftXBox.pack_start(self.shiftXLabel, fill=False)
		
		self.shiftXAdjustment = gtk.Adjustment(value=0, lower=-100, upper=100, step_incr=1, page_incr=10)
		self.shiftXSpinButton = gtk.SpinButton(adjustment=self.shiftXAdjustment, climb_rate=0.0, digits=0)
		toShow.append(self.shiftXSpinButton)
		self.shiftXBox.pack_start(self.shiftXSpinButton, fill=False)
		self.shiftXSlider = gtk.HScale(adjustment=self.shiftXAdjustment)
		toShow.append(self.shiftXSlider)
		self.shiftXBox.pack_start(self.shiftXSlider, fill=True)
		
		#-------------------------------------------------------------------------------------------------
		
		self.shiftYBox = gtk.HBox()
		self.mainBox.pack_start(self.shiftYBox, fill=False)
		toShow.append(self.shiftYBox)
		self.shiftYLabel = gtk.Label("Y Shift")
		toShow.append(self.shiftYLabel)
		self.shiftYBox.pack_start(self.shiftYLabel, fill=False)
		
		self.shiftYAdjustment = gtk.Adjustment(value=0, lower=-100, upper=100, step_incr=1, page_incr=10)
		
		self.shiftYSpinButton = gtk.SpinButton(adjustment=self.shiftYAdjustment, climb_rate=0.0, digits=0)
		toShow.append(self.shiftYSpinButton)
		self.shiftYBox.pack_start(self.shiftYSpinButton, fill=False)
		
		self.shiftYSlider = gtk.HScale(adjustment=self.shiftYAdjustment)
		toShow.append(self.shiftYSlider)
		self.shiftYBox.pack_start(self.shiftYSlider, fill=True)
		
		#-------------------------------------------------------------------------------------------------
		
		self.stigXBox = gtk.HBox()
		self.mainBox.pack_start(self.stigXBox, fill=False)
		toShow.append(self.stigXBox)
		self.stigXLabel = gtk.Label("X Stigmation")
		toShow.append(self.stigXLabel)
		self.stigXBox.pack_start(self.stigXLabel, fill=False)
		
		self.stigXAdjustment = gtk.Adjustment(value=0, lower=-100, upper=100, step_incr=1, page_incr=10)
		
		self.stigXSpinButton = gtk.SpinButton(adjustment=self.stigXAdjustment, climb_rate=0.0, digits=0)
		toShow.append(self.stigXSpinButton)
		self.stigXBox.pack_start(self.stigXSpinButton, fill=False)
		
		self.stigXSlider = gtk.HScale(adjustment=self.stigXAdjustment)
		toShow.append(self.stigXSlider)
		self.stigXBox.pack_start(self.stigXSlider, fill=True)
		
		#-------------------------------------------------------------------------------------------------
		
		self.stigYBox = gtk.HBox()
		self.mainBox.pack_start(self.stigYBox, fill=False)
		toShow.append(self.stigYBox)
		self.stigYLabel = gtk.Label("Y Stigmation")
		toShow.append(self.stigYLabel)
		self.stigYBox.pack_start(self.stigYLabel, fill=False)
		
		self.stigYAdjustment = gtk.Adjustment(value=0, lower=-100, upper=100, step_incr=1, page_incr=10)
		
		self.stigYSpinButton = gtk.SpinButton(adjustment=self.stigYAdjustment, climb_rate=0.0, digits=0)
		toShow.append(self.stigYSpinButton)
		self.stigYBox.pack_start(self.stigYSpinButton, fill=False)
		
		self.stigYSlider = gtk.HScale(adjustment=self.stigYAdjustment)
		toShow.append(self.stigYSlider)
		self.stigYBox.pack_start(self.stigYSlider, fill=True)
		
		#-------------------------------------------------------------------------------------------------
		
		self.condBox = gtk.HBox()
		self.mainBox.pack_start(self.condBox, fill=False)
		toShow.append(self.condBox)
		self.condLabel = gtk.Label("Condenser Lens")
		toShow.append(self.condLabel)
		self.condBox.pack_start(self.condLabel, fill=False)
		
		self.condAdjustment = gtk.Adjustment(value=0, lower=-100, upper=100, step_incr=1, page_incr=10)
		
		self.condSpinButton = gtk.SpinButton(adjustment=self.condAdjustment, climb_rate=0.0, digits=0)
		toShow.append(self.condSpinButton)
		self.condBox.pack_start(self.condSpinButton, fill=False)
		
		self.condSlider = gtk.HScale(adjustment=self.condAdjustment)
		toShow.append(self.condSlider)
		self.condBox.pack_start(self.condSlider, fill=True)
		
		#-------------------------------------------------------------------------------------------------
		
		self.objBox = gtk.HBox()
		self.mainBox.pack_start(self.objBox, fill=False)
		toShow.append(self.objBox)
		self.objLabel = gtk.Label("Objective Lens")
		toShow.append(self.objLabel)
		self.objBox.pack_start(self.objLabel, fill=False)
		
		self.objAdjustment = gtk.Adjustment(value=0, lower=-100, upper=100, step_incr=1, page_incr=10)
		
		self.objSpinButton = gtk.SpinButton(adjustment=self.objAdjustment, climb_rate=0.0, digits=0)
		toShow.append(self.objSpinButton)
		self.objBox.pack_start(self.objSpinButton, fill=False)
		
		self.objSlider = gtk.HScale(adjustment=self.objAdjustment)
		toShow.append(self.objSlider)
		self.objBox.pack_start(self.objSlider, fill=True)
		
		#-------------------------------------------------------------------------------------------------
		
		self.filaBox = gtk.HBox()
		self.mainBox.pack_start(self.filaBox, fill=False)
		toShow.append(self.filaBox)
		self.filaLabel = gtk.Label("Filament Current")
		toShow.append(self.filaLabel)
		self.filaBox.pack_start(self.filaLabel, fill=False)
		
		self.filaAdjustment = gtk.Adjustment(value=0, lower=-100, upper=100, step_incr=1, page_incr=10)
		
		self.filaSpinButton = gtk.SpinButton(adjustment=self.filaAdjustment, climb_rate=0.0, digits=0)
		toShow.append(self.filaSpinButton)
		self.filaBox.pack_start(self.filaSpinButton, fill=False)
		
		self.filaSlider = gtk.HScale(adjustment=self.filaAdjustment)
		toShow.append(self.filaSlider)
		self.filaBox.pack_start(self.filaSlider, fill=True)
		
		#-------------------------------------------------------------------------------------------------
		
		self.magBox = gtk.HBox()
		self.mainBox.pack_start(self.magBox, fill=False)
		toShow.append(self.magBox)
		self.magLabel = gtk.Label("Magnification")
		toShow.append(self.magLabel)
		self.magBox.pack_start(self.magLabel, fill=False)
		
		self.magAdjustment = gtk.Adjustment(value=0, lower=-100, upper=100, step_incr=1, page_incr=10)
		
		self.magSpinButton = gtk.SpinButton(adjustment=self.magAdjustment, climb_rate=0.0, digits=0)
		toShow.append(self.magSpinButton)
		self.magBox.pack_start(self.magSpinButton, fill=False)
		
		self.magSlider = gtk.HScale(adjustment=self.magAdjustment)
		toShow.append(self.magSlider)
		self.magBox.pack_start(self.magSlider, fill=True)
		
		#-------------------------------------------------------------------------------------------------
		
		# connectivity / sync values
		# format is:
		# "Connecttion status; connected flag value; ungrey reconnect button if connected flag lowered
		# "Sync status; sync flag value; ungrey resync if connected and sync flag lowered
		
		self.connectBox = gtk.HBox()
		toShow.append(self.connectBox)
		self.mainBox.pack_start(self.connectBox, fill=False)
		
		self.syncBox = gtk.HBox()
		toShow.append(self.syncBox)
		self.mainBox.pack_start(self.syncBox, fill=False)
		
		self.connectLabel = gtk.Label("Connection status: not connected")
		toShow.append(self.connectLabel)
		self.connectBox.pack_start(self.connectLabel, fill=False)
		
		self.connectButton = gtk.Button("Reconnect")
		toShow.append(self.connectButton)
		self.connectBox.pack_start(self.connectButton, fill=False)
		#TODO
		#self.connectButton.connect("clicked", self.changeMode, None)
		
		self.syncLabel = gtk.Label("Sync status: not connected")
		toShow.append(self.syncLabel)
		self.syncBox.pack_start(self.syncLabel, fill=False)
		self.syncButton = gtk.Button("Resync")
		toShow.append(self.syncButton)
		self.syncBox.pack_start(self.syncButton, fill=False)
		#TODO
		#self.syncButton.connect("clicked", self.changeMode, None)
		
		#-------------------------------------------------------------------------------------------------
		
		# The final step is to display all widgets.
		
		for i in toShow:
			i.show()
		
	def main(self):
		# All PyGTK applications must have a gtk.main(). Control ends here
		# and waits for an event to occur (like a key press or mouse event).
		gtk.main()

if __name__ == "__main__":
	pool = MainWindow()
	pool.main()