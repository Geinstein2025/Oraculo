import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# 2. Estilo CSS de Alto Contraste
st.markdown("""
    <style>
    /* Fondo general de la app */
    .stApp { background-color: #F8F9FB; }
    
    /* Títulos y Secciones */
    h3 { color: #4A148C !important; font-weight: bold; border-bottom: 2px solid #E1BEE7; padding-bottom: 5px; }
    
    /* Contenedor de la Carta (Blanco puro sobre fondo gris) */
    .main-card {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
        border-left: 8px solid #7B1FA2;
        margin-top: 10px;
    }

    /* Badge del número */
    .num-badge {
        background-color: #7B1FA2; color: white;
        padding: 3px 10px; border-radius: 8px;
        font-weight: bold; font-size: 1rem; margin-left: 10px;
    }

    /* Etiquetas de Datos Rápidos (Debajo de orientación) */
    .mini-dato {
        background-color: #EDE7F6; /* Morado muy claro */
        color: #4A148C;
        border: 1px solid #D1C4E9;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        display: inline-block;
        font-weight: bold;
        margin-top: 5px;
    }

    /* Caja de "Lo que representa" (Fondo de contraste) */
    .highlight-box {
        background-color: #F3F0F9; /* Contraste suave para lectura larga */
        padding: 15px;
        border-radius: 12px;
        border-left: 4px solid #7B1FA2;
        color: #2D3436;
        line-height: 1.6;
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
    st.markdown("<h1 style='text-align:center; color:#4A148C; margin-bottom:20px;'>🔮 MI ORÁCULO</h1>", unsafe_allow_html=True)

    # --- 1. ZONA SUPERIOR (Compacta) ---
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
    st.write("")
    st.markdown("### 🔍 Mensajes Específicos")
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

    # --- 3. SIGNIFICADO Y REPRESENTACIÓN (DISEÑO DE CONTRASTE) ---
    color_vibe = "#2E7D32" if posicion == "Derecha" else "#C62828"
    palabra_clave = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']

    st.markdown(f"""
        <div class="main-card">
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <h1 style="color:{color_vibe}; margin:0; font-size:2.2rem;">{carta_sel}</h1>
                <span class="num-badge">#{fila['N°']}</span>
            </div>
            <p style="color:#7B1FA2; font-weight:bold; font-size:1.1rem; margin-bottom:15px;">✨ {palabra_clave}</p>
            
            <p style="font-size:1.1rem; color:#333; line-height:1.7;">{fila['Significado']}</p>
            
            <div style="margin-top:25px;">
                <p style="color:#4A148C; font-weight:bold; margin-bottom:8px; font-size:0.9rem;">💡 LO QUE REPRESENTA:</p>
                <div class="highlight-box">
                    {fila['Que representa']}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error: {e}")
