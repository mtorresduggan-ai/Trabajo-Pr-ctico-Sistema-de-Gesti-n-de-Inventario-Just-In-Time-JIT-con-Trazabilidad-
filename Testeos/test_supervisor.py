import pytest
from unittest.mock import Mock
from datetime import date

from supervisor import Supervisor


def test_recibir_remesa():
    supervisor = Supervisor("Ana", "112233", 12345678, date(2026, 1, 1), "ana@gmail.com", "ana", "Clave1234!")

    material = Mock()
    remesa = Mock()
    deposito = Mock()
    solicitud = Mock()

    remesa.get_materiales.return_value = [material]
    remesa.get_cantidades.return_value = [5]
    remesa.get_fechas_vencimiento.return_value = [date(2027, 1, 1)]
    remesa.get_fecha_llegada.return_value = date.today()
    remesa.get_solicitud.return_value = solicitud

    supervisor.validar_fechas_vencimiento = Mock()
    supervisor.validar_listas = Mock()
    Supervisor.validar_fechas_vencimiento = Mock()
    Supervisor.validar_listas = Mock()

    supervisor.recibir_remesa(remesa, deposito)

    deposito.ingresar.assert_called_once_with(material, date(2027, 1, 1), 5)
    solicitud.set_estado.assert_called_once_with("Recibido")


def test_sacar_pedido_sin_stock():
    supervisor = Supervisor("Ana", "112233", 12345678, date(2026, 1, 1), "ana@gmail.com", "ana", "Clave1234!")

    material = Mock()
    material.get_nombre.return_value = "Aluminio"

    pedido = Mock()
    pedido.get_materiales.return_value = [material]
    pedido.get_cantidades.return_value = [5]

    deposito = Mock()
    deposito.materiales_sin_stock.return_value = [material]

    tareas = Mock()

    try:
        supervisor.sacar_pedido(pedido, deposito, tareas)
        assert False, "Debería producirse un ValueError"
    except ValueError:
        pedido.set_estado.assert_not_called()


def test_sacar_pedido_correctamente():
    supervisor = Supervisor("Ana", "112233", 12345678, date(2026, 1, 1), "ana@gmail.com", "ana", "Clave1234!")

    material = Mock()
    material.get_nombre.return_value = "Aluminio"
    material.get_punto_reposicion.return_value = 10

    pedido = Mock()
    pedido.get_materiales.return_value = [material]
    pedido.get_cantidades.return_value = [5]

    deposito = Mock()
    deposito.materiales_sin_stock.return_value = []
    deposito.stock_total.return_value = 15

    tareas = Mock()
    tareas.existe_tarea_reposicion.return_value = True

    supervisor.sacar_pedido(pedido, deposito, tareas)

    deposito.retirar.assert_called_once_with(material, 5)
    pedido.set_estado.assert_called_once_with("Despachado")


def test_ejecutar_siguiente_tarea_sin_pendientes():
    supervisor = Supervisor("Ana", "112233", 12345678, date(2026, 1, 1), "ana@gmail.com", "ana", "Clave1234!")

    tareas_supervisor = Mock()
    tareas_supervisor.ver_primera.return_value = None

    try:
        supervisor.ejecutar_siguiente_tarea(tareas_supervisor, Mock())
        assert False, "Debería producirse un ValueError"
    except ValueError:
        tareas_supervisor.sacar.assert_not_called()


def test_retirar_vencidos():
    supervisor = Supervisor("Ana", "112233", 12345678, date(2026, 1, 1), "ana@gmail.com", "ana", "Clave1234!")

    deposito = Mock()

    supervisor.retirar_vencidos(deposito)

    deposito.retirar_vencidos.assert_called_once_with(date.today())