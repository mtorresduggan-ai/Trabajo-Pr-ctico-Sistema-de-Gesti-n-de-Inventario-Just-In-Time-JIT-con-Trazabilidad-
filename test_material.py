import pytest
from material import Material


def test_crear_material():
    material = Material("Aluminio", "Al", "kg", 100)

    assert material.nombre == "Aluminio"
    assert material.composicion == "Al"
    assert material.unidad_medida == "kg"
    assert material.punto_reposicion == 100


def test_nombre_invalido():
    with pytest.raises(TypeError):
        Material(123, "Al", "kg", 100)


def test_nombre_vacio():
    with pytest.raises(ValueError):
        Material("", "Al", "kg", 100)


def test_punto_reposicion_negativo():
    with pytest.raises(ValueError):
        Material("Aluminio", "Al", "kg", -10)


def test_set_punto_reposicion():
    material = Material("Aluminio", "Al", "kg", 100)

    material.set_punto_reposicion(150)

    assert material.punto_reposicion == 150


def test_necesita_reposicion_true():
    material = Material("Aluminio", "Al", "kg", 100)

    assert material.necesita_reposicion(80) == True


def test_necesita_reposicion_false():
    material = Material("Aluminio", "Al", "kg", 100)

    assert material.necesita_reposicion(150) == False


def test_stock_negativo():
    material = Material("Aluminio", "Al", "kg", 100)

    with pytest.raises(ValueError):
        material.necesita_reposicion(-20)