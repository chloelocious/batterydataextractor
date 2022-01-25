# -*- coding: utf-8 -*-
"""
batterydataextractor.nlp.abbrev

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Abbreviation detection.
author:
"""
import spacy
import itertools


# Just for demonstration using spacy
# TODO: Change into transformers version
class AbbreviationDetector(object):
    """"""
    def __init__(self, model_name="en_abbreviation_detection_roberta_lar"):
        self.model = spacy.load(model_name)

    def detect(self, tokens):
        doc = self.model(" ".join(tokens))
        entities = doc.ents
        text_label = [(e.text, e.label_) for e in entities]
        g_list = [list(g) for k, g in itertools.groupby(text_label, key=lambda x: x[-1])]
        new_tuples = [("".join(i), j[0]) for i, j in [zip(*i) for i in g_list]]
        pairs = []
        for index, tuples in enumerate(new_tuples):
            if tuples[-1] == "LF":
                lf_tokens = tuples[0].split(" ")
                left, right = index, index
                # TODO: Need to optimise this logic
                while True:
                    if right < len(new_tuples):
                        if new_tuples[right][-1] == "AC":
                            abbrev_text = [new_tuples[right][0]]
                            break
                        right += 1
                    else:
                        if new_tuples[left][-1] == "AC" and left >= 0:
                            abbrev_text = [new_tuples[left][0]]
                            break
                        left -= 1
                pair = (abbrev_text, lf_tokens)
                pairs.append(pair)
        return pairs


class ChemAbbreviationDetector(AbbreviationDetector):
    """Chemistry-aware abbreviation detector.
    This abbreviation detector has an additional list of string equivalents (e.g. Silver = Ag) that improve abbreviation
    detection on chemistry texts.
    """
    #: Minimum abbreviation length
    abbr_min = 3
    #: Maximum abbreviation length
    abbr_max = 10
    #: String equivalents to use when detecting abbreviations.
    # TODO: include rule-based abbrev into it.
    abbr_equivs = [
        ('silver', 'Ag'),
        ('gold', 'Au'),
        ('mercury', 'Hg'),
        ('lead', 'Pb'),
        ('tin', 'Sn'),
        ('tungsten', 'W'),
        ('iron', 'Fe'),
        ('sodium', 'Na'),
        ('potassium', 'K'),
        ('copper', 'Cu'),
        ('sulfate', 'SO4'),
        ('methanol', 'MeOH'),
        ('ethanol', 'EtOH'),
        ('hydroxy', 'OH'),
        ('hexadecyltrimethylammonium bromide', 'CTAB'),
        ('cytarabine', 'Ara-C'),
        ('hydroxylated', 'OH'),
        ('hydrogen peroxide', 'H2O2'),
        ('quartz', 'SiO2'),
        ('amino', 'NH2'),
        ('amino', 'NH2'),
        ('ammonia', 'NH3'),
        ('ammonium', 'NH4'),
        ('methyl', 'CH3'),
        ('nitro', 'NO2'),
        ('potassium carbonate', 'K2CO3'),
        ('carbonate', 'CO3'),
        ('borohydride', 'BH4'),
        ('triethylamine', 'NEt3'),
        ('triethylamine', 'Et3N'),
    ]