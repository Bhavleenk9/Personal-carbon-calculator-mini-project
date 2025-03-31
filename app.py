import streamlit as st
import matplotlib.pyplot as plt
from db import create_table, insert_user_data, create_connection, check_table_exists

# Establish database connection
conn = create_connection()

# Ensure table exists at the start of the app
create_table(conn)

# Comprehensive dataset for 30+ countries
EMISSION_FACTORS = {
    "India": {"Transportation": 0.14, "Electricity": 0.82, "Diet": 1.25, "Waste": 0.1, "Water": 0.02},
    "United States": {"Transportation": 0.41, "Electricity": 0.45, "Diet": 1.77, "Waste": 0.18, "Water": 0.03},
    "China": {"Transportation": 0.12, "Electricity": 0.57, "Diet": 1.02, "Waste": 0.13, "Water": 0.01},
    "Germany": {"Transportation": 0.25, "Electricity": 0.42, "Diet": 1.5, "Waste": 0.15, "Water": 0.02},
    "France": {"Transportation": 0.2, "Electricity": 0.08, "Diet": 1.3, "Waste": 0.12, "Water": 0.02},
    "Brazil": {"Transportation": 0.18, "Electricity": 0.1, "Diet": 1.6, "Waste": 0.14, "Water": 0.02},
    "United Kingdom": {"Transportation": 0.23, "Electricity": 0.3, "Diet": 1.4, "Waste": 0.1, "Water": 0.02},
    "Canada": {"Transportation": 0.45, "Electricity": 0.2, "Diet": 1.8, "Waste": 0.17, "Water": 0.03},
    "Australia": {"Transportation": 0.5, "Electricity": 0.55, "Diet": 1.75, "Waste": 0.15, "Water": 0.03},
    "Russia": {"Transportation": 0.3, "Electricity": 0.6, "Diet": 1.1, "Waste": 0.13, "Water": 0.02},
    "Japan": {"Transportation": 0.25, "Electricity": 0.5, "Diet": 1.2, "Waste": 0.1, "Water": 0.02},
    "South Korea": {"Transportation": 0.27, "Electricity": 0.65, "Diet": 1.3, "Waste": 0.12, "Water": 0.02},
    "South Africa": {"Transportation": 0.3, "Electricity": 0.85, "Diet": 1.4, "Waste": 0.14, "Water": 0.02},
    "Mexico": {"Transportation": 0.22, "Electricity": 0.35, "Diet": 1.5, "Waste": 0.13, "Water": 0.02},
    "Italy": {"Transportation": 0.19, "Electricity": 0.25, "Diet": 1.35, "Waste": 0.12, "Water": 0.02},
    "Spain": {"Transportation": 0.2, "Electricity": 0.3, "Diet": 1.4, "Waste": 0.13, "Water": 0.02},
    "Argentina": {"Transportation": 0.21, "Electricity": 0.4, "Diet": 1.6, "Waste": 0.12, "Water": 0.02},
    "Turkey": {"Transportation": 0.23, "Electricity": 0.45, "Diet": 1.3, "Waste": 0.14, "Water": 0.02},
    "Indonesia": {"Transportation": 0.2, "Electricity": 0.7, "Diet": 1.3, "Waste": 0.12, "Water": 0.02},
}

# Initialize the app
st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")

if "page" not in st.session_state:
    st.session_state.page = 1

def next_page():
    st.session_state.page += 1

def previous_page():
    st.session_state.page -= 1

# **Page 1: Personal Information**
if st.session_state.page == 1:
    st.title("🌱 Personal Carbon Calculator")

    with st.form("user_info"):
        st.subheader("Enter your details")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120, value=25)
        gender = st.radio("Gender", ["Male", "Female", "Other"])
        submitted = st.form_submit_button("Next")

    if submitted:
        st.session_state.name = name
        st.session_state.age = age
        st.session_state.gender = gender
        next_page()

