import streamlit as st

st.set_page_config(
    page_title="Sistema de Gestión de Productos",
    page_icon="🏭",
    layout="wide",
)

st.title("🏭 Sistema de Gestión de Productos")
st.markdown("""
Bienvenido al **Sistema de Gestión de Productos**.

Utiliza el menú de la izquierda para navegar entre las secciones:

- 📊 **Dashboard**: KPIs, gráficos y alertas de bajo stock
- 🛍️ **Productos**: Crear, editar, eliminar y filtrar productos
""")
