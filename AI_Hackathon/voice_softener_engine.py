import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part

def get_project_id():
    import subprocess
    try:
        return subprocess.check_output(['gcloud', 'config', 'get-value', 'project']).decode('utf-8').strip()
    except:
        return os.environ.get("GOOGLE_CLOUD_PROJECT")

PROJECT_ID = get_project_id()
vertexai.init(project=PROJECT_ID, location="us-central1")

# 시나리오별 페르소나 정의 (ppt_prompt.md 기반)
PERSONAS = {
    "A": "Professional Executive Mode (비즈니스 미팅 실언, 기밀 정보, 부적절 표현 차단 및 정중한 비즈니스 톤으로 변환)",
    "B": "Kind Explainer (의사, 변호사 등 전문직의 어려운 용어를 일반인이 이해하기 쉬운 평범한 말로 재합성)",
    "C": "Calm Colleague (콜센터 상담원 등이 듣는 폭언, 무례한 발화를 누그러진 톤과 정중한 표현으로 순화)",
    "D": "Gentle Interpreter (자폐 스펙트럼 아동이나 치매 환자의 혼란스러운 발화를 맥락 파악 후 또렷하고 부드러운 톤으로 전달)"
}

def soften_voice_to_text(audio_file_path, scenario_type="C"):
    """
    Gemini 2.5 Flash를 사용하여 오디오를 시나리오별 페르소나에 맞춰 정제된 텍스트로 변환합니다.
    """
    model = GenerativeModel("gemini-2.5-flash")
    persona = PERSONAS.get(scenario_type, PERSONAS["C"])
    
    with open(audio_file_path, "rb") as f:
        audio_data = f.read()
    
    # 파일 확장자에 따른 mime_type 결정
    mime_type = "audio/mpeg"
    if audio_file_path.endswith(".wav"):
        mime_type = "audio/wav"

    audio_part = Part.from_data(data=audio_data, mime_type=mime_type)
    
    system_instruction = f"""
    당신은 'Voice Softener' 시스템의 핵심 엔진입니다. 
    제공된 오디오를 듣고, 다음 페르소나 설정에 맞춰 발화 내용을 재구성하여 정제된 한국어 텍스트로 출력하세요.
    
    [현재 시나리오 페르소나]: {persona}
    
    [작업 지침]:
    1. 오디오의 전체적인 맥락과 화자의 '의도'를 정확히 파악하세요.
    2. 페르소나에 맞춰서 문장을 완전히 새로 작성하되, 핵심 메시지는 잃지 않아야 합니다.
    3. 원문의 공격적인 어조, 전문 용어의 난해함, 발화의 파편화 등을 완전히 해결하세요.
    4. **매우 중요 (비언어적 표현)**: 문장의 분위기를 더 살리기 위해 적절한 위치에 비언어적 표현 태그를 반드시 삽입하세요. 
       **태그는 반드시 대괄호 안에 영어로만(Only English in brackets) 작성해야 합니다.** 한국어로 작성하면 TTS가 그대로 읽어버리므로 절대 금지합니다.
       (예시 태그: [laughing], [chuckling], [sighs], [coughs], [clears throat], [breath], [pause] 등)
    5. 출력은 오직 정제된 최종 한국어 문장만 하며, 부연 설명은 하지 마세요.
    """
    
    response = model.generate_content([system_instruction, audio_part])
    return response.text.strip()

def soften_text_to_text(input_text, scenario_type="C"):
    """
    Gemini 2.5 Flash를 사용하여 텍스트를 시나리오별 페르소나에 맞춰 정제된 텍스트로 변환합니다.
    """
    model = GenerativeModel("gemini-2.5-flash")
    persona = PERSONAS.get(scenario_type, PERSONAS["C"])
    
    system_instruction = f"""
    당신은 'Voice Softener' 시스템의 핵심 엔진입니다. 
    제공된 텍스트를 분석하고, 다음 페르소나 설정에 맞춰 발화 내용을 재구성하여 정제된 한국어 텍스트로 출력하세요.
    
    [현재 시나리오 페르소나]: {persona}
    
    [작업 지침]:
    1. 입력 텍스트의 전체적인 맥락과 화자의 '의도'를 정확히 파악하세요.
    2. 페르소나에 맞춰서 문장을 완전히 새로 작성하되, 핵심 메시지는 잃지 않아야 합니다.
    3. 원문의 공격적인 어조, 전문 용어의 난해함, 발화의 파편화 등을 완전히 해결하세요.
    4. **매우 중요 (비언어적 표현)**: 문장의 분위기를 더 살리기 위해 적절한 위치에 비언어적 표현 태그를 반드시 삽입하세요. 
       **태그는 반드시 대괄호 안에 영어로만(Only English in brackets) 작성해야 합니다.** 한국어로 작성하면 TTS가 그대로 읽어버리므로 절대 금지합니다.
       (예시 태그: [laughing], [chuckling], [sighs], [coughs], [clears throat], [breath], [pause] 등)
    5. 출력은 오직 정제된 최종 한국어 문장만 하며, 부연 설명은 하지 마세요.
    """
    
    response = model.generate_content([system_instruction, input_text])
    return response.text.strip()

if __name__ == "__main__":
    # 간단한 테스트 인터페이스
    print("Voice Softener Engine Loaded.")
