import random

from constant import *


class Question:
    def __init__(self, question: str, answer_1: str, answer_2: str, answer_3: str, answer_4: str, answer_5: str,
                 correct_answer: int):

        # Build the question line
        self.question = []

        for i in question.split("\n"):
            self.question.append(FONT.render(i, True, COLOR_BLACK))

        # Build the answers
        self.answers = [

            FONT.render(answer_1, True, COLOR_BLACK),
            FONT.render(answer_2, True, COLOR_BLACK),
            FONT.render(answer_3, True, COLOR_BLACK),
            FONT.render(answer_4, True, COLOR_BLACK),
            FONT.render(answer_5, True, COLOR_BLACK)

        ]

        # Initialise the buttons
        self.buttons = [

            Button(0, SCREEN_HEIGHT - 160, SCREEN_WIDTH, 32, lambda: self.act_checkanswer(5)),
            Button(0, SCREEN_HEIGHT - 192, SCREEN_WIDTH, 32, lambda: self.act_checkanswer(4)),
            Button(0, SCREEN_HEIGHT - 224, SCREEN_WIDTH, 32, lambda: self.act_checkanswer(3)),
            Button(0, SCREEN_HEIGHT - 256, SCREEN_WIDTH, 32, lambda: self.act_checkanswer(2)),
            Button(0, SCREEN_HEIGHT - 288, SCREEN_WIDTH, 32, lambda: self.act_checkanswer(1))

        ]

        self.correct_answer = correct_answer

        # Shows what page of the question is active
        self.phase = "getready"

        # Animation frames
        self.countdown = 2 * SCREEN_REFRESH_RATE

    def phase_answering(self):

        # Draw the question text line by line
        for i in range(0, len(self.question)):
            SCREEN.blit(self.question[i], (0, i * 32))

        # Draw the buttons and the answers
        for i in range(5, 0, -1):
            SCREEN.blit(pygame.transform.scale(IMAGE_BUTTON, (SCREEN_WIDTH, 32)), (0, SCREEN_HEIGHT - 128 - i * 32))
            SCREEN.blit(self.answers[-i], (0, SCREEN_HEIGHT - 128 - i * 32))

        # Activate buttons
        for i in self.buttons:
            i.loop()

    def loading_bar(self, text, redirect):

        if self.countdown > 0:
            title = FONT.render(text, True, COLOR_BLACK)
            time = FONT.render(str(self.countdown // SCREEN_REFRESH_RATE), True, COLOR_BLACK)

            SCREEN.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 16))
            SCREEN.blit(time, (SCREEN_WIDTH // 2 - time.get_width() // 2, SCREEN_HEIGHT // 2 + 8))

            pygame.draw.rect(SCREEN, (0, 255, 0), (
                SCREEN_WIDTH // 2 - self.countdown // 2,
                SCREEN_HEIGHT // 2 + 40,
                self.countdown,
                16
            ))

            self.countdown -= 1

        if self.countdown <= 0:
            self.phase = redirect
            self.countdown = 2 * SCREEN_REFRESH_RATE

    def act_checkanswer(self, answer):

        # Check for the answer
        if self.correct_answer == answer:
            self.phase = "correctanswer"

        else:
            self.phase = "incorrectanswer"

    def loop(self):
        # Detect and change between pages
        if self.phase == "getready":
            self.loading_bar("Hazır Ol", "answering")

        if self.phase == "answering":
            self.phase_answering()

        if self.phase == "correctanswer":
            self.loading_bar("Doğru Cevap", "end")

        if self.phase == "incorrectanswer":
            self.loading_bar("Yanlış Cevap", "end")


class Game:
    def __init__(self):

        self.questions = [
            Question("is A \n = A?", "A", "B", "C", "D", "E", 1),
            Question("is B \n = B?", "A", "B", "C", "D", "E", 2)
        ]

        self.selected_question = random.randint(0, len(self.questions) - 1)

    def loop(self):

        try:
            self.questions[self.selected_question].loop()

            if self.questions[self.selected_question].phase == "end":
                self.selected_question = random.randint(0, len(self.questions) - 1)
                self.questions[self.selected_question].phase = "getready"

        except:
            pass
