import streamlit as st
import pandas as pd
import numpy as np

# Set the title
st.title("Professioni esposte ai robot")


### Prepare data

# Import data of profession exposure
prof_exp_df = pd.read_excel("MATCHING_Prof_Robot_19012021.xlsx", sheet_name="Tabella_MATCHING")
# Transform string type into boolean
prof_exp_df['robot'] = prof_exp_df['robot'].map({"si": True, "no": False})
prof_exp_df['complementare'] = prof_exp_df['complementare'].map({"si": True, "no": False})
# Keep only the integer part of the IFR classification codes
prof_exp_df['IFR_l1_rev'] = prof_exp_df['IFR_l1_rev'].astype('Int64')
prof_exp_df['IFR_l2_rev'] = prof_exp_df['IFR_l2_rev'].astype('Int64')

# Import data of IFR classification
class_robot_df = pd.read_excel("IFR_Classification_Application.xlsx")


### Sidebar

prof_list = prof_exp_df['descrizione_unita_prof'].tolist()

with st.sidebar:
    selected_prof = st.selectbox("Seleziona una professione", prof_list, index=None)




### Filtering

if (selected_prof is None):
    robot_exposure = np.nan
    complementary = np.nan
    robot_cat1 = np.nan
    robot_cat2 = np.nan
else: 
    robot_exposure = prof_exp_df.loc[prof_exp_df['descrizione_unita_prof'] == selected_prof, 'robot'].values[0]
    complementary = prof_exp_df.loc[prof_exp_df['descrizione_unita_prof'] == selected_prof, 'complementare'].values[0]
    robot_cat1 = prof_exp_df.loc[prof_exp_df['descrizione_unita_prof'] == selected_prof, 'IFR_l1_rev'].values[0]
    robot_cat2 = prof_exp_df.loc[prof_exp_df['descrizione_unita_prof'] == selected_prof, 'IFR_l2_rev'].values[0]

if (pd.isna(robot_cat1) & pd.isna(robot_cat2)):
    application_cat = np.nan
elif ((not pd.isna(robot_cat1)) & pd.isna(robot_cat2)):
    application_cat = class_robot_df.loc[class_robot_df['ifr_class'] == robot_cat1, 'application_area_it'].values[0]
elif (pd.isna(robot_cat1) & (not pd.isna(robot_cat2))):
    application_cat = class_robot_df.loc[class_robot_df['ifr_class'] == robot_cat2, 'application_area_it'].values[0]
else:
    application_cat = class_robot_df.loc[class_robot_df['ifr_class'] == robot_cat2, 'application_area_it'].values[0]


### Display data

if (selected_prof is None):
    st.write("Seleziona una professione.")
else:
    st.write("Professione selezionata: {}".format(selected_prof))
    st.write("La professione è esposta ai robot: {}".format("Sì" if robot_exposure else "No"))
    if (complementary == True):
        st.write("I robots sono complementari: Sì")
    if (not pd.isna(application_cat)):
        st.write("L'applicazione dei robots è': {}".format(application_cat))



### Methodology


### About us

