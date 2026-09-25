import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(page_title="Ideal Gas Law Process Simulator", page_icon="⚗️", layout="wide")

# ============================================================
# THEME — high-contrast dark theme, custom colours + fonts
# ============================================================
NAVY = "#0f2942"        # deep navy (used in hero + accents)
STEEL = "#2e8bd4"        # bright steel blue accent
BG = "#0b0f19"           # page background (near-black navy)
PANEL = "#141b2b"        # card / sidebar background
PANEL_BORDER = "#2a3a52"
TEXT = "#f4f7fb"         # primary text — near white
SUBTEXT = "#b9c4d4"      # secondary text
ACCENT = "#ffb703"       # amber accent for high contrast on dark navy
GOOD = "#3ddc97"
WARN = "#ffb703"
BAD = "#ff6b6b"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Roboto+Mono:wght@500&display=swap');

html, body, [class*="css"]  {{
    font-family: 'Inter', sans-serif;
}}

/* ---- Global page background + default text colour ---- */
.stApp {{
    background: {BG};
    color: {TEXT};
}}
.stApp, .stApp p, .stApp span, .stApp label, .stApp li, .stApp div {{
    color: {TEXT};
}}
h1, h2, h3, h4, h5, h6 {{ color: {TEXT} !important; }}
.stMarkdown, .stCaption, [data-testid="stCaptionContainer"] {{ color: {SUBTEXT}; }}
a, a:visited {{ color: {STEEL} !important; }}

