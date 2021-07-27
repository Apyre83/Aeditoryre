#coding: UTF8
import sqlite3, tkinter, string, re

#classe qui permet la gestion des comptes de l'user
class Accounts:
    def __init__(self, superieur):

        self.fenetre = superieur
        self.caracteres = list(string.ascii_letters) + [i for i in range(10)]

        #regex pour vérifier si l'adresse email est valide
        self.regex = '^[a-z0-9]+[\._]?[a0--z9]+[@]\w+[.]\w{2,3}$'
        self.label_created = False  # pour savoir si après un message d'erreur est déjà affiché => supprimer
        self.label_created_login = False  # pareil qu'en haut

    def register(self):

        #nouvelle fenetre tkinter
        self.fenetre_register = tkinter.Tk()

        #regler les dimensions de la fenetre
        self.fenetre_register.geometry(f"400x500+{self.fenetre_register.winfo_screenwidth() // 2 - 250}+"
                                       f"{self.fenetre_register.winfo_screenheight() // 2 - 200}")

        #le titre de la fenetre
        self.fenetre_register.title("Register a new account -*-Aeditoryre")

        #faire en sorte que l'on ne puisse pas changer les dimensions de la fenetre
        self.fenetre_register.resizable(width=False, height=False)

        #mettre la couleur du fond d'une certaine couleur
        self.fenetre_register["bg"] = "#141B33"

        #création du label pour indiquer les regles du pseudo à choisir
        self.entry_username_label = tkinter.Label(self.fenetre_register, width=30, height=4,
                                                  text="Entrez un nom d'utilisateur,\ncelui-ci doit posséder uniquement"
                                                       "\ndes chiffres et lettres (minuscules\n ou majuscules) seulement:", )
        self.entry_username_label.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=90, pady=5)
        #création de la zone de texte pour saisir le pseudo
        self.entry_username = tkinter.Entry(self.fenetre_register, width=35)
        self.entry_username.grid(row=1, column=0)

        #séparer distinctement le pseudo de l'email
        self.separator = tkinter.Label(self.fenetre_register, width=30, height=2, bg="#141B33")
        self.separator.grid(row=2, column=0, sticky=tkinter.W + tkinter.E, pady=5)

        #pareil que pour le pseudo
        self.entry_email_label = tkinter.Label(self.fenetre_register, width=30, height=2,
                                               text="Entrez l'adresse e-mail que vous\n voulez utiliser:")
        self.entry_email_label.grid(row=3, column=0, pady=5)
        self.entry_email = tkinter.Entry(self.fenetre_register, width=35)
        self.entry_email.grid(row=4, column=0)

        #deuxieme séparateur
        self.separator2 = tkinter.Label(self.fenetre_register, width=30, height=2, bg="#141B33")
        self.separator2.grid(row=5, column=0, sticky=tkinter.W + tkinter.E, pady=5)

        #pareil que pour le pseudo et l'email
        self.entry_password_label = tkinter.Label(self.fenetre_register, width=30, height=4,
                                                  text="Entrez votre mot de passe,\ncelui-ci doit être compris en 3 et\n 14 carac"
                                                       "tères et doit posséder\nau moins une majuscule")
        self.entry_password_label.grid(row=6, column=0, pady=5)
        self.entry_password = tkinter.Entry(self.fenetre_register, width=35, show="*")
        self.entry_password.grid(row=7, column=0)

        #création du boutton pour valider son choix
        self.button_register = tkinter.Button(self.fenetre_register, width=20, height=4,
                                              text="CONFIRMER\nL'ENREGISTREMENT", command=self.enregistrement_register)
        self.button_register.grid(row=8, column=0, pady=40)

        #faire en sorte que la fenetre tourne en boucle
        self.fenetre_register.mainloop()

    #fonction qui s'appelle lorsque on clique sur le bouton au dessus
    def enregistrement_register(self):

        #on récupère les informations rentrées
        self.username = self.entry_username.get()
        self.email = self.entry_email.get()
        self.password = self.entry_password.get()

        #on récupère le résultat de la vérification des informations (si elle sont cohérantes)
        self.result = self.verification_register(self.username, self.email, self.password)

        #on créer un nouveau label avec soit un message d'erreur soit un message pour nous dire que c'est validé
        if self.label_created:
            self.message_erreur.destroy()
        self.label_created = True
        self.message_erreur = tkinter.Label(self.fenetre_register, font=("Arial", 10), bg="#141B33", fg="#DC143C")

        if self.result == 1:
            self.message_erreur['text'] = "vous devez renseigner ce champ"
            self.message_erreur.grid(row=2, column=0, sticky=tkinter.N)

        elif self.result == 2:
            self.message_erreur["text"] = "votre pseudo ne doit contenir\nque des lettres ou des chiffres"
            self.message_erreur.grid(row=2, column=0, sticky=tkinter.N)

        elif self.result == 3:
            self.message_erreur["text"] = "vous devez renseigner ce champ"
            self.message_erreur.grid(row=5, column=0, sticky=tkinter.N)

        elif self.result == 4:
            self.message_erreur["text"] = "cette adresse email est invalide"
            self.message_erreur.grid(row=5, column=0, sticky=tkinter.N)

        elif self.result == 5:
            self.message_erreur["text"] = "vous devez renseigner ce champ"
            self.message_erreur.grid(row=8, column=0, sticky=tkinter.N)

        elif self.result == 6:
            self.message_erreur["text"] = "votre mot de passe doit être\ncompris entre 3 et 14 caractères"
            self.message_erreur.grid(row=8, column=0, sticky=tkinter.N)

        elif self.result == 7:
            self.message_erreur["text"] = "votre mot de passe doit\ncontenir au moins une majuscule"
            self.message_erreur.grid(row=8, column=0, sticky=tkinter.N)

        #presque tout est bon, il manque juste à vérifier si les informations sont déjà utlisées
        else:
            self.result = self.validation_register(self.username, self.email, self.password)
            if self.result == 1:  # pseudo déjà utilisé
                self.message_erreur["text"] = "Votre pseudo est déjà utilisé,\nveuillez en choisir un autre"
                self.message_erreur.grid(row=8, column=0, sticky=tkinter.S)

            elif self.result == 2:  # email déjà utilisé
                self.message_erreur["text"] = "Votre email est déjà utilisé"
                self.message_erreur.grid(row=8, column=0, sticky=tkinter.S)

            else:
                self.message_fin = tkinter.Label(self.fenetre_register, bg="#141B33", fg="#A39DD6",
                                                 text="Inscription réussie !\nVeuillez retourner à l'accueil pour vous connecter")
                self.message_fin.grid(row=8, column=0, sticky=tkinter.S)
                self.label_created = False

    def verification_register(self, username, email, password):
        """    
        Ici on fait les différentes vérifications et on retourne un nombre correspond à l'erreur ou à la réussite
        """
        if not username:
            return 1  # 1 = l'user n'a pas saisi de pseudo
        for cara in username:
            if not (cara in self.caracteres):
                return 2  # 2 = problème dans le pseudo --> il contient des caractères différents de lettres

        if not email:
            return 3  # 3 = l'user n'a pas saisi d'email
        if not (re.search(self.regex, email)):  # vérifier l'email à partir du regex
            return 4  # 4 = l'user a fait une erreur d'email

        if not password:
            return 5  # 5 = pas de mot de passe
        if not (3 <= len(password) <= 14):
            return 6  # 6= mauvaise taille de mot de passe

        self.reponse = 7  # 7 il n'y a pas de majuscule
        for cara in password:
            if cara.isalpha():
                if cara.isupper():
                    self.reponse = 0
        return self.reponse

    def validation_register(self, username, email, password):
        """    
        Une autre vérification sur si les informations sont déjà utilisées quelque part (dans la base de donnée)
        """
        try:
            #on se connecte à la base de donnée
            self.connexion = sqlite3.connect("database.db")
            self.cursor = self.connexion.cursor()
            self.infos = self.cursor.execute("SELECT pseudo, email FROM users").fetchall()
            for personnes in self.infos:
                if username == personnes[0]:
                    return 1
                if email == personnes[1]:
                    return 2

            self.cursor.execute("INSERT INTO users (pseudo, email, password) VALUES (?, ?, ?)",
                                (username, email, password))
            self.connexion.commit()
            self.connexion.close()
            return 0

        #utiliser pour le deboggage
        except Exception as e:
            print(f"Numéro 1 dans validation register : {e}")

    def login(self):
        self.fenetre_login = tkinter.Tk()
        self.fenetre_login.geometry(f"400x500+{self.fenetre_login.winfo_screenwidth() // 2 - 250}+"
                                    f"{self.fenetre_login.winfo_screenheight() // 2 - 200}")
        self.fenetre_login.title("Login -*- Aeditoryre")
        self.fenetre_login.resizable(width=False, height=False)
        self.fenetre_login["bg"] = "#141B33"

        self.login_separator1 = tkinter.Label(self.fenetre_login, bg="#141B33", width=40)
        self.login_separator1.grid(row=0, column=0, sticky=tkinter.W + tkinter.E, padx=60)

        self.login_email_label = tkinter.Label(self.fenetre_login, width=35, height=1,
                                               text="Entrez votre adresse email:")
        self.login_email_label.grid(row=1, column=0, pady=5)
        self.login_email_entry = tkinter.Entry(self.fenetre_login, width=41)
        self.login_email_entry.grid(row=2, column=0)

        self.login_separator2 = tkinter.Label(self.fenetre_login, bg="#141B33", width=40, height=4)
        self.login_separator2.grid(row=3, column=0)

        self.login_password_label = tkinter.Label(self.fenetre_login, width=35, height=1,
                                                  text="Entrez votre mot de passe:")
        self.login_password_label.grid(row=4, column=0, pady=5)
        self.login_password_entry = tkinter.Entry(self.fenetre_login, width=41, show="*")
        self.login_password_entry.grid(row=5, column=0)

        self.button_login = tkinter.Button(self.fenetre_login, width=20, height=4,
                                           text="SE CONNECTER", command=self.authentification_login)
        self.fenetre_login.bind("<Return>", self.authentification_login)
        self.button_login.grid(row=6, column=0, pady=40)

        self.fenetre_login.protocol("WM_DELETE_WINDOW", self.returnItemLogin)
        self.fenetre_login.mainloop()

    def returnItemLogin(self):

        self.request = False
        self.fenetre_login.destroy()
        self.fenetre_login.quit()

    def authentification_login(self, *args):
        self.email_login = self.login_email_entry.get()
        self.password_login = self.login_password_entry.get()
        self.result_login = self.existing_infos_login(self.email_login, self.password_login);

        if self.label_created_login:
            self.message_erreur_login.destroy()
        self.label_created_login = True
        self.message_erreur_login = tkinter.Label(self.fenetre_login, font=("Arial", 10), bg="#141B33", fg="#DC143C")

        if self.result_login == 1:  # absence d'email
            self.message_erreur_login["text"] = "vous devez saisir un email"
            self.message_erreur_login.grid(row=3, column=0, sticky=tkinter.N)
        elif self.result_login == 2:  # absence de mot de passe
            self.message_erreur_login["text"] = "vous devez saisir un mot de passe"
            self.message_erreur_login.grid(row=6, column=0, sticky=tkinter.N)

        elif self.result_login == 3: #mauvais identifiants
            self.message_erreur_login["text"] = "les informations sont incorrectes"
            self.message_erreur_login.grid(row=8, column=0)

        elif self.result_login == 0: #pas erreur
            self.message_fin_login = tkinter.Label(self.fenetre_login, bg="#141B33", fg="#A39DD6",
                                            text="Connexion réussie !\nVeuillez retourner à l'accueil pour continuer à programmer")
            self.message_fin_login.grid(row=8, column=0)
            self.label_created_login = False


            self.connexion = sqlite3.connect("database.db")
            self.cursor = self.connexion.cursor()
            self.request = self.cursor.execute("SELECT * FROM users WHERE email = ?", (self.email_login,)).fetchall()[0]

            self.fenetre_login.destroy()
            self.fenetre_login.quit()

    def existing_infos_login(self, email, password):
        if not email:
            return 1  # abscence d'email

        if not password:
            return 2  # abscence de mot de passe
        try:
            self.connexion = sqlite3.connect("database.db")
            self.cursor = self.connexion.cursor()
            self.infos = self.cursor.execute("SELECT email, password FROM users").fetchall()
            self.connexion.close()

            for infos in self.infos:
                if email == infos[0] and password == infos[1]:
                    return 0  # tout est bon
            return 3  # l'user n'a pas saisi les bonnes infos

        except Exception as e:
            return 4