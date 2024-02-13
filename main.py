import tkinter as tk
from tkinter import PhotoImage, Canvas
import ctypes
import pyautogui
import random

class Playboy:
    def __init__(self, scene, x=0, y=0):
        self.scene = scene 
        self.image = PhotoImage(file='Figura.png') 
        self.image = self.image.subsample(16)
        self.image_bomb = PhotoImage (file ='Explosion-8.png')
        self.image_bomb =  self.image_bomb.subsample(8)
        self.imageRef = scene.canvas.create_image(x,y,image=self.image)
        self.bomb_status = False

    def update (self):
        x, y = pyautogui.position()
        ban_x, ban_y = self.scene.canvas.coords (self.imageRef)
        dist = (abs(x-ban_x)) +abs ((y-ban_y))
        
        if self.bomb_status:
            self.scene.canvas.itemconfig(self.imageRef, image=self.image_bomb)
            if random.random() < 0.1: 
                new_playboy= Playboy(self.scene, x, y)
                self.scene.PlayBoy.append (new_playboy)
                return

            self.scene.canvas.move(
                self.imageRef,
                random.choice((-30, 300)),
                random.choice((-30, 300)),
            )
            self.scene.canvas.itemconfig(self.imageRef, image=self.image)
            self.bomb_status = False

        elif dist < 5:
            self.scene.canvas.itemconfig(self.imageRef, image=self.image_bomb)
            self.bomb_status = True

        else:
            self.scene.canvas.move (
                self.imageRef,
                1 if x > ban_x else -1, 
                1 if y > ban_y else -1
            )
            


class Scene:
    def __init__(self, window: tk.Tk):
        self.screen_width = window.winfo_screenwidth()
        self.screen_height = window.winfo_screenheight()
        self.canvas = Canvas (
            window,
            width=self.screen_width,
            height=self.screen_height,           
            highlightthickness=0,
            bg='white'           
        )
        self.canvas.pack()
        self.PlayBoy = list()

    def update (self):
        for PlayBoys in self.PlayBoy:
            PlayBoys.update()  

    def new_Playboy(self, x, y):
        Playboy_instance= Playboy(self)
        self.canvas.move(Playboy_instance.imageRef, x, y)
        self.PlayBoy.append(Playboy_instance)

class Game:
    
        def __init__(self):
           self.window = self.create_window() 
           self.apply_click_through (self.window)
           self.scene = Scene(self.window)


        def update (self):
            self.scene.update()
            self.window.after(20, self.update)

        def create_window (self):
            window = tk.Tk ()
            window.wm_attributes ("-topmost", True)
            window.attributes ("-fullscreen", True)
            window.overrideredirect(True)
    #Transparencia
            window.attributes('-transparentcolor', 'white')
            window.config (bg= 'white')
            return window

        def apply_click_through (self, window):
        #constantes API Windows

            WS_EX_TRANSPARENT = 0x00000020
            WS_EX_LAYERED = 0x00080000
            GWL_EXSTYLE = -20 

        #obtener el identuificador de ventana 

            hwnd = ctypes.windll.user32.GetParent (window.winfo_id())

    # Obtener los estulpos actuales de la ventana 

            style = ctypes.windll.user32.GetWindowLongW (hwnd, GWL_EXSTYLE)

    #Establecer nuevo estilo

            style = style | WS_EX_TRANSPARENT | WS_EX_LAYERED

            ctypes.windll.user32.SetWindowLongW (hwnd, GWL_EXSTYLE, style)

        def Start (self):
            self.update ()
            self.window.mainloop() 

game_instance = Game()
game_instance.scene.new_Playboy(100, 100)
game_instance.Start()