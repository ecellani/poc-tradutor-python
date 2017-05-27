# coding=utf-8
import os

import sys

import signal
from bson.json_util import dumps

from infrastructure.amqp import client as amqp_client

"""
Created on May 26, 2017

@author: Erick Cellani
"""

__body = {
    "idOferta": "1000001469",
    "cdSistemaOrigem": "SIAE",
    "idConcurso": "1000",
    "dsConcurso": "VG1 - VESTIBULAR 2017-2 - 20/05/2017",
    "dtConcursoProva": "20/05/2017",
    "hrConcursoProva": "14h",
    "idConcursoLocal": "1000FTG",
    "dsConcursoLocal": "Faculdade Anhanguera de Guarulhos",
    "dsConcursoEndereco": "Avenida Papa Pio,291 - Macedo",
    "idMarca": "FTGANH",
    "dsMarca": "ANHANGUERA",
    "idUnidade": "FTG",
    "dsUnidade": "Anhanguera de Guarulhos",
    "dsUnidadeEstado": "SP",
    "dsUnidadeCidade": "Guarulhos",
    "dsUnidadeEndereco": "Avenida Papa Pio,291 - Macedo",
    "idCurso": "EGCVSD",
    "dsCurso": "Engenharia Civil",
    "dsCursoTraduzido": "Engenharia Civil - Bacharelado",
    "idModalidade": "A5",
    "dsModalidade": "PRESENCIAL",
    "dsModalidadeTraduzido": "Presencial",
    "dsAreaConhecimentoTraduzido": "NAO INFORMADO",
    "dsDuracao": "10",
    "idTurno": "DIU",
    "dsTurno": "Diurno",
    "dsTurnoTraduzido": "Manhã",
    "idDiaDaSemana": "DIU",
    "dsDiaDaSemana": "Diurno",
    "dsDiaDaSemanaTraduzido": "Seg a Sex",
    "idHorarioAula": "DIU",
    "dsHorarioAula": "08:00 às 17:00",
    "vlInscricao": "30",
    "vlMensalidadeDe": "957.33",
    "idTipo": "BCH",
    "dsTipo": "Bacharel",
    "dtInicioInscricao": "24/04/2017",
    "dtTerminoInscricao": "19/05/2017"
}
__amqp_conn = None


def produce():
    try:
        __amqp_conn = amqp_client.connect('localhost')
        i = 0
        while i < 1000:
            amqp_client.send(__amqp_conn.channel(), 'ponte', dumps(__body))
            i = i + 1

    except Exception as e:
        raise e
    finally:
        if __amqp_conn:
            print 'AMQP Connection closed'
            __amqp_conn.close()


if __name__ == '__main__':
    print '(PID) %r producer.py' % os.getpid()
    signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
    print('Press Ctrl+C to exit')
    produce()
