import install_requirements
import pygame
import sys
import random
import json
from spellchecker import SpellChecker


pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('The-Wordle-Theme-Song.mp3')
pygame.mixer.music.play(-1)

screen_width = 1000
screen_height = 800

screen = pygame.display.set_mode((screen_width,  screen_height))
pygame.display.set_caption('WORDLE')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (169, 169, 169)
RED = (255, 0, 0)  
HIGHLIGHT_COLOR = (100, 100, 255) 

with open('config.json') as file:
    data_dict = json.load(file)

word_list = data_dict['words_list']

def select_random_word(length:int = 5, random_mode:bool = False):
    if random_mode:
        return random.choice(word_list).upper()
    else:
        specific_words = [i for i in word_list if len(i) == length]
        return random.choice(specific_words).upper()


spell = list(SpellChecker())
font = pygame.font.Font(None, 60)
popup_font = pygame.font.Font(None, 30)
menu_font = pygame.font.Font(None, 35)
box_size = 70
padding = 10
random_mode = True
selected_word = select_random_word(random_mode=random_mode)
print(selected_word)
max_word_length = len(selected_word)  
max_guesses = 6  
guesses = [[] for _ in range(max_guesses)] 
current_guess_row = 0 
popup_message = ""
show_popup = False  
popup_timer = 0 
option_screen_rect = pygame.Rect(300, 200, 400, 210)
menu_button_rect = pygame.Rect(screen_width -130, 10, 90, 40)
min_length = 5
max_length = 10
current_length = min_length
current_game_mode = "Random Mode"
current_level = data_dict["game_level"]

