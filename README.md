# Outlier Detection and Cleaning App

A Streamlit web app to detect and handle outliers in multiple numeric columns using various methods with trimming or capping options. The app provides intuitive visualization and descriptive statistics before and after cleaning, enabling easy data preprocessing.

---

## Features

- **Multiple Outlier Detection Methods:**
  - Z-Score method (threshold > 3)
  - Interquartile Range (IQR) method
  - Percentile Winsorization

- **Outlier Handling Options:**
  - Trimming (remove outlier rows)
  - Capping (replace outliers with boundary values)

- **Visualizations:**
  - Distribution plots (histograms + KDE) before and after cleaning
  - Interactive box plots before and after cleaning

- **Summary Statistics:**
  - `describe()` output for selected columns before and after cleaning

- **Multi-column Support:**
  - Select multiple numeric columns to process simultaneously

- **Download Cleaned Data:**
  - Export the cleaned dataset as a CSV file

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/outlier-detection-app.git
   cd outlier-detection-app
