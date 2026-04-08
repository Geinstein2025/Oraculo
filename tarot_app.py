import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# 2. CSS Maestro de Alto Contraste
st.markdown("""
    <style>
    /* Fondo global místico claro */
    .stApp { background-color: #F8F9FB !important; }
    
    /* Fondo Blanco para tarjetas principales */
    .main-card {
        background-color: #FFFFFF !important;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.05);
        border-top: 6px solid #7B1FA2;
    }

    /* Estilo del Selector (Barra Negra) */
    div[data-baseweb="select"] > div {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border: 1px solid #7B1FA2 !important;
    }
    div[data-baseweb="select"] svg { fill: white !important; }

    /* --- SOLUCIÓN DE CONTRASTE: Caja de Significado --- */
    .significado-box {
        background-color: #E3F2FD !important; /* Azul Cielo Suave */
        color: #1F1F1F !important; /* Gris Carbón Oscuro para lectura */
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #2196F3; /* Borde azul para definición */
        line-height: 1.7;
        font-size: 1.1rem;
        margin-bottom: 20px;
    }

    /* Títulos de secciones */
    .section-title { color: #4A148C !important; font-weight: bold; font-size: 1.5rem; border-bottom: 2px solid #E1BEE7; margin: 15px 0; }
    .num-badge { background-color: #7B1FA2 !important; color: white !important; padding: 2px 10px; border-radius: 8px; font-weight: bold; }
    .mini-dato { background-color: #EDE7F6 !important; color: #4A148C !important; border: 1px solid #D1C4E9; padding: 4px 12px; border-radius: 15px; font-weight: bold; display: inline-block;}
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

    # --- 1. SELECCIÓN ---
    col_arc, col_ene = st.columns([2, 1])
    with col_arc:
        carta_sel = st.selectbox("Elige tu Arcano:", df['Arcano'].unique())
    
    fila = df[df['Arcano'] == carta_sel].iloc[0]
    
    with col_ene:
        posicion = st.radio("Orientación:", ["Derecha", "Invertida"], horizontal=True)
        st.markdown(f"""
            <div class="mini-dato">R: {fila['SI/NO']}</div>
            <div class="mini-dato">T: {fila['Tiempo']}</div>
        """, unsafe_allow_html=True)

    # --- 2. MENSAJES ESPECÍFICOS ---
    st.markdown('<div class="section-title">🔍 Mensajes Específicos</div>', unsafe_allow_html=True)
    tabs = st.tabs(["❤️ Amor", "💼 Trabajo", "💰 Dinero", "🏥 Salud"])
    
    def render_content(col_name):
        texto = fila[col_name]
        if pd.notna(texto) and str(texto).strip() != "":
            # Mismo fondo azul para consistencia
            st.markdown(f"<div style='background-color:#E3F2FD; color:#1F1F1F !important; padding:15px; border-radius:10px;'>{texto}</div>", unsafe_allow_html=True)
        else: st.write("Sin detalles.")

    with tabs[0]: render_content('Amor' if posicion == "Derecha" else 'Amor Inv')
    with tabs[1]: render_content('Trabajo' if posicion == "Derecha" else 'Trabajo Inv')
    with tabs[2]: render_content('Dinero' if posicion == "Derecha" else 'Dinero Inv')
    with tabs[3]: render_content('Salud' if posicion == "Derecha" else 'Salud Inv')

    # --- 3. CUERPO DE LA CARTA (DISEÑO DE ALTO CONTRASTE) ---
    st.markdown('<div class="section-title">📖 Significado Arcano</div>', unsafe_allow_html=True)
    
    color_vibe = "#2E7D32" if posicion == "Derecha" else "#C62828"
    palabra_clave = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']

    # Contenedor de la carta
    st.markdown(f"""
    <div class="main-card">
        <div style="display: flex; align-items: center; margin-bottom: 5px;">
            <span style="color:{color_vibe} !important; font-size: 2.2rem; font-weight: bold;">{carta_sel}</span>
            <span class="num-badge">#{fila['N°']}</span>
        </div>
        <div style="color:{color_vibe} !important; font-weight:bold; font-size:1.2rem; margin-bottom:15px;">
            ✨ {palabra_clave}
        </div>
        
        <div class="significado-box">
            {fila['Significado']}
        </div>
        
        <div style="margin-top:20px;">
            <b style="color:#4A148C !important;">💡 LO QUE REPRESENTA:</b>
            <div style="background-color:#F3F0F9; color:#1F1F1F !important; padding:12px; border-radius:10px; border-left:4px solid #7B1FA2;">
                {fila['Que representa']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error: {e}")
