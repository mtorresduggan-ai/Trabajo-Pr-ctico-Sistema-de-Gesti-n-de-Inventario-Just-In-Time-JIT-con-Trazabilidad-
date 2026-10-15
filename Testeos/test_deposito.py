import pytest
from deposito import Deposito
from estante import Estante
from datetime import date


def test_entrada_stock():
    deposito = Deposito("Principal")
    estante = Estante()

    estante.agregar_caja(date(2027, 5, 10), 100)
    deposito.stock["Aluminio"] = estante

    assert deposito.stock_total("Aluminio") == 100


def test_salida_stock():
    deposito = Deposito("Principal")
    estante = Estante()

    estante.agregar_caja(date(2027, 5, 10), 100)
    estante.sacar_cajas(30)
    deposito.stock["Aluminio"] = estante

    assert deposito.stock_total("Aluminio") == 70


def test_salida_de_varias_cajas():
    deposito = Deposito("Principal")
    estante = Estante()

    estante.agregar_caja(date(2027, 5, 10), 20)
    estante.agregar_caja(date(2027, 6, 10), 30)

    estante.sacar_cajas(35)
    deposito.stock["Aluminio"] = estante

    assert deposito.stock_total("Aluminio") == 15


def test_salida_sin_stock_suficiente():
    estante = Estante()
    estante.agregar_caja(date(2027, 5, 10), 20)

    try:
        estante.sacar_cajas(30)
        assert False
    except ValueError:
        assert estante.stock_total() == 20