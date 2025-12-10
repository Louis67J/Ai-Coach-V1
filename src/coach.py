from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_coaching(profile):
    prompt = f"""
Tu es un coach cycliste expert.
Voici le profil analysé des 24 derniers mois :

{profile}

Écris un rapport d'entraînement clair, structuré, motivant, avec :
- analyse
- forces
- faiblesses
- recommandations pour la semaine prochaine
"""

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt
    )

    return response.output_text
