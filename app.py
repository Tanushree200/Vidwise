from flask import Flask, request, send_file, render_template, jsonify
import os
from transcript import get_transcript
from summarize import summarize_transcript
from generate_ppt import create_ppt_from_summary
from rag_embed import create_vectorstore_from_transcript
from rag_qa import answer_question

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize_video():
    data = request.json
    video_url = data.get("url")

    transcript = get_transcript(video_url)
    if transcript.startswith("Error") or transcript == "Invalid YouTube URL":
        return jsonify({"error": transcript})

    summary_json = summarize_transcript(transcript)

    
    import json
    try:
        slides = json.loads(summary_json)
    except Exception as e:
        slides = [{
            "title": "⚠️ Error Parsing Summary",
            "bullets": [str(e), "Raw Output:", summary_json]
        }]

    return jsonify({
        "transcript": transcript,
        "slides": slides
    })


@app.route("/generate_ppt", methods=["POST"])
def generate_ppt():
    data = request.get_json()
    transcript = data.get("transcript", "")

    if not transcript.strip():
        return jsonify({"error": "Transcript is empty"}), 400

    
    from datetime import datetime
    filename = f"presentation_{datetime.now().strftime('%Y%m%d%H%M%S')}.pptx"
    filepath = os.path.join("static", "generated", filename)
    os.makedirs("static/generated", exist_ok=True)

    
    create_ppt_from_summary(transcript, save_path=filepath)

    
    return jsonify({ "ppt_url": f"/static/generated/{filename}" })

@app.route("/chat", methods=["POST"])
def chat_with_video():
    try:
        data = request.get_json(force=True)  
        print("Received data:", data)
    except Exception as e:
        print("Error parsing JSON:", e)
        return jsonify({"error": "Invalid JSON"}), 400

    question = data.get("question", "").strip()
    transcript = data.get("transcript", "").strip()

    if not question or not transcript:
        print("Missing data:", {"question": question, "transcript": transcript})
        return jsonify({"error": "Missing question or transcript"}), 400

    
    create_vectorstore_from_transcript(transcript)

    
    answer = answer_question(question)

    return jsonify({"answer": answer})




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
