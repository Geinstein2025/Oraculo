import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# 2. CSS Maestro para visibilidad en Celular
st.markdown("""
    <style>
    /* Forzamos fondo blanco en todo el celular */
    .stApp { background-color: #FFFFFF !important; }
    
    /* Selector de Arcano: BARRA NEGRA / TEXTO BLANCO */
    div[data-baseweb="select"] > div {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
    }
    div[data-baseweb="select"] div { color: #FFFFFF !important; }
    div[data-baseweb="select"] svg { fill: white !important; }

    /* TEXTO MORADO PARA TODO LO DEMÁS (Para que no desaparezca) */
    /* Esto incluye "Derecha", "Invertida", "Orientación" y los textos de las cajas */
    p, span, label, div[data-testid="stMarkdownContainer"] p, .stRadio label {
        color: #4A148C !important; 
        font-weight: 500 !important;
    }

    /* Títulos grandes en Morado */
    h1, h2, h3, h4 { color: #4A148C !important; }

    /* CAJA AZUL (Con texto morado para contraste) */
    .caja-azul {
        background-color: #E3F2FD !important;
        color: #4A148C !important;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #BBDEFB;
        margin-bottom: 15px;
        font-size: 1rem;
    }

    /* BADGES (Respuesta, Tiempo, #) */
    .badge-container { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 5px; }
    .mini-badge {
        background-color: #F3F0F9;
        border: 1px solid #D1C4E9;
        color: #4A148C !important;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
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
    # En celular, las columnas se apilan. Ponemos el selector arriba.
    st.write("**Elegir Arcano:**")
    carta_sel = st.selectbox("", df['Arcano'].unique(), label_visibility="collapsed")
    
    fila = df[df['Arcano'] == carta_sel].iloc[0]

    # Orientación y Badges
    col_radio, col_info = st.columns([1, 1])
    with col_radio:
        posicion = st.radio("**Orientación:**", ["Derecha", "Invertida"], horizontal=True)
    
    with col_info:
        st.markdown(f"""
            <div class="badge-container">
                <div class="mini-badge">R: {fila['SI/NO']}</div>
                <div class="mini-badge">T: {fila['Tiempo']}</div>
                <div class="mini-badge">#{fila['N°']}</div>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- SIGNIFICADO (INICIO) ---
    color_vibe = "#2E7D32" if posicion == "Derecha" else "#C62828"
    palabra_clave = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']

    st.markdown(f"<h2 style='color:{color_vibe};'>{carta_sel}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color:{color_vibe};'>✨ {palabra_clave}</h4>", unsafe_allow_html=True)
    
    # Caja azul con texto morado
    st.markdown(f"<div class='caja-azul'>{fila['Significado']}</div>", unsafe_allow_html=True)

    # --- TABS ---
    st.subheader("🔍 Detalles Específicos")
    tabs = st.tabs(["❤️ Amor", "💼 Trabajo", "💰 Dinero", "🏥 Salud"])
    
    def render_tab(col_name):
        texto = fila[col_name]
        if pd.notna(texto) and str(texto).strip() != "":
            st.markdown(f"<div class='caja-azul'>{texto}</div>", unsafe_allow_html=True)
        else: st.write("Sin detalles.")

    with tabs[0]: render_tab('Amor' if posicion == "Derecha" else 'Amor Inv')
    with tabs[1]: render_tab('Trabajo' if posicion == "Derecha" else 'Trabajo Inv')
    with tabs[2]: render_tab('Dinero' if posicion == "Derecha" else 'Dinero Inv')
    with tabs[3]: render_tab('Salud' if posicion == "Derecha" else 'Salud Inv')

    # --- LO QUE REPRESENTA ---
    st.markdown("### 💡 LO QUE REPRESENTA")
    st.markdown(f"<div class='caja-azul'>{fila['Que representa']}</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error: {e}")
