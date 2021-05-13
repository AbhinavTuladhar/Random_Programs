from tkinter import *
from tkinter import messagebox
import random

class Password_Generator:

	def __init__(self, master):
		self.master = master

		self.frame = LabelFrame(self.master, font = ("Helvetica", 13), text = "How many characters?")
		self.frame.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan = 2)

		self.num_entry = Entry(self.frame, width = 10, font = ("Helvetica", 16))
		self.num_entry.grid(row = 0, column = 0, padx = 10, pady = 10)

		self.pwd_entry = Entry(self.master, width = 30, bg = "systembuttonface", bd = 0, font = ("Helvetica", 18))
		self.pwd_entry.grid(row = 1, column = 0, padx = 10, pady = 10, columnspan = 2)

		self.btn_generate = Button(self.master, text = "Generate Random Password", command = self.generate)
		self.btn_generate.grid(row = 2, column = 0, padx = 10, pady = 10)

		self.copy_pwd = Button(self.master, text = "Copy to Clipboard", command = self.copy_clipboard)
		self.copy_pwd.grid(row = 2, column = 1, padx = 10, pady = 10)

	def generate(self):

		self.pwd_entry.delete(0, END)

		pwd_length = int(self.num_entry.get())
		password = ""

		for x in range(pwd_length):
			random_character = chr(random.randint(33, 126))
			password += random_character

		self.pwd_entry.insert(0, password)

	def copy_clipboard(self):

		self.master.clipboard_clear()
		self.master.clipboard_append(self.pwd_entry.get())

		messagebox.showinfo("Success!", "Successfully copied to clipboard")

if __name__ == "__main__":
	window = Tk()
	window.title("Random passowrd generator")

	object = Password_Generator(window)
	window.mainloop()