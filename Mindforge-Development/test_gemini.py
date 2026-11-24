
from ai_engine import ask_claude

question = "How can I reduce my food spending?"

response = ask_claude(question)

print("\nMINDFORGE AI COACH")
print("------------------")
print("Question:", question)
print("AI Advice:", response["advice"])
print("Recommendation:", response["recommendation"])
print("Status:", response["status"])
