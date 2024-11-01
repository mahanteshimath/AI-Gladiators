# AI-Gladiators
This is for HEALY AI app https://healy-ai.streamlit.app/

# Healy AI - Your Health Companion

Welcome to **Healy AI**, your personal health monitoring application designed to help you track, improve, and maintain your well-being. With features ranging from symptom checking to diet planning, Healy AI is your all-in-one solution for a healthier lifestyle.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features
Healy AI offers the following features to support your health journey:
- 🤖 **AI Health Assistant**: Get instant answers to your health queries and receive guidance from our AI.
- 📊 **Health Tracker**: Track your vital health statistics over time, including blood pressure, heart rate, and more.
- 💊 **Medication Reminder**: Never miss a dose with our timely medication reminder system, ensuring you stay on track.
- 🍎 **Diet Planner**: Plan and track your meals for optimal nutrition and a balanced diet that suits your lifestyle.
- 🩺 **Symptom Checker**: Understand possible causes of your symptoms and get guidance on when to seek professional care.
- 🕵️‍♂️ **Food Inspector**: Help you understand food package ingredients and identify any hazardous or banned contents.

## Demo (Click to watch)


[![Watch the Demo](https://github.com/mahanteshimath/AI-Gladiators/blob/main/images/Designer.jpeg)](https://www.youtube.com/embed/rr4d_6AUSM8)


## Installation
To get started with Healy AI, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/mahanteshimath/AI-Gladiators.git
   cd AI-Gladiators
   ```

2. **Set Up the Environment:**
   It's recommended to create a virtual environment for this project.
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install Requirements:**
   Install the required Python packages using `pip`.
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. **Run the Application:**
   Start the Streamlit application by executing:
   ```bash
   streamlit run Home.py
   ```

2. **Accessing Features:**
   Once the application is running, you can access the following features from the sidebar:
   - **AI Health Assistant**: For instant health queries.
   - **Health Tracker**: To log and track your health metrics.
   - **Medication Reminder**: To set reminders for your medication schedule.
   - **Diet Planner**: To plan your meals and track nutritional intake.
   - **Symptom Checker**: To check symptoms and receive health insights.

## Project Structure
The project consists of the following files and directories:

```
.
├── .devcontainer
    └── devcontainer.json
├── .streamlit
    └── config.toml
├── Home.py
├── README.md
├── images
    └── Designer.jpeg
├── packages.txt
├── pages
    ├── 1_🤖_Health_Assistant.py
    ├── 2_📊_Health_Tracker.py
    ├── 3_💊_Medication_Reminder.py
    ├── 4_🍎_Diet_Planner.py
    ├── 5_🩺_Symptom_Checker.py
    └── 6_🕵️‍♂️_Food_Inspector.py
├── requirements.txt
├── samples
    ├── FoodContent.jpg
    ├── FoodContent.pdf
    ├── FoodContent.txt
    ├── Maggi.jpg
    └── product-label-sun-chips.jpg
├── style.css
└── utils.py
```

## Contributing
Contributions are welcome! If you have suggestions for improvements or want to contribute code, please fork the repository and submit a pull request.

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them.
4. Push to your branch and create a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Thank you for checking out Healy AI! Together, let's embark on a journey to better health and well-being.


Feel free to modify any sections as per your project's specific details or needs! If you have any further requests or changes, let me know!!!
