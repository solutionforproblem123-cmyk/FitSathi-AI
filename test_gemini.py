from services.gemini_service import generate_ai_recommendation

response = generate_ai_recommendation(
    "Reply with exactly this sentence: Gemini connection successful."
)

print(response)