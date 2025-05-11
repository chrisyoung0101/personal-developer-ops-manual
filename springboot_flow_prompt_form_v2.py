
print("""
────────────────────────────────────────────────────────────────────────────
🧠 Spring Boot Flow Documentation Helper
────────────────────────────────────────────────────────────────────────────

This interactive script helps you document the full lifecycle of a Spring Boot
service endpoint — from controller to service logic, external integrations,
error handling, and unit tests.

Use it as a personal second brain to stay organized and answer questions
confidently during meetings or code reviews.

🟢 Instructions:
- Answer each question to the best of your knowledge.
- You can enter multiple bullet points. Press ENTER after each line.
- Type 'done' on a new line when you're finished with a question.
- Navigation:
  <     → Go to the previous question
  >     → Skip the current question
  d     → Finish early

Let's get started!
────────────────────────────────────────────────────────────────────────────
""")

# Prompt for custom file name
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

# Flatten list of questions with references to their section
flat_questions = []
for section, qs in form_structure.items():
    for q in qs:
        flat_questions.append((section, q))

# Initialize answer storage
answers = [[] for _ in flat_questions]
index = 0

# Loop through questions
while index < len(flat_questions):
    section, question = flat_questions[index]
    print(f"\nSection: {section}")
    print(f"Q{index + 1}/{len(flat_questions)}: {question}")
    if answers[index]:
        print("Current Answers:")
        for line in answers[index]:
            print(f"  - {line}")
    print("Enter each line of your answer. Type 'done' to finish. '<', '>', or 'd' for navigation.")
    
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
            index = len(flat_questions)
            break
        elif line.lower() == "done":
            answers[index] = input_lines
            index += 1
            break
        else:
            input_lines.append(line)

# Build output text
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

# Save to text file
with open(filename, "w", encoding="utf-8") as f:
    f.write(output)

# Print final result
print("\nCompleted Documentation:")
print(output)
print(f"\nSaved to: {filename}")
