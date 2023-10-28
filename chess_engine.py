# Libraries used
import random
import chess
import pygame
import sys
import tkinter as tk
import game_controller as gc
from button import Button
from tkinter import messagebox
import pygetwindow as gw

# Buttons images
AI_START_BUTTON_IMAGE = pygame.image.load("images/ai_button.png")
HUMAN_START_BUTTON_IMAGE = pygame.image.load("images/human_button.png")
WHITE_BUTTON_IMAGE = pygame.image.load(f"images/pieces/w/K.png")
BLACK_BUTTON_IMAGE = pygame.image.load(f"images/pieces/b/k.png")
BUTTON_0_IMAGE = pygame.image.load("images/button_0.png")
BUTTON_1_IMAGE = pygame.image.load("images/button_1.png")
BUTTON_2_IMAGE = pygame.image.load("images/button_2.png")
BUTTON_3_IMAGE = pygame.image.load("images/button_3.png")
BUTTON_4_IMAGE = pygame.image.load("images/button_4.png")
BUTTON_GO_BACK_IMAGE = pygame.image.load("images/button_go_back.png")
GO_BUTTON_IMAGE = pygame.image.load("images/horse-button.png")
SCREEN_SIZE_1_BUTTON_IMAGE = pygame.image.load("images/screen_size_1_button.png")
SCREEN_SIZE_2_BUTTON_IMAGE = pygame.image.load("images/screen_size_2_button.png")

clock = pygame.time.Clock()


def initialize_pygame_tkinter():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Chess Engine')
    root = tk.Tk()
    root.withdraw()


def start_game_configuration():
    gc.board.set_fen(chess.STARTING_FEN)
    gc.board.turn = chess.WHITE
    gc.board.clear_stack()
    gc.board._is_checkmate = False
    get_piece_images()
    draw_board(gc.chess_screen, gc.board)
    pygame.display.flip()


def get_piece_images():
    for piece_type in ['p', 'r', 'n', 'b', 'q', 'k']:
        filename = f"images/pieces/b"
        put_image_on_list(filename, piece_type)

    for piece_type in ['P', 'R', 'N', 'B', 'Q', 'K']:
        filename = f"images/pieces/w"
        put_image_on_list(filename, piece_type)


def put_image_on_list(filename, piece_type):
    filename += f"/{piece_type}.png"
    img = pygame.image.load(filename)
    img = pygame.transform.scale(img, (gc.SQUARE_SIZE, gc.SQUARE_SIZE))
    gc.piece_images[chess.Piece.from_symbol(piece_type)] = img


def draw_board(screen, board):
    for square in chess.SQUARES:
        file = chess.square_file(square) * gc.SQUARE_SIZE
        rank = (7 - chess.square_rank(square)) * gc.SQUARE_SIZE

        square_color = (255, 255, 255) if (chess.square_file(square) + chess.square_rank(square)) % 2 != 0 else (
        150, 150, 150)

        square_rectangle = pygame.Rect(file, rank, gc.SQUARE_SIZE, gc.SQUARE_SIZE)
        pygame.draw.rect(screen, square_color, square_rectangle)
        piece = board.piece_at(square)

        if piece:
            img = gc.piece_images[piece]
            screen.blit(img, (file, rank))


def get_square_from_mouse(mouse_position):
    rank = int(mouse_position[0] / gc.SQUARE_SIZE)  # As I want to get a single square,
    file = int(mouse_position[1] / gc.SQUARE_SIZE)  # I cast to int, so I don't get decimals.
    square = chess.square(rank, 7 - file)
    return square


def highlight_selected_square(current_square, last_square):
    if last_square is not None:
        file = last_square.x / gc.SQUARE_SIZE
        rank = 7 - (last_square.y / gc.SQUARE_SIZE)
        square_color = (255, 255, 255) if (file + rank) % 2 != 0 else (150, 150, 150)
        pygame.draw.rect(gc.chess_screen, square_color, last_square, gc.HIGHLIGHT_WIDTH)
    file = chess.square_file(current_square) * gc.SQUARE_SIZE  # I need to get the file and rank to print the rectangle,
    rank = (7 - chess.square_rank(current_square)) * gc.SQUARE_SIZE  # so I undo the square formula.
    return pygame.Rect(file, rank, gc.SQUARE_SIZE, gc.SQUARE_SIZE)


