# RAG-WYnova
This is the pratical test for the AI engineer position at WYnova.

## Overview
The goal of this project is to demonstrate the ability to build a minimal Retrieval-Augmented Generation (RAG) application in a standardized way. 
My project uses the European Union's PDF on Fundamental Rights as a knowledge base, which is available on the [European Union website](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A12012P%2FTXT).

# Run and Test Locally
## Pre-requesites
Ensure you have the following installed:
- Python (tested with version 3.12.3, but it may work with others): [Download and Installation Guide](https://www.python.org/downloads/)
- If using Docker to run locally: [Installation Guide](https://docs.docker.com/engine/install/)

## Steps
### Clone the Repository
- Clone the repository:
```bash
git clone https://github.com/diogofranciscop/RAG-WYnova
```
- Change into the project directory:
``` bash
cd your/path/RAG-WYnova
```
### API Key setup
- Get your [groq API key](https://console.groq.com/keys)
- Save the API key in a `.env` file:
```bash
GROQ_API_KEY=your_api_key
```
- **Important**: Ensure that the .env file is listed in the .gitignore file to prevent accidental exposure of the API.
#### Using CLI
- Start by initializing a virtual environment:
```bash
python -m venv ven
```
- Activate the virtual environment:
```bash
source venv/bin/activate
```
- Install the requirements:
```bash
pip install -r requirements.txt
```
- Run the application locally:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- Test the endpoint:
```bash
curl -X POST "http://127.0.0.1:8000/ask" -H "Content-Type: application/json" -d '{"question": "write here your question"}'
```

#### Using docker
- Ensure the `./start.sh` is executable:
```bash
chmod +x start.sh
```
- Run the application using Docker:
```bash
./start.sh
```
- Ensure you have the necessary permissions. On Linux, you may need:
```bash
sudo ./start.sh
```
- Test the endpoint:
```bash
curl -X POST "http://127.0.0.1:8000/ask" -H "Content-Type: application/json" -d '{"question": "write here your question"}'
```

### Demo of the application
- Example of testing the endpoint:
```bash
curl -X POST "http://127.0.0.1:8000/ask" -H "Content-Type: application/json" -d '{"question": "If Im accused of a crime what are my rights?"}'
```
- The LLM's response and the relevant snippets used:
```Json
{"answer":"If you're accused of a crime, your rights under the European Union's Fundamental Rights include:\n\n1. **Presumption of innocence**: You are presumed innocent until proven guilty according to law (Article 48).\n2. **Right to defense**: Your rights of defense are guaranteed, and you have the right to be advised, defended, and represented (Article 48 and Article 47).\n3. **Right to a fair trial**: You are entitled to a fair and public hearing within a reasonable time by an independent and impartial tribunal (Article 47).\n4. **Right to an effective remedy**: You have the right to an effective remedy before a tribunal if your rights and freedoms are violated (Article 47).\n5. **Protection against double jeopardy**: You cannot be tried or punished twice for the same offense (Article 50).\n6. **Access to legal aid**: If you lack sufficient resources, legal aid shall be made available to ensure effective access to justice (Article 47).",
"relevant_snippets":[
"Article 48: Presumption of innocence and right of defence. Everyone who has been charged shall be presumed innocent until proved guilty according to law. Respect for the rights of the defence of anyone who has been charged shall be guaranteed.",
"Article 50: Right not to be tried or punished twice in criminal proceedings for the same criminal offence. No one shall be liable to be tried or punished again in criminal proceedings for an offence for which he or she has already been finally acquitted or convicted within the Union in accordance with the law. ",
"Article 47: Right to an effective remedy and to a fair trial. Everyone whose rights and freedoms guaranteed by the law of the Union are violated has the right to an effective remedy before a tribunal in compliance with the conditions laid down in this Article. Everyone is entitled to a fair and public hearing within a reasonable time by an independent and impartial tribunal previously established by law. Everyone shall have the possibility of being advised, defended and represented. Legal aid shall be made available to those who lack sufficient resources in so far as such aid is necessary to ensure effective access to justice."
```

## Cloud Deployment
To deploy this container on a cloud provider, I think I would start by uploading the Docker image to a container registry, like Amazon Elastic Container Registry, Azure Container Registry, or Google Container Registry. After that, I’d use one of their services to actually run the container, like AWS Fargate, Azure Container Instances, or Google Cloud Run. These seem like easier options because they handle a lot of the setup for you. If I needed more control I might look into something like Kubernetes.

# Contact
If you have any question about my documentation or code [contact me](mailto:diogofranciscop@hotmail.com)
