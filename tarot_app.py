import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# 2. CSS para Barra Negra y texto visible
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

    /* Texto general en negro */
    p, span, label { color: #000000 !important; }
    h1, h2, h3 { color: #4A148C !important; }

    /* Estilo para las cajitas de la derecha (Respuesta/Tiempo) */
    .dato-mini {
        border: 1px solid #E1BEE7;
        padding: 5px 10px;
        border-radius: 8px;
        font-size: 0.85rem;
        margin-bottom: 5px;
        background-color: #FDFBFF;
        display: block;
        text-align: center;
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

    # --- 1. SECCIÓN SUPERIOR REORGANIZADA ---
    col_izq, col_der = st.columns([2, 1])

    with col_izq:
        st.write("Elegir Arcano:")
        carta_sel = st.selectbox("", df['Arcano'].unique(), label_visibility="collapsed")
    
    fila = df[df['Arcano'] == carta_sel].iloc[0]

    with col_der:
        posicion = st.radio("Orientación:", ["Derecha", "Invertida"], horizontal=True)
        # Cajitas a la derecha debajo de la orientación
        st.markdown(f"""
            <div class="dato-mini"><b>Respuesta:</b> {fila['SI/NO']}</div>
            <div class="dato-mini"><b>Tiempo:</b> {fila['Tiempo']}</div>
            <div class="dato-mini"><b>Número:</b> #{fila['N°']}</div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- 2. DETALLES ESPECÍFICOS (TABS) ---
    st.subheader("🔍 Detalles Específicos")
    tabs = st.tabs(["❤️ Amor", "💼 Trabajo", "💰 Dinero", "🏥 Salud"])
    
    def render_tab(col_name):
        texto = fila[col_name]
        if pd.notna(texto) and str(texto).strip() != "":
            st.info(texto)
        else: st.write("Sin detalles.")

    with tabs[0]: render_tab('Amor' if posicion == "Derecha" else 'Amor Inv')
    with tabs[1]: render_tab('Trabajo' if posicion == "Derecha" else 'Trabajo Inv')
    with tabs[2]: render_tab('Dinero' if posicion == "Derecha" else 'Dinero Inv')
    with tabs[3]: render_tab('Salud' if posicion == "Derecha" else 'Salud Inv')

    # --- 3. SIGNIFICADO (ÁREA DE ABAJO) ---
    st.subheader("📖 Interpretación")
    
    color_vibe = "#2E7D32" if posicion == "Derecha" else "#C62828"
    palabra_clave = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']

    # Nombre y Palabra Clave
    st.markdown(f"<h2 style='color:{color_vibe}; margin-bottom:0;'>{carta_sel}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color:{color_vibe}; opacity:0.8;'>✨ {palabra_clave}</h4>", unsafe_allow_html=True)
    
    # Significado (Texto Negro Puro)
    st.write(fila['Significado'])
    
    st.write("")
    st.markdown("---")
    st.markdown("**💡 LO QUE REPRESENTA:**")
    st.write(fila['Que representa'])

except Exception as e:
    st.error(f"Error: {e}")
