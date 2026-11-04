from gestor_archivos import GestorArchivos


def test_escribir_csv(tmp_path):
    ruta = tmp_path / "prueba.csv"

    resultado = GestorArchivos.escribir_csv(
        ruta,
        ["id", "nombre"],
        [[1, "Aluminio"], [2, "Acero"]]
    )

    assert resultado is True


def test_leer_csv(tmp_path):
    ruta = tmp_path / "prueba.csv"
    GestorArchivos.escribir_csv(ruta, ["id", "nombre"], [[1, "Aluminio"], [2, "Acero"]])

    datos = GestorArchivos.leer_csv_dict(ruta)

    assert len(datos) == 2
    assert datos[0]["nombre"] == "Aluminio"
    assert datos[1]["nombre"] == "Acero"


def test_leer_csv_inexistente(tmp_path):
    datos = GestorArchivos.leer_csv_dict(tmp_path / "archivo_que_no_existe.csv")

    assert datos == []