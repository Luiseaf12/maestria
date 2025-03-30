import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import os
import plotly.express as px
import plotly.graph_objects as go
from prophet.plot import plot_plotly
from plotly.subplots import make_subplots
import json


# Helper functions for HTML generation
def generate_table_rows(df):
    rows = ""
    for _, row in df.iterrows():
        rows += (
            f"<tr><td>{row['ds'].strftime('%Y-%m-%d')}</td><td>{row['y']}</td></tr>\n"
        )
    return rows


def generate_forecast_rows(forecast, df):
    rows = ""
    # Get the first 7 future days
    future_forecast = forecast[forecast["ds"] > df["ds"].max()].head(7)
    for _, row in future_forecast.iterrows():
        rows += f"<tr><td>{row['ds'].strftime('%Y-%m-%d')}</td><td>{row['yhat']:.2f}</td><td>{row['yhat_lower']:.2f}</td><td>{row['yhat_upper']:.2f}</td></tr>\n"
    return rows


# Cargar los datos del archivo JSON
json_file_path = "json_ventas.json"
ventas = []

if os.path.exists(json_file_path):
    try:
        with open(json_file_path, "r") as file:
            ventas = json.load(file)
        print(f"Datos cargados desde {json_file_path}")
    except Exception as e:
        print(f"Error al cargar el archivo JSON: {e}")
        # Si hay un error, usar una lista de datos vacía
else:
    print(f"El archivo {json_file_path} no existe.")

# Load data
df = pd.DataFrame(ventas)
# Convert dates to datetime format
df["ds"] = pd.to_datetime(df["ds"])

print(df.head())
print(f"Total de registros cargados: {len(df)}")

# Create the model
model = Prophet()
model.fit(df)

# Make predictions
future = model.make_future_dataframe(periods=365)
forecast = model.predict(future)

# Show results
print(forecast.tail())


# Función para mostrar ventas de abril del año pasado y predicción para este año
def mostrar_ventas_abril():
    # Obtener el año actual (2025)
    año_actual = 2025
    año_pasado = año_actual - 1

    # Ventas de abril del año pasado
    ventas_abril_pasado = df[
        (df["ds"].dt.month == 4) & (df["ds"].dt.year == año_pasado)
    ]

    # Predicción para abril de este año
    prediccion_abril_actual = forecast[
        (forecast["ds"].dt.month == 4) & (forecast["ds"].dt.year == año_actual)
    ]

    # Imprimir resultados
    if not ventas_abril_pasado.empty:
        ventas_total = ventas_abril_pasado["y"].sum()
        print(f"\nVentas en abril del {año_pasado}: {ventas_total:.2f}")
    else:
        print(f"\nNo hay datos de ventas para abril del {año_pasado}")

    if not prediccion_abril_actual.empty:
        prediccion_total = prediccion_abril_actual["yhat"].mean()
        print(
            f"Predicción de ventas para abril del {año_actual}: {prediccion_total:.2f}"
        )
    else:
        print(f"No hay predicciones para abril del {año_actual}")


# Ejecutar la función
mostrar_ventas_abril()

# Create HTML file for visualization
html_file = "sales_forecast.html"

# Check if file exists
if os.path.exists(html_file):
    print(f"El archivo {html_file} ya existe, será sobrescrito.")

# Create interactive plot with plotly
fig = plot_plotly(model, forecast)
fig.update_layout(
    title="Pronóstico de Ventas",
    xaxis_title="Fecha",
    yaxis_title="Ventas",
    legend_title="Leyenda",
)

# Create components plot
components_fig = make_subplots(
    rows=3, cols=1, subplot_titles=["Tendencia", "Patrón Semanal", "Patrón Anual"]
)

# Add trend
components_fig.add_trace(
    go.Scatter(x=forecast["ds"], y=forecast["trend"], mode="lines", name="Tendencia"),
    row=1,
    col=1,
)

# Add weekly seasonality if available
if "weekly" in forecast.columns:
    components_fig.add_trace(
        go.Scatter(
            x=forecast["ds"], y=forecast["weekly"], mode="lines", name="Patrón Semanal"
        ),
        row=2,
        col=1,
    )

# Add yearly seasonality if available
if "yearly" in forecast.columns:
    components_fig.add_trace(
        go.Scatter(
            x=forecast["ds"], y=forecast["yearly"], mode="lines", name="Patrón Anual"
        ),
        row=3,
        col=1,
    )

components_fig.update_layout(height=900, title_text="Componentes del Pronóstico")

# Generate table rows
table_rows = generate_table_rows(df)
forecast_rows = generate_forecast_rows(forecast, df)

# Create HTML file with both visualizations
with open(html_file, "w") as f:
    f.write(
        f"""
    <html>
    <head>
        <title>Pronóstico de Ventas</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }}
            h1, h2 {{
                color: #333;
            }}
            .plot-container {{
                width: 100%;
                height: 500px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
            tr:hover {{
                background-color: #f5f5f5;
            }}
        </style>
    </head>
    <body>
        <h1>Análisis de Pronóstico de Ventas</h1>
        
        <div class="container">
            <h2>Vista General del Pronóstico</h2>
            <div class="plot-container" id="forecast-plot"></div>
        </div>
        
        <div class="container">
            <h2>Componentes del Pronóstico</h2>
            <div class="plot-container" id="components-plot"></div>
        </div>
        
        <div class="container">
            <h2>Datos Históricos Recientes</h2>
            <table>
                <tr>
                    <th>Fecha</th>
                    <th>Ventas</th>
                </tr>
                {table_rows}
            </table>
        </div>
        
        <div class="container">
            <h2>Pronóstico Futuro (Próximos 7 Días)</h2>
            <table>
                <tr>
                    <th>Fecha</th>
                    <th>Pronóstico</th>
                    <th>Límite Inferior</th>
                    <th>Límite Superior</th>
                </tr>
                {forecast_rows}
            </table>
        </div>
        
        <script>
            var forecastPlot = {fig.to_json()}
            var componentsPlot = {components_fig.to_json()}
            
            Plotly.newPlot('forecast-plot', forecastPlot.data, forecastPlot.layout);
            Plotly.newPlot('components-plot', componentsPlot.data, componentsPlot.layout);
        </script>
    </body>
    </html>
    """
    )

print(f"Archivo HTML creado: {html_file}")
print(
    f"Abre este archivo en tu navegador web para ver la visualización interactiva del pronóstico"
)
