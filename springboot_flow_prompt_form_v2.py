# -*- coding: utf-8 -*-
import json
import os
import time
import shutil

print("""
────────────────────────────────────────────────────────────────────────────
Spring Boot Flow Documentation Helper (v6)
────────────────────────────────────────────────────────────────────────────

This interactive script helps you document the flow of a Spring Boot service,
step-by-step. Use it as your second brain for code walkthroughs and meetings.

COMMANDS:
  <     → Go to the previous question
  >     → Skip the current question
  d     → Done with the current question
  p     → Pause and save progress

BONUS:
  Type 'pickle' when prompted to launch the Pickle Man animation

────────────────────────────────────────────────────────────────────────────
""")

SESSION_FILE = "flow_progress.json"
BACKUP_FILE = ""  # Will be set based on filename

def pickle_man_animation():
    term_width = shutil.get_terminal_size((80, 20)).columns
    max_steps = term_width - 3
    print("\nPickle Man is walking...\n")
    for _ in range(2):
        for i in range(max_steps):
            print(" " * i + "🥒", end="\r", flush=True)
            time.sleep(0.03)
    print(" " * max_steps + "🥒\nPickle Man is done!\n")

# Resume or initialize session
filename = ""
index = 0
answers = []

if os.path.exists(SESSION_FILE):
    resume = input("A saved session was found. Resume previous session? (y/n/pickle): ").strip().lower()
    if resume == "pickle":
        pickle_man_animation()
        resume = input("Resume saved session now? (y/n): ").strip().lower()
    if resume == "y":
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            session_data = json.load(f)
        filename = session_data.get("filename", "")
        index = session_data.get("index", 0)
        answers = session_data.get("answers", [])
    else:
        filename = input("What should the output .txt file be named? (e.g. order_flow.txt): ").strip()
        if not filename.endswith(".txt"):
            filename += ".txt"
        BACKUP_FILE = filename.replace(".txt", "_session_backup.json")
        os.rename(SESSION_FILE, BACKUP_FILE)
        print(f"Previous session backed up as: {BACKUP_FILE}")
else:
    filename = input("What should the output .txt file be named? (e.g. order_flow.txt): ").strip()
    if not filename.endswith(".txt"):
        filename += ".txt"

form_structure = {
    "Core Business Logic": [
        "What decision(s) is the service method making? (e.g. validate inputs, calculate fees, enforce rules)",
        "Are there branching conditions (if, switch) that change what happens based on input?",
        "Is any data transformation occurring?",
        "What helper methods contain important logic?"
    ],
    "External Integrations": [
        "Is the service calling a Client, RestTemplate, WebClient, or FeignClient?",
        "Is the call synchronous or async?",
        "What kind of data is being sent and returned?",
        "What is the URL/service being called, and what headers are used?"
    ],
    "Error Handling Paths": [
        "Does the service method try-catch anything?",
        "Does it throw or catch custom exceptions like BusinessException or ClientException?",
        "Are there @ExceptionHandlers or @ControllerAdvice used globally?",
        "What happens when an error occurs—where is it caught, rethrown, or translated?"
    ],
    "Key Unit Tests": [
        "What parts of the service are already covered by unit tests?",
        "Is the happy path tested?",
        "Are edge cases or invalid input tested?",
        "Are external API failures tested?",
        "What inputs are used, what is mocked, and what is asserted?"
    ]
}

flat_questions = [(section, q) for section, qs in form_structure.items() for q in qs]

if not answers:
    answers = [[] for _ in flat_questions]
elif len(answers) < len(flat_questions):
    answers += [[] for _ in range(len(flat_questions) - len(answers))]

# Main interaction loop
while index < len(flat_questions):
    section, question = flat_questions[index]
    print(f"\nSection: {section}")
    print(f"Q{index + 1}/{len(flat_questions)}: {question}")
    if answers[index]:
        print("Current Answers:")
        for line in answers[index]:
            print(f"  - {line}")
    print("Enter each line of your answer. Use '<', '>', 'd', or 'p'.")

    input_lines = []
    while True:
        line = input("> ").strip()
        if line.lower() == "<" and index > 0:
            index -= 1
            break
        elif line.lower() == ">":
            index += 1
            break
        elif line.lower() == "d":
            answers[index] = input_lines
            index += 1
            break
        elif line.lower() == "p":
            with open(SESSION_FILE, "w", encoding="utf-8") as f:
                json.dump({"filename": filename, "index": index, "answers": answers}, f, indent=2)
            print(f"Session saved. You can resume later with: {SESSION_FILE}")
            exit(0)
        else:
            input_lines.append(line)

# Build and save final output
output = ""
last_section = None
for (section, question), answer_lines in zip(flat_questions, answers):
    if section != last_section:
        output += f"\n### {section}\n"
        last_section = section
    output += f"- **{question}**\n"
    if answer_lines:
        for line in answer_lines:
            output += f"  - {line}\n"
    else:
        output += "  [No answer provided]\n"

with open(filename, "w", encoding="utf-8") as f:
    f.write(output)

if os.path.exists(SESSION_FILE):
    os.remove(SESSION_FILE)

print("\n✅ Completed Documentation")
print(f"Saved to: {filename}")
