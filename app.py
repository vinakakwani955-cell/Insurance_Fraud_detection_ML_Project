import streamlit as st
import pandas as pd
import joblib

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="ClaimGuard | Insurance Fraud Detection",
    page_icon="🛡️",
    layout="wide"
)


def html(markup: str):
    """Render HTML flush-left so Markdown never treats indentation as a code block."""
    st.markdown("".join(line.strip() for line in markup.strip().splitlines()),
                unsafe_allow_html=True)


# --------------------------------------------------
# Global Styling  (dark purple theme)
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg:        #0F0A1F;
    --surface:   #171030;
    --surface-2: #1E1640;
    --border:    #2E2352;
    --border-2:  #3B2E68;
    --text:      #EDE9FE;
    --muted:     #A79BCB;
    --dim:       #7C70A3;
    --primary:   #8B5CF6;
    --primary-2: #A78BFA;
    --primary-d: #6D28D9;
    --ok:        #34D399;
    --warn:      #FBBF24;
    --bad:       #F87171;
}

html, body, [class*="css"], .stApp {
    font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif;
}

.stApp, [data-testid="stAppViewContainer"] {
    background:
        radial-gradient(900px 420px at 85% -8%, rgba(139,92,246,0.20), transparent 60%),
        radial-gradient(700px 380px at -5% 0%, rgba(109,40,217,0.14), transparent 55%),
        var(--bg);
    color: var(--text);
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.block-container, [data-testid="stMainBlockContainer"] {
    padding-top: 1.4rem !important;
    padding-bottom: 2rem !important;
    max-width: 1280px;
}

/* ---------------- Top bar ---------------- */
.cg-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    flex-wrap: wrap;
    padding: 0.2rem 0 1.1rem 0;
    margin-bottom: 1.2rem;
    border-bottom: 1px solid var(--border);
}
.cg-brand { display: flex; align-items: center; gap: 0.75rem; }
.cg-logo {
    width: 38px; height: 38px;
    border-radius: 10px;
    background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
    display: grid; place-items: center;
    box-shadow: 0 6px 18px rgba(124,58,237,0.45);
}
.cg-logo svg { width: 20px; height: 20px; }
.cg-brand-name { color: var(--text); font-size: 1.05rem; font-weight: 700; letter-spacing: -0.01em; line-height: 1.1; }
.cg-brand-tag  { color: var(--dim); font-size: 0.72rem; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; margin-top: 2px; }
.cg-badges { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.cg-badge {
    display: inline-flex; align-items: center; gap: 0.45rem;
    padding: 0.32rem 0.75rem;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: rgba(30,22,64,0.7);
    color: var(--muted);
    font-size: 0.75rem; font-weight: 500;
}
.cg-badge-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--ok); box-shadow: 0 0 0 3px rgba(52,211,153,0.18); }

/* ---------------- Hero ---------------- */
.cg-hero {
    background: linear-gradient(135deg, rgba(109,40,217,0.28) 0%, rgba(23,16,48,0.95) 55%);
    border: 1px solid var(--border-2);
    border-radius: 16px;
    padding: 1.9rem 2.1rem 1.6rem 2.1rem;
    margin-bottom: 1.6rem;
}
.cg-eyebrow {
    color: var(--primary-2);
    font-size: 0.72rem; font-weight: 600;
    letter-spacing: 0.14em; text-transform: uppercase;
    margin-bottom: 0.55rem;
}
.cg-hero-title {
    color: #F5F3FF;
    font-size: 2rem; font-weight: 700;
    letter-spacing: -0.02em;
    margin: 0 0 0.5rem 0; line-height: 1.15;
}
.cg-hero-sub {
    color: var(--muted);
    font-size: 0.97rem; max-width: 680px; line-height: 1.6;
    margin-bottom: 1.4rem;
}
.cg-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 0.8rem; }
.cg-stat {
    background: rgba(15,10,31,0.55);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.85rem 1rem;
}
.cg-stat-num { color: var(--text); font-size: 1.05rem; font-weight: 650; letter-spacing: -0.01em; }
.cg-stat-label { color: var(--dim); font-size: 0.75rem; margin-top: 0.15rem; }

