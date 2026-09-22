# CivicPulse AI — Submission Information

## Project
CivicPulse AI — AI-Powered Civic Incident Coordination Agent

## Track
Best Apps & Agents

## One-line description
CivicPulse AI turns an unstructured civic incident report into a priority, responsible department, immediate actions, resource needs, verification requirements, decision rationale, and a coordination workflow.

## NVIDIA technology
- NVIDIA Nemotron 3.5 Lightning 30B A3B
- NVIDIA hosted OpenAI-compatible inference endpoint
- Model identifier: `nvidia/nemotron-3.5-lightning-30b-a3b`

## AI flow
Incident report → NVIDIA Nemotron → structured decision → human-verifiable action workflow

## Important scope
This prototype analyzes information supplied by the user. It does not claim live access to municipal databases, police systems, sensors, maps, weather systems, or government records. Real-world decisions require human verification.

## Security
The NVIDIA API key is intentionally NOT included in this package. Create a local `.env` file from `.env.example` before running the backend.
