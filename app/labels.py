"""
File cấu hình nhãn hiển thị song ngữ (tiếng Anh + giải thích tiếng Việt) cho VietTrans.
Dễ dàng chỉnh sửa hoặc mở rộng ngôn ngữ mà không cần can thiệp vào mã nguồn logic.
"""

LABELS = {
    # 10 mục cấu trúc nội dung của mỗi thẻ học thuật
    "card_sections": {
        "term_vi": {
            "en": "Vietnamese Term",
            "vi": "Từ / cụm từ tiếng Việt",
            "icon": "book-open"
        },
        "suggested_translation": {
            "en": "Suggested Translation",
            "vi": "Gợi ý cách dịch tiếng Anh",
            "icon": "language"
        },
        "meaning": {
            "en": "Meaning",
            "vi": "Giải thích nghĩa",
            "icon": "align-left"
        },
        "cultural_note": {
            "en": "Cultural Note",
            "vi": "Thông tin văn hóa liên quan",
            "icon": "landmark"
        },
        "translation_strategy": {
            "en": "Translation Strategy",
            "vi": "Chiến lược dịch phù hợp",
            "icon": "compass"
        },
        "example": {
            "en": "Example in Context",
            "vi": "Ví dụ trong ngữ cảnh",
            "icon": "quote-right"
        },
        "common_mistake": {
            "en": "Common Mistake",
            "vi": "Lỗi dịch thường gặp",
            "icon": "exclamation-triangle"
        },
        "translation_tip": {
            "en": "Translation Tip",
            "vi": "Lưu ý khi dịch",
            "icon": "check-circle"
        },
        "mini_practice": {
            "en": "Mini Practice",
            "vi": "Bài luyện tập ngắn",
            "icon": "pencil-alt"
        },
        "audio": {
            "en": "Audio Pronunciation",
            "vi": "Phát âm chuẩn",
            "icon": "volume-up"
        }
    },
    
    # Nhãn nút bấm và thao tác giao diện
    "ui": {
        "listen_vi": "Nghe tiếng Việt",
        "listen_en": "Listen in English",
        "show_hint": "Xem gợi ý",
        "hide_hint": "Ẩn gợi ý",
        "show_answer": "Xem gợi ý đáp án",
        "hide_answer": "Ẩn đáp án",
        "your_translation_placeholder": "Nhập bản dịch thử nghiệm của bạn tại đây...",
        "check_translation": "So sánh với đáp án",
        "share": "Chia sẻ thẻ này",
        "copied": "Đã sao chép liên kết!",
        "prev_card": "Thẻ trước",
        "next_card": "Thẻ kế tiếp",
        "related_cards": "Thẻ cùng nhóm văn hóa",
        "scans": "lượt quét",
        "pending_review": "Nội dung đang chờ giảng viên duyệt",
        "reviewed": "Đã kiểm duyệt học thuật"
    }
}
