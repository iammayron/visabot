# Appointment Scheduler Bot for US Consulate

This project is a robot designed to schedule appointments at the US consulate for Brazilians. Follow the steps below to install the necessary dependencies and run the bot.

---

## Table of Contents
1. [Installing Python](#installing-python)
   - [Windows](#windows)
   - [Mac](#mac)
   - [Linux](#linux)
2. [Setting up the Project](#setting-up-the-project)
3. [Running the Bot](#running-the-bot)
4. [Push Notification](#using-pushover-for-notifications)

---

## Installing Python

### Windows
1. Download Python from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/).
2. Run the installer.
3. **Important**: During installation, check the box for **"Add Python to PATH"**.
4. Verify the installation:
   ```bash
   python --version
   ```
5.	Install pip if it’s not already installed:
    ```bash
    python -m ensurepip
    ```

### Mac

1.	Open the Terminal.
2.	Check if Python is installed:
    ```bash
    python3 --version
    ```
    If not, install Python using Homebrew:
    ```bash
    brew install python
    ```
3.	Verify the installation:
    ```bash
    python3 --version
    ```

### Linux

1.	Open the Terminal.
2.	Install Python using your package manager:
    - Ubuntu/Debian:
        ```bash
        sudo apt update
        sudo apt install python3 python3-pip
        ```
	- Fedora:
        ```bash
        sudo dnf install python3 python3-pip
        ```
3.	Verify the installation:
    ```bash
    python3 --version
    ```

## Setting up the Project

1.	Clone or download the repository to your local machine.
2.	Open the Terminal (or Command Prompt/PowerShell on Windows).
3.	Navigate to the project folder:
    ```bash
    cd path/to/project
    ```
4.	Run the setup script:
    ```bash
    ./setup.sh
    ```
    This script will:
	 - Install all Python dependencies listed in the requirements.txt file.

## Running the Bot

1.	Prepare the .env File:
    - Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
    - Open the .env file in a text editor and set the following variables:
	    - **EMAIL**: Your email address.
	    - **PASSWORD**: Your password.
	    - **SCHEDULE_ID**: The ID of the schedule you are targeting.
	    - **CONSULATE_SCHEDULED_DATE**: Current scheduled date. (Format: YYYY-MM-DD)
	    - **CONSULATE_SCHEDULED_STATE**: The Brazilian state where you will to schedule the appointment. (Brasília, Porto Alegre, Recife, Rio de Janeiro, São Paulo)
        - **BIOMETRICS_SCHEDULED_STATE**: The Brazilian state where you will schedule the appointment for the biometrics (Optional). (Brasília, Rio de Janeiro, São Paulo)
	    - Optional: Specify the desired date and time range:
	        - **SCHEDULE_CONSULATE_DATE_FROM** and **SCHEDULE_CONSULATE_DATE_TO** (Format: YYYY-MM-DD)
	        - **SCHEDULE_TIME_FROM** and **SCHEDULE_TIME_TO** (Format: HH:MM)
	    - Optional: Enable free push notifications using Pushover.

2.	Run the bot:
    - Windows:
        ```bash
        python main.py
        ```
    - Linux / Mac:
        ```bash
        python3 main.py
        ```


## Using Pushover for Notifications

The bot can send notifications to your computer or mobile device via Pushover.

1.	Create an account at pushover.net.
2.	Copy your User Key and add it to .env as PUSHOVER_USER.
3.	Create a new application on Pushover:
•	Copy the API Token and add it to .env as PUSHOVER_TOKEN.
4.	Ensure PUSHOVER_ENABLED is set to true.

Note: Notifications will include an audible alert on your computer.

---

#### Notes

- Ensure you have a stable internet connection.
- If you encounter errors during setup, make sure pip and Python are installed correctly.
- Use pushover to receive real-time updates about appointment availability.