# **Page 2: Lifestyle & Consumption**
elif st.session_state.page == 2:
    st.title(f"Hello, {st.session_state.name}! Let's calculate your footprint.")

    with st.form("lifestyle_data"):
        st.subheader("Your Habits")
        country = st.selectbox("Select your country", list(EMISSION_FACTORS.keys()))
        distance = st.slider("🚗 Daily commute (km)", 0, 100, 10)
        electricity = st.slider("💡 Monthly electricity (kWh)", 0, 1000, 200)
        waste = st.slider("🗑️ Weekly waste (kg)", 0, 100, 5)
        meals = st.number_input("🍽️ Meals per day", min_value=1, max_value=10, value=3)
        water = st.slider("💧 Daily water usage (liters)", 0, 500, 100)
        submitted = st.form_submit_button("Calculate")

    if submitted:
        st.session_state.country = country
        st.session_state.distance = distance
        st.session_state.electricity = electricity
        st.session_state.waste = waste
        st.session_state.meals = meals
        st.session_state.water = water
        next_page()

    if st.button("Back"):
        previous_page()
        # Reset all session states if needed
        del st.session_state.name
        del st.session_state.age
        del st.session_state.gender
        del st.session_state.country
        del st.session_state.distance
        del st.session_state.electricity
        del st.session_state.waste
        del st.session_state.meals
        del st.session_state.water

# **Page 3: Results & Recommendations**
elif st.session_state.page == 3:
    st.title("📊 Your Carbon Footprint Results")

    country = st.session_state.country
    distance_yearly = st.session_state.distance * 365
    electricity_yearly = st.session_state.electricity * 12
    meals_yearly = st.session_state.meals * 365
    waste_yearly = st.session_state.waste * 52
    water_yearly = st.session_state.water * 365

    transportation = EMISSION_FACTORS[country]["Transportation"] * distance_yearly / 1000
    electricity = EMISSION_FACTORS[country]["Electricity"] * electricity_yearly / 1000
    diet = EMISSION_FACTORS[country]["Diet"] * meals_yearly / 1000
    waste = EMISSION_FACTORS[country]["Waste"] * waste_yearly / 1000
    water = EMISSION_FACTORS[country]["Water"] * water_yearly / 1000

    total = transportation + electricity + diet + waste + water

    categories = ["Transportation", "Electricity", "Diet", "Waste", "Water"]
    values = [transportation, electricity, diet, waste, water]

    st.success(f"🌍 Your total footprint: **{total:.2f} tonnes CO2 per year**")
    fig, ax = plt.subplots()
    ax.pie(values, labels=categories, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    st.subheader("🔻 Reduction Tips")
    st.write("- Use public transport or cycle more.")
    st.write("- Reduce electricity consumption.")
    st.write("- Shift to a plant-based diet.")
    st.write("- Recycle and compost waste.")
    st.write("- Reduce water wastage.")

    # Insert data into the database
    user_data = (
        st.session_state.name, st.session_state.age, st.session_state.gender, st.session_state.country,
        st.session_state.distance, st.session_state.electricity, st.session_state.waste, st.session_state.meals,
        st.session_state.water, transportation, electricity, diet, waste, water, total
    )
    insert_user_data(conn, user_data)

    st.subheader("📊 More Data on Carbon Footprint Emissions")
    st.write("Here are some global insights about carbon footprint emissions:")
    st.write("- **Global transportation**: Accounts for around 14% of global greenhouse gas emissions.")
    st.write("- **Electricity and heat production**: Contributes to over 25% of global emissions.")
    st.write("- **Agriculture**: Responsible for approximately 24% of emissions, with diet being a significant factor.")
    st.write("- **Waste**: Waste management and disposal contribute to around 5% of total global emissions.")
    st.write("- **Water use**: Water extraction, treatment, and distribution also contribute to carbon emissions, though less than other sectors.")

    # Acknowledgment
    st.subheader("Acknowledgments")
    st.write("""
    This project is made by the following people:
    - Bhavleen Kaur
    - Faizan Hamid
    - Mehak Sharma
    - Sadhana Rao
    - Prajjwal Gupta

    Under the supervision of Ms. Somdatta Patra.
    """)

    if st.button("Start Over"):
        st.session_state.page = 1
        # Reset session states when starting over
        del st.session_state.name
        del st.session_state.age
        del st.session_state.gender
        del st.session_state.country
        del st.session_state.distance
        del st.session_state.electricity
        del st.session_state.waste
        del st.session_state.meals
        del st.session_state.water
