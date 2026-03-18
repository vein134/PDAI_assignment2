"""
smart_relocation.py - HomeIQ: Smart Relocation Advisor
Run:     streamlit run smart_relocation.py
Install: pip install streamlit plotly pandas numpy requests openai fpdf2
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import requests
from io import StringIO
import json
import openai
from fpdf import FPDF
from datetime import date

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(page_title="HomeIQ - Smart Relocation Advisor", page_icon="🏠", layout="wide")

# ── Global CSS — Premium Dark Theme ───────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --navy:      #0a0e1a;
    --navy-2:    #111827;
    --navy-3:    #1a2235;
    --navy-4:    #243048;
    --gold:      #c9a84c;
    --gold-light:#e8c97a;
    --gold-dim:  #7a6030;
    --cream:     #f5f0e8;
    --white:     #ffffff;
    --muted:     #8899aa;
}

.stApp, [data-testid="stAppViewContainer"] {
    background: var(--navy) !important;
    font-family: 'DM Sans', sans-serif !important;
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
.stDeployButton { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebarCollapsedControl"] { display: none !important; }

[data-testid="stSidebar"] {
    background: #0d1526 !important;
    border-right: 1px solid #2a3550 !important;
}
[data-testid="stSidebar"] * {
    color: #dde6f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stToggle label {
    color: #b0c0d0 !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
[data-testid="stSidebar"] h1 {
    font-family: 'Playfair Display', serif !important;
    color: var(--gold) !important;
    font-size: 22px !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stNumberInput > div > div > input,
[data-testid="stSidebar"] input {
    background: #1a2640 !important;
    border: 1px solid #2a3550 !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    font-size: 14px !important;
}

div[data-baseweb="popover"],
div[data-baseweb="select"] ul,
div[data-baseweb="menu"] {
    background: #1a2640 !important;
    border: 1px solid #2a3550 !important;
    border-radius: 8px !important;
}
div[data-baseweb="menu"] li,
div[data-baseweb="option"] {
    background: #1a2640 !important;
    color: #f5f0e8 !important;
}
div[data-baseweb="option"]:hover,
div[data-baseweb="option"][aria-selected="true"] {
    background: #243048 !important;
    color: #c9a84c !important;
}
[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMin"],
[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMax"],
[data-testid="stSidebar"] .stSlider span {
    color: #b0c0d0 !important;
    font-size: 13px !important;
}

.stMarkdown, .stText, p, li, span, label, div {
    color: var(--cream) !important;
    font-family: 'DM Sans', sans-serif !important;
}
h1, h2, h3, h4 {
    font-family: 'Playfair Display', serif !important;
    color: var(--white) !important;
}

[data-testid="stDataFrame"] { background: var(--navy-3) !important; }
[data-testid="stDataFrame"] td,
[data-testid="stDataFrame"] th {
    color: #ffffff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
}
[data-testid="stDataFrame"] thead th {
    background: var(--navy-4) !important;
    color: var(--gold) !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.stCaption, [data-testid="stCaptionContainer"] p {
    color: #aabbcc !important;
    font-size: 13px !important;
}
[data-testid="stTabContent"] p,
[data-testid="stTabContent"] span,
[data-testid="stTabContent"] div {
    color: var(--cream) !important;
}
table { width: 100%; border-collapse: collapse; }
table td, table th {
    color: var(--white) !important;
    background: var(--navy-3) !important;
    border: 1px solid var(--navy-4) !important;
    padding: 8px 12px !important;
    font-size: 13px !important;
}
table thead th {
    background: var(--navy-4) !important;
    color: var(--gold) !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
[data-testid="stMetric"] {
    background: var(--navy-3) !important;
    border: 1px solid var(--navy-4) !important;
    border-radius: 12px !important;
    padding: 20px !important;
}
[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
[data-testid="stMetricValue"] {
    color: var(--white) !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 28px !important;
}
[data-testid="stTabs"] [role="tablist"] {
    background: var(--navy-2) !important;
    border-bottom: 1px solid var(--navy-4) !important;
    gap: 4px;
    padding: 4px 8px 0;
}
[data-testid="stTabs"] [role="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border: none !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500;
    padding: 10px 18px !important;
    border-radius: 8px 8px 0 0 !important;
    transition: all 0.2s;
}
[data-testid="stTabs"] [role="tab"]:hover { color: var(--gold-light) !important; background: var(--navy-3) !important; }
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: var(--navy-3) !important;
    color: var(--gold) !important;
    border-bottom: 2px solid var(--gold) !important;
}
[data-testid="stTabContent"] {
    background: var(--navy-2) !important;
    border: 1px solid var(--navy-4) !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
    padding: 24px !important;
}
.stButton > button {
    background: linear-gradient(135deg, var(--gold), var(--gold-dim)) !important;
    color: var(--navy) !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(201,168,76,0.35) !important;
}
.stDownloadButton > button {
    background: var(--navy-3) !important;
    color: var(--gold) !important;
    border: 1px solid var(--gold-dim) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
[data-testid="stAlert"] {
    background: var(--navy-3) !important;
    border-radius: 10px !important;
    border-left-width: 3px !important;
}
[data-testid="stExpander"] {
    background: var(--navy-3) !important;
    border: 1px solid var(--navy-4) !important;
    border-radius: 10px !important;
}
hr { border-color: var(--navy-4) !important; margin: 24px 0 !important; }
[data-testid="stChatMessage"] {
    background: var(--navy-3) !important;
    border: 1px solid var(--navy-4) !important;
    border-radius: 12px !important;
}
[data-testid="stChatInput"] textarea {
    background: var(--navy-3) !important;
    border: 1px solid var(--navy-4) !important;
    color: var(--white) !important;
    border-radius: 10px !important;
}
.stTextArea textarea {
    background: #1a2640 !important;
    border: 1px solid #2a3550 !important;
    color: #f5f0e8 !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextArea textarea::placeholder {
    color: #8899aa !important;
}

/* Global input styling for all form elements */
.stNumberInput input,
.stTextInput input,
.stSelectbox > div > div,
.stMultiSelect > div > div,
.stSelectbox [data-baseweb="select"] > div,
.stMultiSelect [data-baseweb="select"] > div,
input[type="number"],
input[type="text"] {
    background: #1a2640 !important;
    border: 1px solid #2a3550 !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    font-family: 'DM Sans', sans-serif !important;
}
/* Labels for all inputs */
.stNumberInput label,
.stTextInput label,
.stSelectbox label,
.stMultiSelect label,
.stSlider label,
.stTextArea label {
    color: #b0c0d0 !important;
    font-size: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
}
/* Slider text */
.stSlider [data-testid="stTickBarMin"],
.stSlider [data-testid="stTickBarMax"],
.stSlider span,
.stSlider div[data-testid="stThumbValue"] {
    color: #f5f0e8 !important;
}
/* Dropdown menus globally */
[data-baseweb="select"] span,
[data-baseweb="tag"] span {
    color: #ffffff !important;
}
/* Multiselect tags */
[data-baseweb="tag"] {
    background: #243048 !important;
    border: 1px solid #c9a84c44 !important;
    color: #f5f0e8 !important;
}
/* Placeholder text */
input::placeholder,
textarea::placeholder {
    color: #8899aa !important;
}
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--navy-2); }
::-webkit-scrollbar-thumb { background: var(--navy-4); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Plotly theme ───────────────────────────────────────────────────────────
PLOT_THEME = dict(
    paper_bgcolor="#111827", plot_bgcolor="#1a2235",
    font=dict(color="#f5f0e8", family="DM Sans"),
    xaxis=dict(gridcolor="#243048", linecolor="#243048"),
    yaxis=dict(gridcolor="#243048", linecolor="#243048"),
    legend=dict(
        bgcolor="rgba(26,34,53,0.9)",
        bordercolor="#2a3550",
        borderwidth=1,
        font=dict(color="#f5f0e8", size=12),
    ),
)
def hex_to_rgba(hex_color, alpha=0.13):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

C = dict(gold="#c9a84c", green="#2dd4a0", red="#f87171", blue="#60a5fa",
         muted="#8899aa", purple="#a78bfa", orange="#fb923c", cyan="#22d3ee")

# ── Live Data: Bank of England & ONS ──────────────────────────────────────
@st.cache_data(show_spinner="Fetching live data from Bank of England & ONS...", ttl=3600)
def fetch_live_data():
    data = {}
    try:
        boe_url = (
            "https://www.bankofengland.co.uk/boeapps/iadb/fromshowcolumns.asp"
            "?csv.x=yes&Datefrom=01/Jan/2020&Dateto=now"
            "&SeriesCodes=IUMBEDR&CSVF=TN&UsingCodes=Y&VPD=Y&VFD=N"
        )
        resp = requests.get(boe_url, timeout=10)
        resp.raise_for_status()
        df_boe = pd.read_csv(StringIO(resp.text), skiprows=1, names=["DATE", "base_rate"])
        df_boe["base_rate"] = pd.to_numeric(df_boe["base_rate"], errors="coerce")
        data["base_rate_current"] = round(float(df_boe["base_rate"].dropna().iloc[-1]), 2)
    except Exception:
        data["base_rate_current"] = 3.75
    try:
        mort_url = (
            "https://www.bankofengland.co.uk/boeapps/iadb/fromshowcolumns.asp"
            "?csv.x=yes&Datefrom=01/Jan/2020&Dateto=now"
            "&SeriesCodes=IUMBV34,IUMBV42&CSVF=TN&UsingCodes=Y&VPD=Y&VFD=N"
        )
        resp = requests.get(mort_url, timeout=10)
        resp.raise_for_status()
        df_mort = pd.read_csv(StringIO(resp.text), skiprows=1, names=["DATE", "rate_2yr", "rate_5yr"])
        df_mort["rate_2yr"] = pd.to_numeric(df_mort["rate_2yr"], errors="coerce")
        df_mort["rate_5yr"] = pd.to_numeric(df_mort["rate_5yr"], errors="coerce")
        data["rate_2yr_current"] = round(float(df_mort["rate_2yr"].dropna().iloc[-1]), 2)
        data["rate_5yr_current"] = round(float(df_mort["rate_5yr"].dropna().iloc[-1]), 2)
    except Exception:
        data["rate_2yr_current"] = 4.2
        data["rate_5yr_current"] = 4.4
    try:
        ons_cpi_url = "https://api.ons.gov.uk/v1/datasets/mm23/timeseries/D7G7/data"
        resp = requests.get(ons_cpi_url, timeout=10)
        resp.raise_for_status()
        months = resp.json().get("months", [])
        df_cpi = pd.DataFrame(months)[["date", "value"]].rename(columns={"date": "DATE", "value": "cpi"})
        df_cpi["cpi"] = pd.to_numeric(df_cpi["cpi"], errors="coerce")
        data["cpi_current"] = round(float(df_cpi["cpi"].dropna().iloc[-1]), 1)
    except Exception:
        data["cpi_current"] = 3.0
    try:
        ons_earn_url = "https://api.ons.gov.uk/v1/datasets/lms/timeseries/KAB9/data"
        resp = requests.get(ons_earn_url, timeout=10)
        resp.raise_for_status()
        months = resp.json().get("months", [])
        df_earn = pd.DataFrame(months)[["date", "value"]].rename(columns={"date": "DATE", "value": "eg"})
        df_earn["eg"] = pd.to_numeric(df_earn["eg"], errors="coerce")
        data["earnings_growth_current"] = round(float(df_earn["eg"].dropna().iloc[-1]), 1)
    except Exception:
        data["earnings_growth_current"] = 5.9
    return data

live = fetch_live_data()

# ── Regional Data Model ───────────────────────────────────────────────────
# Sources: ONS House Price Statistics (Dec 2024), ONS Annual Survey of Hours
# and Earnings (2024), VOA Council Tax Valuation Lists, ONS Regional GVA,
# Ofsted Regional Statistics, ONS Crime Survey for England & Wales.
# QoL scores (0-100) are composite indices derived from ONS wellbeing data,
# DEFRA green space statistics, and NHS regional performance metrics.
# Live macro data (base rate, CPI, earnings growth) is fetched from BoE IADB
# and ONS APIs at runtime — see fetch_live_data() above.
REGIONS = {
    "London": {
        "avg_price": 520000, "rental_yield": 3.2, "avg_salary": 44000,
        "col_index": 100, "council_tax": 1898,
        "commute": 40, "green_space": 45, "schools": 75, "safety": 50,
        "culture": 95, "healthcare": 80, "job_market": 95,
    },
    "South East": {
        "avg_price": 380000, "rental_yield": 3.8, "avg_salary": 38000,
        "col_index": 88, "council_tax": 2050,
        "commute": 55, "green_space": 75, "schools": 80, "safety": 72,
        "culture": 65, "healthcare": 75, "job_market": 80,
    },
    "South West": {
        "avg_price": 310000, "rental_yield": 4.1, "avg_salary": 34000,
        "col_index": 82, "council_tax": 2100,
        "commute": 60, "green_space": 90, "schools": 72, "safety": 80,
        "culture": 60, "healthcare": 68, "job_market": 55,
    },
    "East of England": {
        "avg_price": 340000, "rental_yield": 3.9, "avg_salary": 36000,
        "col_index": 85, "council_tax": 1950,
        "commute": 50, "green_space": 70, "schools": 74, "safety": 75,
        "culture": 50, "healthcare": 70, "job_market": 65,
    },
    "East Midlands": {
        "avg_price": 230000, "rental_yield": 4.6, "avg_salary": 32000,
        "col_index": 75, "council_tax": 1850,
        "commute": 65, "green_space": 72, "schools": 68, "safety": 70,
        "culture": 50, "healthcare": 65, "job_market": 55,
    },
    "West Midlands": {
        "avg_price": 245000, "rental_yield": 4.5, "avg_salary": 33000,
        "col_index": 77, "council_tax": 1780,
        "commute": 58, "green_space": 60, "schools": 65, "safety": 60,
        "culture": 70, "healthcare": 72, "job_market": 65,
    },
    "Yorkshire": {
        "avg_price": 200000, "rental_yield": 5.0, "avg_salary": 31000,
        "col_index": 73, "council_tax": 1750,
        "commute": 62, "green_space": 80, "schools": 66, "safety": 62,
        "culture": 65, "healthcare": 68, "job_market": 55,
    },
    "North West": {
        "avg_price": 210000, "rental_yield": 5.2, "avg_salary": 32000,
        "col_index": 74, "council_tax": 1800,
        "commute": 58, "green_space": 65, "schools": 64, "safety": 55,
        "culture": 80, "healthcare": 72, "job_market": 65,
    },
    "North East": {
        "avg_price": 155000, "rental_yield": 5.8, "avg_salary": 30000,
        "col_index": 70, "council_tax": 1700,
        "commute": 68, "green_space": 75, "schools": 60, "safety": 58,
        "culture": 50, "healthcare": 64, "job_market": 40,
    },
    "Wales": {
        "avg_price": 195000, "rental_yield": 4.8, "avg_salary": 30500,
        "col_index": 72, "council_tax": 1650,
        "commute": 60, "green_space": 92, "schools": 62, "safety": 75,
        "culture": 55, "healthcare": 60, "job_market": 40,
    },
    "Scotland": {
        "avg_price": 195000, "rental_yield": 4.7, "avg_salary": 33000,
        "col_index": 74, "council_tax": 1450,
        "commute": 62, "green_space": 88, "schools": 72, "safety": 68,
        "culture": 75, "healthcare": 74, "job_market": 60,
    },
    "Northern Ireland": {
        "avg_price": 175000, "rental_yield": 5.5, "avg_salary": 30000,
        "col_index": 68, "council_tax": 1350,
        "commute": 65, "green_space": 85, "schools": 70, "safety": 72,
        "culture": 45, "healthcare": 62, "job_market": 35,
    },
}

QOL_DIMS = ["commute", "green_space", "schools", "safety", "culture", "healthcare"]
QOL_LABELS = ["Commute", "Green Space", "Schools", "Safety", "Culture", "Healthcare"]
REGION_COLORS = dict(zip(REGIONS.keys(), [
    C["gold"], C["blue"], C["green"], "#818cf8", C["purple"], C["orange"],
    C["cyan"], C["red"], "#f472b6", "#34d399", "#fbbf24", "#fb7185"
]))

# ── Commute cost data (annual season tickets to key hubs, drive miles one-way) ──
COMMUTE_COSTS = {
    ("South East", "London"): {"season_ticket": 4500, "drive_miles": 45},
    ("South West", "London"): {"season_ticket": 8500, "drive_miles": 120},
    ("East of England", "London"): {"season_ticket": 5200, "drive_miles": 55},
    ("East Midlands", "London"): {"season_ticket": 9200, "drive_miles": 110},
    ("West Midlands", "London"): {"season_ticket": 10400, "drive_miles": 120},
    ("Yorkshire", "London"): {"season_ticket": 11500, "drive_miles": 185},
    ("North West", "London"): {"season_ticket": 11800, "drive_miles": 200},
    ("North East", "London"): {"season_ticket": 12500, "drive_miles": 260},
    ("Wales", "London"): {"season_ticket": 9800, "drive_miles": 155},
    ("Scotland", "London"): {"season_ticket": 13500, "drive_miles": 400},
    ("Northern Ireland", "London"): {"season_ticket": 15000, "drive_miles": 500},
    ("East Midlands", "West Midlands"): {"season_ticket": 3200, "drive_miles": 50},
    ("Yorkshire", "North West"): {"season_ticket": 3800, "drive_miles": 60},
    ("Yorkshire", "West Midlands"): {"season_ticket": 5500, "drive_miles": 90},
    ("North West", "West Midlands"): {"season_ticket": 4200, "drive_miles": 80},
    ("South East", "South West"): {"season_ticket": 4800, "drive_miles": 100},
    ("Scotland", "North East"): {"season_ticket": 4500, "drive_miles": 105},
    ("Wales", "West Midlands"): {"season_ticket": 3600, "drive_miles": 70},
    ("East of England", "East Midlands"): {"season_ticket": 4000, "drive_miles": 75},
}
HMRC_MILEAGE_RATE = 0.45  # per mile

# ── Financial helpers ─────────────────────────────────────────────────────
def compute_uk_tax(gross):
    """UK income tax + NI. Returns dict with net annual/monthly."""
    personal_allowance = 12570
    if gross > 125140:
        personal_allowance = 0
    elif gross > 100000:
        personal_allowance = max(0, 12570 - (gross - 100000) / 2)
    taxable = max(0, gross - personal_allowance)
    tax = 0
    if taxable > 0:
        basic = min(taxable, 37700)
        tax += basic * 0.20
    if taxable > 37700:
        higher = min(taxable - 37700, 87440)
        tax += higher * 0.40
    if taxable > 125140:
        tax += (taxable - 125140) * 0.45
    # NI (Class 1, employee)
    ni = 0
    if gross > 12570:
        ni_basic = min(gross, 50270) - 12570
        ni += ni_basic * 0.08
    if gross > 50270:
        ni += (gross - 50270) * 0.02
    net = gross - tax - ni
    return {"gross": gross, "tax": round(tax), "ni": round(ni),
            "net_annual": round(net), "net_monthly": round(net / 12)}

def compute_stamp_duty(price, ftb=False):
    if ftb:
        if price <= 425000:
            return 0
        elif price <= 625000:
            return round((price - 425000) * 0.05)
    bands = [(250000, 0.0), (675000, 0.05), (925000, 0.10), (1500000, 0.12)]
    tax, prev = 0.0, 0.0
    for threshold, rate in bands:
        if price <= prev:
            break
        tax += (min(price, threshold) - prev) * rate
        prev = threshold
    return round(tax)

def compute_monthly_budget(salary, partner_salary, region_name, deposit_pct, mortgage_rate):
    """Compute monthly budget breakdown for a region if buying."""
    r = REGIONS[region_name]
    household_gross = salary + partner_salary
    tax1 = compute_uk_tax(salary)
    tax2 = compute_uk_tax(partner_salary) if partner_salary > 0 else {"net_monthly": 0}
    net_monthly = tax1["net_monthly"] + tax2["net_monthly"]
    # Housing: mortgage payment
    price = r["avg_price"]
    loan = price * (1 - deposit_pct / 100)
    mr = mortgage_rate / 100 / 12
    n = 25 * 12
    monthly_mortgage = loan * (mr * (1 + mr)**n) / ((1 + mr)**n - 1) if mr > 0 else loan / n
    monthly_rent = int(price * r["rental_yield"] / 100 / 12)
    council_tax_monthly = r["council_tax"] / 12
    # Living costs scaled by CoL index (base £1500/month at London=100)
    living_costs = 1500 * r["col_index"] / 100
    return {
        "net_monthly": round(net_monthly),
        "monthly_mortgage": round(monthly_mortgage),
        "monthly_rent": round(monthly_rent),
        "council_tax_monthly": round(council_tax_monthly),
        "living_costs": round(living_costs),
        "disposable_buy": round(net_monthly - monthly_mortgage - council_tax_monthly - living_costs),
        "disposable_rent": round(net_monthly - monthly_rent - council_tax_monthly - living_costs),
        "price": price,
        "loan": round(loan),
    }

def compute_regional_score(region_name, profile, financial_weight=50, deposit_pct=15):
    """Composite score (0-100) = weighted financial + QoL."""
    r = REGIONS[region_name]
    salary = profile.get("salary") or 50000
    partner_salary = profile.get("partner_salary") or 0
    user_budget = profile.get("budget") or None
    priorities = profile.get("priorities") or []

    household_income = salary + partner_salary
    # Financial sub-score — use region avg price but penalise if it exceeds user budget
    price_for_scoring = r["avg_price"]
    if user_budget and user_budget < r["avg_price"]:
        # Over-budget penalty: treat effective price as 10% above budget
        price_for_scoring = user_budget * 1.10
    affordability = price_for_scoring / max(household_income, 1)
    afford_score = max(0, min(100, 100 - (affordability - 3) * 20))  # 3x = 100, 8x = 0

    budget_data = compute_monthly_budget(salary, partner_salary, region_name, deposit_pct,
                                          live["rate_5yr_current"])
    disp_score = max(0, min(100, budget_data["disposable_buy"] / 30))  # £3000 disp = 100

    financial_score = (afford_score * 0.5 + disp_score * 0.5)

    # QoL sub-score
    priority_map = {
        "green_space": "green_space", "schools": "schools", "safety": "safety",
        "culture": "culture", "healthcare": "healthcare", "commute": "commute",
        "family_friendly": "schools", "affordability": None,
    }
    weights = {d: 1.0 for d in QOL_DIMS}
    for p in priorities:
        dim = priority_map.get(p)
        if dim and dim in weights:
            weights[dim] = 2.5  # boost priority dimensions

    total_w = sum(weights.values())
    qol_score = sum(r[d] * weights[d] for d in QOL_DIMS) / total_w

    # Composite
    fw = financial_weight / 100
    composite = financial_score * fw + qol_score * (1 - fw)

    return {
        "financial_score": round(financial_score, 1),
        "qol_score": round(qol_score, 1),
        "composite": round(composite, 1),
        "affordability_ratio": round(affordability, 1),
        "disposable_monthly": budget_data["disposable_buy"],
        "monthly_mortgage": budget_data["monthly_mortgage"],
        "monthly_rent": budget_data["monthly_rent"],
        "price": r["avg_price"],
    }

def compute_affordability(salary, partner_salary, region_name, deposit_pct, current_savings=0):
    """Mortgage affordability analysis for a specific region."""
    r = REGIONS[region_name]
    household_income = salary + partner_salary
    max_borrowing = household_income * 4.5
    price = r["avg_price"]
    deposit = price * deposit_pct / 100
    loan = price - deposit
    stamp = compute_stamp_duty(price, True)
    solicitor = 1500
    survey = 500
    total_upfront = deposit + stamp + solicitor + survey
    shortfall = max(0, total_upfront - current_savings)
    # Estimate monthly savings capacity (30% of disposable)
    t = compute_uk_tax(salary)
    t2 = compute_uk_tax(partner_salary) if partner_salary else {"net_monthly": 0}
    net_monthly = t["net_monthly"] + t2["net_monthly"]
    living = 1500 * r["col_index"] / 100
    est_monthly_save = max(100, (net_monthly - living - r["council_tax"] / 12) * 0.30)
    months_to_save = int(np.ceil(shortfall / est_monthly_save)) if shortfall > 0 else 0
    # Stress test: payments at various rates
    stress_rates = np.arange(2.0, 10.5, 0.5)
    stress_payments = []
    for sr in stress_rates:
        mr = sr / 100 / 12
        mp = loan * (mr * (1 + mr)**300) / ((1 + mr)**300 - 1)
        stress_payments.append(round(mp))
    return {
        "max_borrowing": round(max_borrowing),
        "loan_needed": round(loan),
        "can_borrow": loan <= max_borrowing,
        "price": price, "deposit": round(deposit), "stamp": stamp,
        "solicitor": solicitor, "survey": survey,
        "total_upfront": round(total_upfront), "shortfall": round(shortfall),
        "months_to_save": months_to_save, "est_monthly_save": round(est_monthly_save),
        "stress_rates": stress_rates.tolist(), "stress_payments": stress_payments,
        "net_monthly": round(net_monthly),
        "danger_line": round(net_monthly * 0.35),
    }

def run_regional_monte_carlo(regions_list, profile, n_sims=1000, horizon=10, seed=42, deposit_pct=15):
    """Vectorised Monte Carlo across multiple regions."""
    rng = np.random.default_rng(seed)
    salary = (profile.get("salary") or 50000)
    partner_salary = (profile.get("partner_salary") or 0)
    base_rate = live["rate_5yr_current"]
    cpi = live["cpi_current"]

    results = {}
    # Shared macro shocks (same for all regions in each sim)
    rate_shocks = rng.normal(0, 1.0, (n_sims, horizon))  # annual rate perturbation
    inflation_shocks = rng.normal(0, 1.0, (n_sims, horizon))

    for region_name in regions_list:
        r = REGIONS[region_name]
        price = float(r["avg_price"])
        loan = price * (1 - deposit_pct / 100)
        deposit = price * deposit_pct / 100
        stamp = compute_stamp_duty(price, True)
        monthly_rent_base = price * r["rental_yield"] / 100 / 12
        col_factor = r["col_index"] / 100

        # Region-specific appreciation distribution
        appreciation = rng.normal(3.5, 2.0, (n_sims, horizon))
        yearly_vol = rng.normal(0, 3.0, (n_sims, horizon))

        # Effective mortgage rate per sim (sample first year shock, not mean)
        eff_rates = np.clip(base_rate + rate_shocks[:, 0], 1.0, 10.0)
        mr = eff_rates / 100 / 12
        n_months = 25 * 12
        monthly_mortgages = loan * (mr * (1 + mr)**n_months) / ((1 + mr)**n_months - 1)

        # Tax calculation for household
        t1 = compute_uk_tax(salary)
        t2 = compute_uk_tax(partner_salary) if partner_salary else {"net_monthly": 0}
        net_monthly = t1["net_monthly"] + t2["net_monthly"]
        living_costs = 1500 * col_factor

        # Year-by-year simulation
        prop_values = np.full(n_sims, float(price))
        cum_buy_costs = np.full(n_sims, float(deposit + stamp))
        cum_rent_costs = np.zeros(n_sims)
        loan_balances = np.full(n_sims, float(loan))
        current_rent = np.full(n_sims, monthly_rent_base)

        wealth_buy_paths = np.zeros((n_sims, horizon))
        wealth_rent_paths = np.zeros((n_sims, horizon))

        for yr in range(horizon):
            app = appreciation[:, yr] + yearly_vol[:, yr]
            prop_values *= (1 + app / 100)

            # Buy path: pay mortgage + maintenance, build equity
            interest = loan_balances * (eff_rates / 100)
            principal = np.minimum(monthly_mortgages * 12 - interest, loan_balances)
            loan_balances = np.maximum(0, loan_balances - principal)
            equity = prop_values - loan_balances
            cum_buy_costs += monthly_mortgages * 12 + prop_values * 0.01

            # Rent path: pay rent (inflation-adjusted)
            rent_inflation = cpi + inflation_shocks[:, yr] * 1.5
            current_rent *= (1 + np.clip(rent_inflation, 0, 10) / 100)
            cum_rent_costs += current_rent * 12

            # Net wealth: equity minus total costs paid (buy) vs negative costs (rent)
            wealth_buy_paths[:, yr] = equity - cum_buy_costs
            wealth_rent_paths[:, yr] = -cum_rent_costs

        # Net advantage of buying: final buy wealth minus final rent wealth
        net_advantage = wealth_buy_paths[:, -1] - wealth_rent_paths[:, -1]

        results[region_name] = {
            "wealth_outcomes": net_advantage,
            "equity_paths": wealth_buy_paths,
            "p10": float(np.percentile(net_advantage, 10)),
            "p50": float(np.percentile(net_advantage, 50)),
            "p90": float(np.percentile(net_advantage, 90)),
            "mean": float(np.mean(net_advantage)),
            "std": float(np.std(net_advantage)),
        }

    # Compute P(region wins) — which region gives best outcome in each sim
    all_outcomes = np.column_stack([results[r]["wealth_outcomes"] for r in regions_list])
    best_indices = np.argmax(all_outcomes, axis=1)
    for i, region_name in enumerate(regions_list):
        results[region_name]["prob_best"] = float(np.mean(best_indices == i))

    return results

# ── LLM: Life Brief Parser ────────────────────────────────────────────────
def parse_life_brief(text, api_key):
    """Extract structured JSON from free-text life brief using GPT-4o."""
    client = openai.OpenAI(api_key=api_key)
    system_prompt = """You are a data extraction engine. Parse the user's relocation brief into structured JSON.
