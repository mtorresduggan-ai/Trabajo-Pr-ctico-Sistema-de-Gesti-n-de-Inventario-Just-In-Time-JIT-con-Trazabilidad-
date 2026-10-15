from datetime import date
from unittest.mock import Mock

from material import Material
from deposito import Deposito
from remesa import Remesa
from supervisor import Supervisor_deposito
from pendientes import Pendientes

def test_ingreso_remesa_por_supervisor():
    Material.todos.clear()
    Remesa.todos.clear()

    aluminio = Material("Aluminio", "Al", "kg", 100)
    deposito = Deposito("Depósito central")
    tareas = Pendientes()

    proveedor = Mock()
    proveedor.plazo_estimado = 5

    solicitud = Mock()
    solicitud.fecha = date(2026, 10, 1)
    solicitud.estado = "Solicitado"

    remesa = Remesa([aluminio],proveedor,solicitud,[20], [date(2027, 10, 1)],deposito, tareas,date(2026, 10, 5) )

    # La remesa genera una tarea pendiente
    assert not tareas.es_vacia()
    assert tareas.ver_primera().tipo == "remesa"

    # El supervisor ejecuta la tarea
    supervisor = Supervisor_deposito.__new__(Supervisor_deposito)
    supervisor.ejecutar_siguiente_tarea(tareas, Pendientes())

    # Se verifica el ingreso al depósito
    assert deposito.stock_total(aluminio) == 20
    assert solicitud.estado == "Recibida"
    assert tareas.es_vacia()