import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# 2. CSS Mínimo y Robusto (Solo para la barra negra y colores de texto)
st.markdown("""
    <style>
    /* Forzamos que la app sea clara */
    .stApp { background-color: white !important; }
    
    /* Selector de Arcanos: BARRA NEGRA / TEXTO BLANCO */
    div[data-baseweb="select"] > div {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
    }
    div[data-baseweb="select"] svg { fill: white !important; }
    
    /* Forzamos que TODO el texto sea negro para que no desaparezca */
    p, span, label, div { color: #000000 !important; }
    
    /* Títulos en morado para que se vea bonito */
    h1, h2, h3 { color: #4A148C !important; }
    
    /* Ajuste para que las pestañas (Tabs) se vean claras */
    .stTabs [data-baseweb="tab"] { color: #4A148C !important; }
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
    st.title("🔮 MI ORÁCULO")

    # --- 1. SELECCIÓN ---
    col_arc, col_ene = st.columns([2, 1])
    with col_arc:
        carta_sel = st.selectbox("Elige tu Arcano:", df['Arcano'].unique())
    
    fila = df[df['Arcano'] == carta_sel].iloc[0]
    
    with col_ene:
        posicion = st.radio("Orientación:", ["Derecha", "Invertida"], horizontal=True)

    # --- 2. DATOS RÁPIDOS (Respuesta y Tiempo) ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Respuesta", fila['SI/NO'])
    c2.metric("Tiempo", fila['Tiempo'])
    c3.metric("Número", f"#{fila['N°']}")

    st.divider()

    # --- 3. SIGNIFICADO PRINCIPAL ---
    # Usamos colores dinámicos pero con funciones simples de Streamlit
    color_vibe = "green" if posicion == "Derecha" else "red"
    palabra_clave = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']

    st.subheader(f"✨ {palabra_clave}")
    st.write(fila['Significado'])
    
    st.info(f"**LO QUE REPRESENTA:** \n{fila['Que representa']}")

    # --- 4. MENSAJES ESPECÍFICOS ---
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
    st.error(f"Hubo un detalle al cargar: {e}")
