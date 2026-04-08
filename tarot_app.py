import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# 2. CSS para visibilidad total
st.markdown("""
    <style>
    /* Forzamos fondo claro en la app */
    .stApp { background-color: #FFFFFF !important; }

    /* --- ESTILO DE LA BARRA DE SELECCIÓN --- */
    /* Fondo negro para la caja */
    div[data-baseweb="select"] > div {
        background-color: #1A1A1A !important;
        border: 1px solid #7B1FA2 !important;
    }

    /* ¡CLAVE!: Color de texto BLANCO para la opción seleccionada */
    div[data-baseweb="select"] div {
        color: #FFFFFF !important;
    }

    /* Color de las opciones dentro del menú desplegable */
    div[data-baseweb="popover"] li {
        color: #FFFFFF !important;
        background-color: #1A1A1A !important;
    }

    /* Color de la flechita */
    div[data-baseweb="select"] svg {
        fill: white !important;
    }

    /* Texto general de la app en negro para que se vea siempre */
    p, span, label, h1, h2, h3 { color: #000000 !important; }
    
    /* Títulos en morado */
    .titulo-morado { color: #4A148C !important; font-weight: bold; }
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
    st.markdown("<h1 class='titulo-morado' style='text-align:center;'>🔮 MI ORÁCULO</h1>", unsafe_allow_html=True)

    # --- 1. SELECCIÓN ---
    col_arc, col_ene = st.columns([2, 1])
    with col_arc:
        carta_sel = st.selectbox("Elige tu Arcano:", df['Arcano'].unique())
    
    fila = df[df['Arcano'] == carta_sel].iloc[0]
    
    with col_ene:
        posicion = st.radio("Orientación:", ["Derecha", "Invertida"], horizontal=True)

    # --- 2. RESUMEN RÁPIDO ---
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.info(f"**Respuesta:** {fila['SI/NO']}")
    c2.success(f"**Tiempo:** {fila['Tiempo']}")
    c3.warning(f"**Número:** #{fila['N°']}")

    # --- 3. SIGNIFICADO ---
    palabra_clave = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']
    
    st.subheader(f"✨ {palabra_clave}")
    st.write(fila['Significado'])
    
    st.markdown("---")
    st.markdown("**💡 LO QUE REPRESENTA:**")
    st.write(fila['Que represents'] if 'Que represents' in fila else fila['Que representa'])

    # --- 4. DETALLES ESPECÍFICOS ---
    st.subheader("🔍 Detalles Específicos")
    tabs = st.tabs(["❤️ Amor", "💼 Trabajo", "💰 Dinero", "🏥 Salud"])
    
    def render_tab(col_name):
        texto = fila[col_name]
        if pd.notna(texto) and str(texto).strip() != "":
            st.write(texto)
        else: st.write("Sin detalles adicionales.")

    with tabs[0]: render_tab('Amor' if posicion == "Derecha" else 'Amor Inv')
    with tabs[1]: render_tab('Trabajo' if posicion == "Derecha" else 'Trabajo Inv')
    with tabs[2]: render_tab('Dinero' if posicion == "Derecha" else 'Dinero Inv')
    with tabs[3]: render_tab('Salud' if posicion == "Derecha" else 'Salud Inv')

except Exception as e:
    st.error(f"Error al cargar: {e}")
