import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# 2. CSS Optimizado para Móviles y Contraste
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    
    /* Barra de Selección: NEGRA / Texto: BLANCO */
    div[data-baseweb="select"] > div {
        background-color: #1A1A1A !important;
        border: 1px solid #7B1FA2 !important;
    }
    div[data-baseweb="select"] div { color: #FFFFFF !important; }
    div[data-baseweb="popover"] li { color: #FFFFFF !important; background-color: #1A1A1A !important; }
    div[data-baseweb="select"] svg { fill: white !important; }

    /* CAJA DE TEXTO AZUL (Contraste Asegurado) */
    .caja-azul {
        background-color: #E3F2FD !important;
        color: #000000 !important; /* Forzamos Negro Puro */
        padding: 18px;
        border-radius: 12px;
        line-height: 1.6;
        margin-top: 10px;
        margin-bottom: 20px;
        border: 1px solid #BBDEFB;
        font-size: 1rem;
    }

    /* Etiquetas de Respuesta/Tiempo (Estilo Compacto) */
    .badge-container { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; margin-bottom: 10px; }
    .mini-badge {
        background-color: #F0F2F6;
        border: 1px solid #D1C4E9;
        color: #4A148C !important;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: bold;
    }

    /* Forzar visibilidad de títulos */
    h1, h2, h3, h4 { color: #4A148C !important; margin-bottom: 5px !important; }
    b, strong { color: #000000 !important; }
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

    # --- 1. CONTROLES (Simplificados para que no desaparezcan) ---
    st.write("**Elegir Arcano:**")
    carta_sel = st.selectbox("", df['Arcano'].unique(), label_visibility="collapsed")
    
    fila = df[df['Arcano'] == carta_sel].iloc[0]

    # Orientación y Badges (en una sola línea o auto-ajustable)
    col_radio, col_badges = st.columns([1, 1])
    with col_radio:
        posicion = st.radio("**Orientación:**", ["Derecha", "Invertida"], horizontal=True)
    
    with col_badges:
        st.markdown(f"""
            <div class="badge-container">
                <div class="mini-badge">R: {fila['SI/NO']}</div>
                <div class="mini-badge">T: {fila['Tiempo']}</div>
                <div class="mini-badge">#{fila['N°']}</div>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- 2. SIGNIFICADO PRINCIPAL (INICIO) ---
    color_vibe = "#2E7D32" if posicion == "Derecha" else "#C62828"
    palabra_clave = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']

    st.markdown(f"<h2 style='color:{color_vibe};'>{carta_sel}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color:{color_vibe};'>✨ {palabra_clave}</h4>", unsafe_allow_html=True)
    
    # Caja Azul de Inicio
    st.markdown(f"<div class='caja-azul'>{fila['Significado']}</div>", unsafe_allow_html=True)

    # --- 3. DETALLES ESPECÍFICOS (TABS) ---
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

    # --- 4. LO QUE REPRESENTA ---
    st.markdown("<h3 style='color:#4A148C;'>💡 LO QUE REPRESENTA</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='caja-azul'>{fila['Que representa']}</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error: {e}")
