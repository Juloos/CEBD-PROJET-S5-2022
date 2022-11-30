import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


# Classe permettant d'afficher la fenêtre de visualisation des données
class AppEditeurInscriptionsV1(QDialog):

    # Constructeur
    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/v1_editeurInscriptions.ui", self)
        self.data = data

        # attribuer les valeurs aux comboBox
        # les contraintes d'intégrité suivantes ne sont pas prises en compte dans la conception de l'interface:
        #   - correlation entre categorie de l'épreuve et type de participant (équipe ou individuel)
        #   - correlation entre discipline de l'épreuve et discipline du participant
        self.refreshAll()

    def tryquery(self, query):
        try:
            # print(query)
            return self.data.cursor().execute(query)
        except sqlite3.Error as err:
            display.refreshLabel(
                self.ui.label_editeurInscriptions,
                "Impossible d'effectuer la requête dans la DB : " + repr(err)
            )
            return None

    def num_get1(self):
        return self.ui.num_comboBox1.currentText()

    def num_get2(self):
        return self.ui.num_comboBox2.currentText()

    def num_get3(self):
        return self.ui.num_comboBox3.currentText()

    def numEp_get1(self):
        return self.ui.numEp_comboBox1.currentText()

    def numEp_get2(self):
        return self.ui.numEp_comboBox2.currentText()

    def numEp_get3(self):
        return self.ui.numEp_comboBox3.currentText()

    def refreshNumComboBox1(self):
        # proposer des épreuves où le participant sélectionné n'est pas déjà inscrit, pour les inscriptions
        self.ui.numEp_comboBox1.clear()
        result = self.tryquery(
            "SELECT DISTINCT numEp FROM LesEpreuves WHERE numEp NOT IN ("
            "   SELECT numEp FROM LesParticipations WHERE num = {}"
            ") ORDER BY numEp".format(self.num_get1())
        )
        if result is not None:
            for numEp, *_ in result:
                self.ui.numEp_comboBox1.addItem(str(numEp))

    def refreshNumComboBox2(self):
        # proposer des épreuves où le participant sélectionné est inscrit, pour les désinscriptions
        self.ui.numEp_comboBox2.clear()
        result = self.tryquery(
            "SELECT numEp FROM LesParticipations WHERE num = {} ORDER BY numEp".format(self.num_get2())
        )
        if result is not None:
            for numEp, *_ in result:
                self.ui.numEp_comboBox2.addItem(str(numEp))
        self.refreshNumComboBox3()
        self.refreshNumEpComboBox3()

    def refreshNumEpComboBox2(self):
        self.refreshNumComboBox3()
        self.refreshNumEpComboBox3()

    def refreshNumComboBox3(self):
        # proposer des épreuves où le participant sélectionné n'est pas déjà inscrit, pour les modifications
        self.ui.numEp_comboBox3.clear()
        result = self.tryquery(
            "SELECT DISTINCT numEp FROM LesEpreuves WHERE numEp NOT IN ("
            "   SELECT numEp FROM LesParticipations WHERE num = {} AND numEp != {}"
            ") ORDER BY numEp".format(self.num_get2(), self.numEp_get2())
        )
        if result is not None:
            for num, *_ in result:
                self.ui.numEp_comboBox3.addItem(str(num))
        self.ui.numEp_comboBox3.setCurrentText(self.numEp_get2())

    def refreshNumEpComboBox3(self):
        # proposer des participants qui ne sont pas déjà inscrit dans l'épreuve sélectionné, pour les modifications
        self.ui.num_comboBox3.clear()
        result = self.tryquery(
            "SELECT DISTINCT num FROM LesParticipants WHERE num NOT IN ("
            "   SELECT num FROM LesParticipations WHERE numEp = {} AND num != {}"
            ") ORDER BY num".format(self.numEp_get2(), self.num_get2())
        )
        if result is not None:
            for num, *_ in result:
                self.ui.num_comboBox3.addItem(str(num))
        self.ui.num_comboBox3.setCurrentText(self.num_get2())

    def refreshAll(self):
        self.ui.num_comboBox1.clear()
        self.ui.num_comboBox2.clear()
        self.ui.num_comboBox3.clear()
        self.ui.numEp_comboBox3.clear()

        participants = self.tryquery("SELECT num FROM LesParticipants ORDER BY num")
        epreuves = self.tryquery("SELECT DISTINCT numEp FROM LesEpreuves ORDER BY numEp")
        participants_epreuves = self.tryquery("SELECT DISTINCT num FROM LesParticipations ORDER BY num")

        if participants is not None:
            for num, *_ in participants:
                self.ui.num_comboBox1.addItem(str(num))
                self.ui.num_comboBox3.addItem(str(num))
            self.refreshNumComboBox1()

        if epreuves is not None:
            for numEp, *_ in epreuves:
                self.ui.numEp_comboBox3.addItem(str(numEp))

        if participants_epreuves is not None:
            for num, *_ in participants_epreuves:
                self.ui.num_comboBox2.addItem(str(num))
            self.refreshNumComboBox2()

    def ajouterInscription(self):
        if self.tryquery(
            "INSERT INTO LesParticipations VALUES ({},{})".format(self.num_get1(), self.numEp_get1())
        ) is not None:
            display.refreshLabel(self.ui.label_editeurInscriptions,
                                 "Le participant '{}' a été inscrit dans l'épreuve '{}'".format(
                                    self.num_get1(), self.numEp_get1()
                                 ))
            self.data.commit()
            self.refreshAll()

    def supprimerInscription(self):
        if self.tryquery(
            "DELETE FROM LesParticipations WHERE num = {} AND numEp = {}".format(self.num_get2(), self.numEp_get2())
        ) is not None:
            display.refreshLabel(self.ui.label_editeurInscriptions,
                                 "Le participant '{}' a été désinscrit de l'épreuve '{}'".format(
                                    self.num_get2(), self.numEp_get2()
                                 ))
            self.data.commit()
            self.refreshAll()

    def modifierInscription(self):
        oldNum = self.num_get2()
        oldNumEp = self.numEp_get2()
        newNum = self.num_get3()
        newNumEp = self.numEp_get3()
        if oldNum != newNum or oldNumEp != newNumEp:
            if self.tryquery(
                "UPDATE LesParticipations SET num = {}, numEp = {} WHERE num = {} AND numEp = {}".format(
                    newNum, newNumEp, oldNum, oldNumEp
                )
            ) is not None:
                if oldNum != newNum:
                    display.refreshLabel(self.ui.label_editeurInscriptions,
                                         "Le participant '{}' a été remplacé par le participant '{}' "
                                         "dans l'épreuve '{}'".format(oldNum, newNum, newNumEp))
                else:
                    display.refreshLabel(self.ui.label_editeurInscriptions,
                                         "Le participant '{}' a changé d'épreuve '{}' pour l'épreuve '{}'".format(
                                            oldNum, oldNumEp, newNumEp
                                         ))
                self.data.commit()
                self.refreshAll()
        else:
            display.refreshLabel(self.ui.label_editeurInscriptions,
                                 "Impossible d'effectuer la modification : les valeurs sont identiques"
                                 )
