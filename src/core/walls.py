"""
Wall file
"""
from enums.config import Config
import random


class Wall ():

    def __init__(self, position_p=random.uniform(0,100), size_p=10.0, color_p=Config.DEFAULT_COLOR_RED.value):
        self.position = position_p
        self.size = size_p
        self.color = color_p

    def __repr__(self):
        return "Wall: position={}, color={}".format(
            self.position, self.color)
    
    def get_size(self):
        return self.size
    
    def get_color(self):
        return self.color
    
    def get_position(self):
        return self.position
    
    def set_size(self,size_p):
        self.size = size_p
    
    def set_color(self, color_p):
        self.color = color_p
    
    def set_position(self, position_p):
        self.position = position_p
    

    