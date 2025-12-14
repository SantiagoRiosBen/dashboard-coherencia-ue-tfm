# Dashboard de coherencia nutricional–asequibilidad en la Unión Europea (TFM UNIR)

Este repositorio contiene el código, los notebooks y el modelo de datos del Trabajo Fin de Máster **“Dashboard interactivo de coherencia nutricional–asequibilidad en la Unión Europea”** del Máster Universitario en Análisis y Visualización de Datos Masivos / Visual Analytics and Big Data (UNIR).

El objetivo del proyecto es **diseñar y documentar una metodología reproducible** que integre datos abiertos de composición de alimentos, precios y asequibilidad para caracterizar, por país y año, la relación entre el **perfil nutricional de la oferta alimentaria** y la **asequibilidad económica** en los países de la Unión Europea, a través de un dashboard interactivo en Power BI.

---

## Objetivos del proyecto

- Integrar datos abiertos de **OpenFoodFacts**, **Eurostat** y **FAOSTAT** por país y año.
- Definir un **índice sintético de perfil nutricional** basado en nutrientes críticos (energía, azúcares, grasas saturadas y sodio por 100 g).
- Construir un **panel analítico país–año** con indicadores nutricionales, de precios, gasto alimentario y asequibilidad.
- Desarrollar un **dashboard interactivo en Power BI** para explorar la coherencia nutricional–asequibilidad en la UE.
- Documentar el flujo de trabajo de forma **trazable y reproducible**, en coherencia con el marco **CRISP-DM**.

---

## Estructura del repositorio

La organización del proyecto sigue una estructura de carpetas orientada a separar claramente datos, código, notebooks y dashboard:

- `environment.yml`  
  Definición del entorno de conda utilizado en el proyecto (Python y principales bibliotecas).

- `README.md`  
  Este archivo. Describe el objetivo del proyecto, los requisitos y cómo reproducir el análisis.

- `data_raw/`  
  Estructura para almacenar los **ficheros originales** descargados de las fuentes oficiales (no se versionan por tamaño y licencias).  
  - `data_raw/openfoodfacts/`  
    Volcado completo de OpenFoodFacts (`en.openfoodfacts.org.products.csv`, etc.).  
  - `data_raw/eurostat/`  
    Tablas tabulares de Eurostat (`prc_hicp_aind_tabular.tsv`, `hbs_str_t211_tabular.tsv`, etc.).  
  - `data_raw/faostat/`  
    Ficheros CSV del dominio **Cost and Affordability of a Healthy Diet (CoAHD)** de FAOSTAT.

- `data_processed/`  
  Resultados intermedios y finales de los procesos ETL en formato **Parquet**.  
  - `data_processed/openfoodfacts/` – subconjuntos filtrados y con índice nutricional.  
  - `data_processed/eurostat/` – tablas HICP y HBS reestructuradas en formato largo.  
  - `data_processed/faostat/` – indicadores de coste y asequibilidad depurados.  
  - `data_processed/panel/` – panel analítico país–año (`panel_coherencia_ue.parquet`).

- `notebooks/`  
  Cuadernos de Jupyter que implementan la exploración de datos y los pipelines ETL.  
  - `notebooks/exploratory/`  
    Exploración y comprensión de cada fuente:
      - `01_exploracion_off.ipynb`
      - `02_exploracion_eurostat.ipynb`
      - `03_exploracion_faostat.ipynb`
      - `21_panel_indicadores_ue.ipynb` (exploración del panel integrado).
  - `notebooks/pipelines/`  
    Notebooks de **extracción, transformación y carga (ETL)**:
      - `01_pre_etl_openfoodfacts.ipynb`
      - `11_etl_off_ue.ipynb`
      - `12_etl_eurostat_hicp.ipynb`
      - `13_etl_eurostat_hbs.ipynb`
      - `14_etl_faostat.ipynb`
      - `21_indice_nutricional_off.ipynb`

- `src/`  
  Módulos Python reutilizables que apoyan a los notebooks:
  - `src/etl/` – funciones auxiliares para rutas, lectura/escritura y consultas con DuckDB.
  - `src/indicators/` – funciones para el cálculo del **índice sintético de perfil nutricional** y otros indicadores derivados.
  - `src/viz/` – funciones de apoyo a la preparación de datos para visualizaciones y análisis por cuadrantes.

- `dashboard/`  
  Archivo del dashboard desarrollado en Power BI:
  - `dashboard/dashboard.pbix` – informe interactivo con las tres páginas descritas en la memoria (visión general, relación perfil nutricional–coste de dieta saludable, precios y gasto alimentario).
  - `dashboard/README.md` – instrucciones específicas sobre la apertura y actualización del informe en Power BI.

- `.gitignore`  
  Configuración para excluir ficheros de gran tamaño y datos originales que no pueden redistribuirse.

---

## Requisitos previos

- **Python** 3.11 (gestionado a través de **conda** o **mamba**).
- **Anaconda** o **Miniconda** para gestionar el entorno definido en `environment.yml`.
- **Power BI Desktop** (versión indicada en `dashboard/README.md`) para abrir `dashboard/dashboard.pbix`.
- Espacio en disco suficiente para manejar los volcados de datos (especialmente el volcado de OpenFoodFacts, ~11 GB).

