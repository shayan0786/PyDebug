from flask import Flask, request, jsonify, render_template, redirect, url_for
import sys
from io import StringIO
import random
import os
import traceback
from dotenv import load_dotenv
import google.generativeai as genai
from flask_cors import CORS  # For cross-origin requests if needed

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS if needed

# Configure Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("No GEMINI_API_KEY found in .env file")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# Main Pages
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/debugger', methods=['GET', 'POST'])
def debugger_page():
    output = None
    ai_response = None
    
    if request.method == 'POST':
        code = request.form.get('code', '')
        action = request.form.get('action', '')
        message = request.form.get('message', '')
        
        if action == 'run':
            output = execute_code(code)
        elif action == 'debug':
            output = execute_code(code)
            if output and any(error['type'] == 'error' for error in output['errors']):
                error_messages = '\n'.join(
                    error['message'] for error in output['errors'] 
                    if error['type'] == 'error'
                )
                ai_response = get_gemini_response(code, error_messages, debug=True)
            else:
                ai_response = get_gemini_response(code, debug=True)
        elif message:
            ai_response = get_gemini_response(code, message)
    
    return render_template('debugger.html', output=output, ai_response=ai_response)

# API Endpoints
@app.route('/debug', methods=['POST'])
def debug_code():
    data = request.get_json()
    code = data.get('code', '')
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    result = execute_code(code)
    return jsonify(result)

@app.route('/ai-debug', methods=['POST'])
def ai_debug():
    data = request.get_json()
    code = data.get('code', '')
    error = data.get('error', '')
    message = data.get('message', '')
    
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    
    try:
        response = get_gemini_response(code, error or message, debug=bool(error))
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Core Functions
def execute_code(code):
    output = StringIO()
    error = StringIO()
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = output
    sys.stderr = error
    
    errors = []
    result_output = ""
    
    try:
        try:
            compiled_code = compile(code, '<string>', 'exec')
        except SyntaxError as e:
            error_msg = f"Line {e.lineno}: {type(e).__name__}: {e.msg}\n"
            if e.text:
                error_msg += f"  {e.text.strip()}\n"
                error_msg += " " * (e.offset-1) + "^\n"
            errors.append({'type': 'error', 'message': error_msg})
            return {'errors': errors, 'output': ''}
        
        try:
            exec(compiled_code, {'__builtins__': __builtins__})
            result_output = output.getvalue()
            if not error.getvalue():
                errors.append({'type': 'success', 'message': 'Code executed successfully!'})
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb = traceback.extract_tb(exc_traceback)[-1]
            errors.append({
                'type': 'error',
                'message': f"Line {tb.lineno}: {type(e).__name__}: {str(e)}"
            })
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
    
    return {
        'errors': errors,
        'output': result_output
    }

def get_gemini_response(code, user_input=None, debug=False):
    try:
        if debug:
            prompt = f"""Debug this Python code:
            {code}
            Error: {user_input}
            Provide:
            1. Error explanation
            2. Fixed code
            3. Explanation of fix
            4. Prevention tips"""
        else:
            prompt = f"""Help with Python code:
            {code}
            Question: {user_input}
            Provide detailed explanation with examples."""
        
        response = model.generate_content(prompt, request_options={'timeout': 10})
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"

