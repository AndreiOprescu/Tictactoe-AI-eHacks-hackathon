from tkinter import *
from tkinter import messagebox
from Impossible_AI import ImpossibleAI


class App:
    def __init__(self, master):
        self.master = master
        master.geometry("198x305")
        master.resizable(False, False)

        self.turn = 0

        self.player_turn = Label(master, text="Player {}'s turn".format((self.turn + 1) % 2 + 1), width=27, bg='Yellow')
        self.player_turn.grid(columnspan=4)
        self.button1_1 = Button(master, text="", width=8, height=4, command=lambda: self.mark_button(self.button1_1))
        self.button1_1.grid(row=1, column=1)
        self.button2_1 = Button(master, text="", width=8, height=4, command=lambda: self.mark_button(self.button2_1))
        self.button2_1.grid(row=2, column=1)
        self.button3_1 = Button(master, text="", width=8, height=4, command=lambda: self.mark_button(self.button3_1))
        self.button3_1.grid(row=3, column=1)
        self.button1_2 = Button(master, text="", width=8, height=4, command=lambda: self.mark_button(self.button1_2))
        self.button1_2.grid(row=1, column=2)
        self.button2_2 = Button(master, text="", width=8, height=4, command=lambda: self.mark_button(self.button2_2))
        self.button2_2.grid(row=2, column=2)
        self.button3_2 = Button(master, text="", width=8, height=4, command=lambda: self.mark_button(self.button3_2))
        self.button3_2.grid(row=3, column=2)
        self.button1_3 = Button(master, text="", width=8, height=4, command=lambda: self.mark_button(self.button1_3))
        self.button1_3.grid(row=1, column=3)
        self.button2_3 = Button(master, text="", width=8, height=4, command=lambda: self.mark_button(self.button2_3))
        self.button2_3.grid(row=2, column=3)
        self.button3_3 = Button(master, text="", width=8, height=4, command=lambda: self.mark_button(self.button3_3))
        self.button3_3.grid(row=3, column=3)
        self.reset = Button(master, text="Restart Game", command=self.restart, width=27, height=4, bg="Red")
        self.reset.grid(columnspan=4)

        self.squares = [[self.button1_1, self.button2_1, self.button3_1],
                        [self.button1_2, self.button2_2, self.button3_2],
                        [self.button1_3, self.button2_3, self.button3_3]]

        self.winning_formations = [
            [self.button1_1, self.button2_1, self.button3_1],
            [self.button1_2, self.button2_2, self.button3_2],
            [self.button1_3, self.button2_3, self.button3_3],
            [self.button1_1, self.button1_2, self.button1_3],
            [self.button2_1, self.button2_2, self.button2_3],
            [self.button3_1, self.button3_2, self.button3_3],
            [self.button1_1, self.button2_2, self.button3_3],
            [self.button1_3, self.button2_2, self.button3_1]
        ]

        self.first = True

        self.ai_player = ImpossibleAI(self.squares, self.winning_formations, self.first)
        self.mark_button(self.ai_player.next_move)

    def message_box(self, title, message):
        answer = messagebox.askquestion(title, message)
        if answer.lower() == "yes":
            self.restart()
            self.player_turn.config(text="Player {}'s turn".format((self.turn + 1) % 2 + 1))
        else:
            exit()

    def restart(self):
        widgets = self.master.winfo_children()
        for widget in widgets:
            if (widgets.index(widget) > 0) & (widgets.index(widget) < 10):
                widget.config(text="", bg="White")
        self.turn = 0
        self.player_turn.config(text="Player {}'s turn".format((self.turn + 1) % 2 + 1))
        self.mark_button(self.ai_player.next_move)

    def mark_button(self, button):
        if button['text'] == "":
            if self.turn % 2 == 0:
                button.config(text="x", bg='blue')
            else:
                button.config(text="o", bg='green')
            self.is_game_won()
            self.turn += 1
            self.player_turn.config(text="Player {}'s turn".format((self.turn + 1) % 2 + 1))
            if self.turn % 2 == 0:
                self.mark_button(self.ai_player.next_move)

    def is_game_won(self):
        for formation in self.winning_formations:
            if (formation[0]['text'] == formation[1]['text']) & \
                    (formation[1]['text'] == formation[2]['text']) & \
                    (formation[1]['text'] != ""):
                self.message_box("Player {} won!".format((self.turn + 1) % 2 + 1),
                                 "Player {} won! \nDo you want to play again?".format((self.turn + 1) % 2 + 1))
                self.turn = 0
        occupied_cells = 0
        widgets = self.master.winfo_children()
        for widget in widgets:
            if (widgets.index(widget) > 0) & (widgets.index(widget) < 10):
                if widget['text'] != "":
                    occupied_cells += 1
        if occupied_cells == 9:
            self.message_box("It's a tie!", "It's a tie! \nDo you want to play again?")
            self.turn = 0


if __name__ == '__main__':
    root = Tk()
    root.title("Tic Tac Toe")
    app = App(root)
    root.mainloop()

