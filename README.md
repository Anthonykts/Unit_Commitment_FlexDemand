# Flexible Demand and Unit Commitment in U.S. Electricity Markets

This project explores the integration of flexible demand into the U.S. day-ahead electricity markets through a unit commitment framework. The model is designed to be general and agnostic, meaning it does not rely on specific technical characteristics of individual loads or consumers. This allows for flexible, scenario-based analyses and facilitates the evaluation of different demand response strategies without the need for detailed technical data for each load. The project aims to provide insights into how flexible demand can influence system operation, generation scheduling, and market outcomes in the U.S. electricity context.

## 🔑 Key Features of the Model

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

## 🌟 Benefits of the General and Agnostic Approach
- Applicability across multiple markets without detailed load information
- Policy analysis capabilities: Suitable for system operators, regulators, or governments to evaluate the impact of flexible demand on market stability and social welfare
- Educational and research tool: Ideal for teaching, research simulations, and scenario analysis

## 📌 Model Overview

The U.S. day-ahead electricity markets clear generation schedules and prices using a **unit commitment and economic dispatch framework**, where generators submit offers including energy prices, capacities, and operational constraints. The market clearing process determines which units are committed and their hourly dispatch to meet forecasted demand at minimum system cost. 

To incorporate demand flexibility, the model allows part of the demand to be shifted across hours within the day, while maintaining **energy neutrality** (total daily consumption remains unchanged). This allows flexible loads to adapt their consumption to market conditions, providing potential cost savings, reduced peak loads, and increased social welfare.

## 🔎 Key Elements  

- **Demand Flexibility Parameter (αd):** Maximum fraction of baseline demand that can be shifted across hours.  
- **Discomfort Costs:** Optional penalties that model the inconvenience of shifting consumption from preferred hours.  
- **Objective:** Maximize **social welfare**, defined as the sum of consumer surplus and producer surplus.  
- **Energy Neutrality:** Ensures total daily consumption remains constant.  
- **Sensitivity Analysis:** Study how varying α affects market outcomes, prices, and social welfare.  

---

## 🏗️ Project Structure

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

## 📄 Main Project Overview

The main project demonstrates the flexible demand model using real market data from the Greek day-ahead electricity market for May 17, 2024. To capture demand flexibility and consumer preferences, three additional columns were added to the input dataset:
- Flexibility parameter (α)
- Optional discomfort costs for shifting consumption

For privacy reasons, the full input Excel file cannot be shared. Instead, a screenshot of the first few rows of the dataset is provided for reference, illustrating the structure of the data, the flexibility parameters, and the cost information. This allows users to replicate the workflow with their own data if desired.
The model optimizes hourly generation schedules, shifted demand, and social welfare, respecting energy neutrality constraints, providing insights into how flexible demand affects the Greek day-ahead market.

## 📌 Summary

The model allows shifting part of the baseline demand from high-cost hours to low-cost hours without changing the total daily consumption. This shift is energy-neutral, maintaining total consumption over the day while adapting the timing of consumption to market conditions. By including parameters such as α (maximum fraction of shiftable demand) and optional discomfort costs, the model provides a flexible, general, and agnostic framework to study the effects of demand flexibility on market prices, generation schedules, and social welfare in U.S. electricity markets.

## ⚙️ Solver Requirements

For large-scale unit commitment problems with flexible demand, a **high-performance solver** is recommended:

- **Gurobi**: Recommended for solving MILP efficiently. **Requires a valid license**.
- **GLPK** or **CBC** can be used for smaller instances, but may struggle with computational time on large datasets.

> **Note:** The model includes binary variables for unit commitment decisions, which increases complexity. Using Gurobi with a proper license ensures faster and more reliable optimization results.

## 📚 Dependencies

- Python ≥ 3.8 
- pandas – Data handling
- numpy – Numerical operations
- gurobipy – Solver and optimization API
- xlsxwriter / openpyxl 


## 📄 License / Credits

This project is provided for educational and research purposes. You are free to use, modify, and share it under the MIT License. See the LICENSE file for details.
The code and models were developed as part of a study on flexible demand in the European day-ahead electricity market.
