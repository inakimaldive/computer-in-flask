# Flask-Computer-in-a-Browser

This project is a Flask application that provides a simple web interface for creating and managing content. It uses HTMX for dynamic content updates and GitHub Actions to automate content creation.

## Features

- **Landing Page:** A simple landing page with a navigation bar.
- **Show Time:** A page that displays the current date and time, updated every second using HTMX.
- **Create Post:** A form that allows users to create new posts. When a user submits the form, a GitHub Action is triggered to create a new markdown file in the `/contents` directory.

## How it Works

The application is built with Flask and uses a few key technologies:

- **HTMX:** Used for the real-time clock feature, allowing the frontend to update without a full page reload.
- **GitHub Actions:** Automates the creation of new posts. When a user submits the "Create Post" form, a workflow is triggered that creates a new markdown file in the `contents` directory.

## Running Locally

To run the application locally, you will need to have Python and Flask installed.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/inakimaldive/computer-in-flask.git
    ```
2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up the `GITHUB_TOKEN`:**
    To use the "Create Post" feature, you will need to create a GitHub personal access token with the `repo` and `workflow` scopes. Add this token as an environment variable named `GITHUB_TOKEN`.
    ```bash
    export GITHUB_TOKEN="your_github_token"
    ```
4.  **Run the application:**
    ```bash
    ./start_server.sh
    ```
The application will be available at `http://localhost:5001`.

## One-Click Deploy

You can also deploy this application to Vercel with a single click:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Finakimaldive%2Fcomputer-in-flask)


## rememeber

Grant write permission to GitHub Actions

Go to your repo settings:

    Settings → Actions → General

    Scroll down to Workflow permissions

    Select:

        ✅ Read and write permissions

    Click Save