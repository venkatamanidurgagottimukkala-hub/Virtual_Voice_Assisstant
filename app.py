from flask import Flask, request, render_template_string
import ollama
import markdown

app = Flask(__name__)


HTML = """
<!DOCTYPE html>
<html>

<head>

    <title>AI Voice Virtual Assistant</title>

    <style>

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f4f6f8;
        }

        .container {
            width: 750px;
            margin: 50px auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }

        h1 {
            text-align: center;
            margin-bottom: 30px;
        }

        .input-area {
            display: flex;
            gap: 10px;
        }

        input {
            flex: 1;
            padding: 14px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 8px;
        }

        button {
            padding: 14px 20px;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            background: #2563eb;
            color: white;
        }

        button:hover {
            opacity: 0.9;
        }

        .mic-button {
            background: #dc2626;
        }

        .response {
            margin-top: 30px;
            padding: 25px;
            background: #f8fafc;
            border-radius: 12px;
            line-height: 1.6;
        }

        .response h2 {
            margin-top: 0;
        }

        .response h3 {
            margin-top: 20px;
        }

        .response ul,
        .response ol {
            padding-left: 25px;
        }

        .response li {
            margin-bottom: 8px;
        }

        .response code {
            background: #e5e7eb;
            padding: 3px 6px;
            border-radius: 4px;
        }

        .response pre {
            background: #1e293b;
            color: white;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
        }

    </style>

</head>


<body>

<div class="container">

    <h1>🤖 AI Voice Virtual Assistant</h1>


    <form method="POST">

        <div class="input-area">

            <input
                type="text"
                id="question"
                name="question"
                placeholder="Ask me anything..."
                required
            >

            <button
                type="button"
                class="mic-button"
                onclick="startListening()">
                🎤
            </button>

            <button type="submit">
                Ask AI
            </button>

        </div>

    </form>


    {% if answer %}

    <div class="response">

        <h2>🤖 AI Response</h2>

        {{ answer | safe }}

    </div>

    {% endif %}

</div>


<script>

function startListening() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {

        alert(
            "Speech recognition is not supported in this browser."
        );

        return;
    }


    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";

    recognition.start();


    recognition.onstart = function() {

        console.log("Listening...");

    };


    recognition.onresult = function(event) {

        const text =
            event.results[0][0].transcript;

        document.getElementById("question").value = text;

    };


    recognition.onerror = function(event) {

        alert(
            "Microphone error: " + event.error
        );

    };

}

</script>

</body>

</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    answer = ""

    if request.method == "POST":

        question = request.form["question"]


        prompt = f"""
Answer the following question clearly and concisely.

Use this structure when appropriate:

## Main Answer

Give a simple direct explanation.

## Key Points

- Point 1
- Point 2
- Point 3

## Example

Give an example if useful.

Do not give unnecessary long explanations.

Question:
{question}
"""


        response = ollama.chat(

            model="llama3.2",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            options={
                "temperature": 0.3,
                "num_predict": 150
            }
        )


        raw_answer = response["message"]["content"]

        answer = markdown.markdown(
            raw_answer,
            extensions=["fenced_code"]
        )


    return render_template_string(
        HTML,
        answer=answer
    )


if __name__ == "__main__":

    app.run(debug=True)