popup_width = 600
popup_height = 200
popup_rect = pygame.Rect((screen_width // 2 - popup_width // 2, screen_height // 2 - popup_height // 2, popup_width, popup_height))



entry_boxes = [
        [pygame.Rect(
            (screen_width // 2) - ((max_word_length * (box_size + padding) - padding) // 2) + i * (box_size + padding), 
            100 + j * (box_size + padding), box_size, box_size
        ) for i in range(max_word_length)] for j in range(max_guesses)
    ]

option_rects = [
    pygame.Rect(option_screen_rect.x + 20, option_screen_rect.y + 20, 160, 40),
    pygame.Rect(option_screen_rect.x + 20, option_screen_rect.y + 60, 160, 40),
    pygame.Rect(option_screen_rect.x + 20, option_screen_rect.y + 100, 160, 40)
]


def check_guess(guess, target):
    feedback = []
    for i in range(len(guess)):
        if guess[i] == target[i]:
            feedback.append(GREEN)  
        elif guess[i] in target:
            feedback.append(YELLOW)  
        else:
            feedback.append(GRAY)  
    return feedback


def is_valid_word(word):
    if not word.isalpha():
        return False
    return word.lower() in spell


def show_popup_message(message):
    global popup_message, show_popup, popup_timer
    popup_message = message
    show_popup = True
    popup_timer = pygame.time.get_ticks()  


def reset_game():
    global selected_word, guesses, current_guess_row, show_popup, guess_correct, current_length, random_mode, max_word_length, entry_boxes
    selected_word = select_random_word(random_mode=random_mode, length=current_length) 
    print(selected_word)
    max_word_length = len(selected_word) 
    guesses = [[] for _ in range(max_guesses)]  
    current_guess_row = 0  
    show_popup = False  
    guess_correct = False  
    entry_boxes = [
        [pygame.Rect(
            (screen_width // 2) - ((max_word_length * (box_size + padding) - padding) // 2) + i * (box_size + padding), 
            100 + j * (box_size + padding), box_size, box_size
        ) for i in range(max_word_length)] for j in range(max_guesses)
    ]


def draw_persistent_menu():
    pygame.draw.rect(screen, BLACK, menu_button_rect)
    menu_text = menu_font.render("Menu".upper(), True, WHITE)
    screen.blit(menu_text, (menu_button_rect.x + 20, menu_button_rect.y + 10))


def handle_menu_click(mouse_pos):
    if menu_button_rect.collidepoint(mouse_pos):
        return True  
    return False


def handle_option_click(mouse_pos, selected_option, adjust_length=False):
    global current_length, current_game_mode
    if selected_option == 2:  
     
        left_arrow_rect, right_arrow_rect = show_option_screen(selected_option)
        if left_arrow_rect.collidepoint(mouse_pos):
            if current_length > min_length:
                current_length -= 1
        elif right_arrow_rect.collidepoint(mouse_pos):
            if current_length < max_length:
                current_length += 1

        current_game_mode = f"{current_length}-letter words"

    else:
        if selected_option == 0:
            current_game_mode = "Random Mode"
        elif selected_option == 1:
            current_game_mode =f"Level {current_level}"


def show_option_screen(selected_option):
    pygame.draw.rect(screen, BLACK, option_screen_rect)
    pygame.draw.rect(screen, GRAY, option_screen_rect, 3)  

    
    options = ["Random Mode", "Play Levels", "Specific Length"]

    for i, option_rect in enumerate(option_rects):
        text_color = WHITE
        if i == selected_option:
            text_color = HIGHLIGHT_COLOR
        
        option_text = menu_font.render(options[i].upper(), True, text_color)
        screen.blit(option_text, (option_rect.x + 20, option_rect.y + 10))

    if selected_option == 2:
        length_text = menu_font.render(f"Length: {current_length}".upper(), True, WHITE)
        screen.blit(length_text, (option_screen_rect.x + 120, option_screen_rect.y + 140))

        left_arrow_rect = pygame.Rect(option_screen_rect.x + 120, option_screen_rect.y + 160, 40, 40)
        right_arrow_rect = pygame.Rect(option_screen_rect.x + 220, option_screen_rect.y + 160, 40, 40)

        pygame.draw.rect(screen, BLACK, left_arrow_rect)
        pygame.draw.rect(screen, BLACK, right_arrow_rect)
        
        left_arrow_text = menu_font.render("<|", True, WHITE)
        right_arrow_text = menu_font.render("|>", True, WHITE)
        
        screen.blit(left_arrow_text, (left_arrow_rect.x + 12, left_arrow_rect.y + 5))
        screen.blit(right_arrow_text, (right_arrow_rect.x + 12, right_arrow_rect.y + 5))

        return left_arrow_rect, right_arrow_rect  

    return None, None 

def display_current_game_mode(current_game_mode):
    mode_text = menu_font.render(f"{current_game_mode}".upper(), True, WHITE)
    screen.blit(mode_text, (20, 20))


clock = pygame.time.Clock()
guess_correct = False
menu_open = False
selected_option = 0
last_selected_option = selected_option

while True:
    screen.fill(BLACK)
    
    draw_persistent_menu()
    display_current_game_mode(current_game_mode)
    
    for j in range(max_guesses): 
        for i in range(max_word_length):  
            pygame.draw.rect(screen, WHITE, entry_boxes[j][i], 2)  
            if i < len(guesses[j]):  
                txt_surface = font.render(guesses[j][i], True, WHITE)
                screen.blit(txt_surface, (entry_boxes[j][i].x + (box_size - txt_surface.get_width()) / 2, 
                                        entry_boxes[j][i].y + (box_size - txt_surface.get_height()) / 2))


    for j in range(current_guess_row):  
        feedback = check_guess(guesses[j], selected_word)

        for i in range(max_word_length):
            pygame.draw.rect(screen, feedback[i], entry_boxes[j][i])
            txt_surface = font.render(guesses[j][i], True, WHITE)
            screen.blit(txt_surface, (entry_boxes[j][i].x + (box_size - txt_surface.get_width()) / 2, 
                                      entry_boxes[j][i].y + (box_size - txt_surface.get_height()) / 2))
    
    if menu_open:
            left_arrow_rect, right_arrow_rect = show_option_screen(selected_option)
    
    if show_popup:
    
        pygame.draw.rect(screen, GRAY, popup_rect)  
        
        txt_surface = popup_font.render(popup_message, True, WHITE)
        screen.blit(txt_surface, (popup_rect.x + (popup_width - txt_surface.get_width()) / 2, 
                                popup_rect.y + (popup_height - txt_surface.get_height()) / 2))

     
        if pygame.time.get_ticks() - popup_timer > 2000:  
            show_popup = False  


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif guess_correct or current_guess_row == max_guesses:
            if guess_correct and current_game_mode == f"Level {current_level}":
                print(current_level)
                current_level += 1
                current_length = current_level + 4
                data_dict["game_level"] = current_level
                with open('config.json', 'w') as file:
                    json.dump(data_dict, file)

            pygame.time.wait(4000)
            reset_game()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if handle_menu_click(mouse_pos): 
                    menu_open = not menu_open 
                elif menu_open:
                    handle_option_click(mouse_pos, selected_option)  

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN: 
                    if menu_open:
                        selected_option = (selected_option + 1) % 3
            elif event.key == pygame.K_UP: 
                if menu_open:
                    selected_option = (selected_option - 1) % 3
            elif event.key == pygame.K_BACKSPACE and guesses[current_guess_row]:
                guesses[current_guess_row].pop() 
            
            elif event.key == pygame.K_RETURN:
                if menu_open:
                        if selected_option == 2:
                            random_mode = False
                            reset_game()
                        elif selected_option == 0:
                            random_mode = True
                            reset_game()
                        elif selected_option == 1:
                            random_mode = False
                            current_length = current_level + 4
                            reset_game()
                        
                        else:
                            handle_option_click(pygame.mouse.get_pos(), selected_option) 

                if len(guesses[current_guess_row]) == max_word_length:  
                    guess = "".join(guesses[current_guess_row])
                    
                    if is_valid_word(guess): 
                        feedback = check_guess(guesses[current_guess_row], selected_word)
                        print(f'Guess: {guesses[current_guess_row]}, Feedback: {feedback}')
                        
                        if guess == selected_word:
                            guess_correct = True
                        current_guess_row += 1 
                    else:
                        show_popup_message(f"Invalid word: {guess}. Only real words are allowed!")
            elif len(guesses[current_guess_row]) < max_word_length and event.unicode.isalpha():
                guesses[current_guess_row].append(event.unicode.upper())  

        if guess_correct:
            show_popup_message("YOU GOT THE WORD!!")
        elif current_guess_row == max_guesses:
            show_popup_message(f'THE WORD WAS {selected_word}')

    pygame.display.flip()
    clock.tick(30)