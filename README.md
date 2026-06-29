# 🤖 Multi-Agent Local Blog Writing Pipeline

An automated, local multi-agent system powered by **Gemma 4** that collaborates to research topics, write beautiful blog posts in Markdown, and critically evaluate the draft with an editorial validation report.

This pipeline operates entirely on your laptop without using external AI API keys.

---

## 🛠️ Prerequisites & Installation

Follow these steps sequentially to set up your environment on a new machine.

### 1. Install Python
1. Download **Python 3.11 or newer** from the [Official Python Website](https://python.org).
2. Run the installer.
3. **CRITICAL STEP (Windows):** Check the box that says **"Add python.exe to PATH"** before clicking install.

### 2. Install Ollama & Gemma 4
1. Download and install **Ollama** from [Ollama's Official Website](https://ollama.com).
2. Once installed, open your terminal (or Git Bash) and download the **Gemma 4** model by running:
   ```bash
   ollama run gemma4:latest
   ```
3. Keep the Ollama application running in the background.

---

## 🚀 Setup and Execution Instructions

Open **VS Code**, open your project folder, and launch a **Git Bash** terminal panel to execute the following commands.

### 1. Initialize a Virtual Environment
Isolate your project dependencies from the rest of your computer:
```bash
# Create the environment folder named .venv
python -m venv .venv

# Activate the environment in Git Bash
source .venv/Scripts/activate
```
*Note: Once active, you will see `(.venv)` appear at the very beginning of your terminal line.*

### 2. Install Project Dependencies
Upgrade your package manager and install the lightweight network requirements:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Review Project File Structure
Ensure your local project workspace directory matches the following layout:
```text
my_agent_blog/
├── .venv/               # Virtual environment files (Generated automatically)
├── research_soul.md     # Persona/Rules for the Researcher Agent
├── summary_soul.md      # Persona/Rules for the Content Writer Agent
├── validation_soul.md   # Persona/Rules for the Chief Editor Agent
├── app.py               # Main multi-agent execution script
└── requirements.txt     # Library package requirements list
```

### 4. Run the Pipeline
Execute the main orchestrator script:
```bash
python app.py
```

---

## 📝 Workflow Details

When you run the script, the system will execute the following steps interactively:
1. **Interactive Prompt**: It will ask you: `What topic do you want the blog post to be about?`
2. **Research Agent**: Collects recent industry data, news, and technical developments.
3. **Summary Agent**: Ingests raw research points and formats a complete blog draft using Markdown layout structures (headers, lists, bold accents).
4. **Validation Agent**: Acts as an editor to critically grade your blog post based on **Relevance**, **Accuracy**, and **Readability**.

### 💾 Output Files
Once the system completes its run, it automatically saves two files directly to your folder:
* `draft_blog.md` - Your ready-to-publish Markdown article.
* `validation_report.md` - Your editor's actionable review checklist.

*Tip: Open `draft_blog.md` in VS Code and press `Ctrl + Shift + V` (`Cmd + Shift + V` on Mac) to view a live stylized visual preview of your new post!*
# blog_generator
allows local blog generation
