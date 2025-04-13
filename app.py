from flask import Flask, render_template, request
from groq import Groq
import os

# Load the API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or "your_groq_api_key_here"

# Initialize Flask app
app = Flask(__name__)

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

# Function to send the user's prompt to the Groq API and get the response
def get_groq_response(prompt):
    """Sends a prompt to Groq API and returns the response."""
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",  # Use the model Groq provides (you can check documentation for more models)
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7  # Control creativity of the response (higher = more creative)
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error occurred: {str(e)}"

# Route for the homepage
@app.route("/", methods=["GET", "POST"])
def index():
    """Render the home page and handle form submissions."""
    if request.method == "POST":
        # Get the programming problem description from the form
        problem_description = request.form["problem_description"]
        
        # Generate the code
        code = get_groq_response(problem_description)
        
        return render_template("index.html", code=code, problem_description=problem_description)

    return render_template("index.html", code=None)

if __name__ == "__main__":
    app.run(debug=True)
