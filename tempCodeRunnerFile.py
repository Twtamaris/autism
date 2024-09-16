class Button():
    # def __init__(self):

        
        
    def play_pause_button():
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

        return play_pause, play_text