import random
import os

class cell:
    def __init__(self):
        self.val = 0
        self.isBomb = False
        self.isFlag = False
        self.ishidden = True
    
    def inc(self):
        self.val += 1
    
    def setBomb(self):
        self.isBomb = True
        self.val = -1
    
    def toggleFlag(self):
        self.isFlag = not self.isFlag
        return self.isFlag
    
    def reveal(self):
        if self.isFlag or self.isBomb: return
        self.ishidden = False
    
    def print(self):
        output = str(self.val)
        if self.isFlag:     output = '>'
        elif self.ishidden: output = '-'
        elif self.isBomb:   output = '#'
        elif self.val == 0: output = ' '
        print(output, end = ' ')

class minesweeper:
    def __init__(self):
        self.col = 0
        self.row = 0
        self.mode = "Mine"
        self.menu = "Main Menu"
        self.bombCount = 0
        self.flagCount = 0
        self.isWin = False
        self.board = []
    
    def genGame(self, col, row, bombs):
        self.col = col
        self.row = row
        self.mode = "Mine"
        self.menu = "Game"
        self.bombCount = bombs
        self.flagCount = self.bombCount
        self.isWin = False
        self.board = [
            [cell() for i in range(col)]
            for j in range(row)
            ]
        self.genBombs()
        
    def get(self, col, row):
        return self.board[row][col]
    
    def isVisible(self, vis):
        for r in range(self.row):
            for c in range(self.col):
                self.get(c, r).ishidden = vis
    
    def countHidden(self):
        count = 0
        for r in range(self.row):
            for c in range(self.col):
                if self.get(c, r).ishidden:
                    count += 1
        return count            
    
    def genBombs(self):
        gridSize = self.col * self.row
        bombPlaced = 0
        for r in range(self.row):
            for c in range(self.col):
                gridCount = (self.col * r) + c
                baseChance = self.bombCount / (10 * gridSize)
                addChance = (1 - baseChance) * (self.bombCount - bombPlaced) / (gridSize - gridCount)
                totalChance = int(100 * (baseChance + addChance))
                if random.randrange(100) < totalChance and bombPlaced < self.bombCount:
                    self.get(c, r).setBomb()
                    bombPlaced += 1
                    self.genNumbers(c, r)
                    
    def genNumbers(self, col, row):
        rad = 1
        r = [-rad,rad]
        c = [-rad,rad]
        
        if row + rad >= self.row: r[1] = self.row - row - 1
        if row - rad < 0: r[0] = -row
        if col + rad >= self.col: c[1] = self.col - col - 1
        if col - rad < 0: c[0] = -col
        
        for i in range(row + r[0], row + r[1] + 1):
            for j in range(col + c[0], col + c[1] + 1):
                if not self.get(j, i).isBomb:
                    self.get(j, i).inc()
    
    def update(self):
        if self.menu == "Main Menu":
            return self.mainMenu()
        elif self.menu == "Game":
            self.game()
        elif self.menu == "Post Game":
            self.postGame()    
        elif self.menu == "Controls":
            self.controls()
        elif self.menu == "Custom":
            self.custom()    
        elif self.menu == "Credits":
            self.credits()
        elif self.menu == "Easter1":
            self.easter1()
        return False    
            
    def mainMenu(self):
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
        
        if inp == '1': self.genGame(7, 7, 5)
        if inp == '2': self.genGame(12, 12, 15)
        if inp == '3': self.genGame(15, 15, 20)
        if inp == '4': self.menu = "Custom"
        if inp == '5': self.menu = "Credits"
        if inp == "This deserves a 100": self.menu = "Easter1"
        
        return (inp == '6')
    
    def game(self):
        self.printBoard()
        print(
            "[1] Mode: Mine",
            "[2] Mode: Flag",
            "[3] Controls",
            "[4] Give Up",
        sep = '\n')
        print('_' * (2 * self.col + 3))
        
        Aascii = ord('A')
        inp = input('\nInput: ')
        
        if len(inp) == 1:
            try:
                if int(inp) == 1: self.mode = "Mine"
                if int(inp) == 2: self.mode = "Flag"
                if int(inp) == 3: self.menu = "Controls"
                if int(inp) == 4: self.triggerPostGame(False)
            except: pass
            return
            
        for i in range((len(inp) + 1) // 3):
            col = ord(inp[i * 3]) - Aascii
            row = ord(inp[i * 3 + 1]) - Aascii 
            if col < 0 or row < 0 or col >= self.col or row >= self.row:
                continue
            self.checkInput(col, row)
                
    def printBoard(self):
        Aascii= ord('A')
        print()
        
        print('X', end = ' ')
        for c in range(self.col):
            print(chr(c + Aascii), end = ' ')
        print('X', end = ' ')    
            
        for r in range(self.row):
            print('\n' + chr(r + Aascii), end = ' ')    
            for c in range(self.col):
                self.get(c, r).print()
            print(chr(r + Aascii), end = ' ')  
                
        print()        
        print('X', end = ' ')
        for c in range(self.col):
            print(chr(c + Aascii), end = ' ')
        print('X', end = ' ')    ;        
                
        print('\n' + '_' * (2 * self.col + 3))
        print(' ' * (self.col - 9), "Flags:", self.flagCount, "Mode:", self.mode, '\n')                     
                
    def checkInput(self, col, row):
        if self.mode == "Flag":
            if self.get(col, row).toggleFlag(): self.flagCount -= 1
            else: self.flagCount += 1
            return
        
        self.get(col, row).reveal()
        
        if self.get(col, row).isBomb and not self.get(col, row).isFlag:
            self.triggerPostGame(False)
        elif self.countHidden() == self.bombCount:
            self.triggerPostGame(True)
        elif self.get(col, row).val == 0:
            self.clearBlank(col, row)
    
    def clearBlank(self, col, row):
        if self.get(col, row).val > 0: return
        
        rad = 1
        r = [-rad,rad]
        c = [-rad,rad]
        
        if row + rad >= self.row: r[1] = self.row - row - 1
        if row - rad < 0: r[0] = -row
        if col + rad >= self.col: c[1] = self.col - col - 1
        if col - rad < 0: c[0] = -col
        
        for i in range(row + r[0], row + r[1] + 1):
            for j in range(col + c[0], col + c[1] + 1):
                if not self.get(j, i).isBomb and self.get(j, i).ishidden:
                    self.get(j, i).ishidden = False
                    self.clearBlank(j, i)
    
    def triggerPostGame(self, isWin):
        self.isWin = isWin
        self.menu = "Post Game"
    
    def postGame(self):
        if not self.isWin:
            self.isVisible(False)
        self.printBoard()
        if self.isWin:
            print('\n' + ' ' * (self.col - 6), "Y O U  W I N")
        else:
            print('\n' + ' ' * (self.col - 7), "Y O U  L O S E")
       
        print("\nWhat now?")
        print("[1] Play Again")
        print("[2] Go Back to Menu")
        inp = input("\nInput: ")
        
        if inp == '1':
            self.genGame(self.col, self.row, self.bombCount)
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
                colInp = int(input("How many columns: "))
                rowInp = int(input("How many rows: "))
                bombInp = int(input("How many bombs: "))
            except: continue    
            print()
            if colInp == -1 or rowInp == -1 or bombInp == -1:
                self.menu = "Main Menu"
                return
                
            if colInp < 5 or rowInp < 5: print("Column/Row too small")
            elif colInp > 26 or rowInp > 26: print("Column/Row too large")
            elif bombInp < 1: print("Game must have at least 1 bomb")
            elif bombInp >= colInp * rowInp: print("Too many bombs")
            else: break
        self.genGame(colInp, rowInp, bombInp)
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
    game = minesweeper()
    while True:
        os.system('cls')
        if game.update(): break
