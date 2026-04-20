import streamlit as st
import pandas as pd
from utils.api_client import (
    list_products,
    get_product,
    create_product,
    update_product,
    delete_product,
)

st.set_page_config(page_title="Gestión de Productos", page_icon="🛍️", layout="wide")

st.title("🛍️ Gestión de Productos")

# Tabs
tab_list, tab_create, tab_edit, tab_delete = st.tabs(
    ["📋 Listar / Filtrar", "➕ Crear", "✏️ Editar", "🗑️ Eliminar"]
)

# ── LIST / FILTER ──────────────────────────────────────────────────────────────
with tab_list:
    st.subheader("Filtros")
    fc1, fc2, fc3 = st.columns(3)
    filter_nombre = fc1.text_input("Nombre", key="filter_nombre")
    filter_sku = fc2.text_input("SKU", key="filter_sku")
    filter_cat = fc3.text_input("Categoría", key="filter_cat")

    try:
        result = list_products(
            nombre=filter_nombre or None,
            sku=filter_sku or None,
            categoria=filter_cat or None,
        )
        items = result.get("items", [])
        st.caption(f"Total: {result.get('total', 0)} productos")
        if items:
            df = pd.DataFrame(items)
            display_cols = ["id", "sku", "nombre", "categoria", "precio_compra", "precio_venta",
                            "stock_actual", "stock_minimo", "proveedor"]
            df_display = df[display_cols].copy()
            df_display.columns = ["ID", "SKU", "Nombre", "Categoría", "P. Compra", "P. Venta",
                                   "Stock Actual", "Stock Mínimo", "Proveedor"]
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        else:
            st.info("No se encontraron productos.")
    except Exception as e:
        st.error(f"Error: {e}")

# ── CREATE ─────────────────────────────────────────────────────────────────────
with tab_create:
    st.subheader("Nuevo Producto")
    with st.form("form_create"):
        c1, c2 = st.columns(2)
        sku = c1.text_input("SKU *")
        nombre = c2.text_input("Nombre *")
        descripcion = st.text_area("Descripción")
        c3, c4 = st.columns(2)
        categoria = c3.text_input("Categoría *")
        proveedor = c4.text_input("Proveedor")
        c5, c6 = st.columns(2)
        precio_compra = c5.number_input("Precio Compra *", min_value=0.0, step=0.01, format="%.2f")
        precio_venta = c6.number_input("Precio Venta *", min_value=0.0, step=0.01, format="%.2f")
        c7, c8 = st.columns(2)
        stock_actual = c7.number_input("Stock Actual *", min_value=0, step=1)
        stock_minimo = c8.number_input("Stock Mínimo *", min_value=0, step=1)
        submitted = st.form_submit_button("Crear Producto")

    if submitted:
        if not sku or not nombre or not categoria:
            st.error("SKU, Nombre y Categoría son obligatorios.")
        else:
            try:
                payload = {
                    "sku": sku, "nombre": nombre, "descripcion": descripcion,
                    "categoria": categoria, "proveedor": proveedor,
                    "precio_compra": precio_compra, "precio_venta": precio_venta,
                    "stock_actual": stock_actual, "stock_minimo": stock_minimo,
                }
                created = create_product(payload)
                st.success(f"Producto creado con ID {created['id']}")
            except Exception as e:
                st.error(f"Error al crear: {e}")

# ── EDIT ───────────────────────────────────────────────────────────────────────
with tab_edit:
    st.subheader("Editar Producto")
    edit_id = st.number_input("ID del producto a editar", min_value=1, step=1, key="edit_id")
    load_btn = st.button("Cargar datos", key="btn_load")

    if load_btn:
        try:
            product = get_product(int(edit_id))
            st.session_state["edit_product"] = product
        except Exception as e:
            st.error(f"Error al cargar: {e}")
            st.session_state.pop("edit_product", None)

    if "edit_product" in st.session_state:
        p = st.session_state["edit_product"]
        with st.form("form_edit"):
            ec1, ec2 = st.columns(2)
            e_sku = ec1.text_input("SKU", value=p["sku"])
            e_nombre = ec2.text_input("Nombre", value=p["nombre"])
            e_desc = st.text_area("Descripción", value=p.get("descripcion") or "")
            ec3, ec4 = st.columns(2)
            e_cat = ec3.text_input("Categoría", value=p["categoria"])
            e_prov = ec4.text_input("Proveedor", value=p.get("proveedor") or "")
            ec5, ec6 = st.columns(2)
            e_pc = ec5.number_input("Precio Compra", value=float(p["precio_compra"]), min_value=0.0, step=0.01, format="%.2f")
            e_pv = ec6.number_input("Precio Venta", value=float(p["precio_venta"]), min_value=0.0, step=0.01, format="%.2f")
            ec7, ec8 = st.columns(2)
            e_sa = ec7.number_input("Stock Actual", value=int(p["stock_actual"]), min_value=0, step=1)
            e_sm = ec8.number_input("Stock Mínimo", value=int(p["stock_minimo"]), min_value=0, step=1)
            save_btn = st.form_submit_button("Guardar cambios")

        if save_btn:
            try:
                payload = {
                    "sku": e_sku, "nombre": e_nombre, "descripcion": e_desc,
                    "categoria": e_cat, "proveedor": e_prov,
                    "precio_compra": e_pc, "precio_venta": e_pv,
                    "stock_actual": e_sa, "stock_minimo": e_sm,
                }
                updated = update_product(int(edit_id), payload)
                st.success(f"Producto ID {updated['id']} actualizado correctamente.")
                st.session_state["edit_product"] = updated
            except Exception as e:
                st.error(f"Error al actualizar: {e}")

# ── DELETE ─────────────────────────────────────────────────────────────────────
with tab_delete:
    st.subheader("Eliminar Producto")
    del_id = st.number_input("ID del producto a eliminar", min_value=1, step=1, key="del_id")
    if st.button("🗑️ Eliminar", key="btn_delete"):
        try:
            delete_product(int(del_id))
            st.success(f"Producto ID {del_id} eliminado correctamente.")
        except Exception as e:
            st.error(f"Error al eliminar: {e}")
