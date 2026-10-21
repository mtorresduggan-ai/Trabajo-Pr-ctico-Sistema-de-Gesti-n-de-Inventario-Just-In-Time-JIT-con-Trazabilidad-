from datetime import date
from estante import Estante


def test_agregar_caja():
    estante = Estante()
    estante.agregar_caja(date(2027, 5, 10), 100)

    assert estante.stock_total() == 100


def test_agregar_cajas_mismo_vencimiento():
    estante = Estante()
    estante.agregar_caja(date(2027, 5, 10), 100)
    estante.agregar_caja(date(2027, 5, 10), 50)

    assert estante.stock_total() == 150


def test_agregar_cajas_ordenadas_por_vencimiento():
    estante = Estante()
    estante.agregar_caja(date(2027, 6, 10), 30)
    estante.agregar_caja(date(2027, 5, 10), 20)

    assert estante.get_primera().get_fecha_vencimiento() == date(2027, 5, 10)


def test_sacar_cajas():
    estante = Estante()
    estante.agregar_caja(date(2027, 5, 10), 100)
    estante.sacar_cajas(30)

    assert estante.stock_total() == 70


def test_sacar_cajas_de_varias_cajas():
    estante = Estante()
    estante.agregar_caja(date(2027, 5, 10), 20)
    estante.agregar_caja(date(2027, 6, 10), 30)
    estante.sacar_cajas(35)

    assert estante.stock_total() == 15


def test_sacar_todo_el_stock():
    estante = Estante()
    estante.agregar_caja(date(2027, 5, 10), 20)
    estante.sacar_cajas(20)

    assert estante.stock_total() == 0


def test_sacar_sin_stock_suficiente():
    estante = Estante()
    estante.agregar_caja(date(2027, 5, 10), 20)

    try:
        estante.sacar_cajas(30)
        assert False
    except ValueError:
        assert estante.stock_total() == 20


def test_hay_cajas_vencidas():
    estante = Estante()
    estante.agregar_caja(date(2027, 5, 10), 20)

    assert estante.hay_cajas_vencidas(date(2027, 5, 11))


def test_no_hay_cajas_vencidas():
    estante = Estante()
    estante.agregar_caja(date(2027, 5, 10), 20)

    assert not estante.hay_cajas_vencidas(date(2027, 5, 10))


def test_retirar_cajas_vencidas():
    estante = Estante()
    estante.agregar_caja(date(2027, 5, 10), 20)
    estante.agregar_caja(date(2027, 6, 10), 30)

    estante.retirar_cajas_vencidas(date(2027, 5, 11))

    assert estante.stock_total() == 30