import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Function to load data
@st.cache_resource
def load_data(file, num_rows):
    if num_rows == 'all':
        data = pd.read_csv(file)
    else:
        data = pd.read_csv(file, nrows=int(num_rows))

    # Filter DataFrame to include only valid rows
    return data


# Streamlit app
st.title("Ezee Exploratory Data Analysis tool")

# Upload file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Check if file is uploaded
if uploaded_file is not None:
# Ask the user to select the number of rows
    num_rows = st.selectbox("Select the number of rows to analyze:", ['100', '500', '1000', '10000', '50000', 'all'])

    # Check if the user has selected the number of rows before loading the data
    if num_rows is not None:
        iris_df = load_data(uploaded_file, num_rows)

        # Display summary information
        st.write("## Summary Information")
        st.write(iris_df.describe())

        # Display dataset
        st.write("## Raw Dataset")
        st.write(iris_df)

        # Sidebar for selecting features
        selected_features = st.sidebar.multiselect("Select Features:", iris_df.columns)
        # EDA Plots
        if selected_features:
            st.write("## EDA Plots")

            # Pair plot
            st.write("### Pair Plot")
            numeric_columns = iris_df.select_dtypes(include=['float64', 'int64']).columns
            if len(numeric_columns) >= 2:
                pair_fig = sns.pairplot(iris_df[selected_features], height=3)
                st.pyplot(pair_fig)
            else:
                st.write("Not enough numeric columns for a pair plot.")

            # Box plot
            st.write("### Box Plot")
            try:
                # Attempt to create the box plot
                box_fig = px.box(iris_df, x=selected_features)
                st.plotly_chart(box_fig)
            except ValueError as e:
                st.warning(f"Skipping Box Plot due to non-convertible values: {e}")

            # Correlation heatmap
            st.write("### Correlation Heatmap")
            try:
                # Attempt to create the correlation heatmap
                corr_matrix = iris_df[selected_features].corr()
                sns.set(font_scale=1.2)
                heatmap_fig, ax = plt.subplots(figsize=(8, 6))
                sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", linewidths=.5, ax=ax)
                st.pyplot(heatmap_fig)
            except ValueError as e:
                st.warning(f"Skipping Correlation Heatmap due to non-convertible values: {e}")

            # Violin plot
            st.write("### Violin Plot")
            try:
                # Attempt to create the violin plot
                violin_fig = px.violin(iris_df, x=selected_features, box=True, points="all")
                st.plotly_chart(violin_fig)
            except ValueError as e:
                st.warning(f"Skipping Violin Plot due to non-convertible values: {e}")

        else:
            st.warning("Select at least one feature to generate EDA plots.")

        # # EDA Plots
        # if selected_features:
        #     st.write("## EDA Plots")

        #     # Pair plot
        #     st.write("### Pair Plot")
        #     numeric_columns = iris_df.select_dtypes(include=['float64', 'int64']).columns
        #     if len(numeric_columns) >= 2:
        #         pair_fig = sns.pairplot(iris_df[selected_features], height=3)
        #         st.pyplot(pair_fig)
        #     else:
        #         st.write("Not enough numeric columns for a pair plot.")

        #     # Box plot
        #     st.write("### Box Plot")
        #     # Check if 'species' is in the DataFrame
        #     # for selected in selected_features:
        #     box_fig = px.box(iris_df, x=selected_features)
        #     st.plotly_chart(box_fig)
        

        #     # Correlation heatmap
        #     st.write("### Correlation Heatmap")
        #     corr_matrix = iris_df[selected_features].corr()
        #     sns.set(font_scale=1.2)
        #     heatmap_fig, ax = plt.subplots(figsize=(8, 6))
        #     sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", linewidths=.5, ax=ax)
        #     st.pyplot(heatmap_fig)

        #     # Violin plot
        #     # for selected in selected_features:
        #     st.write("### Violin Plot")
        #     violin_fig = px.violin(iris_df,x=selected_features, box=True, points="all")
        #     st.plotly_chart(violin_fig)

        # else:
        #     st.warning("Select at least one feature to generate EDA plots.")







