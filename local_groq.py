from groq import Groq
import os

# Load the API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or "your_groq_api_key_here"

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

# Function to generate code based on the problem description
def generate_code_for_problem(problem_description):
    """Generates code to solve the problem described by the user."""
    prompt = f"Please generate a Python code to solve the following problem: {problem_description}"
    code = get_groq_response(prompt)
    return code

# Main function to interact with the user
def main():
    """Main function to drive the AI Code Generator Agent."""
    print("Welcome to the AI Code Generator Agent!")
    print("You can ask for code examples in any programming language.")
    print("Type 'exit' or 'quit' to stop the agent.")
    
    while True:
        # Get user input
        problem_description = input("\nDescribe the programming problem or ask for a code snippet: ")
        
        # Check if user wants to exit
        if problem_description.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        
        # Generate code based on the problem description
        print("\nGenerating code... Please wait.")
        code = generate_code_for_problem(problem_description)
        
        # Display the generated code
        print("\nGenerated Code:\n")
        print(code)

# Start the program
if __name__ == "__main__":
    main()