def highlight_ai_square(ai_square):
    file = chess.square_file(ai_square) * gc.SQUARE_SIZE
    rank = (7 - chess.square_rank(ai_square)) * gc.SQUARE_SIZE
    return pygame.Rect(file, rank, gc.SQUARE_SIZE, gc.SQUARE_SIZE)


def update_text_box(color, difficulty):
    gc.color_text_surface = gc.FONT.render(str(color), True, gc.TEXT_COLOR)
    gc.color_text_rect = gc.color_text_surface.get_rect()
    gc.color_text_rect.center = (gc.BOARD_SIZE / 2, gc.BOARD_SIZE / 16)
    gc.difficulty_text_surface = gc.FONT.render(str(difficulty), True, gc.TEXT_COLOR)
    gc.difficulty_text_rect = gc.difficulty_text_surface.get_rect()
    gc.difficulty_text_rect.center = (gc.BOARD_SIZE / 2, gc.BOARD_SIZE / 10)
    gc.chess_screen.blit(gc.color_text_surface, gc.color_text_rect)
    gc.chess_screen.blit(gc.difficulty_text_surface, gc.difficulty_text_rect)
    pygame.display.update()


def check_if_movement_is_possible(og_square, current_square):
    origin_uci_code = get_unicode_from_square(og_square)
    destination_uci_code = get_unicode_from_square(current_square)

    possible_move = origin_uci_code + destination_uci_code

    for square in chess.SQUARES:
        if square == current_square:
            moves = list(gc.board.generate_legal_moves())
            if gc.board.piece_at(og_square).piece_type == 1:
                for move in moves:
                    if move.promotion:
                        gc.promotion = True
                        return True
            for move in moves:
                if possible_move == str(move):
                    return True
    return False


def get_unicode_from_square(square):
    file = chess.square_file(square)
    rank = chess.square_rank(square)
    return chr(ord('a') + file) + str(rank + 1)


def check_if_piece_is_correct_color(current_square):
    return gc.board.piece_at(current_square).color == gc.board.turn


def get_button_from_mouse(mouse_position):
    button_name = "None"
    gc.ai_start_button.check_click(mouse_position)
    gc.human_start_button.check_click(mouse_position)
    gc.screen_size_1_button.check_click(mouse_position)
    gc.screen_size_2_button.check_click(mouse_position)

    if gc.ai_start_button.clicked:
        gc.ai_start_button.clicked = False
        button_name = gc.ai_start_button.name
    elif gc.human_start_button.clicked:
        gc.human_start_button.clicked = False
        button_name = gc.human_start_button.name
    elif gc.screen_size_1_button.clicked:
        gc.screen_size_1_button.clicked = False
        button_name = gc.screen_size_1_button.name
    elif gc.screen_size_2_button.clicked:
        gc.screen_size_2_button.clicked = False
        button_name = gc.screen_size_2_button.name

    return button_name


def get_button_from_mouse_difficulty(mouse_position):
    gc.button_0.check_click(mouse_position)
    gc.button_1.check_click(mouse_position)
    gc.button_2.check_click(mouse_position)
    gc.button_3.check_click(mouse_position)
    gc.button_4.check_click(mouse_position)
    gc.white_button.check_click(mouse_position)
    gc.black_button.check_click(mouse_position)
    gc.button_go_back.check_click(mouse_position)
    gc.go_button.check_click(mouse_position)

    button_name = "None"

    if gc.button_0.clicked:
        gc.button_0.clicked = False
        button_name = gc.button_0.name
    elif gc.button_1.clicked:
        gc.button_1.clicked = False
        button_name = gc.button_1.name
    elif gc.button_2.clicked:
        gc.button_2.clicked = False
        button_name = gc.button_2.name
    elif gc.button_3.clicked:
        gc.button_3.clicked = False
        button_name = gc.button_3.name
    elif gc.button_4.clicked:
        gc.button_4.clicked = False
        button_name = gc.button_4.name
    elif gc.white_button.clicked:
        gc.white_button.clicked = False
        button_name = gc.white_button.name
    elif gc.black_button.clicked:
        gc.black_button.clicked = False
        button_name = gc.black_button.name
    elif gc.button_go_back.clicked:
        gc.button_go_back.clicked = False
        button_name = gc.button_go_back.name
    elif gc.go_button.clicked:
        gc.go_button.clicked = False
        button_name = gc.go_button.name

    return button_name


