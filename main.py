import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


### Prepare data

# Import data of profession exposure
prof_exp_df = pd.read_excel("MATCHING_Prof_Robot_19012021.xlsx", sheet_name="Tabella_MATCHING")
# Transform string type into boolean
prof_exp_df['robot'] = prof_exp_df['robot'].map({"si": True, "no": False})
prof_exp_df['complementare'] = prof_exp_df['complementare'].map({"si": True, np.nan: False})
# Keep only the integer part of the IFR classification codes
prof_exp_df['IFR_l1_rev'] = prof_exp_df['IFR_l1_rev'].astype('Int64')
prof_exp_df['IFR_l2_rev'] = prof_exp_df['IFR_l2_rev'].astype('Int64')
# Adapt the IFR classification
ifr_codes = [111, 112, 113, 114, 115, 116, 117, 118, 119, 160, 170, 190, 200]
cat1 = prof_exp_df['IFR_l1_rev'].where(prof_exp_df['IFR_l1_rev'].isin(ifr_codes), np.nan)
cat2 = prof_exp_df['IFR_l2_rev'].where(prof_exp_df['IFR_l2_rev'].isin(ifr_codes), np.nan)
prof_exp_df['IFR_class'] = cat1.combine_first(cat2)

# Import data of IFR classification
class_robot_df = pd.read_excel("IFR_Classification_Application.xlsx")
# Create a dictionary of applications
app_dict = class_robot_df[class_robot_df["ifr_class"].isin(ifr_codes)].set_index("application_area_it")["ifr_class"].to_dict()

# Import data on robot installation
robot_df = pd.read_csv('data_robots_italy.csv', sep=',', dtype={'year': 'int64', 'ifr_act': 'int64', 'ifr': 'object', 'robots_it': 'object'})
# Keep only relevant IFR classes
robot_df = robot_df[robot_df["ifr_act"].isin(ifr_codes)]



### Sidebar

prof_list = prof_exp_df['descrizione_unita_prof'].tolist()

with st.sidebar:
    selected_prof = st.selectbox("Seleziona una professione", prof_list, index=None)
    selected_app = st.selectbox("Seleziona un'applicazione", list(app_dict.keys()))

# Get the code of the application
selected_cat = app_dict[selected_app]



### Filtering

if (selected_prof is None):
    robot_exposure = np.nan
    complementary = np.nan
    robot_cat = np.nan
    application_cat = np.nan
else: 
    robot_exposure = prof_exp_df.loc[prof_exp_df['descrizione_unita_prof'] == selected_prof, 'robot'].values[0]
    complementary = prof_exp_df.loc[prof_exp_df['descrizione_unita_prof'] == selected_prof, 'complementare'].values[0]
    robot_cat = prof_exp_df.loc[prof_exp_df['descrizione_unita_prof'] == selected_prof, 'IFR_class'].values[0]
    if pd.isna(robot_cat):
        application_cat = np.nan
    else:
        application_cat = class_robot_df.loc[class_robot_df['ifr_class'] == robot_cat, 'application_area_it'].values[0]



### Display data

## Text
st.header("Professioni esposte ai robot")
if (selected_prof is None):
    st.write("Seleziona una professione.")
else:
    st.write("Professione selezionata: {}".format(selected_prof))
    st.write("La professione è esposta ai robot: {}".format("Sì" if robot_exposure else "No"))
    st.write("I robots sono complementari: {}".format("Sì" if complementary else "No"))
    if (not pd.isna(application_cat)):
        st.write("L'applicazione dei robots è: {} (codice IFR: {})".format(application_cat, robot_cat))

## Plot
st.header("Numero di robot installati")
chart = (
    alt.Chart(robot_df)
    .mark_line()
    .encode(
        x=alt.X("year:O", axis=alt.Axis(title="Anno")),
        y=alt.Y("robots_it:Q", axis=alt.Axis(title="Numero di robot installati")),
        color=alt.Color('ifr_act:N', scale=alt.Scale(scheme='category10'), legend=None),
        opacity=alt.condition(
            alt.datum.ifr_act == selected_cat,
            alt.value(1),
            alt.value(0.3) 
        ),
        tooltip=[alt.Tooltip("robots_it:Q", title="Numero di robot installati"), alt.Tooltip("year:O", title="Anno")],
    ).properties(title=["Numero di robot installati per anno con applicazione in:","{}".format(selected_app)])
)

st.altair_chart(chart, use_container_width=True)



### Methodology

st.header("Methodology")
st.write("We use the information contained in the 2013 Italian National Institute for Public Policies Analysis (Inapp) Survey of Professions (Indagine Campionaria sulle Professioni, Inapp ICP) and we manually match each robot application following the definition of the International Federation of Robotics with one or more occupations on the basis of the occupation's description, its three primary occupation-specific activities according to Inapp ICP scores and, where necessary, additional information provided in the survey. "
         "By relating robots and occupations on the basis of functional analogies, we determine whether an occupation is *exposed* to a given robot application, that is if its main activities can be associated with a specific industrial robot application, or not. "
         "Using the same approach, we identify what we refer to as robot operators (i.e., occupations complementary to robots), that is workers who are involved in the design, installation, maintenance and operation of forms of automation related to robotization and whose activities cannot be performed by a robot application. ")

st.subheader("References")
st.markdown("- Caselli, M., Fracasso, A., Scicchitano, S., Traverso, S., Tundis, E. (2021). Stop worrying and love the robot: An activity-based approach to assess the impact of robotization on employment dynamics. GLO Discussion Paper Series 802, Global Labor Organization (GLO).")



### About us

st.header("About us")
st.write("This dashboard is based on a methodology developed by:")
st.write("- Mauro Caselli, School of International Studies \& Dep. of Economics and Management, University of Trento, Italy")
st.write("- Andrea Fracasso, School of International Studies \& Dep. of Economics and Management, University of Trento, Italy")
st.write("- Sergio Scicchitano, John Cabot University, Rome, National Institute for Public Policies Analysis (INAPP), Italy, and Global Labor Organisation (GLO), Germany")
st.write("- Silvio Traverso, Department of Law, Political, Economic and Social Sciences, University of Eastern Piedmont, Italy")
st.write("- Enrico Tundis, Ispat, Italy")

st.write("Contact: mauro.caselli@unitn.it")

