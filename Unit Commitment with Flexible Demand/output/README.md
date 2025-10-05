# Sensitivity Analysis – Project Summary

This repository contains the results of the sensitivity analyses conducted on:

- **Flexibility Index**
- **Discomfort Costs**

The purpose of these analyses is to understand how changes in key parameters affect system performance, costs, and social welfare, and to identify the parameters with the most significant impact.

## Contents

- `flexibility_sensitivity.xlsx` – Sensitivity analysis results for the flexibility index.  
- `discomfort_cost_sensitivity.xlsx` – Sensitivity analysis results for discomfort costs.  
- `plots/` – Graphical representation of the sensitivity analyses, including:
  - Demand curves  
  - Electricity prices  
  - start-up / shut-down cost
  - Profit  
  - Utility
  - Social welfare  

- `README.md` – This file, including methodology and conclusions.
# Sensitivity Analysis – Project Summary

## Case Study: Temporal Flexibility in the U.S. Day-Ahead Wholesale Electricity Market

This case study examines the effect of ** flexibility factor (a𝑑)** on market outcomes, independent of the above sensitivity analyses.

**Market Data and Participants**  
- Hourly analysis over 24 hours.  
- 7 producers, each submitting 5 bids per hour.  
- Technical characteristics included in bids; RES excluded.  

**Sensitivity to Temporal Flexibility (a𝑑)**  
- \(a_d\) represents the degree of temporal flexibility of consumers.  
- Increasing \(a_d\) allows more shiftable quantities and enhances market adaptability.  
- Demand uniformity coefficient \(m_0\) rises; demand curve nearly flat for \(a_d \ge 0.4\).  

**Effect on Market Clearing and Costs**  
- Cleared quantity remains constant.  
- Start-up and hold costs vanish for \(a_d \ge 0.2\).  
- Fixed operating and production costs decrease and stabilize for \(a_d \ge 0.3\).  
- Net demand curve smooths as \(a_d\) increases, creating a more stable system.  

**Revenues, Profits, and Welfare**  
- **Producer profits:** Increase for \(0 \le a_d \le 0.2\), slightly decrease for \(0.2 \le a_d \le 0.4\), stabilize for \(a_d \ge 0.4\).  
- **Consumer welfare:** Initially decreases for \(0 \le a_d \le 0.2\), increases for \(0.2 \le a_d \le 0.4\), stabilizes for \(a_d \ge 0.4\).  

**Conclusions**  
- Temporal flexibility smooths the demand curve and reduces start-up/hold costs.  
- System becomes more stable and efficient.  
- Saturation at \(a_d \ge 0.4\); additional flexibility beyond this point gives no extra benefits.  
- Managing flexible quantities optimizes costs and producer profits.

## Sensitivity Analysis – Discomfort Costs

In addition to flexibility, the sensitivity of **discomfort costs** was analyzed to understand how changes in key parameters affect consumer discomfort, system costs, and social welfare.

**Key Findings**  
- Discomfort costs are primarily affected by variations in demand patterns and electricity prices.  
- High start-up or shut-down costs can increase overall system costs, indirectly impacting consumer welfare.  
- Changes in discomfort costs highlight trade-offs between operational costs, market flexibility, and social welfare.  
- Identifying the parameters with the greatest impact guides system optimization and operational decisions.

**Conclusions**  
- Reducing discomfort costs requires careful management of demand shifts and operational costs.  
- Targeted optimization of high-impact parameters enhances consumer welfare while maintaining system efficiency.  
- Sensitivity analysis offers actionable insights for planners and operators to balance cost, flexibility, and welfare.