def initialize_menu_screen():
    gc.end = False
    gc.ai_start_button = Button("AI BUTTON", gc.BOARD_SIZE / 2, gc.BOARD_SIZE / 3, AI_START_BUTTON_IMAGE,
                                gc.BOARD_SIZE * 0.0005)
    gc.human_start_button = Button("HUMAN BUTTON", gc.BOARD_SIZE / 2, gc.BOARD_SIZE / 1.5, HUMAN_START_BUTTON_IMAGE,
                                   gc.BOARD_SIZE * 0.001)
    gc.screen_size_1_button = Button("SCREEN SIZE 1 BUTTON", gc.BOARD_SIZE / 3, gc.BOARD_SIZE / 1.2,
                                     SCREEN_SIZE_1_BUTTON_IMAGE, gc.BOARD_SIZE * 0.001)
    gc.screen_size_2_button = Button("SCREEN SIZE 2 BUTTON", gc.BOARD_SIZE / 1.5, gc.BOARD_SIZE / 1.2,
                                     SCREEN_SIZE_2_BUTTON_IMAGE, gc.BOARD_SIZE * 0.001)
    gc.chess_screen.fill((248, 248, 248))
    gc.ai_start_button.draw()
    gc.human_start_button.draw()
    gc.screen_size_1_button.draw()
    gc.screen_size_2_button.draw()
    pygame.display.flip()


def menu_management(current_event):
    if current_event.type == pygame.MOUSEBUTTONDOWN:
        mouse_position = pygame.mouse.get_pos()
        button_selected = get_button_from_mouse(mouse_position)
        if button_selected == "AI BUTTON":
            gc.current_screen = gc.DIFFICULTY
        elif button_selected == "HUMAN BUTTON":
            start_game_configuration()
            gc.current_screen = gc.HUMAN
        elif button_selected == "SCREEN SIZE 1 BUTTON":
            modify_screen(512)
        elif button_selected == "SCREEN SIZE 2 BUTTON":
            modify_screen(1024)


def modify_screen(size):
    gc.BOARD_SIZE = size
    gc.chess_screen = pygame.display.set_mode((gc.BOARD_SIZE, gc.BOARD_SIZE))
    update_text_box("Color: " + gc.print_color, "Difficulty: " + str(gc.depth))
    gc.FONT = pygame.font.Font(None, int(gc.BOARD_SIZE * 0.037))
    gc.SQUARE_SIZE = gc.BOARD_SIZE // 8
    move_window()


def move_window():
    window_title = pygame.display.get_caption()[0]
    window = gw.getWindowsWithTitle(window_title)[0]
    x, y = window.left, window.top
    window.moveTo(x, y + 300)


def difficulty_button_creation():
    gc.white_button = Button("WHITE BUTTON", gc.BOARD_SIZE / 3, gc.BOARD_SIZE / 6, WHITE_BUTTON_IMAGE,
                             gc.BOARD_SIZE * 0.0015)
    gc.black_button = Button("BLACK BUTTON", gc.BOARD_SIZE / 1.5, gc.BOARD_SIZE / 6, BLACK_BUTTON_IMAGE,
                             gc.BOARD_SIZE * 0.0015)
    gc.button_0 = Button("BUTTON 0", gc.BOARD_SIZE / 3, gc.BOARD_SIZE / 3, BUTTON_0_IMAGE, gc.BOARD_SIZE * 0.001)
    gc.button_1 = Button("BUTTON 1", gc.BOARD_SIZE / 3, gc.BOARD_SIZE / 2, BUTTON_1_IMAGE, gc.BOARD_SIZE * 0.001)
    gc.button_2 = Button("BUTTON 2", gc.BOARD_SIZE / 1.5, gc.BOARD_SIZE / 2, BUTTON_2_IMAGE, gc.BOARD_SIZE * 0.001)
    gc.button_3 = Button("BUTTON 3", gc.BOARD_SIZE / 3, gc.BOARD_SIZE / 1.5, BUTTON_3_IMAGE, gc.BOARD_SIZE * 0.001)
    gc.button_4 = Button("BUTTON 4", gc.BOARD_SIZE / 1.5, gc.BOARD_SIZE / 1.5, BUTTON_4_IMAGE, gc.BOARD_SIZE * 0.001)
    gc.button_go_back = Button("BUTTON GO BACK", gc.BOARD_SIZE / 2, gc.BOARD_SIZE / 1.3, BUTTON_GO_BACK_IMAGE,
                               gc.BOARD_SIZE * 0.001)
    gc.go_button = Button("GO BUTTON", gc.BOARD_SIZE / 2, gc.BOARD_SIZE / 1.1, GO_BUTTON_IMAGE,
                          gc.BOARD_SIZE * 0.00123)


