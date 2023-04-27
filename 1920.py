import numpy as np
import random


def display_board(board): #display board
    print("        8 1")
    print("        \u2190 \u2192")
    print("  "*2,end='')
    for j in range(len(board)):
        print(j,end=' ')
    print("\n"+"  "*2+"-"*(len(board)*2-1))
    for i in range(len(board)): #formating display board
        if i == 2:
            row = "7\u2191"
        elif i == 3:
            row = "6\u2193"
        else:
            row = "  "
        row += str(i)+"|"+" ".join(map(str,board[i][:3]))+"|"+\
              " ".join(map(str,board[i][3:]))#setting the column segregation 
        if i == len(board)//2:
            print("    "+"-"*(len(board)*2-1)) #setting the row segregation
        if i == 2:
            row += "\u21912"
        elif i == 3:
            row += "\u21933"
        print(row)
    print("        \u2190 \u2192")
    print("        5 4")
    

def check_victory(board,turn,rot): #check win/lose/draw or continue
    #unrotate board first
    if rot%2 == 0: #if rot is even
        unrot = rot - 1 
    else: #if rot is odd
        unrot = rot + 1 
    rotate(board,unrot) #unrotate board

    #check win when marble is placed
    if win(board, turn): #check if current player wins when placing marble
        return turn #current player wins
    else: #check win after rotation
        rotate(board,rot) #rotate board
        if turn == 1:
            opponent = 2
        else: #current player is 2
            opponent = 1 #opponent is 1
        if win(board, turn): #if current player gets 5 in a row
            if win (board, opponent): #if opponent gets 5 in a row
                return 3 #game draw
            else: #opponent didn't get 5 in a row
                return turn #current player wins
        elif win(board,opponent): #current player didn't get 5 in a row but opponent got
            return opponent #opponent wins
        else: #both didn't get 5 in a row
            draw = True 
            for i in range(6): #run through all rows
                for j in range(6): #run through all columns
                    if board[i][j]==0: #there's empty space to put marble
                        draw = False 
                        break
                if draw == False: break 
            else: #no empty space to put marbles
                return 3 #game draw
            return 0 #game continue

        
def win(board,turn): #check if there is a win
    for i in range(6): #horizontal win
        for j in range(2):
            if board[i][j] == turn:
                if board[i][j]==board[i][j+1]==board[i][j+2]\
                   ==board[i][j+3]==board[i][j+4]:
                    return True
    for i in range(6): #vertical win
        for j in range(2):
            if board[j][i] == turn:
                if board[j][i]==board[j+1][i]==board[j+2][i]\
                   ==board[j+3][i]==board[j+4][i]:
                    return True
    for i in range(2):
        for j in range(2):#diagonal right down(southeast) win
            if board[i][j] == turn:
                if board[i][j]==board[i+1][j+1]==board[i+2][j+2]\
                   ==board[i+3][j+3]==board[i+4][j+4]:
                    return True
    for i in range(4,6): #diagonal right up(northeast) win
        for j in range(2):
            if board[i][j] == turn:
                if board[i][j]==board[i-1][j+1]==board[i-2][j+2]\
                   ==board[i-3][j+3]==board[i-4][j+4]:
                    return True
    return False

    
def apply_move(board,turn,row,col,rot): #place marble and rotate
    insert(board,turn,row,col) #place marble
    rotate(board,rot) #rotate board
    return board


def insert(board,turn,row,col): #place marble at position
    board[row][col] = turn
    return board


def rotate(board,rot): #rotate board
    if rot == 1 or rot == 2:
        subboard = board[:3,3:6]
        if rot == 1:
            board[:3,3:6]=np.rot90(subboard,3)
        else:
            board[:3,3:6]=np.rot90(subboard)            
    elif rot == 3 or rot == 4:
        subboard = board[3:6,3:6]
        if rot == 3:
            board[3:6,3:6]=np.rot90(subboard,3)
        else:
            board[3:6,3:6]=np.rot90(subboard)
    elif rot == 5 or rot == 6:
        subboard = board[3:6,:3]
        if rot == 5:
            board[3:6,:3]=np.rot90(subboard,3)
        else:
            board[3:6,:3]=np.rot90(subboard)
    else:
        subboard = board[:3,:3]
        if rot == 7:
            board[:3,:3]=np.rot90(subboard,3)
        else:
            board[:3,:3]=np.rot90(subboard)
    return board


def check_move(board,row,col): #check if position is filled/empty
    if board[row][col] != 0: #position is filled
        return False
    return True


