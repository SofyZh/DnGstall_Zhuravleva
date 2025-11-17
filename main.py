import pygame
import sys
from pygame.locals import *

pygame.init()

#Tokens:

SCREEN_WIDTH = 525
SCREEN_HEIGHT = 630
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("D&Gstal")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (90, 90, 92)
LIGHT_GREEN = (42, 255, 113)
DARK_GREEN = (44,155,113)

title_font = pygame.font.SysFont('Text me one', 60, bold=False)
lesser_title_font = pygame.font.SysFont('Text me one', 40, bold=False)
button_font = pygame.font.SysFont('Rubik', 26)
info_font = pygame.font.SysFont('Rubik', 18)

MAIN_SCREEN = 0
SELECT_IMAGE_SCREEN = 1
EDIT_SCREEN = 2
COMPLETE_SCREEN = 3

current_screen = MAIN_SCREEN
selected_image = None
edited_image = None


class Button:
    def __init__(self, x, y, width, height, text, color=LIGHT_GREEN, hover_color=DARK_GREEN):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        #pygame.draw.rect(surface, GRAY, self.rect, 2, border_radius=10)

        text_surf = button_font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def is_clicked(self, pos, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False


edit_more_button = Button(SCREEN_WIDTH/2-150, 250, 300, 75, "Edit Mode")
invisible_watermark_button = Button(SCREEN_WIDTH/2-150, 350, 300, 75, "Invisible Watermark")
proceed_button = Button(SCREEN_WIDTH/2-100, 400, 200, 50, "Proceed")
complete_button = Button(SCREEN_WIDTH/2-100, 450, 200, 50, "Complete")
download_button = Button(SCREEN_WIDTH/2-100, 450, 200, 50, "Download")
back_button = Button(50, 50, 100, 40, "Back")


def draw_main_screen():
    screen.fill(BLACK)

    # Title
    title_text = title_font.render("D&Gstal", True, LIGHT_GREEN)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

    # Buttons
    edit_more_button.draw(screen)
    invisible_watermark_button.draw(screen)



def draw_select_image_screen():
    screen.fill(BLACK)

    # Title
    title_text = lesser_title_font.render("Select Image", True, LIGHT_GREEN)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 120))

    # Proceed button
    proceed_button.draw(screen)

    # Back button
    back_button.draw(screen)

    # File selection placeholder
    file_rect = pygame.Rect(SCREEN_WIDTH/2-150, 220, 300, 150)
    pygame.draw.rect(screen, GRAY, file_rect, border_radius=10)
    pygame.draw.rect(screen, LIGHT_GREEN, file_rect, 2, border_radius=10)

    file_text = button_font.render("File selection area", True, LIGHT_GREEN)
    screen.blit(file_text, (SCREEN_WIDTH // 2 - file_text.get_width() // 2, 275))


def draw_edit_screen():
    screen.fill(BLACK)

    title_text = lesser_title_font.render("Edit Mode", True, LIGHT_GREEN)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 120))

    complete_button.draw(screen)

    back_button.draw(screen)

    file_rect = pygame.Rect(SCREEN_WIDTH / 2 - 150, 220, 300, 150)
    pygame.draw.rect(screen, GRAY, file_rect, border_radius=10)
    pygame.draw.rect(screen, LIGHT_GREEN, file_rect, 2, border_radius=10)

    file_text = button_font.render("Edit tools will", True, LIGHT_GREEN)
    screen.blit(file_text, (SCREEN_WIDTH // 2 - file_text.get_width() // 2, 260))
    file_text = button_font.render("appear here", True, LIGHT_GREEN)
    screen.blit(file_text, (SCREEN_WIDTH // 2 - file_text.get_width() // 2, 290))


def draw_complete_screen():
    screen.fill(BLACK)

    title_text = lesser_title_font.render("Edit Complete", True, LIGHT_GREEN)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 120))

    download_button.draw(screen)

    back_button.draw(screen)

    file_rect = pygame.Rect(SCREEN_WIDTH / 2 - 150, 220, 300, 150)
    pygame.draw.rect(screen, GRAY, file_rect, border_radius=10)
    pygame.draw.rect(screen, LIGHT_GREEN, file_rect, 2, border_radius=10)

    preview_text = button_font.render("Edited Image Preview", True, LIGHT_GREEN)
    screen.blit(preview_text, (SCREEN_WIDTH // 2 - preview_text.get_width() // 2, 275))



running = True
skip_edit_flag = False
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT: running = False

        if current_screen == MAIN_SCREEN:
            edit_more_button.check_hover(mouse_pos)
            invisible_watermark_button.check_hover(mouse_pos)

            if edit_more_button.is_clicked(mouse_pos, event): current_screen = SELECT_IMAGE_SCREEN

            if invisible_watermark_button.is_clicked(mouse_pos, event):
                skip_edit_flag = True
                current_screen = SELECT_IMAGE_SCREEN

        elif current_screen == SELECT_IMAGE_SCREEN:
            proceed_button.check_hover(mouse_pos)
            back_button.check_hover(mouse_pos)

            if proceed_button.is_clicked(mouse_pos, event):
                if skip_edit_flag: current_screen = COMPLETE_SCREEN
                else: current_screen = EDIT_SCREEN
            elif back_button.is_clicked(mouse_pos, event): current_screen = MAIN_SCREEN

        elif current_screen == EDIT_SCREEN:
            complete_button.check_hover(mouse_pos)
            back_button.check_hover(mouse_pos)

            if complete_button.is_clicked(mouse_pos, event): current_screen = COMPLETE_SCREEN
            elif back_button.is_clicked(mouse_pos, event): current_screen = SELECT_IMAGE_SCREEN

        elif current_screen == COMPLETE_SCREEN:
            download_button.check_hover(mouse_pos)
            back_button.check_hover(mouse_pos)

            if download_button.is_clicked(mouse_pos, event):
                print("Download functionality is to be implemented")
            elif back_button.is_clicked(mouse_pos, event): current_screen = MAIN_SCREEN

    if current_screen == MAIN_SCREEN: draw_main_screen()
    elif current_screen == SELECT_IMAGE_SCREEN: draw_select_image_screen()
    elif current_screen == EDIT_SCREEN: draw_edit_screen()
    elif current_screen == COMPLETE_SCREEN: draw_complete_screen()

    pygame.display.flip()

pygame.quit()
sys.exit()