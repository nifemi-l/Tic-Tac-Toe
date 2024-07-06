<<<<<<< HEAD
#Global variable to track exit request
exit_requested = False 

# Global variables to keep track of score
score_X = 0
score_O = 0

def main(): 
    """Control the script sequence."""
    round_num = 1

    pos = [1, 2, 3, 4, 5, 6, 7, 8, 9] # initial positional values

    welcome_message()

    print(f'\n+++ Round {round_num} +++')

    executive(pos, round_num)
    
def executive(pos, round_num, letters = ['X', 'O']): 
    """Print, increment, call different functions."""
    global exit_requested
    if exit_requested:
        return # exit immediately
    
    if round_num != 'break':

        print_table(pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8], False)
    
    # variable to keep track of how many runs the users go through
    run_track = 0

    status, _ = check_win(pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8], pos, round_num)

    break_loop1, break_loop2 = 0, 0

    while status is not True: 
        if break_loop1 == 0 and break_loop2 == 0:
            break_loop1 = executive_helper(letters[0], pos, run_track, round_num)
            
            if break_loop1 == 0:
                break_loop2 = executive_helper(letters[1], pos, run_track, round_num)
        else: 
            break

def executive_helper(letter, pos, run_track, round_num): 
    """Help the executive function by running repetitive task."""
    global exit_requested
    if exit_requested:
        return 1 # exit immediately
    
    break_loop = play_table(letter, pos, run_track, round_num)

    if break_loop: 
        exit_requested = True
        return 1 # break  

    status, letter = check_win(pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8], pos, round_num)

    if status == 'break':
        return 1

    if status is True: 
        # asking the user if they would like to play again
        answer = play_again(pos, round_num)

        if answer is False: 
            return 1
        
    return 0
        
def play_table(player_letter, pos, run_track, round_num):
    """Query the user, play the table, validate."""
    global exit_requested
    # Check for exit_requested at the start of the function
    if exit_requested:
        return True 
    
    while True:
        print("Press 0 to break")

        player_input_str = input(f"{player_letter}: Select your move (1-9): ")

        status, player_input = input_validator(player_input_str)

        if player_input == 0: 
            print("\nGoodbye!\n")
            return True

        try: 
            if status is False:
                raise Exception
            
            if player_input != 0: 

                if pos[player_input - 1] != "X" and  pos[player_input - 1] != "O":

                    pos[player_input - 1] = player_letter # finding the position using adjusted input index

                    print_table(pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8], False)

                    run_track += 1
                
                elif pos[player_input - 1] == "X" or pos[player_input - 1] == "O":

                    print('That position has been played. Please try again.')

                    # recursively call this function to adjust and ask the same player who raised the exception to try again
                    play_table(player_letter, pos, run_track, round_num)

                    raise Exception 

        except Exception as e: 
            print('\nInvalid input. Please try again.')
            print_table(pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8], False)
        
        return False

def play_again(pos, round_num): 
    """Ask the user if they would like to play again, populate new game."""
    global exit_requested
    # Check for exit_requested at the start of the function
    if exit_requested:
        return 
    
    x = 0

    while x == 0: 
        # asking the user if they would like to play again
        play_again = input("Would you like to play again? (y/n): ").lower()

        if play_again == 'y': 
            # clean the table
            pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8] = 1, 2, 3, 4, 5, 6, 7, 8, 9

            # new round print
            round_num += 1
            print(f'\n+++ Round {round_num} +++')

            # score-update
            print_table(1,2,3,4,5,6,7,8,9, True)
            print()

            x = 1 

            # setting the game back in motion with this call 
            # switching the letter position to allow for playing order alternation once restarted
            return executive(pos, round_num,letters = ['O', 'X'])
            
        elif play_again == 'n': 
            print('\nGoodbye!')
            exit_requested = True
            x = 1
            return False
        
        else: 
            print ("Invalid input. Please try again.")

