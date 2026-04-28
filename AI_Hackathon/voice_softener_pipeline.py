import os
import sys
from voice_softener_engine import soften_voice_to_text
from gemini_tts_pro import generate_gemini_tts_pro

def run_voice_softener_pipeline(input_audio, output_audio, scenario="C", voice="Aoede"):
    """
    Voice Softener Pipeline: 
    1. Audio Input -> Gemini 2.5 Flash (Contextual Refinement)
    2. Refined Text -> Gemini 2.5 Flash TTS (Re-synthesis)
    """
    print(f"\n=== Voice Softener Pipeline 시작 (시나리오 {scenario}) ===")
    
    if not os.path.exists(input_audio):
        print(f"오류: 입력 파일 '{input_audio}'을 찾을 수 없습니다.")
        return

    # 1. 시나리오별 텍스트 정제
    print(f"[1/2] Gemini 2.5 Flash가 맥락을 분석하고 문장을 재구성 중...")
    try:
        refined_text = soften_voice_to_text(input_audio, scenario)
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
    # 사용 예시: python3 voice_softener_pipeline.py <input.mp3> <output.mp3> <scenario(A/B/C/D)>
    if len(sys.argv) >= 4:
        run_voice_softener_pipeline(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("사용법: python3 voice_softener_pipeline.py <입력파일> <출력파일> <시나리오(A,B,C,D)>")
        print("예시: python3 voice_softener_pipeline.py input.mp3 output.mp3 C")
