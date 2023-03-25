import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import pandas as pd

st.set_page_config(initial_sidebar_state='expanded')

st.title('Mohrs Circle')
st.markdown('This is a web app to explore Mohrs circle')


st.sidebar.title('Inputs')

Unit = st.sidebar.selectbox('Unit',('(MPa)', '(psi)'))
sigma_x=st.sidebar.number_input("$\sigma_x$ "+Unit,-250,250,value=200)
sigma_y=st.sidebar.number_input("$\sigma_y$ "+Unit ,-250,250,value=100)
tau_xy=st.sidebar.number_input("$\\tau_{xy}$ "+Unit,-250,250,value=100)
theta=st.sidebar.number_input("$\\theta$ ($\degree$)",-90,90,value=45)


sigma_x1 = round((sigma_x + sigma_y) / 2 +  ((sigma_x - sigma_y) / 2)*np.cos(2*theta*np.pi/180) + tau_xy*np.sin(2*theta*np.pi/180),2) 
sigma_y1 = round((sigma_x + sigma_y) / 2 -  ((sigma_x - sigma_y) / 2)*np.cos(2*theta*np.pi/180) - tau_xy*np.sin(2*theta*np.pi/180),2) 
tau_x1y1 = round(-(sigma_x-sigma_y)/2*np.sin(2*theta*np.pi/180)+tau_xy*np.cos(2*theta*np.pi/180),2)


p_stress1 = round((sigma_x + sigma_y) / 2 +  (((sigma_x - sigma_y) / 2)**2 + tau_xy **2)**0.5,2)
p_stress2 = round((sigma_x + sigma_y) / 2 -  (((sigma_x - sigma_y) / 2)**2 + tau_xy **2)**0.5,2)
max_shear = round((((sigma_x - sigma_y) / 2)**2 + tau_xy **2)**0.5,2)

theta_p1 =round(np.arctan(2*tau_xy/(sigma_x-sigma_y))/2*180/np.pi,2)
theta_p2 =round(theta_p1+90,2)

theta_s1 =round(np.arctan(-(sigma_x-sigma_y)/(2*tau_xy))/2*180/np.pi,2)
theta_s2 =round(theta_s1+90,2)

radius = round((p_stress1 - p_stress2) / 2,2)
center_x = round((sigma_x + sigma_y) / 2,2)
center_y = 0






df = pd.DataFrame({'x': [p_stress1, p_stress2, center_x, center_x,sigma_x,sigma_y,sigma_x1,sigma_y1],
                   'y': [0, 0, 0, max_shear,tau_xy,-tau_xy,tau_x1y1,-tau_x1y1],
                   'Stresses': ['Principal', 'Principal', 'Average', 'Max Shear','Applied','Applied','Rotated','Rotated']})

fig = px.scatter(df, x = "x", y = "y", color = "Stresses")


fig.update_xaxes(nticks=5)
fig.update_yaxes(nticks=5,scaleanchor = "x",scaleratio = 1,)


fig.update_layout(xaxis_title='r$\sigma$ '+Unit, yaxis_title='test '+Unit)
fig.update_yaxes(autorange="reversed")


fig.add_shape(type="circle",
    xref="x", yref="y",
    x0=center_x-radius, y0=center_y-radius, x1=center_x+radius, y1=center_y+radius,
    line_color="lightblue",layer='below'
)

fig.add_shape(type="line",
    xref="x", yref="y",
    x0=sigma_x, y0=tau_xy, x1=sigma_y, y1=-tau_xy,
    line=dict(
        color="red",
        width=1,
    ),layer='below')

fig.add_shape(type="line",
    xref="x", yref="y",
    x0=sigma_x1, y0=tau_x1y1, x1=sigma_y1, y1=-tau_x1y1,
    line=dict(
        color="green",
        width=1,
    ),layer='below')

st.plotly_chart(fig)
col3, col4, col5 = st.columns(3)

col3.metric(label="$\sigma_{x1}$ "+Unit, value=round(sigma_x1,2))
col4.metric(label="$\sigma_{y1}$ "+Unit, value=round(sigma_y1,2))
col5.metric(label="$\\tau_{x1y1}$ "+Unit, value=round(tau_x1y1,2))

col3.metric(label="$\sigma_{1}$ "+Unit, value=round(p_stress1,2))
col4.metric(label="$\sigma_{2}$ "+Unit, value=round(p_stress2,2))
col5.metric(label="$\\tau_{max}$ "+Unit, value=round(max_shear,2))

col3.metric(label="$\\theta_{p,1}$", value=round(theta_p1,2))
col4.metric(label="$\\theta_{p,2}$", value=round(theta_p2,2))

col3.metric(label="$\\theta_{s,1}$", value=round(theta_s1,2))
col4.metric(label="$\\theta_{s,2}$", value=round(theta_s2,2))




