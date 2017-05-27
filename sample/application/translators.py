"""
Created on May 26, 2017

@author: Erick Cellani
"""


class Translator:

    def __init__(self, mongo_conn, db):
        self.mongo_conn = mongo_conn
        self.db = db

    def translate_default(self, collection, filter_field, filter_value):
        try:
            coll = self.mongo_conn[self.db][collection]
            doc = coll.find_one({filter_field: filter_value})
            return doc
        except Exception as e:
            raise e

    def translate_modality(self, offer):
        try:
            doc = self.translate_default('deParaModalidade', 'deDsModalidade', offer['dsModalidade'])
            if doc:
                offer['dsModalidade'] = doc['paraDsModalidade']
        except Exception as e:
            # print e.message
            pass

    def translate_knowledge_area(self, offer):
        try:
            doc = self.translate_default('deParaAreaConhecimento', 'deDsAreaConhecimento', offer['dsAreaConhecimento'])
            if doc:
                offer['dsAreaConhecimento'] = doc['paraDsAreaConhecimento']
        except Exception as e:
            # print e.message
            pass

    def translate_shift(self, offer):
        try:
            doc = self.translate_default('deParaTurno', 'deDsTurno', offer['dsTurno'])
            if doc:
                offer['dsTurno'] = doc['paraDsTurno']
        except Exception as e:
            # print e.message
            pass

    def translate_class(self, offer):
        try:
            doc = self.translate_default('deParaCurso', 'deDsCurso', offer['dsCurso'])
            if doc:
                offer['dsCurso'] = doc['paraDsCurso']
        except Exception as e:
            # print e.message
            pass

    def translate_week_day(self, offer):
        try:
            doc = self.translate_default('deParaDiaDaSemana', 'deDsDiaDaSemana', offer['dsDiaDaSemana'])
            if doc:
                offer['dsDiaDaSemana'] = doc['paraDsDiaDaSemana']
        except Exception as e:
            # print e.message
            pass

    def translate_unity_brand(self, offer):
        try:
            coll = self.mongo_conn[self.db]['deParaUnidadeMarca']
            doc = coll.find_one({'idUnidade': offer['idUnidade'], 'idSistema': offer['cdSistemaOrigem']})
            if doc:
                offer['dsMarca'] = doc['paraDsMarca']
                offer['dsUnidade'] = doc['paraDsUnidade']
        except Exception as e:
            # print e.message
            pass
