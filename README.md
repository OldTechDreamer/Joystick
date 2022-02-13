# Joystick
Python/Linux Joystick / Game controller reader

# Requirements
* Linux
* Python 3 (or python 2 (not tested))

# Example

def OnEvent(time, value, type, number):
    # Handel joystick event with:
    # time = Event timestamp in milliseconds
		#	value = Value of joystick (+ and -)
		#	type = Type of Joystick (1 = button, 2 = stick, 3 = initial state)
		#	number = Axis (0 = X1, 1 = Y1, 2 = X2, 3 = Y2, etc...)

joystick = Joystick("/dev/input/js0")	# Create the instance (path to linux joystick device js0, js1, js2, etc...)
joystick.Open()							          # Open it
joystick.AddListener(OnEvent)			    # Listen for events
joystick.Close()						          # Close it
