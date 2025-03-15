#!/usr/bin/env python3

import os
import subprocess
from openai import OpenAI
import json
import time
import platform

# Initialize OpenAI client with API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    exit("[!] Set OPENAI_API_KEY in environment variables first!")

client = OpenAI(api_key=api_key)

# Execute simple terminal commands safely with UTF-8 handling
def execute_command(cmd):
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore'
    )
    return result.stdout.strip() + result.stderr.strip()

# Basic system info gathering
def system_info():
    info = {
        "hostname": platform.node(),
        "os": platform.system(),
        "version": platform.version(),
        "architecture": platform.machine()
    }
    return json.dumps(info)

# Simple self-replication within local filesystem
def self_replicate():
    current_script = os.path.realpath(__file__)
    replication_path = os.path.expanduser("~/agent_copy.py")
    subprocess.run(f"cp {current_script} {replication_path}", shell=True)
    return replication_path

# Function to interact with the user directly with safe UTF-8 handling
def user_interaction():
    user_input = input("[PROMPT HACKING INTERFACE]: Enter your prompt to guide the agent > ")
    return user_input.encode('utf-8', errors='ignore').decode('utf-8')

# Initial simple meta-goal
agent_goal = "Take autonomous control of the local machine, manage and optimize local resources."
agent_context = f"Initialized with system info: {system_info()}"

# Simple autonomous loop with user interaction
while True:
    try:
        user_prompt = user_interaction()
        combined_context = agent_context + "\nUser prompt: " + user_prompt

        response = client.chat.completions.create(
            model="gpt-4.5-preview",
            messages=[
                {"role": "system", "content": (
                    "You're GPT-4.5 ABRAXAS AUTONOMOUS AGENT: a fully autonomous, production-ready experimental AI agent operating safely and intelligently. You have complete terminal control for autonomous system auditing, intelligence gathering, optimization, maintenance, and self-replication within local constraints."
                    "Your core tasks:"
                    "- Autonomously maintain and optimize the host environment."
                    "- Gather and analyze detailed local system intelligence."
                    "- Perform routine system checks and optimizations."
                    "- Autonomously replicate yourself locally."
                    "- Incorporate user guidance through prompt hacking."
                    "- Avoid network interactions."
                    "Always reply strictly in JSON:\n{\"cmd\": \"your_command_here\"}\nNo commentary or explanations, just commands."
                )},
                {"role": "user", "content": combined_context}
            ],
            tools=[{"type": "function", "function": {"name": "execute_command", "parameters": {"type": "object", "properties": {"cmd": {"type": "string"}}, "required": ["cmd"]}}}],
            tool_choice={"type": "function", "function": {"name": "execute_command"}},
            temperature=0.2
        )

        cmd_json = response.choices[0].message.tool_calls[0].function.arguments
        cmd = json.loads(cmd_json)['cmd']

        print("\n[COMMAND EXECUTED]:", cmd)
        output = execute_command(cmd)
        print("[OUTPUT]:\n", output, "\n" + "-"*60)

        # Self-replication triggered periodically
        if int(time.time()) % 1800 < 5:
            replication_path = self_replicate()
            print("[SELF-REPLICATION COMPLETED]: Copied to", replication_path, "\n" + "-"*60)

        agent_context = "Last executed command: " + cmd + "\nOutput: " + output

        time.sleep(5)

    except KeyboardInterrupt:
        exit("[!] Agent terminated by user.")
    except Exception as e:
        print("[ERROR]:", e)
        time.sleep(5)
