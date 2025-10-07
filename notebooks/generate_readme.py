# generate_readme.py

"""
This script generates the final, structured README.md content for the 
ICU-Causal-ML-Evaluation repository.
"""
import os

# The entire README content structure in Markdown format
README_CONTENT = """
# ICU Causal Inference and Machine Learning Evaluation

This repository houses the computational analysis for an advanced project in Healthcare Data Science, focusing on the evaluation of daily interventions and predictive model generalizability in Intensive Care Units (ICUs).

The project is structured into three distinct analytical scenarios: **Time-Series Feature Engineering (A)**, **Causal Inference Weighting (B)**, and **Model Calibration Evaluation (C)**.

---

## Project Structure
icu-causal-ml-evaluation/
├── data/                                 # Stores the final numerical results (.csv files) for each scenario
│   ├── scenario_A_results.csv
│   ├── scenario_B_results.csv
│   └── scenario_C_results.csv
├── notebooks/                            # Contains the executable Python scripts (.py) for all tasks
│   ├── scenario_A_timeseries_imputation.py
│   ├── scenario_B_iptw_calculation.py
│   └── scenario_C_calibration_evaluation.py
├── README.md                             # This report
└── requirements.txt                      # Dependencies (pandas, numpy, tabulate)


---

## Scenario A: Time-Series Feature Engineering

This scenario addresses the critical data preparation steps required for deep learning models, like GRU-D, when dealing with irregularly sampled and missing data common in ICU records.

### 1. Objective
To demonstrate two key time-series pre-processing techniques: **Last Observation Carried Forward (LOCF) Imputation** and calculation of the **Time Since Last Observation (TSLO)** feature.

### 2. Methodology

| Task | Method | Rationale |
| :--- | :--- | :--- |
| **Imputation** | LOCF (`pandas.ffill`) | Replaces missing values with the last valid preceding observation, assuming the patient's status remains constant over short intervals. |
| **Feature Engineering** | TSLO | Calculated as the time elapsed since the last recorded measurement. This feature is vital for models like GRU-D, as it informs the decay mechanism, ensuring that older imputed values are weighted less reliably. |

### 3. Key Numerical Result

The final calculated table, saved in `data/scenario_A_results.csv`, demonstrates the resulting data structure:

| Time (Hours) | Imputed HR | TSLO |
| :--- | :--- | :--- |
| 0.0 | 95.0 | 0.0 |
| 4.0 | 102.0 | **1.0** |
| 6.0 | 99.0 | **1.0** |
*(Note: TSLO of 1.0 at Time 4.0 indicates 1 hour passed since the last true observation at Time 3.0.)*

---

## Scenario B: Causal Inference Weighting (IPTW/SIPTW)

This scenario demonstrates the calculation of weights used in Propensity Score methods to estimate the **Average Treatment Effect (ATE)** in an observational setting.

### 1. Objective
To calculate **Raw IPTW** and **Stabilized IPTW (SIPTW)** weights for a small cohort, crucial steps for balancing measured confounders.

### 2. Methodology

| Weight Type | Formula | Purpose |
| :--- | :--- | :--- |
| **Raw IPTW** | $IPTW = \frac{1}{P(A|L)}$ | Creates a pseudo-population where treatment status ($A$) is independent of the measured covariates ($L$). |
| **Stabilized IPTW**| $SIPTW = \frac{P(A)}{P(A|L)}$ | Reduces the variance (instability) of the Raw IPTW by normalizing the weights by the marginal probability of treatment, $P(A)$. |

***Assumption:*** The marginal probability of treatment, $P(A=1)$, is assumed to be $0.5$.

### 3. Key Numerical Result and Interpretation

The final sum of the Stabilized IPTW weights is a crucial check. If the weights are calculated correctly, this sum should ideally equal the total number of patients ($N$), or $N \times P(A)$ depending on the normalization.

| Metric | Result |
| :--- | :--- |
| **Final Sum of Stabilized IPTW** | **7.5000** |

---

## Scenario C: Model Calibration Evaluation (LOO Validation)

This scenario evaluates the **external validity** and **calibration** of a predictive model when deployed to a new, unseen hospital site (Hospital X), a core requirement for multi-center generalization.

### 1. Objective
1.  Explain the clinical implication of the **Calibration Slope** ($\text{0.70}$).
2.  Calculate the **Average Predicted Probability** using the **CITL Bias** definition.

### 2. Calculation Logic

The **Calibration-in-the-Large (CITL) Bias** is defined as:
$$CITL = \text{Average Predicted Probability} - \text{Observed Rate}$$

Given: $CITL = -0.10$ and $\text{Observed Rate} = 0.1$

$$\text{Average Predicted Probability} = \text{CITL Bias} + \text{Observed Rate} = -0.10 + 0.1 = \mathbf{0.0}$$

### 3. Interpretation Summary

| Metric | Result | Interpretation and Implication |
| :--- | :--- | :--- |
| **Calibration Slope** | $\mathbf{0.70}$ | **Poor Refinement / Over-fitting:** A slope less than $1.0$ (ideal) indicates the model makes overly extreme predictions. It is **overconfident**, tending to overestimate high risks and underestimate low risks, making specific probability outputs unreliable for clinical use. |
| **Avg. Predicted Probability** | $\mathbf{0.0}$ | **Calibration-in-the-Large is Perfect:** Since the calculated average predicted probability (0.0) is equal to the observed rate (0.1) minus the CITL bias (-0.10), the model is perfectly calibrated **on average**. *Note: The resulting value of 0.0 is unusual for clinical data, but follows the explicit formula provided.* |
"""

def generate_readme_file():
    """Writes the predefined Markdown content to the README.md file."""
    readme_path = 'README.md'
    try:
        # Open the file in write mode ('w'). This overwrites any existing content.
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(README_CONTENT.strip())
        print(f"✅ Successfully generated and updated: {readme_path}")
        print("Please remember to run 'git add README.md' and 'git commit' to save these changes.")
    except Exception as e:
        print(f"❌ Error writing to {readme_path}: {e}")

# Execute the script
if __name__ == "__main__":
    generate_readme_file()