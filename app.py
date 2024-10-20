import streamlit as st
import pandas as pd

# Define prioritization methods
def rice_score(reach, impact, confidence, effort):
    return (reach * impact * confidence) / effort

def value_vs_effort(value, effort):
    return value / effort

def mosow_priority(priority):
    return {'Must Have': 1, 'Should Have': 2, 'Could Have': 3, 'Won’t Have': 4}.get(priority, 4)

# App title
st.title('Feature Prioritization Tool for Product Managers')

# Input feature details
st.subheader('Enter Feature Details')
feature_name = st.text_input('Feature Name')

# Choose prioritization model
model = st.selectbox('Select Prioritization Model', ['RICE', 'MoSCoW', 'Value vs Effort'])

if model == 'RICE':
    reach = st.number_input('Reach (0-1000)', min_value=0, max_value=1000, value=100)
    impact = st.slider('Impact (1-5)', 1, 5, 3)
    confidence = st.slider('Confidence (1-100%)', 1, 100, 80)
    effort = st.number_input('Effort (hours)', min_value=1, value=10)
    if st.button('Calculate Priority'):
        score = rice_score(reach, impact, confidence, effort)
        st.write(f'RICE Score for "{feature_name}": {score}')

elif model == 'MoSCoW':
    priority = st.selectbox('Select Priority', ['Must Have', 'Should Have', 'Could Have', 'Won’t Have'])
    if st.button('Set Priority'):
        mosow_score = mosow_priority(priority)
        st.write(f'MoSCoW Priority for "{feature_name}": {priority} (Score: {mosow_score})')

elif model == 'Value vs Effort':
    value = st.number_input('Value', min_value=1, value=10)
    effort = st.number_input('Effort', min_value=1, value=10)
    if st.button('Calculate Priority'):
        ve_score = value_vs_effort(value, effort)
        st.write(f'Value vs Effort Score for "{feature_name}": {ve_score}')

# Option to clear input data
if st.button('Clear'):
    st.experimental_rerun()
