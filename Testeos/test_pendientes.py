import pytest
from unittest.mock import Mock

from pendientes import Tareas_pendientes
from tarea import Tarea


def test_es_vacia():
    tareas = Tareas_pendientes()

    assert tareas.es_vacia() == True


def test_agregar():
    tareas = Tareas_pendientes()

    tarea = Tarea("pedido", Mock())

    tareas.agregar(tarea)

    assert tareas.es_vacia() == False
    assert tareas.ver_primera().get_tipo() == tarea.get_tipo()


def test_agregar_varias():
    tareas = Tareas_pendientes()

    tarea1 = Tarea("pedido", Mock())
    tarea2 = Tarea("remesa", Mock())

    tareas.agregar(tarea1)
    tareas.agregar(tarea2)

    assert tareas.ver_primera().get_tipo() == "pedido"
    
    segunda = tareas.get_frente().get_siguiente()
    assert segunda.get_tipo() == "remesa"


def test_agregar_objeto_incorrecto():
    tareas = Tareas_pendientes()

    try:
        tareas.agregar("no es una tarea")
        assert False
    except TypeError:
        assert tareas.es_vacia() == True


def test_sacar():
    tareas = Tareas_pendientes()

    tarea = Tarea("pedido", Mock())
    tareas.agregar(tarea)

    tareas.sacar()

    assert tareas.es_vacia() == True
    assert tareas.get_final() is None


def test_sacar_sin_tareas():
    tareas = Tareas_pendientes()

    try:
        tareas.sacar()
        assert False
    except ValueError:
        assert tareas.es_vacia() == True


def test_ver_primera():
    tareas = Tareas_pendientes()

    tarea = Tarea("pedido", Mock())
    tareas.agregar(tarea)

    assert tareas.ver_primera().get_tipo() == "pedido"


def test_ver_primera_vacia():
    tareas = Tareas_pendientes()

    assert tareas.ver_primera() == None
