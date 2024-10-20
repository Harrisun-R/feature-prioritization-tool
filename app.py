import streamlit as st
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np

# Define prioritization methods
def rice_score(reach, impact, confidence, effort):
    return (reach * impact * (confidence / 100)) / effort

def value_vs_effort(value, effort):
    return value / effort

def mosow_priority(priority):
    return {'Must Have': 1, 'Should Have': 2, 'Could Have': 3, 'Won’t Have': 4}.get(priority, 4)

def kano_model(satisfaction, dissatisfaction):
    return (satisfaction - dissatisfaction)

def ice_score(impact, confidence, ease):
    return (impact * confidence * ease) / 100

def weighted_scoring(weight, score):
    return weight * score

# Export DataFrame to Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Prioritization Results')
    processed_data = output.getvalue()
    return processed_data

# Export Dataframe to CSV
def to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# App title
st.title('Feature Prioritization Tool for Product Managers')
LINKEDIN_URL = "https://www.linkedin.com/in/harrisun-raj-mohan/"
st.markdown("Created by Harrisun Raj Mohan")
st.write(f"[Connect on LinkedIn]({LINKEDIN_URL})")

# Explanations for prioritization models
model_explanations = {
    'RICE': 'The RICE model helps prioritize features based on Reach, Impact, Confidence, and Effort.',
    'MoSCoW': 'The MoSCoW model prioritizes based on Must Have, Should Have, Could Have, and Won’t Have.',
    'Value vs Effort': 'The Value vs Effort model ranks features based on their value to the business versus the effort required.',
    'KANO Model': 'The KANO model evaluates features based on customer satisfaction and dissatisfaction.',
    'ICE': 'The ICE model helps prioritize based on Impact, Confidence, and Ease of implementation.',
    'Weighted Scoring': 'The Weighted Scoring model assigns a score based on different weighted factors to rank features.'
}

# Prioritization model selection
models = ['RICE', 'MoSCoW', 'Value vs Effort', 'KANO Model', 'ICE', 'Weighted Scoring']
model = st.selectbox('Select Prioritization Model', models)

# Display explanation of the selected model
st.markdown(f"**Model Explanation**: {model_explanations[model]}")

# Number of features to input
num_features = st.number_input('How many features do you want to add?', min_value=1, value=1)

# Initialize DataFrame for results
df = pd.DataFrame(columns=['Feature Name', 'Model', 'Priority'])

