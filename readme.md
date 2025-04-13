for local ai agent 
local ai agent.py 

import requests

def ask_ollama(prompt, model="phi"):
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False
        })

        response.raise_for_status()  # Raise an error for bad HTTP codes

        data = response.json()

        # Debugging: print the full response
        if "response" not in data:
            print("⚠️ Full API response (no 'response' key):")
            print(data)
            return "❌ Error: 'response' key not found in API output."

        return data["response"]

    except Exception as e:
        return f"❌ Exception occurred: {e}"

if __name__ == "__main__":
    print("🤖 Your Local AI Coding Assistant (Ollama + CodeLlama)\n")
    while True:
        user_input = input("🧠 Ask a coding question (or type 'exit'): ")
        if user_input.lower() in ["exit", "quit"]:
            break
        output = ask_ollama(user_input)
        print(f"\n🧾 AI Says:\n{output}\n")
# Works in COnsole But need to install Ollama From CHrome

app.py web view 

from flask import Flask, render_template, request
import requests
import re
import markdown  # For rendering markdown nicely

app = Flask(__name__)

# 🔍 Step 1: Simple intent classifier
def classify_intent(prompt):
    prompt_lower = prompt.lower()
    if "write" in prompt_lower or "generate" in prompt_lower:
        return "code"
    elif "explain" in prompt_lower:
        return "explain"
    elif "error" in prompt_lower or "fix" in prompt_lower:
        return "fix"
    else:
        return "general"

# 🧠 Ask the local Ollama model
def ask_ollama(prompt, model="phi"):
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False
        })
        response.raise_for_status()
        data = response.json()

        # Optional: Extract code blocks wrapped in [PYTHON]...[/PYTHON]
        code_blocks = re.findall(r"\[PYTHON\](.*?)\[/PYTHON\]", data.get("response", ""), re.DOTALL)
        return code_blocks[0].strip() if code_blocks else data.get("response", "").strip()

    except Exception as e:
        return f"❌ Error: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    result_html = None
    intent = None
    if request.method == 'POST':
        prompt = request.form['prompt']
        intent = classify_intent(prompt)
        print(f"🧠 Detected intent: {intent}")

        raw_text = ask_ollama(prompt)

        # Markdown to HTML conversion with syntax highlighting
        result_html = markdown.markdown(
            raw_text,
            extensions=['fenced_code', 'codehilite']
        )

    return render_template('index.html', result=result_html)

if __name__ == "__main__":
    app.run(debug=True)

