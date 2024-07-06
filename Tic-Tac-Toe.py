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
main()