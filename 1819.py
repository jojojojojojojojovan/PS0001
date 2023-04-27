import numpy as np
from random import randint

class Game:
    mat = None # this represents the board matrix
    rows = 0 # this represents the number of rows of the board
    cols = 0 # this represents the number of columns of the board
    turn = 0 # this represents whose turn it is (1 for player 1, 2 for player 2)
    wins = 0 # this represents the number of consecutive disks you need to force in order to win
    col = 0 # this represents the column in which the last disk was placed
    row = 0 # this represents the row in which the last disk was placed
    pop = 0  # this represents if the move is pop (0 for add, 1 for pop)

    
def check_victory(game):
    draw = True
    for i in game.mat[game.rows-1]:
        if i == 0:
            draw = False
    if draw:
        return 3
    elif udwin(game)==game.turn or\
    lrwin(game,game.row,game.turn,game.pop)==game.turn or\
    newin(game,game.row,game.turn,game.pop)==game.turn or\
    nwwin(game,game.row,game.turn,game.pop)==game.turn:
        return game.turn
    elif udwin(game)==0 and lrwin(game,game.row,game.turn,game.pop)==0 and \
         newin(game,game.row,game.turn,game.pop)==0 and\
         nwwin(game,game.row,game.turn,game.pop)==0:
        return 0
    else:
        if game.turn == 1:
            return 2
        else:
            return 1


def udwin(game): #vertical(up down) win
    if game.pop:
        return 0
    else:
        ud = 1
        row = game.row - 1
        while row>=0 and ud != game.wins:
            if game.mat[row][game.col] == game.turn:
                ud+=1
                row-=1
            else: break
        if ud == game.wins: return game.turn
        else: return 0


def lrwin(game,row,turn,pop): #horizontal(left right) win
    if pop:
        opponent = False
        for i in range(game.row):
            if 1<=lrwin(game,i,game.mat[i][game.col],0)<=2:
                if game.mat[i][game.col] == game.turn:
                    return game.turn
                else:
                    opponent = True
        if opponent:
            if game.turn == 1:
                return 2
            else:
                return 1
        else:
            return 0
    else:
        lr = 1
        col_l = game.col - 1
        col_r = game.col + 1
        while col_r<game.cols and lr != game.wins:
            if game.mat[row][col_r] == turn:
                lr+=1
                col_r+=1
            else:
                break
        while col_l>=0 and lr != game.wins:
            if game.mat[row][col_l] == turn:
                lr+=1
                col_l-=1
            else:
                break
        if lr == game.wins:
            return turn
        else:
            return 0


def newin(game,row,turn,pop): #diagonal right (northeast) win
    if pop:
        opponent = False
        for i in range(game.row):
            if 1<=newin(game,i,game.mat[i][game.col],0)<=2:
                if game.mat[i][game.col] == game.turn:
                    return game.turn
                else:
                    opponent = True
        if opponent:
            if game.turn == 1:
                return 2
            else:
                return 1
        else:
            return 0
    else:
        ne = 1
        col_r = game.col + 1
        col_l = game.col - 1
        row_u = row + 1
        row_d = row - 1
        while row_u<game.rows and col_r<game.cols and ne != game.wins:
            if game.mat[row_u][col_r] == turn:
                ne+=1
                row_u+=1
                col_r+=1
            else:
                break
        while row_d>=0 and col_l>=0 and ne!=game.wins:
            if game.mat[row_d][col_l] == turn:
                ne+=1
                row_d-=1
                col_l-=1
            else:
                break
        if ne == game.wins:
            return turn
        else:
            return 0

        
def nwwin(game,row,turn,pop): #diagonal left (northwest) win
    if pop:
        opponent = False
        for i in range(game.row):
            if 1<=nwwin(game,i,game.mat[i][game.col],0)<=2:
                if game.mat[i][game.col] == game.turn:
                    return game.turn
                else:
                    opponent = True
        if opponent:
            if game.turn == 1:
                return 2
            else:
                return 1
        else:
            return 0
    else:
        nw = 1
        col_r = game.col + 1
        col_l = game.col - 1
        row_u = row + 1
        row_d = row - 1
        while row_u<game.rows and col_l>=0 and nw != game.wins:
            if game.mat[row_u][col_l] == turn:
                nw+=1
                row_u+=1
                col_l-=1
            else:
                break
        while row_d>=0 and col_r<game.cols and nw != game.wins:
            if game.mat[row_d][col_r] == turn:
                nw+=1
                row_d-=1
                col_r+=1
            else:
                break
        if nw == game.wins:
            return turn
        else:
            return 0
    

def apply_move(game,col,pop):
    game.row = 0
    while True:
        if game.row<game.rows-1 and game.mat[game.row][col]!=0: #5
            game.row+=1
        elif not pop:
            game.mat[game.row][col] = game.turn
            break
        else:
            for i in range(game.row):
                game.mat[i][col] = game.mat[i+1][col]
            game.mat[game.row][col] = 0
            break
    return game
            
        
def check_move(game,col,pop):
    row = game.rows-1
    if pop:
        if game.mat[0][col] != game.turn:
            return False
        else:
            return True
    elif game.mat[row][col]!=0: return False
    else: return True


