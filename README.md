# Unit Commitment with Flexible Demand in U.S. Electricity Markets

---

## Table of Contents

1. [Introduction](#introduction)
2. [Key Features](#key-features)
3. [Model Overview](#model-overview)
4. [Key Model Components](#key-model-components)
5. [Project Structure](#project-structure)
6. [Input Overview](#input-overview)
7. [Summary](#summary)
8. [Solver Requirements](#solver-requirements)
9. [Results & Analysis](#results--analysis)
10. [Case Study: Temporal Flexibility](#case-study-temporal-flexibility)
11. [Case Study: Discomfort Costs](#case-study-discomfort-costs)
12. [Summary of Behavioral Findings](#summary-of-behavioral-findings)
13. [Overall Conclusions](#overall-conclusions)
14. [General Conclusions from the Thesis](#general-conclusions-from-the-thesis)
15. [Dependencies](#dependencies)
16. [License / Credits](#license--credits)

---


## Introduction

This project explores the integration of **flexible demand** into the U.S. day-ahead electricity markets via a **unit commitment framework**. The model is designed to be **general and agnostic**, meaning it does not rely on specific technical characteristics of individual loads or consumers. This enables scenario-based analyses and the evaluation of different demand response strategies without needing detailed technical data for each load. The project provides insights into how flexible demand influences system operation, generation scheduling, and market outcomes.

---

## Key Features 

**1. Independence from specific loads**  
- Demand is represented using general flexibility parameters (α) and optional discomfort costs, without requiring device-level data.

**2. Temporal (time-shifting) flexibility**  
- Energy-neutral demand shifting within the day (e.g., 24 hours).  
- Allows adaptation to market conditions to reduce costs or peak loads.

**3. Mixed-Integer Linear Programming (MILP) formulation**  
- Captures generator **on/off decisions** using binary variables.  
- Linear constraints for dispatch and flexible demand.  
- Solvable with GLPK, CBC, or Gurobi.  

**4. Flexible participation in market offers**  
- Generators submit multi-block offers (price, capacity, startup/shutdown costs).  
- Flexible loads submit Hourly Orders with α (flexibility) and discomfort costs.  
- Model optimizes market clearing, generation schedules, and social welfare.

**5. Integration of discomfort costs**  
- Optional penalties to account for consumer inconvenience when shifting demand.

**6. Sensitivity analysis**  
- Across different **α (flexibility) levels**.  
- Across **discomfort cost values** to study trade-offs between welfare optimization and user convenience.

---

## Model Overview

The U.S. day-ahead electricity markets clear generation schedules and prices using a **unit commitment and economic dispatch framework**, where generators submit offers including energy prices, capacities, and operational constraints. The market clearing process determines which units are committed and their hourly dispatch to meet forecasted demand at **minimum system cost**.

To incorporate demand flexibility, the model allows part of the demand to be shifted across hours within the day, while maintaining **energy neutrality** (total daily consumption remains unchanged). This allows flexible loads to adapt their consumption to market conditions, providing potential cost savings, reduced peak loads, and increased social welfare.

### Benefits of the General and Agnostic Approach

- Applicability across multiple markets without detailed load information  
- Policy analysis capabilities: Suitable for system operators, regulators, or governments to evaluate the impact of flexible demand on market stability and social welfare  
- Educational and research tool: Ideal for teaching, research simulations, and scenario analysis  

---

## Key Model Components

| Element | Description |
|----------|--------------|
| **αd (Flexibility Parameter)** | Max fraction of baseline demand that can shift within the day. |
| **Discomfort Cost (Bd)** | Monetary penalty for deviating from preferred hours. |
| **Objective Function** | Maximize **social welfare** (consumer + producer surplus). |
| **Energy Neutrality** | Ensures total daily energy remains constant. |

---

## Project Structure

```bash
Unit_Commitment_FlexDemand/
├── README.md
├── LICENSE
├── requirements.txt
│
└── main/
    ├── code/
    │   └── UnitCommitment_FlexDemand.py        
    │
    ├── input/
    │   └── UnitCommitment_inputs.csv          
    │
    └── output/
        ├── Sensitivity_Analysis_Flexibility/   
        └── Sensitivity_Analysis_Discomfort/    
```

---

## Input Overview

This project demonstrates the **flexible demand model** applied to the **U.S. day-ahead electricity market**. To capture demand flexibility and consumer preferences, the input dataset includes additional fields for:

- **Flexibility parameter (α)**  
- **Optional discomfort costs** for shifting consumption  

For privacy reasons, the full input Excel file cannot be shared. Instead, a screenshot of the first few rows of the dataset is provided for reference, illustrating the structure of the data, the flexibility parameters, and the cost information.  
Users can replicate the workflow with their own U.S. market data if desired.  

The model optimizes **hourly generation schedules**, **demand shifts**, and **social welfare**, while ensuring **energy neutrality** — providing insights into how flexible demand impacts market operations, generation scheduling, and welfare outcomes in the U.S. electricity context.

---

## Summary

The model allows shifting part of the baseline demand from **high-cost hours** to **low-cost hours** without changing the total daily consumption.  
This shift is **energy-neutral**, maintaining total consumption over the day while adapting the timing of usage to market conditions.  

By including parameters such as **α (maximum fraction of shiftable demand)** and **discomfort costs**, the model provides a **flexible, general, and agnostic framework** to study the effects of demand flexibility on market prices, generation schedules, and social welfare in U.S. electricity markets.

---

## Solver Requirements

For large-scale unit commitment problems with flexible demand, a **high-performance solver** is recommended:

- **Gurobi** → Recommended for solving MILP efficiently (**requires valid license**)  
- **GLPK** or **CBC** → Suitable for smaller instances, but may experience longer computational times on large datasets  

> **Note:** The model includes binary variables for unit commitment decisions, which increases complexity.  
> Using **Gurobi** with a proper license ensures faster and more reliable optimization results.

---
## Results & Analysis

### Sensitivity Analysis – Project Summary

This section presents the results of the **sensitivity analyses** conducted on:

- **Flexibility Index (αₑ)**
- **Discomfort Costs**

The purpose of these analyses is to understand how changes in key parameters affect **system performance**, **costs**, and **social welfare**, and to identify which parameters have the most significant impact.

####  Contents

- `flexibility_sensitivity.xlsx` – Sensitivity results for flexibility index  
- `discomfort_cost_sensitivity.xlsx` – Sensitivity results for discomfort costs  
- `plots/` – Graphical representation of analyses, including:
  - Demand curves  
  - Electricity prices  
  - Start-up / shut-down costs  
  - Profit and utility  
  - Social welfare

---

### ⚙️ Case Study: Temporal Flexibility in the U.S. Day-Ahead Market

This case study examines the effect of the **flexibility factor (αd)** on market outcomes, independent of the above sensitivity analyses.

#### Market Data and Setup

- **Hourly analysis:** 24-hour time horizon  
- **Participants:** 7 producers (each submitting 5 hourly bids)  
- **Bids:** Include technical characteristics and startup/shutdown costs  
- **RES units:** Excluded from this study  

---

### 🔍 Sensitivity to Temporal Flexibility (αd)

- (αd) represents the degree of **temporal flexibility of consumers**.  
- Increasing (αd) allows more **shiftable quantities** and enhances **market adaptability**.  
- Demand uniformity coefficient (m₀) rises; demand curve becomes nearly flat for (αd ≥ 0.4).
#### 📈 Key Plots

---

## 📈 Key Plots

### Figure 1 – Demand Curve under different α
<img width="723" height="397" alt="Demand Curve" src="https://github.com/user-attachments/assets/014a6581-2b2c-464c-886e-e8af33baf8f3" />

*The demand curve becomes smoother as flexibility (α) increases, indicating higher adaptability and reduced demand peaks.*

---

### Figure 2 – Electricity Prices
<img width="620" height="318" alt="image" src="https://github.com/user-attachments/assets/3ee4cb4f-0fb6-43e9-8520-8a038ee902d3" />

*Average electricity prices stabilize with increasing demand flexibility, reducing volatility and improving market efficiency.*

---

### Figure 3 – Shifted Load
<img width="616" height="342" alt="image" src="https://github.com/user-attachments/assets/efafe467-e88e-4812-9b93-4e51a0363f5e" />

*Load shifting visualization showing redistribution of consumption from high-cost to low-cost hours.*

---

### Figure 4 – Start-up / Shut-down Costs
<img width="670" height="372" alt="image" src="https://github.com/user-attachments/assets/bacf4043-74b9-4bcb-80ad-514041c39b89" />

*Start-up and hold costs vanish for α ≥ 0.2, reflecting smoother generation scheduling and fewer unit transitions.*

---

### Figure 5 – Producer Profits
<img width="575" height="357" alt="image" src="https://github.com/user-attachments/assets/0fb6743d-3777-47f2-b173-07752957f00b" />

*Producer profits increase initially with flexibility but stabilize beyond α ≥ 0.4, showing diminishing returns.*

---

### Figure 6 – Utility
<img width="618" height="340" alt="image" src="https://github.com/user-attachments/assets/19a492cc-188a-48d6-b9dc-d272947b3a34" />

*Utility trends indicate that moderate flexibility levels optimize both producer and consumer benefits.*

---

### Figure 7 – Social Welfare
<img width="527" height="273" alt="image" src="https://github.com/user-attachments/assets/1dc7264e-6ae3-4e31-875c-1b696288ac06" />

*Overall social welfare rises with flexibility, peaking at α ≈ 0.4 before plateauing.*

---

### 💰 Effect on Market Clearing and Costs

- **Cleared quantity** remains constant across αd values.  
- **Start-up and hold costs** vanish for αd ≥ 0.2.  
- **Fixed operating and production costs** decrease and stabilize for αd ≥ 0.3.  
- **Net demand curve** smooths as αd increases, creating a more stable system.

---
---

### 🔍 Sensitivity to Discomfort Costs (Bd_sh_AWAY, Bd_sh_TOWARDS)

This section analyzes the impact of **discomfort costs** on market outcomes, system operation, and social welfare.  
Discomfort cost represents the **monetary penalty consumers associate with shifting demand** from their preferred hours — capturing the *psychological and behavioral cost of flexibility*.

As discomfort costs increase, consumers become less willing to shift demand, reducing effective flexibility and changing market clearing outcomes.

---

### ⚙️ Key Observations

- **Higher discomfort costs** reduce overall demand flexibility and limit load-shifting potential.  
- **Electricity prices** increase slightly as flexibility decreases.  
- **System operating costs** rise, reflecting reduced optimization potential.  
- **Social welfare** declines beyond moderate discomfort levels.  
- **Producer revenues** stabilize, while **consumer utility** falls as shifting becomes less attractive.

---

## 📈 Key Plots

### Figure 1 – Demand Curve under different Discomfort Cost Levels
<img width="731" height="387" alt="image" src="https://github.com/user-attachments/assets/54e862b6-24fd-406c-aa3f-35253c0d5cf8" />

*The demand curve becomes less elastic as discomfort costs increase, illustrating the reduced willingness of consumers to shift demand.*

---

### Figure 2 – Electricity Prices
<img width="751" height="416" alt="image" src="https://github.com/user-attachments/assets/38166a76-2f99-474c-b02d-a0ed9f7563c6" />

*Average electricity prices rise as discomfort costs increase, driven by reduced flexibility and higher reliance on conventional units.*

---

### Figure 3 – Shifted Load / Load Redistribution
<img width="733" height="312" alt="image" src="https://github.com/user-attachments/assets/926b22a8-9145-4ef6-9253-e84929b638e9" />

*Higher discomfort costs limit demand shifting, concentrating consumption in preferred hours and lowering adaptability.*

---

### Figure 4 – Producer Profits
<img width="630" height="355" alt="image" src="https://github.com/user-attachments/assets/d60d9d19-9ac9-42b1-81d4-d103fab2ea36" />

*Producer profits remain relatively stable at low discomfort levels but decline as consumer flexibility diminishes.*

---

### Figure 5 – Consumer Utility
<img width="712" height="417" alt="image" src="https://github.com/user-attachments/assets/cf3821f1-f034-4ab5-b100-36c16123a1ff" />

*Consumer utility drops as discomfort costs increase, showing the trade-off between comfort and participation in flexibility programs.*

---

### Figure 6 – Social Welfare
<img width="651" height="357" alt="image" src="https://github.com/user-attachments/assets/78b979c5-b478-408c-af98-89e544e10fe1" />

*Overall social welfare declines steadily with higher discomfort costs, underscoring the importance of balancing incentives and flexibility.*

---
---

### 🔎 Summary of Behavioral Findings

| Metric | Effect of Increasing Flexibility (↑αd) | Effect of Increasing Discomfort (↑Bd) |
|--------|-----------------------------------------|---------------------------------------|
| Electricity Prices | ↓ Volatility | ↑ Slightly |
| Start-up Costs | ↓ | ↑ |
| Producer Profits | ↑ then Stable | ↓ |
| Consumer Utility | ↑ to Moderate α | ↑ |
| Social Welfare | ↑ (max α≈0.4) | ↓ |

> ⚖️ **Balanced Outcome:**  
> Optimal welfare occurs when α ≈ 0.3–0.5 and Bd ≤ 50 €/MWh — a level ensuring both efficiency and consumer participation.

---

## 🧭 Overall Conclusions

- **Demand flexibility** significantly improves **market efficiency** and **welfare** by enabling smoother balancing and lower operational costs.  
- **Higher flexibility** (αd ≥ 0.3) eliminates startup costs and stabilizes prices.  
- **Discomfort costs** represent a critical behavioral barrier; moderate levels ensure realistic participation.  
- **Shifting demand** toward renewable-rich hours enhances sustainability and reduces emissions.  
- Policymakers should **promote low-discomfort mechanisms** (e.g., automation, incentives) to sustain flexibility participation.

---


## 📝 General Conclusions from the Thesis

This thesis focused on integrating **flexible demand** into **Day-Ahead Wholesale Electricity Markets**, aiming to design **optimal market-clearing mechanisms** that consider the complexity of demand flexibility and temporal coupling.

**Key Findings:**
- Integrating flexible demand improves **market efficiency** and **social welfare** by enabling smoother balancing of supply and demand, reducing price volatility, and promoting system stability.  
- In both **Greek** and **U.S.** market case studies, increasing the degree of demand flexibility eliminates additional start-up and hold costs, further reducing total production costs.  
- Shifting demand to periods of **high renewable generation** and **low conventional load** reduces the use of conventional units, leveraging **zero-cost and zero-emission** renewable energy without inducing curtailment.  
- **Producer revenues** stabilize as price volatility decreases, while **consumers** benefit from lower peak prices and smoother cost patterns.  
- Maintaining reasonable limits for **discomfort costs** (e.g., ≤50 €/MWh) ensures that demand flexibility remains feasible and attractive for consumers.

---

## 📚 Dependencies

- **Python ≥ 3.8**  
- **pandas** – Data handling  
- **numpy** – Numerical operations  
- **gurobipy** – Solver and optimization API  
- **xlsxwriter / openpyxl** – Excel export and manipulation  

---

## 📄 License / Credits

This project is provided for educational and research purposes. You are free to use, modify, and share it under the MIT License. See the LICENSE file for details.  

The code and models were developed as part of the **Diploma Thesis titled _"Analysis of the Impact of Flexible Demand on the Day-Ahead Wholesale Electricity Market"_**, conducted at the **University of Patras**, School of Electrical and Computer Engineering.  

The research focuses on the **optimization and market integration of flexible demand** in **modern Day-Ahead Wholesale Electricity Markets**, analyzing both **European (simple bidding)** and **U.S. (complex bidding)** market mechanisms. It examines how different clearing strategies can incorporate time flexibility of demand, assess their impact on market efficiency, system operation, and social welfare, and proposes optimal frameworks that account for temporal coupling constraints.

![Python Version](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)