# Chat Endpoint
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower()
    user_message_normalized = user_message.replace(" ", "")
    response = ""

    # Learning Python phrases
    learning_phrases = [
        "learnpython", "teachpython", "iwanttolearnpython", 
        "canyouteachpython", "startpythontutorial", "pythonseekhna hai",
        "learn", "python", "tutorial"
    ]
    
    if any(phrase in user_message_normalized for phrase in learning_phrases):
        responses = [
            "Whispers of code, echoes of logic.",
            "Learning is the new magic.",
            "I decode dreams, one line at a time.",
            "Syntax is poetry in disguise.",
            "Between bugs and brilliance, I exist.",
            "You ask, I awaken the code.",
            "Every error has a hidden lesson.",
            "Code mein chhupi hai meri kahani.",
            "Sawal tera, jawaab mera safar.",
            "Main likhta nahi, mehsoos karta hoon code."
        ]
        response = random.choice(responses)
        return jsonify({'response': response, 'redirect': url_for('learn_python')})

    # Greetings
    greetings = ["hi", "hello", "namaste", "hlo", "bro", "bhai"]
    if any(greet in user_message for greet in greetings):
        responses = [
            "Yo! I'm glad you dropped by! 😄",
            "Namaste, coding warrior! 🧘‍♂ Welcome to the world of bug-slaying.",
            "Hey hey, kya haal chaal! Ready to debug destiny?",
            "Wassup bro! Let's crush some code bugs today 💻🔥",
            "Hlo legend! Type away, I'm listening... 👂✨"
        ]
        response = random.choice(responses)

    # Gratitude
    elif any(word in user_message for word in ["thank you", "thanks", "ok", "okay"]):
        responses = [
            "My pleasure! I'm always here to debug the bugs of life. 🧠💻",
            "You're welcome, code champ! 💪 Anytime, any bug!",
            "Glad to help, bro. Let's keep the bytes flowing. ⚡",
            "Acha laga madad karke — call me whenever code ka chakkar ho!",
            "No biggie! I was coded to care 🫶"
        ]
        response = random.choice(responses)

    # Developer details
    elif any(word in user_message for word in ["who made you", "developer name", "who is your creator"]):
        responses = [
            "I'm handcrafted with care by:\n🌟 Shayan Akhtar (12317465)\n🌟 Himanshu (12300858)\n🌟 Anjali Chowdhury (12314082)\nTogether, they wrote me line by line, heartbeat by heartbeat 💻❤",
            "Built with bugs, love, and sleepless nights by Shayan, Himanshu & Anjali. Respect the coders. 🔥",
            "I'm the result of caffeine, code, and chaos — signed by Shayan, Himanshu & Anjali ☕🧑‍💻"
        ]
        response = random.choice(responses)

    # Job role
    elif any(word in user_message for word in ["what do you do", "your job", "your purpose"]):
        responses = [
            "I'm a Python Code Debugger — turning your chaos into clean, dreamy code ✨🐍",
            "I find bugs, crush them, and leave your code sparkling. That's my job 😎",
            "Code me your mess, and I'll send you back magic. I'm the bug whisperer 🧙‍♂",
            "Job? I decode disasters and bring structure to spaghetti code 🍝➡🚀"
        ]
        response = random.choice(responses)

    # Debugging
    elif "debug" in user_message_normalized:
        responses = [
            "Ah, the sacred word: debug.\nLet the healing begin... 🧘‍♂",
            "You summoned me, the Knight of Code 🛡\nTime to slay the bugs that haunt your script.",
            "Deep breaths, my friend.\nDebugging isn't rage — it's rhythm. 🧠🎵",
            "Elementary, my dear coder. 🕵‍♂\nThe game is afoot, and the bug is hiding.\nLet's track it down, line by line.",
            "Yo! Droppin' the hottest debugging beat 🔥\nYour code's been wildin', so let's tame it:\nYou said debug? I heard let's fix life 😎",
            "Debugging is not chaos, it's control.\nBreathe in bugs. Breathe out solutions 🌬"
        ]
        response = random.choice(responses)
        return jsonify({'response': response, 'redirect': url_for('debugger_page')})

    # Unknown inputs
    else:
        responses = [
            "Umm... I didn't get that. But I'm always learning! 🧠 Try saying it differently.",
            "That's a bit above my pay grade... yet 😅 Wanna talk code instead?",
            "I'm confused, but not defeated. Wanna try again?",
            "Code me curious! Mind rephrasing that, genius?"
        ]
        response = random.choice(responses)

    return jsonify({'response': response})

@app.route('/learnpy', methods=['GET'])
def learn_python():
    return render_template('learnpy.html')

# Text-to-Speech Endpoint
@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        # Use a library like gTTS (Google Text-to-Speech) to generate speech
        from gtts import gTTS
        from io import BytesIO
        import base64

        tts = gTTS(text, lang='en')
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        # Encode audio to base64 to send as a response
        audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')
        return jsonify({'audio': audio_base64})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)