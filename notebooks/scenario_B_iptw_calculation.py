# scenario_B_iptw_calculation.py

"""
ICU-Causal-ML-Evaluation: Scenario B Implementation

==============================================================================
REPORT: Inverse Probability of Treatment Weighting (IPTW) Calculation (Scenario B)
==============================================================================

## Scenario B: Causal Inference using Propensity Score Weighting (IPTW/SIPTW)

This script calculates the weights necessary for Inverse Probability of Treatment Weighting (IPTW). IPTW is a core method in causal inference used to create a pseudo-population where treatment assignment is independent of measured confounders.

### Problem Description
We analyze a small, cross-sectional cohort with observed treatment status (A) and estimated propensity scores (g).

Input Data:
| Patient ID | Treatment (A, 1=Yes, 0=No) | Estimated Propensity (g) |
|------------|----------------------------|--------------------------|
| 1          | 1                          | 0.8                      |
| 2          | 1                          | 0.4                      |
| 3          | 0                          | 0.9                      |
| 4          | 0                          | 0.2                      |

### Tasks:
1. Calculate the **Raw IPTW** for each patient.
2. Calculate the **Stabilized IPTW (SIPTW)** for each patient.
3. Calculate the **Sum of SIPTW** for the entire cohort.

### Methodological Formulas
* **Raw IPTW:** $IPTW = 1 / P(A|L)$ where $P(A|L)$ is the conditional probability of receiving the observed treatment.
* **Stabilized IPTW (SIPTW):** $SIPTW = P(A) / P(A|L)$
* **Assumption:** The marginal probability of treatment $P(A=1)$ is **0.5**.
"""

import pandas as pd
import numpy as np
import os
from io import StringIO

OUTPUT_FILEPATH = 'data/scenario_B_results.csv'
P_A1 = 0.5  # Assumed Marginal probability of treatment P(A=1)

def calculate_iptw_weights():
    """
    Calculates Raw and Stabilized IPTW weights based on patient data and 
    saves the results to a CSV file including metadata.
    """
    # 1. Initialize the data
    data = {
        'Patient ID': [1, 2, 3, 4],
        'A (Treatment)': [1, 1, 0, 0],
        'g (Propensity Score)': [0.8, 0.4, 0.9, 0.2]
    }
    df = pd.DataFrame(data)

    print("--- Scenario B: Initial Data ---")
    print(df.to_markdown(index=False))
    print(f"Assumption: Marginal P(A=1) = {P_A1}")
    print("-" * 60)

    # --- Step 1: Calculate the conditional probability P(A|L) ---
    # P(A|L) = g if A=1, or (1-g) if A=0
    df['P(A|L)'] = np.where(df['A (Treatment)'] == 1, 
                            df['g (Propensity Score)'], 
                            1 - df['g (Propensity Score)'])
    
    # --- Task 1: Calculate Raw IPTW ---
    df['Raw IPTW'] = 1 / df['P(A|L)']

    # --- Step 2: Calculate the marginal probability P(A) ---
    # P(A) is 0.5 if A=1, or 1 - 0.5 = 0.5 if A=0
    df['P(A)'] = np.where(df['A (Treatment)'] == 1, P_A1, 1 - P_A1)

    # --- Task 2: Calculate Stabilized IPTW (SIPTW) ---
    df['Stabilized IPTW'] = df['P(A)'] / df['P(A|L)']

    # --- Task 3: Calculate the Sum of Stabilized IPTW ---
    sum_siptw = df['Stabilized IPTW'].sum()

    # --- Present Results ---
    results_table = df[['Patient ID', 'A (Treatment)', 'g (Propensity Score)', 'Raw IPTW', 'Stabilized IPTW']]

    print("--- IPTW and SIPTW Results per Patient ---")
    print(results_table.to_markdown(index=False, floatfmt=".4f"))
    print("-" * 60)
    print(f"✅ Final Sum of Stabilized Weights (Cohort Sum of SIPTW): {sum_siptw:.4f}")
    print("-" * 60)

    # ==========================================================================
    # SAVE NUMERICAL RESULTS TO FILE WITH METADATA
    # ==========================================================================
    
    # Create the metadata section (documentation for the results file)
    metadata = StringIO()
    metadata.write("# Results for Scenario B: IPTW and Stabilized IPTW Calculation\n")
    metadata.write("# ------------------------------------------------------------------\n")
    metadata.write("# Task: Calculate Raw IPTW, Stabilized IPTW, and the Sum of SIPTW.\n")
    metadata.write(f"# ASSUMPTION: Marginal Probability P(A=1) = {P_A1}\n")
    metadata.write("# Columns: Raw IPTW and Stabilized IPTW per patient.\n")
    metadata.write("# Date Generated: " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    metadata.write("# ------------------------------------------------------------------\n")
    
    # Ensure the 'data' directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILEPATH), exist_ok=True)

    # Write the metadata and the actual data to the file
    with open(OUTPUT_FILEPATH, 'w') as f:
        # Write the header/metadata
        f.write(metadata.getvalue())
        
        # Write the actual data
        results_table.to_csv(f, index=False, float_format='%.4f')

    print(f"\n✅ Numerical results successfully saved to: {OUTPUT_FILEPATH} (Includes metadata header)")

# Execute the function when the script is run directly
if __name__ == "__main__":
    calculate_iptw_weights()