# scenario_C_calibration_evaluation.py

"""
ICU-Causal-ML-Evaluation: Scenario C Implementation

==============================================================================
REPORT: Model Calibration and Evaluation (Scenario C)
==============================================================================

## Scenario C: Multi-Center Model Evaluation and Calibration

This script analyzes the performance metrics of a predictive model tested on a held-out hospital (Hospital X) to assess its external validity, focusing on Calibration-in-the-Large (CITL) Bias and Calibration Slope.

### Input Data (Hospital X Metrics):
| Metric | Result |
| :--- | :--- |
| Area Under the ROC Curve (AUC) | 0.85 |
| Calibration-in-the-Large (CITL) Bias | -0.10 |
| Calibration Slope | 0.70 |
| Number of Positive Cases (O) | 100 |

### Assumptions & Given Values:
* Total Number of Patients (N) = 1000
* Observed Rate = 0.1
* CITL Definition: $CITL = \text{Average Predicted Probability} - \text{Observed Rate}$

### Tasks:
1. Explain the clinical implication of the observed Calibration Slope (0.70).
2. Calculate the Average Predicted Probability.
3. State the interpretation of both metrics, providing calculation logic.
"""

import pandas as pd
import numpy as np
import os
from io import StringIO

OUTPUT_FILEPATH = 'data/scenario_C_results.csv'

def analyze_calibration_metrics():
    """
    Performs calculations for Scenario C to find the Average Predicted Probability 
    based on the CITL Bias and Observed Rate.
    Saves the numerical result and interpretations to a CSV file.
    """
    
    # Input Data and Assumptions
    CITL_BIAS = -0.10
    OBSERVED_RATE = 0.1 # This is 100 positive cases / 1000 total patients = 0.1
    N_TOTAL = 1000
    CALIBRATION_SLOPE = 0.70
    
    print("--- Scenario C: Calibration Analysis ---")
    print(f"CITL Bias (Given): {CITL_BIAS}")
    print(f"Observed Rate (O/N): {OBSERVED_RATE} (Calculated as 100/1000)")
    print(f"Calibration Slope (Given): {CALIBRATION_SLOPE}\n")

    # --- TASK 2: Calculate Average Predicted Probability ---
    
    # Formula Rearrangement:
    # Average Predicted Probability = CITL Bias + Observed Rate
    
    average_predicted_prob = CITL_BIAS + OBSERVED_RATE
    
    # --- TASK 1 & 3: Interpretation Summary ---
    
    interpretation_data = {
        'Metric': [
            '1. Calibration Slope',
            '2. Average Predicted Probability (Calculated)',
            '3. Clinical Implication (Slope 0.70)'
        ],
        'Result': [
            CALIBRATION_SLOPE, 
            average_predicted_prob, 
            'N/A'
        ],
        'Calculation/Interpretation Logic': [
            # Task 3: Interpretation of Calibration Slope
            "The ideal slope is 1.0. A slope of 0.70 (< 1.0) indicates **poor refinement** and **overly extreme predictions** (Over-fitting). The model is too confident in its predictions.",
            
            # Task 3: Interpretation of Avg. Predicted Prob. (Calculation Logic)
            f"Logic: Avg. Predicted Prob. = CITL Bias + Observed Rate. {CITL_BIAS} + {OBSERVED_RATE} = {average_predicted_prob:.2f}. A result of 0.0 means the model is perfectly calibrated *on average* (CITL=0), as the observed rate is also 0.1. *Note: This is an unusual outcome based on the given inputs.*",
            
            # Task 1: Clinical Implication
            "For individual patients, the model overestimates high risks (e.g., predicting 80% when true risk is 60%) and underestimates low risks. This lack of reliability compromises clinical decision-making based on specific probabilities."
        ]
    }
    
    results_df = pd.DataFrame(interpretation_data)
    
    print("--- Final Calculated Result & Interpretation Summary ---")
    print(results_df.to_markdown(index=False, floatfmt=".2f"))
    print("-" * 60)
    
    # ==========================================================================
    # SAVE NUMERICAL RESULTS TO FILE WITH METADATA
    # ==========================================================================
    
    # Create the metadata section 
    metadata = StringIO()
    metadata.write("# Results for Scenario C: Calibration Evaluation\n")
    metadata.write("# ------------------------------------------------------------------\n")
    metadata.write("# Task: Calculate Average Predicted Probability and provide interpretations.\n")
    metadata.write(f"# Input Values: CITL Bias={CITL_BIAS}, Observed Rate={OBSERVED_RATE}\n")
    metadata.write("# Date Generated: " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    metadata.write("# ------------------------------------------------------------------\n")
    
    os.makedirs(os.path.dirname(OUTPUT_FILEPATH), exist_ok=True)
    
    # Save the results (including interpretation)
    with open(OUTPUT_FILEPATH, 'w') as f:
        f.write(metadata.getvalue())
        results_df.to_csv(f, index=False)

    print(f"\n✅ Numerical results and interpretation saved to: {OUTPUT_FILEPATH} (Includes metadata header)")

# Execute the function
if __name__ == "__main__":
    analyze_calibration_metrics()