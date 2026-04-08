import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# 2. Estilo CSS (Simplificado y robusto)
st.markdown("""
    <style>
    .stApp { background-color: #F0F2F6; }
    
    /* Contenedor de la carta */
    .main-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.05);
        border-top: 6px solid #7B1FA2;
    }

    /* Badge del número al lado del nombre */
    .numero-badge {
        background-color: #7B1FA2;
        color: white;
        padding: 4px 12px;
        border-radius: 10px;
        font-size: 1.2rem;
        font-weight: bold;
        vertical-align: middle;
        margin-left: 10px;
    }

    /* Barra de datos inferior */
    .data-bar {
        display: flex;
        justify-content: space-around;
        background-color: #4A148C;
        color: white;
        padding: 12px;
        border-radius: 12px;
        margin-top: 15px;
        text-align: center;
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

    # 1. SELECCIÓN (Arriba)
    c1, c2 = st.columns([2, 1])
    with c1:
        carta_sel = st.selectbox("Carta:", df['Arcano'].unique())
    with c2:
        posicion = st.radio("Energía:", ["Derecha", "Invertida"], horizontal=True)
    
    fila = df[df['Arcano'] == carta_sel].iloc[0]

    # 2. MENSAJES ESPECÍFICOS (Ahora en la parte superior)
    st.markdown("### 🔍 Mensajes Específicos")
    t1, t2, t3, t4 = st.tabs(["❤️ Amor", "💼 Trabajo", "💰 Dinero", "🏥 Salud"])
    
    def render_content(col_name):
        texto = fila[col_name]
        if pd.notna(texto) and str(texto).strip() != "":
            st.info(texto)
        else:
            st.write("_Sin detalles disponibles._")

    with t1: render_content('Amor' if posicion == "Derecha" else 'Amor Inv')
    with t2: render_content('Trabajo' if posicion == "Derecha" else 'Trabajo Inv')
    with t3: render_content('Dinero' if posicion == "Derecha" else 'Dinero Inv')
    with t4: render_content('Salud' if posicion == "Derecha" else 'Salud Inv')

    st.divider()

    # 3. SIGNIFICADO PRINCIPAL (Debajo de los mensajes)
    color_vibe = "#2E7D32" if posicion == "Derecha" else "#C62828"
    palabra_clave = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']

    st.markdown(f"""
    <div class="main-card">
        <div style="margin-bottom: 10px;">
            <span style="color:{color_vibe}; font-size: 2.2rem; font-weight: bold;">{carta_sel}</span>
            <span class="numero-badge">#{fila['N°']}</span>
        </div>
        <h4 style="color:#7B1FA2; margin
