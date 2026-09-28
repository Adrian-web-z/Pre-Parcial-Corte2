[README.md.md](https://github.com/user-attachments/files/32771838/README.md.md)
# Caja de Recaudo con Tope de Seguridad — PagaYa S.A.S.

**Asignatura:** Programación de Computadores I  
**Institución:** Universidad de Santander (UDES)  
**Empresa:** PagaYa S.A.S.  
**Entorno de Ejecución:** Python 3.x / Google Colab  

---

## Integrantes del Equipo

* **Nikolas Peña Verdugo** — Código: `01251152021`
* **Adrian Felipe Romero Barajas** — Código: `01251152018`
* **Antonio Jose Rincon Herrera** — Código: `01251152001`

---

## Descripción del Proyecto

Este repositorio contiene la solución completa para el módulo de control de caja de la empresa **PagaYa S.A.S.**, dedicada a la recaudación de pagos de facturas de servicios para terceros. 

El sistema gestiona la atención al cliente por turnos, valida los montos ingresados, aplica políticas automatizadas de suspensión por seguridad cuando la caja alcanza o supera el **tope máximo de recaudo**, y ofrece un sistema integral de persistencia y gestión de turnos mediante un menú interactivo y exportación a archivos CSV.

---

## Requerimientos Funcionales Implementados

| Código | Requerimiento | Descripción / Estado |
| :--- | :--- | :--- |
| **RF1** | **Inicio de Turno** | Captura obligatoria del cajero y validación estricta del tope máximo (`tope > 0`). |
| **RF2** | **Atención de Clientes** | Procesamiento en orden de llegada, acumulación de efectivo y conteo de transacciones válidas. |
| **RF3** | **Validación de Montos** | Rechazo de montos `<= 0` y entradas no numéricas sin detener la ejecución ni alterar acumulados. |
| **RF4** | **Suspensión por Seguridad** | Detención automática al cumplir `recaudoTotal >= tope`. Registra la última transacción completa y muestra mensaje a tesorería. |
| **RF5** | **Cierre por Fin de Cola** | Finalización voluntaria del turno mediante la palabra clave `FIN` o el valor `0`. |
| **RF6** | **Reporte Final** | Generación de resumen detallado con formato estricto de moneda COP, cálculo de promedios (evitando división por cero) y motivo de cierre. |

---

## Reglas de Negocio y Características Adicionales

1. **Regla de Cruce de Tope:** Si el pago del último cliente hace que se supere el tope de seguridad, el monto **se registra completo** y luego se suspende la caja (el recaudo final puede ser superior al tope).
2. **Formato Monetario (COP):**
   * **Valores enteros:** Formateados con punto como separador de miles (ej: `$1.050.000`)[cite: 5].
   * **Promedios:** Formateados con punto de miles y coma decimal a dos posiciones (ej: `$350.000,00`)[cite: 5].
3. **Gestión CRUD de Turnos[cite: 5, 6]:**
   * **Crear:** Registro de turnos asignando un `ID` único incremental[cite: 5, 6].
   * **Leer / Consultar:** Visualización detallada del historial de turnos procesados[cite: 5].
   * **Actualizar:** Modificación del cajero asignado a un turno por su `ID`[cite: 5].
   * **Eliminar:** Borrado de registros de turno por `ID`[cite: 5].
4. **Persistencia en CSV[cite: 5, 6]:**
   * Lectura y escritura automática del archivo `turnos.csv` con codificación `utf-8-sig`[cite: 5].
   * Compatibilidad con descarga automática en entornos **Google Colab** (`google.colab.files.download`)[cite: 5].

---

## Estructura de Datos (Análisis y Diseño)

### Variables e Identificadores Principales

| Identificador | Tipo | Uso / Descripción |
| :--- | :--- | :--- |
| `cajero` | Texto | Nombre o código del cajero a cargo. |
| `tope` | Entero | Límite máximo de recaudo para el turno[cite: 6]. |
| `entradaMonto` | Texto | Entrada bruta ingresada por teclado[cite: 6]. |
| `recaudoTotal` | Entero | Suma de dinero recaudado en transacciones válidas[cite: 6]. |
| `numTransacciones` | Entero | Cantidad de pagos procesados con éxito[cite: 6]. |
| `promedio` | Real | Promedio por transacción (`recaudoTotal / numTransacciones`)[cite: 6]. |
| `motivoCierre` | Texto | `Tope alcanzado` o `Fin de cola`[cite: 6]. |
| `turnos` | Lista | Lista de diccionarios con el historial de la sesión[cite: 5, 6]. |

---

## Instalación y Ejecución

### Opción 1: Ejecución Local en Python

1. Clona este repositorio o descarga el archivo `caja_recaudo.py`[cite: 5]:
   ```bash
   git clone [https://github.com/Adrian-web-z/Pre-Parcial-Corte2.git](https://github.com/Adrian-web-z/Pre-Parcial-Corte2.git)
   cd tu-repositorio
