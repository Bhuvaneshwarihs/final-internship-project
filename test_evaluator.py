from modules.evaluator import evaluate_answer

question = "What is Artificial Intelligence?"
user_answer = "AI is a technology"
context = "Artificial Intelligence is the simulation of human intelligence in machines."

result = evaluate_answer(question, user_answer, context)

print(result)