def difficulty_button_draw():
    gc.button_0.draw()
    gc.button_1.draw()
    gc.button_2.draw()
    gc.button_3.draw()
    gc.button_4.draw()
    gc.button_go_back.draw()
    gc.white_button.draw()
    gc.black_button.draw()
    gc.go_button.draw()


def initialize_difficulty_screen():
    gc.end = False
    difficulty_button_creation()
    gc.chess_screen.fill((248, 248, 248))
    difficulty_button_draw()
    pygame.display.flip()


def difficulty_management(current_event):
    if current_event.type == pygame.MOUSEBUTTONDOWN:
        mouse_position = pygame.mouse.get_pos()
        button_selected = get_button_from_mouse_difficulty(mouse_position)

        if button_selected == "BUTTON 0":
            gc.depth = 0
            gc.random = True
            update_text_box("Color: " + gc.print_color, "Difficulty: 0 (Random AI Movements).")
        elif button_selected == "BUTTON 1":
            gc.depth = 1
            gc.random = False
            update_text_box("Color: " + gc.print_color, "Difficulty: " + str(gc.depth))
        elif button_selected == "BUTTON 2":
            gc.depth = 2
            gc.random = False
            update_text_box("Color: " + gc.print_color, "Difficulty: " + str(gc.depth))
        elif button_selected == "BUTTON 3":
            gc.depth = 3
            gc.random = False
            update_text_box("Color: " + gc.print_color, "Difficulty: " + str(gc.depth))
        elif button_selected == "BUTTON 4":
            gc.depth = 4
            gc.random = False
            update_text_box("Color: " + gc.print_color, "Difficulty: " + str(gc.depth))
        elif button_selected == "BUTTON GO BACK":
            gc.depth = 0
            gc.random = False
            gc.start_color = None
            gc.ai_start_color = None
            gc.current_screen = gc.MENU
            gc.print_color = "None"
        elif button_selected == "WHITE BUTTON":
            gc.start_color = True
            gc.ai_start_color = False
            gc.print_color = "White."
            update_text_box("Color: " + gc.print_color, "Difficulty: " + str(gc.depth))
        elif button_selected == "BLACK BUTTON":
            gc.start_color = False
            gc.ai_start_color = True
            gc.print_color = "Black."
            update_text_box("Color: " + gc.print_color, "Difficulty: " + str(gc.depth))
        elif button_selected == "GO BUTTON":
            if gc.start_color is not None and (gc.depth != 0 or gc.random):
                start_game_configuration()
                gc.current_screen = gc.GAME


def game_ended(screen):
    gc.start_color = None
    gc.depth = 0
    gc.current_screen = screen
    gc.print_color = "None"
    gc.ai_square_selected = None
    gc.square_selected = None
    gc.random = False
    gc.ai_move = None


def game_management():
    while not gc.board.is_game_over():
        for current_event in pygame.event.get():
            if current_event.type == pygame.QUIT:
                game_ended(gc.MENU)
                return

            elif current_event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                gc.square_selected = get_square_from_mouse(mouse_pos)

                if gc.count == 0:
                    if not gc.board.piece_at(gc.square_selected):
                        error_box("Pick a square with a piece please.")
                        continue
                    else:
                        if check_if_piece_is_correct_color(gc.square_selected):
                            origin_square = gc.square_selected
                            gc.count = 1
                        else:
                            error_box("Pick a piece of your color.")
                            continue
                else:
                    if check_if_movement_is_possible(origin_square, gc.square_selected):
                        check_if_movement_can_be_done(origin_square)
                    else:
                        if gc.board.piece_at(gc.square_selected):
                            if check_if_piece_is_correct_color(gc.square_selected):
                                gc.count = 1
                                origin_square = gc.square_selected
                            else:
                                message = you_are_in_check(True)
                                error_box(message)
                                continue
                        else:
                            message = you_are_in_check(False)
                            error_box(message)
                            continue

        if gc.square_selected is not None:
            empty_square_selected()

        if gc.board.is_checkmate():
            checkmate()
            return

        if gc.board.is_variant_draw():
            return

        pygame.display.flip()
        clock.tick(60)


