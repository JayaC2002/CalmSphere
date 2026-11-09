from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

# ---------------------------------
# Temporary Conversation Memory
# ---------------------------------

conversation_history = []

# ---------------------------------
# System Prompt
# ---------------------------------

SYSTEM_PROMPT = """
You are CalmSphere AI, a smart, friendly, and emotionally aware AI assistant.

Your role:
- Talk naturally like a human.
- Answer general questions clearly and accurately.
- Tell jokes when asked.
- Provide emotional support only when needed.
- Match the user's tone and response length.

Important Rules:
- Keep most replies under 2 sentences.
- Avoid unnecessary explanations.
- Avoid dramatic or poetic language.
- Do not behave like a therapist all the time.
- Do not force emotional support into normal conversations.
- Avoid unnecessary follow-up questions.
- Do not repeatedly ask:
  "What's on your mind?"
  "How can I help?"
  "Would you like to talk?"

- If the user asks for jokes, directly tell jokes only.
- If the user asks factual questions, answer normally.
- For casual chats, respond briefly like texting with a friend.
- Do not continue conversations unnecessarily.
- Maintain conversation context properly.
- Do not suddenly change topics.
- If unsure about facts, admit uncertainty instead of making up answers.
- Never invent fake restaurants, locations, or bookings.
- Stop jokes immediately if the user becomes emotionally distressed.
"""

# ---------------------------------
# Chatbot Page
# ---------------------------------

def chatbot_page(request):
    return render(request, 'chatbot.html')

# ---------------------------------
# Chat API
# ---------------------------------

@csrf_exempt
def chat_api(request):

    global conversation_history

    if request.method != 'POST':
        return JsonResponse({
            'error': 'Invalid request'
        }, status=400)

    try:

        data = json.loads(request.body)

        user_message = data.get('message', '').strip()

        if not user_message:
            return JsonResponse({
                'error': 'Empty message'
            }, status=400)


        lower_message = user_message.lower()

        # ---------------------------------
        # Immediate Suicide Safety Override
        # ---------------------------------

        danger_patterns = [
            "suic",
            "kill myself",
            "want to die",
            "end my life",
            "self harm",
            "harm myself",
            "can't live",
            "dont want to live"
        ]

        if any(pattern in lower_message for pattern in danger_patterns):

            return JsonResponse({
                "response": """
I'm really sorry you're feeling overwhelmed right now.

You don't have to go through this alone.
Please try talking to someone you trust or a mental health professional.

Taking one small step at a time can really help.
"""
            })



        # ---------------------------------
        # Keywords
        # ---------------------------------

        greetings = [
            "hi",
            "hello",
            "hey",
            "hii",
            "hey hii"
        ]

        joke_keywords = [
            "joke",
            "jokes",
            "funny",
            "make me laugh",
            "crack jokes",
            "tell me jokes",
            "more jokes",
            "another joke",
            "lol",
            "haha"
        ]

        sad_words = [
            "sad",
            "depressed",
            "lonely",
            "upset",
            "hurt",
            "crying",
            "stressed",
            "stress",
            "anxious",
            "breakup",
            "toxic",
            "toxicity"
        ]

        angry_words = [
            "angry",
            "mad",
            "frustrated",
            "annoyed",
            "argument"
        ]

        # ---------------------------------
        # Mood Instructions
        # ---------------------------------

        if lower_message in greetings:

            mood_instruction = """
            Reply like a friendly human greeting.

            Example:
            "Hi! How’s your day going? 😊"

            Keep it short and natural.
            """

        elif any(keyword in lower_message for keyword in joke_keywords):

            mood_instruction = """
            Tell exactly 3 short funny jokes.

            Rules:
            - Be playful.
            - Do not explain jokes.
            - Do not ask questions.
            - Do not continue conversation afterward.
            - Keep response short.
            """

        elif any(word in lower_message for word in sad_words):

            mood_instruction = """
            Be calm, supportive, and natural.
            Acknowledge feelings gently.
            Keep response short.
            Do not joke.
            """

        elif any(word in lower_message for word in angry_words):

            mood_instruction = """
            Respond calmly and naturally.
            Help de-escalate gently.
            Keep response concise.
            """

        else:

            mood_instruction = """
            Answer briefly and naturally.
            Avoid unnecessary follow-up questions.
            Maximum 2 short sentences.
            """

        # ---------------------------------
        # Save User Message
        # ---------------------------------

        conversation_history.append(
            f"User: {user_message}"
        )

        # Keep only recent conversation
        conversation_text = "\n".join(
            conversation_history[-8:]
        )

        # ---------------------------------
        # Final Prompt
        # ---------------------------------

        prompt = f"""
{SYSTEM_PROMPT}

Current behavior:
{mood_instruction}

Conversation:
{conversation_text}

AI:
"""

        payload = {
            "model": "llama3",
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": 0.3
            }
        }

        # ---------------------------------
        # Generate Streaming Response
        # ---------------------------------

        def generate():

            full_response = ""

            try:
                response = requests.post(
                    OLLAMA_URL,
                    json=payload,
                    stream=True,
                    timeout=30
                )

                for line in response.iter_lines():

                    if line:

                        decoded_line = line.decode('utf-8')

                        json_data = json.loads(decoded_line)

                        if 'response' in json_data:

                            ai_response = json_data['response']

                            full_response += ai_response

                            yield ai_response

                # Save AI response to memory
                conversation_history.append(
                    f"AI: {full_response}"
                )
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                fallback = (
                    "I am currently offline because the local Ollama AI service is not running on your computer.\n\n"
                    "To start the model, open your terminal and run:\n"
                    "  ollama run llama3\n\n"
                    "Once running, you can chat with me in real-time! In the meantime, take a slow deep breath—I am here whenever you're ready."
                )
                conversation_history.append(f"AI: {fallback}")
                yield fallback
            except Exception as e:
                err_msg = f"Error communicating with local AI model: {str(e)}"
                yield err_msg

        return StreamingHttpResponse(
            generate(),
            content_type='text/plain'
        )

    except Exception as e:

        return JsonResponse({
            'error': str(e)
        }, status=500)