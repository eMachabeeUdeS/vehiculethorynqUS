#!/usr/bin/env python
'''
**********************************************************************
* Filename    : vehicle.py
* Description : A module to control the wheels of RPi Car
* Author      : Étienne Machabée
* Brand       : ornithorynqUS
* E-mail      : mace2801@usherbrooke.ca
**********************************************************************
'''

from picar import back_wheels
from picar import front_wheels
import time
import picar

class vehicle:

    VEHICLE_STATES = {
    'STOP' : 0,
    'FORWARD' : 1,
    'BACKWARD' : 2,
    }

    WHEELBASE = 0.14 # 14cm d'empattement
    TRACK = 0.1143 # 11cm de voie

    _speedprct = 0 # Vitesse de la roue la plus rapide en pourcentage
    _wheel_angle = 0 # Angle des roues, 0 est le centre
    _state = VEHICLE_STATES['STOP'] # État, 0 = stop, 1 = avancer, 2 = arrêté

    def __init__(self):
        picar.setup()
        self.bw = back_wheels.Back_Wheels(db='config')
        self.fw = front_wheels.Front_Wheels(db='config')

    # Getter pour la vitesse en m/s
    def getspeedms(self):
        return 0.002736871508379887 * self._speedprct - 0.01346368715083793

    # Getter pour l'angle des roues en radians
    def getwheelanglerad(self):
        return self._wheel_angle

    # Convertit l'angle des roues en radians en rayon de virage en mètres
    def angle_to_radius(self, angle):
        try:
            # print("Angle commandé:", angle)
            if angle <= np.pi/2:
                radius = WHEELBASE/np.tan(angle)
        except:
            print("Erreur de calcul du rayon")
            return 0
        return radius

    # Ajuste la vitesse du robot, équivalent à la librairie du robot
    # Crée un différentiel pour les virages, rendant le rayon de virage plus bas
    def speed(self, percent):
        if percent < 0:
            self._speedprct = 0
            return
        elif percent > 100:
            self._speedprct = 100
            return
        else:
            self._speedprct = percent
        # Calculer les deux vitesses (extérieure et intérieure)
        radius = angle_to_radius(self._wheel_angle)
        if _wheel_angle = 0: # Centre
            self.bw.speed(percent, percent)
        elif _wheel_angle < 0: # Gauche
            circonleft = np.abs((radius - TRACK / 2) * 2 * np.pi)
            circonright = np.abs((radius + TRACK / 2) * 2 * np.pi)
            ratio = circonleft / circonright
            speedleft = percent * ratio
            speedright = percent
            self.bw.speed(speedleft, speedright)
        elif _wheel_angle > 0: # Droite
            circonleft = np.abs((radius + TRACK / 2) * 2 * np.pi)
            circonright = np.abs((radius - TRACK / 2) * 2 * np.pi)
            ratio = circonright / circonleft
            speedleft = percent
            speedright = percent * ratio
            self.bw.speed(speedleft, speedright)

    # Mettre les roues droites
    def turn_straight(self):
        self._wheel_angle = np.radians(90-90)
        self.fw.turn_straight()

    # Tourner à gauche au max
    def turn_left(self):
        self.fw.turn_left()

    # Tourner à droite au max
    def turn_right(self):
        self.fw.turn_right()

    # Tourner à un angle, en degrés. 90 est tout droit.
    def turn(self, angle):
        if angle >= 0:
            self._wheel_angle = np.radians(90-angle)
            self.fw.turn(angle)

    # Avancer
    def forward(self):
        self._state = VEHICLE_STATES['FORWARD']
        self.bw.forward()

    # Reculer
    def backward(self):
        self._state = VEHICLE_STATES['BACKWARD']
        self.bw.backward()

    # Arrêter
    def stop(self):
        self._speedprct = 0
        self._state = VEHICLE_STATES['STOP']
        self.bw.stop()
