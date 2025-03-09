# 🏏 Dream11 Cricket Prediction Project 🤖📊

Welcome to the Dream11 Cricket Prediction Project, an advanced end-to-end solution that leverages granular cricket data and cutting-edge machine learning to predict player performances and build optimal fantasy teams. Our approach integrates multiple specialized datasets, intricate feature engineering, robust predictive modeling, and interpretability tools to deliver unbiased, data-driven predictions. This project is designed to forecast a player's upcoming match performance based solely on their historical statistics, ensuring a fair, player-agnostic prediction model. 🚀

---

## 📌 Table of Contents
- [📌 Project Overview](#project-overview)
- [🛠️ Dataset Details and Feature Engineering](#dataset-details-and-feature-engineering)
- [🧬 Training Data Preparation](#training-data-preparation)
- [🤓 Modeling](#modeling)
- [🔮 Prediction Pipeline](#prediction-pipeline)
- [🔢 Evaluation Metrics](#evaluation-metrics)
- [🌐 Deployment](#deployment)
- [🏁 Conclusion](#conclusion)
- [📝 License](#license)

---

## 📌 Project Overview
This project tackles the challenge of predicting Dream11 fantasy cricket outcomes using a multi-faceted approach:

- **Data Integration:** Comprehensive ball-by-ball data from Cricsheet is transformed into specialized datasets.
- **Feature Engineering:** We derive complex performance metrics from player interactions, venue trends, and individual form, with an emphasis on unbiased, statistic-driven predictions.
- **Predictive Modeling:** A finely tuned XGBoost model predicts Dream Points, with evaluation incorporating Dream11 scoring nuances such as captain and vice-captain multipliers.
- **Interpretability:** SHAP values and Gemini API integration provide detailed, human-readable explanations for player selections.
- **User Experience:** An interactive Streamlit app allows users to input match details and receive predictions along with comprehensive rationales.

> **Key Note:** Our model exclusively uses **past data** to predict future performance. We have not used any upcoming match data or the data from the match for which predictions are being made, ensuring our model remains purely data-driven and unbiased. Additionally, the model is designed to predict a player's performance based only on **statistical features** without any reliance on player names or identities, ensuring fairness and avoiding biases. This allows our model to function effectively as a cricket prediction system that only considers past performance trends.

---

## 🛠️ Dataset Details and Feature Engineering
### 📄 Player Form Dataset
- **Columns:** `Player`, `total_points`, `Date`, `Venue`, `Runs_Scored`, `Balls_Faced`, `Wickets_Taken`, `Runs_Given`, `Balls_Thrown`, `Boundaries_Scored`, `Boundaries_Given`, `Number_of_Dismissals`, `Strike_Rate`, `Economy`, `Batting_Average`, `EWMA Fantasy Points`
- **Importance:** Captures a player's overall performance over time with an emphasis on recent trends using an Exponential Weighted Moving Average (EWMA). It helps in understanding historical performance and current form, which is crucial for predicting future performance.

### 📄 Player vs Venue Dataset
- **Columns:** `Date`, `Venue`, `player_Id`, `player_name`, `runs_scored`, `balls_faced`, `wickets_taken`, `runs_given`, `balls_thrown`, `boundaries_scored`, `boundaries_given`, `number_of_dismissals`, `strike_rate`, `economy`, `batting_average`, `fantasy_points`
- **Importance:** Focuses on player performance at specific venues, allowing the model to factor in environmental and pitch conditions that can significantly influence outcomes.

### 🌦️ Weather Data
- **Columns:** `venue`, `start_date`, `latitude`, `longitude`, `temperature`, `precipitation`, `wind_speed`
- **Importance:** Records external environmental conditions during each match. Although its impact is relatively peripheral, it can offer insights into match dynamics.

### ⚔️ Player vs Player Dataset
- **Columns:** `player1_id`, `player1_name`, `player2_id`, `player2_name`, `match_date`, `runs_b1_b2`, `balls_b1_b2`, `boundaries_b1_b2`, `dismissals_b1_b2`, `runs_b2_b1`, `balls_b2_b1`, `boundaries_b2_b1`, `dismissals_b2_b1`, `strike_rate_b1_b2`, `strike_rate_b2_b1`, `economy_b1_b2`, `economy_b2_b1`, `fantasy_point_p1_p2`, `fantasy_point_p2_p1`
- **Importance:** Analyzes head-to-head encounters between players, quantifying the direct impact of player matchups. This data refines predictive power by highlighting individual interaction effects.

---

## 🧬 Training Data Preparation
### 📋 X_train Construction
- Data integrated from:
  - **800 days** of player vs opponent statistics
  - **180 days** of recent form data
  - **3000 days** of venue-specific performance
  - Integrated weather and match metadata
- **126 features per row**, totaling 45,000 rows in training data.

### 📋 Y_train: Dream Points Calculation
- Y_train represents the **actual Dream Points** scored by players, calculated using historical match statistics.
- **Captain/Vice-Captain logic is applied only in evaluation** to ensure unbiased training.

---

## 🤓 Modeling
### 🔧 XGBoost Model Configuration
```python
params = {
    'objective': 'reg:squarederror',
    'eval_metric': 'rmse',
    'max_depth': 5,
    'learning_rate': 0.01,
    'n_estimators': 250,
    'subsample': 0.6,
    'colsample_bytree': 0.8,
    'reg_alpha': 1,
    'reg_lambda': 1
}
```

---

## 🔮 Prediction Pipeline
- Predictions incorporate Dream11 scoring adjustments:
  - **Captain’s score × 2**
  - **Vice-Captain’s score × 1.5**

### 🧠 Interpretability via SHAP
- SHAP values highlight the **top 5 influential features** per player.

### 🗨️ Gemini API Integration
- Generates clear, human-readable explanations for each player's predicted performance.

---

## 🔢 Evaluation Metrics
- **Mean Absolute Error (MAE):** The core evaluation metric used. The model's MAE is **390 points** with an average predicted team score of **1014 points**.

--- 

## 📹Video Demo

- **[Click here to watch the demo video](https://drive.google.com/file/d/1Z_ZDy6rfrYn-GWxwrQGqFUYGfcIlLeuZ/view?usp=sharing)**

--- 


## 🌐 Deployment
### 🚀 Streamlit App
- Run the app using the command:
```bash
streamlit run app.py
```
- Users can easily select:
  - **Team A** and **Team B**
  - **Match Date**
  - Click **Predict** to generate the Dream11 team.

---

## 🏁 Conclusion
This project combines:
✅ Multi-source cricket data
✅ Sophisticated feature engineering
✅ A robust, unbiased XGBoost model
✅ Transparent interpretability with SHAP
✅ An intuitive Streamlit UI for seamless interaction
✅ Effective model training strategy with comprehensive data points and customized evaluation metrics
✅ Model designed to function without any player name bias, ensuring fair and precise results

---

## 📝 License
This project is licensed under the **MIT License**.

---

## 📧 Contact
For questions, suggestions, or collaborations, feel free to reach out. 😊 

mail-b23cy1021@iitj.ac.in

