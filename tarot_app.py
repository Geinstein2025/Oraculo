import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# 2. CSS para Barra Negra y Etiquetas Estilo Orientación
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    
    /* Selector: NEGRO / Texto: BLANCO */
    div[data-baseweb="select"] > div {
        background-color: #1A1A1A !important;
        border: 1px solid #7B1FA2 !important;
    }
    div[data-baseweb="select"] div { color: #FFFFFF !important; }
    div[data-baseweb="popover"] li { color: #FFFFFF !important; background-color: #1A1A1A !important; }
    div[data-baseweb="select"] svg { fill: white !important; }

    /* ETIQUETAS ESTILO ORIENTACIÓN (Pequeñas y en línea) */
    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
        margin-top: 10px;
    }
    .mini-badge {
        background-color: #F8F9FB;
        border: 1px solid #E1BEE7;
        color: #4A148C !important;
        padding: 2px 10px;
        border-radius: 20px; /* Redondeado como los botones de radio */
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
    }
    
    /* Forzar texto negro en lo demás */
    p, span, label { color: #000000 !important; }
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

    # --- 1. SECCIÓN SUPERIOR ---
    col_izq, col_der = st.columns([2, 1])

    with col_izq:
        st.write("**Elegir Arcano:**")
        carta_sel = st.selectbox("", df['Arcano'].unique(), label_visibility="collapsed")
    
    fila = df[df['Arcano'] == carta_sel].iloc[0]

    with col_der:
        posicion = st.radio("**Orientación:**", ["Derecha", "Invertida"], horizontal=True)
        
        # Etiquetas compactas estilo "orientación"
        st.markdown(f"""
            <div class="badge-container">
                <div class="mini-badge">R: {fila['SI/NO']}</div>
                <div class="mini-badge">T: {fila['Tiempo']}</div>
                <div class="mini-badge">#{fila['N°']}</div>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- 2. DETALLES ESPECÍFICOS ---
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

    # --- 3. SIGNIFICADO ---
    st.subheader("📖 Interpretación")
    color_vibe = "#2E7D32" if posicion == "Derecha" else "#C62828"
    palabra_clave = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']

    st.markdown(f"<h2 style='color:{color_vibe}; margin-bottom:0;'>{carta_sel}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color:{color_vibe};'>✨ {palabra_clave}</h4>", unsafe_allow_html=True)
    
    st.write(fila['Significado'])
    
    st.markdown("---")
    st.markdown("**💡 LO QUE REPRESENTA:**")
    st.write(fila['Que representa'])

except Exception as e:
    st.error(f"Error: {e}")