def game_management_ai_random_moves():
    while not gc.board.is_game_over():
        for current_event in pygame.event.get():
            if current_event.type == pygame.QUIT:
                game_ended(gc.DIFFICULTY)
                return

            elif current_event.type == pygame.MOUSEBUTTONDOWN and gc.board.turn == gc.start_color:
                mouse_pos = pygame.mouse.get_pos()
                gc.square_selected = get_square_from_mouse(mouse_pos)

                if gc.count == 0:
                    if not gc.board.piece_at(gc.square_selected):
                        error_box("Pick a square with a piece please.")
                        continue
                    else:
                        if check_if_piece_is_correct_color(gc.square_selected):
                            origin_square = gc.square_selected
                            gc.count = 1
                        else:
                            error_box("Pick a piece of your color.")
                            continue
                else:
                    if check_if_movement_is_possible(origin_square, gc.square_selected):
                        check_if_movement_can_be_done(origin_square)
                    else:
                        if gc.board.piece_at(gc.square_selected):
                            if check_if_piece_is_correct_color(gc.square_selected):
                                gc.count = 1
                                origin_square = gc.square_selected
                            else:
                                message = you_are_in_check(True)
                                error_box(message)
                                continue
                        else:
                            message = you_are_in_check(False)
                            error_box(message)
                            continue
            elif gc.board.turn == gc.ai_start_color and (not gc.board.is_checkmate() or not gc.board.is_stalemate()):
                if gc.random:
                    gc.ai_move = return_random_movement()
                else:
                    gc.ai_move = return_ai_move(gc.board, gc.depth)
                ai_movement_finished(gc.ai_move)

        if gc.square_selected is not None:
            empty_square_selected()

        if gc.ai_square_selected is not None:
            gc.ai_square_selected = highlight_ai_square(gc.ai_move.to_square)
            pygame.draw.rect(gc.chess_screen, gc.HIGHLIGHT_COLOR_AI, gc.ai_square_selected, gc.HIGHLIGHT_WIDTH)

        if gc.board.is_checkmate():
            checkmate()
            return

        if gc.board.is_stalemate():
            stalemate()
            return

        pygame.display.flip()
        clock.tick(60)


def error_box(message):
    messagebox.showerror("Error!", message, icon="error")
    gc.square_selected = None
    clock.tick(1000)


def checkmate():
    pygame.display.flip()
    messagebox.showinfo("Victory!", "Checkmate! Color: " + gc.color + " has won!", icon="info")
    screen = gc.DIFFICULTY if gc.current_screen == gc.GAME else gc.MENU
    game_ended(screen)


def stalemate():
    pygame.display.flip()
    if gc.color == "WHITE":
        gc.color = "BLACK"
    else:
        gc.color = "WHITE"
    messagebox.showinfo("Draw!", "Stalemate. Color: " + gc.color + " can't do any movement.", icon="info")
    screen = gc.DIFFICULTY if gc.current_screen == gc.GAME else gc.MENU
    game_ended(screen)


def empty_square_selected():
    gc.last_square_selected = highlight_selected_square(gc.square_selected, gc.last_square_selected)
    pygame.draw.rect(gc.chess_screen, gc.HIGHLIGHT_COLOR, gc.last_square_selected, gc.HIGHLIGHT_WIDTH)


def check_if_movement_can_be_done(origin_square):
    gc.color = "WHITE" if gc.board.turn == chess.WHITE else "BLACK"
    if gc.promotion:
        origin_uci_code = get_unicode_from_square(origin_square)
        destination_uci_code = get_unicode_from_square(gc.square_selected)
        if origin_uci_code == destination_uci_code:
            error_box("Choose a different square")
            gc.square_selected = None
            return
        possible_move = origin_uci_code + destination_uci_code
        if gc.board.is_legal(chess.Move.from_uci(possible_move + "q")):
            move = chess.Move.from_uci(possible_move + "q")
        else:
            error_box("You can't do this move, choose a new one")
            gc.square_selected = None
            return
    else:
        move = chess.Move(origin_square, gc.square_selected)
    do_movement(move)


