import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA Y TEMA
st.set_page_config(
    page_title="Oráculo Personal",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ESTILO CSS PERSONALIZADO (Aquí es donde ocurre la magia visual)
st.markdown("""
    <style>
    /* Fondo místico y fuentes */
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    h1 {
        color: #9D50BB;
        text-align: center;
        font-family: 'Serif';
        text-shadow: 2px 2px 4px #000000;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1F2630;
        border-radius: 10px 10px 0px 0px;
        color: white;
        padding: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #6E48AA !important;
    }
    /* Tarjetas de información */
    .metric-card {
        background-color: #1F2630;
        padding: 15px;
        border-radius: 15px;
        border-left: 5px solid #9D50BB;
        margin-bottom: 10px;
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
st.title("✨ MI ORÁCULO MÍSTICO ✨")

try:
    df = cargar_datos()
    
    # Buscador elegante en la parte superior
    carta_sel = st.selectbox("🔮 Consulta tu Arcano:", df['Arcano'].unique())
    posicion = st.radio("Orientación de la energía:", ["Derecha", "Invertida"], horizontal=True)
    
    fila = df[df['Arcano'] == carta_sel].iloc[0]
    st.divider()

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style='margin:0;'>🗂️ Ficha Técnica</h3>
            <p><b>Número:</b> {fila['N°']}<br>
            <b>Respuesta:</b> {fila['SI/NO']}<br>
            <b>Tiempo:</b> {fila['Tiempo']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info(f"**Representa:** {fila['Que representa']}")

    with col2:
        if posicion == "Derecha":
            st.markdown(f"## {carta_sel} (Al Derecho)")
            st.success(f"**Palabra Clave:** {fila['Palabra clave']}")
            st.write(fila['Significado'])
        else:
            st.markdown(f"## {carta_sel} (Invertida)")
            st.warning(f"**Palabra Clave:** {fila['Palabra invertida']}")
            # Nota: Asegúrate de que tu Excel tenga columna 'Significado Inv' si quieres texto distinto
            st.write(fila['Significado']) 

    st.markdown("<br><h3 style='text-align: center;'>🔍 Enfoques Específicos</h3>", unsafe_allow_html=True)
    
    # Pestañas con Iconos
    t1, t2, t3, t4 = st.tabs(["❤️ AMOR", "💼 TRABAJO", "💰 DINERO", "🏥 SALUD"])
    
    with t1:
        st.write(fila['Amor'] if posicion == "Derecha" else fila['Amor Inv'])
    with t2:
        st.write(fila['Trabajo'] if posicion == "Derecha" else fila['Trabajo Inv'])
    with t3:
        st.write(fila['Dinero'] if posicion == "Derecha" else fila['Dinero Inv'])
    with t4:
        st.write(fila['Salud'] if posicion == "Derecha" else fila['Salud Inv'])

except Exception as e:
    st.error(f"Error al conectar con el Oráculo: {e}")
