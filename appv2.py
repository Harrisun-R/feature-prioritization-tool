import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from transformers import pipeline  # For LLM-based suggestions

# Initialize the pre-trained model for suggesting prioritization models
llm = pipeline('text-generation', model='gpt2')  # or use OpenAI API if available

# Function to suggest prioritization model based on feature descriptions
def suggest_prioritization_model(feature_descriptions):
    input_text = "Suggest the best prioritization model for the following features:\n" + '\n'.join(feature_descriptions)
    suggestion = llm(input_text, max_length=50, num_return_sequences=1)
    return suggestion[0]['generated_text']

# Prioritization Methods
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

# Export DataFrame to CSV
def to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# App title
st.title('AI-Powered Feature Prioritization Tool for Product Managers')

# Placeholder for user branding
st.markdown("Created by Harrisun Raj Mohan (https://www.linkedin.com/in/harrisun-raj-mohan/)")

# Number of features to input
num_features = st.number_input('How many features do you want to add?', min_value=1, value=1)

# Initialize list to store feature descriptions
feature_descriptions = []

# Feature input and description gathering
for i in range(0,num_features):
    with st.expander(f'Feature {i + 1} Details', expanded=True):
        feature_name = st.text_input(f'Feature Name {i + 1}', key=f"feature_{i}")
        feature_description = st.text_area(f'Feature Description {i + 1}', key=f"description_{i}")
        feature_descriptions.append(feature_description)

# Suggest the best prioritization model based on the features provided
if st.button('Suggest Prioritization Model'):
    suggestion = suggest_prioritization_model(feature_descriptions)
    st.markdown(f"**Suggested Prioritization Model:** {suggestion}")

# Allow the user to manually select a prioritization model if desired
models = ['RICE', 'MoSCoW', 'Value vs Effort', 'KANO Model', 'ICE', 'Weighted Scoring']
model = st.selectbox('Select Prioritization Model', models)

# Explanation of selected prioritization model
model_explanations = {
    'RICE': 'The RICE model helps prioritize features based on Reach, Impact, Confidence, and Effort.',
    'MoSCoW': 'The MoSCoW model prioritizes based on Must Have, Should Have, Could Have, and Won’t Have.',
    'Value vs Effort': 'The Value vs Effort model ranks features based on their value to the business versus the effort required.',
    'KANO Model': 'The KANO model evaluates features based on customer satisfaction and dissatisfaction.',
    'ICE': 'The ICE model helps prioritize based on Impact, Confidence, and Ease of implementation.',
    'Weighted Scoring': 'The Weighted Scoring model assigns a score based on different weighted factors to rank features.'
}
st.markdown(f"**Model Explanation**: {model_explanations[model]}")

# Initialize DataFrame for results
df = pd.DataFrame(columns=['Feature Name', 'Model', 'Priority'])

# Feature input and calculation logic based on model
for i in range(num_features):
    with st.expander(f'Feature {i + 1} Details', expanded=True):
        feature_name = st.text_input(f'Feature Name {i + 1}', key=f"feature_{i}")

        if model == 'RICE':
            reach = st.number_input(f'Reach (0-1000)', min_value=0, max_value=1000, value=100, key=f"reach_{i}")
            impact = st.slider(f'Impact (1-5)', 1, 5, 3, key=f"impact_{i}")
            confidence = st.slider(f'Confidence (1-100%)', 1, 100, 80, key=f"confidence_{i}")
            effort = st.number_input(f'Effort (hours)', min_value=1, value=10, key=f"effort_{i}")
            score = rice_score(reach, impact, confidence, effort)
            df = pd.concat([df, pd.DataFrame({'Feature Name': [feature_name], 'Model': ['RICE'], 'Priority': [score]})], ignore_index=True)

        elif model == 'MoSCoW':
            priority = st.selectbox(f'Select Priority', ['Must Have', 'Should Have', 'Could Have', 'Won’t Have'], key=f"priority_{i}")
            mosow_score = mosow_priority(priority)
            df = pd.concat([df, pd.DataFrame({'Feature Name': [feature_name], 'Model': ['MoSCoW'], 'Priority': [priority]})], ignore_index=True)

        elif model == 'Value vs Effort':
            value = st.number_input(f'Value', min_value=1, value=10, key=f"value_{i}")
            effort = st.number_input(f'Effort', min_value=1, value=10, key=f"effort_val_{i}")
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

# Display prioritization results
if not df.empty:
    st.subheader('Prioritization Results')
    st.dataframe(df)

    # Choose file format for download (CSV or Excel)
    file_format = st.selectbox('Choose file format to download', ['CSV', 'Excel'])

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
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    # Plot the quadrant only for specific models
    if model in ['MoSCoW', 'KANO Model', 'Value vs Effort']:
        st.subheader(f'Quadrant Plot for {model}')
        if model == 'MoSCoW':
            plt.scatter(df['Feature Name'], df['Priority'])
            plt.title('MoSCoW Quadrant Plot')
        elif model == 'KANO Model':
            plt.scatter(df['Feature Name'], df['Priority'])
            plt.title('KANO Quadrant Plot')
        elif model == 'Value vs Effort':
            plt.scatter(df['Feature Name'], df['Priority'])
            plt.title('Value vs Effort Quadrant Plot')
        plt.xlabel('Feature Name')
        plt.ylabel('Priority')
        st.pyplot(plt)