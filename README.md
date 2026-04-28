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

## 🎙 Gemini TTS Pro 단독 사용 가이드

파이프라인을 거치지 않고 직접 `gemini_tts_pro.py`의 기능을 사용하여 텍스트를 음성으로 변환할 수 있습니다. 이 모듈은 감정(Emotion), 어투(Tone), 그리고 표현 태그(Expression Tags)를 상세하게 지정할 수 있는 기능을 제공합니다.

### 1. 기본 사용법 (Python 스크립트 활용)

`AI_Hackathon/gemini_tts_pro.py` 파일 내의 `generate_gemini_tts_pro` 함수를 호출하여 사용합니다.

```python
from gemini_tts_pro import generate_gemini_tts_pro

generate_gemini_tts_pro(
    text="안녕하세요, 만나서 반갑습니다.",
    output_filename="output.mp3",
    voice_name="Aoede",    # 목소리 선택
    emotion="cheerful",    # 감정/어투 지정
    speed=1.0              # 속도 (0.25 ~ 4.0)
)
```

### 2. 감정 및 어투 지정 (Emotion & Tone)

`emotion` 파라미터에 자연어 형태의 설명을 넣으면 Gemini TTS가 그에 맞춰 음성을 생성합니다.

*   **기뿐/활기찬**: `cheerful`, `happy and energetic`, `excited`
*   **차분한/부드러운**: `calm and soothing`, `soft and gentle`, `whispering`
*   **전문적인/진지한**: `professional and authoritative`, `serious and calm`
*   **슬픈/우울한**: `sad and gloomy`, `melancholy`

### 3. 표현 태그 활용 (Expression Tags)

텍스트 중간에 대괄호 `[]`를 사용하여 비언어적 표현을 삽입할 수 있습니다. (모델에 따라 지원 여부 차이가 있을 수 있습니다.)

*   `[laughing]`: 웃음소리
*   `[chuckling]`: 낄낄거리는 소리
*   `[coughs]`: 기침 소리
*   `[sighs]`: 한숨 소리

**예시 문장:**
`"[laughing] 아, 진짜요? [sighs] 휴, 다행이네요. 정말 감사합니다!"`

### 4. 사용 가능한 목소리 (Voices)

| 이름 | 특징 |
| :--- | :--- |
| **Aoede** | 맑고 차분하며 신뢰감 있는 목소리 (기본값) |
| **Puck** | 밝고 장난기 있으며 활기찬 목소리 |
| **Fenrir** | 깊고 묵직하며 권위 있는 남성적인 목소리 |
| **Kore** | 부드럽고 따뜻한 느낌의 목소리 |
| **Charon** | 진중하고 낮은 톤의 목소리 |

## 🎭 시나리오 코드 (Scenario Codes)

| 코드 | 페르소나 이름 | 설명 |
| :--- | :--- | :--- |
| **A** | Professional Executive | 비즈니스 실언 방지 및 정중한 비즈니스 톤 변환 |
| **B** | Kind Explainer | 전문 용어(의료, 법률 등)를 쉬운 일상어로 변환 |
| **C** | Calm Colleague | 폭언 및 무례한 발화를 누그러진 톤과 정중한 표현으로 순화 |
| **D** | Gentle Interpreter | 인지 장애나 혼란스러운 발화를 맥락에 맞게 또렷하게 전달 |

---
© 2026 HarmonyVoice Team. Powered by Google Gemini.
