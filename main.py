import openai
import speech_recognition as sr
import pyttsx3

# Configurez votre clé d'API OpenAI
openai.api_key = 'YOUR_API_KEY'

# Configurez le modèle à utiliser
model = 'gpt-3.5-turbo'

# Créez un objet Recognizer pour la reconnaissance vocale
recognizer = sr.Recognizer()

# Créez un objet TTS (Text-to-Speech) pour la synthèse vocale
engine = pyttsx3.init()

def transcribe_speech():
    # Utilisez le microphone comme source audio
    with sr.Microphone() as source:
        print("Dites quelque chose...")
        audio = recognizer.listen(source)

    try:
        # Transcrire la parole en texte en utilisant la reconnaissance vocale
        text = recognizer.recognize_google(audio, language="fr-FR")
        return text
    except sr.UnknownValueError:
        print("Impossible de comprendre la parole.")
    except sr.RequestError as e:
        print("Erreur lors de la requête : {0}".format(e))
    return ""

def generate_response(user_input):
    # Appel à l'API GPT pour générer une réponse
    response = openai.Completion.create(
        engine=model,
        prompt=user_input,
        max_tokens=50
    )

    # Obtenez la réponse générée
    generated_text = response.choices[0].text.strip()
    return generated_text

def speak_text(text):
    # Synthétiser la réponse en parole en utilisant la synthèse vocale
    engine.say(text)
    engine.runAndWait()

# Boucle de conversation avec le chatbot
speak_text("Chatbot: Bonjour ! Comment puis-je vous aider ?")

while True:
    # Obtenir l'entrée vocale de l'utilisateur
    user_input = transcribe_speech()

    # Générer une réponse en utilisant l'entrée de l'utilisateur
    response = generate_response(user_input)

    # Afficher et lire la réponse générée
    print("Chatbot:", response)
    speak_text("Chatbot: " + response)

    # Condition de sortie
    if user_input.lower() == 'au revoir':
        break
