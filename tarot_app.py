import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# 2. Estilo CSS para optimizar espacio
st.markdown("""
    <style>
    .stApp { background-color: #F0F2F6; }
    .header-container { display: flex; align-items: center; gap: 10px; }
    .num-badge {
        background-color: #7B1FA2; color: white;
        padding: 2px 8px; border-radius: 6px;
        font-weight: bold; font-size: 0.9rem;
    }
    /* Estilo para las etiquetas pequeñas de datos */
    .mini-dato {
        background-color: #FFFFFF;
        border: 1px solid #7B1FA2;
        padding: 5px 10px;
        border-radius: 8px;
        font-size: 0.85rem;
        display: inline-block;
        margin-right: 5px;
        margin-top: 5px;
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
    st.markdown("<h1 style='text-align:center; color:#4A148C; margin-bottom:0;'>🔮 MI ORÁCULO</h1>", unsafe_allow_html=True)

    # --- 1. SELECCIÓN Y DATOS RÁPIDOS (ZONA SUPERIOR) ---
    col_arc, col_ene = st.columns([2, 1])
    
    with col_arc:
        carta_sel = st.selectbox("Elige tu Arcano:", df['Arcano'].unique())
    
    fila = df[df['Arcano'] == carta_sel].iloc[0]
    
    with col_ene:
        posicion = st.radio("Orientación:", ["Derecha", "Invertida"], horizontal=True)
        # AQUÍ UBICAMOS LOS DATOS DE RESPUESTA Y TIEMPO (Debajo de la radio)
        st.markdown(f"""
            <div class="mini-dato"><b>R:</b> {fila['SI/NO']}</div>
            <div class="mini-dato"><b>T:</b> {fila['Tiempo']}</div>
        """, unsafe_allow_html=True)

    # --- 2. MENSAJES ESPECÍFICOS ---
    st.write("")
    st.markdown("### 🔍 Mensajes Específicos")
    tabs = st.tabs(["❤️ Amor", "💼 Trabajo", "💰 Dinero", "🏥 Salud"])
    
    def render_content(col_name):
        texto = fila[col_name]
        if pd.notna(texto) and str(texto).strip() != "":
            st.info(texto)
        else: st.write("_Sin detalles._")

    with tabs[0]: render_content('Amor' if posicion == "Derecha" else 'Amor Inv')
    with tabs[1]: render_content('Trabajo' if posicion == "Derecha" else 'Trabajo Inv')
    with tabs[2]: render_content('Dinero' if posicion == "Derecha" else 'Dinero Inv')
    with tabs[3]: render_content('Salud' if posicion == "Derecha" else 'Salud Inv')

    st.divider()

    # --- 3. SIGNIFICADO Y REPRESENTACIÓN ---
    color_vibe = "#2E7D32" if posicion == "Derecha" else "#C62828"
    palabra_clave = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']

    with st.container(border=True):
        st.markdown(f"""
            <div class="header-container">
                <h1 style="color:{color_vibe}; margin:0; font-size:1.8rem;">{carta_sel}</h1>
                <span class="num-badge">#{fila['N°']}</span>
            </div>
            <p style="color:#7B1FA2; font-weight:bold; margin-top:5px;">✨ {palabra_clave}</p>
        """, unsafe_allow_html=True)
        
        st.write(fila['Significado'])
        
        st.markdown("---")
        st.markdown("**💡 Lo que representa:**")
        st.write(fila['Que representa'])

except Exception as e:
    st.error(f"Error: {e}")
