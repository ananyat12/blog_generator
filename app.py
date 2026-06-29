import json
import requests

# 1. Local Engine Settings (Matches Ollama / LM Studio)
LOCAL_API_URL = "http://localhost:11434/v1/chat/completions" # Adjust port to 1234 if using LM Studio

MODEL_NAME = "gemma4:latest"

def query_gemma_old(system_prompt, user_input):
    """Helper function to send prompts to your local Gemma 4 engine."""
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.3
    }
    try:
        response = requests.post(LOCAL_API_URL, json=payload)
        response.raise_for_status()
        return response.json()['choices']['message']['content']
    except Exception as e:
        return f"Error connecting to Gemma 4: {str(e)}"

def query_gemma(agent_name, system_prompt, user_input):
    """Helper function to stream responses from Gemma 4 via OpenAI-compatible endpoint."""
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.3,
        "stream": True 
    }
    
    print(f"   ⚙️  [DEBUG] Connecting to Ollama for {agent_name}...")
    
    try:
        response = requests.post(LOCAL_API_URL, json=payload, stream=True, timeout=180)
        response.raise_for_status()
        
        full_response = ""
        print(f"\n🗣️ [{agent_name} Response]: ", end="", flush=True)
        
        for line in response.iter_lines():
            if line:
                # Clean the OpenAI SSE format prefix ("data: ") if present
                line_str = line.decode('utf-8').strip()
                if line_str.startswith("data: "):
                    line_str = line_str[6:]
                if line_str == "[DONE]" or not line_str:
                    continue
                    
                try:
                    chunk = json.loads(line_str)
                    # Correctly index the OpenAI-compatible stream array structure
                    choices = chunk.get('choices', [])
                    if choices:
                        delta = choices[0].get('delta', {})
                        content = delta.get('content', '')
                        print(content, end="", flush=True)
                        full_response += content
                except json.JSONDecodeError:
                    continue
                
        print("\n")
        return full_response
        
    except Exception as e:
        print(f"\n   ❌ [ERROR]: Step failed. Details: {str(e)}")
        return f"Error: {str(e)}"


# 2. Read your agent profiles (Souls) from your VS Code workspace
def read_soul(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

if __name__ == "__main__":
    print("🤖 Initializing Multi-Agent System Locally...")
    
    # Load agent profiles from files
    research_soul = read_soul("research_soul.md")
    summary_soul = read_soul("summary_soul.md")
    validation_soul = read_soul("validation_soul.md")
    
    # INTERACTIVE USER INPUT FOR THE TOPIC
    print("\n--------------------------------------------------")
    topic = input("📝 What topic do you want the blog post to be about? ")
    print("--------------------------------------------------\n")
    
    # --- AGENT 1: RESEARCH AGENT ---
    print(f"\n[1/3] 🔍 Research Agent is gathering data points for '{topic}'...")
    # Add "Research_Agent" as the first argument below:
    research_output = query_gemma("Research_Agent", research_soul, f"Gather the core news and tech updates for the last 7 days regarding: {topic}")
    
    # --- AGENT 2: SUMMARY AGENT ---
    print("[2/3] ✍️ Summary Agent is drafting the blog post in Markdown...")
    # Add "Summary_Agent" as the first argument below:
    blog_post = query_gemma("Summary_Agent", summary_soul, f"Using these raw research notes, write the Markdown blog post:\n\n{research_output}")
    
    # --- AGENT 3: VALIDATION AGENT ---
    print("[3/3] 🔎 Validation Agent is evaluating the draft...")
    # Add "Validation_Agent" as the first argument below:
    validation_report = query_gemma("Validation_Agent", validation_soul, f"Critically evaluate this drafted blog post based on Relevance, Accuracy, and Readability:\n\n{blog_post}")
    
    # --- OUTPUT RESULTS & FILE SAVING ---
    print("\n================ SYSTEM COMPLETE ================\n")
    
    # 1. Save the Blog Post to a file named 'draft_blog.md'
    try:
        with open("draft_blog.md", "w", encoding="utf-8") as blog_file:
            blog_file.write(blog_post)
        print("💾 Success! Draft blog post saved to: draft_blog.md")
    except Exception as e:
        print(f"❌ Failed to save blog post: {str(e)}")
        
    # 2. Save the Validation Report to a file named 'validation_report.md'
    try:
        with open("validation_report.md", "w", encoding="utf-8") as report_file:
            report_file.write(validation_report)
        print("💾 Success! Validation report saved to: validation_report.md")
    except Exception as e:
        print(f"❌ Failed to save validation report: {str(e)}")

