# 🛡️ SOC Security Monitoring Dashboard

## 📌 Project Overview

This project is a beginner-friendly Security Operations Center (SOC) monitoring dashboard built using Python, Pandas, Streamlit, and Plotly.

The dashboard analyzes simulated security alerts and provides an interactive interface for monitoring, filtering, searching, and investigating security events.

This project was created as a cybersecurity portfolio project to demonstrate fundamental SOC analyst skills.

---

## 🎯 Project Objectives

- Analyze security alert logs
- Monitor alert severity
- Identify critical and high-severity incidents
- Track open security incidents
- Search for specific alerts and source IP addresses
- Identify repeated source IP activity
- Analyze common security event types
- Support basic incident investigation
- Display analyst observations

---

## 🛠️ Technologies Used

- Python 3.14
- Pandas
- Streamlit
- Plotly
- CSV

---

## 🔐 Security Events

The simulated dataset contains:

- Brute Force
- Phishing
- Malware
- Failed Login
- Port Scan
- Suspicious Login

---

## 📊 Dashboard Features

### 1. Security Alert Monitoring

Displays:

- Total Alerts
- Critical Alerts
- High Alerts
- Open Incidents

### 2. Alert Filtering

Alerts can be filtered by:

- Severity
- Status
- Event Type

### 3. Alert Search

Search for alerts using:

- Alert ID
- Source IP address

### 4. Incident Investigation

Individual alerts display:

- Alert ID
- Timestamp
- Source IP
- Username
- Event Type
- Severity
- Status
- Analyst Observation

### 5. Repeated Source IP Detection

Identifies source IP addresses that appear multiple times in the security logs.

### 6. SOC Attack Summary

Provides a summary of the frequency of different security event types.

---

## 🔎 Example Investigation

Example alert:

```text
Alert ID: ALT003
Timestamp: 2026-09-25 08:35:00
Source IP: 172.16.0.8
Username: user2
Event Type: Malware
Severity: Critical
Status: Open