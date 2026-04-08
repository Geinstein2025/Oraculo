import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# 2. Estilo CSS Avanzado (Diseño Compacto y Elegante)
st.markdown("""
    <style>
    .stApp { background-color: #F0F2F6; }
    .main .block-container { padding-top: 1.5rem; }
    
    /* Título principal */
    .main-title {
        color: #4A148C;
        text-align: center;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 20px;
    }

    /* Tarjeta Principal de la Carta */
    .carta-container {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 20px;
        border-top: 10px solid #7B1FA2;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* Estilo del Nombre y Número */
    .nombre-carta {
        display: inline-block;
        font-size: 2.4rem;
        font-weight: 800;
        margin: 0;
    }
    .numero-carta {
        display: inline-block;
        font-size: 1.5rem;
        color: #7B1FA2;
        background: #F3E5F5;
        padding: 2px 12px;
        border-radius: 10px;
        vertical-align: middle;
        margin-left: 15px;
        font-weight: 600;
    }

    /* Ficha técnica horizontal */
    .ficha-tecnica {
        display: flex;
        justify-content: space-around;
        background: #4A148C;
        color: white;
        padding: 15px;
        border-radius: 15px;
        margin-top: 20px;
    }
    .ficha-item { text-align: center; }
    .ficha-label { font-size: 0.8rem; text-transform: uppercase; opacity: 0.8; }
    .ficha-valor { font-size: 1.2rem; font-weight: bold; }

    /* Ajuste de pestañas */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #E1E4E8;
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
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
    
    st.markdown("<div class='main-title'>🔮 MI ORÁCULO PERSONAL</div>", unsafe_allow_html=True)

    # Bloque de Selección Superior (Más compacto)
    col_a, col_b = st.columns([2, 1])
    with col_a:
        carta_sel = st.selectbox("Elige tu Arcano:", df['Arcano'].unique())
    with col_b:
        posicion = st.radio("Energía:", ["Derecha", "Invertida"], horizontal=True)
    
    fila = df[df['Arcano'] == carta_sel].iloc[0]
    st.write("")

    # --- DISEÑO DE LA CARTA ---
    color_vibe = "#2E7D32" if posicion == "Derecha" else "#C62828"
    palabra_clave = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']

    st.markdown(f"""
    <div class="carta-container">
        <div>
            <span class="nombre-carta" style="color:{color_vibe};">{carta_sel}</span>
            <span class="numero-carta">#{fila['N°']}</span>
        </div>
        <p style="color:#7B1FA2; font-weight:700; font-size:1.3rem; margin: 15px 0;">✨ {palabra_clave}</p>
        <p style="font-size:1.15rem; line-height:1.6; color:#333;">{fila['Significado']}</p>
        
        <div class="ficha-tecnica">
            <div class="ficha-item">
                <div class="ficha-label">Respuesta</div>
                <div class="ficha-valor">{fila['SI/NO']}</div>
            </div>
            <div class="ficha-item">
                <div class="ficha-label">Tiempo</div>
                <div class="ficha-valor">{fila['Tiempo']}</div>
            </div>
            <div class="ficha-item">
                <div class="ficha-label">Representa</div>
                <div class="ficha-valor" style="font-size:0.9rem;">{fila['Que representa']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- DETALLES ESPECÍFICOS ---
    st.markdown("### 🔍 Mensajes por