def do_movement(move):
    gc.color = "WHITE" if gc.board.turn == chess.WHITE else "BLACK"
    gc.board.push(move)
    draw_board(gc.chess_screen, gc.board)
    gc.count = 0
    gc.promotion = False


def you_are_in_check(there_is_piece):
    if not gc.board.is_check() and there_is_piece:
        message = "Pick a piece of your color or choose the square you want to move on."
    elif not gc.board.is_check() and not there_is_piece:
        message = "Move cannot be done. Choose a new one."
    else:
        message = "Move cannot be done. You are being check. Choose a new one."
    return message


def ai_movement_finished(move):
    gc.color = "WHITE" if gc.board.turn == chess.WHITE else "BLACK"
    gc.ai_square_selected = move.to_square
    gc.board.push(move)
    draw_board(gc.chess_screen, gc.board)
    gc.count = 0


def return_random_movement():
    moves = list(gc.board.legal_moves)
    if len(moves) == 0:
        moves = list(gc.board.pseudo_legal_moves)
    move = random.choice(moves)
    return move


def return_ai_move(board, depth):
    best_eval = float('-inf')
    best_move = None

    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, float('-inf'), float('inf'), False)
        board.pop()
        if eval > best_eval:
            best_eval = eval
            best_move = move
    return best_move