Extract ONLY what is explicitly stated or clearly implied. Use null for anything not mentioned.

Required JSON schema:
{
    "salary": <int, annual gross GBP>,
    "partner_salary": <int or 0>,
    "job_type": <"remote"|"hybrid"|"office">,
    "office_location": <string region name or null>,
    "commute_days": <int 0-5>,
    "budget": <int, max property budget GBP or null>,
    "priorities": <list of: "green_space", "schools", "safety", "culture", "healthcare", "commute", "affordability", "family_friendly">,
    "age": <int or null>,
    "household": <"single"|"couple"|"family">,
    "children": <int or 0>,
    "notes": <string, any other relevant context>
}

If salary not stated but budget is, estimate salary from 4.5x mortgage rule.
If budget not stated but salary is, estimate budget as (salary + partner_salary) * 4.5 * 0.85 + deposit.
Map locations to: London, South East, South West, East of England, East Midlands, West Midlands, Yorkshire, North West, North East, Wales, Scotland, Northern Ireland."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        response_format={"type": "json_object"},
        max_tokens=500,
        temperature=0.2,
    )
    return json.loads(response.choices[0].message.content)

# ── PDF Report ────────────────────────────────────────────────────────────
def generate_pdf(profile, rankings, live_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(10, 14, 26)
    pdf.rect(0, 0, 210, 35, "F")
    pdf.set_text_color(201, 168, 76)
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_xy(10, 8)
    pdf.cell(0, 12, "HomeIQ - Smart Relocation Report", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(180, 180, 180)
    pdf.set_xy(10, 22)
    pdf.cell(0, 8, f"Generated {date.today().strftime('%d %B %Y')}", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Your Profile", ln=True)
    pdf.set_font("Helvetica", "", 10)
    for k, v in [("Salary", f"£{(profile.get('salary') or 0):,}"),
                  ("Partner Salary", f"£{(profile.get('partner_salary') or 0):,}"),
                  ("Work Type", profile.get("job_type") or "N/A"),
                  ("Budget", f"£{(profile.get('budget') or 0):,}" if profile.get("budget") else "Auto"),
                  ("Priorities", ", ".join(profile.get("priorities") or []))]:
        pdf.cell(80, 7, k, border="B")
        pdf.cell(110, 7, str(v), border="B", ln=True)
    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Regional Ranking", ln=True)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(10, 14, 26)
    pdf.set_text_color(201, 168, 76)
    for h, w in [("Region", 40), ("Score", 25), ("Financial", 25), ("QoL", 25), ("Affordability", 30), ("Disposable", 30)]:
        pdf.cell(w, 8, h, fill=True, border=1)
    pdf.ln()
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 9)
    for r in rankings[:10]:
        pdf.cell(40, 7, r["region"], border=1)
        pdf.cell(25, 7, f"{r['composite']}", border=1)
        pdf.cell(25, 7, f"{r['financial_score']}", border=1)
        pdf.cell(25, 7, f"{r['qol_score']}", border=1)
        pdf.cell(30, 7, f"{r['affordability_ratio']}x", border=1)
        pdf.cell(30, 7, f"£{r['disposable_monthly']:,}", border=1)
        pdf.ln()
    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(0, 5, "Disclaimer: Illustrative purposes only. Not financial advice. "
                   "Data sourced from Bank of England and ONS public APIs.")
    return bytes(pdf.output())

# ── LLM: Neighbourhood Finder ────────────────────────────────────────────
def find_neighbourhoods(region, profile, budget, live_data, api_key):
    """Use GPT-4o to recommend specific neighbourhoods within a region based on user priorities."""
    client = openai.OpenAI(api_key=api_key)
    priorities = profile.get("priorities", [])
    household = profile.get("household", "single")
    children = profile.get("children", 0)
    job_type = profile.get("job_type", "remote")
    office_loc = profile.get("office_location")

    system_prompt = f"""You are a UK property and neighbourhood expert. Given a UK region, user profile, and budget,
recommend exactly 5 specific neighbourhoods/towns/areas within or close to that region.

CRITICAL RULES:
- Return ONLY real UK places that actually exist
- Each area must be a specific town, neighbourhood, or suburb — NOT a broad region
- Include the postcode district (e.g. "M20" for Didsbury, "BS9" for Stoke Bishop)
- Estimated average property prices should be realistic for 2024-2025
- School ratings should reflect actual Ofsted area performance (Outstanding/Good/Requires Improvement)
- Be specific about transport links (actual station names, actual road numbers)

Return JSON with this exact schema:
{{
    "neighbourhoods": [
        {{
            "name": "<specific place name>",
            "postcode_area": "<postcode district>",
            "type": "<suburb|town|village|city_neighbourhood>",
            "avg_property_price": <int>,
            "price_range": "<e.g. £180k - £320k>",
            "school_rating": "<Outstanding|Good|Mixed|Requires Improvement>",
            "notable_schools": ["<school name 1>", "<school name 2>"],
            "transport": "<key transport links — stations, motorways>",
            "commute_to_centre": "<minutes to nearest city centre>",
            "green_space_score": <1-10>,
            "safety_score": <1-10>,
            "family_score": <1-10>,
            "culture_score": <1-10>,
            "match_score": <1-100, how well it matches the user's priorities>,
            "pros": ["<pro 1>", "<pro 2>", "<pro 3>"],
            "cons": ["<con 1>", "<con 2>"],
            "description": "<2-3 sentence description of the area's character>"
        }}
    ],
    "region_summary": "<1-2 sentence overview of the region's neighbourhood landscape>"
}}"""

    user_msg = f"""Region: {region}
Budget: £{budget:,} (flexible ±20%)
Household: {household}{f', {children} children' if children else ''}
Work: {job_type}{f', office in {office_loc}' if office_loc else ''}
Priorities: {', '.join(p.replace('_', ' ') for p in priorities) if priorities else 'balanced'}
Current mortgage rate: {live_data.get('rate_5yr_current', 4.5)}%

Find 5 specific areas that best match this profile. Rank by match_score (highest first).
Prioritise areas with {'excellent schools and family amenities' if 'schools' in priorities or 'family_friendly' in priorities else 'good overall livability'}.
{'Focus on areas with good commute links to ' + office_loc if office_loc else ''}"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg}
        ],
        response_format={"type": "json_object"},
        max_tokens=2000,
        temperature=0.3,
    )
    return json.loads(response.choices[0].message.content)

# ── Analysis settings — read from session state (set by Brief tab widgets) ─
OPENAI_KEY = st.secrets["OPENAI_KEY"]

financial_weight = int(st.session_state.get("cfg_fw", 50))
sb_priorities    = list(st.session_state.get("cfg_priorities", ["schools", "green_space"]))
horizon          = int(st.session_state.get("cfg_horizon", 10))
deposit_pct      = int(st.session_state.get("cfg_deposit", 15))

# ── Build profile from Brief tab form inputs ──────────────────────────────
def get_active_profile():
    sal = int(st.session_state.get("bp_sal", 50000) or 50000)
    psal = int(st.session_state.get("bp_psal", 0) or 0)
    job = st.session_state.get("bp_job", "remote") or "remote"
    office_raw = st.session_state.get("bp_office", "N/A") or "N/A"
    budget_raw = st.session_state.get("bp_budget", 0) or 0
    hh = st.session_state.get("bp_hh", "single") or "single"
    p = {
        "salary": sal,
        "partner_salary": psal,
        "job_type": job,
        "office_location": office_raw if office_raw != "N/A" else None,
        "commute_days": int(st.session_state.get("bp_commute_days", 0) or 0),
        "budget": int(budget_raw) if budget_raw > 0 else None,
        "priorities": list(st.session_state.get("cfg_priorities", ["schools", "green_space"])),
        "household": hh,
    }
    # Merge extra LLM-extracted metadata (age, children, notes) if available
    extra = st.session_state.get("user_profile", {})
    for k in ("age", "children", "notes"):
        if extra.get(k):
            p[k] = extra[k]
    return p

profile = get_active_profile()

# ── Compute rankings ──────────────────────────────────────────────────────
rankings = []
for rname in REGIONS:
    score = compute_regional_score(rname, profile, financial_weight, deposit_pct)
    rankings.append({"region": rname, **score})
rankings.sort(key=lambda x: x["composite"], reverse=True)
top_region = rankings[0]["region"]

# ── Hero header ───────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,#111827 0%,#1a2235 50%,#111827 100%);
            border:1px solid #243048;border-radius:16px;padding:40px 48px;
            margin-bottom:32px;position:relative;overflow:hidden;">
    <div style="position:absolute;top:-60px;right:-60px;width:240px;height:240px;
                background:radial-gradient(circle,rgba(201,168,76,0.12) 0%,transparent 70%);border-radius:50%;"></div>
    <div style="font-family:'Playfair Display',serif;font-size:13px;color:#c9a84c;
                letter-spacing:0.15em;text-transform:uppercase;margin-bottom:10px;">
        Smart Relocation Intelligence
    </div>
    <h1 style="font-family:'Playfair Display',serif;font-size:42px;color:#ffffff;
               margin:0 0 12px 0;font-weight:900;line-height:1.1;">
        Where Should You<br>Live in the UK?
    </h1>
    <p style="color:#8899aa;font-size:15px;max-width:580px;line-height:1.6;margin:0;">
        Powered by live <strong style="color:#c9a84c;">Bank of England</strong> and
        <strong style="color:#c9a84c;">ONS</strong> data. Set your profile in the Your Brief tab
        to discover which region optimises your financial and lifestyle outcome.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Key metrics ───────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Best Region", top_region, f"Score: {rankings[0]['composite']}")
c2.metric("Best Disposable", f"£{max(r['disposable_monthly'] for r in rankings):,}/mo",
          max(rankings, key=lambda x: x["disposable_monthly"])["region"])
c3.metric("Most Affordable", f"{min(r['affordability_ratio'] for r in rankings)}x",
          min(rankings, key=lambda x: x["affordability_ratio"])["region"])
c4.metric("Best QoL", f"{max(r['qol_score'] for r in rankings)}",
          max(rankings, key=lambda x: x["qol_score"])["region"])

st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────
tab_brief, tab_ranking, tab_mc, tab_afford, tab_areas, tab_advisor = st.tabs([
    "Your Brief", "Ranking & Compare",
    "Monte Carlo", "Affordability & Costs",
    "Neighbourhoods", "AI Advisor"
])

# ── TAB 1: Your Brief ────────────────────────────────────────────────────
with tab_brief:
    # ── Section 1: AI text brief ──────────────────────────────────────────
    st.markdown("<div style='font-family:Playfair Display,serif;font-size:20px;color:#fff;margin-bottom:4px;'>Tell Us About Yourself</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#8899aa;font-size:13px;margin-bottom:14px;'>Describe your situation in plain English and AI will fill your profile. Or just fill the form below directly.</div>", unsafe_allow_html=True)

    brief_text = st.text_area(
        "Life Brief",
        height=120,
        placeholder="e.g. I'm a 32-year-old software engineer earning £75k, working remotely. "
                    "My partner earns £40k. We want to start a family and prefer green spaces and good schools. "
                    "Our budget is around £400k.",
        label_visibility="collapsed",
    )
    btn_col, status_col = st.columns([1, 3])
    with btn_col:
        parse_clicked = st.button("AI Auto-fill", key="parse_btn", type="primary")
    with status_col:
        if st.session_state.get("brief_parsed"):
            st.success("Profile auto-filled — review and adjust below.")
    if parse_clicked:
        if not brief_text.strip():
            st.warning("Please write a brief first.")
        else:
            with st.spinner("Extracting your profile with AI..."):
                try:
                    parsed = parse_life_brief(brief_text, OPENAI_KEY)
                    if parsed.get("salary"):
                        st.session_state.bp_sal = int(parsed["salary"])
                    if parsed.get("partner_salary"):
                        st.session_state.bp_psal = int(parsed["partner_salary"])
                    if parsed.get("job_type") in ["remote", "hybrid", "office"]:
                        st.session_state.bp_job = parsed["job_type"]
                    if parsed.get("office_location"):
                        st.session_state.bp_office = parsed["office_location"]
                    if parsed.get("budget"):
                        st.session_state.bp_budget = int(parsed["budget"])
                    if parsed.get("household") in ["single", "couple", "family"]:
                        st.session_state.bp_hh = parsed["household"]
                    if parsed.get("commute_days") is not None:
                        st.session_state.bp_commute_days = int(parsed["commute_days"] or 0)
                    st.session_state.user_profile = parsed
                    st.session_state.brief_parsed = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Could not parse brief: {str(e)}")

    # ── Section 2: Profile form ───────────────────────────────────────────
    st.divider()
    st.markdown("<div style='font-family:Playfair Display,serif;font-size:18px;color:#fff;margin-bottom:12px;'>Your Profile</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("Annual Salary (£)", 15000, 500000,
                        value=int(st.session_state.get("bp_sal", 50000) or 50000),
                        step=1000, key="bp_sal")
        st.number_input("Partner Salary (£)", 0, 500000,
                        value=int(st.session_state.get("bp_psal", 0) or 0),
                        step=1000, key="bp_psal")
    with col2:
        _job_opts = ["remote", "hybrid", "office"]
        _job_cur = st.session_state.get("bp_job", "remote") or "remote"
        st.selectbox("Work Type", _job_opts,
                     index=_job_opts.index(_job_cur) if _job_cur in _job_opts else 0,
                     key="bp_job")
        st.number_input("Max Property Budget (£)", 0, 2000000,
                        value=int(st.session_state.get("bp_budget", 0) or 0),
                        step=10000, key="bp_budget",
                        help="Leave 0 to auto-calculate from salary.")
    with col3:
        _hh_opts = ["single", "couple", "family"]
        _hh_cur = st.session_state.get("bp_hh", "single") or "single"
        st.selectbox("Household Type", _hh_opts,
                     index=_hh_opts.index(_hh_cur) if _hh_cur in _hh_opts else 0,
                     key="bp_hh")
        _office_opts = ["N/A"] + list(REGIONS.keys())
        _office_cur = st.session_state.get("bp_office", "N/A") or "N/A"
        st.selectbox("Office Location", _office_opts,
                     index=_office_opts.index(_office_cur) if _office_cur in _office_opts else 0,
                     key="bp_office")

    # ── Section 3: Analysis settings ─────────────────────────────────────
    st.divider()
    st.markdown("<div style='font-family:Playfair Display,serif;font-size:18px;color:#fff;margin-bottom:12px;'>Analysis Settings</div>", unsafe_allow_html=True)
    as1, as2, as3, as4 = st.columns([2, 3, 1, 1])
    with as1:
        st.slider("Financial vs QoL Weight", 0, 100,
                  value=int(st.session_state.get("cfg_fw", 50)),
                  help="0 = pure quality of life · 100 = pure financial",
                  key="cfg_fw")
    with as2:
        if "cfg_priorities" not in st.session_state:
            st.session_state.cfg_priorities = ["schools", "green_space"]
        st.multiselect("Your Priorities",
            ["green_space", "schools", "safety", "culture", "healthcare", "commute", "family_friendly"],
            format_func=lambda x: x.replace("_", " ").title(),
            key="cfg_priorities")
    with as3:
        st.slider("Horizon (yrs)", 5, 25,
                  value=int(st.session_state.get("cfg_horizon", 10)),
                  key="cfg_horizon")
    with as4:
        st.slider("Deposit (%)", 5, 50,
                  value=int(st.session_state.get("cfg_deposit", 15)),
                  key="cfg_deposit")

    # ── Section 4: Live market data ───────────────────────────────────────
    st.divider()
    st.markdown("<div style='font-family:Playfair Display,serif;font-size:18px;color:#fff;margin-bottom:12px;'>Live Market Data</div>", unsafe_allow_html=True)
    ld1, ld2, ld3, ld4 = st.columns(4)
    for col, label, val, color in [
        (ld1, "BoE Base Rate",   f"{live['base_rate_current']}%",       "#c9a84c"),
        (ld2, "CPI Inflation",   f"{live['cpi_current']}%",             "#60a5fa"),
        (ld3, "5yr Fixed Rate",  f"{live['rate_5yr_current']}%",        "#f87171"),
        (ld4, "Earnings Growth", f"{live['earnings_growth_current']}%", "#2dd4a0"),
    ]:
        col.markdown(
            f'<div style="background:#1a2235;border:1px solid #243048;border-radius:10px;padding:14px 16px;">'
            f'<div style="color:#8899aa;font-size:10px;text-transform:uppercase;letter-spacing:0.08em;">{label}</div>'
            f'<div style="font-size:26px;font-weight:700;color:{color};margin-top:4px;">{val}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

# ── TAB 2: Regional Ranking & Compare ────────────────────────────────────
with tab_ranking:
    st.markdown("<div style='color:#8899aa;font-size:13px;margin-bottom:20px;'>All 12 UK regions ranked by your personalised composite score. Select regions below to compare.</div>", unsafe_allow_html=True)

    # Ranked bar chart
    st.markdown("<div style='font-family:Playfair Display,serif;font-size:20px;color:#fff;margin-bottom:8px;'>Regional Ranking</div>", unsafe_allow_html=True)
    sorted_r = list(reversed(rankings))
    fig_rank = go.Figure()
    fig_rank.add_trace(go.Bar(
        y=[r["region"] for r in sorted_r],
        x=[r["composite"] for r in sorted_r],
        orientation="h",
        marker_color=[REGION_COLORS.get(r["region"], C["gold"]) for r in sorted_r],
        text=[f"{r['composite']:.0f}" for r in sorted_r],
        textposition="auto",
    ))
    fig_rank.update_layout(**PLOT_THEME, height=480, xaxis_title="Composite Score (0-100)",
                            showlegend=False)
    st.plotly_chart(fig_rank, use_container_width=True)

    # Score table
    st.divider()
    st.markdown("<div style='font-family:Playfair Display,serif;font-size:18px;color:#fff;margin-bottom:8px;'>Detailed Scores</div>", unsafe_allow_html=True)
    df_rank = pd.DataFrame([{
        "Region": r["region"],
        "Composite": r["composite"],
        "Financial": r["financial_score"],
        "Quality of Life": r["qol_score"],
        "Affordability": f"{r['affordability_ratio']}x",
        "Disposable (£/mo)": f"£{r['disposable_monthly']:,}",
        "Avg Price": f"£{r['price']:,}",
        "Mortgage (£/mo)": f"£{r['monthly_mortgage']:,}",
    } for r in rankings])
    st.dataframe(df_rank.set_index("Region"), use_container_width=True)

    # Compare selected regions
    st.divider()
    st.markdown("<div style='font-family:Playfair Display,serif;font-size:18px;color:#fff;margin-bottom:8px;'>Compare Regions</div>", unsafe_allow_html=True)
    default_compare = [rankings[0]["region"], rankings[1]["region"]]
    compare_regions = st.multiselect("Select regions to compare", list(REGIONS.keys()),
                                      default=default_compare, max_selections=3, key="compare_sel")

    if len(compare_regions) >= 2:
        cols = st.columns(len(compare_regions))
        for i, rname in enumerate(compare_regions):
            with cols[i]:
                b = compute_monthly_budget((profile.get("salary") or 50000),
                                            (profile.get("partner_salary") or 0),
                                            rname, deposit_pct, live["rate_5yr_current"])
                fig_w = go.Figure(go.Waterfall(
                    orientation="v",
                    measure=["absolute", "relative", "relative", "relative", "total"],
                    x=["Net Income", "Mortgage", "Council Tax", "Living", "Disposable"],
                    y=[b["net_monthly"], -b["monthly_mortgage"], -b["council_tax_monthly"],
                       -b["living_costs"], 0],
                    connector={"line": {"color": "#243048"}},
                    decreasing={"marker": {"color": C["red"]}},
                    increasing={"marker": {"color": C["green"]}},
                    totals={"marker": {"color": C["gold"]}},
                ))
                fig_w.update_layout(**PLOT_THEME, height=320, showlegend=False,
                                     yaxis_tickprefix="£", yaxis_tickformat=",",
                                     title=dict(text=rname, font=dict(color=REGION_COLORS.get(rname, C["gold"]), size=13)))
                st.plotly_chart(fig_w, use_container_width=True)
                st.metric("Disposable", f"£{b['disposable_buy']:,}/mo")

        # Radar chart for compared regions
        st.divider()
        st.markdown("<div style='font-family:Playfair Display,serif;font-size:18px;color:#fff;margin-bottom:8px;'>Quality of Life Comparison</div>", unsafe_allow_html=True)
        fig_radar = go.Figure()
        for rname in compare_regions:
            rdata = REGIONS[rname]
            scores = [rdata[d] for d in QOL_DIMS] + [rdata[QOL_DIMS[0]]]
            labels = QOL_LABELS + [QOL_LABELS[0]]
            fig_radar.add_trace(go.Scatterpolar(
                r=scores, theta=labels, name=rname,
                line_color=REGION_COLORS.get(rname, C["gold"]),
                fill="toself",
                fillcolor=hex_to_rgba(REGION_COLORS.get(rname, C["gold"]), 0.08),
            ))
        fig_radar.update_layout(
            **{k: v for k, v in PLOT_THEME.items() if k not in ("xaxis", "yaxis")},
            height=420,
            polar=dict(
                bgcolor="#1a2235",
                radialaxis=dict(gridcolor="#243048", range=[0, 100], tickfont=dict(color="#8899aa")),
                angularaxis=dict(gridcolor="#243048", tickfont=dict(color="#f5f0e8")),
            ),
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # PDF export
    st.divider()
    if st.button("Download PDF Report", key="pdf_btn"):
        pdf_bytes = generate_pdf(profile, rankings, live)
        st.session_state.pdf_bytes = pdf_bytes
    if "pdf_bytes" in st.session_state:
        st.download_button("Download PDF", data=st.session_state.pdf_bytes,
                            file_name=f"homeiq_relocation_{date.today()}.pdf",
                            mime="application/pdf", key="pdf_dl")

# ── TAB 4: Monte Carlo ──────────────────────────────────────────────────
with tab_mc:
    st.markdown("<div style='color:#8899aa;font-size:13px;margin-bottom:20px;'>Run 1,000+ simulations across regions to see the probability distribution of financial outcomes.</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:Playfair Display,serif;font-size:20px;color:#fff;margin-bottom:16px;'>Cross-Regional Monte Carlo Simulation</div>", unsafe_allow_html=True)

    mc_col1, mc_col2 = st.columns(2)
    with mc_col1:
        n_sims = st.slider("Simulations", 500, 3000, 1000, 250, key="mc_nsims")
    with mc_col2:
        mc_regions = st.multiselect("Regions to simulate", list(REGIONS.keys()),
                                     default=[r["region"] for r in rankings[:5]], key="mc_regions")

    if st.button("Run Monte Carlo", key="mc_run") and len(mc_regions) >= 2:
        with st.spinner(f"Running {n_sims:,} simulations across {len(mc_regions)} regions..."):
            mc = run_regional_monte_carlo(mc_regions, profile, n_sims, horizon, deposit_pct=deposit_pct)
            st.session_state.mc_results = mc
            st.session_state.mc_results_regions = mc_regions

    if "mc_results" in st.session_state:
        mc = st.session_state.mc_results
        mc_regs = st.session_state.mc_results_regions

        # P(Region Wins)
        st.divider()
        st.markdown("<div style='font-family:Playfair Display,serif;font-size:18px;color:#fff;margin-bottom:8px;'>Probability Each Region Wins</div>", unsafe_allow_html=True)
        prob_cols = st.columns(min(len(mc_regs), 5))
        sorted_mc = sorted(mc_regs, key=lambda r: mc[r]["prob_best"], reverse=True)
        for i, rname in enumerate(sorted_mc[:5]):
            with prob_cols[i]:
                prob = mc[rname]["prob_best"] * 100
                st.metric(rname, f"{prob:.0f}%",
                          "Most likely" if i == 0 else None,
                          delta_color="normal" if i == 0 else "off")

        # Histogram overlay
        st.divider()
        st.markdown("<div style='font-family:Playfair Display,serif;font-size:18px;color:#fff;margin-bottom:8px;'>Wealth Outcome Distribution</div>", unsafe_allow_html=True)
        fig_hist = go.Figure()
        for rname in mc_regs:
            fig_hist.add_trace(go.Histogram(
                x=mc[rname]["wealth_outcomes"], name=rname,
                marker_color=REGION_COLORS.get(rname, C["gold"]),
                opacity=0.5, nbinsx=50,
            ))
        fig_hist.add_vline(x=0, line_dash="solid", line_color=C["red"], line_width=2,
                            annotation_text="Break-even", annotation_font_color=C["red"])
        fig_hist.update_layout(**PLOT_THEME, barmode="overlay", height=420,
                                xaxis_title="Net Wealth Outcome (£)", yaxis_title="Frequency",
                                xaxis_tickprefix="£", xaxis_tickformat=",")
        st.plotly_chart(fig_hist, use_container_width=True)

        # Summary table
        st.divider()
        mc_table = []
        for rname in sorted_mc:
            m = mc[rname]
            mc_table.append({
                "Region": rname,
                "P(Wins)": f"{m['prob_best']*100:.0f}%",
                "Median": f"£{m['p50']:,.0f}",
                "P10 (Worst)": f"£{m['p10']:,.0f}",
                "P90 (Best)": f"£{m['p90']:,.0f}",
                "Mean": f"£{m['mean']:,.0f}",
                "Std Dev": f"£{m['std']:,.0f}",
            })
        st.dataframe(pd.DataFrame(mc_table).set_index("Region"), use_container_width=True)

        # LLM Risk Narrative
        st.divider()
        st.markdown("<div style='font-family:Playfair Display,serif;font-size:18px;color:#fff;margin-bottom:8px;'>AI Risk Narrative</div>", unsafe_allow_html=True)
        mc_narrative_key = f"mc_nar_{n_sims}_{','.join(mc_regs)}_{profile.get('salary')}_{horizon}"
        if st.session_state.get("mc_narrative_key") != mc_narrative_key:
            mc_summary = "\n".join([
                f"- {rname}: P(Wins)={mc[rname]['prob_best']*100:.1f}%, Median=£{mc[rname]['p50']:,.0f}, "
                f"P10=£{mc[rname]['p10']:,.0f}, P90=£{mc[rname]['p90']:,.0f}, Mean=£{mc[rname]['mean']:,.0f}"
                for rname in sorted_mc
            ])
            mc_prompt = f"""You are an expert UK relocation financial analyst. Interpret these cross-regional
Monte Carlo simulation results. Write 5-6 sentences of flowing prose. Be specific with numbers and
probabilities. Compare the top regions. Mention risks. Do NOT use bullet points.

USER: Salary £{(profile.get('salary') or 50000):,}, {profile.get('job_type') or 'remote'} worker, {horizon}yr horizon
PRIORITIES: {', '.join(profile.get('priorities') or [])}

SIMULATION RESULTS ({n_sims} simulations):
{mc_summary}

LIVE MARKET: BoE rate {live['base_rate_current']}%, CPI {live['cpi_current']}%"""

            with st.spinner("Generating AI risk narrative..."):
                try:
                    client = openai.OpenAI(api_key=OPENAI_KEY)
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": mc_prompt}],
                        max_tokens=400, temperature=0.7,
                    )
                    mc_narrative = response.choices[0].message.content or "Analysis complete."
                except Exception as e:
                    mc_narrative = "AI narrative temporarily unavailable. See the statistics above for detailed results."
                st.session_state.mc_narrative = mc_narrative
                st.session_state.mc_narrative_key = mc_narrative_key

        mc_narrative = st.session_state.get("mc_narrative", "")
        if mc_narrative:
            st.markdown(
                f'<div style="background:linear-gradient(135deg,#111827,#1a2235);border:1px solid #c9a84c44;'
                f'border-left:4px solid #c9a84c;border-radius:12px;padding:24px 28px;">'
                f'<div style="color:#f5f0e8;font-size:15px;line-height:1.8;font-family:\'DM Sans\',sans-serif;">'
                f'{mc_narrative}</div>'
                f'<div style="color:#8899aa;font-size:11px;margin-top:16px;border-top:1px solid #243048;padding-top:10px;">'
                f'Generated by GPT-4o interpreting {n_sims:,} cross-regional simulations &middot; Not financial advice'
                f'</div></div>',
                unsafe_allow_html=True)

# ── TAB 4: Affordability & Costs ─────────────────────────────────────────
with tab_afford:
    st.markdown("<div style='color:#8899aa;font-size:13px;margin-bottom:20px;'>Mortgage approval, stress test, and full relocation cost breakdown.</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:Playfair Display,serif;font-size:20px;color:#fff;margin-bottom:16px;'>Affordability & Relocation Costs</div>", unsafe_allow_html=True)

    af_col1, af_col2 = st.columns(2)
    with af_col1:
        af_region = st.selectbox("Target Region", list(REGIONS.keys()),
                                  index=list(REGIONS.keys()).index(top_region), key="af_region")
    with af_col2:
        af_savings = st.number_input("Current Savings (£)", 0, 500000, 20000, 1000, key="af_savings")

    af = compute_affordability((profile.get("salary") or 50000), (profile.get("partner_salary") or 0),
                                af_region, deposit_pct, af_savings)

    # Lender approval metrics
    st.divider()
    af1, af2, af3, af4 = st.columns(4)
    af1.metric("Max Borrowing (4.5x)", f"£{af['max_borrowing']:,}",
               "Approved" if af["can_borrow"] else "Insufficient",
               delta_color="normal" if af["can_borrow"] else "inverse")
    af2.metric("Loan Needed", f"£{af['loan_needed']:,}",
               f"{'within' if af['can_borrow'] else 'exceeds'} limit")
    af3.metric("Total Upfront", f"£{af['total_upfront']:,}")
    af4.metric("Savings Shortfall", f"£{af['shortfall']:,}",
               f"{af['months_to_save']} months to save" if af['shortfall'] > 0 else "Ready",
               delta_color="inverse" if af['shortfall'] > 0 else "normal")

    # Stress test chart
    st.divider()
    st.markdown("<div style='font-family:Playfair Display,serif;font-size:18px;color:#fff;margin-bottom:8px;'>Mortgage Stress Test</div>", unsafe_allow_html=True)
    st.caption("Monthly payment at various interest rates. Red line = 35% of net income (lender danger zone).")
    fig_stress = go.Figure()
    colors = [C["green"] if p < af["danger_line"] else C["red"] for p in af["stress_payments"]]
    fig_stress.add_trace(go.Bar(
        x=[f"{r}%" for r in af["stress_rates"]], y=af["stress_payments"],
        marker_color=colors,
        text=[f"£{p:,}" for p in af["stress_payments"]], textposition="auto",
    ))
    fig_stress.add_hline(y=af["danger_line"], line_dash="dash", line_color=C["red"],
                          annotation_text=f"35% limit: £{af['danger_line']:,}",
                          annotation_font_color=C["red"])
    fig_stress.update_layout(**PLOT_THEME, height=350, showlegend=False,
                              xaxis_title="Mortgage Rate", yaxis_title="Monthly Payment (£)",
                              yaxis_tickprefix="£", yaxis_tickformat=",")
    st.plotly_chart(fig_stress, use_container_width=True)

    # Deposit savings timeline (only if shortfall)
    if af["shortfall"] > 0:
        st.divider()
        st.markdown("<div style='font-family:Playfair Display,serif;font-size:18px;color:#fff;margin-bottom:8px;'>Deposit Savings Timeline</div>", unsafe_allow_html=True)
        months_arr = list(range(af["months_to_save"] + 1))
        savings_arr = [af_savings + af["est_monthly_save"] * m for m in months_arr]
        fig_save = go.Figure()
        fig_save.add_trace(go.Scatter(x=months_arr, y=savings_arr, mode="lines",
                                       line=dict(color=C["green"], width=3), name="Savings"))
        fig_save.add_hline(y=af["total_upfront"], line_dash="dash", line_color=C["gold"],
                            annotation_text=f"Target: £{af['total_upfront']:,}",
                            annotation_font_color=C["gold"])
        fig_save.update_layout(**PLOT_THEME, height=300, showlegend=False,
                                xaxis_title="Months", yaxis_title="Savings (£)",
                                yaxis_tickprefix="£", yaxis_tickformat=",")
        st.plotly_chart(fig_save, use_container_width=True)
        st.markdown(f"""<div style="background:linear-gradient(135deg,#1a2235,#243048);border-left:4px solid {C['gold']};
            border-radius:12px;padding:18px 24px;">
            <div style="color:#c9a84c;font-family:'Playfair Display',serif;font-size:16px;font-weight:700;">
                Save ~£{af['est_monthly_save']:,}/month to be ready in {af['months_to_save']} months</div>
            <div style="color:#8899aa;font-size:13px;margin-top:4px;">Based on 30% of your estimated disposable income.</div>
        </div>""", unsafe_allow_html=True)

    # Relocation costs breakdown
    st.divider()
    st.markdown("<div style='font-family:Playfair Display,serif;font-size:18px;color:#fff;margin-bottom:8px;'>Total Relocation Costs</div>", unsafe_allow_html=True)
    mv_price = REGIONS[af_region]["avg_price"]
    mv_deposit = mv_price * deposit_pct / 100
    mv_stamp = compute_stamp_duty(mv_price, True)
    costs = {
        "Deposit": mv_deposit, "Stamp Duty": mv_stamp, "Solicitor": 1500,
        "Survey": 500, "Mortgage Fee": 999, "Removal": 1200,
        "Furniture": 2000, "EPC/Searches": 300,
    }
    total_cost = sum(costs.values())
    st.metric("Total Relocation Cost", f"£{total_cost:,.0f}")

    fig_costs = go.Figure(go.Bar(
        y=list(costs.keys()), x=list(costs.values()), orientation="h",
        marker_color=[C["gold"], C["red"], C["blue"], C["purple"], C["orange"],
                      C["green"], C["cyan"], C["muted"]],
        text=[f"£{v:,.0f}" for v in costs.values()], textposition="auto",
    ))
    fig_costs.update_layout(**PLOT_THEME, height=340, showlegend=False,
                             xaxis_title="Cost (£)", xaxis_tickprefix="£", xaxis_tickformat=",")
    st.plotly_chart(fig_costs, use_container_width=True)

# ── TAB 5: Neighbourhood Finder ──────────────────────────────────────────
with tab_areas:
    st.markdown("<div style='color:#8899aa;font-size:13px;margin-bottom:20px;'>Drill down from regions to specific neighbourhoods. AI recommends real areas based on your priorities, budget, and lifestyle.</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:Playfair Display,serif;font-size:20px;color:#fff;margin-bottom:16px;'>Neighbourhood Finder</div>", unsafe_allow_html=True)

    area_col1, area_col2 = st.columns([1, 1])
    with area_col1:
        area_region = st.selectbox(
            "Select Region to Explore",
            [r["region"] for r in rankings],
            index=0, key="area_region",
            help="Regions are sorted by your ranking — top pick is pre-selected"
        )
    with area_col2:
        area_budget = st.number_input(
            "Target Budget (£)", 50000, 2000000,
            value=int(profile.get("budget") or REGIONS[area_region]["avg_price"]),
            step=10000, key="area_budget"
        )

    area_extras = st.text_input(
        "Any specific requirements?",
        placeholder="e.g. within 20 min of Manchester centre, near outstanding primary schools, quiet village feel...",
        key="area_extras"
    )

    if st.button("Find Neighbourhoods", key="find_areas_btn", type="primary"):
        with st.spinner("AI is researching specific areas..."):
            try:
                search_profile = {**profile}
                if area_extras:
                    existing_notes = search_profile.get("notes", "") or ""
                    search_profile["notes"] = f"{existing_notes} {area_extras}".strip()

                areas_result = find_neighbourhoods(
                    area_region, search_profile, area_budget, live, OPENAI_KEY
                )
                # Validate and sanitize LLM output
                for a in areas_result.get("neighbourhoods", []):
                    a.setdefault("name", "Unknown Area")
                    a.setdefault("postcode_area", "")
                    a.setdefault("type", "area")
                    a.setdefault("avg_property_price", 0)
                    a.setdefault("price_range", "N/A")
                    a.setdefault("school_rating", "N/A")
                    a.setdefault("notable_schools", [])
                    a.setdefault("transport", "N/A")
                    a.setdefault("commute_to_centre", "N/A")
                    a.setdefault("match_score", 50)
                    a.setdefault("description", "")
                    a.setdefault("pros", [])
                    a.setdefault("cons", [])
                    for dim in ["green_space_score", "safety_score", "family_score", "culture_score"]:
                        a[dim] = max(1, min(10, int(a.get(dim, 5) or 5)))
                    # Sanity check: flag if price is wildly off budget
                    if a["avg_property_price"] and a["avg_property_price"] > area_budget * 2:
                        a["cons"] = a["cons"] + ["Significantly above budget"]
                st.session_state.area_results = areas_result
                st.session_state.area_search_region = area_region
            except Exception as e:
                st.error(f"Could not find neighbourhoods: {str(e)}")

    if st.session_state.get("area_results"):
        result = st.session_state.area_results
        search_region = st.session_state.get("area_search_region", "")

        if result.get("region_summary"):
            st.markdown(
                f'<div style="background:linear-gradient(135deg,#111827,#1a2235);border:1px solid #c9a84c44;'
                f'border-left:4px solid #c9a84c;border-radius:12px;padding:16px 20px;margin-bottom:20px;">'
                f'<div style="color:#c9a84c;font-size:11px;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:4px;">'
                f'{search_region} Overview</div>'
                f'<div style="color:#f5f0e8;font-size:14px;">{result["region_summary"]}</div>'
                f'</div>',
                unsafe_allow_html=True)

        neighbourhoods = result.get("neighbourhoods", [])
        if neighbourhoods:
            # Match score overview bar chart
            st.markdown("<div style='font-family:Playfair Display,serif;font-size:18px;color:#fff;margin-bottom:8px;'>Match Scores</div>", unsafe_allow_html=True)
            sorted_areas = sorted(neighbourhoods, key=lambda x: x.get("match_score", 0), reverse=True)

            fig_match = go.Figure()
            fig_match.add_trace(go.Bar(
                y=[a["name"] for a in reversed(sorted_areas)],
                x=[a.get("match_score", 0) for a in reversed(sorted_areas)],
                orientation="h",
                marker_color=[C["gold"] if i == len(sorted_areas) - 1 else C["blue"]
                              for i in range(len(sorted_areas))],
                text=[f"{a.get('match_score', 0)}%" for a in reversed(sorted_areas)],
                textposition="auto",
            ))
            fig_match.update_layout(**PLOT_THEME, height=280, showlegend=False,
                                     xaxis_title="Match Score (0-100)", xaxis_range=[0, 100])
            st.plotly_chart(fig_match, use_container_width=True)

            # Radar chart comparing areas
            st.divider()
            st.markdown("<div style='font-family:Playfair Display,serif;font-size:18px;color:#fff;margin-bottom:8px;'>Area Comparison Radar</div>", unsafe_allow_html=True)
            radar_dims = ["green_space_score", "safety_score", "family_score", "culture_score"]
            radar_labels = ["Green Space", "Safety", "Family", "Culture"]
            area_colors = [C["gold"], C["blue"], C["green"], C["purple"], C["cyan"]]

            fig_radar = go.Figure()
            for idx, area in enumerate(sorted_areas[:5]):
                vals = [area.get(d, 5) for d in radar_dims]
                vals.append(vals[0])
                col = area_colors[idx % len(area_colors)]
                fig_radar.add_trace(go.Scatterpolar(
                    r=vals, theta=radar_labels + [radar_labels[0]],
                    name=area.get("name", "Area"), fill="toself",
                    line_color=col,
                    fillcolor=hex_to_rgba(col),
                ))
            fig_radar.update_layout(**PLOT_THEME, height=400,
                                     polar=dict(bgcolor="rgba(0,0,0,0)",
                                                radialaxis=dict(visible=True, range=[0, 10],
                                                                gridcolor="#243048", tickfont=dict(color="#8899aa")),
                                                angularaxis=dict(gridcolor="#243048", tickfont=dict(color="#8899aa", size=12))))
            st.plotly_chart(fig_radar, use_container_width=True)

            # Price comparison
            st.divider()
            st.markdown("<div style='font-family:Playfair Display,serif;font-size:18px;color:#fff;margin-bottom:8px;'>Price Comparison</div>", unsafe_allow_html=True)
            fig_price = go.Figure()
            fig_price.add_trace(go.Bar(
                x=[a["name"] for a in sorted_areas],
                y=[a.get("avg_property_price", 0) for a in sorted_areas],
                marker_color=[area_colors[i % len(area_colors)] for i in range(len(sorted_areas))],
                text=[f"£{a.get('avg_property_price', 0):,}" for a in sorted_areas],
                textposition="auto",
            ))
            fig_price.add_hline(y=area_budget, line_dash="dash", line_color=C["gold"],
                                annotation_text=f"Your Budget: £{area_budget:,}",
                                annotation_font_color=C["gold"])
            fig_price.update_layout(**PLOT_THEME, height=350, showlegend=False,
                                     yaxis_title="Avg Property Price (£)", yaxis_tickprefix="£",
                                     yaxis_tickformat=",")
            st.plotly_chart(fig_price, use_container_width=True)

            # Detailed area cards
            st.divider()
            st.markdown("<div style='font-family:Playfair Display,serif;font-size:18px;color:#fff;margin-bottom:16px;'>Detailed Area Profiles</div>", unsafe_allow_html=True)

            for idx, area in enumerate(sorted_areas):
                is_top = idx == 0
                border_col = "#c9a84c" if is_top else "#243048"
                top_border = "border-left:4px solid #c9a84c;" if is_top else ""
                score_bg = "#c9a84c" if is_top else "#4a90d9"
                badge = '<span style="background:#c9a84c;color:#0a0e1a;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600;margin-left:8px;">TOP PICK</span>' if is_top else ""

                notable = area.get("notable_schools", [])
                schools_html = "<br>".join(f"• {s}" for s in notable[:3]) if notable else ""

                pros_html = "".join(
                    f'<span style="background:#2dd4a022;color:#2dd4a0;padding:3px 8px;border-radius:6px;font-size:11px;margin:2px 4px 2px 0;display:inline-block;">&#10003; {p}</span>'
                    for p in area.get("pros", [])
                )
                cons_html = "".join(
                    f'<span style="background:#f4726822;color:#f47268;padding:3px 8px;border-radius:6px;font-size:11px;margin:2px 4px 2px 0;display:inline-block;">&#10007; {c}</span>'
                    for c in area.get("cons", [])
                )

                a_name = area.get("name", "Unknown")
                a_postcode = area.get("postcode_area", "")
                a_type = area.get("type", "").replace("_", " ").title()
                a_score = area.get("match_score", 0)
                a_desc = area.get("description", "")
                a_price = area.get("avg_property_price", 0) or 0
                a_range = area.get("price_range", "")
                a_school = area.get("school_rating", "N/A")
                a_transport = area.get("transport", "N/A")
                a_commute = area.get("commute_to_centre", "N/A")

                card_html = (
                    f'<div style="background:linear-gradient(135deg,#111827,#1a2235);border:1px solid {border_col};'
                    f'border-radius:12px;padding:20px 24px;margin-bottom:16px;{top_border}">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">'
                    f'<div>'
                    f'<span style="font-family:Georgia,serif;font-size:18px;color:#fff;font-weight:600;">{a_name}</span>'
                    f'{badge}'
                    f'<span style="color:#8899aa;font-size:12px;margin-left:8px;">{a_postcode} &middot; {a_type}</span>'
                    f'</div>'
                    f'<div style="background:{score_bg};color:#0a0e1a;padding:6px 14px;border-radius:8px;font-weight:700;font-size:16px;">'
                    f'{a_score}%</div>'
                    f'</div>'
                    f'<div style="color:#b0c0d0;font-size:13px;margin-bottom:12px;">{a_desc}</div>'
                    f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:12px;">'
                    f'<div><div style="color:#8899aa;font-size:10px;text-transform:uppercase;">Avg Price</div>'
                    f'<div style="color:#c9a84c;font-size:16px;font-weight:700;">&#163;{a_price:,}</div>'
                    f'<div style="color:#8899aa;font-size:11px;">{a_range}</div></div>'
                    f'<div><div style="color:#8899aa;font-size:10px;text-transform:uppercase;">Schools</div>'
                    f'<div style="color:#f5f0e8;font-size:14px;font-weight:600;">{a_school}</div>'
                    f'<div style="color:#8899aa;font-size:11px;">{schools_html}</div></div>'
                    f'<div><div style="color:#8899aa;font-size:10px;text-transform:uppercase;">Transport</div>'
                    f'<div style="color:#f5f0e8;font-size:12px;">{a_transport}</div></div>'
                    f'<div><div style="color:#8899aa;font-size:10px;text-transform:uppercase;">Commute to Centre</div>'
                    f'<div style="color:#f5f0e8;font-size:14px;font-weight:600;">{a_commute}</div></div>'
                    f'</div>'
                    f'<div style="margin-bottom:8px;">{pros_html}</div>'
                    f'<div>{cons_html}</div>'
                    f'</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)

            # Summary table
            st.divider()
            st.markdown("<div style='font-family:Playfair Display,serif;font-size:18px;color:#fff;margin-bottom:8px;'>Summary Table</div>", unsafe_allow_html=True)
            df_areas = pd.DataFrame([{
                "Area": a["name"],
                "Postcode": a.get("postcode_area", ""),
                "Avg Price": f"£{a.get('avg_property_price', 0):,}",
                "Schools": a.get("school_rating", "N/A"),
                "Green Space": f"{a.get('green_space_score', 0)}/10",
                "Safety": f"{a.get('safety_score', 0)}/10",
                "Family": f"{a.get('family_score', 0)}/10",
                "Culture": f"{a.get('culture_score', 0)}/10",
                "Match": f"{a.get('match_score', 0)}%",
            } for a in sorted_areas])
            st.dataframe(df_areas, use_container_width=True, hide_index=True)
        else:
            st.warning("No neighbourhoods returned. Try a different region or adjust your budget.")

# ── TAB 6: AI Advisor (Tool Use) ─────────────────────────────────────────
with tab_advisor:
    st.markdown("<div style='color:#8899aa;font-size:13px;margin-bottom:20px;'>Ask anything about relocation. The advisor can compute scenarios, compare regions, and run simulations on demand.</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:Playfair Display,serif;font-size:20px;color:#fff;margin-bottom:4px;'>AI Relocation Advisor</div>", unsafe_allow_html=True)
    st.markdown("""<div style='color:#8899aa;font-size:14px;margin-bottom:16px;'>Try:
        <em style='color:#c9a84c;'>"Compare Yorkshire vs North West"</em> ·
        <em style='color:#c9a84c;'>"Can I afford London on £80k?"</em> ·
        <em style='color:#c9a84c;'>"What's the best region for families?"</em> ·
        <em style='color:#c9a84c;'>"Run Monte Carlo for Scotland"</em> ·
        <em style='color:#c9a84c;'>"Find neighbourhoods in Yorkshire near good schools"</em>
    </div>""", unsafe_allow_html=True)

    ADVISOR_TOOLS = [
        {"type": "function", "function": {
            "name": "compare_regions",
            "description": "Compare two UK regions with detailed financial and QoL breakdown.",
            "parameters": {"type": "object", "properties": {
                "region1": {"type": "string"}, "region2": {"type": "string"},
            }, "required": ["region1", "region2"]}
        }},
        {"type": "function", "function": {
            "name": "run_scenario",
            "description": "Run financial analysis for a specific region with custom salary/budget.",
            "parameters": {"type": "object", "properties": {
                "region": {"type": "string"},
                "salary": {"type": "number", "description": "Annual salary (GBP)"},
                "partner_salary": {"type": "number"},
            }, "required": ["region"]}
        }},
        {"type": "function", "function": {
            "name": "find_best_region",
            "description": "Find the best region for a specific priority.",
            "parameters": {"type": "object", "properties": {
                "priority": {"type": "string", "description": "One of: affordability, green_space, schools, safety, culture, healthcare, disposable_income, overall"},
            }, "required": ["priority"]}
        }},
        {"type": "function", "function": {
            "name": "run_monte_carlo_tool",
            "description": "Run Monte Carlo simulation for specific regions.",
            "parameters": {"type": "object", "properties": {
                "regions": {"type": "string", "description": "Comma-separated region names"},
                "n_simulations": {"type": "integer"},
            }, "required": ["regions"]}
        }},
        {"type": "function", "function": {
            "name": "check_affordability",
            "description": "Check mortgage affordability for a region including max borrowing, stress test, and deposit timeline.",
            "parameters": {"type": "object", "properties": {
                "region": {"type": "string"},
                "current_savings": {"type": "integer", "description": "Current savings in GBP. Default 20000."},
            }, "required": ["region"]}
        }},
        {"type": "function", "function": {
            "name": "estimate_moving_costs",
            "description": "Estimate total relocation costs for a specific region including deposit, stamp duty, solicitor, survey, removal.",
            "parameters": {"type": "object", "properties": {
                "region": {"type": "string"},
            }, "required": ["region"]}
        }},
        {"type": "function", "function": {
            "name": "find_neighbourhoods_tool",
            "description": "Find specific neighbourhoods/towns within a UK region that match the user's priorities. Returns 5 real areas with prices, school ratings, transport links, and match scores.",
            "parameters": {"type": "object", "properties": {
                "region": {"type": "string", "description": "UK region to search in"},
                "requirements": {"type": "string", "description": "Any specific requirements like 'near good schools', 'village feel', 'within 20 min of city centre'"},
            }, "required": ["region"]}
        }},
    ]

    def execute_advisor_tool(name, arguments_json):
        args = json.loads(arguments_json) if arguments_json else {}
        if name == "compare_regions":
            r1, r2 = args.get("region1", "London"), args.get("region2", "Yorkshire")
            results = []
            for rname in [r1, r2]:
                if rname not in REGIONS:
                    return f"Region '{rname}' not found. Available: {', '.join(REGIONS.keys())}"
                s = compute_regional_score(rname, profile, financial_weight, deposit_pct)
                b = compute_monthly_budget((profile.get("salary") or 50000), (profile.get("partner_salary") or 0),
                                            rname, deposit_pct, live["rate_5yr_current"])
                r = REGIONS[rname]
                results.append(f"{rname}: Score={s['composite']}, Financial={s['financial_score']}, QoL={s['qol_score']}, "
                              f"Price=£{r['avg_price']:,}, Mortgage=£{b['monthly_mortgage']:,}/mo, "
                              f"Disposable=£{b['disposable_buy']:,}/mo, Affordability={s['affordability_ratio']}x")
            return "Region comparison:\n" + "\n".join(results)

        elif name == "run_scenario":
            rname = args.get("region", "London")
            if rname not in REGIONS:
                return f"Region '{rname}' not found."
            sal = args.get("salary", (profile.get("salary") or 50000))
            psal = args.get("partner_salary", (profile.get("partner_salary") or 0))
            custom_profile = {**profile, "salary": sal, "partner_salary": psal}
            s = compute_regional_score(rname, custom_profile, financial_weight, deposit_pct)
            b = compute_monthly_budget(sal, psal, rname, deposit_pct, live["rate_5yr_current"])
            return (f"{rname} scenario (Salary: £{sal:,}):\n"
                    f"Score: {s['composite']}, Affordability: {s['affordability_ratio']}x\n"
                    f"Mortgage: £{b['monthly_mortgage']:,}/mo, Rent: £{b['monthly_rent']:,}/mo\n"
                    f"Disposable (buy): £{b['disposable_buy']:,}/mo, (rent): £{b['disposable_rent']:,}/mo")

        elif name == "find_best_region":
            priority = args.get("priority", "overall")
            if priority == "overall":
                return f"Best overall: {rankings[0]['region']} (score {rankings[0]['composite']})"
            elif priority == "affordability":
                best = min(rankings, key=lambda x: x["affordability_ratio"])
                return f"Most affordable: {best['region']} ({best['affordability_ratio']}x income)"
            elif priority == "disposable_income":
                best = max(rankings, key=lambda x: x["disposable_monthly"])
                return f"Best disposable income: {best['region']} (£{best['disposable_monthly']:,}/mo)"
            elif priority in QOL_DIMS:
                best_r = max(REGIONS.items(), key=lambda x: x[1].get(priority, 0))
                return f"Best for {priority.replace('_', ' ')}: {best_r[0]} (score: {best_r[1][priority]})"
            return f"Unknown priority: {priority}"

        elif name == "run_monte_carlo_tool":
            regs = [r.strip() for r in args.get("regions", "London,Yorkshire").split(",")]
            regs = [r for r in regs if r in REGIONS]
            if len(regs) < 2:
                return "Need at least 2 valid regions."
            n = min(2000, max(100, args.get("n_simulations", 500)))
            mc = run_regional_monte_carlo(regs, profile, n, horizon, deposit_pct=deposit_pct)
            lines = [f"Monte Carlo ({n} sims, {horizon}yr):"]
            for rname in sorted(regs, key=lambda r: mc[r]["prob_best"], reverse=True):
                m = mc[rname]
                lines.append(f"- {rname}: P(Wins)={m['prob_best']*100:.0f}%, Median=£{m['p50']:,.0f}, "
                           f"P10=£{m['p10']:,.0f}, P90=£{m['p90']:,.0f}")
            return "\n".join(lines)

        elif name == "check_affordability":
            rname = args.get("region", top_region)
            if rname not in REGIONS:
                return f"Region '{rname}' not found."
            sav = args.get("current_savings", 20000)
            af = compute_affordability((profile.get("salary") or 50000), (profile.get("partner_salary") or 0),
                                        rname, deposit_pct, sav)
            return (f"Affordability for {rname}:\n"
                    f"- Max borrowing (4.5x): £{af['max_borrowing']:,} — {'Approved' if af['can_borrow'] else 'EXCEEDS LIMIT'}\n"
                    f"- Loan needed: £{af['loan_needed']:,}\n"
                    f"- Total upfront: £{af['total_upfront']:,} (deposit £{af['deposit']:,} + stamp £{af['stamp']:,} + fees)\n"
                    f"- Savings shortfall: £{af['shortfall']:,}\n"
                    f"- Months to save: {af['months_to_save']}\n"
                    f"- Danger rate (35% of income): mortgage > £{af['danger_line']:,}/mo")

        elif name == "estimate_moving_costs":
            rname = args.get("region", top_region)
            if rname not in REGIONS:
                return f"Region '{rname}' not found."
            p = REGIONS[rname]["avg_price"]
            dep = p * deposit_pct / 100
            stamp = compute_stamp_duty(p, True)
            total = dep + stamp + 1500 + 500 + 999 + 1200 + 2000 + 300 + 1200
            return (f"Estimated moving costs to {rname} (price £{p:,}):\n"
                    f"- Deposit ({deposit_pct}%): £{dep:,.0f}\n"
                    f"- Stamp duty: £{stamp:,}\n"
                    f"- Solicitor: ~£1,500 | Survey: ~£500 | Mortgage fee: ~£999\n"
                    f"- Removal: ~£1,200 | Furniture: ~£2,000 | EPC: ~£300\n"
                    f"- Overlap rent (1 month): ~£1,200\n"
                    f"- TOTAL: ~£{total:,.0f}")

        elif name == "find_neighbourhoods_tool":
            rname = args.get("region", top_region)
            if rname not in REGIONS:
                return f"Region '{rname}' not found. Available: {', '.join(REGIONS.keys())}"
            reqs = args.get("requirements", "")
            search_p = {**profile}
            if reqs:
                search_p["notes"] = reqs
            budget = int(profile.get("budget") or REGIONS[rname]["avg_price"])
            try:
                result = find_neighbourhoods(rname, search_p, budget, live, OPENAI_KEY)
                areas = result.get("neighbourhoods", [])
                lines = [f"Top neighbourhoods in {rname}:"]
                for a in areas:
                    lines.append(f"\n**{a['name']}** ({a.get('postcode_area', '')}) — Match: {a.get('match_score', 0)}%")
                    lines.append(f"  Price: £{a.get('avg_property_price', 0):,} ({a.get('price_range', '')})")
                    lines.append(f"  Schools: {a.get('school_rating', 'N/A')}")
                    lines.append(f"  Transport: {a.get('transport', 'N/A')}")
                    lines.append(f"  {a.get('description', '')}")
                return "\n".join(lines)
            except Exception as e:
                return f"Error finding neighbourhoods: {str(e)}"

        return f"Unknown tool: {name}"

    system_ctx = f"""You are HomeIQ's Smart Relocation Advisor — an expert on UK regions, property, and personal finance.
You have the user's profile and live market data. Use tools for numerical questions — do NOT guess numbers.

USER PROFILE: Salary £{(profile.get('salary') or 50000):,}, Partner £{(profile.get('partner_salary') or 0):,},
{profile.get('job_type') or 'remote'} worker, Priorities: {', '.join(profile.get('priorities') or [])},
Horizon: {horizon}yr, Deposit: {deposit_pct}%

TOP RANKED REGIONS:
{chr(10).join(f"- {r['region']}: Score {r['composite']}, Financial {r['financial_score']}, QoL {r['qol_score']}" for r in rankings[:5])}

LIVE MARKET: BoE rate {live['base_rate_current']}%, 5yr fixed {live['rate_5yr_current']}%, CPI {live['cpi_current']}%

Available tools: compare_regions, run_scenario, find_best_region, run_monte_carlo_tool, find_neighbourhoods_tool
Use find_neighbourhoods_tool when the user asks about specific areas, towns, or neighbourhoods within a region."""

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        if message["role"] in ("user", "assistant"):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if user_input := st.chat_input("Ask your relocation advisor..."):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    client = openai.OpenAI(api_key=OPENAI_KEY)
                    messages = [{"role": "system", "content": system_ctx}] + [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.chat_history if m["role"] in ("user", "assistant")
                    ]
                    response = client.chat.completions.create(
                        model="gpt-4o", messages=messages, tools=ADVISOR_TOOLS,
                        tool_choice="auto", max_tokens=800,
                    )
                    iterations = 0
                    while response.choices[0].message.tool_calls and iterations < 3:
                        tool_calls = response.choices[0].message.tool_calls
                        messages.append(response.choices[0].message)
                        for tc in tool_calls:
                            st.info(f"Computing: {tc.function.name}...")
                            result = execute_advisor_tool(tc.function.name, tc.function.arguments)
                            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
                        response = client.chat.completions.create(
                            model="gpt-4o", messages=messages, tools=ADVISOR_TOOLS,
                            tool_choice="auto", max_tokens=800,
                        )
                        iterations += 1
                    reply = response.choices[0].message.content or "Analysis complete — see the results above."
                except Exception as e:
                    reply = f"Sorry, I encountered an error: {str(e)}"
            st.markdown(reply)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})

    if st.session_state.chat_history:
        if st.button("Clear conversation", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:32px 0 16px;color:#243048;font-size:12px;">
    HomeIQ · Smart Relocation Advisor · Live data: Bank of England IADB & ONS API · Not financial advice
</div>
""", unsafe_allow_html=True)
