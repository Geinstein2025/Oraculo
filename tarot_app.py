import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# 2. Estilo CSS Seguro
st.markdown("""
    <style>
    .stApp { background-color: #F0F2F6; }
    
    /* Contenedor de la carta */
    .main-card {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.05);
        border-top: 6px solid #7B1FA2;
    }

    /* Badge del número */
    .numero-badge {
        background-color: #7B1FA2;
        color: white;
        padding: 4px 12px;
        border-radius: 10px;
        font-size: 1.2rem;
        font-weight: bold;
        display: inline-block;
        margin-left: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Carga de datos
sheet_id = "1ZJNYTlIoEm8pmjw2lbjWFBENMitQy7NmG_oT5DhKkHA"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

@st.cache_data(ttl=60)
def cargar_datos():
    data = pd.read_csv(sheet_url)
    data.columns = [str(c).strip() for c in data.columns]
    return data

try:
    df = cargar_datos()
    st.markdown("<h1 style='text-align:center; color:#4A148C;'>🔮 MI ORÁCULO</h1>", unsafe_allow_html=True)

    # --- 1. SELECTORES (Corregidos) ---
    col_arcano, col_energia = st.columns([2, 1])
    with col_arcano:
        lista_cartas = df['Arcano'].unique()
        carta_sel = st.selectbox("Selecciona tu Arcano:", lista_cartas)
    
    with col_energia:
        posicion = st.radio("Orientación:", ["Derecha", "Invertida"], horizontal=True)
    
    fila = df[df['Arcano'] == carta_sel].iloc[0]

    # --- 2. MENSAJES ESPECÍFICOS (Arriba) ---
    st.markdown("### 🔍 Mensajes Específicos")
    t1, t2, t3, t4 = st.tabs(["❤️ Amor", "💼 Trabajo", "💰 Dinero", "🏥 Salud"])
    
    def render_content(col_name):
        texto = fila[col_name]
        if pd.notna(texto) and str(texto).strip() != "":
            st.info(texto)
        else:
            st.write("_Sin detalles específicos._")

    with t1: render_content('Amor' if posicion == "Derecha" else 'Amor Inv')
    with t2: render_content('Trabajo' if posicion == "Derecha" else 'Trabajo Inv')
    with t3: render_content('Dinero' if posicion == "Derecha" else 'Dinero Inv')
    with t4: render_content('Salud' if posicion == "Derecha" else 'Salud Inv')

    st.divider()

    # --- 3. SIGNIFICADO Y FICHA TÉCNICA (Diseño Robusto) ---
    color_vibe = "#2E7D32" if posicion == "Derecha" else "#C62828"
    palabra_clave = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']

    # Encabezado de la carta
    st.markdown(f"""
    <div class="main-card">
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <span style="color:{color_vibe}; font-size: 2.2rem; font-weight: bold;">{carta_sel}</span>
            <span class="numero-badge">#{fila['N°']}</span>
        </div>
        <h4 style="color:#7B1FA2; margin: 10px 0;">✨ {palabra_clave}</h4>
        <p style="font-size:1.1rem; line-height:1.6; color:#333;">{fila['Significado']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Barra de datos usando columnas nativas (Esto NO falla)
    st.
