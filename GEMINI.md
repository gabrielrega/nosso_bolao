# Project Overview

This project is a web application for a "Bolão" (betting pool) for the FIFA World Cup 2026, built using Python and the Streamlit framework. It allows multiple participants to enter their predictions for all matches of the tournament, from the group stage to the final. The application calculates points based on a predefined set of rules and displays a general ranking.

## Main Technologies

*   **Backend:** Python
*   **Web Framework:** Streamlit
*   **Data Handling:** Pandas for data manipulation and a simple JSON file (`bolao_db.json`) for data persistence.

## Architecture

The application is contained within a single `app.py` script.

*   **Data Model:** The application's state, including participant predictions and official results (gabarito), is stored in a JSON file (`bolao_db.json`).
*   **Core Logic:**
    *   Match data and tournament structure are hardcoded in the script.
    *   The `calcular_pontos` function contains the business logic for scoring predictions against the official results.
*   **User Interface:**
    *   Built entirely with Streamlit components.
    *   A sidebar navigates between three main sections:
        1.  **Meus Palpites:** Where users enter their name and predictions.
        2.  **Ranking Geral:** Displays a leaderboard of all participants.
        3.  **Área Admin:** A password-protected section for the administrator to input the actual match results.

# Building and Running

This is a Streamlit project. To run it, you need Python and the required libraries installed.

1.  **Install dependencies:**
    ```bash
    pip install streamlit pandas
    ```

2.  **Run the application:**
    ```bash
    streamlit run app.py
    ```
    The application will be available at `http://localhost:8501`.

# Development Conventions

*   The application follows a simple, single-file script structure.
*   Data is stored in a local JSON file, making it easy to inspect and manage for small-scale use.
*   The admin password is read from the `ADMIN_PASSWORD` environment variable, defaulting to `admin123` if not set. This allows for more secure password management in a production environment.
*   The UI is organized into tabs and expanders for a compact user experience.
