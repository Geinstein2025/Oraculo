import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# 2. CSS Blindado para visibilidad total
st.markdown("""
    <style>
    /* Fondo general */
    .stApp { 
        background-color: #F8F9FB !important; 
    }
    
    /* --- ESTILO PARA SELECTBOX (La barra de elegir carta) --- */
    /* Forzamos que la caja sea blanca y el texto negro */
    div[data-baseweb="select"] > div {
        background-color: white !important;
        color: #2D3436 !important;
        border: 1px solid #7B1FA2 !important;
    }
    
    /* Forzamos que la lista desplegable tenga texto visible */
    div[data-baseweb="popover"] li {
        color: #2D3436 !important;
        background-color: white !important;
    }

    /* Títulos y etiquetas */
    .stSelectbox label, .stRadio label {
        color: #4A148C !important;
        font-weight: bold !important;
    }

    .section-title {
        color: #4A148C !important;
        font-size: 1.5rem;
        font-weight: bold;
        border-bottom: 2px solid #E1BEE7;
        margin-bottom: 15px;
    }

    .num-badge {
        background-color: #7B1FA2 !important; 
        color: #FFFFFF !important;
        padding: 2px 10px; border-radius: 8px;
        font-weight: bold;
    }

    .mini-dato {
        background-color: #EDE7F6 !important;
        color: #4A148C !important;
        border: 1px solid #D1C4E9;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.85rem;
        display: inline-block;
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
    st.markdown("<h1 style='text-align:center; color:#4A148C;'>🔮 MI ORÁCULO</h1>", unsafe_allow_html=True)

    # --- 1. SELECCIÓN ---
    col_arc, col_ene = st.columns([2, 1])
    with col_arc:
        # Selector de carta
        carta_sel = st.selectbox("Elige tu Arcano:", df['Arcano'].unique())
    
    fila = df[df['Arcano'] == carta_sel].iloc[0]
    
    with col_ene:
        posicion = st.radio("Orientación:", ["Derecha", "Invertida"], horizontal=True)
        st.markdown(f"""
            <div class="mini-dato">Respuesta: {fila['SI/NO']}</div>
            <div class="mini-dato">Tiempo: {fila['Tiempo']}</div>
        """, unsafe_allow_html=True)

    # --- 2. MENSAJES ESPECÍFICOS ---
    st.markdown('<div class="section-title">🔍 Mensajes Específicos</div>', unsafe_allow_html=True)
    tabs = st.tabs(["❤️ Amor", "💼 Trabajo", "💰 Dinero", "🏥 Salud"])
    
    def render_content(col_name):
        texto = fila[col_name]
        if pd.notna(texto) and str(texto).strip() != "":
            st.markdown(f"<div style='color: #2D3436; background-color: #E3F2FD; padding: 15px; border-radius: 10px; line-height: 1.5;'>{texto}</div>", unsafe_allow_html=True)
        else: 
            st.write("Sin detalles específicos.")

    with tabs[0]: render_content('Amor' if posicion == "Derecha" else 'Amor Inv')
    with tabs[1]: render_content('Trabajo' if posicion == "Derecha" else 'Trabajo Inv')
    with tabs[2]: render_content('Dinero' if posicion == "Derecha" else 'Dinero Inv')
    with tabs[3]: render_content('Salud' if posicion == "Derecha" else 'Salud Inv')

    # --- 3. SIGNIFICADO ---
    st.markdown('<div class="section-title">📖 Significado Arcano</div>', unsafe_allow_html=True)
    
    color_vibe = "#2E7D32" if posicion == "Derecha" else "#C62828"
    palabra_clave = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']

    with st.container(border=True):
        st.markdown(f"""
            <div style="margin-bottom: 10px;">
                <span style="color:{color_vibe} !important; font-size: 2.2rem; font-weight: bold;">{carta_sel}</span>
                <span class="num-badge">#{fila['N°']}</span>
            </div>
            <p style="color:#7B1FA2 !important; font-weight:bold; font-size:1.1rem;">✨ {palabra_clave}</p>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<div style='color: #2D3436 !important; line-height: 1.6;'>{fila['Significado']}</div>", unsafe_allow_html=True)
        
        st.write("")
        st.markdown("<b style='color: #4A148C;'>💡 LO QUE REPRESENTA:</b>", unsafe_allow_html=True)
        st.success(fila['Que representa'])

except Exception as e:
    st.error(f"Error: {e}")
