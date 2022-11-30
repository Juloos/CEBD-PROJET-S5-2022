import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic


# Classe permettant d'afficher la fenêtre de visualisation des données
class AppTablesDataV1(QDialog):

    # Constructeur
    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/v1_tablesData.ui", self)
        self.data = data

        # On met à jour l'affichage avec les données actuellement présentes dans la base
        self.refreshAllTablesV1()

    ####################################################################################################################
    # Méthodes permettant de rafraichir les différentes tables
    ####################################################################################################################

    # Fonction de mise à jour de l'affichage d'une seule table
    def refreshTable(self, label, table, query):
        display.refreshLabel(label, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            table.setRowCount(0)
            display.refreshLabel(label, "Impossible d'afficher les données de la table : " + repr(e))
        else:
            display.refreshGenericData(table, result)

    # Fonction permettant de mettre à jour toutes les tables
    @pyqtSlot()
    def refreshAllTablesV1(self):

        self.refreshTable(self.ui.label_epreuves, self.ui.tableEpreuves,
                          "SELECT numEp, nomEp, formeEp, nomDi, categorieEp, "
                          "ifnull(nbSportifsEp, 0), dateEp, MedailleOr, MedailleArgent, MedailleBronze "
                          "FROM LesEpreuves ORDER BY numEp")
        self.refreshTable(self.ui.label_sportifs, self.ui.tableSportifs,
                          "SELECT numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp, ageSp "
                          "FROM LesSportifs JOIN LesAgesSportifs USING (numSp) ORDER BY numSp")


        self.refreshTable(self.ui.label_equipes, self.ui.tableEquipes,
                            "SELECT numEq, paysEq FROM LesEquipes ORDER BY numEq")
        self.refreshTable(self.ui.label_disciplines, self.ui.tableDisciplines,
                          "SELECT nomDi FROM LesDisciplines ORDER BY nomDi")
        self.refreshTable(self.ui.label_participants, self.ui.tableParticipants,
                          "SELECT num FROM LesParticipants ORDER BY num")
        self.refreshTable(self.ui.label_participations, self.ui.tableParticipations,
                            "SELECT num, numEp FROM LesParticipations ORDER BY num")
        self.refreshTable(self.ui.label_a, self.ui.tableA,
                            "SELECT nomDi, numEp  FROM A ORDER BY nomDi")
        self.refreshTable(self.ui.label_equipiers, self.ui.tableEquipiers,
                          "SELECT numEq, numSp FROM LesEquipiers ORDER BY numEq"),

        self.refreshTable(self.ui.label_agesSportifs, self.ui.tableAgesSportifs,
                          "SELECT numSp, ageSp FROM LesAgesSportifs ORDER BY numSp")
        self.refreshTable(self.ui.label_nbEquipiers, self.ui.tableNbEquipiers,
                          "SELECT numEq, nbEquipiers FROM LesNbsEquipiers ORDER BY numEq")
