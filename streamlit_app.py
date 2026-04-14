import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Vendor Risk Assessment",
    page_icon="🔐",
    layout="wide",
)

# ── Default data (bundled fallback) ──────────────────────────────────────────
DEFAULT_DATA = {
    "vendor": "Vendor 12345, Inc.",
    "questionnaire": "TPCRA Questionnaire - Part 2",
    "assessment_summary": {
        "total_risks_identified": 21,
        "high": 1,
        "medium": 7,
        "low": 13,
        "overall_posture": "Strong — vendor demonstrates mature security controls across most domains with minor gaps.",
    },
    "risks": [
        {"category": "Organizational Management", "risk": "IT Security Policy last updated March 2024 — approaching annual review threshold; may not reflect latest threat landscape or regulatory changes.", "severity": "Low"},
        {"category": "Human Resource Management", "risk": "Security awareness program described but no mention of phishing simulation exercises or quantitative training effectiveness metrics.", "severity": "Low"},
        {"category": "Infrastructure Security", "risk": "Patch management applies critical OS patches nightly, but no explicit SLA or timeline defined for non-critical/non-OS patches, leaving potential residual vulnerability windows.", "severity": "Low"},
        {"category": "Infrastructure Security", "risk": "Malware controls rely primarily on Sophos Intercept X. No mention of supplementary XDR platform or threat hunting capability beyond automated alerting.", "severity": "Low"},
        {"category": "Data Protection", "risk": "Data in transit uses TLS 1.2 — TLS 1.3 not mentioned; TLS 1.2 is still acceptable but TLS 1.3 provides stronger security guarantees.", "severity": "Low"},
        {"category": "Data Protection", "risk": "Vendor explicitly states they do not rely on a DLP package. Absence of a dedicated DLP tool may reduce detectability of insider data exfiltration.", "severity": "Medium"},
        {"category": "Identity & Access Management", "risk": "Privileged access management relies on procedural controls and RBAC. No dedicated PAM solution (e.g., CyberArk, BeyondTrust) explicitly mentioned.", "severity": "Medium"},
        {"category": "Identity & Access Management", "risk": "MFA implemented via Google Authenticator (TOTP-based). No mention of phishing-resistant MFA (e.g., FIDO2/WebAuthn) for privileged access.", "severity": "Low"},
        {"category": "Application Security", "risk": "Third-party penetration testing is conducted every 2–3 releases rather than on a fixed schedule. Extended intervals increase the window of undetected vulnerabilities.", "severity": "Medium"},
        {"category": "Application Security", "risk": "Secure SDLC described through manual review processes but no automated SAST or DAST tools mentioned in the CI/CD pipeline.", "severity": "Medium"},
        {"category": "Application Security", "risk": "No mention of Software Bill of Materials (SBOM) or automated third-party/open-source library vulnerability tracking (e.g., Snyk, Dependabot).", "severity": "Medium"},
        {"category": "System Security", "risk": "Security log review and monitoring confirmed but no specific SIEM platform identified. Correlation capability and coverage scope are unverified.", "severity": "Low"},
        {"category": "Email", "risk": "Email gateway scans for spam, malware, and phishing but no mention of URL sandboxing or link rewriting technology.", "severity": "Low"},
        {"category": "Mobile Devices", "risk": "BYOD prohibited unless authorized by IT, but no criteria or security baseline defined for approved personal device use.", "severity": "Low"},
        {"category": "Incident Response", "risk": "Incident response commits to 48-hour customer notification but does not explicitly address regulatory breach notification timelines (e.g., PDPA, GDPR 72-hour requirement).", "severity": "Medium"},
        {"category": "Incident Response", "risk": "Incident Response Plan tested annually but no mention of tabletop exercises, red team simulations, or third-party IR retainer.", "severity": "Low"},
        {"category": "Cloud Services", "risk": "Cloud portability confirmed but no specific data portability mechanism, exit strategy timeline, or transition assistance SLA is described.", "severity": "Low"},
        {"category": "Cloud Services", "risk": "Cloud security certifications confirmed (ISO 27001, SOC 2 Type 2) but shared responsibility model between vendor and AWS is not explicitly documented.", "severity": "Low"},
        {"category": "Business Continuity", "risk": "Business Continuity Plan exists and is tested annually, but no RTO or RPO targets are specified, making resilience commitments unverifiable.", "severity": "Medium"},
        {"category": "Business Continuity", "risk": "BCP test results and outcomes not shared; without evidence of test findings and remediation, the effectiveness of the plan cannot be independently assessed.", "severity": "Low"},
        {"category": "AI Controls", "risk": "No AI Controls section present in the questionnaire. Vendor's use of AI/ML tools is unassessed. AI-specific risks (model bias, data poisoning, AI-assisted fraud) are not addressed.", "severity": "High"},
    ],
}

