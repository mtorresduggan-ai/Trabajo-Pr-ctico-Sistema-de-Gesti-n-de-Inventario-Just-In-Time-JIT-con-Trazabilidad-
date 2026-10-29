from datetime import date
from unittest.mock import Mock
from remesa import Remesa


def test_evaluar_proveedor_a_tiempo():
    remesa = Remesa.__new__(Remesa)

    remesa._solicitud = Mock()
    remesa._solicitud.get_fecha.return_value = date(2026, 10, 1)

    remesa._proveedor = Mock()
    remesa._proveedor.get_plazo_estimado.return_value = 5

    remesa._fecha_llegada = date(2026, 10, 5)

    remesa.evaluar_proveedor()

    remesa._proveedor.modificar_puntaje.assert_called_once_with(0.5)


def test_evaluar_proveedor_tarde():
    remesa = Remesa.__new__(Remesa)

    remesa._solicitud = Mock()
    remesa._solicitud.get_fecha.return_value = date(2026, 10, 1)

    remesa._proveedor = Mock()
    remesa._proveedor.get_plazo_estimado.return_value = 5

    remesa._fecha_llegada = date(2026, 10, 8)

    remesa.evaluar_proveedor()

    remesa._proveedor.modificar_puntaje.assert_called_once_with(-0.5)


def test_crear_remesa():
    Remesa.contador = 0

    solicitud = Mock()
    solicitud.get_fecha.return_value = date(2026, 10, 1)

    proveedor = Mock()
    proveedor.get_plazo_estimado.return_value = 5

    materiales = ["Aluminio"]
    cantidades = [20]
    fechas_vencimiento = [date(2027, 10, 1)]

    tareas = Mock()
    deposito = Mock()
    fecha_llegada = date(2026, 10, 5)

    remesa = Remesa(materiales, proveedor, solicitud, cantidades,fechas_vencimiento, deposito, tareas, fecha_llegada)

    assert remesa.get_materiales() == materiales
    assert remesa.get_cantidades() == cantidades
    assert remesa.get_fechas_vencimiento() == fechas_vencimiento
    assert remesa.get_id_remesa() == 1

    tareas.agregar.assert_called_once()


def test_remesas_tienen_ids_distintos():
    Remesa.contador = 0

    solicitud = Mock()
    solicitud.get_fecha.return_value = date(2026, 10, 1)

    proveedor = Mock()
    proveedor.get_plazo_estimado.return_value = 5

    tareas = Mock()
    deposito = Mock()

    remesa1 = Remesa(["Aluminio"], proveedor, solicitud, [20],[date(2027, 10, 1)], deposito, tareas, date(2026, 10, 5))

    remesa2 = Remesa(["Acero"], proveedor, solicitud, [10],[date(2027, 12, 1)], deposito, tareas, date(2026, 10, 5))

    assert remesa1.get_id_remesa() != remesa2.get_id_remesa()
    assert remesa2.get_id_remesa() == remesa1.get_id_remesa() + 1
