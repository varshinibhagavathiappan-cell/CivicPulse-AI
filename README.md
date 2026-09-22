# CivicPulse AI — NVIDIA Best Apps & Agents

## Competition track
Best Apps & Agents

## Concept
CivicPulse is an AI incident-triage and coordination agent. It turns an unstructured civic-service report into:
- incident classification
- priority
- public-safety impact
- responsible department
- immediate actions
- resource needs
- verification requirements
- concise decision rationale
- a 3-step coordination workflow

The NVIDIA model is part of the core decision engine, not a decorative chatbot.

## NVIDIA integration
Model: `nvidia/nemotron-3.5-lightning-30b-a3b`
Endpoint: `https://integrate.api.nvidia.com/v1`

The backend calls the NVIDIA hosted endpoint and asks Nemotron to return a strict JSON decision object. The frontend renders that object into the dashboard.

## Run

1. Copy `.env.example` to `.env` in the project root and put your private NVIDIA API key in it.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Terminal 1:
   `python backend/app.py`
4. Terminal 2:
   `cd frontend`
   `python -m http.server 5500`
5. Open:
   `http://127.0.0.1:5500`

## Test
Use the "Try live demo scenario" button or enter your own incident.

Example:
"A resident reports a broken streetlight beside a school. The road becomes very dark after 7 PM and students walk through the area. No accident has been reported."

## Important
The app does not claim to access live municipal systems, maps, police databases, sensors, or government records. It analyzes information supplied by the user. Human verification is required for real-world decisions.

Never commit or share `.env`.
