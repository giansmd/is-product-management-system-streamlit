import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api_client import get_analytics, list_low_stock, download_inventory_pdf

st.set_page_config(page_title="Dashboard — Inventario", page_icon="📊", layout="wide")

st.title("📊 Dashboard de Inventario")

try:
    analytics = get_analytics()
except Exception as e:
    st.error(f"No se pudo conectar al backend: {e}")
    st.stop()

kpis = analytics["kpis"]

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("📦 Total Productos", kpis["total_productos"])
col2.metric("💰 Valor Inventario", f"${float(kpis['valor_inventario']):,.2f}")
col3.metric("⚠️ Bajo Stock", kpis["productos_bajo_stock"])

mas_valioso = kpis.get("producto_mas_valioso")
if mas_valioso:
    col4.metric("🏆 Más Valioso", mas_valioso["nombre"], f"SKU: {mas_valioso['sku']}")
else:
    col4.metric("🏆 Más Valioso", "—")

st.divider()

# Charts
top_cat = analytics.get("top_categorias", [])
dist_cat = analytics.get("distribucion_categorias", [])

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("🏷️ Top Categorías por Productos")
    if top_cat:
        df_top = pd.DataFrame(top_cat)
        df_top["valor_total"] = df_top["valor_total"].astype(float)
        fig = px.bar(
            df_top,
            x="categoria",
            y="total_productos",
            color="valor_total",
            labels={"categoria": "Categoría", "total_productos": "Productos", "valor_total": "Valor ($)"},
            color_continuous_scale="Blues",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sin datos de categorías.")

with chart_col2:
    st.subheader("📈 Distribución por Categoría")
    if dist_cat:
        df_dist = pd.DataFrame(dist_cat)
        fig2 = px.pie(
            df_dist,
            names="categoria",
            values="total_productos",
            hole=0.4,
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Sin datos de distribución.")

st.divider()

# Low stock table
st.subheader("⚠️ Productos con Bajo Stock")
try:
    low_stock = list_low_stock()
    items = low_stock.get("items", [])
    if items:
        df_low = pd.DataFrame(items)[["sku", "nombre", "categoria", "stock_actual", "stock_minimo", "precio_venta"]]
        df_low.columns = ["SKU", "Nombre", "Categoría", "Stock Actual", "Stock Mínimo", "Precio Venta"]
        st.dataframe(df_low, use_container_width=True, hide_index=True)
    else:
        st.success("No hay productos con bajo stock. ✅")
except Exception as e:
    st.error(f"Error al obtener bajo stock: {e}")

st.divider()

# PDF report
st.subheader("📄 Descargar Reporte de Inventario (PDF)")
categorias_disponibles = ["Todas"] + [c["categoria"] for c in top_cat]
cat_sel = st.selectbox("Filtrar por categoría", categorias_disponibles)
if st.button("📥 Descargar PDF"):
    try:
        cat_param = None if cat_sel == "Todas" else cat_sel
        pdf_bytes = download_inventory_pdf(categoria=cat_param)
        filename = f"inventario{'_' + cat_sel if cat_sel != 'Todas' else ''}.pdf"
        st.download_button(
            label="💾 Guardar PDF",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf",
        )
    except Exception as e:
        st.error(f"Error al generar PDF: {e}")
