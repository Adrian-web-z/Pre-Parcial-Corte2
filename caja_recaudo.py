import csv

turnos = []
siguiente_id = 1
ARCHIVO = "turnos.csv"
ENCABEZADOS = [
    "ID",
    "Cajero",
    "Tope",
    "Transacciones",
    "RecaudoTotal",
    "Promedio",
    "MotivoCierre",
]


def formato_miles(valor):
    texto = f"{int(valor):,}".replace(",", ".")
    return f"${texto}"


def formato_promedio(valor):
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"${texto}"


def tope_valido(texto):
    try:
        numero = int(texto)
        return numero > 0, numero
    except ValueError:
        return False, 0


def interpretar_monto(texto):
    texto = texto.strip()
    if texto.upper() == "FIN" or texto == "0":
        return "cierre", 0
    try:
        numero = int(texto)
        if numero <= 0:
            return "invalido", 0
        return "valido", numero
    except ValueError:
        return "invalido", 0


def guardar_csv():
    with open(ARCHIVO, "w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.writer(archivo, delimiter=",")
        escritor.writerow(ENCABEZADOS)
        for t in turnos:
            escritor.writerow([
                t["id"],
                t["cajero"],
                t["tope"],
                t["transacciones"],
                t["recaudo"],
                round(t["promedio"], 2),
                t["motivo"],
            ])
    print(f"Archivo guardado: {ARCHIVO}")
    try:
        from google.colab import files
        files.download(ARCHIVO)
        print("Descarga iniciada en Colab.")
    except ImportError:
        print("El CSV quedó en la misma carpeta del programa.")


def cargar_csv():
    global siguiente_id
    try:
        with open(ARCHIVO, "r", newline="", encoding="utf-8-sig") as archivo:
            lector = csv.DictReader(archivo, delimiter=",")
            for fila in lector:
                turnos.append({
                    "id": int(fila["ID"]),
                    "cajero": fila["Cajero"],
                    "tope": int(fila["Tope"]),
                    "transacciones": int(fila["Transacciones"]),
                    "recaudo": int(fila["RecaudoTotal"]),
                    "promedio": float(fila["Promedio"]),
                    "motivo": fila["MotivoCierre"],
                })
        if len(turnos) > 0:
            siguiente_id = max(t["id"] for t in turnos) + 1
            print(f"Se cargaron {len(turnos)} turno(s) desde {ARCHIVO}.")
    except FileNotFoundError:
        pass


def iniciar_turno():
    global siguiente_id
    print("\n--- INICIO DE TURNO ---")
    cajero = input("Nombre o código del cajero: ").strip()
    while cajero == "":
        cajero = input("El cajero no puede quedar vacío. Ingrese de nuevo: ").strip()

    valido = False
    tope = 0
    while not valido:
        texto_tope = input("Tope máximo de recaudo (COP, entero mayor que 0): ")
        valido, tope = tope_valido(texto_tope)
        if not valido:
            print("Tope inválido. Debe ser un número entero mayor que cero.")

    recaudo = 0
    transacciones = 0
    motivo = "Fin de cola"
    print("\n--- ATENCIÓN DE CLIENTES ---")
    print("Ingrese el monto de cada cliente. 0 o FIN cierra la cola.")

    while True:
        entrada = input("Monto: ")
        tipo, monto = interpretar_monto(entrada)

        if tipo == "cierre":
            motivo = "Fin de cola"
            break

        if tipo == "invalido":
            print("Monto rechazado. Debe ser un entero mayor que 0.")
            continue

        recaudo = recaudo + monto
        transacciones = transacciones + 1
        print(f"Acumulado: {formato_miles(recaudo)}")

        if recaudo >= tope:
            print("CAJA SUSPENDIDA: se alcanzó el tope de recaudo. Diríjase a tesorería.")
            motivo = "Tope alcanzado"
            break

    if transacciones == 0:
        promedio = 0
    else:
        promedio = recaudo / transacciones

    print("\n===== REPORTE DE TURNO =====")
    print(f"Cajero:             {cajero}")
    print(f"Tope asignado:      {formato_miles(tope)}")
    print(f"Transacciones:      {transacciones}")
    print(f"Recaudo total:      {formato_miles(recaudo)}")
    print(f"Promedio/transacción: {formato_promedio(promedio)}")
    print(f"Motivo de cierre:   {motivo}")

    turnos.append({
        "id": siguiente_id,
        "cajero": cajero,
        "tope": tope,
        "transacciones": transacciones,
        "recaudo": recaudo,
        "promedio": promedio,
        "motivo": motivo,
    })
    print(f"Turno guardado con ID {siguiente_id}.")
    siguiente_id = siguiente_id + 1


def mostrar_turnos():
    if len(turnos) == 0:
        print("No hay turnos registrados.")
        return
    print("\n--- LISTA DE TURNOS ---")
    for t in turnos:
        print(f" ID {t['id']} | Cajero: {t['cajero']} | Tope: {formato_miles(t['tope'])}")
        print(f"    Transacciones: {t['transacciones']} | Recaudo: {formato_miles(t['recaudo'])}")
        print(f"    Promedio: {formato_promedio(t['promedio'])} | Motivo: {t['motivo']}")


def buscar_por_id(id_buscar):
    for i in range(len(turnos)):
        if turnos[i]["id"] == id_buscar:
            return i
    return -1


def editar_turno():
    if len(turnos) == 0:
        print("No hay turnos para editar.")
        return
    mostrar_turnos()
    try:
        id_buscar = int(input("ID del turno a editar: "))
    except ValueError:
        print("ID inválido.")
        return
    i = buscar_por_id(id_buscar)
    if i == -1:
        print("No existe ese ID.")
        return
    print(f"Editando turno {turnos[i]['id']} (cajero actual: {turnos[i]['cajero']})")
    nuevo_cajero = input("Nuevo nombre o código del cajero: ").strip()
    if nuevo_cajero != "":
        turnos[i]["cajero"] = nuevo_cajero
        print("Turno actualizado.")
    else:
        print("No se cambió el cajero.")


def eliminar_turno():
    if len(turnos) == 0:
        print("No hay turnos para eliminar.")
        return
    mostrar_turnos()
    try:
        id_buscar = int(input("ID del turno a eliminar: "))
    except ValueError:
        print("ID inválido.")
        return
    i = buscar_por_id(id_buscar)
    if i == -1:
        print("No existe ese ID.")
        return
    eliminado = turnos.pop(i)
    print(f"Se eliminó el turno ID {eliminado['id']} del cajero {eliminado['cajero']}.")


cargar_csv()
opcion = 0
while opcion != 6:
    print("\n-MENÚ PRINCIPAL-")
    print("1. Iniciar turno (atención de clientes)")
    print("2. Ver turnos")
    print("3. Editar turno (cajero)")
    print("4. Eliminar turno")
    print("5. Guardar y descargar CSV")
    print("6. Salir")
    try:
        opcion = int(input("Ingrese una opción (1-6): "))
    except ValueError:
        print("Opción no válida.")
        opcion = 0
        continue

    if opcion == 1:
        iniciar_turno()
    elif opcion == 2:
        mostrar_turnos()
    elif opcion == 3:
        editar_turno()
    elif opcion == 4:
        eliminar_turno()
    elif opcion == 5:
        if len(turnos) == 0:
            print("No hay turnos para guardar.")
        else:
            guardar_csv()
    elif opcion == 6:
        print("Gracias por usar el módulo de caja. Hasta luego.")
    else:
        print("Opción no válida. Ingrese un número del 1 al 6.")
