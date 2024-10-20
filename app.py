import streamlit as st
import pandas as pd
from io import BytesIO

# Define prioritization methods
def rice_score(reach: int, impact: int, confidence: int, effort: int) -> float:
    """Calculate RICE score."""
    return (reach * impact * (confidence / 100)) / effort

def value_vs_effort(value: int, effort: int) -> float:
    """Calculate Value vs Effort score."""
    return value / effort

def mosow_priority(priority: str) -> int:
    """Assign numeric priority based on MoSCoW method."""
    return {'Must Have': 1, 'Should Have': 2, 'Could Have': 3, 'Won’t Have': 4}.get(priority, 4)

# Export DataFrame to Excel
'''def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Prioritization Results')
    processed_data = output.getvalue()
    return processed_data
'''

# Export Dataframe to CSV
def to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# App title
st.title('Feature Prioritization Tool for Product Managers')

# Feature input section
st.subheader('Enter Multiple Features')

# Select prioritization model first
model = st.selectbox('Select Prioritization Model', ['RICE', 'MoSCoW', 'Value vs Effort'])

# After model selection, allow input of features
st.subheader(f'Enter Features for {model} Model')

# Initialize an empty DataFrame to store feature details
df = pd.DataFrame(columns=['Feature Name', 'Model', 'Priority'])

# Number of features to input
num_features = st.number_input('How many features do you want to add?', min_value=1, value=1)

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

# Display the prioritization table after inputting all features
if not df.empty:
    st.subheader('Prioritization Results')
    st.dataframe(df)

    # Choose file format for download (CSV or Excel)
    file_format = st.selectbox('Choose file format to download', ['CSV'])
    '''file_format = st.selectbox('Choose file format to download', ['CSV', 'Excel'])'''
    
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
