\# Notebooks del proyecto



Esta carpeta contiene los cuadernos de Jupyter utilizados para explorar las fuentes de datos, ejecutar los procesos de ETL y construir el panel analítico país–año que alimenta el dashboard en Power BI.



La organización sigue la lógica del flujo de trabajo descrito en la memoria del TFM.



---



\## 1. Estructura general



\- `notebooks/exploratory/`  

&nbsp; Cuadernos de exploración y comprensión de datos. Se utilizan para inspeccionar las fuentes originales, verificar su estructura y calcular estadísticas descriptivas.



\- `notebooks/pipelines/`  

&nbsp; Cuadernos de tipo ETL (extracción, transformación y carga). A partir de las fuentes en `data\_raw` generan los ficheros intermedios y finales en `data\_processed`.



---



\## 2. Contenido de `notebooks/exploratory/`



Cuadernos orientados a entender cada fuente y el panel integrado:



\- `01\_exploracion\_off.ipynb`  

&nbsp; Exploración de la base de composición de alimentos de OpenFoodFacts:

&nbsp; - Lectura de una muestra del volcado original.

&nbsp; - Inspección de columnas relevantes (países, grupos PNNS, nutrientes por 100 g, fechas).

&nbsp; - Revisión de tasas de datos faltantes en los nutrientes críticos.

&nbsp; - Verificación de rangos y valores atípicos.



\- `02\_exploracion\_eurostat.ipynb`  

&nbsp; Exploración de las tablas de Eurostat:

&nbsp; - `prc\_hicp\_aind\_tabular.tsv` (HICP).

&nbsp; - `hbs\_str\_t211\_tabular.tsv` (HBS).

&nbsp; - Estructura de la columna compuesta (frecuencia, unidad, COICOP, país).

&nbsp; - Periodos disponibles y cobertura geográfica.

&nbsp; - Comprobación de valores especiales (datos faltantes, banderas, etc.).



\- `03\_exploracion\_faostat.ipynb`  

&nbsp; Exploración del dominio CoAHD de FAOSTAT:

&nbsp; - Estructura del fichero (Area, Item, Element, Year, Unit, Value, banderas).

&nbsp; - Rango temporal disponible y países incluidos.

&nbsp; - Tipo y formato de los valores numéricos.

&nbsp; - Identificación de los indicadores relevantes para el proyecto.



\- `21\_panel\_indicadores\_ue.ipynb`  

&nbsp; Exploración del panel integrado país–año:

&nbsp; - Lectura de `panel\_coherencia\_ue.parquet` desde `data\_processed/panel/`.

&nbsp; - Revisión de rangos, distribuciones y valores faltantes de los indicadores principales.

&nbsp; - Comprobaciones de consistencia entre el panel y las tablas procesadas de cada fuente.

&nbsp; - Primeras visualizaciones descriptivas (tablas y gráficos sencillos).



---



\## 3. Contenido de `notebooks/pipelines/`



Cuadernos que ejecutan los procesos ETL y generan los ficheros Parquet utilizados en el panel y el dashboard.



\### 3.1. OpenFoodFacts



\- `01\_pre\_etl\_openfoodfacts.ipynb`  

&nbsp; - Lectura del volcado original `en.openfoodfacts.org.products.csv` desde `data\_raw/openfoodfacts/`.

&nbsp; - Selección de un subconjunto de columnas relevantes (identificación, países, grupos PNNS, nutrientes por 100 g, fechas, etc.).

&nbsp; - Escritura de `openfoodfacts\_subset.parquet` en `data\_processed/openfoodfacts/`.



\- `11\_etl\_off\_ue.ipynb`  

&nbsp; - Filtrado del subconjunto de productos para:

&nbsp;   - Países de la Unión Europea (según etiquetas de país).

&nbsp;   - Periodo 2015–2023 (a partir de la fecha de última modificación).

&nbsp;   - Productos con los cuatro nutrientes críticos informados (energía, azúcares, grasas saturadas y sodio).

&nbsp; - Generación de `openfoodfacts\_eu\_nutri.parquet` en `data\_processed/openfoodfacts/`.



\- `21\_indice\_nutricional\_off.ipynb`  

&nbsp; - Cálculo de percentiles 5 y 95 para cada nutriente crítico.

&nbsp; - Normalización de energía, azúcares, grasas saturadas y sodio a escala 0–1, truncando en dichos percentiles.

&nbsp; - Construcción del índice sintético `off\_nutrient\_index` en escala 0–100.

&nbsp; - Agregación por país y año (medias de índice y variables normalizadas, proporción de productos con índice alto).

&nbsp; - Escritura de:

&nbsp;   - `openfoodfacts\_eu\_nutri\_index.parquet`

&nbsp;   - Tabla agregada `off\_agg.parquet` (según nomenclatura usada en el proyecto).



\### 3.2. Eurostat



\- `12\_etl\_eurostat\_hicp.ipynb`  

&nbsp; - Lectura de `prc\_hicp\_aind\_tabular.tsv` desde `data\_raw/eurostat/`.

