import streamlit as st
import pandas as pd

st.set_page_config(page_title="Oráculo", page_icon="🔮", layout="wide")

# CSS AGRESIVO: Si el celular lo pone blanco, nosotros lo obligamos a ser Morado/Negro
st.markdown("""
    <style>
    /* 1. Fondo de la App siempre Blanco */
    .stApp { background-color: #FFFFFF !important; }

    /* 2. SELECTOR: Fondo Negro, Texto Blanco (Este suele funcionar bien) */
    div[data-baseweb="select"] > div { background-color: #1A1A1A !important; }
    div[data-baseweb="select"] span { color: #FFFFFF !important; }
    div[data-baseweb="select"] svg { fill: #FFFFFF !important; }

    /* 3. EL TRUCO PARA EL CELULAR: Forzar color morado en CUALQUIER texto */
    /* Cubrimos párrafos, etiquetas, radios y contenedores de markdown */
    p, span, label, b, .stRadio > label, div[data-testid="stMarkdownContainer"] p {
        color: #4A148C !important;
        -webkit-text-fill-color: #4A148C !important; /* Para navegadores móviles */
        font-weight: 600 !important;
    }

    /* 4. BOTONES DE RADIO (Derecha/Invertida) */
    /* Forzamos que el texto al lado del círculo sea visible */
    div[data-testid="stWidgetLabel"] p { font-size: 1.1rem !important; }
    
    /* 5. CAJAS AZULES: Con borde más fuerte para que se vean sí o sí */
    .caja-mistica {
        background-color: #E3F2FD !important;
        border: 2px solid #4A148C !important; /* Borde morado para dar visibilidad */
        color: #4A148C !important;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
        font-size: 1rem;
    }

    /* 6. BADGES (R:, T:, #) */
    .badge-container { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 10px; }
    .mini-badge {
        background-color: #4A148C !important; /* Fondo Morado */
        color: #FFFFFF !important;           /* Letra Blanca */
        padding: 5px 12px;
        border-radius: 15px;
        font-size: 0.85rem;
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

    # --- SECCIÓN SUPERIOR ---
    st.markdown("<span><b>Elegir Arcano:</b></span>", unsafe_allow_html=True)
    carta_sel = st.selectbox("", df['Arcano'].unique(), label_visibility="collapsed")
    
    fila = df[df['Arcano'] == carta_sel].iloc[0]

    col_r, col_i = st.columns([1, 1])
    with col_r:
        posicion = st.radio("Orientación:", ["Derecha", "Invertida"], horizontal=True)
    
    with col_i:
        st.markdown(f"""
            <div class="badge-container">
                <div class="mini-badge">R: {fila['SI/NO']}</div>
                <div class="mini-badge">T: {fila['Tiempo']}</div>
                <div class="mini-badge">#{fila['N°']}</div>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- CONTENIDO ---
    color_v = "#2E7D32" if posicion == "Derecha" else "#C62828"
    palabra_k = fila['Palabra clave'] if posicion == "Derecha" else fila['Palabra invertida']

    st.markdown(f"<h2 style='color:{color_v};'>{carta_sel}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color:{color_v};'>✨ {palabra_k}</h4>", unsafe_allow_html=True)
    
    # Significado
    st.markdown(f"<div class='caja-mistica'>{fila['Significado']}</div>", unsafe_allow_html=True)

    # Tabs
    st.markdown("### 🔍 Detalles")
    t1, t2, t3, t4 = st.tabs(["❤️ Amor", "💼 Trabajo", "💰 Dinero", "🏥 Salud"])
    
    def render(col):
        val = fila[col]
        st.markdown(f"<div class='caja-mistica'>{val if pd.notna(val) else 'Sin detalles'}</div>", unsafe_allow_html=True)

    with t1: render('Amor' if posicion == "Derecha" else 'Amor Inv')
    with t2: render('Trabajo' if posicion == "Derecha" else 'Trabajo Inv')
    with t3: render('Dinero' if posicion == "Derecha" else 'Dinero Inv')
    with t4: render('Salud' if posicion == "Derecha" else 'Salud Inv')

    st.markdown("### 💡 LO QUE REPRESENTA")
    st.markdown(f"<div class='caja-mistica'>{fila['Que representa']}</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error: {e}")
