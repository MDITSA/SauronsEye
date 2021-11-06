# Following modules are needed:
# pygame, opencv-python, face_recognition
#
# Every other module in the requirements.txt is a automatically installed dependency with pip (as far as i remember cmake is needed to for dlib)

import pygame
import cv2
import face_recognition

pygame.init()

class SauronsEye(object):
    def __init__(self):
        pygame.display.set_caption('SauronsEye')

        self.video_capture = cv2.VideoCapture(1)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 270)
        self.face_locations = []

        self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.display_width, self.display_height = self.display_surface.get_size()

        self.image = pygame.image.load(r'media\eye.png').convert_alpha()
        self.image_width, self.image_height = self.image.get_size()

        pygame.mixer.music.load('media/voice.mp3')

        self.image_center_pos_width = self.display_width/2-(self.image_width/2)
        self.image_center_pos_height = self.display_height/2-(self.image_height/2)

        self.image_pos_x = self.image_center_pos_width
        self.image_pos_y = self.image_center_pos_height

        self.bg_colour = (0,0,0)
        self.tick = pygame.time.get_ticks()

    def find_face(self):
        ret, self.frame = self.video_capture.read()
        self.rgb_frame = self.frame[:, :, ::-1]
        self.face_locations = face_recognition.face_locations(self.rgb_frame)
        for face_top, face_right, face_bottom, face_left in self.face_locations:
            self.face_top_resized = face_top*4
            self.face_right_resized = face_right*4
            self.face_bottom_resized = face_bottom*4
            self.face_left_resized = face_left*4
            
            self.face_center_x = (self.face_left_resized+self.face_right_resized)/2
            self.face_center_y = (self.face_top_resized+self.face_bottom_resized)/2

            self.image_pos_x = 1920-self.face_center_x-(self.image_width/4) #1920- needed because otherwise the movement would be inverted... dont ask me why...
            self.image_pos_y = self.face_center_y-(self.image_height/2)

    def show_eye(self):
        self.display_surface.fill(self.bg_colour)
        self.rect = self.display_surface.blit(self.image,(self.image_pos_x,self.image_pos_y))

        pygame.display.update()

    def play_voice(self):
        pygame.mixer.music.play(0,0.0)

    def main(self): 
        while True:
            for event in pygame.event.get() :
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE :
                    pygame.display.quit()
                    pygame.quit()
                    quit()

            self.find_face()
            self.show_eye()

            self.now = pygame.time.get_ticks()
            if self.now > self.tick + 20000:
                self.play_voice()
                self.tick = self.now

SauronsEye().main()