def input_validator(input): 
    """Validate passed input."""
    try:
        new_int = int(input)

        if new_int not in range(0, 10): 
            raise Exception
        
        else: 
            return True, new_int

    except:
        return False, input
    
def welcome_message(): 
    """Print the user a welcome message."""
    print(f"\n{'='*23}\n=== LET'S PLAY A GAME ===\n{'='*23}")

def print_table(pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9, display = False): 
    """Print the tic tac toe table and score."""
    if display == False:
        print("\nCurrent Board: ")
        print(f' {pos1} | {pos2} | {pos3}')
        print("----------")
        print(f' {pos4} | {pos5} | {pos6}') 
        print("----------")
        print(f' {pos7} | {pos8} | {pos9}')

    elif display == True:
        print(f'\nScore: Player "X" = {score_X} | Player "O" = {score_O}\n')

def check_win(pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9, pos, round_num, break_var = 0): 
    """Check to see if there is a winner, print corresponding message."""
    rows = [[pos1, pos2, pos3], [pos4, pos5, pos6], [pos7, pos8, pos9]]

    columns = [[pos1, pos4, pos7], [pos2, pos5, pos8], [pos3, pos6, pos9]]

    diagonals = [[pos1, pos5, pos9], [pos3, pos5, pos7]]

    winner = []

    if break_var == 1: 

        return 'break', None
    
    else: 

        for row in rows + columns + diagonals:
            # counters for X and O in each combination
            X_checker = row.count('X')

            O_checker = row.count('O')

            # check if there are 3 X's or O's in a row, column, or diagonal
            if X_checker == 3:
                global score_X
                score_X += 1

                print(f'\nX Wins!\n')
                winner.append('X')

                return True, 'X'
            
            elif O_checker == 3:
                global score_O
                score_O += 1
                
                print(f'\nO Wins!\n')
                winner.append('Y')

                return True, 'O'

    if len(winner) == 0: 
        # checking to see if the table is full with no winners
        table_full = restart_game_check(pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8])

        if table_full == True: 
        
            print("Aww, man! No winner this game! Better luck this round:")

            pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8] = 1, 2, 3, 4, 5, 6, 7, 8, 9 
            print()

            round_num += 1

            print(f'+++ Round {round_num} +++')

            # score-update
            print_table(1, 2, 3, 4, 5, 6, 7, 8, 9, score_X, score_O)

    return False, None

def restart_game_check(pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9): 
    """Check the status of the game and return T/F"""
    value_checker = 0 

    # iterating through all the positions
    for num in str(pos1) + str(pos2) + str(pos3) + str(pos4) + str(pos5) + str(pos6) + str(pos7) + str(pos8) + str(pos9):

        if num == "X" or num == "O": value_checker += 1

    # if all positions are letters and there is no winner
    if value_checker == 9: 
        return True
    
    else: 
        return False

=======
#Author: Waryth "Nifemi" Lawal 
#Created: 12/29/23
#Last modified: 1/1/24

