## FibreBarrier-ML
FibreBarrier-ML is a hybrid materials engineering + machine learning project that models the Water Vapour Transmission Rate (WVTR) of coated fibre-based packaging materials 

This project demonstrates how physics-based assumptions can be combined with data-driven models to accelerate barrier coating development.

## 1. Project Motivation

Traditional WVTR testing requires specialized chambers and long conditioning times.
With FibreBarrier-ML, barrier engineers can:

- Perform rapid virtual WVTR predictions

- Explore design parameters (T, RH, coating weight)

-  Understand sensitivity of WVTR to thickness and environmental conditions

- Use ML as a surrogate for fast screening

## 2. Why This Project Matters

This project demonstrates an end-to-end materials informatics workflow:

- Understanding the physics of moisture diffusion in coatings  
- Identifying governing variables  
- Building a physics-inspired surrogate model  
- Generating a high-quality synthetic dataset  
- Training ML models to replicate physical behaviour  

The project is easily extendable to multilayer coatings, different polymers, Arrhenius-based permeability modelling, sorption isotherms, or coupling with oxygen transmission rate (OTR) predictions.

## 3. Scientific Background

### 3.1. WVTR and Moisture Transport Physics  
Water vapour transmission through polymer coatings is fundamentally a diffusion process.  
In packaging applications, moisture tends to move from a high-humidity environment toward a lower-humidity region through the coating.  

Three main factors govern this behaviour:

- **Diffusivity**: how easily water molecules move through the polymer  
- **Solubility / sorption**: how strongly water molecules interact with the coating  
- **Thickness**: thicker coatings create a longer path, reducing moisture flow  

In practical terms:  
**thicker coatings → slower vapour transport → lower WVTR.**

This inverse relationship is widely validated in packaging science and is routinely used in the design of barrier films and multilayer structures.

---

### 3.2. Temperature Dependence  
Polymer permeability increases with temperature.  
As temperature rises:

- Molecular motion increases  
- Vapour pressure increases  
- Diffusion becomes faster  

This causes **WVTR to rise significantly at higher temperatures**, a behaviour confirmed experimentally across many polymeric coatings.  
Our synthetic model incorporates this trend through a temperature scaling factor.

---

### 3.3. Humidity / Mixing Ratio Effect  
Relative humidity alone is not always the best predictor of moisture loading in air, so the literature introduces the concept of a “mixing ratio,” which quantifies the actual water content in the atmosphere.  

Experiments show a nearly linear connection between mixing ratio and WVTR:  
**higher humidity → higher moisture load → higher WVTR.**

This relationship is preserved in our synthetic generator.

---

### 3.4. Coating Weight and Thickness  
Coating weight (g/m²) is converted to an approximate film thickness using an assumed polymer density.  
This allows the model to simulate how thicker or thinner barriers influence WVTR performance.  

**Heavier coating → thicker barrier → lower WVTR.**

This is one of the strongest and most predictable effects in moisture barrier engineering.

---

## 4. Physics-Informed WVTR Model -  
The synthetic WVTR model used in this project combines:

- humidity-driven moisture loading  
- temperature effects  
- coating thickness effects  
- a global scaling constant to keep values realistic  
- small random noise to simulate experimental scatter  

This results in WVTR values that behave very similarly to actual measurements reported in packaging literature.

The goal is not to recreate exact laboratory physics, but to build a **scientifically meaningful approximation** that generates realistic training data for machine learning.

---

## 5. Dataset Generation

The notebook **01_generate_data.ipynb**:

1. Samples realistic environmental and material parameters  
   - Temperature: 20–60°C  
   - Relative Humidity: 40–95%  
   - Coating Weight: 10–60 g/m²  

2. Computes physically motivated quantities (humidity load, thickness, etc.)

3. Uses the simplified physics model to compute WVTR

4. Saves the generated dataset to:

data/synthetic_wvtr.csv

A dataset of **3000 samples** is produced by default, but this can be easily increased.

---

   ## 6. Machine Learning Model

The notebook **02_train_ml_model.ipynb** trains a regression model (Random Forest, optionally XGBoost) to learn the mapping between input parameters and WVTR.

**Features used:**

- Temperature  
- Relative humidity  
- Coating weight  

**Target:**

- WVTR  

Expected performance on this dataset is extremely high because the underlying physics is well-defined and consistent:

- R² typically between **0.97 and 0.99**  
- Very low prediction error  

Feature importance analysis usually reveals:

1. Humidity (or its proxy, mixing ratio)  
2. Coating weight / thickness  
3. Temperature  

This ordering matches real experimental trends.


## 7. Results
True vs Predicted WVTR

![WVTR Scatter Plot](figures/wvtr_scatter.png)


The strong diagonal trend indicates:

- The ML model successfully captures WVTR behaviour

- Predictions generalize well across the parameter space

- The surrogate can replace slow physical simulations for early-stage analysis


## 8. Key Features

✓ Physics-inspired synthetic dataset

✓ Full ML training pipeline

✓ High-accuracy Random Forest surrogate

✓ Clean, modular code structure

✓ Reproducible Jupyter notebooks

✓ Ready for research or industrial prototyping

## 9. Future Work

Multilayer barrier coating models

Integration with FEM moisture transport simulations

Parameter optimisation (Bayesian search)

Temperature-dependent diffusivity modelling

Transfer learning using real experimental WVTR datasets
