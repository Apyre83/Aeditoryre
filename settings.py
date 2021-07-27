#coding: UTF-8
import json

#classe qui permet la gestion de tous les paramètres de la fenetre principale
class Settings():
    def __init__(self, superieur):

        self.fenetre = superieur

        with open("settings.json", "r") as file:
            self.unread_settings = file.read()
            self.old_settings = json.loads(self.unread_settings)

        self.interpreter = self.old_settings["Interpreter"]
        self.open_status_name = False


        self.fenetre.parent['bg'] = '#07080A'
        self.police_terminal = "Bahnschrift SemiBold"

        self.font_titre_terminal = ("Arial Black", 10)
        self.fontSize = 16  # taille de la police
        self.fontTerminal = 13

        self.dimensions = (self.fenetre.parent.winfo_screenwidth(), self.fenetre.parent.winfo_screenheight())
        self.fenetre.parent.geometry("{}x{}+{}+{}".format(self.dimensions[0], self.dimensions[1], 0, 0))

        self.fenetre.parent.title('Aeditoryre')  # changer le titre


