# pages/5_Diet_Planner.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils import call_llama_3

st.title("Diet Planner")

# Initialize session state for storing meal plan
if 'meal_plan' not in st.session_state:
    st.session_state.meal_plan = pd.DataFrame(columns=['Date', 'Meal', 'Food', 'Calories', 'Protein', 'Carbs', 'Fat'])

# Function to calculate total nutrients for a day
def calculate_daily_totals(date):
    day_data = st.session_state.meal_plan[st.session_state.meal_plan['Date'] == date]
    return {
        'Calories': day_data['Calories'].sum(),
        'Protein': day_data['Protein'].sum(),
        'Carbs': day_data['Carbs'].sum(),
        'Fat': day_data['Fat'].sum()
    }

# Date selection
selected_date = st.date_input("Select date for meal planning", datetime.now())

# Meal selection
meal = st.selectbox("Select meal", ["Breakfast", "Lunch", "Dinner", "Snack"])

# Food input
food = st.text_input("Enter food item")

# Nutrient inputs
col1, col2, col3, col4 = st.columns(4)
with col1:
    calories = st.number_input("Calories", min_value=0, step=1)
with col2:
    protein = st.number_input("Protein (g)", min_value=0.0, step=0.1)
with col3:
    carbs = st.number_input("Carbs (g)", min_value=0.0, step=0.1)
with col4:
    fat = st.number_input("Fat (g)", min_value=0.0, step=0.1)

# Add meal button
if st.button("Add to Meal Plan"):
    new_meal = pd.DataFrame({
        'Date': [selected_date],
        'Meal': [meal],
        'Food': [food],
        'Calories': [calories],
        'Protein': [protein],
        'Carbs': [carbs],
        'Fat': [fat]
    })
    st.session_state.meal_plan = pd.concat([st.session_state.meal_plan, new_meal], ignore_index=True)
    st.success(f"Added {food} to {meal} for {selected_date}")

# Display weekly meal plan
st.subheader("Weekly Meal Plan")
start_of_week = selected_date - timedelta(days=selected_date.weekday())
end_of_week = start_of_week + timedelta(days=6)
week_plan = st.session_state.meal_plan[
    (st.session_state.meal_plan['Date'] >= start_of_week) & 
    (st.session_state.meal_plan['Date'] <= end_of_week)
]

for i in range(7):
    day = start_of_week + timedelta(days=i)
    st.write(f"**{day.strftime('%A, %B %d')}**")
    day_plan = week_plan[week_plan['Date'] == day]
    if not day_plan.empty:
        st.dataframe(day_plan[['Meal', 'Food', 'Calories', 'Protein', 'Carbs', 'Fat']])
        totals = calculate_daily_totals(day)
        st.write(f"Daily Totals: Calories: {totals['Calories']}, Protein: {totals['Protein']}g, Carbs: {totals['Carbs']}g, Fat: {totals['Fat']}g")
    else:
        st.write("No meals planned for this day.")
    st.write("---")

# Generate nutritional advice using Llama 3
if not st.session_state.meal_plan.empty:
    st.subheader("Nutritional Analysis and Advice")
    prompt = f"""Analyze the following weekly meal plan and provide friendly, personalized nutritional advice:

    {week_plan.to_string()}

    Consider the following points in your analysis:
    1. Overall balance of macronutrients (protein, carbs, fat)
    2. Calorie intake and its appropriateness (assume an average adult)
    3. Variety of foods and nutrients
    4. Suggestions for improvements or additions
    5. General healthy eating tips based on this plan

    Provide your analysis in a friendly, encouraging tone."""

    response = call_llama_3(prompt)
    if response:
        st.info(response)

# Option to clear the meal plan
if st.button("Clear Meal Plan"):
    st.session_state.meal_plan = pd.DataFrame(columns=['Date', 'Meal', 'Food', 'Calories', 'Protein', 'Carbs', 'Fat'])
    st.success("Meal plan cleared successfully!")