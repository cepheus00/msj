from tkinter import *
from getpass import *
import socket, sys, threading, hashlib

pseudo = input("Entrez votre pseudo : ")
host = input("Entrez l'adresse IP du serveur : ")
port = 12800
password = getpass("Entrez le mot de passe du serveur : ")
password = password.encode()
password = hashlib.sha1(password).hexdigest()

connexion = socket.socket()

class ThreadReception(threading.Thread):
    """objet thread gérant la réception des messages"""
    def __init__(self, connexion):
        threading.Thread.__init__(self)
        self.connexion = connexion

    def run(self):
        while 1:
            try:
                message_recu = self.connexion.recv(1024)
            except:
                messages.insert('end', "Connexion avec le serveur perdue...")
                break
            message_recu = message_recu.decode()
            messages.insert('end', message_recu)

def envoyer(texteEntree, messages, pseudo, connexion):
    message = texteEntree.get()
    texteEntree.set('')
    if message != '' and message != "Entrez votre message ici...":
        messages.insert('end', "%s : %s" % (pseudo, message))
        try:
            connexion.send(message.encode())
        except:
            messages.insert('end', "Connexion avec le serveur perdue...")

#Initialisation de la fenêtre
fenetre = Tk()
fenetre.geometry("720x480")
fenetre.title("%s@%s - MSJ"%(pseudo, host))
fenetre.iconbitmap(r'icon.ico')

panneau = PanedWindow(fenetre, orient=VERTICAL)

panneau.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)

messages = Listbox(panneau)
panneau.add(messages, height=380)

texteEntree = StringVar()
texteEntree.set("Entrez votre message ici...")
entreeMessage = Entry(panneau, textvariable=texteEntree, width=200)
panneau.add(entreeMessage, height=50)

boutonEnvoi = Button(panneau, text="Envoyer", command= lambda: envoyer(texteEntree, messages, pseudo, connexion))
boutonEnvoi.pack(side=RIGHT)
panneau.add(boutonEnvoi, height=50)

panneau.pack()

#Établissement de la connexion :
connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    connexion.connect((host, port))
except socket.error:
    messages.insert('end', "La connexion a échoué.")
    sys.exit()
messages.insert('end', "Connexion établie avec le serveur.")

connexion.send(pseudo.encode()) #Envoi du pseudo
connexion.send(password.encode()) #Envoi du mot de passe

#Lancement de l'écoute
th_R = ThreadReception(connexion)
th_R.start()
fenetre.mainloop()
