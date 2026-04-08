import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# 2. CSS DE ALTO CONTRASTE (Fondo Oscuro / Letra Blanca)
st.markdown("""
    <style>
    /* Fondo general de la app */
    .stApp { background-color: #FFFFFF !important; }

    /* BARRA DE SELECCIÓN (Negra total) */
    div[data-baseweb="select"] > div {
        background-color: #000000 !important;
        border: 1px solid #4A148C !important;
    }
    div[data-baseweb="select"] span { color: #FFFFFF !important; }
    div[data-baseweb="select"] svg { fill: #FFFFFF !important; }

    /* LAS CAJAS DE LECTURA (Fondo Morado Oscuro para que la letra blanca brille) */
    .caja-lectura {
        background-color: #1F0A33 !important; /* Morado muy oscuro, casi negro */
        color: #FFFFFF !important;           /* LETRA BLANCA */
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        border-left: 5px solid #7B1FA2;      /* Detalle lateral */
        line-height: 1.6;
        font-size: 1.1rem;
    }

    /* Forzamos que cualquier texto dentro de la caja sea blanco */
    .caja-lectura p, .caja-lectura span, .caja-lectura b {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    /* Etiquetas de Respuesta, Tiempo y Número */
    .mini-badge {
        background-color: #4A148C !important;
        color: #FFFFFF !important;
        padding: 5px 12px;
        border-radius: 10px;
        font-weight: bold;
        margin-right: 5px;
        display: inline-block;
        border: 1px solid #FFFFFF;
    }

    /* Títulos de secciones fuera de las cajas */
    .label-seccion {
        color: #4A148C !important;
        font-weight: bold;
        margin-top: 15px;
        display: block;
    }

    /* Radio buttons (Derecha/Invertida) */
    .stRadio label { color: #4A148C !important; font-weight: bold !important; }
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

    # --- SECCIÓN SUPERIOR ---
    st.markdown("<span class='label-seccion'>Elegir Arcano:</span>", unsafe_allow_html=True)
    carta_sel = st.selectbox("", df['Arcano'].unique(), label_visibility="collapsed")
    
    fila = df[df['Arcano'] == carta_sel].iloc[0]

    col_r, col_b = st.columns([1, 1])
    with col_r:
        posicion = st.radio("Orientación:", ["Derecha", "Invertida"], horizontal=True)
    
    with col_b:
        st.markdown(f"""
            <div style="margin-top:25px;">
                <span class="mini-badge">R: {fila['SI/NO']}</span>
                <span class="mini-badge">T: {fila['Tiempo']}</span>
                <span class="mini-badge">#{fila['N°']}</span>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- CONTENIDO PRINCIPAL ---
    color_v = "#2E7D32" if posicion == "Derecha" else "#C62828"
    palabra_k = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']

    st.markdown(f"<h2 style='color:{color_v};'>{carta_sel}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color:{color_v};'>✨ {palabra_k}</h4>", unsafe_allow_html=True)
    
    # Significado (Caja Oscura)
    st.markdown("<span class='label-seccion'>📖 Significado:</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='caja-lectura'>{fila['Significado']}</div>", unsafe_allow_html=True)

    # Detalles Específicos (Tabs)
    st.markdown("<span class='label-seccion'>🔍 Detalles por área:</span>", unsafe_allow_html=True)
    t1, t2, t3, t4 = st.tabs(["❤️ Amor", "💼 Trabajo", "💰 Dinero", "🏥 Salud"])
    
    def render_area(col):
        val = fila[col]
        st.markdown(f"<div class='caja-lectura'>{val if pd.notna(val) else 'Sin detalles'}</div>", unsafe_allow_html=True)

    with t1: render_area('Amor' if posicion == "Derecha" else 'Amor Inv')
    with t2: render_area('Trabajo' if posicion == "Derecha" else 'Trabajo Inv')
    with t3: render_area('Dinero' if posicion == "Derecha" else 'Dinero Inv')
    with t4: render_area('Salud' if posicion == "Derecha" else 'Salud Inv')

    # Representa
    st.markdown("<span class='label-seccion'>💡 Lo que representa:</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='caja-lectura'>{fila['Que representa']}</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error: {e}")
