import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Oráculo",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ESTILO CSS MEJORADO (Más luz y contraste)
st.markdown("""
    <style>
    /* Fondo gris pizarra suave, no negro total */
    .stApp {
        background-color: #F0F2F6;
        color: #1A1A1A;
    }
    
    /* Título principal con color vibrante */
    h1 {
        color: #4A148C;
        text-align: center;
        font-family: 'Helvetica';
        font-weight: 800;
        padding-bottom: 20px;
    }

    /* Caja blanca para los selectores (Contraste alto) */
    .stSelectbox, .stRadio {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* Pestañas (Tabs) más visibles */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #E1E4E8;
        border-radius: 10px;
        padding: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #4A4A4A !important;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        border-radius: 8px;
        color: #4A148C !important;
    }

    /* Tarjetas de información claras */
    .metric-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 20px;
        border-left: 8px solid #7B1FA2;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
        color: #1A1A1A;
    }
    
    /* Estilo para los textos de significado */
    .significado-box {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 20px;
        line-height: 1.6;
        font-size: 1.1rem;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# Conexión a tu Google Sheet
sheet_id = "1ZJNYTlIoEm8pmjw2lbjWFBENMitQy7NmG_oT5DhKkHA"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

@st.cache_data(ttl=60)
def cargar_datos():
    data = pd.read_csv(sheet_url)
    data.columns = [str(c).strip() for c in data.columns]
    return data

# --- CUERPO DE LA APP ---
st.markdown("<h1>🔮 MI ORÁCULO PERSONAL</h1>", unsafe_allow_html=True)

try:
    df = cargar_datos()
    
    # Contenedor para la selección
    with st.container():
        carta_sel = st.selectbox("Elije una carta del mazo:", df['Arcano'].unique())
        posicion = st.radio("Vibración de la carta:", ["Derecha", "Invertida"], horizontal=True)
    
    fila = df[df['Arcano'] == carta_sel].iloc[0]
    st.divider()

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style='margin-top:0; color:#7B1FA2;'>📋 Datos Clave</h3>
            <p style='font-size:1.1rem;'>
            <b>N°:</b> {fila['N°']}<br>
            <b>Respuesta:</b> {fila['SI/NO']}<br>
            <b>Tiempo:</b> {fila['Tiempo']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**💡 Representa:** {fila['Que representa']}")

    with col2:
        st.markdown("<div class='significado-box'>", unsafe_allow_html=True)
        if posicion == "Derecha":
            st.markdown(f"<h2 style='color:#2E7D32; margin-top:0;'>✨ {carta_sel}</h2>", unsafe_allow_html=True)
            st.success(f"**PALABRA CLAVE:** {fila['Palabra clave']}")
            st.write(fila['Significado'])
        else:
            st.markdown(f"<h2 style='color:#C62828; margin-top:0;'>🔄 {carta_sel} (Invertida)</h2>", unsafe_allow_html=True)
            st.warning(f"**PALABRA CLAVE:** {fila['Palabra invertida']}")
            st.write(fila['Significado']) 
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br><h3 style='text-align: center; color:#4A148C;'>🔍 Desglose por Temas</h3>", unsafe_allow_html=True)
    
    # Pestañas con fondo claro
    t1, t2, t3, t4 = st.tabs(["❤️ AMOR", "💼 TRABAJO", "💰 DINERO", "🏥 SALUD"])
    
    with t1:
        st.markdown("<div class='significado-box'>", unsafe_allow_html=True)
        st.write(fila['Amor'] if posicion == "Derecha" else fila['Amor Inv'])
        st.markdown("</div>", unsafe_allow_html=True)
    with t2:
        st.markdown("<div class='significado-box'>", unsafe_allow_html=True)
        st.write(fila['Trabajo'] if posicion == "Derecha" else fila['Trabajo Inv'])
        st.markdown("</div>", unsafe_allow_html=True)
    with t3:
        st.markdown("<div class='significado-box'>", unsafe_allow_html=True)
        st.write(fila['Dinero'] if posicion == "Derecha" else fila['Dinero Inv'])
        st.markdown("</div>", unsafe_allow_html=True)
    with t4:
        st.markdown("<div class='significado-box'>", unsafe_allow_html=True)
        st.write(fila['Salud'] if posicion == "Derecha" else fila['Salud Inv'])
        st.markdown("</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error al conectar con el Oráculo: {e}")
