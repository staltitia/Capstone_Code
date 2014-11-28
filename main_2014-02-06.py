#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import gobject

import os.path as path
import sys
import time
import fileIO

import threading

gobject.threads_init()

readLock = threading.Lock()

global updateFlag

shiftXVal = 0
shiftYVal = 0
stigXVal = 0
stigYVal = 0
condVal = 0
objVal = 0
filaVal = 0
magVal = 0
updateFlag = False

class commThread(threading.Thread):
	def __init__( self ):
		threading.Thread.__init__(self)
		self.shiftXVal = 0
		self.shiftYVal = 0
		self.stigXVal = 0
		self.stigYVal = 0
		self.condVal = 0
		self.objVal = 0
		self.filaVal = 0
		self.magVal = 0
		self.quit = False
		
	def run(self):
		global readLock

		global shiftXVal
		global shiftYVal
		global stigXVal
		global stigYVal
		global condValx
		global objVal
		global filaVal
		global magVal
		while not self.quit:
			readLock.acquire(True)
			tempShiftXVal = shiftXVal
			tempShiftYVal = shiftYVal
			tempStigXVal = stigXVal
			tempStigYVal = stigYVal
			tempCondVal = condVal
			tempObjVal = objVal
			tempFilaVal = filaVal
			tempMagVal = magVal
			readLock.release()
			
			if self.shiftXVal != tempShiftXVal or self.shiftYVal != tempShiftYVal or self.stigXVal != tempStigXVal or self.stigYVal != tempStigYVal or self.condVal != tempCondVal or self.objVal != tempObjVal or self.filaVal != tempFilaVal or self.magVal != tempMagVal:
				self.shiftXVal = tempShiftXVal
				self.shiftYVal = tempShiftYVal
				self.stigXVal = tempStigXVal
				self.stigYVal = tempStigYVal
				self.condVal = tempCondVal
				self.objVal = tempObjVal
				self.filaVal = tempFilaVal
				self.magVal = tempMagVal
				'''
				this is where it should write to serial port or something
				for now, i just sleep
				'''
				time.sleep(0.1)
				sys.stdout.write("Getting here in thread!\n")