/* ---------------- Section headers ---------------- */
.cg-section { display: flex; align-items: center; gap: 0.8rem; margin: 0.2rem 0 1rem 0; }
.cg-step {
    width: 28px; height: 28px; flex-shrink: 0;
    border-radius: 8px;
    background: rgba(139,92,246,0.16);
    border: 1px solid rgba(139,92,246,0.45);
    color: var(--primary-2);
    font-size: 0.8rem; font-weight: 700;
    display: grid; place-items: center;
}
.cg-section-title { color: var(--text); font-size: 0.98rem; font-weight: 600; line-height: 1.2; }
.cg-section-sub { color: var(--dim); font-size: 0.78rem; margin-top: 2px; }
.cg-divider { height: 1px; background: var(--border); margin: 1.3rem 0 1.3rem 0; }

/* ---------------- Form container ---------------- */
div[data-testid="stForm"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.6rem 1.7rem 1.4rem 1.7rem;
}

/* Labels */
[data-testid="stWidgetLabel"] p, label {
    color: var(--muted) !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
}

/* Inputs */
div[data-baseweb="select"] > div,
div[data-baseweb="input"],
div[data-baseweb="base-input"] {
    background-color: var(--bg) !important;
    border-color: var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    transition: border-color .15s ease, box-shadow .15s ease;
}
div[data-baseweb="input"] input { color: var(--text) !important; font-weight: 500; }
div[data-baseweb="select"] > div:hover,
div[data-baseweb="input"]:hover { border-color: var(--border-2) !important; }
div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="input"]:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.25);
}
.stNumberInput button {
    background-color: var(--surface-2) !important;
    color: var(--muted) !important;
    border-color: var(--border) !important;
}
.stNumberInput button:hover { color: #fff !important; background-color: var(--primary-d) !important; }

/* Submit button */
div[data-testid="stFormSubmitButton"] { margin-top: 0.4rem; }
div[data-testid="stFormSubmitButton"] button {
    width: 100%;
    background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 0 !important;
    letter-spacing: 0.01em;
    box-shadow: 0 8px 22px rgba(124,58,237,0.38);
    transition: transform .12s ease, box-shadow .12s ease, filter .12s ease;
}
div[data-testid="stFormSubmitButton"] button:hover {
    filter: brightness(1.1);
    transform: translateY(-1px);
    box-shadow: 0 12px 26px rgba(124,58,237,0.5);
}
div[data-testid="stFormSubmitButton"] button:active { transform: translateY(0); }

/* ---------------- Sticky result column ---------------- */
div[data-testid="stColumn"]:has(.cg-sticky),
div[data-testid="column"]:has(.cg-sticky) {
    position: sticky;
    top: 1.2rem;
    align-self: flex-start;
}

/* ---------------- Result panel ---------------- */
.cg-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.4rem 1.5rem 1.5rem 1.5rem;
}
.cg-panel-head {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 1.1rem;
}
.cg-panel-title { color: var(--text); font-size: 0.95rem; font-weight: 600; }
.cg-chip {
    font-size: 0.7rem; font-weight: 600;
    padding: 0.22rem 0.65rem; border-radius: 999px;
    letter-spacing: 0.04em; text-transform: uppercase;
}
.cg-chip-idle   { color: var(--dim); border: 1px solid var(--border); }
.cg-chip-fraud  { color: var(--bad); background: rgba(248,113,113,0.12); border: 1px solid rgba(248,113,113,0.4); }
.cg-chip-genuine{ color: var(--ok);  background: rgba(52,211,153,0.12);  border: 1px solid rgba(52,211,153,0.4); }