def computer_move(game,level):
    pass


def display_board(game):
    board = np.flipud(game.mat)
##    print("-"*(5+game.cols*3+3))
##    for i in range(game.rows):
##        print(" "*5, end='')
##        for j in range(game.cols):
##            if board[i][j] == 0:
##                print(".",end="  ")
##            elif board[i][j] == 1:
##                print("O",end="  ")
##            else:
##                print("X",end="  ")
##        print()
##    print("-"*(5+game.cols*3+3))
##    print(5*" ",end='')
##    for i in range(game.cols):
##        print(i+1," ",end='')
##    print()
    print("-"*(5+game.cols*3+3))
    for i in board:
        string = " "*5+"  ".join(map(str,i))
        string=string.replace("0",".")
        string=string.replace("1","O")
        string=string.replace("2","X")
        print(string)
    print("-"*(5+game.cols*3+3))
    print(5*" ",end='')
    for i in range(game.cols):
        if i<9:
            print(i+1," ",end='')
        else:
            print(i+1,"",end='')
    print("\n"+"-"*(5+game.cols*3+3))
        
def propername(game, name, player):
    while name == "":
        name = input("Enter a proper player "+player+" name("
                     +game.discs[int(player)]+"): ")
    return name


def menu():
    sameplayer = False
    while True:
        game = Game()
        while True:
            rows = input("How many rows(3-20): ")
            if rows.isdigit() and 3<=int(rows)<=20:
                game.rows = int(rows)
                break
        while True:
            cols = input("How many columns(3-20): ")
            if cols.isdigit() and 3<=int(cols)<=20:
                game.cols = int(cols)
                break
        while True:
            lowest = min(game.cols,game.rows)
            wins = input("How many consecutive discs to win(3-"+str(lowest)+"): ")
            if wins.isdigit() and 3<=int(wins)<=lowest:
                game.wins = int(wins)
                break
        game.mat = np.zeros((game.rows,game.cols),dtype=int)
        game.turn = randint(1,2)
        game.discs = [0,'O','X']
        
        if not sameplayer:
            player1 = input("Enter player 1 name("+game.discs[1]+"): ")
            if player1 == "":
                player1 = propername(game, player1,'1')
                
            player2 = input("Enter player 2 name("+game.discs[2]+"): ")
            if player2 == "":
                player2 = propername(game, player2,'2')
                
            players = [0, player1, player2]
            
            for i in range(1,3):
                players[i] = players[i][0].upper() + players[i][1:]
                
        print("\nChoosing player to start......")        
        print(players[game.turn].upper(), "starts!".upper())

        while True:
            positions = [str(i) for i in range(1,game.cols+1)]
            display_board(game)
            print("\n1. Drop\n2. Pop")
            while True:
                pop = input(players[game.turn]+"'s turn("+game.discs[game.turn]+
                            "). Drop or Pop? ")
                if pop == "1" or pop=="2":
                    game.pop = int(pop)-1
                    break            
            if (not game.pop) or (game.turn not in game.mat[0]):
                if (game.turn not in game.mat[0]) and game.pop:
                    game.pop -= 1
                    print("Cant pop, must drop.")
                pos = input(players[game.turn]+"'s turn("+game.discs[game.turn]+
                            "). Choose position to drop(1-"+str(game.cols)+")! ")
            else: pos = input(players[game.turn]+"'s turn("+game.discs[game.turn]+
                            "). Choose position to pop(1-"+str(game.cols)+")! ")
          
            while (pos not in positions) or \
                  check_move(game,int(pos)-1,game.pop)==False:
                if pos not in positions:
                    print("You have entered an invalid number.")
                else:
                    print("Position selected is invalid.")
                if game.pop: pos = input(players[game.turn]+"'s turn("+
                                         game.discs[game.turn]+"). Choose "\
                                         "position to pop(1-"+str(game.cols)+")! ")
                else: pos = input(players[game.turn]+"'s turn("+game.discs
                                  [game.turn]+"). Choose position to drop(1-"+
                                  str(game.cols)+")! ")
            game.col = int(pos)-1
            apply_move(game, game.col, game.pop)
            winner = check_victory(game)
            if winner==0:
                if game.turn == 1:
                    game.turn = 2
                else:
                    game.turn = 1
            else:
                print()
                display_board(game)
                if winner==3:
                    print("\nGAME OVER, IT'S A DRAW")
                else:
                    print("\nGAME OVER,",players[winner],"WINS")
                print("-"*60+"\n")
                restart = input("New game? (Y/N) ")
                yesno = ["y","Y","n","N","yes","YES","no","NO","Yes","No"]
                while restart not in yesno:
                    restart = input("Enter Y/N\nNew game? (Y/N) ")    
                break
            print()
            
        if restart[0].upper() == "N":
            break
        else:
            same = input("Same players? (Y/N)")
            while same not in yesno:
                same = input("Enter Y/N\nSame players? (Y/N) ")
            if same[0].upper() == "Y":
                sameplayer = True
            else:
                sameplayer = False
        

menu()
