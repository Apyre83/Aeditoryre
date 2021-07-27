#coding:UTF-8

from fenetre import Fenetre
import threading, time
import tkinter

class Main(threading.Thread): #classe principale
    def __init__(self): #fonction d'initialisation
        threading.Thread.__init__(self) #création du Thread (processus qui gère tout)

        self.touchesAuto = {"parenleft": ")", "quotedbl": '"', "quoteright": "'"} #pour gérer les events (voir ligne 27)

        self.counting_decal = 0 #sert à compter les alinéas à faire afin de faciliter l'utilisateur
        self.counting_space = 0
        self.counting_tabs = 0

    def start(self, parent): #fonction qui est nécessaire lorsque on hérite de Thread
        
        self.parent = Fenetre()
        self.parent.start(parent)
        self.parent.mainText.bind("<KeyPress>", self.allThreads) #A AJOUTER L'AUTRE

        self.parent.xScrollBarMainText.bind("<Button-1>", self.allThreads)
        self.parent.mainText.bind("<Button-1>", self.allThreads)
        self.parent.mainText.bind("<MouseWheel>", self.allThreads)
        self.parent.mainText.bind("<Return>", self.allThreads)

    def allThreads(self, *args):
        if "keysym" in dir(args[0]): #c'est un event tkinter clavier
            if args[0].keysym in self.touchesAuto:  # on teste si si c'est un event tkinter clavier avec args[0].keysym, puis on regarde si
                self.ThreadAutoTouches = threading.Thread(target=self.threadTouches, args=(args[0],))
                self.ThreadAutoTouches.start()

            elif args[0].keysym == "Return":
                #partie où retour à la ligne
                self.ThreadAlineasText = threading.Thread(target=self.alineasText)
                self.ThreadAlineasText.start()


        self.ThreadLinesCounting = threading.Thread(target=self.threadLines)
        self.ThreadLinesCounting.start()

    def alineasText(self):


        i = self.parent.mainText.index("@0,0")
        while True:
            dline = self.parent.mainText.dlineinfo(i)
            if dline is None:
                break
            i = self.parent.mainText.index("%s+1line" % i)

        self.nbLignes = int(str(i).split(".")[0])
        self.lastLigne = self.parent.mainText.get("%s.0" % (self.nbLignes - 2), tkinter.END)


        self.counting_space, self.counting_tabs = 0, 0

        for i in range(len(self.lastLigne)):
            if self.lastLigne[i] == " ":
                self.counting_space += 1

            elif self.lastLigne[i] == "\t":
                self.counting_tabs += 1

            else:
                break


        if len(self.lastLigne) <= 2:  # si une ligne du self.mainText est censée être vide, la longueur est de 2, et
            # la chaine de cara est 2 * "\n"
            return


        #une tabulation = 6 espaces
        self.counting_decal = int(self.counting_tabs + self.counting_space // 6)
        if self.lastLigne[-3] == ":": #si il termine par ":" -> condition
            self.counting_decal += 1

        self.parent.mainText.insert(tkinter.INSERT, "".join(["\t" for _ in range(self.counting_decal)]))
        self.parent.mainText.mark_set(tkinter.INSERT, "%d.%d" % (self.nbLignes, self.counting_decal))

    def threadLines(self):
        time.sleep(0.01)

        def actualiser_text(liste):
            self.parent.countingLinesMainText.config(text="".join(liste))

        self.parent.countingLinesMainText.config(text="")
        lignes = []
        i = self.parent.mainText.index("@0,0")

        while True:
            dline = self.parent.mainText.dlineinfo(i)
            if dline is None:
                break

            linenum = str(i).split(".")[0]
            if lignes == []:
                lignes.append("%s" % linenum)
            else:
                lignes.append("\n%s" % linenum)
            i = self.parent.mainText.index("%s+1line" % i)

        actualiser_text(lignes)

    def threadTouches(self, touche):
        time.sleep(0.01) #pour le décalage

        self.parent.mainText.insert(tkinter.INSERT, self.touchesAuto[touche.keysym])
        self.posMouse = self.parent.mainText.index(tkinter.INSERT).split(".")
        self.parent.mainText.mark_set(tkinter.INSERT, "%d.%d" % (int(self.posMouse[0]), int(self.posMouse[1]) - 1))



if __name__ == "__main__":
    root = tkinter.Tk()
    client = Main()
    client.start(root)
    client.parent.mainloop()



