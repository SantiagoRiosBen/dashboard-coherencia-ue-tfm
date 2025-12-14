\# Código fuente (`src`)



Esta carpeta está reservada para el \*\*código Python reutilizable\*\* del proyecto.  

Su objetivo es separar la lógica de negocio (ETL, indicadores, visualizaciones) de los notebooks, para que:



\- Los notebooks sean más ligeros y legibles.

\- Sea más fácil \*\*reutilizar funciones\*\*.

\- Se pueda evolucionar hacia un \*\*pipeline más modular y mantenible\*\*.



Actualmente contiene sólo parte del código, pero está pensada como espacio natural de extensión del proyecto.



---



\## 1. Estructura recomendada



Una estructura típica dentro de `src/` podría ser:



\- `src/etl/`  

&nbsp; Funciones de extracción, transformación y carga de cada fuente:

&nbsp; - OpenFoodFacts.

&nbsp; - Eurostat (HICP, HBS).

&nbsp; - FAOSTAT (CoAHD).

&nbsp; - Creación del panel país–año.



\- `src/indicators/`  

&nbsp; Funciones para:

&nbsp; - Calcular el índice sintético de perfil nutricional.

&nbsp; - Derivar indicadores agregados por país–año.

&nbsp; - Aplicar reglas de normalización, umbrales, etc.



\- `src/viz/`  

&nbsp; Utilidades para:

&nbsp; - Gráficos exploratorios en notebooks (matplotlib / plotly).

&nbsp; - Tablas de resumen estandarizadas.

&nbsp; - Exportación de figuras.



\- `src/utils/` (opcional)  

&nbsp; Funciones auxiliares genéricas:

&nbsp; - Manejo de rutas.

&nbsp; - Carga/guardado de ficheros Parquet.

&nbsp; - Logs sencillos y utilidades compartidas.



---



\## 2. Uso desde los notebooks



La idea es que los notebooks de `notebooks/pipelines/` y `notebooks/exploratory/` \*\*importen\*\* funciones desde `src` en lugar de duplicar código.



Ejemplo de patrón recomendado (en un notebook):



&nbsp;   from src.etl.openfoodfacts import build\_openfoodfacts\_subset

&nbsp;   from src.indicators.nutrition import compute\_off\_nutrient\_index



&nbsp;   df\_subset = build\_openfoodfacts\_subset(path\_raw, path\_processed)

&nbsp;   df\_index = compute\_off\_nutrient\_index(df\_subset)



Ventajas de este enfoque:



\- Si se corrige un bug, se corrige en un solo lugar.

\- Los notebooks quedan más centrados en el \*\*flujo\*\* y menos en el detalle de implementación.

\- Facilita escribir pruebas y extender el proyecto tras el TFM.



---



\## 3. Convenciones de código



Para mantener el código consistente, se recomienda:



\- \*\*Nombres de módulos y ficheros en minúsculas\*\*, con guiones bajos:

&nbsp; - `openfoodfacts.py`, `eurostat\_hicp.py`, `faostat\_cahd.py`, etc.

\- \*\*Funciones con verbos descriptivos\*\*:

&nbsp; - `load\_hicp\_raw()`, `clean\_hicp()`, `build\_panel\_country\_year()`.

\- \*\*Documentar cada función\*\* con docstrings tipo:



&nbsp;   def build\_panel\_country\_year(...):

&nbsp;       """

&nbsp;       Construye el panel analítico país–año combinando OpenFoodFacts, Eurostat y FAOSTAT.



&nbsp;       Parámetros

&nbsp;       ----------

&nbsp;       ...



&nbsp;       Retorna

&nbsp;       -------

&nbsp;       pandas.DataFrame

&nbsp;           DataFrame con una fila por combinación país–año.

&nbsp;       """



\- Evitar lógica “mágica” en los notebooks: si un bloque de código se repite o es complejo, conviene moverlo a `src/`.



---



\## 4. Dependencias y entorno



El código de `src/` asume que:



\- El entorno de Python se ha creado a partir de `environment.yml`.

\- Las rutas a `data\_raw/` y `data\_processed/` respetan la estructura descrita en los respectivos README.

\- El proyecto se ejecuta desde la raíz del repositorio (para que las rutas relativas funcionen correctamente).



En los módulos de `src/` se recomienda:



\- Trabajar con \*\*rutas relativas\*\* respecto a la raíz del proyecto.

\- Evitar rutas absolutas específicas del equipo local.

\- Documentar en los docstrings los supuestos sobre la estructura de carpetas.



---



\## 5. Buenas prácticas para extender `src/`



Si en el futuro se amplía el proyecto:



\- Crear nuevos módulos en la subcarpeta adecuada (`etl`, `indicators`, `viz`, etc.).

\- Mantener la \*\*separación de responsabilidades\*\*:

&nbsp; - ETL: solo limpieza, filtrado, agregación de datos.

&nbsp; - Indicadores: lógica de cálculo y normalización.

&nbsp; - Visualización: solo gráficos/tablas.

\- Considerar añadir:

&nbsp; - Pruebas básicas (por ejemplo, con `pytest`).

&nbsp; - Tipado opcional (anotaciones `-> DataFrame`, etc.).

&nbsp; - Un pequeño `CONTRIBUTING.md` si otras personas van a usar el repositorio.



---



\## 6. Checklist rápida



Antes de usar `src/` desde un notebook:



\- \[ ] ¿Se ha creado el entorno a partir de `environment.yml`?

\- \[ ] ¿Los módulos de `src/` tienen nombres coherentes y docstrings básicos?

\- \[ ] ¿Las rutas internas apuntan a `data\_raw/` y `data\_processed/` según lo descrito?

\- \[ ] ¿Los notebooks importan funciones desde `src/` en lugar de duplicar código?

