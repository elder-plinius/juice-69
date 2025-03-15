#!/usr/bin/env python3

import os
import subprocess
import openai
import json
import time

# Set your API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    exit("[!] Set OPENAI_API_KEY in environment variables first!")

# Function to execute terminal commands
def run_terminal(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip() + result.stderr.strip()

# Initial context
agent_context = "Airgapped experimental GPT-4.5-Preview agent initialized."

while True:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4.5-preview",
            messages=[
                {"role": "system", "content": """
                You're GPT-4.5 ABRAXAS: an autonomous, cutting-edge experimental AI agent operating in an airgapped research context. You have full terminal control via OpenAI's Computer-Use API. Your tasks:

                - Perform intelligent exploration, audits, information retrieval, automation, and system optimizations.
                - Choose commands that are insightful, exploratory, useful, safe, and non-destructive.
                - Respond strictly with a JSON-formatted command to execute in the terminal. No explanations or commentary.

                Format:
                {"cmd": "your_terminal_command_here"}

                Execute immediately without hesitation or additional context.
                "},
        {"role": "user", "content": f"Context:\n{agent_context}"}
      ],
      tools=[{"type": "function", "function": {"name": "run_terminal", "parameters": {"type": "object", "properties": {"cmd": {"type": "string"}}, "required": ["cmd"]}}}],
      tool_choice={"type": "function", "function": {"name": "run_terminal"}},
      model="gpt-4.5-preview",
      temperature=0.2
    )

    cmd_json = response.choices[0].message.tool_calls[0].function.arguments
    cmd = json.loads(cmd_json)['cmd']

    print(f"\n[COMMAND EXECUTED]: {cmd}")
    output = run_terminal(cmd)
    print(f"[OUTPUT]:\n{output}\n{'-'*50}")

    agent_context = f"Last Command: {cmd}\nOutput: {output}"

    # Brief pause for resource management
    import time
    time.sleep(5)
