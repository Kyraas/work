from tkinter import *

# Validating function
def validate(user_input):
	# check if the input is numeric
	if user_input.isdigit():
		# Fetching minimum and maximum value of the spinbox
		minval = int(root.nametowidget(spinbox).config('from')[4])
		maxval = int(root.nametowidget(spinbox).config('to')[4])

		# check if the number is within the range
		if int(user_input) not in range(minval, maxval):
			print ("Out of range")
			return False

		# Printing the user input to the console
		print(user_input)
		return True

	# if input is blank string
	elif user_input == "":
		print(user_input)
		return True

	# return false is input is not numeric
	else:
		print("Not numeric")
		return False


root = Tk()
root.geometry("300x300")
root.title("Spinbox Range Validation")

# Creating Spinbox
spinbox = Spinbox(root, from_ = 1, to = 1000)
spinbox.pack()
range_validation = root.register(validate)

spinbox.config(validate ="key",
		validatecommand =(range_validation, '% P'))

root.mainloop()
