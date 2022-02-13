# Simple gaming controller reader for Linux
# Author: Nicholas Wright
# Example:
#	def OnEvent(time, value, type, number):
#		# Handel joystick event with:
#		#	time = Event timestamp in milliseconds
#		#	value = Value of joystick (+ and -)
#		#	type = Type of Joystick (1 = button, 2 = stick, 3 = initial state)
#		#	number = Axis (0 = X1, 1 = Y1, 2 = X2, 3 = Y2, etc...)
#
#	joystick = Joystick("/dev/input/js0")	# Create the instance
#	joystick.Open()							# Open it
#	joystick.AddListener(OnEvent)			# Listen for events
#	joystick.Close()						# Close it
#	

import time
import struct
import threading

class Joystick():
	STARTUP_THRESHOLD = 0.1		# Time to wait before processing events

	def __init__(self, device, logging = True):
		self.device = device
		self.logging = logging
		
		self.listeners = []		# Listeners to call with events
		
		self.handel = None		# File handler for device
		self.thread = None		# Main thread handle
		self.alive = False		# If the joystick is alive
		
	def Open(self):
		# Close if already open
		if self.alive:
			self._Log("Already open, closing first...")
			self.Close()
	
		# Open the device
		try:
			self.handel = open(self.device, "rb")
			
		except Exception as ex:
			self._Log("Unable to open \"" + self.device + "\" (" + str(ex) + ")")
			return False
		
		# Start the main thread
		self.alive = True
		self.thread = threading.Thread(target = self._MainLoop)
		self.thread.start()
	
		self._Log("Open")
		
	def AddListener(self, listener):
		self.listeners.append(listener)
	
	def Close(self):
		# Don't close again
		if not self.alive:
			return
		
		# Close
		self.alive = False
		self._Log("Closing...")
		
	def _MainLoop(self):
		# Record the start time to eliminate past events
		start_time = time.time()
	
		while self.alive:
			# Read an event
			try:
				event = self.handel.read(8)
			
			except Exception as ex:
				self._Log("Error reading event (" + str(ex) + ")")
				self.Close()
				break
			
			# unpack the data
			jtime, jvalue, jtype, jnumber = struct.unpack("lhBB", event)
			
			# Skip if not past the startup threshold
			if time.time() - start_time < Joystick.STARTUP_THRESHOLD and type != 3:
				continue
			
			# Process
			for listener in self.listeners:
				try:
					listener(jtime, jvalue, jtype, jnumber)
					
				except Exception as ex:
					self._Log("Error calling listener (" + str(ex) + ")")
		
		# When alive == False
		try:
			self.handel.close()
			
		except Exception as ex:
			pass
		
		self._Log("Closed")
	
	def _Log(self, text):
		if self.logging:
			print("[Joystick @ " + self.device.split("/")[-1] + "] " + text)
