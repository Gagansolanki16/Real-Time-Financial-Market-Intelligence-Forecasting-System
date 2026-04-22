# 🚀 Real-Time Financial Market Intelligence & Forecasting System

This project is a comprehensive **Stock Market Analysis and Prediction System** built with **Streamlit**, **Power BI**, and **Machine Learning (XGBoost)**.

---

<img width="1323" height="750" alt="image" src="https://github.com/user-attachments/assets/fe5bf8bd-e758-4623-b808-946fe30f873b" />
<img width="1338" height="746" alt="image" src="https://github.com/user-attachments/assets/de090ef7-e189-4727-9569-75255c164777" />
<img width="1841" height="773" alt="image" src="https://github.com/user-attachments/assets/fa74eb4b-156e-4984-8895-73d8ed9cb30b" />

### 🏗️ **Project Architecture**

The system follows a modular pipeline to ensure data integrity and real-time performance:

* **Data Acquisition:** Python scripts fetch live market data from APIs (Yahoo Finance).
* **Storage:** Processed data is stored in a **SQLite Database** (`stocks.db`) for historical tracking.
* **Machine Learning:** An **XGBoost** model processes trends to generate future price forecasts.
* **Web Interface:** A **Streamlit** app (`strempro.py`) provides an interactive way to view live predictions.
* **Business Intelligence:** **Power BI** (`Project.pbix`) connects to the database for deep-dive exploratory data analysis (EDA).

---

### 🛠️ **Tech Stack**

* **Backend:** Python (Pandas, NumPy, Scikit-learn)
* **Machine Learning:** XGBoost Regressor
* **Frontend/Web:** Streamlit
* **Database:** SQL (SQLite)
* **Visualization:** Power BI Desktop

---

### 📂 **File Structure**

* **`strempro.py`**: The main Streamlit web application for interactive forecasting.
* **`Project.ipynb`**: Jupyter Notebook containing data exploration and model training.
* **`Project.pbix`**: Power BI dashboard for institutional-grade reporting.
* **`stocks.db`**: Local SQL database storing processed market data.
* **`Final_Project_Results.png`**: Screenshot of the model performance and final output.
* **`volcompanies.png`**: Visualization of volatility analysis for various companies.

---

### ✨ **Key Features**

* **Live Market Pulse:** Real-time data fetching and visualization.
* **Predictive Modeling:** Advanced forecasting using Gradient Boosting (**XGBoost**) to identify potential market trends.
* **Interactive UI:** Users can select different stock tickers and timeframes through the Streamlit interface.
* **Institutional Reporting:** Power BI dashboards for analyzing volatility, moving averages, and model error metrics ($RMSE$, $MAE$).

---


