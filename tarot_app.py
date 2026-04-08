import streamlit as st
import pandas as pd

st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# CSS DE ALTO CONTRASTE INVERSO
st.markdown("""
    <style>
    /* Fondo general siempre blanco para nosotros */
    .stApp { background-color: #FFFFFF !important; }

    /* CAJAS OSCURAS: Aquí la letra será blanca por defecto */
    .caja-oscura {
        background-color: #1A1A1A !important; /* Negro Mate */
        color: #FFFFFF !important;           /* Letra Blanca */
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 2px solid #4A148C;           /* Borde Morado */
        font-size: 1.1rem;
        line-height: 1.6;
    }

    /* Forzamos que CUALQUIER texto dentro de la caja sea blanco */
    .caja-oscura p, .caja-oscura span, .caja-oscura div {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    /* Estilo para los títulos de las secciones */
    .titulo-seccion {
        color: #4A148C !important;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 10px;
        display: block;
    }

    /* Botones de Radio y Etiquetas (Fuera de las cajas) */
    /* Si el celular los pone blancos, les ponemos un fondo oscuro propio */
    div[data-testid="stMarkdownContainer"] p {
        color: #000000 !important;
    }
    
    .mini-badge {
        background-color: #4A148C !important;
        color: #FFFFFF !important;
        padding: 5px 15px;
        border-radius: 10px;
        font-weight: bold;
        margin-right: 5px;
        display: inline-block;
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
    st.markdown("<h1 style='text-align:center; color:#1A1A1A;'>🔮 MI ORÁCULO</h1>", unsafe_allow_html=True)

    carta_sel = st.selectbox("Elegir Arcano:", df['Arcano'].unique())
    fila = df[df['Arcano'] == carta_sel].iloc[0]

    col1, col2 = st.columns([1, 1])
    with col1:
        posicion = st.radio("Orientación:", ["Derecha", "Invertida"], horizontal=True)
    with col2:
        st.markdown(f"""
            <div style="margin-top:25px;">
                <span class="mini-badge">R: {fila['SI/NO']}</span>
                <span class="mini-badge">T: {fila['Tiempo']}</span>
                <span class="mini-badge">#{fila['N°']}</span>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- CONTENIDO ---
    color_tit = "#2E7D32" if posicion == "Derecha" else "#C62828"
    palabra = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']

    st.markdown(f"<h2 style='color:{color_tit};'>{carta_sel}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{color_tit};'>✨ {palabra}</h3>", unsafe_allow_html=True)
    
    # SIGNIFICADO
    st.markdown("<span class='titulo-seccion'>📖 Significado:</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='caja-oscura'>{fila['Significado']}</div>", unsafe_allow_html=True)

    # TABS
    st.markdown("<span class='titulo-seccion'>🔍 Detalles:</span>", unsafe_allow_html=True)
    t1, t2, t3, t4 = st.tabs(["❤️ Amor", "💼 Trabajo", "💰 Dinero", "🏥 Salud"])
    
    def render_tab(col):
        val = fila[col]
        st.markdown(f"<div class='caja-oscura'>{val if pd.notna(val) else 'Sin detalles'}</div>", unsafe_allow_html=True)

    with t1: render_tab('Amor' if posicion == "Derecha" else 'Amor Inv')
    with t2: render_tab('Trabajo' if posicion == "Derecha" else 'Trabajo Inv')
    with t3: render_tab('Dinero' if posicion == "Derecha" else 'Dinero Inv')
    with t4: render_tab('Salud' if posicion == "Derecha" else 'Salud Inv')

    # REPRESENTA
    st.markdown("<span class='titulo-seccion'>💡 Lo que representa:</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='caja-oscura'>{fila['Que representa']}</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error: {e}")
