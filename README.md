# Visual Math Worksheet Generator (Pre-K/G1)

A simple web application built with Python and Flask to generate engaging, downloadable PDF math worksheets for Kindergarten and First Grade Students.

This tool is designed to help young learners bridge the gap between abstract numbers and concrete quantities by using a colorful, visual bar method.


## 🌟 Features

* **Visual Learning:** Each number (0-10) is paired with a corresponding number of colorful vertical bars (e.g., `5` is `|||||`) to aid in counting.
* **Engaging Design:**
    * Numbers and bars are colored to make learning more fun.
    * Adjacent problems use different color pairs to keep the page visually interesting.
    * Each page features a friendly, colorful flower border.
* **Customizable Worksheets:**
    * Choose between **Addition (+)** or **Subtraction (-)**.
    * Select **1 Page (18 problems)** or **2 Pages (36 problems)**.
* **Smart Subtraction:** The "**top number >= bottom number**" rule is automatically applied to subtraction problems to prevent negative answers.
* **PDF Download:** Generates a high-quality, print-ready PDF document with one click.

## 🛠️ Technologies Used

* **Backend:** [Python](https://www.python.org/)
* **Web Framework:** [Flask](https://flask.palletsprojects.com/)
* **PDF Generation:** [ReportLab](https://www.reportlab.com/opensource/)
* **Frontend:** HTML & [Tailwind CSS](https://tailwindcss.com/)

## 🚀 How to Run Locally

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd your-repository-name
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    Make sure you have the `requirements.txt` file in your directory.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the App:**
    ```bash
    python visual_math_sheet.py
    ```

5.  **View in Browser:**
    Open your web browser and go to `http://127.0.0.1:5000`

## ☁️ Deployment

This application is ready to be deployed to any PaaS (Platform as a Service) that supports Python, such as [Render](https://render.com/) or [PythonAnywhere](https://www.pythonanywhere.com/).

### Example: Render Deployment

1.  Push this repository (including `visual_math_sheet.py` and `requirements.txt`) to GitHub.
2.  Create a new "Web Service" on Render and connect it to your GitHub repository.
3.  Set the **Start Command** to: `gunicorn visual_math_sheet:app`

Render will automatically install the packages from `requirements.txt` and start the server.
