import pytest
from datetime import date
from unittest.mock import Mock
from remesa import Remesa


def test_evaluar_proveedor_a_tiempo():
    remesa = Remesa.__new__(Remesa)

    remesa.solicitud = Mock()
    remesa.solicitud.fecha = date(2026, 10, 1)

    remesa.proveedor = Mock()
    remesa.proveedor.plazo_estimado = 5

    remesa.fecha_llegada = date(2026, 10, 5)

    remesa.evaluar_proveedor()
    # Verifica que un método se haya llamado exactamente una vez y con ese argumento (en este caso 0.5).
    remesa.proveedor.modificar_puntaje.assert_called_once_with(0.5)


def test_evaluar_proveedor_tarde():
    remesa = Remesa.__new__(Remesa)

    remesa.solicitud = Mock()
    remesa.solicitud.fecha = date(2026, 10, 1)

    remesa.proveedor = Mock()
    remesa.proveedor.plazo_estimado = 5

    remesa.fecha_llegada = date(2026, 10, 8)

    remesa.evaluar_proveedor()

    remesa.proveedor.modificar_puntaje.assert_called_once_with(-0.5)


def test_crear_remesa():
    Remesa.todos.clear()

    solicitud = Mock()
    solicitud.fecha = date(2026, 10, 1)

    proveedor = Mock()
    proveedor.plazo_estimado = 5

    materiales = ["Aluminio"]
    cantidades = [20]
    fechas_vencimiento = [date(2027, 10, 1)]

    tareas = Mock()
    deposito = Mock()
    fecha_llegada = date(2026, 10, 5)

    remesa = Remesa(materiales, proveedor, solicitud, cantidades, fechas_vencimiento, deposito, tareas, fecha_llegada)

    assert remesa.materiales == materiales
    assert remesa.cantidades == cantidades
    assert remesa.fechas_vencimiento == fechas_vencimiento
    assert remesa in Remesa.todos
    tareas.agregar.assert_called_once()
