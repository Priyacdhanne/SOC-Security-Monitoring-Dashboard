import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SOC Security Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# ============================================================
# LOAD SECURITY LOG DATA
# ============================================================

df = pd.read_csv("security_logs.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"])

# ============================================================
# TITLE
# ============================================================

st.title("🛡️ SOC Security Monitoring Dashboard")
st.subheader("Security alert monitoring and analysis")

# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Alert Filters")

# Severity filter
severity_options = ["All"] + sorted(df["severity"].unique().tolist())

selected_severity = st.sidebar.selectbox(
    "Severity",
    severity_options
)

# Status filter
status_options = ["All"] + sorted(df["status"].unique().tolist())

selected_status = st.sidebar.selectbox(
    "Status",
    status_options
)

# Event type filter
event_options = ["All"] + sorted(df["event_type"].unique().tolist())

selected_event = st.sidebar.selectbox(
    "Event Type",
    event_options
)

# ============================================================
# SEARCH ALERT ID / SOURCE IP
# ============================================================

st.sidebar.markdown("---")

search_alert = st.sidebar.text_input(
    "🔍 Search Alert ID or Source IP",
    placeholder="Example: ALT003 or 172.16.0.8"
)

# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

if selected_severity != "All":
    filtered_df = filtered_df[
        filtered_df["severity"] == selected_severity
    ]

if selected_status != "All":
    filtered_df = filtered_df[
        filtered_df["status"] == selected_status
    ]

if selected_event != "All":
    filtered_df = filtered_df[
        filtered_df["event_type"] == selected_event
    ]

# Search Alert ID or Source IP
if search_alert:
    search_alert = search_alert.strip()

    filtered_df = filtered_df[
        filtered_df["alert_id"].astype(str).str.contains(
            search_alert,
            case=False,
            na=False
        )
        |
        filtered_df["source_ip"].astype(str).str.contains(
            search_alert,
            case=False,
            na=False
        )
    ]

# ============================================================
# DASHBOARD METRICS
# ============================================================

total_alerts = len(filtered_df)

critical_alerts = len(
    filtered_df[filtered_df["severity"] == "Critical"]
)

high_alerts = len(
    filtered_df[filtered_df["severity"] == "High"]
)

open_incidents = len(
    filtered_df[filtered_df["status"] == "Open"]
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Alerts",
        total_alerts
    )

with col2:
    st.metric(
        "Critical Alerts",
        critical_alerts
    )

with col3:
    st.metric(
        "High Alerts",
        high_alerts
    )

with col4:
    st.metric(
        "Open Incidents",
        open_incidents
    )

st.divider()

# ============================================================
# ALERTS BY SEVERITY
# ============================================================

st.header("Alerts by Severity")

if len(filtered_df) > 0:

    severity_counts = (
        filtered_df["severity"]
        .value_counts()
        .reset_index()
    )

    severity_counts.columns = ["Severity", "Count"]

    fig_severity = px.bar(
        severity_counts,
        x="Severity",
        y="Count",
        title="Security Alerts by Severity",
        text="Count"
    )

    st.plotly_chart(
        fig_severity,
        use_container_width=True
    )

else:
    st.warning("No alerts match the selected filters.")

# ============================================================
# ALERTS BY EVENT TYPE
# ============================================================

st.header("Alerts by Event Type")

if len(filtered_df) > 0:

    event_counts = (
        filtered_df["event_type"]
        .value_counts()
        .reset_index()
    )

    event_counts.columns = ["Event Type", "Count"]

    fig_events = px.bar(
        event_counts,
        x="Event Type",
        y="Count",
        title="Security Alerts by Event Type",
        text="Count"
    )

    st.plotly_chart(
        fig_events,
        use_container_width=True
    )

# ============================================================
# SECURITY ALERT TABLE
# ============================================================

st.header("Security Alerts")

if len(filtered_df) > 0:

    display_df = filtered_df.copy()

    display_df["timestamp"] = display_df[
        "timestamp"
    ].dt.strftime("%Y-%m-%d %H:%M:%S")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.warning("No alerts match the selected filters.")

# ============================================================
# INCIDENT INVESTIGATION
# ============================================================

st.header("🔍 Incident Investigation")

if len(filtered_df) > 0:

    for _, alert in filtered_df.iterrows():

        with st.expander(
            f"{alert['alert_id']} — "
            f"{alert['event_type']} — "
            f"{alert['severity']}"
        ):

            col1, col2 = st.columns(2)

            with col1:
                st.write(
                    f"**Alert ID:** {alert['alert_id']}"
                )

                st.write(
                    f"**Timestamp:** {alert['timestamp']}"
                )

                st.write(
                    f"**Source IP:** {alert['source_ip']}"
                )

                st.write(
                    f"**Username:** {alert['username']}"
                )

            with col2:
                st.write(
                    f"**Event Type:** {alert['event_type']}"
                )

                st.write(
                    f"**Severity:** {alert['severity']}"
                )

                st.write(
                    f"**Status:** {alert['status']}"
                )

            # Analyst observation
            if alert["severity"] == "Critical":

                observation = (
                    f"Critical {alert['event_type']} alert detected "
                    f"from {alert['source_ip']}. "
                    f"Review the affected account and investigate "
                    f"related activity from this source."
                )

            elif alert["severity"] == "High":

                observation = (
                    f"High-severity {alert['event_type']} activity "
                    f"detected from {alert['source_ip']}. "
                    f"Review related login and network activity."
                )

            else:

                observation = (
                    f"{alert['event_type']} activity detected from "
                    f"{alert['source_ip']}. Review the alert and "
                    f"determine whether additional investigation "
                    f"is required."
                )

            st.info(
                "**Analyst Observation:** " + observation
            )

else:
    st.warning(
        "No alerts match the selected filters."
    )

# ============================================================
# REPEATED SOURCE IPs
# ============================================================

st.header("🚨 Repeated Source IPs")

if len(filtered_df) > 0:

    ip_counts = (
        filtered_df["source_ip"]
        .value_counts()
        .reset_index()
    )

    ip_counts.columns = [
        "Source IP",
        "Alert Count"
    ]

    repeated_ips = ip_counts[
        ip_counts["Alert Count"] > 1
    ]

    if len(repeated_ips) > 0:

        st.dataframe(
            repeated_ips,
            use_container_width=True,
            hide_index=True
        )

        st.info(
            "**Analyst Note:** Source IPs appearing multiple "
            "times may indicate repeated suspicious activity "
            "and should be reviewed during incident investigation."
        )

    else:

        st.write(
            "No repeated source IPs found for the selected filters."
        )

# ============================================================
# SOC ATTACK SUMMARY
# ============================================================

st.header("📊 SOC Attack Summary")

if len(filtered_df) > 0:

    attack_summary = (
        filtered_df["event_type"]
        .value_counts()
        .reset_index()
    )

    attack_summary.columns = [
        "Event Type",
        "Alert Count"
    ]

    st.dataframe(
        attack_summary,
        use_container_width=True,
        hide_index=True
    )

    most_common_event = attack_summary.iloc[0]

    st.info(
        f"**Analyst Summary:** The most frequently observed "
        f"event type is **{most_common_event['Event Type']}** "
        f"with **{most_common_event['Alert Count']}** alerts."
    )

else:

    st.warning(
        "No attack data available for the selected filters."
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SOC Security Monitoring Dashboard | "
    "Python + Pandas + Streamlit"
)