class MainWindow:

	def updateVars(self):
		global readLock
		global updateFlag
		if updateFlag:
			if readLock.acquire(False):
				global shiftXVal
				global shiftYVal
				global stigXVal
				global stigYVal
				global condVal
				global objVal
				global filaVal
				global magVal
				
				shiftXVal = self.shiftXVar
				shiftYVal = self.shiftYVar
				stigXVal = self.stigXVar
				stigYVal = self.stigYVar
				condVal = self.condVar
				objVal = self.objVar
				filaVal = self.filaVar
				magVal = self.magVar
				updateFlag = False
				readLock.release()
			else:
				gobject.idle_add(self.updateVars)

	def destroyWindow(self, widget, window):
		window.destroy()

	def changeMode(self, widget, inVal):
		self.modeVar = inVal
		self.currentMode.set_label(inVal)
		
	def inputModeChangeWrapper(self, widget, inVal):
		self.inputModeChange(inVal)
		
	def inputModeChange(self, inVal):
		if inVal == "Secondary Electron":
			self.SEButton.set_sensitive(False)
			self.xRayButton.set_sensitive(True)
			self.auxButton.set_sensitive(True)
			self.inTypeVar = inVal
		elif inVal == "X-Ray":
			self.SEButton.set_sensitive(True)
			self.xRayButton.set_sensitive(False)
			self.auxButton.set_sensitive(True)
			self.inTypeVar = inVal
		elif inVal == "Auxiliary":
			self.SEButton.set_sensitive(True)
			self.xRayButton.set_sensitive(True)
			self.auxButton.set_sensitive(False)
			self.inTypeVar = inVal
			
	def adjusted(self, widget, inVal=None): #xshift, yshift, xstig, ystig, cond, obj, fila, mag
		global updateFlag
		if inVal == 1: 
			self.shiftXVar = self.shiftXAdjustment.get_value()
		elif inVal == 2:
			self.shiftYVar = self.shiftYAdjustment.get_value()
		elif inVal == 3:
			self.stigXVar = self.stigXAdjustment.get_value()
		elif inVal == 4:
			self.stigYVar = self.stigYAdjustment.get_value()
		elif inVal == 5:
			self.condVar = self.condAdjustment.get_value()
		elif inVal == 6:
			self.objVar = self.objAdjustment.get_value()
		elif inVal == 7:
			self.filaVar = self.filaAdjustment.get_value()
		elif inVal == 8:
			self.magVar = self.magAdjustment.get_value()
		updateFlag = True
		gobject.idle_add(self.updateVars)
		
	def loadFromFile(self, widget, inVal=None):
		chooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
		chooser.show()
		
		filter = gtk.FileFilter()
		filter.set_name("SEM presets file")
		filter.add_pattern("*.ssf")
		chooser.add_filter(filter)
		
		filter = gtk.FileFilter()
		filter.set_name("All files")
		filter.add_pattern("*")
		chooser.add_filter(filter)
		
		response = chooser.run()
		if response == gtk.RESPONSE_OK:
			print chooser.get_filename(), 'selected'
			values = fileIO.readSavedFile(chooser.get_filename())
			for pair in values:
				if pair[0] == "mode":
					self.modeVar = pair[1]
					self.currentMode.set_label(pair[1])
				elif pair[0] == "inType":
					self.inTypeVar = pair[1]
					self.inputModeChange(pair[1])
				elif pair[0] == "xShift":
					self.shiftXVar = float(pair[1])
					self.shiftXAdjustment.set_value(self.shiftXVar)
				elif pair[0] == "yShift":
					self.shiftYVar = float(pair[1])
					self.shiftYAdjustment.set_value(self.shiftYVar)
				elif pair[0] == "xStig":
					self.stigXVar = float(pair[1])
					self.stigXAdjustment.set_value(self.stigXVar)
				elif pair[0] == "yStig":
					self.stigYVar = float(pair[1])
					self.stigYAdjustment.set_value(self.stigYVar)
				elif pair[0] == "condLens":
					self.condVar = float(pair[1])
					self.condAdjustment.set_value(self.condVar)
				elif pair[0] == "objLens":
					self.objVar = float(pair[1])
					self.objAdjustment.set_value(self.objVar)
				elif pair[0] == "filaCurr":
					self.filaVar = float(pair[1])
					self.filaAdjustment.set_value(self.filaVar)
				elif pair[0] == "mag":
					self.magVar = float(pair[1])
					self.magAdjustment.set_value(self.magVar)
				
		elif response == gtk.RESPONSE_CANCEL:
			print 'Closed, no files selected'
		chooser.destroy()
		
	def saveToFile(self, widget, inVal=None):
		chooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
		chooser.show()
		
		filter = gtk.FileFilter()
		filter.set_name("SEM presets file")
		filter.add_pattern("*.ssf")
		chooser.add_filter(filter)
		
		filter = gtk.FileFilter()
		filter.set_name("All files")
		filter.add_pattern("*")
		chooser.add_filter(filter)
		
		response = chooser.run()
		if response == gtk.RESPONSE_OK:
			print "saving as ",chooser.get_filename()		
			#date = time.strftime("%Y-%m-%d_%H_%M_%S", time.gmtime())
			#filename = "SEM presets "+date+".ssf"
			filename = chooser.get_filename()+".ssf"
			values = []
			mode = [ "mode", str(self.modeVar) ]
			inType = [ "inType", str(self.inTypeVar) ]
			xshift = [ "xShift", str(self.shiftXVar) ]
			yshift = [ "yShift", str(self.shiftYVar) ]
			xstig = [ "xStig", str(self.stigXVar) ]
			ystig = [ "yStig", str(self.stigYVar) ]
			cond = [ "condLens", str(self.condVar) ]
			obj = [ "objLens", str(self.objVar) ]
			filacurr = [ "filaCurr", str(self.filaVar) ]
			mag = [ "mag", str(self.magVar) ]
			fileIO.writeSavedFile( filename, [mode,inType,xshift,yshift,xstig,cond,obj,filacurr,mag] )
		elif response == gtk.RESPONSE_CANCEL:
			print 'Closed, no files selected'
		chooser.destroy()
		
	def delete_event(self, widget, event, data=None):
		# If you return FALSE in the "delete_event" signal handler,
		# GTK will emit the "destroy" signal. Returning TRUE means
		# you don't want the window to be destroyed.
		# This is useful for popping up 'are you sure you want to quit?'
		# type dialogs.
		print "delete event occurred"
		self.runThread.quit = True

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
	
		# read initialisation file
		try:
			initVals = fileIO.readInitFile("InitFile.sem")
		except IOError:
			print "Initialisation file not found. Creating new file..."
			fileIO.writeInitFile("InitFile.sem")
			initVals = fileIO.readInitFile("InitFile.sem")
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
		
		#===================== making variable =====================
		self.modeVar = "Slow 1"
		#===================== making variable =====================
		
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
		
		self.SEButton.connect("clicked", self.inputModeChangeWrapper, self.SEButton.get_label())
		self.xRayButton.connect("clicked", self.inputModeChangeWrapper, self.xRayButton.get_label())
		self.auxButton.connect("clicked", self.inputModeChangeWrapper, self.auxButton.get_label())
		
		#===================== making variable =====================
		self.inTypeVar = None
		#===================== making variable =====================
		
		# sliders/spinbuttons
		# format is: 
		# Name of variable; value in spinbutton; slider that is connected to the same variable
		
		#-------------------------------------------------------------------------------------------------
		
		toAdd = [ None, 0, -100, 100, 1, 10 ]
		for varHold in initVals:
			if varHold[0] == "xShift":
				toAdd = varHold
		
		self.shiftXBox = gtk.HBox()
		self.mainBox.pack_start(self.shiftXBox, fill=False)
		toShow.append(self.shiftXBox)
		self.shiftXLabel = gtk.Label("X Shift")
		toShow.append(self.shiftXLabel)
		self.shiftXBox.pack_start(self.shiftXLabel, fill=False)
		
		self.shiftXAdjustment = gtk.Adjustment(value=toAdd[1], lower=toAdd[2], upper=toAdd[3], step_incr=toAdd[4], page_incr=toAdd[5])
		
		#===================== making variable =====================
		self.shiftXVar = self.shiftXAdjustment.get_value()
		#===================== making variable =====================
		
		self.shiftXAdjustment.connect("value_changed", self.adjusted, 1)
		
		self.shiftXSpinButton = gtk.SpinButton(adjustment=self.shiftXAdjustment, climb_rate=0.0, digits=0)
		toShow.append(self.shiftXSpinButton)
		self.shiftXBox.pack_start(self.shiftXSpinButton, fill=False)
		
		self.shiftXSlider = gtk.HScale(adjustment=self.shiftXAdjustment)
		toShow.append(self.shiftXSlider)
		self.shiftXBox.pack_start(self.shiftXSlider, fill=True)
		
		#-------------------------------------------------------------------------------------------------
		
		toAdd = [ None, 0, -100, 100, 1, 10 ]
		for varHold in initVals:
			if varHold[0] == "yShift":
				toAdd = varHold
		
		self.shiftYBox = gtk.HBox()
		self.mainBox.pack_start(self.shiftYBox, fill=False)
		toShow.append(self.shiftYBox)
		self.shiftYLabel = gtk.Label("Y Shift")
		toShow.append(self.shiftYLabel)
		self.shiftYBox.pack_start(self.shiftYLabel, fill=False)
		
		self.shiftYAdjustment = gtk.Adjustment(value=toAdd[1], lower=toAdd[2], upper=toAdd[3], step_incr=toAdd[4], page_incr=toAdd[5])
		
		#===================== making variable =====================
		self.shiftYVar = self.shiftYAdjustment.get_value()
		#===================== making variable =====================
		
		self.shiftYAdjustment.connect("value_changed", self.adjusted, 2)
		
		self.shiftYSpinButton = gtk.SpinButton(adjustment=self.shiftYAdjustment, climb_rate=0.0, digits=0)
		toShow.append(self.shiftYSpinButton)
		self.shiftYBox.pack_start(self.shiftYSpinButton, fill=False)
		
		self.shiftYSlider = gtk.HScale(adjustment=self.shiftYAdjustment)
		toShow.append(self.shiftYSlider)
		self.shiftYBox.pack_start(self.shiftYSlider, fill=True)
		
		#-------------------------------------------------------------------------------------------------
		
		toAdd = [ None, 0, -100, 100, 1, 10 ]
		for varHold in initVals:
			if varHold[0] == "xStig":
				toAdd = varHold
		
		self.stigXBox = gtk.HBox()
		self.mainBox.pack_start(self.stigXBox, fill=False)
		toShow.append(self.stigXBox)
		self.stigXLabel = gtk.Label("X Stigmation")
		toShow.append(self.stigXLabel)
		self.stigXBox.pack_start(self.stigXLabel, fill=False)
		
		self.stigXAdjustment = gtk.Adjustment(value=toAdd[1], lower=toAdd[2], upper=toAdd[3], step_incr=toAdd[4], page_incr=toAdd[5])
		
		#===================== making variable =====================
		self.stigXVar = self.stigXAdjustment.get_value()
		#===================== making variable =====================
		
		self.stigXAdjustment.connect("value_changed", self.adjusted, 3)
		
		self.stigXSpinButton = gtk.SpinButton(adjustment=self.stigXAdjustment, climb_rate=0.0, digits=0)
		toShow.append(self.stigXSpinButton)
		self.stigXBox.pack_start(self.stigXSpinButton, fill=False)
		
		self.stigXSlider = gtk.HScale(adjustment=self.stigXAdjustment)
		toShow.append(self.stigXSlider)
		self.stigXBox.pack_start(self.stigXSlider, fill=True)
		
		#-------------------------------------------------------------------------------------------------
		
		toAdd = [ None, 0, -100, 100, 1, 10 ]
		for varHold in initVals:
			if varHold[0] == "yStig":
				toAdd = varHold
		
		self.stigYBox = gtk.HBox()
		self.mainBox.pack_start(self.stigYBox, fill=False)
		toShow.append(self.stigYBox)
		self.stigYLabel = gtk.Label("Y Stigmation")
		toShow.append(self.stigYLabel)
		self.stigYBox.pack_start(self.stigYLabel, fill=False)
		
		self.stigYAdjustment = gtk.Adjustment(value=toAdd[1], lower=toAdd[2], upper=toAdd[3], step_incr=toAdd[4], page_incr=toAdd[5])
		
		#===================== making variable =====================
		self.stigYVar = self.stigYAdjustment.get_value()
		#===================== making variable =====================
		
		self.stigYAdjustment.connect("value_changed", self.adjusted, 4)
		
		self.stigYSpinButton = gtk.SpinButton(adjustment=self.stigYAdjustment, climb_rate=0.0, digits=0)
		toShow.append(self.stigYSpinButton)
		self.stigYBox.pack_start(self.stigYSpinButton, fill=False)
		
		self.stigYSlider = gtk.HScale(adjustment=self.stigYAdjustment)
		toShow.append(self.stigYSlider)
		self.stigYBox.pack_start(self.stigYSlider, fill=True)
		
		#-------------------------------------------------------------------------------------------------
		
		toAdd = [ None, 0, -100, 100, 1, 10 ]
		for varHold in initVals:
			if varHold[0] == "condLens":
				toAdd = varHold
		
		self.condBox = gtk.HBox()
		self.mainBox.pack_start(self.condBox, fill=False)
		toShow.append(self.condBox)
		self.condLabel = gtk.Label("Condenser Lens")
		toShow.append(self.condLabel)
		self.condBox.pack_start(self.condLabel, fill=False)
		
		self.condAdjustment = gtk.Adjustment(value=toAdd[1], lower=toAdd[2], upper=toAdd[3], step_incr=toAdd[4], page_incr=toAdd[5])
		
		#===================== making variable =====================
		self.condVar = self.condAdjustment.get_value()
		#===================== making variable =====================
		
		self.condAdjustment.connect("value_changed", self.adjusted, 5)
		
		self.condSpinButton = gtk.SpinButton(adjustment=self.condAdjustment, climb_rate=0.0, digits=0)
		toShow.append(self.condSpinButton)
		self.condBox.pack_start(self.condSpinButton, fill=False)
		
		self.condSlider = gtk.HScale(adjustment=self.condAdjustment)
		toShow.append(self.condSlider)
		self.condBox.pack_start(self.condSlider, fill=True)
		
		#-------------------------------------------------------------------------------------------------
		
		toAdd = [ None, 0, -100, 100, 1, 10 ]
		for varHold in initVals:
			if varHold[0] == "objLens":
				toAdd = varHold
		
		self.objBox = gtk.HBox()
		self.mainBox.pack_start(self.objBox, fill=False)
		toShow.append(self.objBox)
		self.objLabel = gtk.Label("Objective Lens")
		toShow.append(self.objLabel)
		self.objBox.pack_start(self.objLabel, fill=False)
		
		self.objAdjustment = gtk.Adjustment(value=toAdd[1], lower=toAdd[2], upper=toAdd[3], step_incr=toAdd[4], page_incr=toAdd[5])
		
		#===================== making variable =====================
		self.objVar = self.objAdjustment.get_value()
		#===================== making variable =====================
		
		self.objAdjustment.connect("value_changed", self.adjusted, 6)
		
		self.objSpinButton = gtk.SpinButton(adjustment=self.objAdjustment, climb_rate=0.0, digits=0)
		toShow.append(self.objSpinButton)
		self.objBox.pack_start(self.objSpinButton, fill=False)
		
		self.objSlider = gtk.HScale(adjustment=self.objAdjustment)
		toShow.append(self.objSlider)
		self.objBox.pack_start(self.objSlider, fill=True)
		
		#-------------------------------------------------------------------------------------------------
		
		toAdd = [ None, 0, -100, 100, 1, 10 ]
		for varHold in initVals:
			if varHold[0] == "filaCurrent":
				toAdd = varHold
		
		self.filaBox = gtk.HBox()
		self.mainBox.pack_start(self.filaBox, fill=False)
		toShow.append(self.filaBox)
		self.filaLabel = gtk.Label("Filament Current")
		toShow.append(self.filaLabel)
		self.filaBox.pack_start(self.filaLabel, fill=False)
		
		self.filaAdjustment = gtk.Adjustment(value=toAdd[1], lower=toAdd[2], upper=toAdd[3], step_incr=toAdd[4], page_incr=toAdd[5])
		
		#===================== making variable =====================
		self.filaVar = self.filaAdjustment.get_value()
		#===================== making variable =====================
		
		self.filaAdjustment.connect("value_changed", self.adjusted, 7)
		
		self.filaSpinButton = gtk.SpinButton(adjustment=self.filaAdjustment, climb_rate=0.0, digits=0)
		toShow.append(self.filaSpinButton)
		self.filaBox.pack_start(self.filaSpinButton, fill=False)
		
		self.filaSlider = gtk.HScale(adjustment=self.filaAdjustment)
		toShow.append(self.filaSlider)
		self.filaBox.pack_start(self.filaSlider, fill=True)
		
		#-------------------------------------------------------------------------------------------------
		
		toAdd = [ None, 0, -100, 100, 1, 10 ]
		for varHold in initVals:
			if varHold[0] == "mag":
				toAdd = varHold
		
		self.magBox = gtk.HBox()
		self.mainBox.pack_start(self.magBox, fill=False)
		toShow.append(self.magBox)
		self.magLabel = gtk.Label("Magnification")
		toShow.append(self.magLabel)
		self.magBox.pack_start(self.magLabel, fill=False)
		
		self.magAdjustment = gtk.Adjustment(value=toAdd[1], lower=toAdd[2], upper=toAdd[3], step_incr=toAdd[4], page_incr=toAdd[5])
		
		#===================== making variable =====================
		self.magVar = self.magAdjustment.get_value()
		#===================== making variable =====================
		
		self.magAdjustment.connect("value_changed", self.adjusted, 8)
		
		self.magSpinButton = gtk.SpinButton(adjustment=self.magAdjustment, climb_rate=0.0, digits=0)
		toShow.append(self.magSpinButton)
		self.magBox.pack_start(self.magSpinButton, fill=False)
		
		self.magSlider = gtk.HScale(adjustment=self.magAdjustment)
		toShow.append(self.magSlider)
		self.magBox.pack_start(self.magSlider, fill=True)
		
		#-------------------------------------------------------------------------------------------------
		
		# save / load values
		# format is .ssf (for SEM saved file):
		# 
		self.saveLoadBox = gtk.HBox()
		toShow.append(self.saveLoadBox)
		self.mainBox.pack_start(self.saveLoadBox, fill=False)
		
		self.saveButton = gtk.Button("Save Settings")
		toShow.append(self.saveButton)
		self.saveLoadBox.pack_start(self.saveButton, fill=False)
		
		self.loadButton = gtk.Button("Load Settings")
		toShow.append(self.loadButton)
		self.saveLoadBox.pack_start(self.loadButton, fill=False)
		
		self.saveButton.connect("clicked", self.saveToFile, None)
		self.loadButton.connect("clicked", self.loadFromFile, None)
		
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
			
		self.runThread = commThread()
		self.runThread.start()
		
	def main(self):
		# All PyGTK applications must have a gtk.main(). Control ends here
		# and waits for an event to occur (like a key press or mouse event).
		gtk.main()

if __name__ == "__main__":
	pool = MainWindow()
	pool.main()