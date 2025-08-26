# Bootcamp Rally Racing Manager

This project was developed as part of an **assessment in the Data Engineering Bootcamp**. It demonstrates how to combine **Snowflake** and **Streamlit** to build an interactive racing team manager and race simulation app.

---

## 📂 Project Structure

- **`snf_script.sql`** – SQL script to create the required Snowflake schema, tables, and initial data setup.
- **`app.py`** – Main Streamlit application that connects to Snowflake via Snowpark and provides the interactive UI.
- **`requirements.txt`** – List of Python dependencies to install for running the app.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/DanielsStulpe/bootcamp_rally_manager
cd bootcamp_rally_manager
```

### 2. Create Virtual Environment (optional but recommended)
```bash
python -m venv venv
# Activate it
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a **.env** file in the project root with your Snowflake credentials:
```env
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account_identifier
SNOWFLAKE_ROLE=your_role
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
```

### 5. Setup Snowflake Schema
Run the `snf_script.sql` in your Snowflake environment to create required tables and schema.

### 6. Run the App
```bash
streamlit run app.py
```

---

## 🎮 Features
- Manage **teams** and their budgets.
- Add **cars** with attributes like speed, handling, reliability, and weight.
- Add **members/racers** and assign cars to them.
- Manage team rosters interactively.
- Start a **race simulation** with dynamic results influenced by performance factors.
- Track **budgets, rankings, and prizes** across races.

---

## 🛠️ Technologies Used
- **Python**
- **Streamlit** for the frontend UI
- **Snowflake** with **Snowpark** for data management
- **Pandas** for data handling
- **dotenv** for environment variable management

---

## 📌 Notes
- This project was designed for educational purposes as part of the Data Engineering Bootcamp.
- Make sure you have access to a Snowflake account with permissions to create schemas, tables, and run queries.
