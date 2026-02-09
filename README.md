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

## 🧠 Task-2: Bayesian Change Point Modeling & Insight Generation

Task-2 focused on **formally detecting and quantifying structural breaks** in Brent oil prices using **Bayesian Change Point Analysis**, building directly on the foundations established in Task-1.

---

### 1. Model Objective and Rationale

Given the clear evidence of:

* Non-stationarity in price levels
* Volatility clustering
* Event-driven regime shifts

a **Bayesian change point model** was selected to:

* Identify *when* a structural change likely occurred
* Quantify *how* price behavior differs across regimes
* Explicitly model uncertainty rather than relying on point estimates

Bayesian inference allows probabilistic interpretation, which is crucial in noisy financial time series like oil prices.

---

### 2. Model Specification

The model was implemented using **PyMC** with the following components:

* **Change Point (τ)**

  * Defined as a discrete uniform random variable over the full time index
  * Represents the unknown time at which the regime shift occurs

* **Regime Means (μ₁, μ₂)**

  * μ₁: Mean log return *before* the change point
  * μ₂: Mean log return *after* the change point

* **Volatility (σ)**

  * Single global volatility parameter shared across regimes
  * Captures overall market uncertainty

* **Likelihood Function**

  * Log returns modeled as a Normal distribution
  * `pm.math.switch()` used to select parameters before and after τ

This structure allows the model to adaptively switch regimes based on the inferred change point.

---

### 3. MCMC Sampling and Diagnostics

* Sampling performed using **NUTS (No-U-Turn Sampler)**
* Multiple chains were run to ensure robustness
* Diagnostic checks included:

  * Trace plots
  * Posterior distributions
  * R-hat convergence statistics

**Key diagnostic findings:**

* μ₁ and σ show strong convergence
* μ₂ exhibits higher uncertainty, reflecting increased post-change volatility
* τ shows a wide posterior, indicating uncertainty in exact timing but clear regime-level change

---

### 4. Change Point Estimation Results

* **Most probable change point date:**
  📅 **June 4, 2012**

* **Posterior behavior:**

  * Heavily skewed toward the later part of the dataset
  * Very wide credible interval, spanning much of the series

This suggests:

* The market experienced **gradual structural adjustment**, not a single sharp break
* Multiple overlapping global shocks contribute to regime instability

---

### 5. Regime Comparison and Quantitative Impact

| Metric          | Before Change (μ₁) | After Change (μ₂)    |
| --------------- | ------------------ | -------------------- |
| Mean Log Return | ~0.00009           | ~0.0082              |
| Volatility      | Lower              | Significantly higher |
| Stability       | Relatively stable  | Highly uncertain     |

**Quantified Impact:**

* Absolute increase in mean log return: **~0.0081**
* Percentage increase: **~8,700%**
* Indicates a shift from near-flat growth to higher expected returns, **at the cost of increased risk**

---

### 6. Event Association and Interpretation

The inferred change point aligns temporally with:

* Post–Global Financial Crisis market restructuring
* Arab Spring–related supply disruptions
* Shifts in OPEC policy behavior
* Increasing financialization of oil markets

Rather than a single triggering event, the results suggest a **structural transition driven by accumulated geopolitical and economic stressors**.

---

### 7. Key Takeaways from Task-2

* Successfully detected a statistically meaningful regime shift
* Quantified how price behavior changed across regimes
* Explicitly modeled uncertainty and avoided overconfident conclusions
* Provided a strong analytical bridge between data and real-world events

---

## 📈 Task-3: Interactive Dashboard Development

Task-3 translated the analytical results into a **decision-support dashboard** that allows stakeholders to interactively explore Brent oil price behavior and its relationship with global events.

---

### 1. Objective

To build an **interactive, user-friendly dashboard** that enables:

* Exploration of historical Brent oil prices
* Visualization of Bayesian change point results
* Event-based interpretation of price and volatility shifts
* Non-technical access to complex statistical findings

---

### 2. System Architecture

The dashboard follows a **client–server architecture**:

#### Backend (Flask)

Responsible for:

* Serving historical price data
* Exposing change point results
* Providing curated event metadata via REST APIs

Structured endpoints include:

* `/prices` – historical Brent price data
* `/change-points` – inferred change point statistics
* `/events` – geopolitical and economic event data

---

#### Frontend (React)

Responsible for:

* Data visualization
* User interaction
* Insight exploration

Key components include:

* **PriceChart** – time series visualization
* **ChangePointChart** – regime shift overlay
* **EventTimeline** – event-based annotations
* **Filters** – date range and event-type selection

---

### 3. Key Dashboard Features

* Interactive price charts with zoom and hover support
* Highlighted change point(s) inferred from Bayesian analysis
* Event overlays to contextualize price movements
* Volatility indicators to assess market risk
* Responsive design for desktop, tablet, and mobile

---

### 4. Setup Instructions (Dashboard)

#### Backend Setup

```bash
cd dashboard/backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

#### Frontend Setup

```bash
cd dashboard/frontend
npm install
npm start
```

---

### 5. Deliverables

* Fully functional Flask backend with documented endpoints
* React-based interactive dashboard
* Screenshots demonstrating dashboard functionality
* README with setup and usage instructions

---

### 6. Task-3 Results

* Analytical results made accessible to non-technical users
* Clear visual linkage between events and price regimes
* Improved interpretability of Bayesian outputs
* Strong alignment with stakeholder decision-making needs

---

## ✅ Overall Project Outcome

Across all three tasks, the project:

* Demonstrated that Brent oil prices undergo **statistically significant regime shifts**
* Quantified the magnitude and uncertainty of these shifts
* Linked statistical findings to real-world geopolitical and economic events
* Delivered both **technical rigor** and **practical usability**

This project provides Birhan Energies with a **robust analytical framework and interactive toolset** for understanding and communicating oil market dynamics.

