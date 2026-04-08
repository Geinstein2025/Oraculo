import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# 2. Estilo CSS (Solo para lo esencial)
st.markdown("""
    <style>
    .stApp { background-color: #F0F2F6; }
    
    /* Título de la Carta con su Número */
    .header-container {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 5px;
    }
    .num-badge {
        background-color: #7B1FA2;
        color: white;
        padding: 2px 10px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1rem;
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
    c_arc, c_ene = st.columns([2, 1])
    with c_arc:
        carta_sel = st.selectbox("Elige tu Arcano:", df['Arcano'].unique())
    with c_ene:
        posicion = st.radio("Orientación:", ["Derecha", "Invertida"], horizontal=True)
    
    fila = df[df['Arcano'] == carta_sel].iloc[0]

    # --- 2. MENSAJES ESPECÍFICOS (ARRIBA) ---
    st.markdown("### 🔍 Mensajes Específicos")
    tabs = st.tabs(["❤️ Amor", "💼 Trabajo", "💰 Dinero", "🏥 Salud"])
    
    def render_content(col_name):
        texto = fila[col_name]
        if pd.notna(texto) and str(texto).strip() != "":
            st.info(texto)
        else:
            st.write("_Sin detalles específicos para esta posición._")

    with tabs[0]: render_content('Amor' if posicion == "Derecha" else 'Amor Inv')
    with tabs[1]: render_content('Trabajo' if posicion == "Derecha" else 'Trabajo Inv')
    with tabs[2]: render_content('Dinero' if posicion == "Derecha" else 'Dinero Inv')
    with tabs[3]: render_content('Salud' if posicion == "Derecha" else 'Salud Inv')

    st.divider()

    # --- 3. SIGNIFICADO Y REPRESENTACIÓN (DISEÑO SEGURO) ---
    color_vibe = "#2E7D32" if posicion == "Derecha" else "#C62828"
    palabra_clave = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']

    # Usamos un st.container con borde para la tarjeta blanca
    with st.container(border=True):
        # Nombre y Número
        st.markdown(f"""
            <div class="header-container">
                <h1 style="color:{color_vibe}; margin:0;">{carta_sel}</h1>
                <span class="num-badge">#{fila['N°']}</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Palabra Clave y Significado
        st.markdown(f"**✨ {palabra_clave}**")
        st.write(fila['Significado'])
        
        st.divider()
        
        # SECCIÓN "REPRESENTA" (Con su propio espacio total)
        st.markdown("### 💡 Lo que representa")
        st.write(fila['Que representa'])

    # --- 4. DATOS RÁPIDOS (ABAJO) ---
    st.write("")
    m1, m2 = st.columns(2)
    m1.success(f"**RESPUESTA:** {fila['SI/NO']}")
    m2.warning(f"**TIEMPO:** {fila['Tiempo']}")

except Exception as e:
    st.error(f"Error: {e}")
