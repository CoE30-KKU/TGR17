# Hydrological Modeling using MATLAB: A Detailed Overview

This document provides a comprehensive overview of the hydrological model developed by the See-It 2023 MATLAB team. This team, comprising Metee Yingyongwatthanakit and Amonrit Tangludee, has effectively utilized MATLAB for simulating complex hydrological processes.

## Team Members

1. [Metee Yingyongwatthanakit](https://github.com/TBBdlz)
2. [Amonrit Tangludee](https://github.com/amonrit)

## Introduction to the Hydrological Model

In the context of TGR#17, Prof. X provided extensive training on MATLAB's application in hydrological modeling. The primary focus was on a critical equation that forms the basis of this model:

$$
Q_{S1} + Q_{S2} = f Q_{S3}
$$

Here, \(Q_{S1}\) represents surface runoff, \(Q_{S2}\) indicates subsurface runoff, and \(Q_{S3}\) is the total runoff. The term \(f\) denotes the runoff coefficient, which is influenced by soil type, land use, and the antecedent moisture condition.

## Day 1: Laying the Foundations

The initial phase involved understanding the theoretical underpinnings of the model. This understanding was immediately put into practice by:

- Defining model variables and parameters.
- Employing the least square method for fitting the model parameters.
- Utilizing polynomial regression for further refinement.
- Incorporating neural networks to enhance parameter fitting accuracy.

## Day 2: Exploring Image Processing

The team's focus shifted to MATLAB's image processing capabilities, involving:

- Basic operations like reading and converting images to grayscale.
- Advanced techniques like constructing RGB images and scaling.
- A challenging task: using the MATLAB mapping toolbox to map a dam.

## Integration and Problem Solving

The project culminated in a series of tasks designed to test our practical and theoretical skills:

1. Retrieve data from a RESTful API (fastAPI).
2. Curve fitting for QH at stations 1 and 3.
3. Calculate the discharge rate at station 1.
4. Determine the water height at station 3.
5. Communicate the height data of station 3 back to the RESTful API.
6. Predict the water height for the next five days at station 1.

The final implementation involved crafting HTTP request codes for server communication via FastAPI and utilizing neural networks for predictive modeling of QH1 and QH3 data.

### Individual Contributions

- **Metee Yingyongwatthanakit**: Spearheaded the design and implementation of neural networks for predicting discharge rates and water heights at the respective stations.
- **Amonrit Tangludee**: Focused on developing the HTTP request codes essential for server (FastAPI) communication.

This project not only showcases our technical proficiency in MATLAB but also our ability to tackle real-world hydrological challenges through computational modeling.
