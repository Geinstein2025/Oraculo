import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# 2. CSS para Contraste Azul y Barra Negra
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

    /* CAJA DE TEXTO AZUL (Igual a la de Detalles Específicos) */
    .caja-azul {
        background-color: #E3F2FD !important; /* Azul suave */
        color: #1A1A1A !important;           /* Texto casi negro para lectura */
        padding: 15px;
        border-radius: 10px;
        line-height: 1.6;
        margin-bottom: 20px;
        border: 1px solid #BBDEFB;           /* Borde azul sutil */
    }

    /* ETIQUETAS COMPACTAS (Respuesta, Tiempo, etc) */
    .badge-container { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 10px; }
    .mini-badge {
        background-color: #F8F9FB;
        border: 1px solid #E1BEE7;
        color: #4A148C !important;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
    }
    
    /* Títulos y etiquetas */
    h1, h2, h3 { color: #4A148C !important; }
    .label-mistic { color: #4A148C !important; font-weight: bold; margin-bottom: 5px; display: block; }
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

    # --- 1. SECCIÓN SUPERIOR ---
    col_izq, col_der = st.columns([2, 1])

    with col_izq:
        st.write("**Elegir Arcano:**")
        carta_sel = st.selectbox("", df['Arcano'].unique(), label_visibility="collapsed")
    
    fila = df[df['Arcano'] == carta_sel].iloc[0]

    with col_der:
        posicion = st.radio("**Orientación:**", ["Derecha", "Invertida"], horizontal=True)
        st.markdown(f"""
            <div class="badge-container">
                <div class="mini-badge">R: {fila['SI/NO']}</div>
                <div class="mini-badge">T: {fila['Tiempo']}</div>
                <div class="mini-badge">#{fila['N°']}</div>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- 2. DETALLES ESPECÍFICOS (TABS) ---
    st.subheader("🔍 Detalles Específicos")
    tabs = st.tabs(["❤️ Amor", "💼 Trabajo", "💰 Dinero", "🏥 Salud"])
    
    def render_tab(col_name):
        texto = fila[col_name]
        if pd.notna(texto) and str(texto).strip() != "":
            # Usamos la misma clase de caja azul para coherencia
            st.markdown(f"<div class='caja-azul'>{texto}</div>", unsafe_allow_html=True)
        else: st.write("Sin detalles.")

    with tabs[0]: render_tab('Amor' if posicion == "Derecha" else 'Amor Inv')
    with tabs[1]: render_tab('Trabajo' if posicion == "Derecha" else 'Trabajo Inv')
    with tabs[2]: render_tab('Dinero' if posicion == "Derecha" else 'Dinero Inv')
    with tabs[3]: render_tab('Salud' if posicion == "Derecha" else 'Salud Inv')

    # --- 3. SIGNIFICADO (INTERPRETACIÓN) ---
    st.subheader("📖 Interpretación")
    
    color_vibe = "#2E7D32" if posicion == "Derecha" else "#C62828"
    palabra_clave = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']

    st.markdown(f"<h2 style='color:{color_vibe}; margin-bottom:0;'>{carta_sel}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color:{color_vibe}; margin-bottom:15px;'>✨ {palabra_clave}</h4>", unsafe_allow_html=True)
    
    # SIGNIFICADO CON CAJA AZUL
    st.markdown(f"<div class='caja-azul'>{fila['Significado']}</div>", unsafe_allow_html=True)
    
    # LO QUE REPRESENTA CON CAJA AZUL
    st.markdown("<span class='label-mistic'>💡 LO QUE REPRESENTA:</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='caja-azul'>{fila['Que representa']}</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error: {e}")
