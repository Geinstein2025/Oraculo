import streamlit as st
import pandas as pd

# 1. Configuración base
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# 2. Estilo mínimo para evitar huecos (Fondo claro y letras legibles)
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FB; }
    .main .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    h1 { color: #4A148C; text-align: center; font-size: 1.8rem; margin-bottom: 1rem; }
    
    /* Caja de resultado principal */
    .resultado-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        border-left: 10px solid #7B1FA2;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Conexión a datos
sheet_id = "1ZJNYTlIoEm8pmjw2lbjWFBENMitQy7NmG_oT5DhKkHA"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

@st.cache_data(ttl=60)
def cargar_datos():
    data = pd.read_csv(sheet_url)
    # Limpiamos nombres de columnas por si acaso
    data.columns = [str(c).strip() for c in data.columns]
    return data

st.markdown("<h1>🔮 MI ORÁCULO</h1>", unsafe_allow_html=True)

try:
    df = cargar_datos()
    
    # Seleccionables simples
    carta_sel = st.selectbox("Selecciona tu Arcano:", df['Arcano'].unique())
    posicion = st.radio("Orientación:", ["Derecha", "Invertida"], horizontal=True)
    
    # Filtrar la fila
    fila = df[df['Arcano'] == carta_sel].iloc[0]
    st.divider()

   # --- PARTE SUPERIOR: SIGNIFICADO ---
    palabra_clave = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']
    color_vibe = "#2E7D32" if posicion == "Derecha" else "#C62828"
    
    # Aquí es donde quitamos el paréntesis con la posición
    st.markdown(f"""
    <div class="resultado-card">
        <h2 style='color:{color_vibe}; margin:0; font-size: 2rem;'>{carta_sel}</h2>
        <p style='color:#7B1FA2; font-weight:bold; font-size:1.2rem; margin:10px 0;'>✨ {palabra_clave}</p>
        <p style='font-size:1.1rem; line-height:1.5;'>{fila['Significado']}</p>
    </div>
    """, unsafe_allow_html=True)

    # --- PARTE MEDIA: DATOS RÁPIDOS ---
    st.write("")
    c1, c2, c3 = st.columns(3)
    c1.metric("Respuesta", fila['SI/NO'])
    c2.metric("Tiempo", fila['Tiempo'])
    c3.metric("Número", fila['N°'])

    # --- PARTE INFERIOR: PESTAÑAS ---
    st.markdown("### 🔍 Detalles Específicos")
    t1, t2, t3, t4 = st.tabs(["❤️ Amor", "💼 Trabajo", "💰 Dinero", "🏥 Salud"])
    
    # Función para limpiar y mostrar el contenido sin cajas vacías
    def render_tab(col):
        contenido = fila[col]
        if pd.notna(contenido) and str(contenido).strip() != "":
            st.info(contenido)
        else:
            st.write("_No hay detalles adicionales para esta posición._")

    with t1: render_tab('Amor' if posicion == "Derecha" else 'Amor Inv')
    with t2: render_tab('Trabajo' if posicion == "Derecha" else 'Trabajo Inv')
    with t3: render_tab('Dinero' if posicion == "Derecha" else 'Dinero Inv')
    with t4: render_tab('Salud' if posicion == "Derecha" else 'Salud Inv')

except Exception as e:
    st.error(f"Hubo un problema al cargar la sabiduría: {e}")
