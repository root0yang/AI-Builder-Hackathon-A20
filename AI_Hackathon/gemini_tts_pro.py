import os
import re
from google.cloud import texttospeech_v1beta1 as texttospeech

def get_project_id():
    import subprocess
    try:
        return subprocess.check_output(['gcloud', 'config', 'get-value', 'project']).decode('utf-8').strip()
    except:
        return os.environ.get("GOOGLE_CLOUD_PROJECT")

PROJECT_ID = get_project_id()

def parse_metadata(text):
    """
    텍스트 앞부분의 [감정: ..., 속도: ...] 형식을 파싱합니다.
    """
    metadata = {}
    match = re.search(r'\[(.*?)\]', text)
    if match:
        meta_str = match.group(1)
        # 감정 추출
        emotion_match = re.search(r'감정:\s*([^,\]]+)', meta_str)
        if emotion_match:
            metadata['emotion'] = emotion_match.group(1).strip()
        
        # 속도 추출
        speed_match = re.search(r'속도:\s*([^,\]]+)', meta_str)
        if speed_match:
            speed_str = speed_match.group(1).strip()
            if "빠름" in speed_str: metadata['speed'] = 1.2
            elif "느림" in speed_str: metadata['speed'] = 0.8
            else: metadata['speed'] = 1.0
            
        # 메타데이터를 제외한 순수 텍스트 반환
        clean_text = text.replace(match.group(0), "").strip()
        return metadata, clean_text
    
    return {}, text

def generate_gemini_tts_pro(
    text, 
    output_filename, 
    voice_name="Aoede", 
    emotion="neutral", 
    speed=1.0,
    language_code="ko-KR",
    model_name="gemini-2.5-flash-tts"
):
    """
    Gemini TTS의 고급 기능(표현 태그 등)을 사용하여 음성을 생성합니다.
    입력 텍스트에 포함된 메타데이터를 파싱하여 감정과 속도를 조절합니다.
    """
    client = texttospeech.TextToSpeechClient()

    # 메타데이터 파싱
    metadata, clean_text = parse_metadata(text)
    
    # 파싱된 값이 있으면 덮어쓰기
    final_emotion = metadata.get('emotion', emotion)
    final_speed = metadata.get('speed', speed)

    # 음성 설정
    voice = texttospeech.VoiceSelectionParams(
        name=voice_name,
        language_code=language_code,
        model_name=model_name
    )

    # 입력 텍스트 설정
    synthesis_input = texttospeech.SynthesisInput(
        text=clean_text,
        prompt=f"Say this in a {final_emotion} style."
    )

    # 오디오 설정
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=final_speed
    )

    print(f"--- Gemini TTS Pro 생성 시작 ---")
    print(f"텍스트(순수): {clean_text}")
    print(f"설정: 목소리={voice_name}, 감정={final_emotion}, 속도={final_speed}")

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

if __name__ == "__main__":
    # 표현 태그 [laughing] 및 감정 조절 테스트
    expressive_text = "[laughing] 아, 진짜요? 그건 생각지도 못했네요! [chuckling] 정말 대단하세요."
    generate_gemini_tts_pro(
        text=expressive_text,
        output_filename="output_expressive.mp3",
        voice_name="Puck",
        emotion="surprised and amused",
        speed=1.0
    )

    # 공식 가이드의 다른 목소리들도 테스트 가능
    # Fenrir: 강하고 대담한 느낌
    generate_gemini_tts_pro(
        text="[coughs] 크흠, 자 이제 시작해볼까요? 모두 집중해주세요.",
        output_filename="output_bold.mp3",
        voice_name="Fenrir",
        emotion="authoritative and serious",
        speed=0.95
    )
