import pandas as pd
import time
# Read input data from Excel file
df = pd.read_excel(r'C:\PYTHON\Inputs\UnitCflexible.xlsx', header=0, sheet_name='Sheet1')
# Start the timer
start_time = time.time()
from gurobipy import *
import gurobipy as gp
model = gp.Model("Unit Commitment with demand flexibility")

# Time periods
time_periods = list(range(1, 25))
# Number of generators participating in the market
generator_numbers = df.iloc[2:9, 0].tolist()
generator_mapping = {t: generator_numbers for t in time_periods}
# Number of demands participating in the market
demand_number = df.iloc[11, 0]
demand_number_list = [demand_number]
# Number of offers per generator
offers_per_generator = 5
# Number of offers per demand
offers_per_demand = 1
# Dictionary to hold the number of offers for each generator
num_offers = {generator: offers_per_generator for generator in generator_numbers}

# PARAMETER'S VALUES
# Simple Offering with demand flexibility parameters
Pdmax = df.loc[11, 'Unnamed: 1':'Unnamed: 24'].tolist()
Bd = df.loc[13, 'Unnamed: 1':'Unnamed: 24'].tolist()
flexibility_factor = df.loc[11, 'Unnamed: 26']
Bd_shaway = df.loc[15, 'Unnamed: 1':'Unnamed: 24'].tolist()
Bd_shtowards = df.loc[16, 'Unnamed: 1':'Unnamed: 24'].tolist()
Pgmin = df.loc[2:8, 'Unnamed: 2'].tolist()

Pgmax = df.loc[2:8, 'Unnamed: 1'].tolist()
Cgb1 = df.loc[2:8, 'Unnamed: 3'].tolist()
Cgb2 = df.loc[2:8, 'Unnamed: 4'].tolist()
Cgb3 = df.loc[2:8, 'Unnamed: 5'].tolist()
Cgb4 = df.loc[2:8, 'Unnamed: 6'].tolist()
Cgb5 = df.loc[2:8, 'Unnamed: 7'].tolist()


# Setting Parameters into dictionaries
Cgb = {}
for i, generator in enumerate(generator_numbers, start=1):
    Cgb[generator] = {
        1: Cgb1[i-1],
        2: Cgb2[i-1],
        3: Cgb3[i-1],
        4: Cgb4[i-1],
        5: Cgb5[i-1]
    }
Cg_b = {}
for g in generator_numbers:
    for b in range(1, offers_per_generator + 1):
        for t in time_periods:
            Cg_b[g, b, t] = Cgb[g][b]
Pg_max = {}
for g in generator_numbers:
    for b in range(1, offers_per_generator + 1):
        for t in time_periods:
            Pg_max[g, b, t] = Pgmax[g-1]
Pg_min = {}
# Populate the G_max dictionary
for g in generator_numbers:
    Pg_min[g] = Pgmin[g-1]

Pd_max = {}
for d in demand_number_list:
    for b in range(1, offers_per_demand + 1):
        for t in time_periods:
            Pd_max[d, b, t] = Pdmax[t-1]
B_d = {}
for d in demand_number_list:
    for b in range(1, offers_per_demand + 1):
        for t in time_periods:
            B_d[d, b, t] = Bd[t-1]
a_d = {}
for d in demand_number_list:
    for b in range(1, offers_per_demand + 1):
        a_d[d, b] = flexibility_factor
Bd_sh_away = {}
for d in demand_number_list:
    for b in range(1, offers_per_demand + 1):
        for t in time_periods:
            Bd_sh_away[d, b, t] = Bd_shaway[t-1]
Bd_sh_towards = {}
for d in demand_number_list:
    for b in range(1, offers_per_demand + 1):
        for t in time_periods:
            Bd_sh_towards[d, b, t] = Bd_shtowards[t-1]

# DEFINE THE DECISION VARIABLES
# Unit commitment Parameters
TgUP = df.loc[2:8, 'Unnamed: 11'].tolist()
TgDN = df.loc[2:8, 'Unnamed: 12'].tolist()
CgUP = df.loc[2:8, 'Unnamed: 9'].tolist()
CgDN = df.loc[2:8, 'Unnamed: 10'].tolist()
Ug0 = df.loc[2:8, 'Unnamed: 13'].tolist()
RgUP = df.loc[2:8, 'Unnamed: 15'].tolist()
RgDN = df.loc[2:8, 'Unnamed: 16'].tolist()
CgNL = df.loc[2:8, 'Unnamed: 8'].tolist()
Pg0 = df.loc[2:8, 'Unnamed: 14'].tolist()
Cg_NL = {}
for g in generator_numbers:
    for t in time_periods:
        Cg_NL[g,t]= CgNL[g-1]