.cg-empty { text-align: center; padding: 1.6rem 0.4rem 1rem 0.4rem; }
.cg-empty-icon {
    width: 64px; height: 64px; margin: 0 auto 1rem auto;
    border-radius: 18px;
    background: rgba(139,92,246,0.12);
    border: 1px dashed rgba(139,92,246,0.5);
    display: grid; place-items: center;
}
.cg-empty-icon svg { width: 28px; height: 28px; }
.cg-empty-title { color: var(--text); font-size: 0.95rem; font-weight: 600; margin-bottom: 0.35rem; }
.cg-empty-text { color: var(--dim); font-size: 0.82rem; line-height: 1.55; }

.cg-gauge-wrap { display: flex; justify-content: center; margin: 0.4rem 0 1.1rem 0; }
.cg-gauge {
    --p: 0; --c: var(--primary);
    width: 176px; height: 176px; border-radius: 50%;
    background: conic-gradient(var(--c) calc(var(--p) * 1%), #2A1F4D 0);
    display: grid; place-items: center;
    box-shadow: 0 0 40px color-mix(in srgb, var(--c) 22%, transparent);
}
.cg-gauge-inner {
    width: 138px; height: 138px; border-radius: 50%;
    background: var(--surface);
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.cg-gauge-num { color: #F5F3FF; font-size: 2rem; font-weight: 700; letter-spacing: -0.02em; line-height: 1; }
.cg-gauge-lab { color: var(--dim); font-size: 0.6rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; margin-top: 0.4rem; text-align: center; line-height: 1.3; padding: 0 0.6rem; }

.cg-verdict-label { text-align: center; font-size: 1.25rem; font-weight: 700; letter-spacing: -0.01em; }
.cg-verdict-fraud   .cg-verdict-label { color: var(--bad); }
.cg-verdict-genuine .cg-verdict-label { color: var(--ok); }
.cg-verdict-note { text-align: center; color: var(--muted); font-size: 0.82rem; line-height: 1.55; margin: 0.4rem 0 1.2rem 0; }

/* Risk meter */
.cg-meter-label { display: flex; justify-content: space-between; color: var(--dim); font-size: 0.72rem; font-weight: 500; margin-bottom: 0.45rem; }
.cg-meter-track { position: relative; width: 100%; height: 8px; border-radius: 6px; background: #2A1F4D; overflow: hidden; }
.cg-meter-fill { height: 100%; border-radius: 6px; background: linear-gradient(90deg, #34D399 0%, #FBBF24 55%, #F87171 100%); }
.cg-meter-scale { position: relative; height: 14px; margin-top: 0.3rem; color: var(--dim); font-size: 0.66rem; }
.cg-meter-scale span { position: absolute; transform: translateX(-50%); }

/* Snapshot */
.cg-snap { display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem; margin-top: 1.1rem; padding-top: 1.1rem; border-top: 1px solid var(--border); }
.cg-snap-item { background: var(--bg); border: 1px solid var(--border); border-radius: 10px; padding: 0.6rem 0.75rem; }
.cg-snap-val { color: var(--text); font-size: 0.95rem; font-weight: 600; }
.cg-snap-lab { color: var(--dim); font-size: 0.68rem; margin-top: 0.1rem; }

/* Expander + table */
div[data-testid="stExpander"] {
    background: var(--surface);
    border: 1px solid var(--border) !important;
    border-radius: 14px;
    margin-top: 1.4rem;
}
div[data-testid="stExpander"] summary { color: var(--text); font-weight: 500; }
div[data-testid="stTable"] table { border-collapse: collapse; width: 100%; }
div[data-testid="stTable"] th, div[data-testid="stTable"] td {
    color: var(--text) !important;
    border-color: var(--border) !important;
    font-size: 0.85rem;
}
div[data-testid="stTable"] th { color: var(--muted) !important; font-weight: 500; }

/* Footer */
.cg-footer {
    color: var(--dim);
    font-size: 0.76rem; text-align: center;
    margin-top: 2.2rem; padding-top: 1.2rem;
    border-top: 1px solid var(--border);
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Load Trained Model
# --------------------------------------------------

@st.cache_resource
def load_model():
    return joblib.load("fraud_logistic_regression.pkl")


try:
    pipeline = load_model()
except Exception as e:
    st.error("Unable to load the trained model.")
    st.error(f"Error: {e}")
    st.stop()


# --------------------------------------------------
# Top Bar + Hero
# --------------------------------------------------

SHIELD_WHITE = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M12 3l8 3v6c0 4.5-3.2 8.2-8 9-4.8-.8-8-4.5-8-9V6l8-3z"/>'
    '<path d="M9 12l2 2 4-4"/></svg>'
)
SHIELD_PURPLE = SHIELD_WHITE.replace('#fff', '#A78BFA')

html(f"""
<div class="cg-nav">
    <div class="cg-brand">
        <div class="cg-logo">{SHIELD_WHITE}</div>
        <div>
            <div class="cg-brand-name">ClaimGuard</div>
            <div class="cg-brand-tag">Risk Analytics</div>
        </div>
    </div>
    <div class="cg-badges">
        <span class="cg-badge"><span class="cg-badge-dot"></span>Model loaded</span>
        <span class="cg-badge">Logistic Regression</span>
    </div>
</div>
""")

html("""
<div class="cg-hero">
    <div class="cg-eyebrow">ClaimGuard &middot; Risk Analytics</div>
    <div class="cg-hero-title">Insurance Fraud Detection</div>
    <div class="cg-hero-sub">Submit a vehicle insurance claim below and get an instant, model-backed fraud risk assessment &mdash; trained on historical claim outcomes rather than fixed rules.</div>
    <div class="cg-stats">
        <div class="cg-stat"><div class="cg-stat-num">9,530</div><div class="cg-stat-label">Claims used for training</div></div>
        <div class="cg-stat"><div class="cg-stat-num">Logistic Regression</div><div class="cg-stat-label">Balanced, GridSearch-tuned</div></div>
        <div class="cg-stat"><div class="cg-stat-num">5-fold CV</div><div class="cg-stat-label">Cross-validated</div></div>
    </div>
</div>
""")


# --------------------------------------------------
# Layout: form (left)  |  assessment panel (right)
# --------------------------------------------------

YES_NO = {"0": "No", "1": "Yes"}

form_col, result_col = st.columns([2.15, 1], gap="large")

# ---------------- Input Form ----------------
with form_col:
    with st.form("fraud_detection_form"):

        html("""
        <div class="cg-section">
            <div class="cg-step">1</div>
            <div><div class="cg-section-title">Claim Details</div>
            <div class="cg-section-sub">How, when, and where the claim was filed</div></div>
        </div>
        """)

        c1, c2, c3 = st.columns(3)
        with c1:
            gender = st.selectbox("Gender", ["M", "F"])
        with c2:
            marital_status = st.selectbox("Marital Status", ["0", "1"])
        with c3:
            property_status = st.selectbox("Property Status", ["Own", "Rent"])

        c4, c5, c6 = st.columns(3)
        with c4:
            claim_day_of_week = st.selectbox(
                "Claim Day", ["Monday", "Tuesday", "Wednesday", "Thursday",
                              "Friday", "Saturday", "Sunday"]
            )
        with c5:
            accident_site = st.selectbox("Accident Site", ["Local", "Parking Lot", "Highway"])
        with c6:
            witness_present = st.selectbox(
                "Witness Present", ["0", "1"], format_func=lambda v: YES_NO[v]
            )

        c7, c8, c9 = st.columns(3)
        with c7:
            channel = st.selectbox("Claim Channel", ["Broker", "Phone", "Online"])
        with c8:
            police_report = st.selectbox(
                "Police Report", ["0", "1"], format_func=lambda v: YES_NO[v]
            )
        with c9:
            vehicle_category = st.selectbox("Vehicle Category", ["Compact", "Medium", "Large"])

        c10, _c11, _c12 = st.columns(3)
        with c10:
            vehicle_color = st.selectbox(
                "Vehicle Color", ["red", "gray", "black", "white", "silver", "other", "blue"]
            )

        html('<div class="cg-divider"></div>')
        html("""
        <div class="cg-section">
            <div class="cg-step">2</div>
            <div><div class="cg-section-title">Driver &amp; Policy Profile</div>
            <div class="cg-section-sub">Who's filing, and their history with the insurer</div></div>
        </div>
        """)

        d1, d2, d3 = st.columns(3)
        with d1:
            age_of_driver = st.number_input("Driver Age", min_value=16, max_value=100, value=40)
        with d2:
            safety_rating = st.number_input("Safety Rating (0-100)", min_value=0, max_value=100, value=70)
        with d3:
            annual_income = st.number_input("Annual Income ($)", min_value=0, value=60000, step=1000)

        d4, d5, d6 = st.columns(3)
        with d4:
            high_education = st.selectbox(
                "High Education", ["0", "1"], format_func=lambda v: YES_NO[v]
            )
        with d5:
            address_change = st.selectbox(
                "Recent Address Change", ["0", "1"], format_func=lambda v: YES_NO[v]
            )
        with d6:
            past_num_of_claims = st.number_input("Past Claims", min_value=0, max_value=20, value=0)

        d7, d8, d9 = st.columns(3)
        with d7:
            liab_prct = st.number_input("Liability %", min_value=0, max_value=100, value=50)
        with d8:
            policy_deductible = st.number_input("Deductible ($)", min_value=0, value=1000, step=100)
        with d9:
            annual_premium = st.number_input("Annual Premium ($)", min_value=0.0, value=1200.0, step=50.0)

        html('<div class="cg-divider"></div>')
        html("""
        <div class="cg-section">
            <div class="cg-step">3</div>
            <div><div class="cg-section-title">Vehicle &amp; Claim Amounts</div>
            <div class="cg-section-sub">What's being claimed, and for how much</div></div>
        </div>
        """)

        e1, e2, e3 = st.columns(3)
        with e1:
            age_of_vehicle = st.number_input("Vehicle Age", min_value=0, max_value=30, value=5)
        with e2:
            vehicle_price = st.number_input("Vehicle Price ($)", min_value=0, value=22000, step=500)
        with e3:
            total_claim = st.number_input("Total Claim ($)", min_value=0, value=20000, step=500)

        e4, e5, e6 = st.columns(3)
        with e4:
            injury_claim = st.number_input("Injury Claim ($)", min_value=0, value=5000, step=100)
        with e5:
            days_open = st.number_input("Days Open", min_value=0.0, value=9.0, step=1.0)
        with e6:
            form_defects = st.number_input("Form Defects", min_value=0, max_value=20, value=4)

        st.write("")
        submitted = st.form_submit_button("Run Fraud Assessment", type="primary")


# --------------------------------------------------
# Prediction
# --------------------------------------------------

new_claim = None
result = None

if submitted:

    new_claim = pd.DataFrame({
        "gender": [gender],
        "marital_status": [marital_status],
        "property_status": [property_status],
        "claim_day_of_week": [claim_day_of_week],
        "accident_site": [accident_site],
        "witness_present": [witness_present],
        "channel": [channel],
        "police_report": [police_report],
        "vehicle_category": [vehicle_category],
        "vehicle_color": [vehicle_color],
        "age_of_driver": [age_of_driver],
        "safety_rating": [safety_rating],
        "annual_income": [annual_income],
        "age_of_vehicle": [age_of_vehicle],
        "past_num_of_claims": [past_num_of_claims],
        "liab_prct": [liab_prct],
        "vehicle_price": [vehicle_price],
        "total_claim": [total_claim],
        "injury_claim": [injury_claim],
        "policy_deductible": [policy_deductible],
        "annual_premium": [annual_premium],
        "days_open": [days_open],
        "high_education": [high_education],
        "address_change": [address_change],
        "form_defects": [form_defects],
    })

    try:
        prediction = pipeline.predict(new_claim)[0]
        probabilities = pipeline.predict_proba(new_claim)[0]
        classes = pipeline.named_steps["model"].classes_

        if "Y" in classes:
            fraud_index = list(classes).index("Y")
            fraud_probability = probabilities[fraud_index]
        else:
            fraud_probability = 0

        result = {
            "pct": fraud_probability * 100,
            "is_fraud": prediction == "Y",
        }
    except Exception as e:
        with result_col:
            st.error("Prediction failed.")
            st.exception(e)


# ---------------- Assessment Panel ----------------
with result_col:
    html('<div class="cg-sticky"></div>')

    if result is None:
        html(f"""
        <div class="cg-panel">
            <div class="cg-panel-head">
                <div class="cg-panel-title">Fraud Assessment</div>
                <span class="cg-chip cg-chip-idle">Awaiting input</span>
            </div>
            <div class="cg-empty">
                <div class="cg-empty-icon">{SHIELD_PURPLE}</div>
                <div class="cg-empty-title">No assessment yet</div>
                <div class="cg-empty-text">Fill in the claim details and select <b>Run Fraud Assessment</b>. The fraud probability and verdict will appear here.</div>
            </div>
        </div>
        """)
    else:
        pct = result["pct"]
        is_fraud = result["is_fraud"]

        verdict_class = "cg-verdict-fraud" if is_fraud else "cg-verdict-genuine"
        chip_class = "cg-chip-fraud" if is_fraud else "cg-chip-genuine"
        gauge_color = "#F87171" if is_fraud else "#34D399"
        verdict_text = "Fraudulent Claim" if is_fraud else "Genuine Claim"
        chip_text = "Flagged" if is_fraud else "Cleared"
        verdict_note = (
            "This claim shows a risk pattern consistent with fraudulent claims in the training data."
            if is_fraud else
            "This claim's pattern is consistent with genuine claims in the training data."
        )

        html(f"""
        <div class="cg-panel {verdict_class}">
            <div class="cg-panel-head">
                <div class="cg-panel-title">Fraud Assessment</div>
                <span class="cg-chip {chip_class}">{chip_text}</span>
            </div>
            <div class="cg-gauge-wrap">
                <div class="cg-gauge" style="--p:{pct:.1f}; --c:{gauge_color};">
                    <div class="cg-gauge-inner">
                        <div class="cg-gauge-num">{pct:.1f}%</div>
                        <div class="cg-gauge-lab">Fraud probability</div>
                    </div>
                </div>
            </div>
            <div class="cg-verdict-label">{verdict_text}</div>
            <div class="cg-verdict-note">{verdict_note}</div>
            <div class="cg-meter-label"><span>Low Risk</span><span>High Risk</span></div>
            <div class="cg-meter-track"><div class="cg-meter-fill" style="width:{pct:.1f}%;"></div></div>
            <div class="cg-meter-scale"><span style="left:0%;transform:none;">0%</span><span style="left:50%;">50%</span><span style="left:100%;transform:translateX(-100%);">100%</span></div>
            <div class="cg-snap">
                <div class="cg-snap-item"><div class="cg-snap-val">${total_claim:,.0f}</div><div class="cg-snap-lab">Total claim</div></div>
                <div class="cg-snap-item"><div class="cg-snap-val">${injury_claim:,.0f}</div><div class="cg-snap-lab">Injury claim</div></div>
                <div class="cg-snap-item"><div class="cg-snap-val">{past_num_of_claims}</div><div class="cg-snap-lab">Past claims</div></div>
                <div class="cg-snap-item"><div class="cg-snap-val">{days_open:g}</div><div class="cg-snap-lab">Days open</div></div>
            </div>
        </div>
        """)

if result is not None:
    with st.expander("View Submitted Claim Details"):
        display_data = new_claim.T
        display_data.columns = ["Value"]
        st.table(display_data)


# --------------------------------------------------
# Footer
# --------------------------------------------------

html("""
<div class="cg-footer">
    ClaimGuard is a student ML project for academic demonstration &mdash; predictions are model estimates, not a substitute for formal claims investigation.
</div>
""")
