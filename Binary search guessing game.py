from tkinter import *
from tkinter import messagebox
import random
import math as maths

class Number_Guessing:

	def __init__(self, master):

		self.master = master
		self.steps = 0	# Count the number of steps
		self.expression = ""	# To keep track of the seequence
		self.start_press = False # To check whether the start button has been pressed or not.
		# Pressing search twice without restting causes the text to get glitched, 
		# so this is just a precautionary measure for visual appeal.

		self.start_frame = LabelFrame(self.master, text = "Enter the lower bound")
		self.start_frame.grid(row = 0, column = 0, padx = 50, pady = 10)
		self.start_entry = Entry(self.start_frame, width = 25)
		self.start_entry.pack(padx = 10, pady = 10)

		self.end_frame = LabelFrame(self.master, text = "Enter the upper bound")
		self.end_frame.grid(row = 0, column = 1, padx = 50, pady = 10)
		self.end_entry = Entry(self.end_frame, width = 25)
		self.end_entry.pack(padx = 10, pady = 10)

		self.button_start = Button(self.master, text = "Start Search!", command = self.btn_press)
		self.button_start.grid(row = 1, column = 0, padx = 10, pady = 10, columnspan = 2)

		self.button_reset = Button(self.master, text = "Reset", command = self.reset)
		self.button_reset.grid(row = 2, column = 0, padx = 10, pady = 10, columnspan = 2)

	def reset(self):

		# Clearing variables for new randomly generated number
		self.result["text"] = ""
		self.expression = 0
		self.steps = 0
		self.start_press = False

	def btn_press(self):

		# Get the starting and ending values
		start = int(self.start_entry.get())
		end = int(self.end_entry.get())
		self.expression = ""
		self.steps = 0

		# Check whether the values are appropriate
		if start >= end:
			messagebox.showerror("Enter again", "Invalid entry. \nPlease enter again.")

		# Check if start button is pressed twice, for reasons mentioned above.
		elif self.start_press == True:
			messagebox.showerror("Warning", "Please reset first. \nThis is to prevent text from glitching.")

		elif (self.start_press == False and start < end):
			self.number = random.randint(start, end)

			# Performing the binary search
			mid = 0

			while (start <= end or mid != self.number):
				mid = (start + end) // 2
				self.steps += 1
				self.expression += str(mid) + " -> "

				if (mid < self.number):
					start = mid + 1
				elif (mid > self.number):
					end = mid - 1
				else:
					break

			self.expression = self.expression[:-3] # Remove the last three characters
			self.display_result()
			self.start_press = True # To indicate start has been pressed

	def display_result(self):

		start = int(self.start_entry.get())
		end = int(self.end_entry.get())
		vowel = "s" # For grammatical purpose

		# Worst case for binary search, O(logn)
		max_steps = maths.floor(maths.log2(end - start)) + 1
		step_expn = "Maximum number of steps expected is " + str(max_steps) + "."
		
		# For grammar
		if self.steps == 1:
			vowel = ""
		#final_expression = "The number is " + str(self.number) + ".\n\n" + self.expression + "\n\nFound in " + str(self.steps) + " steps.\n\n" + step_expn + "."
		final_expression = f'The number is {self.number}. \n\n{self.expression} \n\nFound in {self.steps} step{vowel}.\n\n{step_expn}'

		# Put the label on the screen
		self.result = Label(self.master, text = final_expression, wraplength = 500)
		self.result.grid(row = 3, column = 0, columnspan = 2, padx = 10, pady = 10)

if __name__ == "__main__":
	window = Tk()
	window.title("Binary searching")
	window.resizable(0, 0)

	object = Number_Guessing(window)
	window.mainloop()