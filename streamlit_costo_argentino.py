# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 10:47:04 2025

@author: pablo
"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Precios y Costo Argentino")

# Input Fields
Costo_Argentino = st.number_input("Costo Argentino", value=0.0, step=0.01)
P_t = 0.8  # Fixed value in the original code
productividad_t = st.number_input("Productividad (Tradeable, t)", value=1.0, step=0.01)
productividad_nt = st.number_input("Productividad (Non-Tradeable, nt)", value=1.0, step=0.01)

# Calculate matrices
cost_matrix = np.array([
    [0.4, 0.1, 0.3 / productividad_t],
    [0, 0.1, 0.1],
    [0.3, 0.1, 0.6 / productividad_nt],
])
output_matrix = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [0, 1, 0],
])
resid_vector = np.array([- P_t,
                         Costo_Argentino + P_t,
                         Costo_Argentino*0.5])
net_matrix = output_matrix - cost_matrix
prices = np.linalg.inv(net_matrix) @ resid_vector

# Extract results
P_t_n, P_nt, W = prices.round(3)
Salario_real = round(W / (0.5 * P_t_n + 0.5 * P_nt), 3)
Tipo_de_cambio_real = 1 / (0.5 * P_t_n + 0.5 * P_nt)

# Plot results
fig, ax = plt.subplots()
categories = ["Transables", "Transables Nacionalizados", "No Transables", "Salario", "Salario_real", "Tipo de cambio real"]
values = [P_t, P_t_n, P_nt, W, Salario_real, Tipo_de_cambio_real]


ax.bar(categories, values, color=["orange", "blue", "green", "red", "purple", "gray"])
ax.set_ylabel("Valores")
ax.set_title("Precios y Costo Argentino")
ax.set_ylim(round(min(values)*5,0)/5-0.2, max(values) * 1.2)  # Add some padding for better visualization

# Rotate x-axis labels
plt.xticks(rotation=45)

# Show plot in Streamlit
st.pyplot(fig)

# Display results
st.write("### Results")
st.write(f"**Transables nacionalizados:** {P_t_n}")
st.write(f"**No Transables:** {P_nt}")
st.write(f"**Salario Nominal:** {W}")
st.write(f"**Salario Real:** {Salario_real}")
st.write(f"**Tipo de cambio real:** {Tipo_de_cambio_real}")
