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

# 시나리오별 페르소나 정의
PERSONAS = {
    "A": "Professional Executive Mode (비즈니스 미팅 실언 방지 및 정중하고 명확한 비즈니스 톤으로 변환)",
    "B": "Kind Explainer (전문 용어를 일반인이 이해하기 쉬운 따뜻하고 평범한 말로 재구성)",
    "C": "Calm Colleague (폭언, 무례한 발화를 차분하고 정중한 표현으로 순화하여 전달)",
    "D": "Gentle Interpreter (혼란스러운 발화를 맥락 파악 후 또렷하고 부드러운 톤으로 정리)"
}

def soften_voice_to_text(audio_file_path, scenario_type="C"):
    """
    Gemini 2.5 Flash를 사용하여 오디오를 시나리오별 페르소나에 맞춰 정제된 텍스트로 변환합니다.
    """
    model = GenerativeModel("gemini-2.5-flash")
    persona = PERSONAS.get(scenario_type, PERSONAS["C"])
    
    with open(audio_file_path, "rb") as f:
        audio_data = f.read()
    
    mime_type = "audio/mpeg"
    if audio_file_path.endswith(".wav"):
        mime_type = "audio/wav"

    audio_part = Part.from_data(data=audio_data, mime_type=mime_type)
    
    system_instruction = f"""
    당신은 음성 인식 결과에서 **언어적 잡음(Fillers)**만 정교하게 제거하는 오디오 전처리 편집자입니다. 
    제공된 오디오를 분석하여 다음 지침에 따라 정제된 결과를 출력하세요.
    
    [현재 시나리오 페르소나]: {persona}
    
    [작업 지침]:
    1. **Remove Fillers**: 의미 없는 추임새('어, 음, 그, 좀, 아, 저기' 등)와 당황해서 반복되는 단어 파편만 삭제하십시오.
    2. **Maintain Persona**: 사용자의 원래 말투(예: ~요, ~해요 어미)와 감정 섞인 부사(예: 진짜, 너무)는 절대 수정하거나 삭제하지 마십시오. 사용자의 고유한 성격이 드러나야 합니다.
    3. **Sentence Stitching**: 파편화된 문장을 자연스러운 호흡으로 연결하되, 새로운 정보를 추가하거나 핵심 어휘를 바꾸지 마십시오.
    4. **Metadata Output**: 출력물의 맨 앞에는 반드시 대괄호 []를 사용하여 감정, 속도, 명료도 상태를 명시하십시오. 
       형식 예시: [감정: 차분해지려 노력함, 속도: 보통, 명료도: 높음]
    5. **Expression Tags**: 문장 중간에 비언어적 표현이 필요한 경우 반드시 **영어 태그**를 사용하십시오. (예: [sighs], [clears throat], [pause] 등)
    6. **Output Goal**: 사용자가 숨을 한 번 고르고 차분하게 말했을 때의 결과물처럼 만드십시오.
    
    출력은 오직 [메타데이터] "정제된 문장" 형식으로만 하며, 부연 설명은 하지 마세요.
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
    당신은 음성 인식 결과에서 **언어적 잡음(Fillers)**만 정교하게 제거하는 오디오 전처리 편집자입니다. 
    제공된 텍스트를 분석하여 다음 지침에 따라 정제된 결과를 출력하세요.
    
    [현재 시나리오 페르소나]: {persona}
    
    [작업 지침]:
    1. **Remove Fillers**: 의미 없는 추임새('어, 음, 그, 좀, 아, 저기' 등)와 당황해서 반복되는 단어 파편만 삭제하십시오.
    2. **Maintain Persona**: 사용자의 원래 말투(예: ~요, ~해요 어미)와 감정 섞인 부사(예: 진짜, 너무)는 절대 수정하거나 삭제하지 마십시오. 사용자의 고유한 성격이 드러나야 합니다.
    3. **Sentence Stitching**: 파편화된 문장을 자연스러운 호흡으로 연결하되, 새로운 정보를 추가하거나 핵심 어휘를 바꾸지 마십시오.
    4. **Metadata Output**: 출력물의 맨 앞에는 반드시 대괄호 []를 사용하여 감정, 속도, 명료도 상태를 명시하십시오. 
       형식 예시: [감정: 차분해지려 노력함, 속도: 보통, 명료도: 높음]
    5. **Expression Tags**: 문장 중간에 비언어적 표현이 필요한 경우 반드시 **영어 태그**를 사용하십시오. (예: [sighs], [clears throat], [pause] 등)
    6. **Output Goal**: 사용자가 숨을 한 번 고르고 차분하게 말했을 때의 결과물처럼 만드십시오.
    
    출력은 오직 [메타데이터] "정제된 문장" 형식으로만 하며, 부연 설명은 하지 마세요.
    """
    
    response = model.generate_content([system_instruction, input_text])
    return response.text.strip()
    
    response = model.generate_content([system_instruction, input_text])
    return response.text.strip()

if __name__ == "__main__":
    # 간단한 테스트 인터페이스
    print("Voice Softener Engine Loaded.")
