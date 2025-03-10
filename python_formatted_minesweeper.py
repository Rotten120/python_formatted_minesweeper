import random
import os

class Cell:
    def __init__(self):
        self.val = 0
        self.is_bomb = False
        self.is_flag = False
        self.is_hidden = True
    
    def inc(self):
        self.val += 1
    
    def set_bomb(self):
        self.is_bomb = True
        self.val = -1
    
    def toggle_flag(self):
        self.is_flag = not self.is_flag
        return self.is_flag
    
    def reveal(self):
        if self.is_flag or self.is_bomb: return
        self.is_hidden = False
    
    def print(self):
        output = str(self.val)
        if self.is_flag: output = '>'
        elif self.is_hidden: output = '-'
        elif self.is_bomb: output = '#'
        elif self.val == 0: output = ' '
        print(output, end = ' ')

class MineSweeper:
    def __init__(self):
        self.col = 0
        self.row = 0
        self.mode = "Mine"
        self.menu = "Main Menu"
        self.bomb_count = 0
        self.flag_count = 0
        self.is_win = False
        self.board = []
    
    def gen_game(self, col, row, bombs):
        self.col = col
        self.row = row
        self.mode = "Mine"
        self.menu = "Game"
        self.bomb_count = bombs
        self.flag_count = self.bomb_count
        self.is_win = False

        #c is current index for column
        #r is current index for row
        self.board = [
            [Cell() for c in range(col)]
            for r in range(row)
            ]
        self.gen_bombs()
        
    def get(self, col, row):
        return self.board[row][col]
    
    def is_visible(self, vis):
        for row in range(self.row):
            for col in range(self.col):
                self.get(col, row).is_hidden = vis
    
    def count_hidden(self):
        count = 0
        for row in range(self.row):
            for col in range(self.col):
                if self.get(col, row).is_hidden:
                    count += 1
        return count            
    
    def gen_bombs(self):
        grid_size = self.col * self.row
        bomb_placed = 0
        for row in range(self.row):
            for col in range(self.col):
                grid_count = (self.col * row) + col
                base_chance = self.bomb_count / (10 * grid_size)
                add_chance = (1 - base_chance) * (self.bomb_count - bomb_placed) / (grid_size - grid_count)
                total_chance = int(100 * (base_chance + add_chance))
                if random.randrange(100) < total_chance and bomb_placed < self.bomb_count:
                    self.get(col, row).set_bomb()
                    bomb_placed += 1
                    self.gen_numbers(col, row)
                    
    def gen_numbers(self, col, row):
        rad = 1
        row_delta = [-rad,rad]
        col_delta = [-rad,rad]
        
        if row + rad >= self.row: row_delta[1] = self.row - row - 1
        if row - rad < 0: row_delta[0] = -row
        if col + rad >= self.col: col_delta[1] = self.col - col - 1
        if col - rad < 0: col_delta[0] = -col

        #c is current index for column
        #r is current index for row
        for c in range(row + row_delta[0], row + row_delta[1] + 1):
            for r in range(col + col_delta[0], col + col_delta[1] + 1):
                if not self.get(r, c).is_bomb:
                    self.get(r, c).inc()
    
    def update(self):
        if self.menu == "Main Menu":
            return self.main_menu()
        elif self.menu == "Game":
            self.game()
        elif self.menu == "Post Game":
            self.post_game()    
        elif self.menu == "Controls":
            self.controls()
        elif self.menu == "Custom":
            self.custom()    
        elif self.menu == "Credits":
            self.credits()
        elif self.menu == "Easter1":
            self.easter1()
        return False    
            
    def main_menu(self):
        print('_' * 27)
        print(' ' * 2, "M I N E S W E E P E R")  
        print()
        print("              ,--.!,")
        print("           __/   -*-")
        print("         ,d08b.  '|`")
        print("         0088MM")     
        print("         `9MMP'")     
        print()
        print("MAIN MENU")
        print("[1] Beginner")      
        print("[2] Intermediate")
        print("[3] Advanced")
        print("[4] Custom")
        print("[5] Credits")
        print("[6] Quit")
        print('_' * 27)
        inp = input("\nInput: ")
        
        if inp == '1': self.gen_game(7, 7, 5)
        if inp == '2': self.gen_game(12, 12, 15)
        if inp == '3': self.gen_game(15, 15, 20)
        if inp == '4': self.menu = "Custom"
        if inp == '5': self.menu = "Credits"
        if inp == "This deserves a 100": self.menu = "Easter1"
        
        return (inp == '6')
    
    def game(self):
        self.print_board()
        print(
            "[1] Mode: Mine",
            "[2] Mode: Flag",
            "[3] Controls",
            "[4] Give Up",
        sep = '\n')
        print('_' * (2 * self.col + 3))
        
        A_ascii = ord('A')
        inp = input('\nInput: ')
        
        if len(inp) == 1:
            try:
                if int(inp) == 1: self.mode = "Mine"
                if int(inp) == 2: self.mode = "Flag"
                if int(inp) == 3: self.menu = "Controls"
                if int(inp) == 4: self.trigger_post_game(False)
            except: pass
            return
            
        for i in range((len(inp) + 1) // 3):
            col = ord(inp[i * 3]) - A_ascii
            row = ord(inp[i * 3 + 1]) - A_ascii 
            if col < 0 or row < 0 or col >= self.col or row >= self.row:
                continue
            self.check_input(col, row)
                
    def print_board(self):
        A_ascii= ord('A')
        print()
        
        print('X', end = ' ')
        for col in range(self.col):
            print(chr(col + A_ascii), end = ' ')
        print('X', end = ' ')    
            
        for row in range(self.row):
            print('\n' + chr(row + A_ascii), end = ' ')    
            for col in range(self.col):
                self.get(col, row).print()
            print(chr(row + A_ascii), end = ' ')  
                
        print()        
        print('X', end = ' ')
        for col in range(self.col):
            print(chr(col + A_ascii), end = ' ')
        print('X', end = ' ')    ;        
                
        print('\n' + '_' * (2 * self.col + 3))
        print(' ' * (self.col - 9), "Flags:", self.flag_count, "Mode:", self.mode, '\n')                     
                
    def check_input(self, col, row):
        if self.mode == "Flag":
            if self.get(col, row).toggle_flag(): self.flag_count -= 1
            else: self.flag_count += 1
            return
        
        self.get(col, row).reveal()
        
        if self.get(col, row).is_bomb and not self.get(col, row).is_flag:
            self.trigger_post_game(False)
        elif self.count_hidden() == self.bomb_count:
            self.trigger_post_game(True)
        elif self.get(col, row).val == 0:
            self.clear_blank(col, row)
    
    def clear_blank(self, col, row):
        if self.get(col, row).val > 0: return
        
        rad = 1
        row_delta = [-rad,rad]
        col_delta = [-rad,rad]
        
        if row + rad >= self.row: row_delta[1] = self.row - row - 1
        if row - rad < 0: row_delta[0] = -row
        if col + rad >= self.col: col_delta[1] = self.col - col - 1
        if col - rad < 0: col_delta[0] = -col

        #c is current index for column
        #r is current index for row
        for c in range(row + row_delta[0], row + row_delta[1] + 1):
            for r in range(col + col_delta[0], col + col_delta[1] + 1):
                if not self.get(r, c).is_bomb and self.get(r, c).is_hidden:
                    self.get(r, c).is_hidden = False
                    self.clear_blank(r, c)
    
    def trigger_post_game(self, is_win):
        self.is_win = is_win
        self.menu = "Post Game"
    
    def post_game(self):
        if not self.is_win:
            self.is_visible(False)
        self.print_board()
        if self.is_win:
            print('\n' + ' ' * (self.col - 6), "Y O U  W I N")
        else:
            print('\n' + ' ' * (self.col - 7), "Y O U  L O S E")
       
        print("\nWhat now?")
        print("[1] Play Again")
        print("[2] Go Back to Menu")
        inp = input("\nInput: ")
        
        if inp == '1':
            self.gen_game(self.col, self.row, self.bomb_count)
            self.menu = "Game"
        if inp == '2':
            self.menu = "Main Menu"    
    
    def custom(self):
        print('_' * 27)
        print(' ' * 7 , "C U S T O M")
        print()
        print()
        print("         /\"*._         _")
        print("     .-*'`    `*-.._.-'/")
        print("   < * ))     ,       (")
        print("     `*-._`._(__.--*\"`.\\")       
        print()
        print()
        print("Note:")
        print("+ Columns and rows have minimum of 5")
        print("  and max of 26")
        print("+ Bombs have minimum of 1")
        print("+ Input -1 at any input to exit")
        print()
        
        while True:
            try:
                print('_' * 27)
                col_inp = int(input("How many columns: "))
                row_inp = int(input("How many rows: "))
                bomb_inp = int(input("How many bombs: "))
            except: continue    
            print()
            if col_inp == -1 or row_inp == -1 or bomb_inp == -1:
                self.menu = "Main Menu"
                return
                
            if col_inp < 5 or row_inp < 5: print("Column/Row too small")
            elif col_inp > 26 or row_inp > 26: print("Column/Row too large")
            elif bomb_inp < 1: print("Game must have at least 1 bomb")
            elif bomb_inp >= col_inp * rowInp: print("Too many bombs")
            else: break
        self.gen_game(col_inp, row_inp, bomb_inp)
        self.menu = "Game"
    
    def credits(self):
        print('_' * 27)
        print(' ' * 6, "C R E D I T S")
        print()
        print("         ,--./,-.")
        print("        /,-._.--~\\")
        print("         __}  {")
        print("        \`-._,-`-,")
        print("         `._,._,'")  
        print()
        print("Programmed by:")
        print("Von Zedric B. Delos Reyes")
        print("BSCPE 1-2")
        print()
        print("Released on:")
        print("February 25, 2025")
        print()
        print("Ascii Arts are sourced from:")
        print("https://www.asciiart.eu/") 
        print('_' * 27)
        print()
        print("[1] Back")
        inp = input("\nInput: ")
        if inp == '1': self.menu = "Main Menu"
        
    def controls(self):
        print('\n' + '_' * 27)
        print(' ' * 5, "C O N T R O L S")
        print()
        print("Type the letter of column and row")
        print("of the cell you want to check.")
        print()
        print("Example:\nInput: AB\nChecks cell at column A row B.")
        print()
        print("You can also input multiple cells")
        print("at once by separating each input")
        print("with whitespace")
        print()
        print("Example:")
        print("Input: AB GD BC")
        print("Checks all of the following cells")
        print('\n' + '_' * 27)
        print()
        print("[1] Resume")
        inp = input("\nInput : ")
        if inp == '1': self.menu = "Game"
        
    def easter1(self):
        print("YES!!! THANK YOU POOOO")
        
        print()
        print("               __")
        print("    ..=====.. |==|")
        print("    ||     || |= |")
        print(" _  ||     || |^*| _")
        print("|=| o=,===,=o |__||=|")
        print("|_|  _______)~`)  |_|")
        print("    [=======]  ()       ldb")    
        print()   

        print("[1] Back")
        inp = input("\nInput: ")
        if inp == '1': self.menu = "Main Menu"

if __name__ == '__main__':
    game = MineSweeper()
    while True:
        os.system('cls')
        if game.update(): break