# DEFINE THE DECISION VARIABLES
# POWER OF GENERATION
p_g = {}
for t in range(1, len(time_periods) + 1):
    for idx, g in enumerate(generator_numbers, start=1):  # Loop over generators
        for b in range(1, offers_per_generator + 1):  # Loop over offers
            p_g[g, b, t] = model.addVar(vtype=GRB.CONTINUOUS,  name=f"p_g_{g}_{t}_{b}")
# BINARIES
u_g = {}
for t in range(1, len(time_periods) + 1):
    for idx, g in enumerate(generator_numbers, start=1):
        u_g[g, t] = model.addVar(vtype=GRB.BINARY, name=f"u_g_{g}_{t}")
# POWER OF FLEXIBLE DEMAND
pd_b = {}
for t in range(1, len(time_periods) + 1):
    for idx, d in enumerate(range(1, demand_number + 1), start=1):  # Loop over demand nodes
        for b in range(1, offers_per_demand + 1):  # Loop over offers
            pd_b[d, b, t] = model.addVar(vtype=GRB.CONTINUOUS,  name=f"p_d_baseline{d}_{t}_{b}")
pd_sh_away = {}
for t in range(1, len(time_periods) + 1):
    for idx, d in enumerate(range(1, demand_number + 1), start=1):  # Loop over demand nodes
        for b in range(1, offers_per_demand + 1):  # Loop over offers
            pd_sh_away[d, b, t] = model.addVar(vtype=GRB.CONTINUOUS,  name=f"pd_shift_away{d}_{t}_{b}")
pd_sh_towards = {}
for t in range(1, len(time_periods) + 1):
    for idx, d in enumerate(range(1, demand_number + 1), start=1):  # Loop over demand nodes
        for b in range(1, offers_per_demand + 1):  # Loop over offers
            pd_sh_towards[d, b, t] = model.addVar(vtype=GRB.CONTINUOUS,  name=f"pd_shift_towards{d}_{t}_{b}")
# Start Up COST Decision Variable
cg_UP = {}
for t in range(1, len(time_periods) + 1):
    for idx, g in enumerate(generator_numbers, start=1):
        cg_UP[g, t] = model.addVar(vtype=GRB.CONTINUOUS, name=f"cgUP[{g},{t}]")
# Shut Down COST Decision Variable
cg_DN = {}
for t in range(1, len(time_periods) + 1):
    for idx, g in enumerate(generator_numbers, start=1):
        cg_DN[g, t] = model.addVar(vtype=GRB.CONTINUOUS,  name=f"cgDN[{g},{t}]")

# Define the constraints dictionary
constraints = {}
# Constraint 1: Power Balance Constraint
for t in range(1, len(time_periods) + 1):
    constraint_name1 = f"Power_Balance_{t}"
    constraint_expr1 = quicksum(p_g[g, b, t] for g in generator_numbers for b in range(1, offers_per_generator + 1)) -\
                       quicksum(pd_b[d, b, t] + pd_sh_towards[d, b, t] - pd_sh_away[d, b, t] for d in range(1, demand_number + 1) for b in range(1, offers_per_demand + 1))
    constraints[constraint_name1] = model.addConstr(constraint_expr1 == 0, name=constraint_name1)
# Constraint 2: Power demand limits
constraint_counter2 = 0
for t in range(1, len(time_periods) + 1):
    for d in demand_number_list:
        for b in range(1, offers_per_demand + 1):
            # Lower limit constraint
            constraint_name2a = f"Power_Demand_Limit_lower{d}_{b}_{t}"
            constraint_expression2 = f"{pd_b[d,b,t]} >= 0"
            constraints[constraint_name2a] = model.addConstr(pd_b[d, b, t] >= 0, name=constraint_name2a)
            # Upper limit constraint
            constraint_name2b = f"Power_Demand_Limit_Upper_{d}_{b}_{t}"
            constraint_expression3 = f"{pd_b[d,b,t]} <= {Pd_max[d, b, t]}"
            constraints[constraint_name2b] = model.addConstr(pd_b[d, b, t] <= Pd_max[d, b, t], name=constraint_name2b)
