import pandas as pd
import streamlit as st

# Streamlit file uploader
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file:
    # Read the Excel file from the uploaded file
    df = pd.read_excel(uploaded_file, sheet_name='CAPA')  # Replace with the name of your sheet

    # Drop columns with names starting with "Unnamed:"
    df = df.loc[:, ~df.columns.str.contains('^Unnamed:')]
    if 'Classification' in df.columns:
        df = df.drop(columns=['Classification'])

    # Function to determine severity based on the provided conditions
    def determine_severity(row):
        aging = row['CAPA Age [days]']
        if row['Product (saftey/perfromance)/Labeling nonconfirmances on the market'] == 'X':
            if aging <= 250:
                return 'High'
            elif 250 < aging <= 365:
                return 'High'
            else:
                return 'High'
        elif row['- External Audit Findings -  Production'] == 'X':
            if aging <= 250:
                return 'Medium'
            elif 250 < aging <= 365:
                return 'Medium'
            else:
                return 'High'
        elif row['Other nonconformities'] == 'X':
            if aging <= 250:
                return 'Low'
            elif 250 < aging <= 365:
                return 'Low'
            else:
                return 'Medium'
        else:
            return 'Unknown'

    # Apply the function to each row in the dataframe
    df['Severity'] = df.apply(determine_severity, axis=1)

    # Filter options for 'CAPA in Phase'
    phase_options = df['CAPA in Phase'].unique().tolist()
    phase_options.insert(0, 'All')  # Add 'All' option

    # Add multiselect for filtering with default selected values
    selected_phase = st.multiselect("Select CAPA in Phase to filter", phase_options, default=['Implementation', 'Investigation'])

    # Filter dataframe based on selected phases
    if 'All' in selected_phase:
        df_filtered = df
    else:
        df_filtered = df[df['CAPA in Phase'].isin(selected_phase)]

    # Function to highlight severity column
    def highlight_severity(row):
        color = ''
        if row['Severity'] == 'High':
            color = 'background-color: red'
        elif row['Severity'] == 'Medium':
            color = 'background-color: yellow'
        elif row['Severity'] == 'Low':
            color = 'background-color: green'
        return [''] * (len(row) - 1) + [color]

    # Apply the highlight function to the dataframe
    styled_df = df_filtered.style.apply(highlight_severity, axis=1)

    # Display the dataframe
    st.write(f"Data from Excel file (Sheet: CAPA):")
    st.dataframe(styled_df)
else:
    st.write("Please upload an Excel file.")
