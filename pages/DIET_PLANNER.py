import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils import call_llama_3, get_databricks_connection

st.title("AI-Powered Diet Planner")

# Initialize session state for storing meal plan
if 'meal_plan' not in st.session_state:
    st.session_state.meal_plan = pd.DataFrame(columns=['Date', 'Meal', 'Food', 'Calories', 'Protein', 'Carbs', 'Fat', 'Cuisine', 'created_at'])

# Function to save meal plan to Databricks
def save_to_databricks(meal_plan):
    with get_databricks_connection() as connection:
        with connection.cursor() as cursor:
            for _, row in meal_plan.iterrows():
                cursor.execute("""
                    INSERT INTO workspace.AI_GLADIATORS.meal_plans 
                    (date, meal, food, calories, protein, carbs, fat, cuisine, created_at) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (row['Date'], row['Meal'], row['Food'], row['Calories'], row['Protein'], row['Carbs'], row['Fat'], row['Cuisine'], row['created_at']))

# Cuisine selection
cuisine = st.selectbox("Select cuisine", ["Indian", "Italian", "Chinese", "Mexican", "Mediterranean"])
veg_non = st.selectbox("Select Diet", ["Veg","Non-Veg"])

# Calorie and protein goals
daily_calories = st.number_input("Daily calorie goal", min_value=1000, max_value=5000, value=2000, step=100)
daily_protein = st.number_input("Daily protein goal (g)", min_value=20, max_value=300, value=60, step=5)

# Generate meal plan button
if st.button("Generate Meal Plan"):
    st.session_state.meal_plan = pd.DataFrame(columns=['Date', 'Meal', 'Food', 'Calories', 'Protein', 'Carbs', 'Fat', 'Cuisine', 'created_at'])
    
    prompt = f"""Generate a 7-day meal plan with 3 meals per day (Breakfast, Lunch, Dinner) for {cuisine} cuisine and {veg_non} diet.
    The daily calorie goal is {daily_calories} calories with {daily_protein}g of protein.
    For each meal, provide:
    1. Name of the dish
    2. Estimated calories
    3. Estimated protein (g)
    4. Estimated carbs (g)
    5. Estimated fat (g)

    Present the information in a structured format for easy parsing, like this:

    Day 1:
    Breakfast: Dish Name | Calories: X | Protein: Xg | Carbs: Xg | Fat: Xg
    Lunch: Dish Name | Calories: X | Protein: Xg | Carbs: Xg | Fat: Xg
    Dinner: Dish Name | Calories: X | Protein: Xg | Carbs: Xg | Fat: Xg

    ... (continue for all 7 days)
    """

    response = call_llama_3(prompt, max_tokens=2000)
    
    if response:
        st.subheader("Generated Meal Plan")
        st.text(response)
        
        # Parse the response and create a DataFrame
        days = response.split("Day")[1:]  # Split by "Day" and remove the first empty element
        for day_num, day_plan in enumerate(days, start=1):
            meals = day_plan.strip().split("\n")[1:]  # Remove the "Day X:" line
            for meal in meals:
                if not meal.strip() or meal.strip() == '**':
                    continue  # Skip empty lines or lines with just asterisks
                try:
                    meal_parts = meal.split("|")
                    if len(meal_parts) < 5:
                        continue
                    meal_type_and_food = meal_parts[0].split(":", 1)
                    if len(meal_type_and_food) == 2:
                        meal_type, food = meal_type_and_food
                    else:
                        meal_type, food = "Unknown", meal_type_and_food[0]
                    
                    calories = int(meal_parts[1].split(":")[1].strip().rstrip("calories"))
                    protein = float(meal_parts[2].split(":")[1].strip().rstrip("g"))
                    carbs = float(meal_parts[3].split(":")[1].strip().rstrip("g"))
                    fat = float(meal_parts[4].split(":")[1].strip().rstrip("g"))
                    
                    new_meal = pd.DataFrame({
                        'Date': [datetime.now().date() + timedelta(days=day_num-1)],
                        'Meal': [meal_type.strip()],
                        'Food': [food.strip()],
                        'Calories': [calories],
                        'Protein': [protein],
                        'Carbs': [carbs],
                        'Fat': [fat],
                        'Cuisine': [cuisine],
                        'created_at': [datetime.now()]
                    })
                    st.session_state.meal_plan = pd.concat([st.session_state.meal_plan, new_meal], ignore_index=True)
                except Exception as e:
                    st.warning(f"Error parsing meal: {meal}. Error: {str(e)}")
        
        st.success("Meal plan generated successfully!")

# Display and confirm meal plan
if not st.session_state.meal_plan.empty:
    st.subheader("Generated Meal Plan")
    for i in range(7):
        day = datetime.now().date() + timedelta(days=i)
        st.write(f"**{day.strftime('%A, %B %d')}**")
        day_plan = st.session_state.meal_plan[st.session_state.meal_plan['Date'] == day]
        if not day_plan.empty:
            st.dataframe(day_plan[['Meal', 'Food', 'Calories', 'Protein', 'Carbs', 'Fat']])
        st.write("---")
    
    # if st.button("Accept and Save Meal Plan"):
    #     save_to_databricks(st.session_state.meal_plan)
    #     st.success("Meal plan saved to Databricks successfully!")

# Option to clear the meal plan
if st.button("Clear Meal Plan"):
    st.session_state.meal_plan = pd.DataFrame(columns=['Date', 'Meal', 'Food', 'Calories', 'Protein', 'Carbs', 'Fat', 'Cuisine', 'created_at'])
    st.success("Meal plan cleared successfully!")
