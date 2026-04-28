import os
from google.cloud import texttospeech_v1beta1 as texttospeech

def get_project_id():
    import subprocess
    try:
        return subprocess.check_output(['gcloud', 'config', 'get-value', 'project']).decode('utf-8').strip()
    except:
        return os.environ.get("GOOGLE_CLOUD_PROJECT")

PROJECT_ID = get_project_id()

def generate_gemini_tts(
    text, 
    output_filename, 
    voice_name="Aoede", 
    emotion="happy and energetic", 
    speed=1.0,
    language_code="ko-KR"
):
    """
    Gemini TTS를 사용하여 감정과 속도가 조절된 음성을 생성합니다.
    
    Args:
        text: 변환할 텍스트
        output_filename: 저장할 파일명 (.mp3)
        voice_name: 사용할 목소리 이름 (Aoede, Puck, Charon, Kore, Fenrir 등)
        emotion: 감정 및 스타일 프롬프트 (예: "sad", "excited", "whispering")
        speed: 말하기 속도 (0.25 ~ 4.0)
        language_code: 언어 코드 (ko-KR, en-US 등)
    """
    client = texttospeech.TextToSpeechClient()

    # 가이드에 따른 음성 및 모델 설정
    # 모델명은 가이드에 언급된 gemini-3.1-flash-tts-preview 또는 gemini-3.0-flash-tts 등을 시도해볼 수 있습니다.
    # 여기서는 사용자가 기존에 사용하던 gemini-3.0-flash-tts를 기본으로 시도합니다.
    voice = texttospeech.VoiceSelectionParams(
        name=voice_name,
        language_code=language_code,
        model_name="gemini-3.1-flash-tts-preview" 
    )

    # 감정/스타일 제어를 위한 프롬프트 설정
    # 텍스트와 함께 감정 지시어를 전달합니다.
    synthesis_input = texttospeech.SynthesisInput(
        text=text,
        prompt=f"Say this in a {emotion} tone."
    )

    # 속도 및 인코딩 설정
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speed
    )

    print(f"--- Gemini TTS 생성 시작 ---")
    print(f"텍스트: {text[:30]}...")
    print(f"설정: 목소리={voice_name}, 감정={emotion}, 속도={speed}, 모델=gemini-3.1-flash-tts-preview")

    try:
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        with open(output_filename, "wb") as out:
            out.write(response.audio_content)
            print(f"성공! 음성 파일이 생성되었습니다: {output_filename}")

    except Exception as e:
        print(f"오류 발생: {str(e)}")
        # 만약 3.1 모델이 아직 지원되지 않는다면 3.0으로 재시도
        if "3.1" in str(e):
            print("gemini-3.1-flash-tts-preview 모델을 찾을 수 없어 gemini-3.0-flash-tts로 재시도합니다.")
            try:
                voice.model_name = "gemini-3.0-flash-tts"
                response = client.synthesize_speech(
                    input=synthesis_input,
                    voice=voice,
                    audio_config=audio_config
                )
                with open(output_filename, "wb") as out:
                    out.write(response.audio_content)
                    print(f"성공! (gemini-3.0-flash-tts) 음성 파일이 생성되었습니다: {output_filename}")
            except Exception as e2:
                print(f"재시도 실패: {str(e2)}")

if __name__ == "__main__":
    # 테스트 1: 활기찬 한국어 음성
    generate_gemini_tts(
        text="와, 드디어 제미나이 TTS를 성공적으로 구현했어요! 정말 신기하고 재미있네요.",
        output_filename="output_happy.mp3",
        voice_name="Puck",
        emotion="very happy and excited",
        speed=1.1
    )

    # 테스트 2: 차분한 한국어 음성
    generate_gemini_tts(
        text="오늘 하루는 어떠셨나요? 잠시 여유를 가지고 차분하게 생각해보는 시간을 가져보세요.",
        output_filename="output_calm.mp3",
        voice_name="Aoede",
        emotion="calm and soothing",
        speed=0.9
    )
