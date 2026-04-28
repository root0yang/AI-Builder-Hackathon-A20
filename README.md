# HarmonyVoice: Voice Softener Pipeline

HarmonyVoice는 거친 발화, 어려운 전문 용어, 또는 혼란스러운 표현을 Gemini 2.5 Flash와 Gemini TTS Pro를 활용하여 상황에 맞는 부드럽고 정제된 음성으로 변환해주는 시스템입니다.

## 🛠 주요 기능

1.  **Contextual Refinement**: Gemini 2.5 Flash가 입력된 오디오나 텍스트의 맥락을 분석하여 페르소나에 맞게 문장을 재구성합니다.
2.  **Expressive Synthesis**: 정제된 텍스트를 Gemini TTS Pro를 통해 감정과 톤이 살아있는 자연스러운 음성으로 합성합니다.
3.  **Multi-Scenario Support**: 4가지 주요 시나리오(비즈니스, 전문직, 고객상담, 케어 서비스)를 지원합니다.

## 📂 프로젝트 구조

*   `voice_softener_pipeline.py`: 오디오 파일(.mp3, .wav)을 입력으로 받는 메인 파이프라인
*   `voice_softener_pipeline_text.py`: 텍스트 문장을 직접 입력으로 받는 파이프라인
*   `voice_softener_engine.py`: Gemini 모델을 이용한 텍스트 정제 엔진
*   `gemini_tts_pro.py`: Gemini TTS Pro를 이용한 음성 합성 모듈
*   `HarmonyVoice_Project_Proposal.pdf`: 프로젝트 제안서
*   `ppt_prompt.md`: 프로젝트 발표 및 페르소나 정의 프롬프트

## 🚀 사용 방법

### 1. 텍스트 입력 파이프라인 (추천)

거친 문장이나 난해한 문장을 직접 입력하여 정제된 음성 파일을 생성합니다.

```bash
python3 AI_Hackathon/voice_softener_pipeline_text.py "입력텍스트" <출력파일명.mp3> <시나리오코드>
```

**예시 (고객상담 시나리오 C):**
```bash
python3 AI_Hackathon/voice_softener_pipeline_text.py "야! 너 장난해? 당장 이리 안 와? 왜 이렇게 늦어!" output_c.mp3 C
```

### 2. 오디오 입력 파이프라인

녹음된 음성 파일을 입력하여 정제된 새 음성 파일을 생성합니다.

```bash
python3 AI_Hackathon/voice_softener_pipeline.py <입력파일명.mp3> <출력파일명.mp3> <시나리오코드>
```

**예시 (의료/전문직 시나리오 B):**
```bash
python3 AI_Hackathon/voice_softener_pipeline.py input_doctor.mp3 output_kind_doctor.mp3 B
```

## 🎭 시나리오 코드 (Scenario Codes)

| 코드 | 페르소나 이름 | 설명 |
| :--- | :--- | :--- |
| **A** | Professional Executive | 비즈니스 실언 방지 및 정중한 비즈니스 톤 변환 |
| **B** | Kind Explainer | 전문 용어(의료, 법률 등)를 쉬운 일상어로 변환 |
| **C** | Calm Colleague | 폭언 및 무례한 발화를 누그러진 톤과 정중한 표현으로 순화 |
| **D** | Gentle Interpreter | 인지 장애나 혼란스러운 발화를 맥락에 맞게 또렷하게 전달 |

---
© 2026 HarmonyVoice Team. Powered by Google Gemini.
