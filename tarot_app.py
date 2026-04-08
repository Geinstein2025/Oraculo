import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# 2. ESTILO CSS REFINADO (Elimina espacios fantasma)
st.markdown("""
    <style>
    .stApp { background-color: #F0F2F6; color: #1A1A1A; }
    h1 { color: #4A148C; text-align: center; font-weight: 800; margin-bottom: 0px; }
    
    /* Ajuste de contenedores para evitar espacios en blanco */
    .block-container { padding-top: 2rem; }
    
    .metric-card {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 15px;
        border-left: 8px solid #7B1FA2;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    
    .significado-box {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
        margin-top: 5px;
    }

    /* Quitar bordes innecesarios en radio buttons */
    div.row-widget.stRadio > div{ background-color: transparent !important; box-shadow: none !important; }
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

st.markdown("<h1>🔮 MI ORÁCULO PERSONAL</h1>", unsafe_allow_html=True)

try:
    df = cargar_datos()
    
    # Selectores compactos
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        carta_sel = st.selectbox("Carta:", df['Arcano'].unique())
    with col_sel2:
        posicion = st.radio("Energía:", ["Derecha", "Invertida"], horizontal=True)
    
    fila = df[df['Arcano'] == carta_sel].iloc[0]
    st.divider()

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style='margin:0; color:#7B1FA2;'>📋 Datos Clave</h4>
            <p style='margin-bottom:0;'><b>N°:</b> {fila['N°']}<br>
            <b>SI/NO:</b> {fila['SI/NO']}<br>
            <b>Tiempo:</b> {fila['Tiempo']}</p>
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"💡 {fila['Que representa']}")

    with col2:
        # Solo dibujamos la caja si hay significado
        texto_sig = fila['Significado']
        if pd.notna(texto_sig):
            color_titulo = "#2E7D32" if posicion == "Derecha" else "#C62828"
            label_pos = f"{carta_sel}" if posicion == "Derecha" else f"{carta_sel} (Invertida)"
            
            st.markdown(f"""
            <div class='significado-box'>
                <h2 style='color:{color_titulo}; margin:0;'>✨ {label_pos}</h2>
                <p style='color:#666; font-weight:bold; margin-bottom:10px;'>
                    {fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']}
                </p>
                <p style='margin:0;'>{texto_sig}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color:#4A148C; margin-top:20px;'>🔍 Mensajes Específicos</h3>", unsafe_allow_html=True)
    
    t1, t2, t3, t4 = st.tabs(["❤️ AMOR", "💼 TRABAJO", "💰 DINERO", "🏥 SALUD"])
    
    # Función para mostrar contenido solo si existe
    def mostrar_tab(columna):
        contenido = fila[columna]
        if pd.notna(contenido) and str(contenido).strip() != "":
            st.markdown(f"<div class='significado-box'>{contenido}</div>", unsafe_allow_html=True)
        else:
            st.info("No hay información específica para esta posición.")

    with t1: mostrar_tab('Amor' if posicion == "Derecha" else 'Amor Inv')
    with t2: mostrar_tab('Trabajo' if posicion == "Derecha" else 'Trabajo Inv')
    with t3: mostrar_tab('Dinero' if posicion == "Derecha" else 'Dinero Inv')
    with t4: mostrar_tab('Salud' if posicion == "Derecha" else 'Salud Inv')

except Exception as e:
    st.error(f"Error: {e}")
