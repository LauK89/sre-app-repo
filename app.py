import streamlit as st
import time

# 1. OBLIGATORIO: Debe ser la primerísima llamada de Streamlit
st.set_page_config(
    page_title="SRE Incident Response - Databricks App", 
    page_icon="🚨", 
    layout="centered"
)

# 2. Inicialización segura del SDK de Databricks
try:
    from databricks.sdk import WorkspaceClient
    w = WorkspaceClient()
except Exception as e:
    w = None

# Estilos CSS oscuros y agresivos tipo centro de mando / SRE
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .status-card-red {
        background-color: #3b1111;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #ff4b4b;
        text-align: center;
        margin-bottom: 20px;
    }
    .status-card-green {
        background-color: #0e3b1f;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #00ff66;
        text-align: center;
        margin-bottom: 20px;
    }
    .big-code { 
        font-size: 48px !important; 
        font-weight: bold; 
        color: #00FF66; 
        text-align: center;
        letter-spacing: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Control de estado de la sesión
if 'patched' not in st.session_state:
    st.session_state.patched = False

# --- ESTADO 1: INCIDENTE ACTIVO (PANTALLA ROJA) ---
if not st.session_state.patched:
    st.markdown("""
        <div class="status-card-red">
            <h1>🚨 CRITICAL ALARM: OVERHEAT DETECTED</h1>
            <p>Datacenter: <b>MADRID-SOUTH</b> | Affected Node: <b>NODE-MAD-03</b></p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    col1.metric("Temperatura CPU", "98.7 ºC", delta="🔥 CRITICAL (+56.2 ºC)", delta_color="inverse")
    col2.metric("Estado del Parche", "BLOQUEADO", delta="🔒 Requiere Hotfix Port")

    st.markdown("---")
    st.subheader("🔑 Introduzca el puerto de emergencia (Hotfix Port):")
    st.caption("Obtenido tras la investigación en Genie y la tabla de gobernanza Unity Catalog.")
    
    user_input = st.text_input("Puerto de Remediación (Hotfix Port):", placeholder="Ej: 8080")
    
    if st.button("🚀 DESPLEGAR PARCHE DE REMEDIACIÓN", use_container_width=True):
        if user_input.strip() == "7421":
            with st.spinner("Conectando con Databricks Workflows y aplicando parche SQL en 'sre_escape_db'..."):
                time.sleep(2.0)
            
            st.session_state.patched = True
            st.rerun()
        else:
            st.error("❌ PUERTO INCORRECTO. Consulta en Genie la tabla 'dim_security_access' para obtener el puerto asignado a NODE-MAD-03.")

# --- ESTADO 2: INCIDENTE RESUELTO / VICTORIA (PANTALLA VERDE) ---
else:
    st.balloons()
    st.markdown("""
        <div class="status-card-green">
            <h1>✅ SYSTEM RECOVERED & STABILIZED</h1>
            <p>Hotfix 7421 aplicado correctamente en <b>NODE-MAD-03</b></p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    col1.metric("Temperatura CPU", "42.0 ºC", delta="-56.7 ºC Cooled")
    col2.metric("Estado del Parche", "OPERACIONAL", delta="🟢 ONLINE")

    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>🔓 COMBINACIÓN DE APERTURA DEL COFRE:</h3>", unsafe_allow_html=True)
    st.markdown("<p class='big-code'>7 4 2 1</p>", unsafe_allow_html=True)
    st.info("💡 Pon este código en el candado físico que hay en la mesa del stand para sacar tu premio.")
    
    if st.button("🔄 Reiniciar Sistema (Para el siguiente jugador)", use_container_width=True):
        st.session_state.patched = False
        st.rerun()