# Input features based on the selected model
for i in range(num_features):
    with st.expander(f'Feature {i + 1} Details', expanded=True):
        feature_name = st.text_input(f'Feature Name {i + 1}', key=f"feature_{i}")
    
        if model == 'RICE':
            reach = st.number_input(f'Reach (0-1000) for Feature {i + 1}', min_value=0, max_value=1000, value=100, key=f"reach_{i}")
            impact = st.slider(f'Impact (1-5) for Feature {i + 1}', 1, 5, 3, key=f"impact_{i}")
            confidence = st.slider(f'Confidence (1-100%) for Feature {i + 1}', 1, 100, 80, key=f"confidence_{i}")
            effort = st.number_input(f'Effort (hours) for Feature {i + 1}', min_value=1, value=10, key=f"effort_{i}")
            score = rice_score(reach, impact, confidence, effort)
            df = pd.concat([df, pd.DataFrame({'Feature Name': [feature_name], 'Model': ['RICE'], 'Priority': [score]})], ignore_index=True)
        
        elif model == 'MoSCoW':
            priority = st.selectbox(f'Select Priority for Feature {i + 1}', ['Must Have', 'Should Have', 'Could Have', 'Won’t Have'], key=f"priority_{i}")
            mosow_score = mosow_priority(priority)
            df = pd.concat([df, pd.DataFrame({'Feature Name': [feature_name], 'Model': ['MoSCoW'], 'Priority': [priority]})], ignore_index=True)
        
        elif model == 'Value vs Effort':
            value = st.number_input(f'Value for Feature {i + 1}', min_value=1, value=10, key=f"value_{i}")
            effort = st.number_input(f'Effort for Feature {i + 1}', min_value=1, value=10, key=f"effort_val_{i}")
            ve_score = value_vs_effort(value, effort)
            df = pd.concat([df, pd.DataFrame({'Feature Name': [feature_name], 'Model': ['Value vs Effort'], 'Priority': [ve_score]})], ignore_index=True)

        elif model == 'KANO Model':
            satisfaction = st.number_input(f'Satisfaction', min_value=1, max_value=5, key=f"satisfaction_{i}")
            dissatisfaction = st.number_input(f'Dissatisfaction', min_value=1, max_value=5, key=f"dissatisfaction_{i}")
            kano_score = kano_model(satisfaction, dissatisfaction)
            df = pd.concat([df, pd.DataFrame({'Feature Name': [feature_name], 'Model': ['KANO Model'], 'Priority': [kano_score]})], ignore_index=True)

        elif model == 'ICE':
            impact = st.number_input(f'Impact (1-10)', min_value=1, max_value=10, key=f"impact_ice_{i}")
            confidence = st.number_input(f'Confidence (1-10)', min_value=1, max_value=10, key=f"confidence_ice_{i}")
            ease = st.number_input(f'Ease (1-10)', min_value=1, max_value=10, key=f"ease_{i}")
            ice_score_value = ice_score(impact, confidence, ease)
            df = pd.concat([df, pd.DataFrame({'Feature Name': [feature_name], 'Model': ['ICE'], 'Priority': [ice_score_value]})], ignore_index=True)

        elif model == 'Weighted Scoring':
            weight = st.number_input(f'Weight (1-10)', min_value=1, max_value=10, key=f"weight_{i}")
            score = st.number_input(f'Score (1-10)', min_value=1, max_value=10, key=f"score_{i}")
            weighted_score = weighted_scoring(weight, score)
            df = pd.concat([df, pd.DataFrame({'Feature Name': [feature_name], 'Model': ['Weighted Scoring'], 'Priority': [weighted_score]})], ignore_index=True)

# Display the prioritization table after inputting all features
if not df.empty:
    st.subheader('Prioritization Results')
    st.dataframe(df)

    # Generate quadrant plot for MoSCoW, KANO, and Value vs Effort
    if model in ['MoSCoW', 'KANO Model', 'Value vs Effort']:
        st.subheader('Quadrant Plot')

        if model == 'MoSCoW':
            df['Priority Level'] = df['Priority'].apply(lambda x: 1 if x == 'Must Have' else 2 if x == 'Should Have' else 3 if x == 'Could Have' else 4)
            x = df['Feature Name']
            y = df['Priority Level']
            xlabel = 'Features'
            ylabel = 'Priority Level'
        elif model == 'KANO Model':
            x = df['Feature Name']
            y = df['Priority']
            xlabel = 'Features'
            ylabel = 'Satisfaction vs Dissatisfaction'
        elif model == 'Value vs Effort':
            x = df['Feature Name']
            y = df['Priority']
            xlabel = 'Features'
            ylabel = 'Value vs Effort'

        # Plotting with matplotlib
        fig, ax = plt.subplots()
        ax.scatter(x, y, color='b')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
    # Choose file format for download (CSV or Excel)
    file_format = st.selectbox('Choose file format to download', ['CSV'])
    
    # Button to download the table in the selected format
    if file_format == 'CSV':
        st.download_button(
            label="Download Results as CSV",
            data=to_csv(df),
            file_name='prioritization_results.csv',
            mime='text/csv'
        )
    elif file_format == 'Excel':
        st.download_button(
            label="Download Results as Excel",
            data=to_excel(df),
            file_name='prioritization_results.xlsx',
            mime='application/vnd.ms-excel'
        )

# Option to clear input data
if st.button('Clear'):
    st.experimental_set_query_params()
    st.stop()
