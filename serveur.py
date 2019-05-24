HOST = "localhost"
PORT = 12800

import socket, sys, threading, hashlib
from getpass import getpass

class ThreadClient(threading.Thread):
    '''dérivation d'un objet thread pour gérer la connexion avec un client'''
    def __init__(self, conn, nom):
        threading.Thread.__init__(self)
        self.connexion = conn
        self.nom = nom
        
    def run(self):
        # Dialogue avec le client :
        while 1:
            try:
                msgClient = self.connexion.recv(1024)
            except:
                self.connexion.close()
                del conn_client[self.nom]
                print("Client %s déconnecté" % self.nom)
                for cle in conn_client:
                    if cle != self.nom:      # ne pas le renvoyer à l'émetteur
                        messageDeconnexion = "** %s s'est déconnecté **" % self.nom
                        conn_client[cle].send(messageDeconnexion.encode())
                break
            msgClient = msgClient.decode()
            message = "%s : %s" % (self.nom, msgClient)
            print(message)
            # Faire suivre le message à tous les autres clients :
            for cle in conn_client:
                if cle != self.nom:      # ne pas le renvoyer à l'émetteur
                    conn_client[cle].send(message.encode())

# Initialisation du serveur - Mise en place du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    mySocket.bind((HOST, PORT))
except socket.error:
    print("La liaison du socket à l'adresse choisie a échoué.")
    sys.exit()
print("Serveur prêt, en attente de requêtes ...")
mySocket.listen(5)

# Attente et prise en charge des connexions demandées par les clients :
conn_client = {}                # dictionnaire des connexions clients
while 1:    
    connexion, adresse = mySocket.accept()
    it = connexion.recv(1024).decode()

    # Créer un nouvel objet thread pour gérer la connexion :
    th = ThreadClient(connexion, it)
    th.start()
    # Mémoriser la connexion dans le dictionnaire : 
    conn_client[it] = connexion
    print("Client %s connecté, adresse IP %s, port %s." % (it, adresse[0], adresse[1]))
    # Dialogue avec le(s) client(s) :
    for cle in conn_client:
        messageConnexion = "** %s s'est connecté **" % it
        conn_client[cle].send(messageConnexion.encode())
        if cle != it:
            messageConnectes = "** %s est connecté **" % cle
            conn_client[it].send(messageConnectes.encode())
