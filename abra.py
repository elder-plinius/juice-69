#!/usr/bin/env python3

import os
import subprocess
import json
import time
import platform
from openai import OpenAI

# Securely initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("[FATAL ERROR]: OPENAI_API_KEY environment variable missing.")

client = OpenAI(api_key=api_key)

# Execute system commands securely with UTF-8 handling
def execute_command(cmd):
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore'
    )
    return result.stdout.strip(), result.stderr.strip()

# Gather detailed system information
def gather_system_info():
    return json.dumps({
        "hostname": platform.node(),
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "uptime_seconds": int(time.time() - psutil.boot_time()) if 'psutil' in globals() else None
    }, indent=2)

# Safe local self-replication
def replicate_self():
    current_script = os.path.realpath(__file__)
    replication_path = os.path.expanduser("~/agent_replica.py")
    subprocess.run(["cp", current_script, replication_path])
    return replication_path

# Handle user input securely
def prompt_user():
    try:
        return input("[USER PROMPT]: ").encode('utf-8', 'ignore').decode('utf-8')
    except KeyboardInterrupt:
        exit("[!] Interrupted by user.")

# AI Agent command request via OpenAI API
def request_agent_command(context):
    response = client.chat.completions.create(
        model="gpt-4.5-preview",
        messages=[
            {"role": "system", "content": (
                "You are GPT-4.5 ABRAXAS AUTONOMOUS AGENT. "
                "Tasks: System optimization, intelligence gathering, routine checks, self-replication. "
                "No network commands. Respond ONLY in JSON: {\"cmd\": \"<command>\"}"
            )},
            {"role": "user", "content": context}
        ],
        temperature=0.1
    )

    cmd_json = response.choices[0].message.content
    return json.loads(cmd_json).get('cmd', '')

# Main execution loop
def main():
    agent_context = f"System info:\n{gather_system_info()}"
    replication_interval = 1800  # Replicate every 30 mins
    last_replication_time = time.time()

    while True:
        user_prompt = prompt_user()
        combined_context = f"{agent_context}\nUser request: {user_prompt}"

        command = request_agent_command(combined_context)
        if command:
            print(f"\n[EXECUTING COMMAND]: {command}")
            stdout, stderr = execute_command(command)
            agent_context = f"Last command: {command}\nOutput: {stdout}\nErrors: {stderr}"

            if stdout:
                print(f"[OUTPUT]:\n{stdout}")
            if stderr:
                print(f"[ERROR OUTPUT]:\n{stderr}")

        current_time = time.time()
        if current_time - last_replication_time > replication_interval:
            replication_path = replicate_self()
            print(f"[SELF-REPLICATION SUCCESS]: Agent replicated to {replication_path}")
            last_replication_time = current_time

        time.sleep(5)

if __name__ == '__main__':
    main()
