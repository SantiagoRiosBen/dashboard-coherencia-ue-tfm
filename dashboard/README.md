# Dashboard interactivo de coherencia nutricional–asequibilidad (Power BI)



Esta carpeta contiene el archivo del **dashboard interactivo** desarrollado en Power BI para el Trabajo Fin de Máster:



- `dashboard.pbix`  

&nbsp; Informe de Power BI que explota el panel analítico país–año construido a partir de datos de **OpenFoodFacts**, **Eurostat** y **FAOSTAT**.



El objetivo del dashboard es **visualizar de forma comparativa** la relación entre el **perfil nutricional de la oferta alimentaria** y la **asequibilidad económica** en los países de la Unión Europea, por país y año.



---



## Requisitos



- **Power BI Desktop** para Windows.  

&nbsp; Se recomienda utilizar una versión igual o posterior a la empleada en el TFM (indicar aquí la versión concreta cuando se conozca, por ejemplo: *2.133.x o superior*).



- Haber generado previamente el panel analítico:



&nbsp; - `data_processed/panel/panel_coherencia_ue.parquet`  



&nbsp; Este fichero se crea al ejecutar los notebooks ETL descritos en el README de la raíz del repositorio.



---



## Archivos de la carpeta



- `dashboard.pbix`  

&nbsp; Archivo principal del informe de Power BI. Incluye:

&nbsp; - Modelo de datos basado en la tabla **Panel** (panel país–año) y la dimensión **DimPais**.

&nbsp; - Medidas DAX para indicadores nutricionales, de precios, gasto y asequibilidad.

&nbsp; - Diseño de las tres páginas del dashboard.



---



## Cómo abrir el dashboard



1. Asegurarse de haber ejecutado los notebooks ETL y de disponer del fichero:



&nbsp;  - `data_processed/panel/panel_coherencia_ue.parquet`



2. Abrir **Power BI Desktop**.



3. En Power BI, seleccionar **Archivo → Abrir** y elegir:



&nbsp;  - `dashboard/dashboard.pbix`



4. Si Power BI muestra un aviso sobre rutas u orígenes de datos:



&nbsp;  - Ir a **Transformar datos → Orígenes de datos**.

&nbsp;  - Editar la ruta del origen que apunta a `panel_coherencia_ue.parquet` para que coincida con la ubicación local de:

&nbsp;    - `../data_processed/panel/panel_coherencia_ue.parquet`  

&nbsp;    (o la ruta absoluta correspondiente en tu equipo).



5. Una vez actualizada la ruta, seleccionar **Actualizar** para recargar los datos.



---



## Modelo de datos (vista general)



El modelo se ha mantenido deliberadamente sencillo:



- **Tabla de hechos**

&nbsp; - `Panel` – panel analítico país–año (`panel_coherencia_ue.parquet`).

&nbsp; - Contiene indicadores nutricionales, de precios, estructura de gasto y asequibilidad.



- **Dimensión**

&nbsp; - `DimPais` – tabla manual con códigos y nombres de países.



- **Relación**

&nbsp; - Relación uno-a-muchos de `DimPais[geo]` hacia `Panel[geo]`.



Las medidas DAX calculan principalmente:



- **Medias simples** para:

&nbsp; - Índice nutricional medio.

&nbsp; - Coste de dieta saludable (LCU, PPP).

&nbsp; - Índices HICP.

&nbsp; - Porcentaje de gasto en alimentación.

&nbsp; - Prevalencia de no asequibilidad.



- **Sumas** para:

&nbsp; - Población que no puede costear una dieta saludable (a partir de millones de personas).



Estas decisiones están documentadas en la memoria del TFM y deben tenerse en cuenta al interpretar los valores agregados.



---



## Páginas del informe



El informe se organiza en **tres páginas principales**, todas con segmentadores de **país** y **año**:



### 1. Visión general UE



- Mapa temático de Europa coloreado por **índice nutricional medio**.

- Gráfico de barras con ranking de países.

- Tarjetas de síntesis con:

&nbsp; - Índice nutricional medio.

&nbsp; - Coste de dieta saludable (PPP).

&nbsp; - Prevalencia de población que no puede costearla.

&nbsp; - Porcentaje del gasto del hogar en alimentación.

&nbsp; - (Opcionalmente) población total afectada.



Uso principal:  

Ofrece una vista rápida de las diferencias entre países y permite identificar casos destacados en términos de perfil nutricional y asequibilidad.



---



### 2. Perfil nutricional y coste de dieta saludable



- **Diagrama de dispersión** país–año:

&nbsp; - Eje X: índice nutricional medio.

&nbsp; - Eje Y: coste de dieta saludable en USD PPP/persona·día.

&nbsp; - Tamaño de burbuja: porcentaje del gasto del hogar en alimentación.

&nbsp; - Color: país.

- **Gráfico temporal**:

&nbsp; - Evolución del índice HICP de alimentos.

&nbsp; - Evolución del índice nutricional medio.



Uso principal:  

Permite lecturas por **cuadrantes** y análisis de coherencia entre perfil nutricional, coste de la dieta y presión presupuestaria.



---



### 3. Precios, gasto alimentario y asequibilidad



- **Gráfico combinado**:

&nbsp; - Columnas: porcentaje del gasto del hogar en alimentación.

&nbsp; - Línea: índice armonizado de precios de alimentos (HICP).

- **Tabla detallada país–año**:

&nbsp; - Coste de dieta saludable (PPP).

&nbsp; - Índices HICP (total y alimentos).

&nbsp; - Porcentaje de gasto alimentario.

&nbsp; - Prevalencia de no asequibilidad.

&nbsp; - Población que no puede costear una dieta saludable.



Uso principal:  

Explorar la relación entre **inflación de alimentos**, **peso del gasto** y **asequibilidad** en distintos países y periodos.



---



## Interpretación y advertencias



- Las medidas mostradas en tarjetas y gráficos (excepto población) son **medias simples** de los países/países–año seleccionados, **no** promedios ponderados por población ni por volumen de consumo.

- El índice nutricional sintético se interpreta como **indicador relativo** construido a partir de OpenFoodFacts (oferta registrada), no como medida normativa ni como estimación exacta de la dieta real.

- El dashboard tiene un propósito **descriptivo y exploratorio**; no establece relaciones causales entre nutrición, precios y asequibilidad.



Estas advertencias se resumen también en la memoria del TFM y deben tenerse presentes al utilizar el informe para análisis o presentaciones.



---



## Licencias y uso de datos



El archivo PBIX utiliza datos derivados de:



- **OpenFoodFacts** (ODbL + DbCL + CC BY-SA).

- **Eurostat** (CC BY 4.0).

- **FAOSTAT (FAO)** (CC BY 4.0).



El repositorio no redistribuye las bases originales; el usuario debe descargarlas desde las fuentes oficiales y respetar sus **condiciones de reutilización**. Cualquier uso del dashboard con datos actualizados o modificados debe citar adecuadamente las fuentes y señalar que se han realizado transformaciones.



---
