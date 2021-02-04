import pygame
import random
pygame.init()
SCREEN_SIZE = (500, 500)
SCREEN_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
running = True
screen = pygame.display.set_mode(SCREEN_SIZE)
X,O,E,T = 1,-1,99999,0
image_x = pygame.image.load("image_x.png").convert_alpha()
image_o = pygame.image.load("image_o.png").convert_alpha()
image_logo = pygame.image.load("logo.png").convert_alpha()
pygame.display.set_icon(image_logo)
pygame.display.set_caption("Tic-Tac-Toe")
board = [[E, E, E],
         [E, E, E],
         [E, E, E],]
line_rect = [0, 0, 0, 0]
turn = O

def draw_board():
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == X:
                screen.blit(image_x, ((j+1)*100, (i+1)*100))
            elif board[i][j] == O:
                screen.blit(image_o, ((j+1)*100, (i+1)*100))
    try:
        pygame.draw.rect(screen, LINE_COLOR, tuple(line_rect))
    except TypeError as e:
        pygame.draw.polygon(screen, LINE_COLOR, tuple(line_rect))       
def winner(board):
    line_rect = [0,0,0,0]
    for row in range(len(board)):
        if sum(board[row]) == 3:
            line_rect = [100, (row+1.5)*100-10, 300, 20]
            return X,line_rect
        elif sum(board[row]) == -3:
            line_rect = [100, (row+1.5)*100-10, 300, 20]
            return O,line_rect
        
    rev_board = list(reversed(list(zip(*board))))
    for col in range(len(rev_board)):
        if sum(rev_board[col]) == 3:
            line_rect = [((2-col)+1.5)*100-10, 100, 20, 300]
            return X,line_rect
        elif sum(rev_board[col]) == -3:
            line_rect = [((2-col)+1.5)*100-10, 100, 20, 300]
            return O,line_rect
        
    dia1 = [board[0][0],board[1][1],board[2][2]]
    dia2 = [board[2][0],board[1][1],board[0][2]]
    dias = [dia1, dia2]
    for dia in range(len(dias)):
        if sum(dias[dia]) == 3:
            if dia == 1: line_rect = [(386,100),(400,114),(114,400),(100,386)]
            elif dia == 0: line_rect = [(100,114),(114,100),(400,386),(386,400)]
            return X,line_rect
        elif sum(dias[dia]) == -3:
            if dia == 1: line_rect = [(386,100),(400,114),(114,400),(100,386)]
            elif dia == 0: line_rect = [(100,114),(114,100),(400,386),(386,400)]
            return O,line_rect
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == E:
                return E,line_rect
    return T,line_rect
def update_board(turn):
    global line_rect
    if turn == X:
        turn = O
        i,j = minimax(X, board, True)
        board[i][j] = X
    elif turn == O:
        x, y = pygame.mouse.get_pos()
        i, j = y//100-1, x//100-1
        if valid_spot(i,j,board):
            turn = X
            board[i][j] = O

    result,line_rect = winner(board)
    if result == X:
        print("X Won")
        turn = E
    elif result == O:
        print("O Won")
        turn = E
    elif result == T:
        print("No One Won")
        turn = E      
    return turn
def random_move(board):
    while True:
       i,j = random.randrange(0, 3), random.randrange(0, 3)
       if valid_spot(i,j,board):
           return (i,j)
def valid_spot(i, j, board):
    return True if board[i][j] == E else False

def minimax(turn, board, first = False):
    score,line = winner(board)
    if score != E:
        return score
    else:
        best_move = (3,0)
        if turn == X: #pick highest score
            high_score = -1000000
            for i in range(len(board)):
                for j in range(len(board)):
                    if board[i][j] == E:
                        board[i][j] = X
                        score = minimax(O, board)
                        if score > high_score:
                            high_score = score
                            best_move = (i,j)
                        board[i][j] = E;
            return high_score if not first else best_move
        elif turn == O:
            low_score = 1000000
            for i in range(len(board)):
                for j in range(len(board)):
                    if board[i][j] == E:
                        board[i][j] = O
                        score = minimax(X, board)
                        if score < low_score:
                            low_score = score
                            best_move = (i,j)
                        board[i][j] = E;       
            return low_score if not first else best_move

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            turn = update_board(turn)        
    screen.fill(SCREEN_COLOR)
    if turn == X:
        turn = update_board(turn)
    draw_board()
    pygame.display.update()
pygame.quit()