def main(): 
    """Control the script sequence."""
    round_num = 1
    pos = [1, 2, 3, 4, 5, 6, 7, 8, 9] #setting initial positional values
    welcome_message() #printing the welcome message
    print()
    print(f'+++ Round {round_num} +++')

    #score tracker
    score_X = 0
    score_O = 0

    print_table(pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8], score_X , score_O, False) #printing board

    #variable to keep track of how many runs the users go through
    run_track = 0

    #variables for keeping track of which position a raised exception should jump back to
    jump_position1 = 0
    jump_position2 = 0

    #variable for keeping track of which player raises an exception (1 = X(Player 1), 2 = O(Player 2))
    player_raised_except = 0 
    
    while True:
        try: 
            #Player 1
            if jump_position1 == 0:
                print("Press 0 to break")
                player1_input = input("X: Select your move (1-9): ")

                #error handling for nonsense input
                try: 
                    player1_input = int(player1_input)
                except: 
                    player_raised_except = 1
                    raise Exception

                #raising an exception if the input is not a num in range
                if player1_input not in range(0, 10): 
                    player_raised_except = 1
                    raise Exception

                #since the position would be -1, avoid printing the -1th index
                if player1_input != 0: 
                    if pos[player1_input - 1] != "X" and  pos[player1_input - 1] != "O":
                        pos[player1_input - 1] = "X" #finding the position using adjusted input index
                        print_table(pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8], score_X, score_O, False)
                        run_track += 1
                    
                    elif pos[player1_input - 1] == "X" or pos[player1_input - 1] == "O":
                        player_raised_except = 1
                        print('That position has been played')
                        raise Exception
            
                if player1_input == 0: 
                    print()
                    print("Goodbye!") 
                    break

                #checking for a winner
                status, letter = check_win(pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8])
                if status == True: 
                    #score update
                    if letter == "X":
                        score_X += 1

                    elif letter == "O":
                        score_O += 1 

                    print_table(pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8], score_X, score_O, True)

                    winner = f'The winner is player {letter}!'
                    print((len(winner) + 2) * '-')
                    print(f'|{winner}|')
                    print((len(winner) + 2) * '-')   
                    print('---') 
                    print()

                    #variable for  keeping track of y/n
                    n = 0

                    while True: 
                        try: 
                            #asking the user if they would like to play again (case-insensitive) 
                            play_again = input("Would you like to play again? (y/n): ").lower()

                            if play_again == 'y': 
                                #clean the table
                                pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8] = 1, 2, 3, 4, 5, 6, 7, 8, 9
                                print()
                                #new round print
                                round_num += 1
                                print(f'+++ Round {round_num} +++')
                                #score-update
                                print_table(1,2,3,4,5,6,7,8,9, score_X, score_O, False)
                                print()
                                #skip player 2's turn
                                jump_position2 = 1
                                break
                                
                            elif play_again == 'n': 
                                print()
                                print('Goodbye!')
                                n = 1
                                break
                            
                            else: 
                                raise Exception
                            
                        except: 
                            print('You did not enter "y" or "n". Try again (case-insensitive)')

                    #break the entire loop if the user does not want to play
                    if n == 1: break 
                
                #checking to see if the table is full with no winners
                table_full = restart_game_check(pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8])
                if table_full == True: 
                    print("Aww, man! No winner this game! Better luck this round:")
                    pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8] = 1, 2, 3, 4, 5, 6, 7, 8, 9 
                    print()
                    round_num += 1
                    print(f'+++ Round {round_num} +++')
                    #score-update
                    print_table(1, 2, 3, 4, 5, 6, 7, 8, 9, score_X, score_O)
                    
                jump_position1 = 0
                jump_position2 = 0

            #Player 2
            if jump_position2 == 0: 
                player2_input = (input("O: Select your move (1-9): "))

                #error handling for nonsense input
                try: 
                    player2_input = int(player2_input)
                except: 
                    player_raised_except = 2
                    raise Exception
                
                #raising an exception if the input is not a num in range
                if player2_input not in range(0, 10): 
                    player_raised_except = 2
                    raise Exception
                
                #handling to avoid overriding a played position
                #since the position would be -1, avoid printing the -1th index
                if player2_input != 0: 
                    if pos[player2_input - 1] != "X" and pos[player2_input - 1] != "O":
                        pos[player2_input - 1] = "O" #finding the position using adjusted input index
                        print_table(pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8], score_X, score_O, False)
                        run_track += 1

                    elif pos[player2_input - 1] == "X" or pos[player2_input - 1] == "O":
                        player_raised_except = 2
                        print('That position has been played.')
                        raise Exception
                
                #checking for a winner
                status, letter = check_win(pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8])
                if status == True: 
                    #score update
                    if letter == "X":
                        score_X += 1

                    elif letter == "O":
                        score_O += 1 

                    print_table(pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8], score_X, score_O, True)

                    winner = f'The winner is player {letter}!'
                    print((len(winner) + 2) * '-')
                    print(f'|{winner}|')
                    print((len(winner) + 2) * '-')
                    print('---') 
                    print()
                    
                    #variable for keeping track of y/n
                    n = 0
                    
                    #check for whether the user wants to play or not
                    while True: 
                        try: 
                            #asking the user if they would like to play again (case-insensitive) 
                            play_again = input("Would you like to play again? (y/n): ").lower()
                            if play_again == 'y': 
                                #clean the table
                                pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8] = 1, 2, 3, 4, 5, 6, 7, 8, 9
                                print()
                                #new round print
                                round_num += 1
                                print(f'+++ Round {round_num} +++')
                                #score-update
                                print_table(1,2,3,4,5,6,7,8,9, score_X, score_O)
                                print()
                                break
                            
                            elif play_again == 'n': 
                                print()
                                print('Goodbye!')
                                n = 1
                                break
                            
                            else: 
                                raise Exception
                            
                        except: 
                            print('You did not enter "y" or "n". Try again (case-insensitive)')

                    #break the entire loop if the user does not want to play
                    if n == 1: break 

                #break statement
                if player2_input == 0: 
                    print()
                    print("Goodbye!") 
                    break

                #checking to see if the table is full with no winners
                table_full = restart_game_check(pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8])
                if table_full == True: 
                    #clean the table
                    print("Aww, man! No winner this game! Better luck this round:")
                    pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8] = 1, 2, 3, 4, 5, 6, 7, 8, 9 
                    print()
                    #new round print
                    round_num += 1
                    print(f'+++ Round {round_num} +++')
                    #score-update
                    print_table(1, 2, 3, 4, 5, 6, 7, 8, 9, score_X, score_O)
                    
                #resetting jump position if any change occurs
                jump_position2 = 0
                jump_position1 = 0
                                   
        except: 
            print()
            print('Invalid Input. Please try again...')
            print_table(pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7], pos[8], score_X, score_O, False)

            #logic for finding jump position:
            #if player 2 raised the exception, none for p1 since it will auto. jump there
            if player_raised_except == 2: 
                #exclude the first player block & go to second
                jump_position1 = 1

