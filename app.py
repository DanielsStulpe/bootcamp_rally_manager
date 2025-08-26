import os
import time
import random
import streamlit as st
import pandas as pd
from snowflake.snowpark import Session
from dotenv import load_dotenv

# -----------------------------
# Snowflake Connection
# -----------------------------
def create_session():
    load_dotenv()  # load variables from .env

    connection_parameters = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "user": os.getenv("SNOWFLAKE_USER"),
        "password": os.getenv("SNOWFLAKE_PASSWORD"),
        "role": os.getenv("SNOWFLAKE_ROLE"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
        "database": os.getenv("SNOWFLAKE_DATABASE"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA")
    }

    return Session.builder.configs(connection_parameters).create()

try:
    session = create_session()
except Exception as e:
    st.error(f"❌ Failed to connect to Snowflake: {e}")
    st.stop()

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🏎️ Bootcamp Rally Racing Manager")

menu = st.sidebar.radio(
    "Menu",
    ["Teams & Budgets", "Add Team", "Add Car", "Add Member", "Manage Team", "Start Race"]
)

# -----------------------------
# Teams & Budgets
# -----------------------------
if menu == "Teams & Budgets":
    st.header("📊 Teams Overview")

    # Fetch teams
    df_teams = session.sql(
        "SELECT team_id, team_name, budget FROM racing.teams ORDER BY team_id"
    ).to_pandas()

    if not df_teams.empty:
        st.subheader("Teams & Budgets")
        st.table(df_teams)

        st.markdown("<br><br>", unsafe_allow_html=True)

        # Fetch members and their cars
        st.subheader("Team Members & Cars")
        df_members = session.sql("""
            SELECT t.team_name, m.member_name, c.car_name
            FROM racing.team_members m
            LEFT JOIN racing.teams t ON m.team_id = t.team_id
            LEFT JOIN racing.cars c ON m.car_id = c.car_id
            ORDER BY t.team_name, m.member_name
        """).to_pandas()

        if df_members.empty:
            st.info("No members or cars added yet.")
        else:
            st.table(df_members)
    else:
        st.info("No teams found yet.")

# -----------------------------
# Add Team
# -----------------------------
elif menu == "Add Team":
    st.header("➕ Add a New Racing Team")

    team_name = st.text_input("Team Name")
    budget = st.number_input("Budget (EUR)", 10000, step=100)

    if st.button("Add Team"):
        query = f"""
        INSERT INTO racing.teams (team_name, budget)
        VALUES ('{team_name}', {budget})
        """
        session.sql(query).collect()
        st.success(f"✅ Team {team_name} with budget {budget} was created!")

# -----------------------------
# Add Car
# -----------------------------
elif menu == "Add Car":
    st.header("➕ Add a New Car")

    df_teams = session.sql(
        "SELECT team_id, team_name, budget FROM racing.teams ORDER BY team_id"
    ).to_pandas()

    if df_teams.empty:
        st.warning("⚠️ No teams available. Please insert teams first.")
    else:
        team_map = dict(zip(df_teams["TEAM_NAME"], df_teams["TEAM_ID"]))
        team_name = st.selectbox("Select Team", list(team_map.keys()))
        team_id = team_map[team_name]

        car_name = st.text_input("Car Name")
        base_speed = st.number_input("Base Speed (km/h)", 100, 300, 150)
        handling = st.slider("Handling (0-1)", 0.0, 1.0, 0.8)
        reliability = st.slider("Reliability (0-1)", 0.0, 1.0, 0.9)
        weight = st.number_input("Weight (kg)", 800, 2000, 1200)

        if st.button("Add Car"):
            query = f"""
            INSERT INTO racing.cars
            (team_id, car_name, base_speed_kmh, handling, reliability, weight_kg)
            VALUES
            ({team_id}, '{car_name}', {base_speed}, {handling}, {reliability}, {weight})
            """
            session.sql(query).collect()
            st.success(f"✅ Car {car_name} added to {team_name}!")

# -----------------------------
# Add Member
# -----------------------------
elif menu == "Add Member":
    st.header("➕ Add a New Team Member / Racer")

    # Fetch teams
    df_teams = session.sql(
        "SELECT team_id, team_name FROM racing.teams ORDER BY team_name"
    ).to_pandas()

    if df_teams.empty:
        st.warning("⚠️ No teams available. Please insert teams first.")
    else:
        team_map = dict(zip(df_teams["TEAM_NAME"], df_teams["TEAM_ID"]))
        team_name = st.selectbox("Select Team", list(team_map.keys()))
        team_id = team_map[team_name]

        member_name = st.text_input("Member / Racer Name")

        if st.button("Add Member"):
            if member_name.strip() == "":
                st.error("❌ Member name cannot be empty!")
            else:
                query = f"""
                INSERT INTO racing.team_members (team_id, member_name)
                VALUES ({team_id}, '{member_name}')
                """
                session.sql(query).collect()
                st.success(f"✅ Member {member_name} added to team {team_name}!")

# -----------------------------
# Manage Team
# -----------------------------
elif menu == "Manage Team":
    st.header("🛠️ Manage Team Cars & Racers")

    df_teams = session.sql("SELECT team_id, team_name FROM racing.teams").to_pandas()
    if df_teams.empty:
        st.warning("⚠️ No teams available.")
    else:
        team_map = dict(zip(df_teams["TEAM_NAME"], df_teams["TEAM_ID"]))
        team_name = st.selectbox("Select Team", list(team_map.keys()))
        team_id = team_map[team_name]

        df_racers = session.sql(
            f"SELECT member_id, member_name, car_id FROM racing.team_members WHERE team_id = {team_id}"
        ).to_pandas()
        df_racers.columns = df_racers.columns.str.lower()

        df_cars = session.sql(
            f"SELECT car_id, car_name FROM racing.cars WHERE team_id = {team_id}"
        ).to_pandas()
        df_cars.columns = df_cars.columns.str.lower()

        selected_cars = {}
        for _, row in df_racers.iterrows():
            st.subheader(f"Racer: {row['member_name']}")
            available_cars = ["None"] + df_cars["car_name"].tolist()

            if pd.notna(row["car_id"]):
                current_car_name = df_cars[df_cars["car_id"] == row["car_id"]]["car_name"].iloc[0]
                default_index = available_cars.index(current_car_name)
            else:
                default_index = 0

            selected_car = st.selectbox(
                f"Assign car for {row['member_name']}",
                available_cars,
                index=default_index,
                key=row['member_id']
            )
            selected_cars[row["member_id"]] = selected_car

        if st.button("Submit Assignments"):
            car_assignments = [v for v in selected_cars.values() if v != "None"]
            if len(car_assignments) != len(set(car_assignments)):
                st.error("❌ Each member must have a unique car! Please correct duplicates.")
            else:
                for member_id, car_name in selected_cars.items():
                    car_id = "NULL" if car_name == "None" else int(df_cars[df_cars["car_name"] == car_name]["car_id"])
                    session.sql(
                        f"UPDATE racing.team_members SET car_id = {car_id} WHERE member_id = {member_id}"
                    ).collect()
                st.success("✅ Cars assigned successfully!")

# -----------------------------
# Start Race
# -----------------------------
elif menu == "Start Race":
    st.header("🏁 Start Race Simulation")

    race_fee = 1000
    race_distance = 100  # km

    df_cars = session.sql("""
        SELECT c.car_id, c.car_name, c.team_id, t.team_name,
               c.base_speed_kmh, c.handling, c.reliability, c.weight_kg,
               tm.member_id, tm.member_name
        FROM racing.cars c
        JOIN racing.teams t ON c.team_id = t.team_id
        JOIN racing.team_members tm ON c.car_id = tm.car_id
    """).to_pandas()

    if df_cars.empty:
        st.warning("⚠️ No cars registered yet.")
    else:
        if st.button("Start Race"):
            race_name = f"Bootcamp Rally {time.strftime('%Y-%m-%d %H:%M:%S')}"
            session.sql(
                f"INSERT INTO racing.races (race_name, distance_km, fee_per_team) VALUES ('{race_name}', {race_distance}, {race_fee})"
            ).collect()

            race_id_df = session.sql(
                f"SELECT race_id FROM racing.races WHERE race_name = '{race_name}' ORDER BY race_id DESC LIMIT 1"
            ).to_pandas()
            race_id = int(race_id_df.iloc[0, 0])

            results = []
            for _, row in df_cars.iterrows():
                team_id = int(row["TEAM_ID"])
                car_id = int(row["CAR_ID"])

                session.sql(f"UPDATE racing.teams SET budget = budget - {race_fee} WHERE team_id = {team_id}").collect()

                speed_factor = row["BASE_SPEED_KMH"] * (0.82 + random.random() * 0.37)
                handling_factor = 1 + (row["HANDLING"] - 0.5) * random.uniform(0.8, 1.2)
                reliability_check = random.random() <= row["RELIABILITY"]

                if not reliability_check:
                    finished = False
                    time_seconds = None
                else:
                    finished = True
                    avg_speed = speed_factor * handling_factor * (1000 / (row["WEIGHT_KG"] / 1000))
                    time_hours = race_distance / avg_speed
                    time_seconds = time_hours * 3600

                results.append({
                    "car_id": car_id,
                    "team_id": team_id,
                    "car_name": row["CAR_NAME"],
                    "team_name": row["TEAM_NAME"],
                    "finished": finished,
                    "time_seconds": time_seconds,
                    "member_name": row["MEMBER_NAME"],
                    "position": None,
                    "prize": 0
                })

            finished_cars = [r for r in results if r["finished"]]
            finished_cars.sort(key=lambda x: x["time_seconds"])
            for pos, res in enumerate(finished_cars, start=1):
                prize = 0
                if pos == 1:
                    prize = 5000
                elif pos == 2:
                    prize = 3500
                elif pos == 3:
                    prize = 1500

                res["position"] = int(pos)
                res["prize"] = prize

                session.sql(
                    f"UPDATE racing.teams SET budget = budget + {prize} WHERE team_id = {res['team_id']}"
                ).collect()

                time_val = float(res["time_seconds"]) if res["time_seconds"] else None
                session.sql(
                    f"""INSERT INTO racing.race_results (race_id, car_id, team_id, finished, time_seconds, position, prize_money)
                    VALUES ({race_id}, {res['car_id']}, {res['team_id']}, {res['finished']}, {time_val}, {pos}, {prize})"""
                ).collect()

            df_results = pd.DataFrame([{
                "Position": None if not r["position"] else int(r["position"]),
                "Car": r["car_name"],
                "Team": r["team_name"],
                "Racer": r["member_name"],
                "Finished": r["finished"],
                "Time (s)": None if not r["finished"] else round(r["time_seconds"], 2),
                "Prize ($)": r["prize"]
            } for r in results]).sort_values(by="Position")

            st.success("🏆 Race completed!")
            st.table(df_results)
