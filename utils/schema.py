# utils/schema.py
from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator

# ----------------------------
# Utilitaires
# ----------------------------

class Levels(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    totalement: Optional[float] = None
    en_partie: Optional[float] = None
    insuffisamment: Optional[float] = None
    pas_du_tout: Optional[float] = None


class ObjectifEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    objectif_label: str
    levels: Optional[Levels] = None
    note_sur_10: Optional[float] = None


# ----------------------------
# Maîtrise des objectifs
# ----------------------------

class MaitriseObjectifsPre(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    mode: Optional[Literal["4_niveaux", "notes_sur_10"]] = None
    par_objectif: Optional[List[ObjectifEntry]] = None
    note_globale_objectifs_preformation: Optional[float] = None


class MaitriseObjectifsAChaud(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    mode: Optional[Literal["4_niveaux", "notes_sur_10"]] = None
    par_objectif: Optional[List[ObjectifEntry]] = None
    note_globale_objectifs_a_chaud: Optional[float] = None


class MaitriseObjectifsAFroid(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    mode: Optional[Literal["4_niveaux", "notes_sur_10"]] = None
    par_objectif: Optional[List[ObjectifEntry]] = None
    note_globale_objectifs_a_froid: Optional[float] = None


# ----------------------------
# Pré-formation
# ----------------------------

class VolonteSuivi(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    nb_votants: Optional[int] = Field(None, alias="nb votants")


class EchelleDistributionItem(BaseModel):
    """
    Un seul des champs 'echele X' doit être renseigné par item.
    Nouveau prompt v2.2 : capture AUSSI 'nb_votants' en plus de 'pourcentage'.
    """
    model_config = ConfigDict(populate_by_name=True)

    echele_5: Optional[str] = Field(None, alias="echele 5")
    echele_4: Optional[str] = Field(None, alias="echele 4")
    echele_3: Optional[str] = Field(None, alias="echele 3")
    echele_2: Optional[str] = Field(None, alias="echele 2")
    echele_1: Optional[str] = Field(None, alias="echele 1")

    nb_votants: Optional[int] = None
    pourcentage: Optional[float] = None

    @model_validator(mode="after")
    def _exactly_one_echele_key(self):
        keys = ["echele_5", "echele_4", "echele_3", "echele_2", "echele_1"]
        present = [k for k in keys if getattr(self, k) is not None]
        if len(present) != 1:
            raise ValueError(
                "Chaque item de distribution doit contenir exactement une clé parmi "
                "'echele 5', 'echele 4', 'echele 3', 'echele 2', 'echele 1'."
            )
        return self

    @field_validator("nb_votants")
    @classmethod
    def _nb_votants_int(cls, v):
        if v is None:
            return v
        if isinstance(v, bool):
            raise ValueError("nb_votants ne doit pas être booléen.")
        try:
            return int(v)
        except Exception as e:
            raise ValueError("nb_votants doit être un entier (ex: 17).") from e

    @field_validator("pourcentage")
    @classmethod
    def _pourcentage_float(cls, v):
        if v is None:
            return v
        try:
            return float(v)
        except Exception as e:
            raise ValueError("pourcentage doit être un nombre sans symbole % (ex: 73).") from e


class PreFormation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    volonte_suivi_formation: Optional[VolonteSuivi] = None
    souhaitez_vous_suivre_distribution: Optional[List[EchelleDistributionItem]] = None
    demande_sujets_a_aborder: Optional[List[str]] = None
    maitrise_objectifs_preformation: Optional[MaitriseObjectifsPre] = None


# ----------------------------
# À chaud
# ----------------------------

class FormationProfitable(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    oui: Optional[float] = None
    non: Optional[float] = None
    oui_percent: Optional[float] = None
    non_percent: Optional[float] = None


class SatisfactionItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    label: Literal["Très satisfait(e)", "Satisfait(e)", "Déçu(e)", "Sans opinion"]
    count: Optional[float] = None
    percent: Optional[float] = None


class MaitriseObjectifsAChaud(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    mode: Optional[Literal["4_niveaux", "notes_sur_10"]] = None
    par_objectif: Optional[List[ObjectifEntry]] = None
    note_globale_objectifs_a_chaud: Optional[float] = None


class AChaud(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    formation_profitable: Optional[FormationProfitable] = None
    satisfaction_contenu: Optional[List[SatisfactionItem]] = None
    note_globale_a_chaud: Optional[float] = None
    points_forts: Optional[List[str]] = None
    points_a_ajuster: Optional[List[str]] = None
    suggestions_complement_sur_formation: Optional[List[str]] = None
    appreciations_intervenants: Optional[List[str]] = None
    maitrise_objectifs_a_chaud: Optional[MaitriseObjectifsAChaud] = None


# ----------------------------
# À froid
# ----------------------------

class AFroid(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    note_sur_10: Optional[float] = None
    maitrise_objectifs_a_froid: Optional[MaitriseObjectifsAFroid] = None
    elements_les_plus_utiles: Optional[List[str]] = None


# ----------------------------
# Intervenants
# ----------------------------

class AdaptationHoraires(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    reponse: Optional[Literal["oui", "non"]] = None
    precisions: Optional[str] = None


class ContenuNonPrevu(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    reponse: Optional[Literal["oui", "non"]] = None
    de_quoi_s_agissait_il: Optional[str] = None


class Intervenants(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    commentaire_conditions_materielles: Optional[str] = None
    commentaire_groupe_apprenants: Optional[str] = None
    commentaire_organisation_generale: Optional[str] = None
    adaptation_horaires: Optional[AdaptationHoraires] = None
    precisions_a_noter: Optional[str] = None
    explication_modification_programme: Optional[str] = None
    contenu_non_prevu: Optional[ContenuNonPrevu] = None
    # v2.1
    retards_apprenants: Optional[Dict[str, Optional[float]]] = None  # {"oui": number|null, "non": number|null}
    handicap_signale: Optional[Dict[str, Optional[float]]] = None    # {"oui": number|null, "non": number|null}


# ----------------------------
# Résultats évaluations
# ----------------------------

class ResultatsEvaluations(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    progression_competences_plus_sur_10: Optional[float] = None


# ----------------------------
# Payload final (v2.2)
# ----------------------------

class OutputPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    version_prompt: Optional[str] = None  # "v2.2"
    Nom_formation: str = Field(..., alias="Nom formation")
    semestre: str = Field(..., alias=" semestre")
    pre_formation: Optional[PreFormation] = None
    a_chaud: Optional[AChaud] = None
    a_froid: Optional[AFroid] = None
    intervenants: Optional[Intervenants] = None
    resultats_evaluations: Optional[ResultatsEvaluations] = None
    meta_extraction: Optional[Dict[str, Optional[bool]]] = None  # {"graphique_non_lisible": bool|null}
    lien_vers_formation: str
