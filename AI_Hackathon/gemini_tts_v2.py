import os
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig, Part

# 현재 환경에서 프로젝트 ID 가져오기
def get_project_id():
    import subprocess
    try:
        return subprocess.check_output(['gcloud', 'config', 'get-value', 'project']).decode('utf-8').strip()
    except:
        return os.environ.get("GOOGLE_CLOUD_PROJECT")

PROJECT_ID = get_project_id()
LOCATION = "us-central1"

print(f"Project ID: {PROJECT_ID}")
vertexai.init(project=PROJECT_ID, location=LOCATION)

def generate_voice_from_gemini(text, output_file, voice_preset="Puck"):
    """
    Gemini 1.5 Flash 002 모델을 사용하여 텍스트를 음성으로 변환합니다.
    voice_preset: "Puck", "Charon", "Kore", "Fenrir", "Aoede" 등 공식 가이드의 목소리 선택 가능
    """
    model = GenerativeModel("gemini-1.5-flash-001")

    # 가이드에 따른 정밀한 프롬프트 설정
    prompt = f"Please read the following text in the voice of {voice_preset}: {text}"

    # 오디오 출력을 위한 설정 (MIME TYPE 지정)
    generation_config = GenerationConfig(
        response_mime_type="audio/mpeg"
    )

    print(f"음성 합성 중... (목소리: {voice_preset})")
    
    try:
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )

        # 응답 데이터에서 오디오 추출
        if response.candidates[0].content.parts:
            part = response.candidates[0].content.parts[0]
            if hasattr(part, 'inline_data'):
                audio_data = part.inline_data.data
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"성공! 음성이 저장되었습니다: {output_file}")
            else:
                print("오디오 데이터를 받지 못했습니다. 모델이 텍스트로 응답했습니다.")
                print(f"응답 내용: {response.text}")
    except Exception as e:
        print(f"오류 발생: {str(e)}")

if __name__ == "__main__":
    test_text = "안녕하세요! 구글 클라우드 제미나이 TTS 기능을 테스트하고 있습니다. 정말 자연스러운 목소리네요."
    
    # 가이드에서 추천하는 다양한 목소리 프리셋 테스트
    generate_voice_from_gemini(test_text, "voice_puck.mp3", "Puck") # 장난기 있고 활기찬
    generate_voice_from_gemini(test_text, "voice_aoede.mp3", "Aoede") # 부드럽고 서정적인
