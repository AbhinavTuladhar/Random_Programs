from tkinter import *
from tkinter import messagebox

class Connect:

	def __init__(self, master):

		self.master = master
		self.buttons = []
		self.click_buttons = []
		self.turn = True # True for X's turn, False for O's turn
		self.check_full = [0 for x in range(7)] # Keep track of which columns are full
		self.turn_dict = { # For cleaner implementation of button clicks
				True : "X",
				False : "O"
		}
		self.colour_dict = {
				"X" : "skyblue",
				"O" : "yellow"
		}
		self.initialise()
		#messagebox.showinfo("Welcome!", "Connect four tiles vertically, diagonally or horizontally to win.")

	def initialise(self):

		# To display whose turn it is
		self.turn_info = Label(self.master, text = "X's Turn")
		self.turn_info.grid(row = 0, column = 0, padx = 10, pady = 10)

		# Creating the game grid
		self.game_grid = Frame(self.master)
		for row in range (6):
			temp = []
			for col in range(7):
				text = f'Row {row + 1}, Col {col + 1}'
				btn = Button(self.game_grid, text = "", height = 5, width = 10)
				temp.append(btn)
			self.buttons.append(temp)

		self.game_grid.grid(row = 1, column = 0, padx = 10, pady = 10)
		for row in range(6):
			for col in range(7):
				self.buttons[row][col].grid(row = row, column = col, sticky = "news")

		# Creating the clickable buttons
		self.btn_grid = Frame(self.master)
		for index in range(7):
			text = "Col " + str(index + 1)
			btn = Button(self.btn_grid, text = text, command = lambda number = index : self.btn_click(number))
			self.click_buttons.append(btn)

		self.btn_grid.grid(row = 2, column = 0, padx = 10, pady = 50)
		for index in range(7):
			self.click_buttons[index].grid(row = 0, column = index, padx = 20)

		for row in range(2):
			Grid.rowconfigure(self.master, row, weight = 1)
			Grid.columnconfigure(self.master, 0, weight = 1)

	def whose_turn(self):
		if self.turn == False:
			self.turn_info.configure(text = "X's Turn")
		else:
			self.turn_info.configure(text = "O's Turn")

	def btn_click(self, column):
		self.whose_turn()
		bottom_row = 5 # Specify the bottom-most row
		#player = "X" if self.turn == True else "O"
		player = self.turn_dict[self.turn]

		# Check if the current column is full or not
		if self.check_full[column] == 6:
			messagebox.showinfo("Error", "Column already full")
			return

		answer = self.buttons[bottom_row][column]["text"]
		# Fill in the corresponding colour if button is empty
		if (answer == ""):
			self.buttons[bottom_row][column].config(text = player, bg = self.colour_dict[player])
		# Insert the 'coin' in the bottom-most available row of that column
		elif (answer != ""):
			bottom_row = 5
			while True:
				answer = self.buttons[bottom_row][column]["text"]
				if answer == "":
					self.buttons[bottom_row][column].config(text = player, bg= self.colour_dict[player])
					break
				else:
					bottom_row -= 1

		# Keep track of the number of coins in that column
		if self.check_full[column] < 6 : self.check_full[column] += 1

		# Check for program termination
		self.victory_check(bottom_row, column)

		# To check if the entire grid is full
		full = [6 for x in range(7)]
		if full == self.check_full:
			messagebox.showinfo("END", "The entire grid is full")
			self.master.destroy()

		# To alternate between player turn
		if self.turn == True:
			self.turn = False
		elif self.turn == False:
			self.turn = True

		print(self.check_full)

	def victory_check(self, bottom_row, column):
		player = self.turn_dict[self.turn]

		"""
		if (bottom_row + 3) <= 5:
			ans = all(self.buttons[Row][column]["text"] == player for Row in range(bottom_row, bottom_row + 3))
			if ans == True:
				choice = messagebox.askyesno("Game over", f'{player} WINS!\nPlay again?')
				if choice == True:
					self.construct()
				else:
					self.master.destroy()
		"""

		# Checking for consecutive vertical slots
		if (bottom_row + 3) <= 5:
			for x in range(7):
				if self.buttons[bottom_row][column]["text"] == player and self.buttons[bottom_row + 1][column]["text"] == player and self.buttons[bottom_row + 2][column]["text"] == player and self.buttons[bottom_row + 3][column]["text"] == player:
					choice = messagebox.askyesno("Game over", f'{player} WINS!\nPlay again?')
					if choice == True:
						self.construct()
					else:
						self.master.destroy()

		# Checking for consecutive horizontal slots
		for cols in range(4):
			if self.buttons[bottom_row][cols]["text"] == player and self.buttons[bottom_row][cols + 1]["text"] == player and self.buttons[bottom_row][cols + 2]["text"] == player and self.buttons[bottom_row][cols + 3]["text"] == player:
				choice = messagebox.askyesno("Game over", f'{player} wins! \nPlay again?')
				if choice == True:
					self.construct()
				else:
					self.master.destroy()

		# Checking in the main diagonal
		for row in range(3):
			for col in range(3, 7):
				if self.buttons[row][col]["text"] == player and self.buttons[row + 1][col - 1]["text"] == player and self.buttons[row + 2][col - 2]["text"] == player and self.buttons[row + 3][col - 3]["text"] == player:
					print("Main diagonal")
					print(f'Rows: {row}, {row + 1}, {row + 2} and {row + 3}')
					print(f'Columns: {col - 3}, {col - 2}, {col - 1} and {col}')
					choice = messagebox.askyesno("Game over", f'{player} wins! \nPlay again?')
					if choice == True:
						self.construct()
					else:
						self.master.destroy()
		# Checking other diagonal:
		for row in range(3):
			for col in range(4):
				if self.buttons[row][col]["text"] == player and self.buttons[row + 1][col + 1]["text"] == player and self.buttons[row + 2][col + 2]["text"] == player and self.buttons[row + 3][col + 3]["text"] == player:
					print("Other diagonal")
					print(f'Rows: {row}, {row + 1}, {row + 2} and {row + 3}')
					print(f'Columns: {col}, {col + 1}, {col + 2} and {col + 3}')
					choice = messagebox.askyesno("Game over", f'{player} wins! \nPlay again?')
					if choice == True:
						self.construct()
					else:
						self.master.destroy()

	def construct(self):

		self.turn = False
		self.check_full = [0 for x in range(7)]
		self.turn_info["text"] = "X's Turn"
		for row in range(6):
			for column in range(7):
				self.buttons[row][column].config(text = "", bg = "systembuttonface")

if __name__ == "__main__":

	window = Tk()
	window.title("Connect Four")

	object = Connect(window)

	window.mainloop()