import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from voice_softener_engine import soften_text_to_text
from gemini_tts_pro import generate_gemini_tts_pro

app = Flask(__name__, static_url_path='')

# 시나리오별 추천 감정 설정
SCENARIO_EMOTIONS = {
    "A": "professional and calm",
    "B": "kind and helpful",
    "C": "stable and polite",
    "D": "gentle and soothing"
}

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/api/soften', methods=['POST'])
def soften_text():
    data = request.json
    input_text = data.get('text', '')
    scenario = data.get('scenario', 'C')
    voice = data.get('voice', 'Aoede')

    if not input_text:
        return jsonify({"error": "텍스트를 입력해주세요."}), 400

    try:
        # 1. 텍스트 정제
        refined_text = soften_text_to_text(input_text, scenario)
        
        # 2. 음성 파일 생성
        audio_filename = f"{uuid.uuid4()}.mp3"
        audio_path = os.path.join('static', 'audio', audio_filename)
        
        target_emotion = SCENARIO_EMOTIONS.get(scenario, "neutral")
        
        generate_gemini_tts_pro(
            text=refined_text,
            output_filename=audio_path,
            voice_name=voice,
            emotion=target_emotion,
            speed=1.0
        )
        
        return jsonify({
            "original_text": input_text,
            "refined_text": refined_text,
            "audio_url": f"/static/audio/{audio_filename}",
            "scenario": scenario
        })

    except Exception as e:
        print(f"Error in /api/soften: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # 포트 8080으로 실행 (Cloud Shell 기본 포트)
    app.run(host='0.0.0.0', port=8080, debug=True)
