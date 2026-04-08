import streamlit as st
import pandas as pd

st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# CSS DE ALTO CONTRASTE (Negro sobre Azul Fuerte)
st.markdown("""
    <style>
    /* 1. Fondo de la App Blanco */
    .stApp { background-color: #FFFFFF !important; }

    /* 2. SELECTOR: Negro total con texto Blanco */
    div[data-baseweb="select"] > div { background-color: #000000 !important; }
    div[data-baseweb="select"] span { color: #FFFFFF !important; font-weight: bold !important; }
    div[data-baseweb="select"] svg { fill: #FFFFFF !important; }

    /* 3. TEXTO DE LECTURA: Negro Puro con "fuerza bruta" */
    /* Aplicamos a párrafos, etiquetas y todo el cuerpo de texto */
    p, span, label, b, .stRadio label, div[data-testid="stMarkdownContainer"] p {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: 700 !important; /* Más grueso para que se vea mejor */
    }

    /* 4. CAJAS DE TEXTO: Azul más intenso para que el negro resalte */
    .caja-segura {
        background-color: #BBDEFB !important; /* Un azul un poco más oscuro que antes */
        border: 2px solid #000000 !important; /* Borde negro para definir la caja */
        color: #000000 !important;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 3px 3px 0px #4A148C; /* Sombra morada para el toque místico */
    }

    /* 5. BADGES: Inversión total (Fondo Negro, Letra Blanca) */
    .mini-badge {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        padding: 5px 12px;
        border-radius: 5px;
        font-size: 0.85rem;
        font-weight: bold;
        display: inline-block;
        margin-right: 5px;
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
    st.markdown("<h1 style='text-align:center; color:#000000;'>🔮 MI ORÁCULO</h1>", unsafe_allow_html=True)

    # --- CONTROLES ---
    st.markdown("### Elegir Arcano:")
    carta_sel = st.selectbox("", df['Arcano'].unique(), label_visibility="collapsed")
    
    fila = df[df['Arcano'] == carta_sel].iloc[0]

    # Orientación y Datos Rápidos
    col1, col2 = st.columns([1, 1])
    with col1:
        posicion = st.radio("Orientación:", ["Derecha", "Invertida"], horizontal=True)
    with col2:
        st.markdown(f"""
            <div style="margin-top:10px;">
                <span class="mini-badge">R: {fila['SI/NO']}</span>
                <span class="mini-badge">T: {fila['Tiempo']}</span>
                <span class="mini-badge">#{fila['N°']}</span>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- CONTENIDO ---
    color_titulo = "#1B5E20" if posicion == "Derecha" else "#B71C1C" # Verde/Rojo muy oscuros
    palabra_k = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']

    st.markdown(f"<h2 style='color:{color_titulo};'>{carta_sel}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{color_titulo};'>✨ {palabra_k}</h3>", unsafe_allow_html=True)
    
    # Significado con Caja Segura
    st.markdown(f"<div class='caja-segura'>{fila['Significado']}</div>", unsafe_allow_html=True)

    # Tabs (Detalles)
    st.markdown("### 🔍 Detalles Específicos")
    t1, t2, t3, t4 = st.tabs(["❤️ Amor", "💼 Trabajo", "💰 Dinero", "🏥 Salud"])
    
    def render_caja(col):
        val = fila[col]
        st.markdown(f"<div class='caja-segura'>{val if pd.notna(val) else 'Sin detalles'}</div>", unsafe_allow_html=True)

    with t1: render_caja('Amor' if posicion == "Derecha" else 'Amor Inv')
    with t2: render_caja('Trabajo' if posicion == "Derecha" else 'Trabajo Inv')
    with t3: render_caja('Dinero' if posicion == "Derecha" else 'Dinero Inv')
    with t4: render_caja('Salud' if posicion == "Derecha" else 'Salud Inv')

    st.markdown("### 💡 LO QUE REPRESENTA")
    st.markdown(f"<div class='caja-segura'>{fila['Que representa']}</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error: {e}")
