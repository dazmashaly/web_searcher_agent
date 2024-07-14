
# Custom Agent

A custom websearch agent useable with Gimini, Ollama, OpenAI and vLLM.

### Agent Schema:
![Agent Schema](schema/Agent%20Schema.png)

   
#### Setup Ollama Server
1. **Download Ollama:**
   Download [https://ollama.com/download](Ollama)

2. **Download an Ollama Model:**
   ```bash
   curl http://localhost:11434/api/pull -d "{\"name\": \"llama3\"}"
   ```
Ollama[https://github.com/ollama/ollama/blob/main/docs/api.md#list-local-models](API documentionation)

### Clone and Navigate to the Repository
1. **Clone the Repo:**
   ```bash
   git clone https://github.com/john-adeojo/custom_agent_tutorial.git
   ```

2. **Navigate to the Repo:**
   ```bash
   cd /path/to/your-repo/custom_agent_tutorial
   ```

3. **Install Requirements:**
   ```bash
   pip install -r requirements.txt
   ```


### Configure API Keys
1. **Open the `config.yaml`:**
   ```bash
   nano config.yaml
   ```

2. **Enter API Keys:**
   - **Serper API Key:** Get it from [https://serper.dev/](https://serper.dev/)
   - **OpenAI API Key:** Get it from [https://openai.com/](https://openai.com/)
   - **Gemini API Key:** Get it from [https://ai.google.dev/gemini-api](https://ai.google.dev/gemini-api)
   - **Claude API Key:** Get it from [https://docs.anthropic.com/en/api/getting-started](https://docs.anthropic.com/en/api/getting-started)
   - **Groq API Key:** Get it from [https://console.groq.com/keys](https://console.groq.com/keys)


   the default model is gimini-1.5-pro
### Run Your Query
```bash
python agent.py 
```
Then enter your query.

inspired by
[https://www.youtube.com/@Data-Centric](Data centric)
