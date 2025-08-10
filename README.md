#  SmartBlog: Smart Blogging Platform

Welcome to **SmartBlog**, a modern, full-stack blogging application built from the ground up to showcase a powerful combination of Python, FastAPI, and Google's Gemini API. This project is a comprehensive, hands-on guide to building a feature-rich web application with a professional UI/UX.

SmartBlog allows users to register, create, manage, and delete their blog posts, interact with content through comments, and leverage AI to enhance their writing process.

---

## Features

- **Full User Authentication**: Secure user registration and login system using JWT (JSON Web Tokens).
- **Complete Post Management (CRUD)**: Logged-in users can Create, Read, Update, and Delete their own blog posts.
- **AI-Powered Writing Tools (Gemini API)**:
    - **Suggest Title**: Automatically generate a compelling title from the post's content.
- **Rich Markdown Editor**: A beautiful side-by-side editor with a live preview for writing content.
---

## Tech Stack

- **Backend**: **Python** with **FastAPI**
- **Database**: **SQLite** with **SQLAlchemy ORM**
- **Authentication**: **Passlib** (for password hashing) & **python-jose** (for JWT)
- **AI Integration**: **Google Gemini API** (`google-generativeai`)
- **Frontend**: **HTML5**, **TailwindCSS**, and vanilla **JavaScript**
- **Markdown Parsing**: **`marked.js`**
- **Server**: **Uvicorn**

---

## Setup and Installation

Follow these steps to get the project running on your local machine.

### 1. Clone the Repository
First, get the project files. If you don't have a repository, simply place all the project files into a folder named `smartblog`.

### 2. Create and Activate a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# Navigate into your project directory
cd smartblog

# Create a virtual environment
python -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# Or activate it (Windows)
.\venv\Scripts\activate
```

### 3. Install Dependencies
Install all the required Python packages using `pip`.

```bash
pip install -r requirements.txt
```

### 4. Set Up Your Gemini API Key
This project uses the Google Gemini API for its AI features.

1.  Get your free API key from **[Google AI Studio](https://aistudio.google.com/)**.
2.  Set this key as an environment variable. This is the most secure way to handle API keys.

    - **On macOS / Linux:**
      ```bash
      export GOOGLE_API_KEY="YOUR_API_KEY_HERE"
      ```
    - **On Windows (Command Prompt):**
      ```bash
      set GOOGLE_API_KEY="YOUR_API_KEY_HERE"
      ```

### 5. Run the Application
With your virtual environment active and the API key set, start the server using Uvicorn.

```bash
uvicorn main:app --reload
```

Your SmartBlog application is now running! Open your browser and navigate to **`http://127.0.0.1:8000`**.

---

## How to Use

1.  **Register a New Account**: Click the "Register" button on the homepage to create a new user.
2.  **Login**: Sign in with your new credentials.
3.  **Explore the Dashboard**: After logging in, you'll see a "Dashboard" link. Here you can:
    - **Create a Post**: Use the Markdown editor to write your content. Try the "✨ Suggest Title" button to see the AI in action!
    - **Manage Your Posts**: View a list of your posts, edit them, or delete them.
4.  **Edit Your Profile**: Click the "My Profile" link in the header to update your name, bio, social links, and privacy settings.
5.  **View Posts and Profiles**: Click on any post title to view its full content and comment section. Click on an author's name to see their public profile and all their posts.
