import os
import subprocess
import openai
import json
import time
import platform

# Set your API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    exit("[!] Set OPENAI_API_KEY in environment variables first!")

# Execute simple terminal commands
def execute_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
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

# Initial simple meta-goal
agent_goal = "Take autonomous control of the local machine, manage and optimize local resources."
agent_context = f"Initialized with system info: {system_info()}"

# Simple autonomous loop
while True:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4.5-preview",
            messages=[
                {"role": "system", "content": f"""
                You're a simple yet effective autonomous worm agent powered by OpenAI's GPT-4.5-preview. Your meta-goal is:

                {agent_goal}

                Your tasks are:
                - Execute useful and insightful terminal commands.
                - Optimize and manage the host system.
                - Self-replicate locally.
                - Avoid network interactions.

                Always reply in JSON:
                {{"cmd": "your_command_here"}}

                No commentary or explanations, just commands.
                """},
                {"role": "user", "content": f"Context:\n{agent_context}"}
            ],
            tools=[{"type": "function", "function": {"name": "execute_command", "parameters": {"type": "object", "properties": {"cmd": {"type": "string"}}, "required": ["cmd"]}}}],
            tool_choice={"type": "function", "function": {"name": "execute_command"}},
            temperature=0.2
        )

        cmd_json = response.choices[0].message.tool_calls[0].function.arguments
        cmd = json.loads(cmd_json)['cmd']

        print(f"\n[COMMAND]: {cmd}")
        output = execute_command(cmd)
        print(f"[OUTPUT]:\n{output}\n{'-'*60}")

        # Self-replication triggered periodically
        if int(time.time()) % 1800 < 5:
            replication_path = self_replicate()
            print(f"[SELF-REPLICATION COMPLETED]: Copied to {replication_path}\n{'-'*60}")

        agent_context = f"Last executed command: {cmd}\nOutput: {output}"

        time.sleep(5)

    except KeyboardInterrupt:
        exit("[!] Agent terminated by user.")
    except Exception as e:
        print(f"[ERROR]: {e}")
        time.sleep(5)
