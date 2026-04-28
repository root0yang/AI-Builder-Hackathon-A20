document.addEventListener('DOMContentLoaded', () => {
    const scenarioCards = document.querySelectorAll('.scenario-card');
    const softenBtn = document.getElementById('softenBtn');
    const inputText = document.getElementById('inputText');
    const voiceSelect = document.getElementById('voice');
    const refinedTextDiv = document.getElementById('refinedText');
    const audioPlayer = document.getElementById('audioPlayer');
    const resultSection = document.getElementById('resultSection');
    const loader = document.getElementById('loader');

    let selectedScenario = 'C';

    // 시나리오 선택 핸들러
    scenarioCards.forEach(card => {
        card.addEventListener('click', () => {
            scenarioCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            selectedScenario = card.dataset.scenario;
        });
    });

    // 변환 버튼 핸들러
    softenBtn.addEventListener('click', async () => {
        const text = inputText.value.trim();
        if (!text) {
            alert('순화할 문장을 입력해주세요.');
            return;
        }

        // 로딩 시작
        loader.classList.remove('hidden');
        resultSection.classList.add('hidden');

        try {
            const response = await fetch('/api/soften', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    scenario: selectedScenario,
                    voice: voiceSelect.value
                }),
            });

            const data = await response.json();

            if (response.ok) {
                // 결과 표시
                displayRefinedText(data.refined_text);
                audioPlayer.src = data.audio_url;
                resultSection.classList.remove('hidden');
                
                // 자동 재생 (브라우저 정책에 따라 안될 수 있음)
                audioPlayer.play().catch(e => console.log("Auto-play prevented", e));
            } else {
                alert('오류 발생: ' + (data.error || '알 수 없는 오류가 발생했습니다.'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('서버와 통신 중 오류가 발생했습니다.');
        } finally {
            // 로딩 종료
            loader.classList.add('hidden');
        }
    });

    // 태그 하이라이팅을 포함한 텍스트 표시 함수
    function displayRefinedText(text) {
        // [tag] 형태를 <span class="tag">[tag]</span>로 변환
        const htmlText = text.replace(/\[([a-zA-Z\s]+)\]/g, '<span class="tag">[$1]</span>');
        refinedTextDiv.innerHTML = htmlText;
    }
});