# Constraint 3: Power Generation Upper and Lower Limits
for t in range(1, len(time_periods) + 1):
    for g in generator_numbers:
        for b in range(1, offers_per_generator + 1):
            # Lower limit constraint
            constraint3_name_lower = f"Power_Gen_Limit_Lower_{g}_{b}_{t}"
            constraint_expression_lower = p_g[g, b, t] >= 0
            constraints[constraint3_name_lower] = model.addConstr(constraint_expression_lower,name=constraint3_name_lower)
            # Upper limit constraint
            constraint3_name_upper = f"Power_Gen_Limit_Upper_{g}_{b}_{t}"
            constraint_expression_upper = p_g[g, b, t] <= Pg_max[g, b, t] * u_g[g, t]
            constraints[constraint3_name_upper] = model.addConstr(constraint_expression_upper,name=constraint3_name_upper)
# Constraint 4 : Minimum Stable Generation
constraint_counter4 = 0
for t in range(1, len(time_periods) + 1):
    for g in generator_numbers:
        constraint_name4 = f"Power_Gen_Lower_Bound_{g}_{b}_{t}"
        constraint_expression4 = Pg_min[g] * u_g[g, t] <= quicksum(p_g[g, b, t] for b in range(1, offers_per_generator + 1))
        constraints[constraint_name4] = model.addConstr(constraint_expression4, name=constraint_name4)
# Constraint 5: Limit of Shifting Away Quantity Constraint
for t in range(1, 25):
    for d in demand_number_list:
        for b in range(1, offers_per_demand + 1):
            # Lower bound constraint
            constraint_name_sh_away_lower = f"Flexibility_SH_AWAY_Lower_{d}_{b}_{t}"
            constraint_expression_sh_away_lower = pd_sh_away[d, b, t] >= 0
            constraints[constraint_name_sh_away_lower] = model.addConstr(constraint_expression_sh_away_lower, name=constraint_name_sh_away_lower)
            # Upper bound constraint
            constraint_name_sh_away_upper = f"Flexibility_SH_AWAY_Upper_{d}_{b}_{t}"
            constraint_expression_sh_away_upper = pd_sh_away[d, b, t] <= a_d[d, b] * pd_b[d, b, t]
            constraints[constraint_name_sh_away_upper] = model.addConstr(constraint_expression_sh_away_upper, name=constraint_name_sh_away_upper)
# Constraint 6: Limit of Shifting Towards Quantity Constraint
constraint_counter6 = 0
for t in range(1, 25):
    for d in demand_number_list:
        for b in range(1, offers_per_demand + 1):
            # Lower bound constraint
            constraint_name_sh_towards_lower = f"Flexibility_SH_TOWARDS_Lower_{d}_{b}_{t}"
            constraint_expression_sh_towards_lower = pd_sh_towards[d, b, t] >= 0
            constraints[constraint_name_sh_towards_lower] = model.addConstr(constraint_expression_sh_towards_lower, name=constraint_name_sh_towards_lower)
            # Upper bound constraint
            constraint_name_sh_towards_upper = f"Flexibility_SH_TOWARDS_Upper_{d}_{b}_{t}"
            constraint_expression_sh_towards_upper = pd_sh_towards[d, b, t] <= a_d[d, b] * pd_b[d, b, t]
            constraints[constraint_name_sh_towards_upper] = model.addConstr(constraint_expression_sh_towards_upper, name=constraint_name_sh_towards_upper)

# Constraint 7: Energy Neutrality
for d in demand_number_list:
    for b in range(1, offers_per_demand + 1):
        constraint_name7 = f"Energy_Balance_{d}"
        constraint_expr7 = quicksum(-pd_sh_away[d, b, t] + pd_sh_towards[d, b, t]for t in range(1, len(time_periods)+1))
        constraints[constraint_name7] = model.addConstr(constraint_expr7 == 0, name=constraint_name7)
# Constraint 8: Ramp Up Rates
for t in range(1, len(time_periods) + 1):
    for g in generator_numbers:
        if t - 1 > 0:
            constraint_name8 = f"Ramp_Up_Rates_{g}_{t}"
            constraint_expr8 = quicksum(p_g[g, b, t] for b in range(1, offers_per_generator + 1)) - quicksum(p_g[g, b, t-1] for b in range(1, offers_per_generator + 1)) - RgUP[g-1]
            constraints[constraint_name8] = model.addConstr(constraint_expr8 <= 0, name=constraint_name8)
        else:
            constraint_name8 = f"Ramp_Up_Rates_{g}_{t}"
            constraint_expr8 = quicksum(p_g[g, b, t] for b in range(1, offers_per_generator + 1)) - Pg0[g-1] - RgUP[g-1]
            constraints[constraint_name8] = model.addConstr(constraint_expr8 <= 0, name=constraint_name8)
