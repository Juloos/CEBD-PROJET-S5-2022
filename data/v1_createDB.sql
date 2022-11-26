-- TODO 1.3a : Créer les tables manquantes et modifier celles ci-dessous
CREATE TABLE LesSportifs
(
  numSp NUMBER(4),
  nomSp VARCHAR2(20),
  prenomSp VARCHAR2(20),
  pays VARCHAR2(20),
  categorieSp VARCHAR2(10),
  dateNaisSp DATE,
  CONSTRAINT SP_CK1 CHECK(numSp > 0),
  CONSTRAINT SP_CK2 CHECK(categorieSp IN ('feminin','masculin')),
  CONSTRAINT SP_PK PRIMARY KEY(numSp)
);

CREATE TABLE LesEpreuves
(
  numEp NUMBER(3),
  nomEp VARCHAR2(20),
  formeEp VARCHAR2(13),
  nomDi VARCHAR2(25),
  categorieEp VARCHAR2(10),
  nbSportifsEp NUMBER(2),
  MedailleOr NUMBER(4),
  MedailleArgent NUMBER(4),
  MedailleBronze NUMBER(4),
  dateEp DATE,
  CONSTRAINT EP_PK PRIMARY KEY (numEp),
  CONSTRAINT EP_CK1 CHECK (formeEp IN ('individuelle','par equipe','par couple')),
  CONSTRAINT EP_CK2 CHECK (categorieEp IN ('feminin','masculin','mixte')),
  CONSTRAINT EP_CK3 CHECK (numEp > 0),
  CONSTRAINT EP_CK4 CHECK (nbSportifsEp > 0)
);
CREATE TABLE LesEquipes
(
  numEq NUMBER(4),
  paysEq VARCHAR2(20),
  CONSTRAINT EQ_PK PRIMARY KEY (numEq, paysEq),
  CONSTRAINT EQ_CK1 CHECK (numEq > 0)
);

CREATE TABLE LesDisciplines
(
  nomDi VARCHAR2(25),
  CONSTRAINT DI_PK PRIMARY KEY (nomDi)
);

CREATE TABLE LesParticipations
(
  num NUMBER(4),
  numEp NUMBER(3),
  CONSTRAINT PA_PK PRIMARY KEY (num, numEp),
  CONSTRAINT PA_CK1 CHECK (num > 0),
  CONSTRAINT PA_CK2 CHECK (numEp > 0)
);

CREATE TABLE LesParticipants
(
  num NUMBER(4),
  CONSTRAINT PA_PK PRIMARY KEY (num),
    CONSTRAINT PA_CK1 CHECK (num > 0)
);

CREATE TABLE A
(
  nomDi VARCHAR2(25),
  numEp NUMBER(3),
  CONSTRAINT A_PK PRIMARY KEY (nomDi, numEp),
  CONSTRAINT A_CK1 CHECK (numEp > 0)
);

CREATE TABLE LesEquipiers
(
  numEq NUMBER(4),
  numSp NUMBER(4),
  CONSTRAINT EQ_PK PRIMARY KEY (numEq, numSp),
  CONSTRAINT EQ_CK1 CHECK (numEq > 0),
  CONSTRAINT EQ_CK2 CHECK (numSp > 0)
);

CREATE VIEW LesAgesSportifs(numSp, ageSp) AS
    SELECT numSp, DATE('now') - dateNaisSp AS ageSp
        FROM LesSportifs;

CREATE VIEW LesNbsEquipiers(numEq, nbEquipiers) AS
    SELECT numEq, COUNT(numSp) AS nbEquipiers
        FROM LesEquipiers;

-- TODO 3.3 : ajouter les éléments nécessaires pour créer le trigger (attention, syntaxe SQLite différent qu'Oracle)