def welcome_message(): 
    print()
    print("========================")
    print("=== LET'S PLAY A GAME ===")
    print ("========================")

def print_table(pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9, score_X, score_O, display = False): 
    """Print the tic tac toe table and score."""
    if display == False:
        print()
        print("Current Board: ")
        print(f' {pos1} | {pos2} | {pos3}')
        print("----------")
        print(f' {pos4} | {pos5} | {pos6}') 
        print("----------")
        print(f' {pos7} | {pos8} | {pos9}')

    #print the score at the end of the game
    elif display == True:
        print()
        print(f'Score: Player "X" = {score_X} | Player "O" = {score_O}')
        print() 

def check_win(pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9): 
    rows = [[pos1, pos2, pos3], [pos4, pos5, pos6], [pos7, pos8, pos9]]
    columns = [[pos1, pos4, pos7], [pos2, pos5, pos8], [pos3, pos6, pos9]]
    diagonals = [[pos1, pos5, pos9], [pos3, pos5, pos7]]

    for row in rows + columns + diagonals:
        # Counters for X and O in each combination
        X_checker = row.count('X')
        O_checker = row.count('O')

        #Check if there are 3 X's or O's in a row, column, or diagonal
        if X_checker == 3:
            return True, 'X'
        elif O_checker == 3:
            return True, 'O'
        
    return False, None

def restart_game_check(pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9): 
    """Check the status of the game and return T/F"""
    #creating a variable for keeping track of the type of positions
    value_checker = 0 

    #iterating through all the positions
    for num in str(pos1) + str(pos2) + str(pos3) + str(pos4) + str(pos5) + str(pos6) + str(pos7) + str(pos8) + str(pos9):
        if num == "X" or num == "O":
            value_checker += 1
    
    #if all positions are letters and there is no winner
    if value_checker == 9: 
        return True
    else: 
        return False

>>>>>>> fcfe227beefd8824a1db53793a10a31b385022ac
main()