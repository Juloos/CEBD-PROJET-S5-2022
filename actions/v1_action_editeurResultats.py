import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic


# Classe permettant d'afficher la fenêtre de visualisation des données
class AppEditeurResultatsV1(QDialog):

    # Constructeur
    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/v1_editeurResultats.ui", self)
        self.data = data

        # attribuer les valeurs aux comboBox
        # les contraintes d'intégrité suivantes ne sont pas prises en compte dans la conception de l'interface :
        #   - les participants d'une épreuve doivent être du genre que la catégorie de l'épreuve comprend
        #   - le type des participants (individuel ou équipe) doit être le même que celui de l'épreuve
        self.refreshAll()

    def tryquery(self, query):
        try:
            # print(query)
            return self.data.cursor().execute(query)
        except sqlite3.Error as err:
            display.refreshLabel(
                self.ui.label_editeurResultats,
                "Impossible d'effectuer la requête dans la DB : " + repr(err)
            )
            return None

    def numEp_get1(self):
        return self.ui.numEp_comboBox1.currentText()

    def numEp_get2(self):
        return self.ui.numEp_comboBox2.currentText()

    def or_get1(self):
        return self.ui.medailleOr_comboBox1.currentText()

    def or_get2(self):
        return self.ui.medailleOr_comboBox2.currentText()

    def argent_get1(self):
        return self.ui.medailleArgent_comboBox1.currentText()

    def argent_get2(self):
        return self.ui.medailleArgent_comboBox2.currentText()

    def bronze_get1(self):
        return self.ui.medailleBronze_comboBox1.currentText()

    def bronze_get2(self):
        return self.ui.medailleBronze_comboBox2.currentText()

    def refreshNumEpComboBox1(self):
        self.ui.medailleOr_comboBox1.clear()
        self.ui.medailleArgent_comboBox1.clear()
        self.ui.medailleBronze_comboBox1.clear()

        for num, *_ in self.tryquery(
                "SELECT num FROM LesParticipations WHERE numEp = {} ORDER BY num".format(self.numEp_get1())
        ):
            self.ui.medailleOr_comboBox1.addItem(str(num))
            self.ui.medailleArgent_comboBox1.addItem(str(num))
            self.ui.medailleBronze_comboBox1.addItem(str(num))

        self.ui.medailleOr_comboBox1.setCurrentIndex(0)
        self.ui.medailleArgent_comboBox1.setCurrentIndex(1)
        self.ui.medailleBronze_comboBox1.setCurrentIndex(2)

    def refreshNumEpComboBox2(self):
        self.ui.medailleOr_comboBox2.clear()
        self.ui.medailleArgent_comboBox2.clear()
        self.ui.medailleBronze_comboBox2.clear()

        for num, *_ in self.tryquery(
                "SELECT num FROM LesParticipations WHERE numEp = {} ORDER BY num".format(self.numEp_get2())
        ):
            self.ui.medailleOr_comboBox2.addItem(str(num))
            self.ui.medailleArgent_comboBox2.addItem(str(num))
            self.ui.medailleBronze_comboBox2.addItem(str(num))

        old_or = self.tryquery("SELECT medailleOr FROM LesEpreuves WHERE numEp = {}".format(self.numEp_get2()))
        old_argent = self.tryquery("SELECT medailleArgent FROM LesEpreuves WHERE numEp = {}".format(self.numEp_get2()))
        old_bronze = self.tryquery("SELECT medailleBronze FROM LesEpreuves WHERE numEp = {}".format(self.numEp_get2()))

        self.ui.medailleOr_comboBox2.setCurrentText(str(old_or.fetchone()[0]))
        self.ui.medailleArgent_comboBox2.setCurrentText(str(old_argent.fetchone()[0]))
        self.ui.medailleBronze_comboBox2.setCurrentText(str(old_bronze.fetchone()[0]))

    def refreshMedailleOrComboBox1(self):
        itemlist = self.tryquery(
            "SELECT num FROM LesParticipations WHERE numEp = {} ORDER BY num".format(self.numEp_get1())
        )
        if itemlist is not None:
            itemlist = set(map(lambda numtuple: numtuple[0], itemlist.fetchall()))
            if self.or_get1() == self.argent_get1():
                self.ui.medailleArgent_comboBox1.setCurrentText(
                    str((itemlist - {int(self.or_get1()), int(self.bronze_get1())}).pop())
                )
            if self.or_get1() == self.bronze_get1():
                self.ui.medailleBronze_comboBox1.setCurrentText(
                    str((itemlist - {int(self.or_get1()), int(self.argent_get1())}).pop())
                )

    def refreshMedailleOrComboBox2(self):
        itemlist = self.tryquery(
            "SELECT num FROM LesParticipations WHERE numEp = {} ORDER BY num".format(self.numEp_get2())
        )
        if itemlist is not None:
            itemlist = set(map(lambda numtuple: numtuple[0], itemlist.fetchall()))
            if self.or_get2() == self.argent_get2():
                self.ui.medailleArgent_comboBox2.setCurrentText(
                    str((itemlist - {int(self.or_get2()), int(self.bronze_get2())}).pop())
                )
            if self.or_get2() == self.bronze_get2():
                self.ui.medailleBronze_comboBox2.setCurrentText(
                    str((itemlist - {int(self.or_get2()), int(self.argent_get2())}).pop())
                )

    def refreshMedailleArgentComboBox1(self):
        itemlist = self.tryquery(
            "SELECT num FROM LesParticipations WHERE numEp = {} ORDER BY num".format(self.numEp_get1())
        )
        if itemlist is not None:
            itemlist = set(map(lambda numtuple: numtuple[0], itemlist.fetchall()))
            if self.argent_get1() == self.or_get1():
                self.ui.medailleOr_comboBox1.setCurrentText(
                    str((itemlist - {int(self.argent_get1()), int(self.bronze_get1())}).pop())
                )
            if self.argent_get1() == self.bronze_get1():
                self.ui.medailleBronze_comboBox1.setCurrentText(
                    str((itemlist - {int(self.argent_get1()), int(self.or_get1())}).pop())
                )

    def refreshMedailleArgentComboBox2(self):
        itemlist = self.tryquery(
            "SELECT num FROM LesParticipations WHERE numEp = {} ORDER BY num".format(self.numEp_get2())
        )
        if itemlist is not None:
            itemlist = set(map(lambda numtuple: numtuple[0], itemlist.fetchall()))
            if self.argent_get2() == self.or_get2():
                self.ui.medailleOr_comboBox2.setCurrentText(
                    str((itemlist - {int(self.argent_get2()), int(self.bronze_get2())}).pop())
                )
            if self.argent_get2() == self.bronze_get2():
                self.ui.medailleBronze_comboBox2.setCurrentText(
                    str((itemlist - {int(self.argent_get2()), int(self.or_get2())}).pop())
                )

    def refreshMedailleBronzeComboBox1(self):
        itemlist = self.tryquery(
            "SELECT num FROM LesParticipations WHERE numEp = {} ORDER BY num".format(self.numEp_get1())
        )
        if itemlist is not None:
            itemlist = set(map(lambda numtuple: numtuple[0], itemlist.fetchall()))
            if self.bronze_get1() == self.or_get1():
                self.ui.medailleOr_comboBox1.setCurrentText(
                    str((itemlist - {int(self.bronze_get1()), int(self.argent_get1())}).pop())
                )
            if self.bronze_get1() == self.argent_get1():
                self.ui.medailleArgent_comboBox1.setCurrentText(
                    str((itemlist - {int(self.bronze_get1()), int(self.or_get1())}).pop())
                )

    def refreshMedailleBronzeComboBox2(self):
        itemlist = self.tryquery(
            "SELECT num FROM LesParticipations WHERE numEp = {} ORDER BY num".format(self.numEp_get2())
        )
        if itemlist is not None:
            itemlist = set(map(lambda numtuple: numtuple[0], itemlist.fetchall()))
            if self.bronze_get2() == self.or_get2():
                self.ui.medailleOr_comboBox2.setCurrentText(
                    str((itemlist - {int(self.bronze_get2()), int(self.argent_get2())}).pop())
                )
            if self.bronze_get2() == self.argent_get2():
                self.ui.medailleArgent_comboBox2.setCurrentText(
                    str((itemlist - {int(self.bronze_get2()), int(self.or_get2())}).pop())
                )

    def refreshAll(self):
        self.ui.numEp_comboBox1.clear()
        self.ui.numEp_comboBox2.clear()

        sans_resultats = self.tryquery("SELECT numEp FROM LesEpreuves WHERE medailleOr IS NULL ORDER BY numEp")
        avec_resultats = self.tryquery("SELECT numEp FROM LesEpreuves WHERE medailleOr IS NOT NULL ORDER BY numEp")

        if sans_resultats is not None:
            for numEp, *_ in sans_resultats:
                self.ui.numEp_comboBox1.addItem(str(numEp))
            self.refreshNumEpComboBox1()
        if avec_resultats is not None:
            for numEp, *_ in avec_resultats:
                self.ui.numEp_comboBox2.addItem(str(numEp))
            self.refreshNumEpComboBox2()

    def ajouterResultat(self):
        if self.tryquery(
            "UPDATE LesEpreuves SET medailleOr = {}, medailleArgent = {}, medailleBronze = {} WHERE ("
            "   numEp = {}"
            ")".format(self.or_get1(), self.argent_get1(), self.bronze_get1(), self.numEp_get1())
        ) is not None:
            display.refreshLabel(self.ui.label_editeurResultats,
                                 "Les résultats pour l'épreuve '{}' ont été ajoutés".format(self.numEp_get1())
                                 )
            self.data.commit()
            self.refreshAll()

    def supprimerResultat(self):
        if self.tryquery(
            "UPDATE LesEpreuves SET medailleOr = NULL, medailleArgent = NULL, medailleBronze = NULL WHERE ("
            "   numEp = {}"
            ")".format(self.numEp_get2())
        ) is not None:
            display.refreshLabel(self.ui.label_editeurResultats,
                                 "Les résultats pour l'épreuve '{}' ont été réinitialisés".format(self.numEp_get2())
                                 )
            self.data.commit()
            self.refreshAll()

    def modifierResultat(self):
        old_or = self.tryquery("SELECT medailleOr FROM LesEpreuves WHERE numEp = {}".format(self.numEp_get2()))
        old_argent = self.tryquery("SELECT medailleArgent FROM LesEpreuves WHERE numEp = {}".format(self.numEp_get2()))
        old_bronze = self.tryquery("SELECT medailleBronze FROM LesEpreuves WHERE numEp = {}".format(self.numEp_get2()))
        if old_or is not None and old_argent is not None and old_bronze is not None:
            old_or = str(old_or.fetchone()[0])
            old_argent = str(old_argent.fetchone()[0])
            old_bronze = str(old_bronze.fetchone()[0])
            if old_or != self.or_get2() or old_argent != self.argent_get2() or old_bronze != self.bronze_get2():
                if self.tryquery(
                    "UPDATE LesEpreuves SET medailleOr = {}, medailleArgent = {}, medailleBronze = {} WHERE ("
                    "   numEp = {}"
                    ")".format(self.or_get2(), self.argent_get2(), self.bronze_get2(), self.numEp_get2())
                ) is not None:
                    labeltext = list()
                    if old_or != self.or_get2():
                        labeltext.append("(medailleOr) '{}' -> '{}'".format(old_or, self.or_get2()))
                    if old_argent != self.argent_get2():
                        labeltext.append("(medailleArgent) '{}' -> '{}'".format(old_argent, self.argent_get2()))
                    if old_bronze != self.bronze_get2():
                        labeltext.append("(medailleBronze) '{}' -> '{}'".format(old_bronze, self.bronze_get2()))
                    display.refreshLabel(
                        self.ui.label_editeurResultats,
                        "Les résultats pour l'épreuve '{}' ont été modifiés: ".format(self.numEp_get2()) +
                        ", ".join(labeltext)
                    )
                    self.data.commit()
                    self.refreshAll()
            else:
                display.refreshLabel(self.ui.label_editeurResultats,
                                     "Impossible d'effectuer la modification : les valeurs sont identiques"
                                     )