def computer_move(board,turn,level): #determine computer move
    if level == 1: #level 1
        rot = random.randint(1,8) #random rot value
        while True:
            row = random.randint(0,5) #random row value
            col = random.randint(0,5) #random col value
            if check_move(board, row, col): #if got space
                return (row,col,rot)
    elif level==2 or level == 3: #level 2 or 3
        open_slot = np.where(board == 0)
        rows = open_slot[0]
        cols = open_slot[1]
        for i in range(len(rows)): #computer can win
            row = rows[i]
            col = cols[i]
            for j in range(1,9):
                temp_board = board.copy()
                rot = j
                apply_move(temp_board,turn,row,col,rot)
                if check_victory(temp_board,turn,rot) == turn: #computer win
                    return (row,col,rot) #use that row,col,rot
                
        #computer cannot win
        choices = []
        acceptable_move = None
        for i in range(len(rows)): #put all possible move in a list
            for j in range(1,9):
                choices.append((rows[i],cols[i],j))
        
        while choices != []: #while list is not empty
            index = random.randint(0,len(choices)-1) #generate random number
            choice = choices[index] #choose 1 choice from list
            row = choice[0]
            col = choice[1]
            rot = choice[2]
            temp_board = board.copy()
            apply_move(temp_board,turn,row,col,rot) #apply move of choice
            open_slot2 = np.where(temp_board == 0) #find where is empty
            rows2 = open_slot2[0]
            cols2 = open_slot2[1]

            #checking if player can win
            playerwin = False
            for l in range(len(rows2)): 
                row2 = rows2[l]
                col2 = cols2[l]
                for m in range(1,9):
                    temp_board2 = temp_board.copy()
                    rot2 = m
                    apply_move(temp_board2,1,row2,col2,rot2)
                    if check_victory(temp_board2,1,rot2)==1:
                        playerwin = True #player still can win with the row,col and rot
                        break
                if playerwin:
                    break
            else: #player cannot win with chosen row col and rot
                if level == 2: return choice #use that choice
                else: #level 3
                    scores = count_score(board, choice)
                    if acceptable_move == None:
                        acceptable_move = choice + scores
                    else:
                        if scores[0] > acceptable_move[3]:
                            acceptable_move = choice + scores
                        elif scores[0] == acceptable_move[3]:
                            if scores[1] > acceptable_move[4]:
                                acceptable_move = choice + scores
                        #else: pass
            choices.remove(choice) #choice cant be used
        else: #all choices cant be used, opponent surely win.   
            if level == 3:
                if acceptable_move != None:
                    return acceptable_move[:3]
            rot = random.randint(1,8)
            index = random.randint(0,len(rows)-1) 
            row = rows[index]
            col = cols[index]
        return(row,col,rot)
    

def count_score(board, inputs): #count score for level 3
    row = inputs[0]
    col = inputs[1]
    rot = inputs[2]
    temp_board = board.copy()
    apply_move(temp_board, 2, row, col, rot)
    player = 0
    opponent = 0
    
    player_slot = np.where(temp_board == 2)
    playerrows = list(player_slot[0])
    playercols = list(player_slot[1])
    opponent_slot = np.where(temp_board == 1)
    opponentrows = list(opponent_slot[0])
    opponentcols = list(opponent_slot[1])
    for i in range(6):
        playerrowcount = playerrows.count(i)
        playercolcount = playercols.count(i)
        opprowcount = opponentrows.count(i)
        oppcolcount = opponentcols.count(i)
        if playerrowcount > 1:
            player+=10**(playerrowcount-1)
        if playercolcount > 1:
            player+=10**(playercolcount-1)
        if opprowcount > 1:
            opponent+=10**(opprowcount-1)
        if oppcolcount > 1:
            opponent+=10**(oppcolcount-1)
    for i in range(1,3):
        d1 = list(temp_board[1:].diagonal()).count(i)
        d2 = list(temp_board.diagonal()).count(i)
        d3 = list(temp_board.diagonal(1)).count(i)
        d4 = list(np.flipud(temp_board).diagonal()).count(i)
        d5 = list(np.flipud(temp_board).diagonal(1)).count(i)
        d6 = list(np.flipud(temp_board)[1:].diagonal()).count(i)
        if i == 1:
            if d1 > 1:
                opponent+=10**(d1-1)
            if d2 > 1:
                opponent+=10**(d2-1)
            if d3 > 1:
                opponent+=10**(d3-1)
            if d4 > 1:
                opponent+=10**(d4-1)
            if d5 > 1:
                opponent+=10**(d5-1)
            if d6 > 1:
                opponent+=10**(d6-1)
        if i == 2:
            if d1 > 1:
                player+=10**(d1-1)
            if d2 > 1:
                player+=10**(d2-1)
            if d3 > 1:
                player+=10**(d3-1)
            if d4 > 1:
                player+=10**(d4-1)
            if d5 > 1:
                player+=10**(d5-1)
            if d6 > 1:
                player+=10**(d6-1)

    points = player - opponent
    return (points,player,opponent)

   
