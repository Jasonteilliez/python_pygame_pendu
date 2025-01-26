import pygame, sys
import random

from settings import *

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.words = self.import_words()
        self.word = self.new_word()
        self.guessed_lettres = set()
        self.correct_lettres = set()
        self.guesses_try = 7

        self.font = pygame.font.Font(FONT2, FONT_SIZE)

        self.end = False
        self.result = False

        self.msg_restart = "Press 'Y' to play again, press 'N' to quit."


    def import_words(self):
        with open('pendu/game/dico.txt') as f:
            words = f.readlines()
        words = [word.strip().upper() for word in words]
        return words
    
    def new_word(self):
        return random.choice(self.words)

    def display_word(self):
        word = ''
        for letter in self.word:
            if letter in self.correct_lettres:
                word += letter + ' '
            else:
                word += '_ '
        word_text = self.font.render(word, False, TEXT_WHITE)
        self.display_surface.blit(word_text, (20,20))

    def display_guessed_letters(self):
        for i in range(26):
            x = 20 + 40 * i
            y = 100
            letter = chr(ord('A') + i)

            text_color = TEXT_WHITE
            if letter in self.guessed_lettres:
                text_color = TEXT_RED
            if letter in self.correct_lettres:
                text_color = TEXT_GREEN

            text = self.font.render(letter, False, text_color)
            text_rect = text.get_rect(center = (x + 15, y + 15))

            pygame.draw.rect(self.display_surface, text_color, (x, y, 30, 30), 2)
            self.display_surface.blit(text, (text_rect)) 

    def display_try(self):
        message = 'Il vous reste ' + str(self.guesses_try) + ' essais.'
        text = self.font.render(message, False, TEXT_WHITE)
        self.display_surface.blit(text, (20, 200))

    def display_result(self):
        if self.result:
            message_result = "Congratulations, you win!"
            text_color =  TEXT_GREEN
        else:
            message_result = "You lose, the word was " + self.word
            text_color =  TEXT_RED
        message = self.font.render(message_result, False, text_color)
        self.display_surface.blit(message, (20,300))
        message = self.font.render(self.msg_restart, False, TEXT_WHITE)
        self.display_surface.blit(message, (20,350))

    def input(self, event):
        if not self.end:
            if event.key >= pygame.K_a and event.key <= pygame.K_z:
                letter = chr(event.key).upper()
                if letter not in self.guessed_lettres:
                    self.guessed_lettres.add(letter)
                    if letter in self.word:
                        self.correct_lettres.add(letter)
                    else:
                        self.guesses_try -=1

        if self.end:
            if event.key == pygame.K_y:
                self.reset_game()
            if event.key == pygame.K_n:
                pygame.quit()
                sys.exit()

    def check_engame(self):
        if self.check_win():
            self.end = True
            self.result = True
        if self.check_lose():
            self.end = True

    def check_win(self):
        for letter in self.word:
            if letter not in self.correct_lettres:
                return False
        return True

    def check_lose(self):
        if self.guesses_try <=0:
            return True
        return False

    def reset_game(self):
        self.word = self.new_word()
        self.guessed_lettres = set()
        self.correct_lettres = set()
        self.guesses_try = 7
        self.end = False
        self.result = False


    def run(self):
        self.display_word()
        self.display_guessed_letters()
        self.display_try()
        self.check_engame()
        if self.end:
            self.display_result()