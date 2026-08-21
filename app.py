# app.py  —  Plan de Estudios UNA · Streamlit
import streamlit as st
from collections import deque
from datos  import G, NOMBRES
from logica import insertar_bst, buscar_bst, inorden_bst, plan

# ─── Configuración de página ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Plan de Estudios UNA",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CSS personalizado ────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Fuente y fondo general */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Ocultar elementos por defecto de Streamlit */
#MainMenu, footer, header { visibility: hidden; }

/* Header propio */
.una-header {
    background: linear-gradient(135deg, #0f2044 0%, #1d5bbf 100%);
    border-radius: 12px;
    padding: 24px 32px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 20px;
}
.una-badge {
    background: #3b82f6;
    color: white;
    font-weight: 700;
    font-size: 1.1rem;
    padding: 8px 16px;
    border-radius: 8px;
    letter-spacing: 1px;
}
.una-title { color: white; font-size: 1.4rem; font-weight: 700; margin: 0; }
.una-sub   { color: #94a3b8; font-size: 0.85rem; margin: 4px 0 0; }

/* Tarjetas de métricas */
.metric-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 18px 20px;
    text-align: center;
}
.metric-num   { font-size: 2rem; font-weight: 700; color: #1d5bbf; }
.metric-label { font-size: 0.8rem; color: #64748b; margin-top: 4px; }

/* Bloques de resultado */
.result-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #1d5bbf;
    border-radius: 8px;
    padding: 16px 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88rem;
    line-height: 1.8;
    white-space: pre-wrap;
    margin-top: 12px;
}
.result-ok     { border-left-color: #16a34a; }
.result-warn   { border-left-color: #b45309; }
.result-error  { border-left-color: #b91c1c; }

/* Tabla de resultados */
.curso-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
.curso-table th {
    background: #1d5bbf;
    color: white;
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
}
.curso-table td { padding: 9px 14px; border-bottom: 1px solid #f1f5f9; }
.curso-table tr:hover td { background: #f8fafc; }
.badge-code {
    background: #eff6ff;
    color: #1d5bbf;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 4px;
}
.badge-ok    { background:#dcfce7; color:#16a34a; padding:2px 8px; border-radius:4px; font-size:0.8rem; font-weight:600; }
.badge-warn  { background:#fef3c7; color:#b45309; padding:2px 8px; border-radius:4px; font-size:0.8rem; font-weight:600; }
.badge-error { background:#fee2e2; color:#b91c1c; padding:2px 8px; border-radius:4px; font-size:0.8rem; font-weight:600; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: #f1f5f9; border-radius: 10px; padding: 4px; }
.stTabs [data-baseweb="tab"] {
    border-radius: 7px;
    color: #475569;
    font-weight: 500;
    padding: 8px 18px;
}
.stTabs [aria-selected="true"] {
    background: #1d5bbf !important;
    color: white !important;
}

/* Botones */
.stButton > button {
    background: #1d5bbf;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 10px 22px;
    transition: background 0.2s;
}
.stButton > button:hover { background: #2d6fd4; }

/* Input */
.stTextInput > div > div > input {
    border-radius: 8px;
    border: 1px solid #cbd5e1;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.95rem;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)


# ─── BST en caché ────────────────────────────────────────────────────────────
@st.cache_resource
def construir_bst():
    raiz = None
    materias_unicas = list(G.keys())
    for valores in G.values():
        for val in valores:
            if val not in materias_unicas:
                materias_unicas.append(val)
    # CORRECCIÓN: sin sorted() para árbol ramificado
    for m in materias_unicas:
        raiz = insertar_bst(raiz, m)
    return raiz


raiz_bst = construir_bst()


# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="una-header">
  <div class="una-badge">UNA</div>
  <div>
    <p class="una-title">Dashboard Académico — Plan de Estudios</p>
    <p class="una-sub">Estructuras de Datos · Análisis de Grafo de Prerrequisitos</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Métricas rápidas ─────────────────────────────────────────────────────────
total_cursos   = len(NOMBRES)
total_nodos    = len(G)
total_enlaces  = sum(len(v) for v in G.values())
nodos_terminal = sum(1 for v in G.values() if not v)

c1, c2, c3, c4 = st.columns(4)
for col, num, label in [
    (c1, total_cursos,   "Materias registradas"),
    (c2, total_nodos,    "Nodos en el grafo"),
    (c3, total_enlaces,  "Relaciones (aristas)"),
    (c4, nodos_terminal, "Materias terminales"),
]:
    col.markdown(f"""
    <div class="metric-card">
      <div class="metric-num">{num}</div>
      <div class="metric-label">{label}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Tabs ────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📋  Orden de Desbloqueo (BFS)",
    "🔍  Índice de Cursos (BST)",
    "⚡  Analizador de Materia",
    "📊  Integridad y Cuellos de Botella",
])


# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — BFS
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("#### Simulación de avance por niveles (BFS)")
    st.caption("Recorre el grafo de prerrequisitos en amplitud desde las materias iniciales "
               "para obtener el orden óptimo de cursado.")

    if st.button("▶  Calcular Orden Matemático", key="bfs"):
        iniciales = ['EIF200', 'MAT030', 'LIX410']
        visitados = set(iniciales)
        cola      = deque(iniciales)
        orden     = []
        while cola:
            m = cola.popleft()
            orden.append(m)
            for sig in G.get(m, []):
                if sig not in visitados:
                    visitados.add(sig)
                    cola.append(sig)

        st.success(f"BFS completado — {len(orden)} materias ordenadas.")

        rows = ""
        for i, cod in enumerate(orden, 1):
            rows += f"""<tr>
              <td style="color:#64748b">{i}</td>
              <td><span class="badge-code">{cod}</span></td>
              <td>{NOMBRES.get(cod, cod)}</td>
            </tr>"""

        st.markdown(f"""
        <table class="curso-table">
          <thead><tr><th>#</th><th>Código</th><th>Nombre de la Materia</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — BST
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("#### Búsqueda en Árbol Binario (BST)")

    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown("**Buscar nodo por código**")
        cod_buscar = st.text_input("Código del Curso", placeholder="ej. EIF201", key="cod_bst",
                                   label_visibility="collapsed")
        if st.button("🔍  Buscar Nodo", key="bst_buscar"):
            cod = cod_buscar.strip().upper()
            if not cod:
                st.warning("Por favor ingresá un código de curso.")
            else:
                nodo, ruta = buscar_bst(raiz_bst, cod)
                if nodo:
                    st.markdown(f"""
                    <div class="result-box result-ok">
✔  Curso encontrado

   Código  : <b>{cod}</b>
   Nombre  : {NOMBRES.get(cod, 'Desconocido')}

Ruta de decisión en el BST:
   {" → ".join(ruta)}
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-box result-error">
✘  La materia [{cod}] NO existe en el índice BST.
                    </div>""", unsafe_allow_html=True)

    with col_b:
        st.markdown("**Índice completo ordenado**")
        if st.button("📋  Ver Recorrido Inorden", key="bst_inorden"):
            lista = []
            inorden_bst(raiz_bst, lista)
            st.markdown(f"""
            <div class="result-box">
<b>Inorden BST — {len(lista)} nodos</b>

{" → ".join(lista)}
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — Analizador de materia
# ════════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("#### Consulta dinámica — Pasado y Futuro de un curso")

    cod_req = st.text_input("Código de la Asignatura", placeholder="ej. EIF201", key="cod_req",
                            label_visibility="collapsed")

    if st.button("⚡  Escanear Impacto", key="req_scan"):
        curso = cod_req.strip().upper()
        if curso not in NOMBRES:
            st.error("Código de curso no registrado en la base de datos.")
        else:
            st.markdown(f"### `{curso}` — {NOMBRES[curso]}")

            col_p, col_f = st.columns(2)

            # ── Hacia atrás (prerrequisitos) ──────────────────────────────
            with col_p:
                st.markdown("**◄◄ Análisis Retrospectivo**")
                directos_atras = plan.get(curso, [])
                if not directos_atras:
                    st.markdown("""<div class="result-box result-ok">
→ Sin prerrequisitos. Es materia de primer ingreso.</div>""", unsafe_allow_html=True)
                else:
                    visitados_atras      = []
                    por_revisar_atras    = list(directos_atras)
                    while por_revisar_atras:
                        actual = por_revisar_atras.pop(0)
                        if actual not in visitados_atras:
                            visitados_atras.append(actual)
                            for pr in plan.get(actual, []):
                                if pr not in visitados_atras:
                                    por_revisar_atras.append(pr)
                    indirectos_atras = [x for x in visitados_atras if x not in directos_atras]
                    st.markdown(f"""<div class="result-box">
<b>Requisitos directos</b>
  {directos_atras}

<b>Requisitos indirectos</b>
  {indirectos_atras}

<b>Peso acumulado:</b> {len(visitados_atras)} materias necesarias antes.
</div>""", unsafe_allow_html=True)

            # ── Hacia adelante (bloqueos) ─────────────────────────────────
            with col_f:
                st.markdown("**►► Análisis Prospectivo**")
                directos_futuro = G.get(curso, [])
                if not directos_futuro and curso in G:
                    st.markdown("""<div class="result-box">
→ Nodo terminal. No desbloquea materias adicionales.</div>""", unsafe_allow_html=True)
                else:
                    visitados_futuro   = []
                    por_revisar_futuro = list(directos_futuro)
                    while por_revisar_futuro:
                        actual = por_revisar_futuro.pop(0)
                        if actual not in visitados_futuro:
                            visitados_futuro.append(actual)
                            for sig in G.get(actual, []):
                                if sig not in visitados_futuro:
                                    por_revisar_futuro.append(sig)
                    indirectos_futuro = [x for x in visitados_futuro if x not in directos_futuro]
                    criticidad        = len(visitados_futuro)
                    estilo            = "result-error" if criticidad >= 5 else "result-ok"
                    alerta            = "⚠ ALERTA DE RIESGO ALTO — Reprobar esta materia congela gran parte de la carrera." \
                                        if criticidad >= 5 else \
                                        "✔ RIESGO CONTROLADO — Impacto moderado/bajo."
                    st.markdown(f"""<div class="result-box {estilo}">
<b>Bloqueos directos</b>
  {directos_futuro}

<b>Bloqueos indirectos</b>
  {indirectos_futuro}

<b>Índice de criticidad:</b> Bloquea {criticidad} materias.

{alerta}
</div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 — Integridad y cuellos de botella
# ════════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("#### Herramientas de validación global")

    col_c, col_b2 = st.columns(2)

    # ── Ciclos ────────────────────────────────────────────────────────────────
    with col_c:
        st.markdown("**🔄 Validar Consistencia (Ciclos)**")
        if st.button("Ejecutar detección de ciclos", key="ciclos"):
            visitados_d, en_ruta, ciclo_detectado = set(), set(), [False]

            def dfs(nodo):
                visitados_d.add(nodo)
                en_ruta.add(nodo)
                for vecino in G.get(nodo, []):
                    if vecino not in visitados_d:
                        if dfs(vecino):
                            return True
                    elif vecino in en_ruta:
                        ciclo_detectado[0] = True
                        return True
                en_ruta.remove(nodo)
                return False

            for n in G:
                if n not in visitados_d:
                    dfs(n)

            if ciclo_detectado[0]:
                st.markdown("""<div class="result-box result-error">
✘  ¡CICLO CIRCULAR DETECTADO!
   El grafo contiene dependencias circulares — revisar datos.
</div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div class="result-box result-ok">
✔  El grafo es un DAG válido
   (Grafo Dirigido Acíclico)
   No existen dependencias circulares.
</div>""", unsafe_allow_html=True)

    # ── Cuellos de botella ────────────────────────────────────────────────────
    with col_b2:
        st.markdown("**📊 Cursos Críticos (Cuellos de botella)**")
        if st.button("Calcular Top 5 críticos", key="bottleneck"):
            impacto = {}
            for curso in G.keys():
                vis  = set()
                cola = deque([curso])
                while cola:
                    act = cola.popleft()
                    for vec in G.get(act, []):
                        if vec not in vis:
                            vis.add(vec)
                            cola.append(vec)
                impacto[curso] = len(vis)

            ordenados = sorted(impacto.items(), key=lambda x: x[1], reverse=True)
            medals    = ["🥇", "🥈", "🥉", "4°", "5°"]

            rows = ""
            for i, (codigo, cant) in enumerate(ordenados[:5]):
                badge = "badge-error" if cant >= 5 else "badge-warn" if cant >= 3 else "badge-ok"
                rows += f"""<tr>
                  <td>{medals[i]}</td>
                  <td><span class="badge-code">{codigo}</span></td>
                  <td>{NOMBRES.get(codigo, '')}</td>
                  <td><span class="{badge}">{cant} cursos</span></td>
                </tr>"""

            st.markdown(f"""
            <table class="curso-table">
              <thead><tr><th>#</th><th>Código</th><th>Materia</th><th>Bloquea</th></tr></thead>
              <tbody>{rows}</tbody>
            </table>""", unsafe_allow_html=True)


# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#94a3b8;font-size:0.8rem;'>"
    "Universidad Nacional · Escuela de Informática · Estructuras de Datos 2026"
    "</p>",
    unsafe_allow_html=True,
)
