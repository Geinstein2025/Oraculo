import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# 2. Estilo CSS (Corregido para evitar que el código se vea como texto)
st.markdown("""
    <style>
    .stApp { background-color: #F0F2F6; }
    
    /* Tarjeta Principal */
    .carta-container {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 20px;
        border-top: 8px solid #7B1FA2;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.05);
    }

    /* Nombre y Número alineados */
    .nombre-wrapper {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 10px;
    }
    .badge-numero {
        background-color: #F3E5F5;
        color: #7B1FA2;
        padding: 5px 12px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 1.2rem;
    }

    /* Ficha técnica horizontal (La barrita morada) */
    .barra-datos {
        display: flex;
        justify-content: space-around;
        background: #4A148C;
        color: white;
        padding: 15px;
        border-radius: 15px;
        margin-top: 20px;
        flex-wrap: wrap;
    }
    .dato-box { text-align: center; min-width: 80px; }
    .dato-titulo { font-size: 0.7rem; text-transform: uppercase; opacity: 0.8; margin-bottom: 5px; }
    .dato-info { font-size: 1.1rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Conexión a datos
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

    # Selección superior
    c_sel1, c_sel2 = st.columns([2, 1])
    with c_sel1:
        carta_sel = st.selectbox("Elige tu Arcano:", df['Arcano'].unique())
    with c_sel2:
        posicion = st.radio("Vibración:", ["Derecha", "Invertida"], horizontal=True)
    
    fila = df[df['Arcano'] == carta_sel].iloc[0]

    # --- DISEÑO DE LA CARTA ---
    color_vibe = "#2E7D32" if posicion == "Derecha" else "#C62828"
    palabra_clave = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']

    # Contenedor de la carta
    st.markdown(f"""
    <div class="carta-container">
        <div class="nombre-wrapper">
            <h1 style="color:{color_vibe}; margin:0; font-size:2.5rem;">{carta_sel}</h1>
            <span class="badge-numero">#{fila['N°']}</span>
        </div>
        <h3 style="color:#7B1FA2; margin: 10px 0;">✨ {palabra_clave}</h3>
        <p style="font-size:1.1rem; line-height:1.6;">{fila['Significado']}</p>
        
        <div class="barra-datos">
            <div class="dato-box">
                <div class="dato-titulo">Respuesta</div>
                <div class="dato-info">{fila['SI/NO']}</div>
            </div>
            <div class="dato-box">
                <div class="dato-titulo">Tiempo</div>
                <div class="dato-info">{fila['Tiempo']}</div>
            </div>
            <div class="dato-box">
                <div class="dato-titulo">Representa</div>
                <div class="dato-info" style="font-size:0.9rem;">{fila['Que representa']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- PESTAÑAS ---
    st.write("")
    st.markdown("### 🔍 Mensajes Específicos")
    t1, t2, t3, t4 = st.tabs(["❤️ Amor", "💼 Trabajo", "💰 Dinero", "🏥 Salud"])
    
    def render_tab(col):
        contenido = fila[col]
        if pd.notna(contenido) and str(contenido).strip() != "":
            st.info(contenido)
        else:
            st.write("_Sin detalles específicos._")

    with t1: render_tab('Amor' if posicion == "Derecha" else 'Amor Inv')
    with t2: render_tab('Trabajo' if posicion == "Derecha" else 'Trabajo Inv')
    with t3: render_tab('Dinero' if posicion == "Derecha" else 'Dinero Inv')
    with t4: render_tab('Salud' if posicion == "Derecha" else 'Salud Inv')

except Exception as e:
    st.error(f"Error: {e}")
