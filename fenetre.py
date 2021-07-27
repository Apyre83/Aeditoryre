#coding: UTF-8

#on fait tous les imports ici
import tkinter

#fichier accounts.py & settings.py
from accounts import Accounts
from settings import Settings

from tkinter import filedialog, ttk
import os, subprocess, threading

"""
Pour les groupes: il y a un menu déroulant, tu peux sélectionner ton groupe, et lorsque tu l'as select, il affiche
les adhérants à droite
"""

#classe principale qui représente l'ide, on hérite de threading
class Fenetre(tkinter.Frame, threading.Thread):
    def __init__(self):

        #threading permet d'effectuer plusieurs actions en même temps
        threading.Thread.__init__(self)

        """#self.police_terminal = "Bahnschrift SemiBold"
        #self.font_titre_terminal = ("Arial Black", 10)
        #self.fontSize = 16  # taille de la police"""
        #self.fontTerminal = 13

        self.userConnedID = None
        self.identifiants = None


    #la fonction start est obligatoire pour faire fonctionner le thread principale, si la classe hérite de threading.Thread
    def start(self, parent):
        tkinter.Frame.__init__(self, master=parent)

        self.parent = parent
        self.grid()

        """self.parent['bg'] = '#07080A'  # changer la couleur
        #self.parent.title('Aeditoryre')  # changer le titre
        # recuperer les dimensions de l'écran
        #self.dimensions = (self.parent.winfo_screenwidth(), self.parent.winfo_screenheight())
        # changer les dimensions de la fenetre
        #self.parent.geometry("{}x{}+{}+{}".format(self.settings.dimensions[0], self.settings.dimensions[1], 0, 0))"""

        # initialisation de la classe Accounts
        self.account = Accounts(self)

        # initialisation de la classe Settings
        self.settings = Settings(self)

        self.settings.interpreter = None
        self.settings.open_status_name = False

        # on installe les widgets
        self.init_widgets()

    def init_widgets(self):

        #création des barres de défilement de la zone de texte principale
        self.xScrollBarMainText = tkinter.Scrollbar(self.parent, orient=tkinter.HORIZONTAL)
        self.xScrollBarMainText.grid(row=3, column=1, sticky="ew")
        self.yScrollBarMainText = tkinter.Scrollbar(self.parent, orient=tkinter.VERTICAL)
        self.yScrollBarMainText.grid(row=0, column=2, rowspan=3, sticky="nsw")

        #lorsque ecran height = 1080, nbCara = 43, lorsque width = 1920, nbCara = 100
        #sachant que les tailles de Text ne se font pas en pixels mais en nb de cara: les rapport sont: longueur = 683/61 et largeur = 128/5
        self.mainText = tkinter.Text(self.parent, wrap=tkinter.NONE, xscrollcommand=self.xScrollBarMainText.set,
                    yscrollcommand=self.yScrollBarMainText.set, font=("Helvetica", self.settings.fontSize), bg='#141B33',
                    width=int(self.settings.dimensions[0] // (683/61) * 60 // 100), height=int(self.settings.dimensions[1] // (128/5) * 95 // 100),
                    fg='#8997C7', undo=True, insertwidth=2, insertbackground="white", tabs=('1c'))
        self.mainText.grid(row=0, column=1, rowspan=3)


        self.xScrollBarMainText.config(command=self.mainText.xview, width=16)
        self.yScrollBarMainText.config(command=self.mainText.yview, width=16)

        #Création de la barres pour afficher les lignes
        self.countingLinesMainText = tkinter.Label(self.parent, width=5, bg="#1B1C33", borderwidth=5, fg="#FFFFFF",
                                                   text="1", font=("Helvetica", self.settings.fontSize),
                                                   anchor=tkinter.N + tkinter.W)
        self.countingLinesMainText.grid(row=0, column=0, rowspan=3, sticky=tkinter.N + tkinter.S)



        #création du terminal
        self.terminal = tkinter.Text(self.parent, wrap=tkinter.NONE, bg="#141B33", font=("Helvetica", self.settings.fontSize),
                                     fg='#8997C7', width=int(self.settings.dimensions[0] // (683/61) * 30 // 100),
                                     height=int(self.settings.dimensions[1] // (128/5) * 25 // 100), borderwidth=3)
        self.terminal.grid(row=2, column=3, sticky=tkinter.S + tkinter.W + tkinter.E)

        self.new_width, self.new_height = int(16 * self.terminal["width"] // 12), int(16 * self.terminal["height"] // 12)
        self.terminal.config(width=self.new_width, height=self.new_height, font=("Helvetica", self.settings.fontTerminal))


        self.text_for_terminal = "Terminal / Console;\nNo selected file, current directory: {}".format(os.getcwd())

        if len(self.text_for_terminal) > 90:
            self.settings.font_titre_terminal = ("Arial Black", 8)

        self.titre_terminal = tkinter.Label(self.parent, text=f"Terminal / Console;\nNo selected file, current directory: {os.getcwd()}",
                            font=self.settings.font_titre_terminal, width=int(self.settings.dimensions[0] // (683/61) * 30 // 100),
                            bg="#0D0D0D", borderwidth=int(self.settings.dimensions[0] / self.settings.dimensions[1] * (9/1.8)), fg="#A6A6A6")
        self.titre_terminal.grid(row=2, column=3, sticky=tkinter.S + tkinter.E + tkinter.W,
                                 pady=int(self.settings.dimensions[1] // (1080/257)))


        #création des groupes:
        self.groups = tkinter.Label(self.parent, bg="#141B33", fg="#8997C7", borderwidth=3, height=self.terminal["height"])
        self.groups.grid(row=2, column=3, sticky=tkinter.E + tkinter.W, pady=int(self.settings.dimensions[1] // (1080/279)))



        self.groupsConnected = tkinter.Label(self.parent, text="Groups: You aren't logged in", bg="#141B33", fg="#A6A6A6",
                                             font=(self.settings.police_terminal, self.settings.fontTerminal, "underline"),
                                             borderwidth=1)

        self.groupsConnected.grid(row=2, column=3, sticky=tkinter.W + tkinter.N, pady=int(self.settings.dimensions[1] // (1080/310)),
                                  padx=int(self.settings.dimensions[0] // (1920/8)))


        # créer le menu en haut de l'écran (file: edit...)
        self.menu = tkinter.Menu(self.parent)
        self.parent.config(menu=self.menu)


        # on ajoute le menu File
        self.file_menu = tkinter.Menu(self.menu, tearoff=False)  # Tearoff permet juste de faire plus joli
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save as", command=self.save_as_file)
        self.file_menu.add_command(label="Select Python interpreter", command=self.select_interpreter)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)

        #Menu Edit, qui est pour l'instant vide, à compléter plus tard
        self.menu_Edit = tkinter.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Edit", menu=self.menu_Edit)
        self.menu_Edit.add_command(label="Edit color")

        #Menu Run, pour lancer les programmes
        self.menu_Run = tkinter.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Run", menu=self.menu_Run)
        self.menu_Run.add_command(label="Run File", command=self.runFile)

        #Menu Account, pour coder à plusieurs
        self.menu_Account = tkinter.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Account", menu=self.menu_Account)
        self.menu_Account.add_command(label="Login", command=self.userConnected, state="active")    #"active" = faire en sorte que les couleurs s'appliquent alors que "normal" permet juste de s'activer, donc si la souris passe dessus la couleur ne changera pas forcément
        self.menu_Account.add_command(label="Register", command=self.account.register, state="active")
        self.menu_Account.add_command(label="Log out", command=self.userLogOff, state="disabled") #state permet de changer l'état du boutton (on peut cliquer dessus ou pas)
        #self.menu_Account.entryconfig(index, options) pour modifier un menu


    def userConnected(self):
        """
        permet de connecter l'utilisateur, puis de gérer les groupes
        les groupes sont séparés par des "," ex: groupe1,groupe2
        """

        #se connecter avec une nouvelle fenetre tkinter
        self.account.login()

        #self.account.request sous forme (pseudo, email, password, groupe="")
        self.identifiants = self.account.request


        if self.identifiants:
            self.groupsConnected["text"] = "Groups: Connected as %s !" % self.identifiants[0]
            self.menu_Account.entryconfig(0, state="disabled")
            self.menu_Account.entryconfig(1, state="disabled")
            self.menu_Account.entryconfig(2, state="active")

            #l'user appartient a un ou plusieurs groupe(s)
            if self.identifiants[3]:
                #faire une liste avec tous les groupes qu'on sépare par une virgule, si il n'y a qu'un seul groupe, c'est une liste vide
                self.options = self.identifiants[3].split(",") if "," in self.identifiants[3] else [self.identifiants[3]]

                #créer le style pour le combo box. A noter que c'est différent qu'avec le label ou autre car la combobox est issue de ttk
                self.comboStyle = ttk.Style()
                self.comboStyle.theme_create('comboStyle', parent="alt", settings={
                    'TCombobox': {
                        'configure': {
                            'selectbackground': "#ffffff",
                            'fieldbackground': "#ffffff",
                            'background': "#ffffff"
                        }}})
                self.comboStyle.theme_use("comboStyle")

                self.groups = ttk.Combobox(self.parent, values=self.options, width=20, height=20)
                self.groups.set("Your groups:")
                self.groups.grid(row=2, column=3, sticky=tkinter.W, padx=20, pady=20)

    def userLogOff(self):
        """
        déconnecter l'utilisateur
        """

        self.identifiants = None
        self.groupsConnected["text"] = "Groups: You aren't logged in"
        self.menu_Account.entryconfig(0, state="active")
        self.menu_Account.entryconfig(1, state="active")
        self.menu_Account.entryconfig(2, state="disabled")
        self.groups.destroy()

    def runFile(self):
        """
        éxécuter le script python, pour se faire, on lance un nouveau thread pour ne pas bloquer l'ide
        """

        self.save_file()
        #self.interpreter = "python" #à enlever après
        #si l'user a entré son chemin d'acces vers son interpreter
        if self.settings.interpreter:
            try:
                test = threading.Thread(target=self.creating_thread, args=(self.open_status_name,))
                test.start()

            #déboggage
            except Exception as e:
                print(f"Numéro 1, dans run file : {e}")

        #afficher un message d'erreur
        else:
            self.terminal.delete("1.0", tkinter.END)
            self.terminal.insert(tkinter.INSERT, "ERROR: No Python interpreter selected")

    def open_file(self, debut=False):  # fonction de l'ouverture d'un fichier

        if not self.text_file and debut:
            # parcourir les fichiers de l'ordinateur
            self.text_file = filedialog.askopenfilename(initialdir="C:/gui/", title="Open file", filetypes=(
                ("Python Files", "*.py"), ("Text Files", "*.txt"), ("HTML Files", "*.html"), ("All Files", "*.*")))

        if self.text_file and :  # si l'user en a selectionné 1
            self.open_status_name = self.text_file
        else:
            return 0

        # mise à jour du nom de la fenetre en fonction du fichier choisi
        self.name = self.text_file
        self.name = self.name.replace("C:/gui/", "")
        self.parent.title(f"{self.name} - Aeditoryre")

        self.mainText.delete("1.0", tkinter.END)  # supprimer le texte

        # ouvrir le fichier
        self.text_file = open(self.text_file, "r", encoding="UTF-8")
        self.donnes = self.text_file.read()

        # on l'ajoute à l'éditor
        self.mainText.insert(tkinter.END, self.donnes)
        self.text_file.close()

        self.titre_terminal['text'] = f"Terminal / Console;\nSelected file: {self.name}"

    def select_interpreter(self):
        """
        Permet de choisir un interpreter, et est necessaire afin d'executer le script pyton
        """
        try:
            self.settings.interpreter = filedialog.askopenfilename(initialdir="C:/gui/", title="Select Python interpreter",
                                                          filetypes=(("Executables", ".exe"), ("All Files", "*.*")))
            if os.path.abspath(self.settings.interpreter).endswith(".exe"):
                self.terminal.delete("1.0", tkinter.END)
                self.terminal.insert(tkinter.INSERT, f"{self.settings.interpreter} selected as Python interpreter, happy codding !")
            else:
                self.terminal.delete("1.0", tkinter.END)
                self.terminal.insert(tkinter.INSERT, "Error while selecting Python interpreter, try again")
                self.terminal = None

        #Utilisé pour le deboggage
        except Exception as e:
            print(f"Numéro 1 dans select interpreter : {e}")

    def new_file(self):
        # supprimer ce qu'il y avait avant
        self.mainText.delete("1.0", tkinter.END)
        # mise a jour du titre
        self.parent.title('New File - Aeditoryre')

        #open_status_name permet de savoir si un fichier vient juste d'être créer ou non (voir fonction save file)
        self.open_status_name = False

    def save_file(self):
        #si le fichier existait déjà (a été ouvert par l'user) alors on le sauvergarde simple
        if self.open_status_name:
            # ouvrir le fichier pour réecrire ce que l'user a écrit
            self.text_file = open(self.open_status_name, 'w', encoding="UTF-8")
            self.text_file.write(self.mainText.get(1.0, tkinter.END))
            # fermer le fichier
            self.text_file.close()

            #mise à jour du titre
            self.name = self.open_status_name
            self.name = self.name.replace("C:/gui/", "")
            self.parent.title(f'{self.name} - Aeditoryre !')

        #sinon il faut le créer
        else:
            self.save_as_file()

    def save_as_file(self):
        self.text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="C:/gui/", title="Save File",
                                                 filetypes=(("Python Files", "*.py"), ("Text Files", "*.txt"),
                                                            ("HTML Files", "*.html"), ("All Files", "*.*")))
        #l'user a bien selectionné comment le sauvergardé
        if self.text_file:
            self.open_status_name = self.text_file

            self.name = self.text_file
            self.name = self.name.replace("C:/gui/", "")
            self.parent.title(f'{self.name} - Aeditoryre !')

            # on écrit les données dans le fichier
            self.text_file = open(self.text_file, 'w', encoding="UTF-8")
            self.text_file.write(self.mainText.get(1.0, tkinter.END))

            # puis on ferme le fichier
            self.text_file.close()

            self.titre_terminal['text'] = f"Terminal / Console;\nSelected file: {self.name}"

        #l'utilisateur n'a rien fait, on pourrait omettre le else mais je le laisse pour être sûr de ne pas avoir fait une erreur
        else:
            return 0

    def creating_thread(self, file):
        """
        Fonction qui execute le code python
        On utilise une module: subprocess:

        "Le module subprocess vous permet de lancer de nouveaux processus,
        les connecter à des tubes d'entrée/sortie/erreur, et d'obtenir leurs
        codes de retour. Ce module a l'intention de remplacer plusieurs anciens modules et fonctions" d'après la documentation officielle de python

        Je pourrai passer par un terminal classique avec le module os mais celui ci est très limité, par exemple si le code a une erreur, je n'ai pas réussi à trouver
        comment la récupérer
        """
        #Problèmes d'encodage à voir plus tard...


        try:
            #commende à executer
            self.command = '"{}" "{}"'.format(self.settings.interpreter.replace('''/''', '''\\'''), file.replace('''/''', '''\\'''))

            #le résultat de l'execution, stderr permet de récupérer la sortie, shell est la gestion d'erreur et l'encoding utilisé est celui de windows car utf8 ne fonctionnait pas ici...
            self.script = subprocess.check_output(self.command, stderr=subprocess.STDOUT, shell=True, encoding="cp850")

            #remplacer ce qu'il y avait écrit dans le terminal avec la nouvelle sortie
            self.terminal.delete("1.0", tkinter.END)
            self.terminal.insert(tkinter.INSERT, self.script)

        #se déclenche si on a rencontré une erreur dans le script
        except subprocess.CalledProcessError as error:

            try:
                #le message est encodé il faut donc le décoder, l'encodate est en utf8 (et est spécifié en haut du fichier)
                self.result = error.output.decode("UTF-8")

                #remplacer ce qu'il y avait écrit dans le terminal avec la nouvelle sortie'
                self.terminal.delete("1.0", tkinter.END)
                self.terminal.insert(tkinter.INSERT, self.result)

            #utilisé pour le deboggage
            except AttributeError as error2:
                print(f"error:  {error}")
                print(f"error output: {error.output}")
                print(f"error2: {error2}")

        #utilisé pour le deboggage
        except Exception as e:
            self.terminal.delete("1.0", tkinter.END)
            self.terminal.insert(tkinter.INSERT, e)
            print(f"Numéro 1 fonction creating thread : {e}")

if __name__ == "__main__":
    root = tkinter.Tk()
    app = Fenetre()
    app.start(root)
    app.mainloop()