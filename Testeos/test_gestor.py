
from gestor_archivos import GestorArchivos


def test_escribir_csv():
    resultado = GestorArchivos.escribir_csv(
        "prueba.csv",
        ["id", "nombre"],
        [[1, "Aluminio"], [2, "Acero"]]
    )

    assert resultado is True


def test_leer_csv():
    datos = GestorArchivos.leer_csv_dict("prueba.csv")

    assert len(datos) == 2
    assert datos[0]["nombre"] == "Aluminio"
    assert datos[1]["nombre"] == "Acero"


def test_leer_csv_inexistente():
    datos = GestorArchivos.leer_csv_dict("archivo_que_no_existe.csv")

    assert datos == []
