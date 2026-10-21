import pytest

from datetime import date
from deposito import Deposito
from estante import Estante
from material import Material


def test_get_nombre():
    deposito = Deposito("Principal")

    assert deposito.get_nombre() == "Principal"


def test_set_nombre():
    deposito = Deposito("Principal")
    deposito.set_nombre("Secundario")

    assert deposito.get_nombre() == "Secundario"


def test_get_stock():
    deposito = Deposito("Principal")

    assert deposito.get_stock() == {}


def test_set_stock():
    deposito = Deposito("Principal")
    material = Material("Aluminio", "Metal", "kg", 20)
    estante = Estante()
    nuevo_stock = {material: estante}

    deposito.set_stock(nuevo_stock)

    assert deposito.get_stock() == nuevo_stock


def test_stock_total():
    deposito = Deposito("Principal")
    material = Material("Aluminio", "Metal", "kg", 20)
    estante = Estante()

    estante.agregar_caja(date(2027, 5, 10), 100)
    estante.agregar_caja(date(2027, 6, 10), 50)
    deposito.set_stock({material: estante})

    assert deposito.stock_total(material) == 150


def test_stock_total_material_inexistente():
    deposito = Deposito("Principal")
    material = Material("Aluminio", "Metal", "kg", 20)

    assert deposito.stock_total(material) == 0


def test_str():
    deposito = Deposito("Principal")
    material = Material("Aluminio", "Metal", "kg", 20)
    estante = Estante()

    estante.agregar_caja(date(2027, 5, 10), 100)
    deposito.set_stock({material: estante})

    resultado = str(deposito)

    assert "Aluminio" in resultado
    assert "100 kg" in resultado
    assert "2027-05-10" in resultado