---

## Puesta en marcha rápida

1. **Clonar el repositorio**

    git clone https://github.com/SantiagoRiosBen/dashboard-coherencia-ue-tfm.git
    cd dashboard-coherencia-ue-tfm

2. **Crear el entorno de conda**

    conda env create -f environment.yml
    conda activate tfm_dashboard

3. **Descargar los datos originales**

   - Descargar el volcado de productos de **OpenFoodFacts** y guardarlo en `data_raw/openfoodfacts/`.
   - Descargar desde **Eurostat** las tablas:
     - `prc_hicp_aind` (HICP)
     - `hbs_str_t211` (HBS)  
     y guardarlas en `data_raw/eurostat/`.
   - Descargar desde **FAOSTAT** el dominio **Cost and Affordability of a Healthy Diet (CoAHD)** y guardar el fichero CSV en `data_raw/faostat/`.

   Las URLs concretas y detalles de licencia se describen en la memoria y en la documentación técnica de las fuentes. El repositorio **no** incluye estos ficheros por restricciones de licencia y tamaño.

4. **Ejecutar los notebooks ETL**

   Ejecutar, en este orden, los notebooks de `notebooks/pipelines/`:

    01_pre_etl_openfoodfacts.ipynb
    11_etl_off_ue.ipynb
    12_etl_eurostat_hicp.ipynb
    13_etl_eurostat_hbs.ipynb
    14_etl_faostat.ipynb
    21_indice_nutricional_off.ipynb

   Estos notebooks generan los ficheros Parquet en `data_processed/` y, finalmente, el panel país–año `data_processed/panel/panel_coherencia_ue.parquet`.

5. **Explorar el panel analítico (opcional)**

   El notebook `notebooks/exploratory/21_panel_indicadores_ue.ipynb` permite inspeccionar el panel integrado, revisar rangos de los indicadores y realizar gráficos exploratorios adicionales.

6. **Abrir el dashboard en Power BI**

   - Abrir `dashboard/dashboard.pbix` con Power BI Desktop.
   - Verificar que la ruta hacia `panel_coherencia_ue.parquet` apunta a la carpeta local `data_processed/panel/`. Si es necesario, actualizar la ruta en el origen de datos.
   - Refrescar los datos desde Power BI para cargar el panel reconstruido localmente.

---

## Uso del dashboard

El dashboard se organiza en tres páginas principales:

1. **Visión general UE**  
   - Mapa temático por país con el **índice nutricional medio** de la oferta.  
   - Ranking de países.  
   - Tarjetas de síntesis con: coste de una dieta saludable (PPP), porcentaje de gasto en alimentación, prevalencia de no asequibilidad y población afectada.

2. **Perfil nutricional y coste de dieta saludable**  
   - Gráfico de dispersión país–año con:
     - Eje X: índice nutricional medio.
     - Eje Y: coste de dieta saludable en dólares PPP por persona y día.
     - Tamaño de burbuja: porcentaje de gasto en alimentación.
   - Gráfico temporal con la evolución conjunta del HICP de alimentos y el índice nutricional medio.

3. **Precios, gasto alimentario y asequibilidad**  
   - Gráfico combinado (columnas + línea) con:
     - Porcentaje de gasto del hogar en alimentación.
     - Índice armonizado de precios de alimentos.
   - Tabla detallada país–año con todos los indicadores económicos y de asequibilidad.

En todas las páginas se incluyen segmentadores de **país** y **año**. Las medidas DAX se calculan, salvo en el caso de la población, como **medias simples de países–año**, tal y como se explica en la memoria.

---

## Licencias de datos y reutilización

Este repositorio se ha diseñado para ser compatible con las licencias de las fuentes originales:

- **OpenFoodFacts**  
  - Base de datos: Open Database Licence (ODbL).  
  - Contenidos: Database Contents License (DbCL).  
  - Imágenes: CC BY-SA.  
  No se redistribuyen los volcados originales ni una base integrada única. El repositorio proporciona scripts y notebooks para que cada usuario reconstruya los datos a partir de las fuentes oficiales.

- **Eurostat**  
  Datos reutilizables bajo **CC BY 4.0**, de acuerdo con la Decisión 2011/833/UE y las condiciones de Eurostat. Se requiere citar la fuente y la fecha de acceso y señalar las transformaciones realizadas.

- **FAOSTAT (FAO)**  
  Datos bajo licencia **CC BY 4.0**. Se sigue la fórmula de citación recomendada por FAO, indicando organización, año de actualización, dominio utilizado y fecha de acceso.

El código propio (notebooks y módulos en `src/`) se pone a disposición con la licencia especificada en el repositorio (si procede). En cualquier caso, el uso de los datos originales queda sujeto a las licencias de sus respectivos proveedores.

---

## Autoría y contacto

Este proyecto ha sido desarrollado por **Santiago Ríos Benjumea** como Trabajo Fin de Máster del **Máster Universitario en Análisis y Visualización de Datos Masivos / Visual Analytics and Big Data** de la **Universidad Internacional de La Rioja (UNIR)**.

Para cuestiones relacionadas con el código, la reproducción del análisis o el dashboard, pueden utilizarse los canales de contacto asociados al perfil de GitHub del autor.