def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluation_function(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def evaluation_function(board):
    score = 0
    ai_pieces = 0
    human_pieces = 0

    # Evaluation of the pieces from each player.
    score, ai_pieces, human_pieces = pieces_evaluation(score, board, ai_pieces, human_pieces)

    # Evaluation of the mobility of the pieces.
    score = pieces_mobility(score, board)

    # Check the position of the king.
    score = king_position(score, board)

    # Check the center control
    score = center_control(score, board)

    # Check the position of the pieces with the score tables
    score = score_tables(score, board, ai_pieces, human_pieces)

    return score


def pieces_evaluation(score, board, ai_pieces, human_pieces):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            piece_value = gc.piece_values[piece.piece_type]
            if piece.color == gc.ai_start_color:
                score += piece_value  # Add to the score if the piece is the same color as the ones AI controls.
                ai_pieces += 1
            else:
                score -= piece_value  # Subtract to the score if the piece is from the other color.
                human_pieces += 1

    return score, ai_pieces, human_pieces


def pieces_mobility(score, board):
    mobility = len(list(board.legal_moves))
    score += mobility * 0.5

    return score


def king_position(score, board):
    king_square = board.king(gc.ai_start_color)
    if king_square:
        # If the king is in check, subtract from the score
        if board.is_check():
            score -= 100
        # If the king is in a safe position (just checking if it's castled), add to the score
        if not gc.ai_start_color:  # Checks if the AI is playing black or white
            if king_square == chess.G8 or king_square == chess.C8:
                score += 50
        else:
            if king_square == chess.G1 or king_square == chess.C1:
                score += 50

    return score


def center_control(score, board):
    center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
    for square in center_squares:
        if not gc.ai_start_color:  # Checks if the AI is playing black or white
            if board.is_attacked_by(chess.BLACK, square):
                score += 100
            elif board.is_attacked_by(chess.WHITE, square):
                score -= 100
        else:
            if board.is_attacked_by(chess.WHITE, square):
                score += 100
            elif board.is_attacked_by(chess.BLACK, square):
                score -= 100

    return score


def score_tables(score, board, ai_pieces, human_pieces):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            row = square // 8
            column = square % 8
            if human_pieces >= 7 or ai_pieces >= 7:  # Here I check if it's endgame (I consider that less than 7
                # pieces from either player is endgame).
                score = king_attack(score, board)
                score = end_game_evaluation(score, piece, row, column)
            else:
                score = early_game_evaluation(score, piece, row, column)

    return score


def king_attack(score, board):
    king_square_human = board.king(not gc.ai_start_color)
    if king_square_human:
        # Here I check if the AI can attack the king, if so, add 10000 points
        if not gc.ai_start_color:  # Need to check AI color, so I can check which color is attacking
            if board.is_attacked_by(chess.BLACK, king_square_human):
                score += 1000
        else:
            if board.is_attacked_by(chess.WHITE, king_square_human):
                score += 1000

    return score


def early_game_evaluation(score, piece, row, column):  # Check position with the evaluation tables (early game)
    if piece.color == gc.ai_start_color:
        if piece.piece_type == chess.PAWN:
            if not gc.ai_start_color:
                score += gc.pawn_scores_black[row][column]
            else:
                score += gc.pawn_scores_white[row][column]
        elif piece.piece_type == chess.KNIGHT:
            if not gc.ai_start_color:
                score += gc.knight_scores_black[row][column]
            else:
                score += gc.knight_scores_white[row][column]
        elif piece.piece_type == chess.BISHOP:
            if not gc.ai_start_color:
                score += gc.bishop_scores_black[row][column]
            else:
                score += gc.bishop_scores_white[row][column]
        elif piece.piece_type == chess.ROOK:
            if not gc.ai_start_color:
                score += gc.rook_scores_black[row][column]
            else:
                score += gc.rook_scores_white[row][column]
        elif piece.piece_type == chess.QUEEN:
            if not gc.ai_start_color:
                score += gc.queen_scores_black[row][column]
            else:
                score += gc.queen_scores_white[row][column]
        elif piece.piece_type == chess.KING:
            if not gc.ai_start_color:
                score += gc.king_scores_black[row][column]
            else:
                score += gc.king_scores_white[row][column]

    return score


def end_game_evaluation(score, piece, row, column):  # Check position with the evaluation tables (endgame)
    if piece.color == gc.ai_start_color:
        if piece.piece_type == chess.PAWN:
            if not gc.ai_start_color:
                score += gc.pawn_scores_black_end_game[row][column]
            else:
                score += gc.pawn_scores_white_end_game[row][column]
        elif piece.piece_type == chess.KNIGHT:
            if not gc.ai_start_color:
                score += gc.knight_scores_black_end_game[row][column]
            else:
                score += gc.knight_scores_white_end_game[row][column]
        elif piece.piece_type == chess.BISHOP:
            if not gc.ai_start_color:
                score += gc.bishop_scores_black_end_game[row][column]
            else:
                score += gc.bishop_scores_white_end_game[row][column]
        elif piece.piece_type == chess.ROOK:
            if not gc.ai_start_color:
                score += gc.rook_scores_black_end_game[row][column]
            else:
                score += gc.rook_scores_white_end_game[row][column]
        elif piece.piece_type == chess.QUEEN:
            if not gc.ai_start_color:
                score += gc.queen_scores_black_end_game[row][column]
            else:
                score += gc.queen_scores_white_end_game[row][column]
        elif piece.piece_type == chess.KING:
            if not gc.ai_start_color:
                score += gc.king_scores_black_end_game[row][column]
            else:
                score += gc.king_scores_white_end_game[row][column]

    return score


def get_last_rank_squares(color):
    square_list = []
    if color == chess.WHITE:
        for square in chess.SQUARES:
            if chess.square_rank(square) == 7:
                square_list.append(square)
    else:
        for square in chess.SQUARES:
            if chess.square_rank(square) == 0:
                square_list.append(square)
    return square_list


if __name__ == '__main__':
    # Start Pygame instance and tkinter
    initialize_pygame_tkinter()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if gc.current_screen == gc.MENU:
                initialize_menu_screen()
                menu_management(event)

            elif gc.current_screen == gc.HUMAN:
                gc.white_last_rank_squares = get_last_rank_squares(chess.WHITE)
                gc.black_last_rank_squares = get_last_rank_squares(chess.BLACK)
                game_management()

            elif gc.current_screen == gc.DIFFICULTY:
                gc.count = 0
                initialize_difficulty_screen()
                if gc.random:
                    update_text_box("Color: " + gc.print_color, "Difficulty: 0 (Random AI Movements).")
                else:
                    update_text_box("Color: " + gc.print_color, "Difficulty: " + str(gc.depth))
                difficulty_management(event)

            elif gc.current_screen == gc.GAME:
                gc.white_last_rank_squares = get_last_rank_squares(chess.WHITE)
                gc.black_last_rank_squares = get_last_rank_squares(chess.BLACK)
                game_management_ai_random_moves()
