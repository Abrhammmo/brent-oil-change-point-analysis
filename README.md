# **Brent Oil Price Change Point Analysis**

## 📌 Project Description

This project investigates how major geopolitical, economic, and policy-driven events influence **Brent crude oil prices** using **Bayesian Change Point Analysis**. The analysis is conducted in the context of **Birhan Energies**, a consultancy firm that provides data-driven insights to stakeholders in the global energy sector.

Brent oil prices are highly volatile and sensitive to external shocks such as political conflicts, OPEC policy changes, economic crises, and international sanctions. Understanding when and how price regimes change is critical for investors, policymakers, and energy companies to manage risk, ensure energy security, and make informed strategic decisions.

The project emphasizes **statistical rigor, interpretability, and clear communication**, with Bayesian methods used to detect structural breaks in oil price behavior.

---

## 🎯 Objectives

* Identify statistically significant structural changes in Brent oil prices
* Quantify changes in price behavior before and after regime shifts
* Relate detected change points to major global events
* Provide insights that support:

  * Investment strategy formulation
  * Energy policy analysis
  * Operational planning in the energy sector

---

## 📊 Data Sources

### Brent Oil Price Data

* **Description**: Daily Brent crude oil prices
* **Time Period**: May 20, 1987 – September 30, 2022
* **Variables**:

  * `Date`: Trading date
  * `Price`: Price in USD per barrel
* **Source**: Publicly available historical commodity price datasets (e.g., financial market data providers)

### Event Data

* A manually curated dataset of major:

  * Geopolitical conflicts
  * OPEC policy decisions
  * Economic shocks
  * Sanctions affecting oil supply
* Each event includes an approximate start date and description
* Used for **interpretation and contextual analysis**, not as direct model inputs

---

## 🧪 Task-1: Foundation for Analysis (What Was Done)

Task-1 focused on building a strong analytical foundation before applying Bayesian change point models.

### 1. Data Analysis Workflow Definition

A clear, step-by-step workflow was designed, covering:

* Data loading and cleaning
* Exploratory data analysis (EDA)
* Time series diagnostics
* Event data integration
* Model justification and insight generation

This workflow ensures transparency, reproducibility, and alignment with real-world decision-making needs.

---

### 2. Exploratory Time Series Analysis

The Brent oil price series was analyzed to understand its statistical properties:

* **Trend Analysis**: Long-term price cycles and structural shifts were identified through visualization.
* **Stationarity Testing**: Augmented Dickey-Fuller (ADF) tests confirmed that price levels are non-stationary, while log returns are closer to stationary.
* **Volatility Analysis**: Rolling volatility analysis revealed volatility clustering, particularly during global crises.

These findings justified the use of **change point models**, which are designed to detect regime shifts rather than assume constant behavior over time.

---

### 3. Log Return Transformation

Log returns were computed to:

* Stabilize variance
* Improve stationarity
* Better capture sudden shocks and volatility regimes

This transformation supports both diagnostic analysis and future modeling decisions.

---

### 4. Event Data Research and Integration

A structured dataset of 15 major global events was compiled, covering:

* Financial crises
* Armed conflicts in oil-producing regions
* OPEC production decisions
* Global pandemics and sanctions

Events were visually overlaid on the Brent oil price series to:

* Identify temporal alignment between price shocks and real-world events
* Support hypothesis generation for later change point interpretation

---

### 5. Assumptions and Limitations

Key assumptions and limitations were explicitly documented, including:

* Oil prices reflect aggregated global market expectations
* Event dates are approximate and may not capture anticipation or delayed reactions
* Multiple overlapping events complicate attribution

**Crucially**, a clear distinction was made between:

* **Statistical correlation in time** (what the analysis detects)
* **Causal impact** (which cannot be proven using price data alone)

This ensures results are interpreted responsibly and accurately.

---

### 6. Communication Strategy

Appropriate communication formats were identified for different stakeholders:

* Interactive dashboards for exploratory analysis
* Written reports for policymakers and decision-makers
* Technical notebooks for transparency and reproducibility

---

## ⚙️ Setup Instructions

### 1️⃣ Create and Activate a Virtual Environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run the Analysis

### Step 1: Time Series Analysis (Task-1)

```bash
jupyter notebook notebooks/01_time_series_analysis.ipynb
```

This notebook includes:

* Data loading and cleaning
* Trend visualization
* Stationarity testing
* Volatility analysis
* Event overlay and interpretation groundwork

---

### Step 2: Bayesian Change Point Modeling

```bash
jupyter notebook notebooks/03_bayesian_change_point_model.ipynb
```

This stage applies Bayesian inference using PyMC to:

* Detect structural breaks
* Quantify regime shifts
* Compare statistical results with known global events

---

## ⚠️ Key Notes

* Change point analysis identifies **when** price behavior changes, not **why**
* Event alignment supports interpretation, not causal claims
* Results should be used as **decision-support evidence**, not definitive predictions