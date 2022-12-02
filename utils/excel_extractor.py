import sqlite3
from sqlite3 import IntegrityError

import pandas


def pretryquery(cursor, query):
    # print(query)
    try:
        cursor.execute(query)
    except IntegrityError as err:
        # print(err)
        pass


def read_excel_file_V0(data: sqlite3.Connection, file):
    tryquery = lambda query: pretryquery(data.cursor(), query)

    # Lecture de l'onglet du fichier excel LesSportifs, en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête
    df_sportifs = pandas.read_excel(file, sheet_name='LesSportifsEQ', dtype=str)
    df_sportifs = df_sportifs.where(pandas.notnull(df_sportifs), 'null')

    for ix, row in df_sportifs.iterrows():
        tryquery(
            "insert into V0_LesSportifs values ({},'{}','{}','{}','{}','{}',{})".format(
                row['numSp'], row['nomSp'], row['prenomSp'], row['pays'],
                row['categorieSp'], row['dateNaisSp'], row['numEq']
            )
        )

    # Lecture de l'onglet LesEpreuves du fichier excel, en interprétant toutes les colonnes comme des string
    # pour construire uniformement la requête
    df_epreuves = pandas.read_excel(file, sheet_name='LesEpreuves', dtype=str)
    df_epreuves = df_epreuves.where(pandas.notnull(df_epreuves), 'null')

    for ix, row in df_epreuves.iterrows():
        query = "insert into V0_LesEpreuves values ({},'{}','{}','{}','{}',{},".format(
            row['numEp'], row['nomEp'], row['formeEp'], row['nomDi'], row['categorieEp'], row['nbSportifsEp']
        )

        if (row['dateEp'] != 'null'):
            query += "'{}')".format(row['dateEp'])
        else:
            query += "null)"

        tryquery(query)


def read_excel_file_V1(data: sqlite3.Connection, file):
    tryquery = lambda query: pretryquery(data.cursor(), query)

    # Lecture de l'onglet du fichier excel LesSportifsEQ, en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête
    df_sportifs = pandas.read_excel(file, sheet_name='LesSportifsEQ', dtype=str)
    df_sportifs = df_sportifs.where(pandas.notnull(df_sportifs), 'null')

    for ix, row in df_sportifs.iterrows():
        tryquery(
            "insert into LesSportifs values ({},'{}','{}','{}','{}','{}')".format(
                row['numSp'], row['nomSp'], row['prenomSp'], row['pays'], row['categorieSp'], row['dateNaisSp']
            )
        )

        tryquery("insert into LesParticipants values ({})".format(row['numSp']))

        if row['numEq'] != 'null':
            tryquery("insert into LesParticipants values ({})".format(row['numEq']))
            tryquery("insert into LesEquipiers values ({},{})".format(row['numEq'], row['numSp']))

            if row['pays'] != 'null':
                tryquery("insert into LesEquipes values ({},'{}')".format(row['numEq'], row['pays']))

    # Lecture de l'onglet du fichier excel LesEpreuves et LesResultats, en interprétant toutes les colonnes comme des
    # string pour construire uniformement la requête
    df_epreuves = pandas.read_excel(file, sheet_name='LesEpreuves', dtype=str)
    df_epreuves = df_epreuves.where(pandas.notnull(df_epreuves), 'null')
    df_resultats = pandas.read_excel(file, sheet_name='LesResultats', dtype=str)
    df_resultats = df_resultats.where(pandas.notnull(df_resultats), 'null')

    for ix, row in df_epreuves.iterrows():
        query = "insert into LesEpreuves values ({},'{}','{}','{}','{}',{},".format(
            row['numEp'], row['nomEp'], row['formeEp'], row['nomDi'], row['categorieEp'], row['nbSportifsEp']
        )

        if row['dateEp'] != 'null':
            query = query + "'{}'".format(row['dateEp'])
        else:
            query = query + "null"

        if row['numEp'] in df_resultats['numEp'].values:
            query += ",{},{},{})".format(
                df_resultats.loc[df_resultats['numEp'] == row['numEp'], 'gold'].values[0],
                df_resultats.loc[df_resultats['numEp'] == row['numEp'], 'silver'].values[0],
                df_resultats.loc[df_resultats['numEp'] == row['numEp'], 'bronze'].values[0]
            )
        else:
            query += ",null,null,null)"
        tryquery(query)

        if row['nomDi'] != 'null':
            tryquery("insert into LesDisciplines values ('{}')".format(row['nomDi']))

    # Lecture de l'onglet du fichier excel LesInscriptions, en interprétant toutes les colonnes comme des
    # string pour construire uniformement la requête
    df_incriptions = pandas.read_excel(file, sheet_name='LesInscriptions', dtype=str)
    df_incriptions = df_incriptions.where(pandas.notnull(df_incriptions), 'null')

    for ix, row in df_incriptions.iterrows():
        tryquery("insert into LesParticipations values ({},{})".format(row['numIn'], row['numEp']))
