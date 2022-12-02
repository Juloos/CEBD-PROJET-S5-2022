CREATE TRIGGER check_insert_medailles_differentes
    BEFORE INSERT ON LesEpreuves
    WHEN (
        -- Pour l'épreuve donnée, on vérifie que les médailles sont toutes différentes les unes des autres
        NEW.medailleOr = NEW.medailleArgent OR
        NEW.medailleArgent = NEW.medailleBronze OR
        NEW.medailleBronze = NEW.medailleOr
    )
    BEGIN
        SELECT RAISE(FAIL, 'Integrity error: les medailles doivent être différentes');
    END;

CREATE TRIGGER check_update_medailles_differentes
    BEFORE UPDATE OF medailleOr, medailleArgent, medailleBronze ON LesEpreuves
    WHEN (
        NEW.medailleOr = NEW.medailleArgent OR
        NEW.medailleArgent = NEW.medailleBronze OR
        NEW.medailleBronze = NEW.medailleOr
    )
    BEGIN
        SELECT RAISE(FAIL, 'Integrity error: les medailles doivent être différentes');
    END;

CREATE TRIGGER check_insert_medailles_attributions
    BEFORE INSERT ON LesEpreuves
    WHEN (
        -- Pour l'épreuve donnée, on vérifie que toutes les médailles sont NULL, ou alors toutes sont non NULL
        (NEW.medailleOr IS NULL AND NEW.medailleArgent IS NOT NULL) OR
        (NEW.medailleOr IS NULL AND NEW.medailleBronze IS NOT NULL) OR
        (NEW.medailleArgent IS NULL AND NEW.medailleOr IS NOT NULL) OR
        (NEW.medailleArgent IS NULL AND NEW.medailleBronze IS NOT NULL) OR
        (NEW.medailleBronze IS NULL AND NEW.medailleOr IS NOT NULL) OR
        (NEW.medailleBronze IS NULL AND NEW.medailleArgent IS NOT NULL)
    )
    BEGIN
        SELECT RAISE(FAIL, 'Integrity error: toutes les médailles doivent être attribuées, ou alors aucune');
    END;

CREATE TRIGGER check_update_medailles_attributions
    BEFORE UPDATE OF medailleOr, medailleArgent, medailleBronze ON LesEpreuves
    FOR EACH ROW
    WHEN (
        (NEW.medailleOr IS NULL AND NEW.medailleArgent IS NOT NULL) OR
        (NEW.medailleOr IS NULL AND NEW.medailleBronze IS NOT NULL) OR
        (NEW.medailleArgent IS NULL AND NEW.medailleOr IS NOT NULL) OR
        (NEW.medailleArgent IS NULL AND NEW.medailleBronze IS NOT NULL) OR
        (NEW.medailleBronze IS NULL AND NEW.medailleOr IS NOT NULL) OR
        (NEW.medailleBronze IS NULL AND NEW.medailleArgent IS NOT NULL)
    )
    BEGIN
        SELECT RAISE(FAIL, 'Integrity error: toutes les médailles doivent être attribuées, ou alors aucune');
    END;

CREATE TRIGGER check_insert_discipline_participants
    BEFORE INSERT ON LesParticipations
    WHEN (
        -- Pour la participation donnée, on vérifie que la discipline de l'épreuve insérée est la même que celle des autres épreuves
        (SELECT nomDi FROM LesEpreuves WHERE numEp = NEW.numEp)
        <>
        (SELECT DISTINCT nomDi FROM LesEpreuves WHERE numEp IN (SELECT numEp FROM LesParticipations WHERE num = NEW.num))
        AND EXISTS (SELECT numEp FROM LesParticipations WHERE num = NEW.num)
    )
    BEGIN
        SELECT RAISE(FAIL, 'Integrity error: la discipline des participants doit etre la meme que celle de l''epreuve');
    END;

CREATE TRIGGER check_update_discipline_participants
    BEFORE UPDATE ON LesParticipations
    FOR EACH ROW
    WHEN (
        -- Pour la participation donnée, on vérifie que la discipline de l'épreuve insérée est la même que celle des autres épreuves
        (SELECT nomDi FROM LesEpreuves WHERE numEp = NEW.numEp)
        <>
        (SELECT DISTINCT nomDi FROM LesEpreuves WHERE numEp IN (SELECT numEp FROM LesParticipations WHERE num = NEW.num))
        AND EXISTS (SELECT numEp FROM LesParticipations WHERE num = NEW.num)
    )
    BEGIN
        SELECT RAISE(FAIL, 'Integrity error: la discipline des participants doit etre la meme que celle de l''epreuve');
    END;