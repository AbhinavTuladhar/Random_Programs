from tkinter import *
from tkinter import messagebox
import random

class Tic_Tac_Toe:

	def __init__(self, master):

		self.master = master
		self.turn = False #True for player2, False for player1
		self.flag = 0
		self.numbers = [x for x in range(0, 9)] # Keep track of the available buttons
		self.title = Label(self.master ,text = "Tic Tac Toe", padx = 10, pady = 10, font = ("Helvetica", 20))

		# For the buttons
		self.buttons = []
		for x in range(0, 9):
			btn = Button(self.master , text = "", font = ("Times New Roman", 16), width = 12, height = 6, command = lambda current_button = x : self.btn_click(current_button))
			self.buttons.append(btn)

		self.title.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan = 3)

		for row in range(3):
			for col in range(3):
				index = row * 3 + col
				self.buttons[index].grid(row = row + 1, column = col)

	def btn_click(self, index):

		if self.buttons[index]["text"] == "" and self.turn == False:
			self.buttons[index]["text"] = "O"
			self.turn = True
			self.flag += 1
			self.numbers.remove(int(index))
			self.victory_check("O")
			self.computer_turn()

		else:
			messagebox.showwarning("Tic-Tac-Toe", "Button has already been clicked!")

		print(self.numbers)

		if (self.flag == 9):
			self.disable_buttons()

	def computer_turn(self):

		comp_choice = 0
		
		if (self.flag == 9):
			self.disable_buttons()
		else:
			comp_choice = random.choice(self.numbers)

		if self.buttons[comp_choice]["text"] == "" and self.turn == True:
			self.buttons[int(comp_choice)]["text"] = "X"
			self.turn = False
			self.flag += 1
			self.numbers.remove(int(comp_choice))
			self.victory_check("X")

	def disable_buttons(self):

		for index in range(9):
			self.buttons[index].configure(state = "disable")
		answer = messagebox.askyesno("Match!", "It's a tie!\nPlay again?")
		if (answer == True):
			self.reset_game()
		else:
			self.master.destroy()

	def reset_game(self):

		self.flag = 0
		self.turn = False
		self.numbers = [x for x in range(0, 9)]
		for index in range(9):
			self.buttons[index].configure(state = "active", text = "")

	def victory_check(self, player):
		
		flag = False
		if (self.buttons[0]["text"] == player and self.buttons[1]["text"] == player and self.buttons[2]["text"] == player):
		   flag = True
		if (self.buttons[0]["text"] == player and self.buttons[3]["text"] == player and self.buttons[6]["text"] == player):
			flag = True
		if (self.buttons[3]["text"] == player and self.buttons[4]["text"] == player and self.buttons[5]["text"] == player):
			flag = True
		if (self.buttons[6]["text"] == player and self.buttons[7]["text"] == player and self.buttons[8]["text"] == player):
			flag = True
		if (self.buttons[1]["text"] == player and self.buttons[4]["text"] == player and self.buttons[7]["text"] == player):
			flag = True
		if (self.buttons[2]["text"] == player and self.buttons[5]["text"] == player and self.buttons[8]["text"] == player):
			flag = True
		if (self.buttons[0]["text"] == player and self.buttons[4]["text"] == player and self.buttons[8]["text"] == player):
			flag = True
		if (self.buttons[2]["text"] == player and self.buttons[4]["text"] == player and self.buttons[6]["text"] == player):
			flag = True

		if (flag == True):
			self.victory_message(player)

	def victory_message(self, player):
		exp1 = ""
		vowel = ""
		extra = ""
		if (player == "O"):
			exp1 = "You"
		elif (player == "X"):
			exp1 = "Computer"
			vowel = "s"

		expression = exp1 + " win" + vowel + "!" + "\nPlay again?"
		answer = messagebox.askyesno("Match ends!", expression)

		if answer == True:
			self.reset_game()
		elif answer == False:
			self.master.destroy()

if __name__ == "__main__":
	window = Tk()
	window.title("Tic Tac Toe")
	window.resizable(0, 0)
	object = Tic_Tac_Toe(window)
	window.mainloop()