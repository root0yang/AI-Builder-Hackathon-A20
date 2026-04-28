import os
import sys
from voice_softener_engine import soften_text_to_text
from gemini_tts_pro import generate_gemini_tts_pro

def run_voice_softener_pipeline_text(input_text, output_audio, scenario="C", voice="Aoede"):
    """
    Voice Softener Pipeline (Text Input): 
    1. Text Input -> Gemini 2.5 Flash (Contextual Refinement)
    2. Refined Text -> Gemini 2.5 Flash TTS (Re-synthesis)
    """
    print(f"\n=== Voice Softener Pipeline (Text) 시작 (시나리오 {scenario}) ===")
    print(f"입력 텍스트: {input_text}")

    # 1. 시나리오별 텍스트 정제
    print(f"[1/2] Gemini 2.5 Flash가 맥락을 분석하고 문장을 재구성 중...")
    try:
        refined_text = soften_text_to_text(input_text, scenario)
        print(f"   >> 정제된 결과: {refined_text}")
    except Exception as e:
        print(f"오류 (Refiner): {e}")
        return

    # 2. 페르소나에 맞는 음성으로 재합성
    # 시나리오별 추천 감정/톤 설정
    emotions = {
        "A": "professional and calm",
        "B": "kind and helpful",
        "C": "stable and polite",
        "D": "gentle and soothing"
    }
    target_emotion = emotions.get(scenario, "neutral")
    
    print(f"[2/2] '{voice}' 목소리로 음성 재합성 중... (스타일: {target_emotion})")
    try:
        generate_gemini_tts_pro(
            text=refined_text,
            output_filename=output_audio,
            voice_name=voice,
            emotion=target_emotion,
            speed=1.0
        )
        print(f"=== 완료! 결과 파일: {output_audio} ===")
    except Exception as e:
        print(f"오류 (TTS): {e}")

if __name__ == "__main__":
    # 사용 예시: python3 voice_softener_pipeline_text.py "입력텍스트" <output.mp3> <scenario(A/B/C/D)>
    if len(sys.argv) >= 4:
        run_voice_softener_pipeline_text(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("사용법: python3 voice_softener_pipeline_text.py \"입력텍스트\" <출력파일> <시나리오(A,B,C,D)>")
        print("예시: python3 voice_softener_pipeline_text.py \"야! 너 장난해? 당장 이리 안 와?\" output_text.mp3 C")