def get_inputs(board,turn): #get row,col,rot inputs from user
    while True: #check if user row,col is valid
        row,col = get_input(board,turn,"row"),get_input(board,turn,"col")
        if check_move(board, row, col): #position choice is empty
            break #end while loop, user input valid
        print("Row {}, Column {} is filled\n".format(row,col)) #user chose filled position
    rot = get_input(board,turn,"rotation") #get rot from user
    return row,col,rot


def get_input(board,turn,input_type): #get user input
    if input_type == "rotation":
        inputs = [str(i) for i in range(1,9)] #rot only has from 1-8
        rotation_index() #display rotation message
    else:
        inputs = [str(i) for i in range(6)] #row/col has from 0-5
    value = input("Player {}, enter {}({}-{}): ".format\
                   (str(turn),input_type,inputs[0],inputs[len(inputs)-1])) #get input from user
    while True: #check validity
        if value in inputs: #user input valid
            return int(value) #return input by user
        #user input invalid
        print("Invalid input") 
        value = input("Player {}, enter {}({}-{}): ".format\
                       (str(turn),input_type,inputs[0],inputs[len(inputs)-1])) #ask again

            
def rotation_index(): #display rotation message
    print("\n1. Top right square turns clockwise")
    print("2. Top right square turns anticlockwise")
    print("3. Bottom right square turns clockwise")
    print("4. Bottom right square turns anticlockwise")
    print("5. Bottom left square turns clockwise")
    print("6. Bottom left square turns anticlockwise")
    print("7. Top left square turns clockwise")
    print("8. Top left square turns anticlockwise\n")


def game_end(board,status): #display board and who won/draw
    display_board(board) #show board
    if status == 3: #draw
        print("Player 1 and player 2 draw")
    elif status == 1: #1 won
        print("Player 1 won")
    else: #2 won
        print("Player 2 won")
        
        
def menu(): #menu function
    play = True
    while play:
        game_board = np.zeros((6,6),dtype=int) #create 6x6 board
        player = random.randint(1,2)
        print("1. Play with friend") 
        print("2. Play with Computer(level 1: Easy)") 
        print("3. Play with Computer(level 2: Medium)")
        print("4. Play with Computer(level 3: Hard)")
        print("5. Exit")
        choice = input("Enter choice(1-5): ") #gets user input on option

        while True: #check if user input is valid
            if choice != "1" and choice != "2" and choice != "3" and choice != "4" and choice != "5": #user input not valid
                print("Invalid choice")
                choice = input("Enter choice(1-5): ") #ask for user input again
            else: break #user input valid
            
        if choice == "5":
            return None
        elif (choice == "2" or choice =="3" or choice == "4") and player == 2:
            print("Computer start".upper())
        else:
            print("Player {} start".format(player).upper())
        print()
        
        while True: #start game
            display_board(game_board) #show board
            print()
            if choice == "2" and player == 2: #computer1's turn
                row,col,rot = computer_move(game_board, 2, 1) #get row,col,rot for computer1
                print("Computer move: row: {}, col: {}, rot: {}".format(row,col,rot))
            elif choice == "3" and player == 2: #computer2's turn
                row,col,rot = computer_move(game_board, 2, 2) #get row,col,rot for computer2
                print("Computer move: row: {}, col: {}, rot: {}".format(row,col,rot))
            elif choice == "4" and player == 2: #computer2's turn
                row,col,rot = computer_move(game_board, 2, 3) #get row,col,rot for computer3
                print("Computer move: row: {}, col: {}, rot: {}".format(row,col,rot))
            else: #player's turn            
                row,col,rot = get_inputs(game_board,player) #get row,col,rot for current player
            apply_move(game_board, player, row, col, rot) #apply move
            game_status = check_victory(game_board, player, rot) #check victory
            if game_status == 0: #no win, lose or draw yet
                if player == 1: #swap players
                    player = 2
                else:
                    player = 1
            else: #win, lose or draw
                game_end(game_board, game_status) #display game over message
                while True:
                    restart = input("Play again? (Y/N)")
                    if restart == "y" or restart == "Y":
                        print()
                        break
                    elif restart == "n" or restart == "N":
                        play = False
                        break
                    else:
                        print("Invalid choice")
                break
        

menu()
