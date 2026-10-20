/* VietTrans Main Client JavaScript */
document.addEventListener('DOMContentLoaded', () => {
    // 1. Theme (Dark/Light mode) Setup
    initTheme();

    // 2. Mobile Menu Toggle
    initMobileMenu();

    // 3. Audio & Web Speech API Synthesis
    initAudioSpeech();

    // 4. Mini Practice Toggle & Compare
    initMiniPractice();

    // 5. Share Card Link
    initShareButton();
});

/* Khởi tạo giao diện sáng / tối */
function initTheme() {
    const savedTheme = localStorage.getItem('viettrans_theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);

    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const current = document.documentElement.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('viettrans_theme', next);
        });
    }
}

/* Menu cho màn hình di động */
function initMobileMenu() {
    const toggleBtn = document.querySelector('.mobile-toggle');
    const navLinks = document.querySelector('.nav-links');
    if (toggleBtn && navLinks) {
        toggleBtn.addEventListener('click', () => {
            navLinks.classList.toggle('is-open');
        });
    }
}

/* Xử lý phát âm từ vựng (chỉ phát âm tiếng Anh chuẩn, rõ ràng) */
function initAudioSpeech() {
    const audioBtn = document.getElementById('audio-play-btn');
    if (!audioBtn) return;

    // Kích hoạt nạp danh sách giọng đọc của trình duyệt từ sớm
    if ('speechSynthesis' in window) {
        window.speechSynthesis.getVoices();
        window.speechSynthesis.onvoiceschanged = () => {
            window.speechSynthesis.getVoices();
        };
    }

    audioBtn.addEventListener('click', () => {
        const audioSrc = audioBtn.getAttribute('data-audio-src');
        const termEn = audioBtn.getAttribute('data-term-en') || '';

        audioBtn.classList.add('is-playing');

        // Trường hợp 1: Có file mp3 thu âm riêng tải lên
        if (audioSrc && audioSrc.trim() !== '') {
            const player = new Audio(audioSrc);
            player.volume = 1.0;
            player.onended = () => audioBtn.classList.remove('is-playing');
            player.onerror = () => playEnglishSpeech(termEn, audioBtn);
            player.play().catch(() => playEnglishSpeech(termEn, audioBtn));
        } else {
            // Trường hợp 2: Phát âm tiếng Anh tự động bằng giọng chuẩn Web Speech API
            playEnglishSpeech(termEn, audioBtn);
        }
    });
}

/**
 * Tìm kiếm giọng đọc tiếng Anh tự nhiên, phát âm to và rõ ràng nhất của thiết bị
 */
function getBestEnglishVoice() {
    if (!('speechSynthesis' in window)) return null;
    const voices = window.speechSynthesis.getVoices();
    if (!voices || voices.length === 0) return null;

    // Danh sách ưu tiên các giọng chất lượng cao, âm lượng chuẩn và phát âm tự nhiên
    const highQualityKeywords = [
        'natural', 'online', 'google us english', 'jenny', 'guy', 'aria',
        'samantha', 'zira', 'karen', 'david', 'google uk english female'
    ];

    for (const kw of highQualityKeywords) {
        const matched = voices.find(v => 
            v.lang.startsWith('en') && v.name.toLowerCase().includes(kw)
        );
        if (matched) return matched;
    }

    // Ưu tiên chuẩn Anh - Mỹ (en-US)
    const usVoice = voices.find(v => v.lang === 'en-US' || v.lang === 'en_US');
    if (usVoice) return usVoice;

    // Ưu tiên chuẩn Anh - Anh (en-GB)
    const gbVoice = voices.find(v => v.lang === 'en-GB' || v.lang === 'en_GB');
    if (gbVoice) return gbVoice;

    // Bất kỳ giọng tiếng Anh nào có sẵn trên máy
    return voices.find(v => v.lang.startsWith('en')) || null;
}

/**
 * Phát âm thuật ngữ tiếng Anh với âm lượng tối đa và tốc độ chuẩn sư phạm
 */
function playEnglishSpeech(textEn, btnElement) {
    if (!('speechSynthesis' in window)) {
        alert('Trình duyệt của bạn chưa hỗ trợ tính năng phát âm trực tiếp.');
        if (btnElement) btnElement.classList.remove('is-playing');
        return;
    }

    if (!textEn || textEn.trim() === '') {
        if (btnElement) btnElement.classList.remove('is-playing');
        return;
    }

    window.speechSynthesis.cancel(); // Dừng các âm thanh đang phát trước đó nếu có

    // Thay thế dấu gạch chéo '/' bằng dấu phẩy để giọng đọc ngắt nhịp tự nhiên, tránh đọc chữ 'slash'
    const cleanSpeechText = textEn.replace(/\s*\/\s*/g, ', ');

    const utterEn = new SpeechSynthesisUtterance(cleanSpeechText);
    utterEn.lang = 'en-US';
    utterEn.volume = 1.0;   // Âm lượng tối đa (to, rõ ràng)
    utterEn.rate = 0.88;     // Tốc độ sư phạm chậm rãi vừa phải giúp sinh viên nghe rõ từng âm tiết
    utterEn.pitch = 1.0;

    const chosenVoice = getBestEnglishVoice();
    if (chosenVoice) {
        utterEn.voice = chosenVoice;
        utterEn.lang = chosenVoice.lang;
    }

    utterEn.onend = () => {
        if (btnElement) btnElement.classList.remove('is-playing');
    };

    utterEn.onerror = (e) => {
        console.warn('SpeechSynthesis error:', e);
        if (btnElement) btnElement.classList.remove('is-playing');
    };

    window.speechSynthesis.speak(utterEn);
}

/* Bật / tắt hiển thị gợi ý đáp án Mini Practice */
function initMiniPractice() {
    const toggleButtons = document.querySelectorAll('.practice-toggle-btn');
    toggleButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-target');
            const answerBox = document.getElementById(targetId);
            if (answerBox) {
                const isShown = answerBox.classList.toggle('is-visible');
                btn.textContent = isShown ? 'Ẩn đáp án gợi ý ▲' : 'Xem đáp án gợi ý ▼';
            }
        });
    });
}

/* Nút sao chép liên kết chia sẻ */
function initShareButton() {
    const shareBtn = document.getElementById('share-card-btn');
    if (!shareBtn) return;

    shareBtn.addEventListener('click', async () => {
        const url = window.location.href;
        try {
            if (navigator.clipboard) {
                await navigator.clipboard.writeText(url);
                showShareFeedback(shareBtn, 'Đã sao chép liên kết!');
            } else if (navigator.share) {
                await navigator.share({
                    title: document.title,
                    url: url
                });
            }
        } catch (err) {
            prompt('Sao chép đường dẫn thẻ tại đây:', url);
        }
    });
}

function showShareFeedback(btn, message) {
    const originalText = btn.innerHTML;
    btn.innerHTML = `<span style="color:var(--color-primary);font-weight:600;">✓ ${message}</span>`;
    setTimeout(() => {
        btn.innerHTML = originalText;
    }, 2500);
}