SEVERITY_COLORS = {"High": "#E24B4A", "Medium": "#EF9F27", "Low": "#639922"}
SEVERITY_ORDER  = ["High", "Medium", "Low"]

# ── Sidebar: upload a different JSON ─────────────────────────────────────────
with st.sidebar:
    st.header("Data source")
    uploaded = st.file_uploader(
        "Upload a risk assessment JSON",
        type="json",
        help="Must follow the same schema as the bundled sample.",
    )
    if uploaded:
        try:
            DATA = json.load(uploaded)
            st.success("Loaded uploaded file.")
        except Exception as e:
            st.error(f"Could not parse JSON: {e}")
            DATA = DEFAULT_DATA
    else:
        DATA = DEFAULT_DATA
        st.info("Using bundled sample data.")

    st.divider()
    st.caption("Vendor Risk Assessment Dashboard · TPCRA")

# ── Load into DataFrame ───────────────────────────────────────────────────────
df      = pd.DataFrame(DATA["risks"])
summary = DATA["assessment_summary"]

# ── Header ───────────────────────────────────────────────────────────────────
st.title(f"🔐 {DATA['vendor']}")
st.caption(DATA["questionnaire"])
st.success(f"✅ {summary['overall_posture']}")
st.divider()

# ── Metric cards ─────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Risks", summary["total_risks_identified"])
c2.metric("🔴 High",     summary["high"])
c3.metric("🟠 Medium",   summary["medium"])
c4.metric("🟢 Low",      summary["low"])

st.divider()

# ── Charts row ───────────────────────────────────────────────────────────────
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("Risks by category")
    cat_df = (
        df.groupby(["category", "severity"])
        .size()
        .reset_index(name="count")
    )
    fig_bar = px.bar(
        cat_df,
        x="count",
        y="category",
        color="severity",
        orientation="h",
        color_discrete_map=SEVERITY_COLORS,
        category_orders={"severity": SEVERITY_ORDER},
        labels={"count": "Number of risks", "category": ""},
    )
    fig_bar.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        legend_title_text="Severity",
        height=380,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis={"categoryorder": "total ascending"},
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.subheader("Distribution")
    sev_counts = df["severity"].value_counts().reindex(SEVERITY_ORDER).reset_index()
    sev_counts.columns = ["severity", "count"]
    fig_donut = go.Figure(go.Pie(
        labels=sev_counts["severity"],
        values=sev_counts["count"],
        hole=0.65,
        marker_colors=[SEVERITY_COLORS[s] for s in sev_counts["severity"]],
        textinfo="label+percent",
        hovertemplate="%{label}: %{value}<extra></extra>",
    ))
    fig_donut.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_donut, use_container_width=True)

st.divider()

# ── Risk table ───────────────────────────────────────────────────────────────
st.subheader("All risks")

col_f1, col_f2 = st.columns([2, 3])
with col_f1:
    severity_filter = st.multiselect(
        "Filter by severity",
        options=SEVERITY_ORDER,
        default=SEVERITY_ORDER,
    )
with col_f2:
    category_filter = st.multiselect(
        "Filter by category",
        options=sorted(df["category"].unique()),
        default=sorted(df["category"].unique()),
    )

filtered_df = df[
    df["severity"].isin(severity_filter) &
    df["category"].isin(category_filter)
].reset_index(drop=True)

st.caption(f"Showing {len(filtered_df)} of {len(df)} risks")

st.dataframe(
    filtered_df[["category", "risk", "severity"]].rename(columns={
        "category": "Category",
        "risk":     "Risk Description",
        "severity": "Severity",
    }),
    use_container_width=True,
    hide_index=True,
    column_config={
        "Severity":         st.column_config.TextColumn(width="small"),
        "Category":         st.column_config.TextColumn(width="medium"),
        "Risk Description": st.column_config.TextColumn(width="large"),
    },
)

st.divider()
st.caption("Generated from TPCRA Questionnaire · Third Party Cyber Risk Assessment")
