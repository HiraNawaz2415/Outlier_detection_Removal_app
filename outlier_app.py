import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="Outlier Detection & Cleaning App", layout="wide")
st.title("📊 Multi-Column Outlier Detection with Trimming & Capping")

# Upload section
uploaded_file = st.file_uploader("📁 Upload a CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### 🔍 Data Preview", df.head())

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if not numeric_cols:
        st.warning("No numeric columns found.")
    else:
        selected_cols = st.multiselect("📌 Select numeric columns", numeric_cols, default=numeric_cols)
        method = st.radio("📈 Outlier Detection Method", ["Z-Score", "IQR", "Percentile Winsorization"])

        # Parameters for Winsorization
        if method == "Percentile Winsorization":
            lower_pct = st.slider("🔻 Lower Percentile (%)", 0.0, 10.0, 1.0, step=0.5)
            upper_pct = st.slider("🔺 Upper Percentile (%)", 90.0, 100.0, 99.0, step=0.5)

        # Capping or Trimming for all methods
        handle_mode = st.radio("⚙️ How to Handle Outliers", ["Trimming", "Capping"])

        if st.button("🚀 Apply Detection & Cleaning"):
            original_df = df.copy()
            cleaned_df = df.copy()

            for col in selected_cols:
                st.markdown(f"---\n### 🔍 Analyzing Column: **{col}**")

                values = cleaned_df[col]
                st.write("**Original describe():**")
                st.dataframe(original_df[col].describe())

                # DISTPLOT before
                st.write("📊 **Distribution Before Cleaning**")
                fig_before, ax1 = plt.subplots()
                sns.histplot(original_df[col], kde=True, ax=ax1)
                st.pyplot(fig_before)

                # Outlier detection and handling
                if method == "Z-Score":
                    z = (values - np.mean(values)) / np.std(values)
                    outliers = (np.abs(z) > 3)

                    if handle_mode == "Trimming":
                        cleaned_df = cleaned_df[~outliers]
                    else:  # Capping
                        cap_min = cleaned_df.loc[~outliers, col].min()
                        cap_max = cleaned_df.loc[~outliers, col].max()
                        cleaned_df[col] = np.where(z > 3, cap_max, cleaned_df[col])
                        cleaned_df[col] = np.where(z < -3, cap_min, cleaned_df[col])

                elif method == "IQR":
                    Q1 = np.percentile(values, 25)
                    Q3 = np.percentile(values, 75)
                    IQR = Q3 - Q1
                    lower = Q1 - 1.5 * IQR
                    upper = Q3 + 1.5 * IQR
                    outliers = (values < lower) | (values > upper)

                    if handle_mode == "Trimming":
                        cleaned_df = cleaned_df[~outliers]
                    else:
                        cleaned_df[col] = np.where(values > upper, upper, cleaned_df[col])
                        cleaned_df[col] = np.where(values < lower, lower, cleaned_df[col])

                elif method == "Percentile Winsorization":
                    lower = np.percentile(values, lower_pct)
                    upper = np.percentile(values, upper_pct)

                    if handle_mode == "Trimming":
                        cleaned_df = cleaned_df[(values >= lower) & (values <= upper)]
                    else:
                        cleaned_df[col] = np.where(values < lower, lower, cleaned_df[col])
                        cleaned_df[col] = np.where(values > upper, upper, cleaned_df[col])

                # Show describe after
                st.write("**Cleaned describe():**")
                st.dataframe(cleaned_df[col].describe())

                # DISTPLOT after
                st.write("📊 **Distribution After Cleaning**")
                fig_after, ax2 = plt.subplots()
                sns.histplot(cleaned_df[col], kde=True, ax=ax2, color="green")
                st.pyplot(fig_after)

                # BOX PLOTS
                st.write("📦 **Box Plot Comparison**")
                fig1 = px.box(original_df, y=col, points="outliers", title=f"{col} - Original")
                fig2 = px.box(cleaned_df, y=col, points="outliers", title=f"{col} - Cleaned")
                col1, col2 = st.columns(2)
                col1.plotly_chart(fig1, use_container_width=True)
                col2.plotly_chart(fig2, use_container_width=True)

            # Final cleaned dataset
            st.write(f"### Final Cleaned Data: {len(cleaned_df)} rows")
            st.dataframe(cleaned_df)

            # Download cleaned data
            def convert_df(df):
                output = BytesIO()
                df.to_csv(output, index=False)
                return output.getvalue()

            st.download_button(
                label="💾 Download Cleaned Data as CSV",
                data=convert_df(cleaned_df),
                file_name="cleaned_data.csv",
                mime="text/csv"
            )
