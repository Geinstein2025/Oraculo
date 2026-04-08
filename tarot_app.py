import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# 2. CSS PARA FONDO OSCURO TOTAL
st.markdown("""
    <style>
    /* CAMBIO DE FONDO TOTAL: Esto pinta hasta los bordes */
    .stApp, .main, .stAppHeader {
        background-color: #120522 !important; 
    }

    /* Forzar que todo texto sea BLANCO para que se vea sobre el fondo oscuro */
    p, span, label, h1, h2, h3, h4, b, .stRadio label {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    /* BARRA DE SELECCIÓN (Negra con borde brillante) */
    div[data-baseweb="select"] > div {
        background-color: #000000 !important;
        border: 2px solid #7B1FA2 !important;
    }

    /* CAJAS DE LECTURA (Un poco más claras que el fondo para dar relieve) */
    .caja-lectura {
        background-color: #2D144A !important; 
        color: #FFFFFF !important;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 1px solid #7B1FA2;
        line-height: 1.6;
        font-size: 1.1rem;
    }

    /* BADGES (Respuesta, Tiempo, #) */
    .mini-badge {
        background-color: #7B1FA2 !important;
        color: #FFFFFF !important;
        padding: 5px 12px;
        border-radius: 10px;
        font-weight: bold;
        margin-right: 5px;
        display: inline-block;
        border: 1px solid #FFFFFF;
    }

    /* Ajuste para los Tabs (Pestañas) */
    .stTabs [data-baseweb="tab"] {
        color: #FFFFFF !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #7B1FA2 !important;
        border-radius: 5px;
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
    st.markdown("<h1 style='text-align:center;'>🔮 MI ORÁCULO</h1>", unsafe_allow_html=True)

    # --- SECCIÓN SUPERIOR ---
    st.write("Elegir Arcano:")
    carta_sel = st.selectbox("", df['Arcano'].unique(), label_visibility="collapsed")
    
    fila = df[df['Arcano'] == carta_sel].iloc[0]

    col_r, col_b = st.columns([1, 1])
    with col_r:
        posicion = st.radio("Orientación:", ["Derecha", "Invertida"], horizontal=True)
    
    with col_b:
        st.markdown(f"""
            <div style="margin-top:10px;">
                <span class="mini-badge">R: {fila['SI/NO']}</span>
                <span class="mini-badge">T: {fila['Tiempo']}</span>
                <span class="mini-badge">#{fila['N°']}</span>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- CONTENIDO ---
    # Colores brillantes para que resalten en el fondo oscuro
    color_v = "#4CAF50" if posicion == "Derecha" else "#FF5252" # Verde y Rojo brillantes
    palabra_k = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']

    st.markdown(f"<h2 style='color:{color_v} !important;'>{carta_sel}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color:{color_v} !important;'>✨ {palabra_k}</h4>", unsafe_allow_html=True)
    
    # Significado
    st.write("📖 **Significado:**")
    st.markdown(f"<div class='caja-lectura'>{fila['Significado']}</div>", unsafe_allow_html=True)

    # Tabs
    st.write("🔍 **Detalles por área:**")
    t1, t2, t3, t4 = st.tabs(["❤️ Amor", "💼 Trabajo", "💰 Dinero", "🏥 Salud"])
    
    def render_tab(col):
        val = fila[col]
        st.markdown(f"<div class='caja-lectura'>{val if pd.notna(val) else 'Sin detalles'}</div>", unsafe_allow_html=True)

    with t1: render_tab('Amor' if posicion == "Derecha" else 'Amor Inv')
    with t2: render_tab('Trabajo' if posicion == "Derecha" else 'Trabajo Inv')
    with t3: render_tab('Dinero' if posicion == "Derecha" else 'Dinero Inv')
    with t4: render_tab('Salud' if posicion == "Derecha" else 'Salud Inv')

    # Representa
    st.write("💡 **Lo que representa:**")
    st.markdown(f"<div class='caja-lectura'>{fila['Que representa']}</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error: {e}")