&nbsp; - Separación de la columna compuesta en `freq`, `unit`, `coicop`, `geo`.

&nbsp; - Transformación de formato ancho a largo (unpivot de años).

&nbsp; - Limpieza de valores numéricos (sustitución de símbolos de datos faltantes, eliminación de banderas).

&nbsp; - Filtrado a:

&nbsp;   - Frecuencia anual.

&nbsp;   - Unidad de índice medio anual.

&nbsp;   - Países de la UE.

&nbsp;   - Años 2015–2023.

&nbsp; - Generación de `hicp\_eu27\_2015\_2023.parquet` y agregados por país y año (índice total y de alimentos).



\- `13\_etl\_eurostat\_hbs.ipynb`  

&nbsp; - Lectura de `hbs\_str\_t211\_tabular.tsv` desde `data\_raw/eurostat/`.

&nbsp; - Separación de la columna compuesta en campos atómicos.

&nbsp; - Transformación a formato largo y limpieza de valores.

&nbsp; - Filtrado a:

&nbsp;   - Frecuencia anual.

&nbsp;   - Unidad en porcentaje del gasto medio del hogar.

&nbsp;   - Países de la UE.

&nbsp; - Selección de la categoría de alimentos y bebidas no alcohólicas.

&nbsp; - Cálculo, para cada país, del:

&nbsp;   - Porcentaje del gasto en alimentación (`food\_budget\_share`).

&nbsp;   - Año de referencia de la encuesta (`hbs\_year`).

&nbsp; - Escritura de `hbs\_eu27\_long.parquet` y de la tabla resumida para el panel.



\### 3.3. FAOSTAT



\- `14\_etl\_faostat.ipynb`  

&nbsp; - Lectura de `FAOSTAT\_data\_en\_12-9-2025.csv` desde `data\_raw/faostat/`.

&nbsp; - Normalización de nombres de columnas y tipos.

&nbsp; - Conversión de la columna de valor a numérico y manejo de datos faltantes.

&nbsp; - Construcción de una tabla de correspondencia entre `Area` y códigos de país (ISO2) compatibles con Eurostat.

&nbsp; - Filtrado a:

&nbsp;   - Periodo 2017–2023.

&nbsp;   - Países de la Unión Europea.

&nbsp; - Derivación de indicadores clave por país y año:

&nbsp;   - `cohd\_lcu` (coste de dieta saludable en moneda local por persona y día).

&nbsp;   - `cohd\_ppp` (coste equivalente en dólares PPP).

&nbsp;   - `pua` (prevalencia de población que no puede costear una dieta saludable).

&nbsp;   - `pop\_unaffordable` (personas que no pueden costearla, en millones).

&nbsp; - Escritura de `faostat\_cahd\_eu27\_2017\_2023.parquet` en `data\_processed/faostat/`.



\### 3.4. Panel integrado



\- (Incluido en alguno de los cuadernos anteriores o en uno específico del panel, según versión del repositorio)  

&nbsp; - Unión de las tablas agregadas por país y año:

&nbsp;   - Nutrientes (OpenFoodFacts).

&nbsp;   - Precios (Eurostat HICP).

&nbsp;   - Estructura de gasto (Eurostat HBS).

&nbsp;   - Coste y asequibilidad de dieta saludable (FAOSTAT CoAHD).

&nbsp; - Construcción del fichero `panel\_coherencia\_ue.parquet` en `data\_processed/panel/`, utilizado posteriormente por el dashboard en Power BI.



---



\## 4. Orden recomendado de ejecución



1\. Preparar el entorno de Python a partir de `environment.yml` en la raíz del repositorio.

2\. Ejecutar los cuadernos de `notebooks/pipelines/` en el siguiente orden:

&nbsp;  1. `01\_pre\_etl\_openfoodfacts.ipynb`

&nbsp;  2. `11\_etl\_off\_ue.ipynb`

&nbsp;  3. `21\_indice\_nutricional\_off.ipynb`

&nbsp;  4. `12\_etl\_eurostat\_hicp.ipynb`

&nbsp;  5. `13\_etl\_eurostat\_hbs.ipynb`

&nbsp;  6. `14\_etl\_faostat.ipynb`

&nbsp;  7. Cuaderno de integración del panel (según nombre en la versión final del repositorio).

3\. Verificar, con `21\_panel\_indicadores\_ue.ipynb` en `notebooks/exploratory/`, que `panel\_coherencia\_ue.parquet` se ha generado correctamente.



---



\## 5. Requisitos de ejecución



Antes de ejecutar los notebooks:



\- Crear el entorno de trabajo a partir de `environment.yml` en la raíz del repositorio.

\- Activar el entorno y lanzar JupyterLab desde la raíz del proyecto.

\- Ajustar, si fuera necesario, las rutas relativas definidas en las primeras celdas de cada notebook, para que apunten correctamente a `data\_raw/` y `data\_processed/`.



Cada notebook incluye celdas iniciales donde se definen las rutas base del proyecto y se importan las bibliotecas necesarias. Se recomienda ejecutar los notebooks de principio a fin, sin saltar celdas intermedias.

