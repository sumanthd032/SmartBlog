import os
import google.generativeai as genai

# For development, you can set the key directly. 
# For production, it's better to use environment variables.
# os.environ['GOOGLE_API_KEY'] = "YOUR_API_KEY_HERE"
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# Initialize the Gemini Model
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_title(content: str) -> str:
    """Generates a blog post title from its content using Gemini."""
    if not content:
        return "Please provide content to generate a title."
        
    prompt = f"""
    Based on the following blog post content, suggest a single, compelling, and SEO-friendly title.
    The title should be concise and no more than 70 characters.

    Content:
    ---
    {content[:1000]}
    ---

    Suggested Title:
    """
    try:
        response = model.generate_content(prompt)
        # Clean up the response to remove potential markdown or quotes
        return response.text.strip().replace('"', '').replace('*', '')
    except Exception as e:
        print(f"Error generating title: {e}")
        return "Error: Could not generate title."


def generate_summary(content: str) -> str:
    """Generates a short summary (TL;DR) of the blog post."""
    if not content:
        return "Please provide content to generate a summary."

    prompt = f"""
    Based on the following blog post content, generate a short, engaging summary or "TL;DR" (Too Long; Didn't Read).
    The summary should be around 2-3 sentences and capture the main points of the article.

    Content:
    ---
    {content[:2000]}
    ---

    Summary:
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Error: Could not generate summary."