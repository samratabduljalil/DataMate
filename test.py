import os
import subprocess

def query_ollama(model, prompt):
    try:
        # Dynamically add Ollama's path
        os.environ["PATH"] += ";C:\\Users\\samra\\.ollama"

        # Run Ollama from Python
        result = subprocess.run(
            ["ollama", "generate", "--model", model],  # Adjust command based on available commands
            input=prompt,
            text=True,
            capture_output=True
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr.strip()}"
    except FileNotFoundError:
        return "Ollama executable not found. Ensure it is installed and added to PATH."
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Example usage
model_name = "llama2-7b"
prompt_text = "What is quantum mechanics?"
response = query_ollama(model_name, prompt_text)
print(response)
