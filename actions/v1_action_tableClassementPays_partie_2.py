import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic


# Classe permettant d'afficher la fonction fournie 1
class AppTableClassementPaysV1(QDialog):

    # Constructeur
    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/v1_tableClassementPays.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):

        display.refreshLabel(self.ui.label_tableClassementPays, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT numEq, 1, 1, 1, 3 FROM LesEquipes")
        except Exception as e:
            self.ui.label_tableClassementPays.setRowCount(0)
            display.refreshLabel(self.ui.label_tableClassementPays, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericData(self.ui.tableClassementPaysV1, result)