# Constraint 9: Ramp Down Rates
for t in range(1, len(time_periods) + 1):
    for g in generator_numbers:
        if t - 1 > 0:
            constraint_name9 = f"Ramp_Down_Rates_{g}_{t}"
            constraint_expr9 = quicksum(p_g[g, b, t-1] for b in range(1, offers_per_generator + 1)) - quicksum(p_g[g, b, t] for b in range(1, offers_per_generator + 1)) - RgDN[g-1]
            constraints[constraint_name9] = model.addConstr(constraint_expr9 <= 0, name=constraint_name9)
        else:
            constraint_name9 = f"Ramp_Down_Rates_{g}_{t}"
            constraint_expr9 = Pg0[g-1] - quicksum(p_g[g, b, t] for b in range(1, offers_per_generator + 1)) - RgDN[g-1]
            constraints[constraint_name9] = model.addConstr(constraint_expr9 <= 0, name=constraint_name9)

# Constraint 10: Startup Cost Non-negativity
for t in range(1, len(time_periods) + 1):
    for g in generator_numbers:
        constraint_name10 = f"Startup_Cost_Nonnegativity_UP_{g}_{t}"
        constraint_expression10 = cg_UP[g, t] >= 0
        constraints[constraint_name10] = model.addConstr(constraint_expression10, name=constraint_name10)
# Constraint 11: Startup Cost Lower Bound
for t in range(1, len(time_periods) + 1):
    for g in generator_numbers:
        if t - 1 > 0:
            constraint_name11 = f"Startup_Cost_Lower_Bound_{g}_{t}"
            constraint_expr11 = (u_g[g, t] - u_g[g, t - 1]) * CgUP[g - 1]
            constraints[constraint_name11] = model.addConstr(cg_UP[g, t] >= constraint_expr11, name=constraint_name11)
        else:
            constraint_name11 = f"Startup_Cost_Lower_Bound_{g}_{t}"
            constraint_expr11 = (u_g[g, t] - Ug0[g - 1]) * CgUP[g - 1]
            constraints[constraint_name11] = model.addConstr(cg_UP[g, t] >= constraint_expr11, name=constraint_name11)
# Constraint 12: Shut Down Cost Non-negativity
for t in range(1, len(time_periods) + 1):
    for g in generator_numbers:
        constraint_name12 = f"SHUT_DOWN_COST_Nonnegativity_UP_{g}_{t}"
        constraint_expression7 = cg_DN[g, t] >= 0
        constraints[constraint_name12] = model.addConstr(constraint_expression7, name=constraint_name12)
# Constraint 13: Shut Down Cost Lower Bound
for t in range(1, len(time_periods) + 1):
    for g in generator_numbers:
        if t - 1 > 0:
            constraint_name13 = f"ShutDown_Cost_Lower_Bound_{g}_{t}"
            constraint_expr13 = (u_g[g, t] - u_g[g, t - 1]) * (-CgDN[g - 1])
            constraints[constraint_name13] = model.addConstr(cg_DN[g, t] >= constraint_expr13, name=constraint_name13)
        else:
            constraint_name13 = f"ShutDown_Cost_Lower_Bound_{g}_{t}"
            constraint_expr13 = (u_g[g, t] - Ug0[g - 1]) * (- CgDN[g - 1])
            constraints[constraint_name13] = model.addConstr(cg_DN[g, t] >= constraint_expr13, name=constraint_name13)
# Constraint 14: Constraint for Minimum UpTime
for g in generator_numbers:
    for t in range(1, len(time_periods) - TgUP[g-1] + 2):
        if t - 1 > 0:
            constraint_name14 = f"Minimum_UpTime_Constraint_{g}_{t}_a"
            constraint_expr14 = quicksum(u_g[g, r] for r in range(t, t + TgUP[g-1])) - TgUP[g-1] * (u_g[g, t] - u_g[g, t - 1])
            constraints[constraint_name14] = model.addConstr(constraint_expr14 >= 0, name=constraint_name14)
        else:
            constraint_name14 = f"Minimum_UpTime_Constraint_{g}_{t}_b"
            constraint_expr14 = quicksum(u_g[g, r] for r in range(t, t + TgUP[g-1])) - TgUP[g-1] * (u_g[g, t] - Ug0[g-1])
            constraints[constraint_name14] = model.addConstr(constraint_expr14 >= 0, name=constraint_name14)
