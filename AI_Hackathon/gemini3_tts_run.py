import os
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

# 환경 설정
PROJECT_ID = "qwiklabs-gcp-03-2291d63ef647"
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)

def generate_gemini_3_tts(
    text, 
    output_filename, 
    voice_name="Puck", 
    emotion="happy", 
    speed=1.0
):
    """
    Gemini 3.0 Flash TTS 모델을 사용하여 정밀한 음성을 생성합니다.
    """
    # Gemini 3.0 Flash TTS 모델 선택
    model = GenerativeModel("gemini-3.0-flash-tts")

    # 시스템 인스트럭션을 통해 감정 및 스타일 지정
    system_instruction = f"""
    You are an advanced TTS engine using the Gemini 3.0 architecture.
    Voice Preset: {voice_name}
    Target Emotion: {emotion}
    Speaking Speed: {speed}x
    
    Generate high-fidelity audio based on the text provided.
    Output format must be audio/mpeg.
    """

    # 모델 재설정 (System Instruction 포함)
    model = GenerativeModel(
        "gemini-3.0-flash-tts",
        system_instruction=[system_instruction]
    )

    print(f"--- Gemini 3.0 TTS 생성 시작 ---")
    print(f"텍스트: {text[:20]}...")
    print(f"설정: 목소리={voice_name}, 감정={emotion}, 속도={speed}")

    try:
        # 오디오 생성 요청
        response = model.generate_content(
            text,
            generation_config=GenerationConfig(
                response_mime_type="audio/mpeg"
            )
        )

        # 결과 저장
        if response.candidates[0].content.parts:
            audio_part = response.candidates[0].content.parts[0]
            if hasattr(audio_part, 'inline_data'):
                with open(output_filename, "wb") as f:
                    f.write(audio_part.inline_data.data)
                print(f"성공! Gemini 3.0 음성 파일 생성됨: {output_filename}")
            else:
                print("오디오 데이터를 생성하지 못했습니다. 응답 형식을 확인하세요.")
    except Exception as e:
        print(f"오류 발생: {str(e)}")

if __name__ == "__main__":
    sample_text = "안녕하세요. 저는 제미나이 3.0 플래시 TTS 모델입니다. 더욱 발전된 음성 합성 기술을 경험해 보세요."
    
    # 정밀 제어 테스트
    generate_gemini_3_tts(
        sample_text, 
        "gemini3_puck_happy.mp3", 
        voice_name="Puck", 
        emotion="energetic and joyful", 
        speed=1.1
    )
