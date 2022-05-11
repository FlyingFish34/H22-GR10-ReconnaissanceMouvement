import requests
import json

#Objet qui contrôle la lumière connectée LIFX
class LightController:
    def __init__(self):
        #Load l'API KEY et le Bulb Label depuis un fichier JSON
        with open('./SavedSettings.json', 'r') as f:
            self.donneesSauvegardees = json.load(f)
            f.close()
        self.tokenAPI = str(self.donneesSauvegardees['apiKey'])
        self.headers = {"Authorization": "Bearer %s" % self.tokenAPI,}
        self.label = str(self.donneesSauvegardees['bulbLabel'])
        self.urlLumiere = 'https://api.lifx.com/v1/lights/label:' + self.label + '/state'
        self.luminosite = 0.7

    def allumerAmpoule(self):
        payload = {"power": "on",
                   "color" : "white",}
        response = requests.put(self.urlLumiere, data=payload, headers=self.headers)

    def eteindreAmpoule(self):
        payload = {"power": "off",}
        response = requests.put(self.urlLumiere, data=payload, headers=self.headers)

    #Petite méthode blague qui allume la lumière en rouge
    def easterEgg(self):
        payload = {"color": "red", }
        response = requests.put(self.urlLumiere, data=payload, headers=self.headers)

    #Méthode qui sauvegarde l'API KEY de l'utilisateur dans un fichier JSON pour les utilisations suivantes
    def changerApiKey(self, newApiKey):
        with open('./SavedSettings.json', 'r') as f:
            donnees = json.load(f)
        donnees['apiKey'] = newApiKey
        self.headers = {"Authorization": "Bearer %s" % newApiKey,}
        with open('./SavedSettings.json', 'w') as f:
            json.dump(donnees, f)
            f.close()

    #Méthode qui sauvegarde le Bulb Label de l'utilisateur dans un fichier JSON pour les utilisations suivantes
    def changerBulbLabel(self, newBulbLabel):
        with open('./SavedSettings.json', 'r') as f:
            donnees = json.load(f)
        donnees['bulbLabel'] = newBulbLabel
        self.urlLumiere = 'https://api.lifx.com/v1/lights/label:' + newBulbLabel + '/state'
        with open('./SavedSettings.json', 'w') as f:
            json.dump(donnees, f)
            f.close()

    #Méthode qui change la luminosité de l'ampoule
    def changerLuminosité(self,monterLuminosite):
        if monterLuminosite :
            self.luminosite = self.luminosite + 0.1
            if self.luminosite > 1.0 :
                self.luminosite = 1.0
        elif not monterLuminosite :
            self.luminosite = self.luminosite - 0.1
            if self.luminosite < 0:
                self.luminosite = 0
        payload = {"brightness": self.luminosite, }
        response = requests.put(self.urlLumiere, data=payload, headers=self.headers)