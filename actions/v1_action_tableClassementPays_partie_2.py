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
            #requete sql pour obtenir tout les pays
            result = cursor.execute("WITH Pays AS (SELECT DISTINCT pays FROM LesSportifs),"
                                     "nbOS AS (SELECT pays, COUNT(medailleOr) AS NO FROM LesEpreuves "
                                     "JOIN LesSportifs ON (numSp = medailleOr) GROUP BY pays),"
                                     "nbOE AS (SELECT paysEQ, COUNT(medailleOr) AS NOE FROM LesEpreuves "
                                     "JOIN LesEquipes ON (medailleOr = numEq) GROUP BY paysEQ),"
                                     "nbAS AS (SELECT pays, COUNT(medailleArgent) AS NA FROM LesEpreuves "
                                     "JOIN LesSportifs ON (numSp = medailleArgent) GROUP BY pays),"
                                     "nbAE AS (SELECT paysEQ, COUNT(medailleArgent) AS NAE FROM LesEpreuves "
                                     "JOIN LesEquipes ON (medailleArgent = numEq) GROUP BY paysEQ),"
                                     "nbBS AS (SELECT pays, COUNT(medailleBronze) AS NB FROM LesEpreuves "
                                     "JOIN LesSportifs ON (numSp = medailleBronze) GROUP BY pays),"
                                     "nbBE AS (SELECT paysEQ, COUNT(medailleBronze) AS NBE FROM LesEpreuves "
                                     "JOIN LesEquipes ON (medailleBronze = numEq) GROUP BY paysEQ)"
                                     "SELECT Pays.pays, ifnull(NO,0) + ifnull(NOE,0) AS nbO, "
                                     "ifnull(NA,0) + ifnull(NAE,0) AS nbA, ifnull(NB,0) + ifnull(NBE,0) AS nbB,"
                                     "ifnull(NO,0) + ifnull(NOE,0) + ifnull(NA,0) + ifnull(NAE,0) "
                                     "+ ifnull(NB,0) + ifnull(NBE,0) AS nbM "
                                     "FROM Pays "
                                     "LEFT JOIN nbOS USING (pays) LEFT JOIN (nbOE) ON(pays =nbOE.paysEQ)"
                                     "LEFT JOIN nbAS USING (pays) LEFT JOIN (nbAE) ON(pays =nbAE.paysEQ)"
                                     "LEFT JOIN nbBS USING (pays) LEFT JOIN (nbBE) ON(pays =nbBE.paysEQ)"
                                     "ORDER BY nbM DESC,nbO DESC, nbA DESC, nbB DESC;")

        except Exception as e:
            display.refreshLabel(self.ui.label_tableClassementPays, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericData(self.ui.tableClassementPaysV1, result)
