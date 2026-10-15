import pytest
from unittest.mock import Mock
from datetime import date

from supervisor import Supervisor


def test_recibir_remesa():
    supervisor = Supervisor("Ana", "112233", "12345678",date(2026, 1, 1), "ana@gmail.com", "ana", "1234")

    material = Mock()
    remesa = Mock()
    deposito = Mock()
    estante = Mock()

    remesa.materiales = [material]
    remesa.cantidades = [5]
    remesa.fechas_vencimiento = [date(2027, 1, 1)]
    remesa.fecha_llegada = date.today()
    remesa.solicitud.estado = "Pendiente"

    deposito.stock = {material: estante}

    supervisor.validar_fechas_vencimiento = Mock()
    supervisor.validar_listas = Mock()

    supervisor.recibir_remesa(remesa, deposito)

    estante.agregar_caja.assert_called_once_with(date(2027, 1, 1), 5)
    deposito.agregar_material.assert_called_once_with(material)
    assert remesa.solicitud.estado == "Recibida"



def test_sacar_pedido_sin_stock():
    supervisor = Supervisor("Ana", "112233", "12345678",date(2026, 1, 1), "ana@gmail.com", "ana", "1234")

    material = Mock()
    material.nombre = "Aluminio"

    pedido = Mock()
    pedido.materiales = [material]
    pedido.cantidades = [5]

    deposito = Mock()
    deposito.stock = {}

    tareas = Mock()

    try:
        supervisor.sacar_pedido(pedido, deposito, tareas)
        assert False, "Debería producirse un ValueError"
    except ValueError:
        assert pedido.estado != "Despachado"


def test_sacar_pedido_correctamente():
    supervisor = Supervisor("Ana", "112233", "12345678",date(2026, 1, 1), "ana@gmail.com", "ana", "1234")

    material = Mock()
    material.nombre = "Aluminio"
    material.punto_reposicion = 10

    pedido = Mock()
    pedido.materiales = [material]
    pedido.cantidades = [5]

    estante = Mock()
    estante.stock_total.return_value = 20

    deposito = Mock()
    deposito.stock = {material: estante}
    deposito.stock_total.return_value = 15

    tareas = Mock()
    tareas.existe_tarea_reposicion.return_value = True

    supervisor.sacar_pedido(pedido, deposito, tareas)

    estante.sacar_cajas.assert_called_once_with(5)
    assert pedido.estado == "Despachado"


def test_ejecutar_siguiente_tarea_sin_pendientes():
    supervisor = Supervisor("Ana", "112233", "12345678",date(2026, 1, 1), "ana@gmail.com", "ana", "1234")
    
    tareas_supervisor = Mock()
    tareas_supervisor.ver_primera.return_value = None

    try:
        supervisor.ejecutar_siguiente_tarea(tareas_supervisor, Mock())
        assert False, "Debería producirse un ValueError"
    except ValueError:
        tareas_supervisor.sacar.assert_not_called()


def test_retirar_vencidos():
    supervisor = Supervisor("Ana", "112233", "12345678",date(2026, 1, 1), "ana@gmail.com", "ana", "1234")

    estante = Mock()
    deposito = Mock()
    deposito.stock = {"AL01": estante}

    supervisor.retirar_vencidos(deposito)

    estante.retirar_cajas_vencidas.assert_called_once_with(date.today())