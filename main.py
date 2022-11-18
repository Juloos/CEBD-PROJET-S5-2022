
import sys, sqlite3
from utils import db
from utils import display
from utils import excel_extractor
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
from actions.v0_action_tablesData import AppTablesDataV0
from actions.v1_action_tablesData import AppTablesDataV1
from actions.v0_action_fct_fournie_1_partie_0 import AppFctFournie1Partie0
from actions.v0_action_fct_fournie_2_partie_0 import AppFctFournie2Partie0
from actions.v0_action_fct_comp_1_partie_1 import AppFctComp1Partie1
from actions.v0_action_fct_comp_2_partie_1 import AppFctComp2Partie1

# Classe utilisée pour lancer la fenêtre principale de l'application et définir ses actions
class AppWindow(QMainWindow):

    # Création d'un signal destiné à être émis lorsque la table est modifiée
    changedValue = pyqtSignal()

    # TODO 2 : ajouter les fenetres (répertoire gui) et les actions (répertoire actions) correspondant aux 2 items de la partie 2.
    # TODO 3 : ajouter les fenetres (rep. gui) et les actions (rep. actions) correspondant aux 2 items de la partie 3.

    # On prévoit des variables pour accueillir les fenêtres supplémentaires
    tablesDataDialogV0 = None
    tablesDataDialogV1 = None
    fct_fournie_1_dialog = None
    fct_fournie_2_dialog = None
    fct_comp_1_dialog = None
    fct_comp_2_dialog = None

    # Constructeur
    def __init__(self):

        # On appelle le constructeur de la classe dont on hérite
        super(AppWindow, self).__init__()

        # On charge le gui de la fenêtre
        self.ui = uic.loadUi("gui/mainWindow.ui", self)

        # On se connecte à la base de données
        self.data = sqlite3.connect("data/jo.db")

    ####################################################################################################################
    # Définition des actions
    ####################################################################################################################

        ###################################### Actions BD V0 (ne pas toucher) #######################################

        # Action en cas de clic sur le bouton de création de base de données (V0)
    def createDBV0(self):

        try:
            # On exécute les requêtes du fichier de création
            db.updateDBfile(self.data, "data/v0_createDB.sql")

        except Exception as e:
            # En cas d'erreur, on affiche un message
            display.refreshLabel(self.ui.label_retour_BD, "L'erreur suivante s'est produite pendant lors de la création de la base : "+repr(e)+".")

        else:
            # Si tout s'est bien passé, on affiche le message de succès et on commit
            display.refreshLabel(self.ui.label_retour_BD, "La base de données a été créée avec succès.")
            self.data.commit()
            # On émet le signal indiquant la modification de la table
            self.changedValue.emit()

    # En cas de clic sur le bouton d'insertion de données
    def insertDBV0(self):

        try:
            # on lit les données dans le fichier Excel
            excel_extractor.read_excel_file_V0(self.data, "data/LesJO.xlsx")

        except Exception as e:
            # En cas d'erreur, on affiche un message
            display.refreshLabel(self.ui.label_retour_BD, "L'erreur suivante s'est produite lors de l'insertion des données : "+repr(e)+".")

        else:
            # Si tout s'est bien passé, on affiche le message de succès et on commit
            display.refreshLabel(self.ui.label_retour_BD, "Un jeu de test a été inséré dans la base avec succès.")
            self.data.commit()
            # On émet le signal indiquant la modification de la table
            self.changedValue.emit()

    # En cas de clic sur le bouton de suppression de la base
    def deleteDBV0(self):

        try:
            # On exécute les requêtes du fichier de suppression
            db.updateDBfile(self.data, "data/v0_deleteDB.sql")

        except Exception as e:
            # En cas d'erreur, on affiche un message
            display.refreshLabel(self.ui.label_retour_BD, "Erreur lors de la suppression de la base de données : " + repr(e)+".")

        else:
            # Si tout s'est bien passé, on affiche le message de succès (le commit est automatique pour un DROP TABLE)
            display.refreshLabel(self.ui.label_retour_BD, "La base de données a été supprimée avec succès.")
            # On émet le signal indiquant la modification de la table
            self.changedValue.emit()

    ###################################### Actions BD V1 #######################################

        # Action en cas de clic sur le bouton de création de base de données (V1)
    def createDBV1(self):

        try:
            # On exécute les requêtes du fichier de création
            db.updateDBfile(self.data, "data/v1_createDB.sql")

        except Exception as e:
             # En cas d'erreur, on affiche un message
            display.refreshLabel(self.ui.label_retour_BD,
                                  "L'erreur suivante s'est produite pendant lors de la création de la base V1: " + repr(
                                      e) + ".")

        else:
            # Si tout s'est bien passé, on affiche le message de succès et on commit
            display.refreshLabel(self.ui.label_retour_BD, "La base de données V1 a été créée avec succès.")
            self.data.commit()
            # On émet le signal indiquant la modification de la table
            self.changedValue.emit()

    # En cas de clic sur le bouton d'insertion de données
    def insertDBV1(self):

        try:
            # on lit les données dans le fichier Excel
            excel_extractor.read_excel_file_V1(self.data, "data/LesJO.xlsx")

        except Exception as e:
            # En cas d'erreur, on affiche un message
            display.refreshLabel(self.ui.label_retour_BD, "L'erreur suivante s'est produite lors de l'insertion des données V1 : "+repr(e)+".")

        else:
            # Si tout s'est bien passé, on affiche le message de succès et on commit
            display.refreshLabel(self.ui.label_retour_BD, "Un jeu de test V1 a été inséré dans la base avec succès.")
            self.data.commit()
            # On émet le signal indiquant la modification de la table
            self.changedValue.emit()

    # Action en cas de clic sur le bouton de création de triggers base de données (V1)
    def createTriggersDBV1(self):

        try:
            # On exécute les requêtes du fichier de création
            db.updateDBfile(self.data, "data/v1_createTriggers.sql", True)

        except Exception as e:
            # En cas d'erreur, on affiche un message
            display.refreshLabel(self.ui.label_retour_BD,
                                 "L'erreur suivante s'est produite pendant lors de la création des triggers de la base V1: " + repr(
                                     e) + ".")

        else:
            # Si tout s'est bien passé, on affiche le message de succès et on commit
            display.refreshLabel(self.ui.label_retour_BD, "Les triggers de la base de données V1 ont été créés avec succès.")
            self.data.commit()
            # On émet le signal indiquant la modification de la table
            self.changedValue.emit()

    # En cas de clic sur le bouton de suppression de la base
    def deleteDBV1(self):

        try:
            # On exécute les requêtes du fichier de suppression
            db.updateDBfile(self.data, "data/v1_deleteDB.sql")

        except Exception as e:
            # En cas d'erreur, on affiche un message
            display.refreshLabel(self.ui.label_retour_BD, "Erreur lors de la suppression de la base de données V1: " + repr(e)+".")

        else:
            # Si tout s'est bien passé, on affiche le message de succès (le commit est automatique pour un DROP TABLE)
            display.refreshLabel(self.ui.label_retour_BD, "La base de données V1 a été supprimée avec succès.")
            # On émet le signal indiquant la modification de la table
            self.changedValue.emit()

    ####################################################################################################################
    # Ouverture des autres fenêtres de l'application
    ####################################################################################################################

    # TODO 2 : ajouter la définition des méthodes déclenchées lors des clicks sur les boutons de la partie 2
    # TODO 3 : ajouter la définition des méthodes déclenchées lors des clicks sur les boutons de la partie 3

    # En cas de clic sur le bouton de visualisation des données
    def openDataV0(self):
        if self.tablesDataDialogV0 is not None:
            self.tablesDataDialogV0.close()
        self.tablesDataDialogV0 = AppTablesDataV0(self.data)
        self.tablesDataDialogV0.show()
        self.changedValue.connect(self.tablesDataDialogV0.refreshAllTablesV0)

    def openDataV1(self):
        if self.tablesDataDialogV1 is not None:
            self.tablesDataDialogV1.close()
        self.tablesDataDialogV1 = AppTablesDataV1(self.data)
        self.tablesDataDialogV1.show()
        self.changedValue.connect(self.tablesDataDialogV1.refreshAllTablesV1)

    # En cas de clic sur la fonction fournie 1
    def open_fct_fournie_1(self):
        if self.fct_fournie_1_dialog is not None:
            self.fct_fournie_1_dialog.close()
        self.fct_fournie_1_dialog = AppFctFournie1Partie0(self.data)
        self.fct_fournie_1_dialog.show()
        self.changedValue.connect(self.fct_fournie_1_dialog.refreshResult)

    # En cas de clic sur la fonction fournie 2
    def open_fct_fournie_2(self):
        if self.fct_fournie_2_dialog is not None:
            self.fct_fournie_2_dialog.close()
        self.fct_fournie_2_dialog = AppFctFournie2Partie0(self.data)
        self.fct_fournie_2_dialog.show()

    # En cas de clic sur la fonction à compléter 1
    def open_fct_comp_1(self):
        if self.fct_comp_1_dialog is not None:
            self.fct_comp_1_dialog.close()
        self.fct_comp_1_dialog = AppFctComp1Partie1(self.data)
        self.fct_comp_1_dialog.show()
        self.changedValue.connect(self.fct_comp_1_dialog.refreshResult)

    # En cas de clic sur la fonction à compléter 2
    def open_fct_comp_2(self):
        if self.fct_comp_2_dialog is not None:
            self.fct_comp_2_dialog.close()
        self.fct_comp_2_dialog = AppFctComp2Partie1(self.data)
        self.fct_comp_2_dialog.show()

    ####################################################################################################################
    # Fonctions liées aux évènements (signal/slot/event)
    ####################################################################################################################

    # TODO 2 : penser à fermer correctement les fenêtres de la partie 2
    # TODO 3 : penser à fermer correctement il faut les fenêtres de la partie 3

    # On intercepte l'évènement de cloture de la fenêtre principale pour intercaler quelques actions avant sa fermeture
    def closeEvent(self, event):

        # On ferme les éventuelles fenêtres encore ouvertes
        if (self.tablesDataDialogV0 is not None):
            self.tablesDataDialogV0.close()
        if (self.tablesDataDialogV1 is not None):
            self.tablesDataDialogV1.close()
        if (self.fct_fournie_1_dialog is not None):
            self.fct_fournie_1_dialog.close()
        if (self.fct_fournie_2_dialog is not None):
            self.fct_fournie_2_dialog.close()
        if (self.fct_comp_1_dialog is not None):
            self.fct_comp_1_dialog.close()
        if (self.fct_comp_2_dialog is not None):
            self.fct_comp_2_dialog.close()

        # On ferme proprement la base de données
        self.data.close()

        # On laisse l'évènement de clôture se terminer normalement
        event.accept()

# Lancement de la fenêtre principale
app = QApplication(sys.argv)
MainWindow = AppWindow()
MainWindow.show()
sys.exit(app.exec_())