# Constraint 15: Constraint for Minimum DownTime
for g in generator_numbers:
    for t in range(1, len(time_periods) - TgDN[g - 1] + 2):
        if t - 1 > 0:
            constraint_name15 = f"Minimum_DownTime_Constraint_{g}_{t}_a"
            constraint_expr15 = quicksum(1 - u_g[g, r] for r in range(t, t + TgDN[g - 1])) + TgDN[g - 1] * (u_g[g, t] - u_g[g, t - 1])
            constraints[constraint_name15] = model.addConstr(constraint_expr15 >= 0, name=constraint_name15)
        else:
            constraint_name15 = f"Minimum_DownTime_Constraint_{g}_{t}_b"
            constraint_expr15 = quicksum(1 - u_g[g, r] for r in range(t, t + TgDN[g - 1])) + TgDN[g - 1] * (
                        u_g[g, t] - Ug0[g - 1])
            constraints[constraint_name15] = model.addConstr(constraint_expr15 >= 0, name=constraint_name15)
# Constraint 16: Must run Constraint
for g in generator_numbers:
    for t in range(len(time_periods) - TgUP[g - 1] + 2, len(time_periods) + 1):
        if t - 1 > 0:
            constraint_name16 = f"Must_Run_Constraint_{g}_{t}_a"
            constraint_expr16 = quicksum(u_g[g, r] - (u_g[g, t] - u_g[g, t - 1]) for r in range(t, len(time_periods) + 1))
            constraints[constraint_name16] = model.addConstr(constraint_expr16 >= 0, name=constraint_name16)
        else:
            constraint_name16 = f"Must_Run_Constraint_{g}_{t}_b"
            constraint_expr16 = quicksum(u_g[g, r] - (u_g[g, t] - Ug0[g - 1]) for r in range(t, len(time_periods) + 1))
            constraints[constraint_name16] = model.addConstr(constraint_expr16 >= 0, name=constraint_name16)
# Constraint 17: Must stop Constraint
for g in generator_numbers:
    for t in range(len(time_periods) - TgDN[g - 1] + 2, len(time_periods) + 1):
        if t - 1 > 0:
            constraint_name17 = f"Must_Stop_Constraint_{g}_{t}_a"
            constraint_expr17 = quicksum(1 - u_g[g, r] - (u_g[g, t - 1] - u_g[g, t]) for r in range(t, len(time_periods) + 1))
            constraints[constraint_name17] = model.addConstr(constraint_expr17 >= 0, name=constraint_name17)
        else:
            constraint_name17 = f"Must_Stop_Constraint_{g}_{t}_b"
            constraint_expr17 = quicksum(1 - u_g[g, r] - (Ug0[g - 1] - u_g[g, t]) for r in range(t, len(time_periods) + 1))
            constraints[constraint_name17] = model.addConstr(constraint_expr17 >= 0, name=constraint_name17)

# OBJECTIVE FUNCTION
SW_expr = (
    quicksum(B_d[d, b, t] * pd_b[d, b, t] for d in demand_number_list for t in range(1, len(time_periods) + 1) for b in range(1, offers_per_demand + 1)) -\
    quicksum(Cg_b[g, b, t] * p_g[g, b, t] for g in generator_numbers for t in range(1, len(time_periods) + 1) for b in range(1, offers_per_generator + 1)) -\
    quicksum(Bd_sh_away[d, b, t] * pd_sh_away[d, b, t] for d in demand_number_list for t in range(1, len(time_periods)+1) for b in range(1, offers_per_demand + 1)) -\
    quicksum(Bd_sh_towards[d, b, t] * pd_sh_towards[d, b, t] for d in demand_number_list for t in range(1, len(time_periods)+1) for b in range(1, offers_per_demand + 1))-
    quicksum(cg_UP[g, t] for g in generator_numbers for t in range(1, len(time_periods) + 1)) -
    quicksum(cg_DN[g, t] for g in generator_numbers for t in range(1, len(time_periods) + 1)) -
    quicksum(Cg_NL[g, t]* u_g[g, t] for g in generator_numbers for t in range(1, len(time_periods) + 1)))

model.setObjective(SW_expr, GRB.MAXIMIZE)
# Optimize the model
model.optimize()