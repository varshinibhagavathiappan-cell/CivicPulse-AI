from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("NVIDIA_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "NVIDIA_API_KEY is missing. "
        "Create a .env file in the project root."
    )

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=API_KEY
)

MODEL = "nvidia/nemotron-3.5-lightning-30b-a3b"

SYSTEM_PROMPT = """
You are CivicPulse AI, a civic incident decision-support agent.

Analyze the incident report and convert it into a practical response.

Return ONLY valid JSON.

Use exactly this structure:

{
  "incident_type": "short incident type",
  "priority": "LOW, MEDIUM, HIGH, or CRITICAL",
  "public_safety": true,
  "summary": "short explanation",
  "department": "responsible department",
  "immediate_actions": [
    "action 1",
    "action 2",
    "action 3"
  ],
  "resources": [
    "resource 1",
    "resource 2"
  ],
  "verification_needed": [
    "information that should be verified"
  ],
  "decision_rationale": "short explanation of why this priority and actions were selected",
  "workflow": [
    {
      "step": 1,
      "action": "first action",
      "owner": "responsible team"
    },
    {
      "step": 2,
      "action": "second action",
      "owner": "responsible team"
    },
    {
      "step": 3,
      "action": "third action",
      "owner": "responsible team"
    }
  ]
}

Rules:

- Keep the response concise.
- Do not write explanations outside the JSON.
- Do not invent live data.
- Do not claim to have checked maps, government systems, sensors, weather systems, police systems, or databases.
- If information is missing, put it under verification_needed.
- This is decision support and human verification is required.
"""


def extract_json(text):
    text = (text or "").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    raise ValueError("NVIDIA returned an unexpected response format.")


def clean_result(result):
    required_fields = [
        "incident_type",
        "priority",
        "public_safety",
        "summary",
        "department",
        "immediate_actions",
        "resources",
        "verification_needed",
        "decision_rationale",
        "workflow"
    ]
    for field in required_fields:
        if field not in result:
            if field in [
                "immediate_actions",
                "resources",
                "verification_needed",
                "workflow"
            ]:
                result[field] = []
            elif field == "public_safety":
                result[field] = False
            else:
                result[field] = "Unknown"

    priority = str(result.get("priority", "MEDIUM")).upper().strip()
    if priority not in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]:
        priority = "MEDIUM"
    result["priority"] = priority
    result["public_safety"] = bool(result.get("public_safety"))
    return result


def run_nemotron(report, demo=False):
    prompt = SYSTEM_PROMPT + "\n\nINCIDENT REPORT:\n" + report
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=700,
        extra_body={
            "chat_template_kwargs": {
                "enable_thinking": False
            }
        }
    )

    raw_response = response.choices[0].message.content or ""
    print("\n==============================")
    print("NVIDIA NEMOTRON RESPONSE")
    print("==============================")
    print(raw_response)
    print("==============================\n")

    result = clean_result(extract_json(raw_response))
    return jsonify({
        "result": result,
        "model": MODEL,
        "status": "success",
        "demo": demo
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "model": MODEL
    })


@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    report = (data.get("report") or "").strip()

    if len(report) < 12:
        return jsonify({
            "error": "Please enter a more detailed incident report."
        }), 400

    try:
        return run_nemotron(report)
    except Exception as error:
        print("\nNVIDIA ERROR:")
        print(error)
        print()
        return jsonify({
            "error": "NVIDIA AI analysis failed.",
            "details": str(error)
        }), 502


@app.route("/api/demo", methods=["POST"])
def demo():
    demo_report = """
A large pothole has formed on the main road near a school.

The pothole is filled with rainwater, making it difficult for drivers to see its depth.

Several two-wheelers have nearly lost control while passing through the area.

The road is heavily used during school opening and closing hours.

No injuries have been reported so far.

The situation may become dangerous if it is not addressed quickly.
"""
    try:
        return run_nemotron(demo_report, demo=True)
    except Exception as error:
        print("\nDEMO ERROR:")
        print(error)
        return jsonify({
            "error": "NVIDIA AI demo failed.",
            "details": str(error)
        }), 502


if __name__ == "__main__":
    print("")
    print("==========================================")
    print("       CIVICPULSE AI SERVER")
    print("==========================================")
    print("NVIDIA Model:")
    print(MODEL)
    print("")
    print("Backend:")
    print("http://127.0.0.1:5000")
    print("")
    print("NVIDIA AI is ready.")
    print("==========================================")
    print("")
    app.run(host="127.0.0.1", port=5000, debug=True)
