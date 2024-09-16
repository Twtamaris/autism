import pygame
from pygame import mixer

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
dark_gray = (50, 50, 50)
light_gray = (170, 170, 170)
blue = (0, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
gold = (212, 175, 55)
WIDTH = 1400
HEIGHT = 800
active_length = 0
active_beat = 0
list_pic = []
rows = 4
columns = 13
# list_messages = []

car_img6 = pygame.image.load('phutu/1.jpg')
for i in range(1, 58):
    car_img = pygame.image.load('phutu/'+str(i)+'.jpg')
    list_pic.append(car_img)

list_messages = ['I ', 'TO ', 'WE ', 'THEY ', 'HE ', 'SHE ', 'IT ', 'ME ', 'am ', 'WANT ', 'EAT ', 'GO ', 'LOVE ', 'FELL ', 'IS ', 'KNOW ', 'NEED ', 'USE ', 'THIS ', 'HELP ', 'you ', 'WEAR ', 'THAT ', 'THE ', 'SOME ', 'MORE ', 'A ', 'THESE ',
                 'GOOD ', 'ICE_CREAM ', 'HUNGRY ', 'CAKE ', 'BAD ', 'FOOD ', 'DOWN ', 'OUT ', 'HERE ', 'THERE ', 'DONE ', 'THOSE ', 'STOP ', 'YES ', 'HELLO ', 'THANK_YOU ', 'NO ', 'BECAUSE ', 'WHAT ', 'WHO ', 'WHEN ', 'WHERE ', 'PLEASE ', 'WITH ', '', '', '', '', '', '']

green_is_on = 0
#
# Dictionary with sound categories
sound_dict = {
    1: ['i', 'to', 'we', 'they'],
    2: ['he', 'she', 'it', 'me'],
    3: ['am', 'want', 'eat', 'go'],
    4: ['love', 'fell', 'is', 'know'],
    5: ['need', 'use', 'this', 'help'],
    6: ['you', 'wear', 'that', 'the'],
    7: ['some', 'more', 'a', 'these'],
    8: ['good', 'ice_cream', 'hungry', 'birthday'],
    9: ['bad', 'food', 'down', 'out'],
    10: ['here', 'there', 'done', 'those'],
    11: ['stop', 'yes', 'hello', 'thank_you'],
    12: ['no', 'because', 'what', 'who'],
    13: ['when', 'where', 'please', 'with']
}

# Create the list of sound variables programmatically
list_sound_variable = []

for key, sound_list in sound_dict.items():
    sound_group = [mixer.Sound(f'sound/{sound}.mp3') for sound in sound_list]
    list_sound_variable.append(sound_group)

# Now you have list_sound_variable populated




screen = pygame.display.set_mode([WIDTH, HEIGHT])

pygame.display.set_caption('The Beat Maker')
label_font = pygame.font.Font('Roboto-Bold.ttf', 32)
medium_font = pygame.font.Font('Roboto-Bold.ttf', 24)
beat_changed = True
timer = pygame.time.Clock()
fps = 60
beats = 13
bpm = 240
instruments = 6
playing = True
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
active_list = [1 for _ in range(instruments)]
pygame.mixer.set_num_channels(instruments * 3)
save_menu = False
load_menu = False
saved_beats = []
file = open('saved_beats.txt', 'r')
for line in file:
    saved_beats.append(line)
beat_name = ''
saved_text = []


typing = False
index = 100
list_rect = []
on_of_list = []
new_messages_list = []


def draw_grid(clicks, beat, actives):
    boxes = []
    for i in range(instruments + 1):
        pygame.draw.line(screen, gray, (0, i * 100), (200, i * 100), 3)
    
    k = 0
    for i in range(beats):
        for j in range(2, instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                if actives[j] == 1:
                    color = green
                else:
                    color = dark_gray

            # Calculate the rectangle's dimensions
            rect_width = (WIDTH - 200) // beats
            rect_height = 100  # Fixed height of each row

            # Draw the grid rectangle
            rect = pygame.draw.rect(screen, color,
                                    [i * rect_width + 205, (j * 100) + 5, rect_width - 10, 90], 0, 3)
            list_rect.append(rect)

            # Outline the rectangles
            pygame.draw.rect(screen, gold, [i * rect_width + 200, j * 100, rect_width, rect_height], 5, 5)
            pygame.draw.rect(screen, black, [i * rect_width + 200, j * 100, rect_width, rect_height], 2, 5)

            # Only blit the picture if k is within bounds of list_pic
            if k < len(list_pic):
                # Dynamically resize the image to fit within the grid cell
                image = pygame.transform.scale(list_pic[k], (rect_width - 20, rect_height - 20))  # Adjust image size
                screen.blit(image, (211 + i * rect_width, (j * 100) + 10))  # Blit the scaled image onto the screen
                k += 1  # Move to the next picture for blitting

            boxes.append((rect, (i, j)))


    pygame.draw.rect(screen, blue,
                            [beat * ((WIDTH - 200) // beats) + 200, 0,
                            ((WIDTH - 200) // beats), instruments * 100],
                            1, 3)



    pygame.draw.rect(screen, black, [0, 0, 1400, 200])
    saurab = pygame.draw.rect(screen, (245,229,229), [110, 90, 1200, 70], 0, 5)
    
    pygame.draw.rect(screen, (248,155,248), [110, 90, 1200, 70], 3, 5)


    return boxes, saurab


def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_list[i] == 1:
            for j in range(13):
                for k in range(4):
                    if i == (k+2) and active_beat == j:
                        list_sound_variable[j][k].play()

# NOTE: This code needs little correction as when the rectangle increases this crashes
# def play_notes():
#     for j in range(13):
#         for i in range(4):
#             if clicked[i+2][j] == 1 and active_list[i+2]== 1 and active_beat == j:
#                 list_sound_variable[j][i].play()


def draw_save_menu(beat_name, typing):
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    menu_text = label_font.render(
        'SAVE MENU: Enter a Name for this Sound', True, white)
    screen.blit(menu_text, (400, 40))
    exit_btn = pygame.draw.rect(
        screen, gray, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = label_font.render('Close', True, white)
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 90))
    saving_btn = pygame.draw.rect(
        screen, gray, [WIDTH // 2 - 100, HEIGHT * 0.75, 200, 100], 0, 5)
    saving_text = label_font.render('Save Sound', True, white)
    screen.blit(saving_text, (WIDTH // 2 - 80, HEIGHT * 0.75 + 30))
    if typing:
        pygame.draw.rect(screen, dark_gray, [400, 200, 600, 200], 0, 5)
    entry_rect = pygame.draw.rect(screen, gray, [400, 200, 600, 200], 5, 5)
    entry_text = label_font.render(f'{beat_name}', True, white)
    screen.blit(entry_text, (430, 250))
    return exit_btn, saving_btn, beat_name, entry_rect


def draw_load_menu(index):
    loaded_clicked = []
    loaded_beats = 0
    loaded_bpm = 0
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    menu_text = label_font.render(
        'LOAD MENU: Select a Sound to load in', True, white)
    screen.blit(menu_text, (400, 40))
    exit_btn = pygame.draw.rect(
        screen, gray, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = label_font.render('Close', True, white)
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 90))
    loading_btn = pygame.draw.rect(
        screen, gray, [WIDTH // 2 - 100, HEIGHT * 0.87, 200, 100], 0, 5)
    loading_text = label_font.render('Load Sound', True, white)
    screen.blit(loading_text, (WIDTH // 2 - 70, HEIGHT * 0.87 + 10))
    delete_btn = pygame.draw.rect(
        screen, gray, [WIDTH // 2 - 400, HEIGHT * 0.87, 200, 100], 0, 5)
    delete_text = label_font.render('Delete', True, white)
    screen.blit(delete_text, (WIDTH // 2 - 385, HEIGHT * 0.87 + 10))
    if 0 <= index < len(saved_beats):
        pygame.draw.rect(screen, light_gray, [190, 100 + index*50, 1000, 50])
    for beat in range(len(saved_beats)):
        if beat < 10:
            beat_clicked = []
            row_text = medium_font.render(f'{beat + 1}', True, white)
            screen.blit(row_text, (200, 100 + beat * 50))
            name_index_start = saved_beats[beat].index('name: ') + 6
            name_index_end = saved_beats[beat].index(', beats:')
            name_text = medium_font.render(
                saved_beats[beat][name_index_start:name_index_end], True, white)
            screen.blit(name_text, (240, 100 + beat * 50))
        if 0 <= index < len(saved_beats) and beat == index:
            beats_index_end = saved_beats[beat].index(', bpm:')
            loaded_beats = int(
                saved_beats[beat][name_index_end + 8:beats_index_end])
            bpm_index_end = saved_beats[beat].index(', selected:')
            loaded_bpm = int(saved_beats[beat]
                             [beats_index_end + 6:bpm_index_end])
            loaded_clicks_string = saved_beats[beat][bpm_index_end + 14: -3]
            loaded_clicks_rows = list(loaded_clicks_string.split("], ["))
            for row in range(len(loaded_clicks_rows)):
                loaded_clicks_row = (loaded_clicks_rows[row].split(', '))
                for item in range(len(loaded_clicks_row)):
                    if loaded_clicks_row[item] == '1' or loaded_clicks_row[item] == '-1':
                        loaded_clicks_row[item] = int(loaded_clicks_row[item])
                beat_clicked.append(loaded_clicks_row)
                loaded_clicked = beat_clicked
    loaded_info = [loaded_beats, loaded_bpm, loaded_clicked]
    entry_rect = pygame.draw.rect(screen, gray, [190, 90, 1000, 600], 5, 5)

    return exit_btn, loading_btn, entry_rect, delete_btn, loaded_info


typing_variable = 100
run = True

# class Button():
#     # def __init__(self):

        
        
#     def play_pause_button():
#         play_pause = pygame.draw.rect(
#         screen, (255, 102, 255), [50, HEIGHT - 150, 200, 100], 0, 5)
#         play_text = label_font.render('Play/Pause', True, white)
#         screen.blit(play_text, (70, HEIGHT - 130))
#         if playing:
#             play_text2 = medium_font.render('Playing', True, dark_gray)
#         else:
#             pygame.draw.rect(screen, (102, 0, 204), [
#                             50, HEIGHT - 150, 200, 100], 0, 5)
#             play_text = label_font.render('Play/Pause', True, white)
#             screen.blit(play_text, (70, HEIGHT - 130))

#             play_text2 = medium_font.render('Paused', True, dark_gray)
#         screen.blit(play_text2, (70, HEIGHT - 100))

#         return play_pause, play_text




while run:

    timer.tick(fps)
    screen.fill(black)

    boxes, saurab = draw_grid(clicked, active_beat, active_list)

    play_pause = pygame.draw.rect(
        screen, (255, 102, 255), [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = label_font.render('Play/Pause', True, white)
    screen.blit(play_text, (70, HEIGHT - 130))
    if playing:
        play_text2 = medium_font.render('Playing', True, dark_gray)
    else:
        pygame.draw.rect(screen, (102, 0, 204), [
                         50, HEIGHT - 150, 200, 100], 0, 5)
        play_text = label_font.render('Play/Pause', True, white)
        screen.blit(play_text, (70, HEIGHT - 130))

        play_text2 = medium_font.render('Paused', True, dark_gray)
    screen.blit(play_text2, (70, HEIGHT - 100))
    # beats per minute buttons
    bpm_rect = pygame.draw.rect(
        screen, (0, 255, 255), [300, HEIGHT - 150, 200, 100], 5, 5)

    pygame.draw.rect(screen, (0, 255, 255), [
                     300, HEIGHT - 150, 200, 100/2], 5, 5)
    # pygame.draw.rect(screen, gray, [300, HEIGHT - 150+50, 200, 100/2], 5, 5)

    bpm_text = medium_font.render('INC SPEED', True, white)
    screen.blit(bpm_text, (320, HEIGHT - 140))
    # bpm_text2 = label_font.render(f'{bpm}', True, white)
    bpm_text2 = medium_font.render('DEC SPEED', True, white)
    screen.blit(bpm_text2, (320, HEIGHT - 90))

    bpm_add_rect = pygame.draw.rect(
        screen, (102, 255, 102), [510, HEIGHT - 150, 48, 48], 0, 5)
    bpm_sub_rect = pygame.draw.rect(
        screen, (204, 0, 0), [510, HEIGHT - 100, 48, 48], 0, 5)

    add_text = medium_font.render('+', True, white)
    screen.blit(add_text, (527, HEIGHT - 140))
    sub_text = medium_font.render('-', True, white)
    screen.blit(sub_text, (530, HEIGHT - 90))

    # beats per loop buttons
    beats_rect = pygame.draw.rect(
        screen, gold, [600, HEIGHT - 150, 200, 100], 3, 5)
    beats_text = medium_font.render('How to Play?', True, white)
    screen.blit(beats_text, (622, HEIGHT - 117))
    beats_text2 = label_font.render(f'{beats}', True, white)
    # screen.blit(beats_text2, (670, HEIGHT - 100))
    beats_add_rect = pygame.draw.rect(
        screen, gray, [810, HEIGHT - 150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(
        screen, gray, [810, HEIGHT - 100, 48, 48], 0, 5)
    
    pygame.draw.rect(
        screen, (249, 226, 226), [810, HEIGHT - 150, 48, 48], 2, 5)
    pygame.draw.rect(
        screen, (249, 226, 226), [810, HEIGHT - 100, 48, 48], 2, 5)
    # beats_add_rect = pygame.draw.rect(
    #     screen, gold, [810, HEIGHT - 150, 48, 48], 3, 5)
    # beats_sub_rect = pygame.draw.rect(
    #     screen, gold, [810, HEIGHT - 100, 48, 48], 3, 5)
    add_text2 = medium_font.render('W', True, white)
    
    screen.blit(add_text2, (820, HEIGHT - 140))
    sub_text2 = medium_font.render('L', True, white)
    screen.blit(sub_text2, (820, HEIGHT - 90))
    
    # clear board button
    if green_is_on == 1:
        clear = pygame.draw.rect(screen, (102, 0, 204), [
                                 1150, HEIGHT - 150, 200, 100], 0, 5)

    else:
        clear = pygame.draw.rect(screen, (255, 102, 255), [
                                 1150, HEIGHT - 150, 200, 100], 0, 5)
    play_text = label_font.render('Clear Board', True, white)
    screen.blit(play_text, (1160, HEIGHT - 130))

    # save and load buttons
    save_button = pygame.draw.rect(
        screen, gray, [900, HEIGHT - 150, 200, 48], 0, 5)
    pygame.draw.rect(screen, (0, 255, 255), [900, HEIGHT - 150, 200, 48], 3, 5)
    save_text = label_font.render('Save Sound', True, white)
    screen.blit(save_text, (920, HEIGHT - 140))
    load_button = pygame.draw.rect(
        screen, gray, [900, HEIGHT - 98, 200, 48], 0, 5)
    load_text = label_font.render('Load Sound', True, white)
    pygame.draw.rect(screen, (0, 255, 255), [900, HEIGHT - 98, 200, 48], 3, 5)
    screen.blit(load_text, (920, HEIGHT - 90))
    # instrument rectangles
    if green_is_on == 0:
        pygame.draw.rect(screen, black, [0, 0, 1400, 200])
        pygame.draw.rect(screen, gray, [110, 90, 1200, 70], 0, 5)
        text_ = label_font.render('Press Key to Start...', True, (207, 201, 201))
        pygame.draw.rect(screen, white, [110, 90, 1200, 70], 2, 5)
        
        screen.blit(text_, (140, 110))
        # pygame.draw.rect(screen, gray, [550, 75, 300, 70], 0, 5)
        new_messages_list = []
    instrument_rects = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0, i * 100), (200, 100))
        instrument_rects.append(rect)
    if beat_changed:
        play_notes()
        beat_changed = False
    if save_menu:
        exit_button, saving_button, beat_name, entry_rect = draw_save_menu(
            beat_name, typing)
    elif load_menu:
        exit_button, loading_button, entry_rect, delete_button, loaded_information = draw_load_menu(
            index)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:
            for i in range(58):
                if list_rect[i].collidepoint(event.pos):
                    typing_variable = i
                    on_of_list.append(i)
                    new_messages_list.append(list_messages[i])
                    green_is_on = 1

            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
            

        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
            if play_pause.collidepoint(event.pos) and playing:
                playing = False
            elif play_pause.collidepoint(event.pos) and not playing:
                playing = True
                active_beat = 0
                active_length = 0
            if clear.collidepoint(event.pos):
                green_is_on = 0

            if beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
            if bpm_add_rect.collidepoint(event.pos):
                bpm += 5
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 5
            if clear.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)]
                           for _ in range(instruments)]
            for i in range(len(instrument_rects)):
                if instrument_rects[i].collidepoint(event.pos):
                    active_list[i] *= -1
            if save_button.collidepoint(event.pos):
                save_menu = True
            if load_button.collidepoint(event.pos):
                load_menu = True
                playing = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                playing = True
                typing = False
                beat_name = ''
            if entry_rect.collidepoint(event.pos):
                if save_menu:
                    if typing:
                        typing = False
                    else:
                        typing = True
                if load_menu:
                    index = (event.pos[1] - 100) // 50
            if save_menu:
                if saving_button.collidepoint(event.pos):
                    file = open('saved_beats.txt', 'w')
                    saved_beats.append(
                        f'\nname: {beat_name}, beats: {beats}, bpm: {bpm}, selected: {clicked}')
                    for i in range(len(saved_beats)):
                        file.write(str(saved_beats[i]))
                    file.close()
                    save_menu = False
                    load_menu = False
                    playing = True
                    typing = False
                    beat_name = ''
            if load_menu:
                if delete_button.collidepoint(event.pos):
                    if 0 <= index < len(saved_beats):
                        saved_beats.pop(index)
                if loading_button.collidepoint(event.pos):
                    if 0 <= index < len(saved_beats):
                        beats = loaded_information[0]
                        bpm = loaded_information[1]
                        clicked = loaded_information[2]
                        index = 100
                        save_menu = False
                        load_menu = False
                        playing = True
                        typing = False
        if event.type == pygame.TEXTINPUT and typing:
            beat_name += event.text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(beat_name) > 0:
                beat_name = beat_name[:-1]
            if event.key == pygame.K_ESCAPE:
                run = False

    beat_length = 3600 // bpm

    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True
    for i in on_of_list:
        if on_of_list.count(i) % 2 == 1:
            # convert list to string
            string_convert = ''.join(new_messages_list)
            saving_text = label_font.render(string_convert, True, black)
            screen.blit(saving_text, (150, 110))
    # saurab = pygame.draw.rect(screen, white, [110, 90, 1200, 70], 0, 5)

    # pygame.draw.rect(screen, (102, 0, 204), [1150, HEIGHT - 150, 200, 100], 0, 5)

    # print(new_messages_list)

        # if typing_variable == i:
        #     saving_text = label_font.render(list_messages[i], True, red)
        #     screen.blit(saving_text, (575, 80))

    pygame.display.flip()
    # pygame.draw.rect(screen, gray, [50, HEIGHT - 150, 200, 100], 0, 5)


file = open('saved_beats.txt', 'w')
for i in range(len(saved_beats)):
    file.write(str(saved_beats[i]))
file.close()
pygame.quit()
