import tkinter as tk


class Game(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.height = self.winfo_screenheight()
        self.width = self.winfo_screenwidth()

        self.ball = None
        self.playerBar = None
        self.computerBar = None

        # # # # menu # # # #
        self.menuFrame = tk.Frame(self)
        self.titleLabel = tk.Label(self.menuFrame, text='Pong But With Windows!')
        self.playButton = tk.Button(self.menuFrame, text='PLAY', command=self.play)

        self.menuFrame.grid(row=0, column=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.titleLabel.grid(row=0, column=0, sticky='nsew')
        self.playButton.grid(row=1, column=0, sticky='nsew')
        self.menuFrame.columnconfigure(0, weight=1)
        self.menuFrame.rowconfigure(0, weight=2)
        self.menuFrame.rowconfigure(1, weight=1)
        # END # menu # END #

        # # # # "in progress" screen # # # #
        self.inProgressFrame = tk.Frame(self)
        self.inProgressLabel = tk.Label(self.inProgressFrame, text='Game in progress...')
        self.closeNoticeLabel = tk.Label(self.inProgressFrame, text='(close this to end game)')

        self.inProgressFrame.grid(row=0, column=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.inProgressLabel.grid(row=0, column=0, sticky='nsew')
        self.closeNoticeLabel.grid(row=1, column=0, sticky='nsew')
        self.inProgressFrame.columnconfigure(0, weight=1)
        self.inProgressFrame.rowconfigure(0, weight=1)
        self.inProgressFrame.rowconfigure(1, weight=1)
        # END # "in progress" screen # END #

        self.inProgressFrame.grid_remove()  # initially, the inProgressFrame should not be visible

    def play(self):
        # self.wm_state('iconic')
        self.inProgressFrame.grid()
        geom = self.winfo_geometry().split('+')
        self.geometry(geom[0] + '+{}+{}'.format(self.width//2 - int(geom[0].split('x')[0])//2, 0))

        self.ball = Ball(self)
        self.computerBar = ComputerBar(self)
        self.playerBar = PlayerBar(self)

        self.bind('<w>', lambda e, y=-self.playerBar.yvel: self.playerBar.move(y))
        self.bind('<s>', lambda e, y=self.playerBar.yvel: self.playerBar.move(y))
        self.bind('<Up>', lambda e, y=-self.playerBar.yvel: self.playerBar.move(y))
        self.bind('<Down>', lambda e, y=self.playerBar.yvel: self.playerBar.move(y))

        self.after(1, self.move_ball)
        self.after(1, self.check_collisions)

    def move_ball(self):
        self.ball.move(self.ball.xvel, self.ball.yvel)
        self.after(1, self.move_ball)

    def check_collisions(self):
        for bar in (self.computerBar, self.playerBar):
            if (self.ball.x + self.ball.width + self.ball.xvel > bar.x) and (
               self.ball.x + self.ball.xvel < bar.x + bar.width) and (
               self.ball.y + self.ball.height > bar.y) and (
               self.ball.y < bar.y + bar.height):
                self.ball.xvel *= -1

            if (self.ball.x + self.ball.width > bar.x) and (
               self.ball.x < bar.x + bar.width) and (
               self.ball.y + self.ball.height + self.ball.yvel > bar.y) and (
               self.ball.y + self.ball.yvel < bar.y + bar.height):
                self.ball.yvel *= -1

        self.after(1, self.check_collisions)


class ComputerBar(tk.Toplevel):
    def __init__(self, game, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.game = game

        self.config(bg='white')
        self.width = self.game.width // 15
        self.height = self.width * 3
        self.x = self.game.width - self.width - self.width // 2
        self.y = (self.game.height // 2) - (self.height // 2)
        self.yvel = 20

        self.draw()

    def move(self, y):
        self.y += y
        if self.y > (self.game.height - self.height):
            self.y = self.game.height - self.height
        elif self.y < 0:
            self.y = 0
        self.draw()

    def draw(self):
        self.geometry("{}x{}+{}+{}".format(self.width, self.height, self.x, self.y))


class PlayerBar(tk.Toplevel):
    def __init__(self, game, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.game = game

        self.config(bg='white')
        self.width = self.game.width // 15
        self.height = self.width * 3
        self.x = self.width // 2
        self.y = (self.game.height // 2) - (self.height // 2)
        self.yvel = 20

        self.draw()

    def move(self, y):
        self.y += y
        if self.y > (self.game.height - self.height):
            self.y = self.game.height - self.height
        elif self.y < 0:
            self.y = 0
        self.draw()

    def draw(self):
        self.geometry("{}x{}+{}+{}".format(self.width, self.height, self.x, self.y))


class Ball(tk.Toplevel):
    def __init__(self, game, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.game = game

        self.config(bg='white')
        self.width = self.game.width // 18
        self.height = self.width
        self.x = (self.game.width // 2) - (self.width // 2)
        self.y = (self.game.height // 2) - (self.height // 2)
        self.xvel = 1
        self.yvel = 1

        self.draw()

    def move(self, x, y):  # 0,0 in top left
        self.x += x
        self.y += y
        self.check_boundaries()
        self.draw()

    def check_boundaries(self):
        if self.x < 0:
            self.x = 0
            self.xvel = -self.xvel
        elif self.x > (self.game.width - self.width):
            self.x = self.game.width - self.width
            self.xvel = -self.xvel
        elif self.y < 0:
            self.y = 0
            self.yvel = -self.yvel
        elif self.y > (self.game.height - self.height):
            self.y = self.game.height - self.height
            self.yvel = -self.yvel

    def draw(self):
        self.geometry("{}x{}+{}+{}".format(self.width, self.height, self.x, self.y))


if __name__ == "__main__":
    g = Game()
    g.mainloop()
