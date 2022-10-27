# Externe Bibliotheken
import pygame as pg
import cv2


# CV zu Pygame
def cv_zu_pygame(bild):
    return pg.image.frombuffer(bild.tobytes(), (bild.shape[1], bild.shape[0]), "BGR")


# Lade video
def lade_video(pfad):

    video = []

    capture = cv2.VideoCapture(pfad)

    while capture.isOpened:

        _, frame = capture.read()

        if not _:
            break

        video.append(cv_zu_pygame(frame))

        # cv2.imshow("Test", frame)
        #
        # if cv2.waitKey(25) & 0xFF == ord('q'):
        #     break

    capture.release()

    return video
