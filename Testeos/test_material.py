import pytest
from material import Material


def test_crear_material():
    material = Material("Aluminio", "Al", "kg", 100)

    assert material.get_nombre() == "Aluminio"
    assert material.get_composicion() == "Al"
    assert material.get_unidad_medida() == "kg"
    assert material.get_punto_reposicion() == 100


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

    assert material.get_punto_reposicion() == 150


def test_necesita_reposicion_true():
    material = Material("Aluminio", "Al", "kg", 100)
    
    assert material.necesita_reposicion(80) is True


def test_necesita_reposicion_false():
    material = Material("Aluminio", "Al", "kg", 100)

    assert material.necesita_reposicion(150) is False


def test_stock_negativo():
    material = Material("Aluminio", "Al", "kg", 100)

    with pytest.raises(ValueError):
        material.necesita_reposicion(-20)


def test_stock_tipo_incorrecto():
    material = Material("Aluminio", "Al", "kg", 100)

    with pytest.raises(TypeError):
        material.necesita_reposicion("50")


def test_id_manual():
    Material.todos.clear()
    material = Material("Acero", "Fe", "kg", 50, id_manual=7)

    assert material.get_id_material() == 7


def test_a_fila():
    Material.todos.clear()
    material = Material("Aluminio", "Al", "kg", 100, id_manual=3)

    assert material.a_fila() == [3, "Aluminio", "Al", "kg", 100]


def test_id_nuevo():
    Material.todos.clear()
    Material("Aluminio", "Al", "kg", 100, id_manual=3)
    material = Material("Acero", "Fe", "kg", 50)

    assert material.get_id_material() == 4
