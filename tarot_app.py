import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# 2. Estilo CSS Centralizado (Aquí definimos los colores una sola vez)
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FB; }
    
    /* Títulos de secciones */
    .section-title {
        color: #4A148C;
        font-size: 1.5rem;
        font-weight: bold;
        border-bottom: 2px solid #E1BEE7;
        margin-bottom: 15px;
        margin-top: 10px;
    }

    /* Badge del número */
    .num-badge {
        background-color: #7B1FA2; color: white;
        padding: 2px 10px; border-radius: 8px;
        font-weight: bold; font-size: 1rem; vertical-align: middle;
    }

    /* Etiquetas de Datos Rápidos (Debajo de orientación) */
    .mini-dato {
        background-color: #EDE7F6;
        color: #4A148C;
        border: 1px solid #D1C4E9;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.85rem;
        display: inline-block;
        font-weight: bold;
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
    st.markdown("<h1 style='text-align:center; color:#4A148C;'>🔮 MI ORÁCULO</h1>", unsafe_allow_html=True)

    # --- 1. ZONA SUPERIOR ---
    col_arc, col_ene = st.columns([2, 1])
    with col_arc:
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
            st.info(texto)
        else: st.write("_Sin detalles específicos._")

    with tabs[0]: render_content('Amor' if posicion == "Derecha" else 'Amor Inv')
    with tabs[1]: render_content('Trabajo' if posicion == "Derecha" else 'Trabajo Inv')
    with tabs[2]: render_content('Dinero' if posicion == "Derecha" else 'Dinero Inv')
    with tabs[3]: render_content('Salud' if posicion == "Derecha" else 'Salud Inv')

    # --- 3. CUERPO DE LA CARTA (DISEÑO BLINDADO) ---
    st.markdown('<div class="section-title">📖 Significado Arcano</div>', unsafe_allow_html=True)
    
    color_vibe = "#2E7D32" if posicion == "Derecha" else "#C62828"
    palabra_clave = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']

    # Contenedor principal con borde nativo (evita el error de código crudo)
    with st.container(border=True):
        # Encabezado: Nombre y Número
        st.markdown(f"""
            <div style="margin-bottom: 10px;">
                <span style="color:{color_vibe}; font-size: 2.2rem; font-weight: bold;">{carta_sel}</span>
                <span class="num-badge">#{fila['N°']}</span>
            </div>
            <p style="color:#7B1FA2; font-weight:bold; font-size:1.1rem;">✨ {palabra_clave}</p>
        """, unsafe_allow_html=True)
        
        # Texto de Significado (Nativo)
        st.write(fila['Significado'])
        
        # Espacio de Contraste para "Lo que representa"
        st.write("")
        st.markdown("**💡 LO QUE REPRESENTA:**")
        # Usamos st.help o st.success para dar un fondo de color sin usar HTML complejo
        st.success(fila['Que representa'])

except Exception as e:
    st.error(f"Error: {e}")