/* ---- Hero banner ---- */
.hero {{
    background: linear-gradient(135deg, {NAVY} 0%, {STEEL} 100%);
    padding: 22px 28px;
    border-radius: 14px;
    color: #ffffff;
    margin-bottom: 18px;
    border: 1px solid {PANEL_BORDER};
}}
.hero h1 {{ margin: 0; font-size: 1.7rem; font-weight: 800; color: #ffffff !important; }}
.hero p {{ margin: 4px 0 0 0; opacity: 0.95; font-size: 0.95rem; color: #eaf2fa !important; }}

/* ---- Team info card ---- */
.team-card {{
    background: {PANEL};
    border-left: 5px solid {ACCENT};
    padding: 12px 16px;
    border-radius: 8px;
    font-size: 0.92rem;
    margin-bottom: 14px;
    color: {TEXT};
    border-top: 1px solid {PANEL_BORDER};
    border-right: 1px solid {PANEL_BORDER};
    border-bottom: 1px solid {PANEL_BORDER};
}}
.team-card b {{ color: {ACCENT}; }}

/* ---- Metrics ---- */
div[data-testid="stMetric"] {{
    background: {PANEL};
    border-radius: 10px;
    padding: 12px 10px 6px 10px;
    border: 1px solid {PANEL_BORDER};
}}
div[data-testid="stMetricLabel"] {{ color: {SUBTEXT} !important; }}
div[data-testid="stMetricValue"] {{ color: {ACCENT} !important; font-family: 'Roboto Mono', monospace; }}
div[data-testid="stMetricDelta"] {{ color: {GOOD} !important; }}

/* ---- Sidebar ---- */
section[data-testid="stSidebar"] {{
    background: {PANEL};
    border-right: 1px solid {PANEL_BORDER};
}}
section[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}
section[data-testid="stSidebar"] .stCaption, section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{
    color: {SUBTEXT} !important;
}}

/* ---- Inputs (text/number/textarea/select) ---- */
.stApp input, .stApp textarea, .stApp select {{
    background-color: #1b2333 !important;
    color: {TEXT} !important;
    border: 1px solid {PANEL_BORDER} !important;
}}
div[data-baseweb="select"] > div {{
    background-color: #1b2333 !important;
    color: {TEXT} !important;
    border-color: {PANEL_BORDER} !important;
}}
div[data-baseweb="popover"] * {{ color: {TEXT} !important; }}
ul[role="listbox"] {{ background-color: #1b2333 !important; }}

/* ---- Radio / checkbox / slider labels ---- */
.stRadio label, .stCheckbox label, .stSlider label {{ color: {TEXT} !important; }}
div[data-testid="stTickBarMin"], div[data-testid="stTickBarMax"] {{ color: {SUBTEXT} !important; }}
.stSlider [data-testid="stThumbValue"] {{ color: {ACCENT} !important; }}

/* ---- Tabs ---- */
button[data-baseweb="tab"] {{ color: {SUBTEXT} !important; }}
button[data-baseweb="tab"][aria-selected="true"] {{ color: {ACCENT} !important; }}
div[data-baseweb="tab-highlight"] {{ background-color: {ACCENT} !important; }}
div[data-baseweb="tab-border"] {{ background-color: {PANEL_BORDER} !important; }}

/* ---- Alerts (info/success/warning/error) ---- */
div[data-testid="stAlert"] {{ background: {PANEL}; border: 1px solid {PANEL_BORDER}; }}
div[data-testid="stAlert"] p {{ color: {TEXT} !important; }}

/* ---- Code / latex ---- */
.katex {{ color: {TEXT} !important; }}
code {{ color: {ACCENT} !important; background: #1b2333 !important; }}

/* ---- Tables ---- */
.stApp table {{ color: {TEXT} !important; }}
.stApp thead tr th {{ color: {ACCENT} !important; background: {PANEL} !important; }}
.stApp tbody tr td {{ color: {TEXT} !important; }}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR — TEAM DETAILS
# ============================================================
st.sidebar.header("👥 Team Details")
group_no = st.sidebar.text_input("Group Name", value="11")
members = st.sidebar.text_area("Member Names (one per line)", value="Dhrumil Patel\nShubh Patel")
enroll = st.sidebar.text_area("Enrollment Numbers (one per line)", value="25012250610063\n25012250610050")
guide_name = st.sidebar.text_input("Guide / Teacher Name", value="Shaikh Mohammed Azim")

st.sidebar.markdown("---")

# ============================================================
# SIDEBAR — GAS PROPERTIES
# ============================================================
st.sidebar.header("🧪 Gas Properties")

gas_data = {
    # name: (R kJ/kg.K, cv kJ/kg.K)
    "Air":              (0.2870, 0.718),
    "Nitrogen (N2)":    (0.2968, 0.743),
    "Oxygen (O2)":      (0.2598, 0.658),
    "Carbon Dioxide (CO2)": (0.1889, 0.657),
    "Helium (He)":      (2.0769, 3.1156),
    "Hydrogen (H2)":    (4.1240, 10.183),
    "Custom": None,
}
gas = st.sidebar.selectbox("Working Fluid (ideal gas)", list(gas_data.keys()))
if gas == "Custom":
    R = st.sidebar.number_input("Specific Gas Constant, R (kJ/kg·K)", min_value=0.0001, value=0.287, step=0.001, format="%.4f")
    cv = st.sidebar.number_input("Specific Heat at Const. Volume, cv (kJ/kg·K)", min_value=0.0001, value=0.718, step=0.001, format="%.4f")
else:
    R, cv = gas_data[gas]
    st.sidebar.caption(f"R = {R:.4f} kJ/kg·K, cv = {cv:.4f} kJ/kg·K (typical value — adjust for your textbook table).")
cp = cv + R
gamma = cp / cv

st.sidebar.markdown("---")

# ============================================================
# SIDEBAR — PROCESS TYPE
# ============================================================
st.sidebar.header("🔄 Process Type")
process = st.sidebar.radio("Select Process", ["Isothermal", "Isobaric", "Isochoric", "Polytropic"])

n_poly = None
if process == "Polytropic":
    n_poly = st.sidebar.slider("Polytropic Index, n", 0.10, 3.00, 1.30, 0.05)
    if abs(n_poly - 1.0) < 1e-6:
        st.sidebar.caption("n ≈ 1 behaves like an isothermal process (PV = const).")

st.sidebar.markdown("---")

# ============================================================
# SIDEBAR — INITIAL STATE
# ============================================================
st.sidebar.header("① Initial State")
P1 = st.sidebar.number_input("Initial Pressure, P₁ (kPa)", min_value=0.001, value=200.0, step=10.0)
V1_L = st.sidebar.number_input("Initial Volume, V₁ (L)", min_value=0.001, value=5.0, step=0.5)
T1 = st.sidebar.number_input("Initial Temperature, T₁ (K)", min_value=0.001, value=320.0, step=5.0)
V1 = V1_L / 1000.0  # m^3

st.sidebar.markdown("---")

# ============================================================
# SIDEBAR — FINAL STATE (only ONE property is known; app solves the rest)
# ============================================================
st.sidebar.header("② Final State (known value)")

known_var = None
known_val = None

if process == "Isothermal":
    st.sidebar.caption("T₂ = T₁ by definition — provide either V₂ or P₂.")
    known_var = st.sidebar.radio("Which final property do you know?", ["Final Volume V₂ (L)", "Final Pressure P₂ (kPa)"])
    if known_var == "Final Volume V₂ (L)":
        known_val = st.sidebar.number_input("Final Volume, V₂ (L)", min_value=0.001, value=10.0, step=0.5)
    else:
        known_val = st.sidebar.number_input("Final Pressure, P₂ (kPa)", min_value=0.001, value=100.0, step=10.0)

elif process == "Isobaric":
    st.sidebar.caption("P₂ = P₁ by definition — provide either V₂ or T₂.")
    known_var = st.sidebar.radio("Which final property do you know?", ["Final Volume V₂ (L)", "Final Temperature T₂ (K)"])
    if known_var == "Final Volume V₂ (L)":
        known_val = st.sidebar.number_input("Final Volume, V₂ (L)", min_value=0.001, value=10.0, step=0.5)
    else:
        known_val = st.sidebar.number_input("Final Temperature, T₂ (K)", min_value=0.001, value=640.0, step=5.0)

elif process == "Isochoric":
    st.sidebar.caption("V₂ = V₁ by definition — provide either P₂ or T₂.")
    known_var = st.sidebar.radio("Which final property do you know?", ["Final Pressure P₂ (kPa)", "Final Temperature T₂ (K)"])
    if known_var == "Final Pressure P₂ (kPa)":
        known_val = st.sidebar.number_input("Final Pressure, P₂ (kPa)", min_value=0.001, value=100.0, step=10.0)
    else:
        known_val = st.sidebar.number_input("Final Temperature, T₂ (K)", min_value=0.001, value=160.0, step=5.0)

else:  # Polytropic
    st.sidebar.caption("PVⁿ = constant — provide either V₂ or P₂.")
    known_var = st.sidebar.radio("Which final property do you know?", ["Final Volume V₂ (L)", "Final Pressure P₂ (kPa)"])
    if known_var == "Final Volume V₂ (L)":
        known_val = st.sidebar.number_input("Final Volume, V₂ (L)", min_value=0.001, value=10.0, step=0.5)
    else:
        known_val = st.sidebar.number_input("Final Pressure, P₂ (kPa)", min_value=0.001, value=80.0, step=10.0)

# ============================================================
# MAIN — HEADER
# ============================================================
st.markdown(f"""
<div class="hero">
    <h1>⚗️ Ideal Gas Law Process Simulator</h1>
    <p>Diploma in Mechanical Engineering — Semester 3 Python Mini Project · Thermodynamics</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="team-card">
<b>Group {group_no}</b> &nbsp;|&nbsp; <b>Member(s):</b> {members.replace(chr(10), ', ')}
&nbsp;|&nbsp; <b>Enrollment No.:</b> {enroll.replace(chr(10), ', ')}
&nbsp;|&nbsp; <b>Guide:</b> {guide_name}
</div>
""", unsafe_allow_html=True)

st.markdown(
    "This app models a closed system of an **ideal gas** undergoing an "
    "**Isothermal**, **Isobaric**, **Isochoric**, or **Polytropic** process. "
    "Provide the fully defined initial state and ONE known final property — "
    "the app solves for the remaining unknown, calculates the **boundary work**, "
    "**heat transferred**, and **change in internal energy**, and plots the process "
    "path on a P–V diagram and a 3D P–V–T surface."
)

# ============================================================
# VALIDATION
# ============================================================
errors = []
if P1 <= 0 or V1 <= 0 or T1 <= 0:
    errors.append("Initial pressure, volume and temperature must all be greater than zero.")
if R <= 0 or cv <= 0:
    errors.append("Gas constant R and specific heat cv must be greater than zero.")
if known_val is not None and known_val <= 0:
    errors.append("The known final-state value must be greater than zero.")

if errors:
    for e in errors:
        st.error(f"⚠️ {e}")
    st.stop()

# mass of gas in the closed system, from the fully-defined initial state
mass = (P1 * V1) / (R * T1)   # kg  (P kPa * V m^3 = kJ ; R kJ/kg.K * T K = kJ/kg)

# ============================================================
# SOLVE FOR THE FINAL STATE
# ============================================================
P2 = V2 = T2 = None

if process == "Isothermal":
    T2 = T1
    if known_var.startswith("Final Volume"):
        V2 = known_val / 1000.0
        P2 = (P1 * V1) / V2
    else:
        P2 = known_val
        V2 = (P1 * V1) / P2

elif process == "Isobaric":
    P2 = P1
    if known_var.startswith("Final Volume"):
        V2 = known_val / 1000.0
        T2 = T1 * (V2 / V1)
    else:
        T2 = known_val
        V2 = V1 * (T2 / T1)

elif process == "Isochoric":
    V2 = V1
    if known_var.startswith("Final Pressure"):
        P2 = known_val
        T2 = T1 * (P2 / P1)
    else:
        T2 = known_val
        P2 = P1 * (T2 / T1)

else:  # Polytropic
    n = n_poly
    if known_var.startswith("Final Volume"):
        V2 = known_val / 1000.0
        P2 = P1 * (V1 / V2) ** n
    else:
        P2 = known_val
        V2 = V1 * (P1 / P2) ** (1.0 / n)
    T2 = (P2 * V2) / (mass * R)

if V2 <= 0 or P2 <= 0 or T2 <= 0:
    st.error("⚠️ The computed final state is non-physical (zero or negative). Adjust your inputs.")
    st.stop()

# ============================================================
# WORK, HEAT, INTERNAL ENERGY
# ============================================================
if process == "Isochoric":
    W = 0.0
elif process == "Isobaric":
    W = P1 * (V2 - V1)
elif process == "Isothermal":
    W = P1 * V1 * np.log(V2 / V1)
else:  # Polytropic
    n = n_poly
    if abs(n - 1.0) < 1e-6:
        W = P1 * V1 * np.log(V2 / V1)
    else:
        W = (P1 * V1 - P2 * V2) / (n - 1.0)

delta_U = mass * cv * (T2 - T1)     # kJ
Q = delta_U + W                     # kJ  (first law, closed system)

if V2 > V1:
    change_label = "Expansion"
elif V2 < V1:
    change_label = "Compression"
else:
    change_label = "No volume change"

# ============================================================
# P–V CURVE FOR THE CURRENT PROCESS
# ============================================================
def process_curve(P1, V1, P2, V2, process, n=None, num=120):
    if process == "Isochoric":
        V_arr = np.full(num, V1)
        P_arr = np.linspace(P1, P2, num)
    elif process == "Isobaric":
        V_arr = np.linspace(V1, V2, num)
        P_arr = np.full(num, P1)
    elif process == "Isothermal":
        V_arr = np.linspace(V1, V2, num)
        C = P1 * V1
        P_arr = C / V_arr
    else:  # Polytropic
        V_arr = np.linspace(V1, V2, num)
        C = P1 * V1 ** n
        P_arr = C / V_arr ** n
    return V_arr, P_arr


V_curve, P_curve = process_curve(P1, V1, P2, V2, process, n_poly)

# ============================================================
# 3D P–V–T SURFACE (Plotly) — ideal gas equation of state, with process path
# ============================================================
def build_pvt_figure(mass, R, V1, V2, T1, T2, process, n=None, n_grid=40):
    V_lo = 0.5 * min(V1, V2)
    V_hi = 1.6 * max(V1, V2)
    T_lo = 0.6 * min(T1, T2)
    T_hi = 1.5 * max(T1, T2)
    if V_lo <= 0:
        V_lo = 0.1 * min(V1, V2)
    if T_lo <= 0:
        T_lo = 0.1 * min(T1, T2)

    V_grid = np.linspace(V_lo, V_hi, n_grid)
    T_grid = np.linspace(T_lo, T_hi, n_grid)
    Vg, Tg = np.meshgrid(V_grid, T_grid)
    Pg = mass * R * Tg / Vg

    # process path points
    num = 60
    if process == "Isochoric":
        V_path = np.full(num, V1)
        T_path = np.linspace(T1, T2, num)
    elif process == "Isobaric":
        V_path = np.linspace(V1, V2, num)
        T_path = T1 + (T2 - T1) * (V_path - V1) / (V2 - V1) if V2 != V1 else np.full(num, T1)
    elif process == "Isothermal":
        V_path = np.linspace(V1, V2, num)
        T_path = np.full(num, T1)
    else:  # Polytropic
        V_path = np.linspace(V1, V2, num)
        P_path_tmp = (P1 * V1 ** n) / V_path ** n
        T_path = (P_path_tmp * V_path) / (mass * R)
    P_path = mass * R * T_path / V_path

    fig = go.Figure()
    fig.add_trace(go.Surface(
        x=Vg, y=Tg, z=Pg,
        colorscale=[[0, "#12314f"], [0.5, STEEL], [1, ACCENT]],
        opacity=0.55, showscale=False, name="P = mRT / V",
        hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter3d(
        x=V_path, y=T_path, z=P_path,
        mode="lines", line=dict(color=ACCENT, width=8), name="Process Path",
    ))
    fig.add_trace(go.Scatter3d(
        x=[V1, V2], y=[T1, T2], z=[P1, P2],
        mode="markers+text", marker=dict(size=6, color=["#3ddc97", "#ff6b6b"]),
        text=["State 1", "State 2"], textposition="top center",
        textfont=dict(color="#f4f7fb", size=12), name="States",
    ))
    fig.update_layout(
        scene=dict(
            xaxis=dict(title="Volume, V (m³)", color="#f4f7fb", gridcolor="#2a3a52", backgroundcolor="#0b0f19"),
            yaxis=dict(title="Temperature, T (K)", color="#f4f7fb", gridcolor="#2a3a52", backgroundcolor="#0b0f19"),
            zaxis=dict(title="Pressure, P (kPa)", color="#f4f7fb", gridcolor="#2a3a52", backgroundcolor="#0b0f19"),
            camera=dict(eye=dict(x=1.6, y=-1.6, z=1.0)),
        ),
        paper_bgcolor="#0b0f19",
        font=dict(color="#f4f7fb"),
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=0.01, xanchor="left", x=0.01,
                    font=dict(color="#f4f7fb")),
        height=560,
    )
    return fig


# ============================================================
# TABS
# ============================================================
tab_results, tab_graphs, tab_3d, tab_formulas = st.tabs(
    ["📐 Results", "📊 Graphs", "🧊 3D P–V–T Surface", "📘 Formulas"]
)

# ---------------- RESULTS TAB ----------------
with tab_results:
    st.subheader(f"{process} Process — {change_label}")

    st.markdown("**Initial State (State 1)**")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pressure, P₁", f"{P1:.2f} kPa")
    c2.metric("Volume, V₁", f"{V1_L:.3f} L")
    c3.metric("Temperature, T₁", f"{T1:.2f} K")
    c4.metric("Gas Mass, m", f"{mass * 1000:.2f} g")

    st.markdown("**Final State (State 2) — solved from process relation**")
    d1, d2, d3 = st.columns(3)
    d1.metric("Pressure, P₂", f"{P2:.2f} kPa")
    d2.metric("Volume, V₂", f"{V2 * 1000:.3f} L")
    d3.metric("Temperature, T₂", f"{T2:.2f} K")

    st.markdown("**Energy Balance (First Law of Thermodynamics)**")
    e1, e2, e3 = st.columns(3)
    e1.metric("Boundary Work, W", f"{W:.3f} kJ", help="Positive = work done BY the gas (expansion)")
    e2.metric("Change in Internal Energy, ΔU", f"{delta_U:.3f} kJ")
    e3.metric("Heat Transferred, Q", f"{Q:.3f} kJ", help="Positive = heat added TO the gas")

    if Q > 0:
        st.success(f"✅ Q = {Q:.3f} kJ of heat is **added to** the gas during this process.")
    elif Q < 0:
        st.info(f"ℹ️ Q = {abs(Q):.3f} kJ of heat is **rejected by** the gas during this process.")
    else:
        st.info("ℹ️ No net heat transfer occurs during this process (Q ≈ 0).")

# ---------------- GRAPHS TAB ----------------
with tab_graphs:
    colA, colB = st.columns(2)

    with colA:
        st.markdown(f"**P–V Diagram — {process} Process**")
        fig1, ax1 = plt.subplots(figsize=(5.4, 4.2))
        ax1.plot(V_curve * 1000, P_curve, color=STEEL, linewidth=2.5, label=f"{process} path")
        ax1.plot(V1 * 1000, P1, "o", color="#3ddc97", markersize=9, label="State 1")
        ax1.plot(V2 * 1000, P2, "o", color="#ff6b6b", markersize=9, label="State 2")
        ax1.fill_between(V_curve * 1000, P_curve, 0, color=STEEL, alpha=0.12)
        ax1.set_xlabel("Volume, V (L)")
        ax1.set_ylabel("Pressure, P (kPa)")
        ax1.set_title(f"Shaded area = boundary work ≈ {W:.2f} kJ")
        ax1.grid(True, linestyle=":", alpha=0.6)
        ax1.legend(fontsize=8)
        st.pyplot(fig1)

    with colB:
        st.markdown("**Work · ΔU · Heat Comparison**")
        fig2, ax2 = plt.subplots(figsize=(5.4, 4.2))
        labels = ["Work, W", "ΔU", "Heat, Q"]
        values = [W, delta_U, Q]
        colors = [STEEL, NAVY, ACCENT]
        bars = ax2.bar(labels, values, color=colors, width=0.55)
        ax2.axhline(0, color="#555555", linewidth=0.8)
        for b in bars:
            h = b.get_height()
            ax2.text(b.get_x() + b.get_width() / 2, h + (0.02 * max(abs(v) for v in values) or 0.1) * (1 if h >= 0 else -1),
                      f"{h:.2f}", ha="center", va="bottom" if h >= 0 else "top", fontsize=9)
        ax2.set_ylabel("Energy (kJ)")
        ax2.grid(True, axis="y", linestyle=":", alpha=0.6)
        st.pyplot(fig2)

    st.markdown("**Comparison of Process Paths from the Same Initial State**")
    if abs(V2 - V1) < 1e-12:
        st.info("ℹ️ The current process is isochoric (V₂ = V₁), so a shared-volume comparison curve isn't applicable. "
                "The chart below instead shows how Isothermal, Isobaric and Polytropic paths would look for a "
                "20% volume expansion from the same initial state.")
        V2_ref = V1 * 1.2
    else:
        V2_ref = V2

    V_iso, P_iso = process_curve(P1, V1, None, V2_ref, "Isothermal")
    V_iba, P_iba = process_curve(P1, V1, None, V2_ref, "Isobaric")
    n_ref = n_poly if n_poly else 1.3
    V_pol, P_pol = process_curve(P1, V1, None, V2_ref, "Polytropic", n_ref)

    fig3, ax3 = plt.subplots(figsize=(9.5, 4.2))
    ax3.plot(V_iso * 1000, P_iso, color="#2e8bd4", linewidth=2, label="Isothermal (n=1)")
    ax3.plot(V_iba * 1000, P_iba, color="#3ddc97", linewidth=2, label="Isobaric (n=0)")
    ax3.plot(V_pol * 1000, P_pol, color=ACCENT, linewidth=2, label=f"Polytropic (n={n_ref:.2f})")
    ax3.axvline(V1 * 1000, color="#888888", linestyle="--", linewidth=1, label="Isochoric (V=V₁)")
    ax3.plot(V1 * 1000, P1, "o", color="#f4f7fb", markersize=8, label="State 1")
    ax3.set_xlabel("Volume, V (L)")
    ax3.set_ylabel("Pressure, P (kPa)")
    ax3.grid(True, linestyle=":", alpha=0.6)
    ax3.legend(fontsize=8)
    st.pyplot(fig3)

# ---------------- 3D P-V-T TAB ----------------
with tab_3d:
    st.markdown(
        "Interactive 3D surface of the ideal gas equation of state **P = mRT / V**, with the current "
        "process path traced across it — drag to rotate, scroll to zoom. The green marker is State 1 "
        "and the red marker is State 2."
    )
    fig3d = build_pvt_figure(mass, R, V1, V2, T1, T2, process, n_poly)
    st.plotly_chart(fig3d, width="stretch")

# ---------------- FORMULAS TAB ----------------
with tab_formulas:
    st.markdown("**Ideal Gas Law**")
    st.latex(r"PV = mRT")

    st.markdown("**Process-Specific Relations**")
    st.latex(r"\text{Isothermal } (T=\text{const}):\quad P_1V_1 = P_2V_2")
    st.latex(r"\text{Isobaric } (P=\text{const}):\quad \dfrac{V_1}{T_1} = \dfrac{V_2}{T_2}")
    st.latex(r"\text{Isochoric } (V=\text{const}):\quad \dfrac{P_1}{T_1} = \dfrac{P_2}{T_2}")
    st.latex(r"\text{Polytropic}:\quad P_1V_1^{\,n} = P_2V_2^{\,n}")

    st.markdown("**Boundary (Moving-Boundary) Work**")
    st.latex(r"\text{Isochoric:}\quad W = 0")
    st.latex(r"\text{Isobaric:}\quad W = P(V_2 - V_1)")
    st.latex(r"\text{Isothermal:}\quad W = P_1V_1 \ln\!\left(\dfrac{V_2}{V_1}\right) = mRT\ln\!\left(\dfrac{V_2}{V_1}\right)")
    st.latex(r"\text{Polytropic } (n\neq1):\quad W = \dfrac{P_1V_1 - P_2V_2}{n-1}")

    st.markdown("**First Law of Thermodynamics (closed system)**")
    st.latex(r"Q = \Delta U + W, \qquad \Delta U = m\,c_v\,(T_2-T_1)")

    st.markdown(
        f"""
        - **P** = absolute pressure (kPa)
        - **V** = volume (m³)
        - **T** = absolute temperature (K)
        - **m** = mass of gas in the closed system (kg) — solved from the initial state as *m = P₁V₁ / (R·T₁)*
        - **R** = specific gas constant (kJ/kg·K); currently **{R:.4f} kJ/kg·K**
        - **cᵥ** = specific heat at constant volume (kJ/kg·K); currently **{cv:.4f} kJ/kg·K**
        - **cₚ** = specific heat at constant pressure = cᵥ + R = **{cp:.4f} kJ/kg·K**
        - **γ (gamma)** = cₚ / cᵥ = **{gamma:.4f}**
        - **n** = polytropic index (n = 0 → isobaric, n = 1 → isothermal, n = γ → isentropic, n → ∞ → isochoric)

        Sign convention used throughout: **W > 0** when the gas expands and does work on its
        surroundings; **Q > 0** when heat is added to the gas. Confirm the exact property values
        and sign convention used in your textbook when writing up the manual vs. app comparison.
        """
    )
