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
            result = cursor.execute(
                "WITH LesPaysParticipants AS ("
                "    SELECT numSp AS num, pays FROM LesSportifs"
                "    UNION"
                "    SELECT numEq AS num, pays FROM LesEquipes"
                "), LesPays AS ("
                "    SELECT DISTINCT pays FROM LesPaysParticipants"
                "), LesNbsMedailleOr AS ("
                "    SELECT pays, COUNT(medailleOr) AS nbOr"
                "        FROM LesEpreuves JOIN LesPaysParticipants ON (num = medailleOr)"
                "        GROUP BY pays"
                "), LesNbsMedailleArgent AS ("
                "    SELECT pays, COUNT(medailleArgent) AS nbArgent"
                "        FROM LesEpreuves JOIN LesPaysParticipants ON (num = medailleArgent)"
                "        GROUP BY pays"
                "), LesNbsMedailleBronze AS ("
                "    SELECT pays, COUNT(medailleBronze) AS nbBronze"
                "        FROM LesEpreuves JOIN LesPaysParticipants ON (num = medailleBronze)"
                "        GROUP BY pays"
                ")"
                "SELECT pays, ifnull(nbOr, 0) AS nbOr, ifnull(nbArgent, 0) AS nbArgent, ifnull(nbBronze, 0) AS nbBronze,"
                "        ifnull(nbOr, 0) + ifnull(nbArgent, 0) + ifnull(nbBronze, 0) AS nbTot"
                "    FROM LesPays"
                "        LEFT JOIN LesNbsMedailleOr USING (pays)"
                "        LEFT JOIN LesNbsMedailleArgent USING (pays)"
                "        LEFT JOIN LesNbsMedailleBronze USING (pays)"
                "    ORDER BY nbTot DESC, nbOr DESC, nbArgent DESC, nbBronze DESC"
            )

        except Exception as e:
            display.refreshLabel(self.ui.label_tableClassementPays, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericData(self.ui.tableClassementPaysV1, result)
