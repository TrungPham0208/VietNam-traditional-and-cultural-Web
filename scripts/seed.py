"""
Script khởi tạo dữ liệu mẫu cho hệ thống VietTrans (scripts/seed.py).
Nạp 5 nhóm văn hóa và 5 thẻ học thuật mẫu:
1. Lì xì (Tết & Lễ hội) - Reviewed: True (đúng chuẩn đề bài)
2. Áo dài (Trang phục & Nghệ thuật) - Reviewed: False
3. Bánh chưng (Ẩm thực) - Reviewed: False
4. Cúng giao thừa (Gia đình, Tín ngưỡng) - Reviewed: False
5. Nón lá (Trang phục & Nghệ thuật) - Reviewed: False
"""
import sys
from pathlib import Path

# Đảm bảo in tiếng Việt trên console Windows không bị lỗi UnicodeEncodeError
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# Thêm thư mục gốc vào PYTHONPATH
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import engine, SessionLocal, Base
from app.models.category import Category
from app.models.card import Card, CardExample, PracticeItem
from app.models.contact import ContactMessage

CATEGORIES_DATA = [
    {
        "slug": "tet-le-hoi",
        "name_vi": "Tết và lễ hội",
        "name_en": "Tet & Traditional Festivals",
        "description": "Các phong tục, nghi lễ, vật phẩm và món ăn gắn liền với Tết Nguyên đán và các ngày hội truyền thống dân tộc.",
        "icon": "lantern",
        "expected_cards_min": 8,
        "expected_cards_max": 10,
        "sort_order": 1
    },
    {
        "slug": "am-thuc",
        "name_vi": "Ẩm thực truyền thống",
        "name_en": "Traditional Cuisine",
        "description": "Tinh hoa các món ăn, thức uống, gia vị và triết lý ẩm thực cân bằng âm dương của người Việt.",
        "icon": "bowl",
        "expected_cards_min": 6,
        "expected_cards_max": 8,
        "sort_order": 2
    },
    {
        "slug": "trang-phuc-nghe-thuat",
        "name_vi": "Trang phục và nghệ thuật",
        "name_en": "Attire & Performing Arts",
        "description": "Trang phục truyền thống các vùng miền, nhạc cụ dân tộc và các loại hình nghệ thuật dân gian độc đáo.",
        "icon": "dress",
        "expected_cards_min": 6,
        "expected_cards_max": 8,
        "sort_order": 3
    },
    {
        "slug": "gia-dinh-tin-nguong",
        "name_vi": "Gia đình, tín ngưỡng",
        "name_en": "Family & Spiritual Beliefs",
        "description": "Đạo hiếu, phong tục thờ cúng tổ tiên, các tín ngưỡng dân gian và nghi lễ vòng đời của người Việt.",
        "icon": "incense",
        "expected_cards_min": 6,
        "expected_cards_max": 8,
        "sort_order": 4
    },
    {
        "slug": "doi-song-phong-tuc",
        "name_vi": "Đời sống và phong tục",
        "name_en": "Daily Life & Customs",
        "description": "Nếp sống làng quê, thói quen sinh hoạt, văn hóa ứng xử và giao tiếp truyền thống của người Việt Nam.",
        "icon": "people",
        "expected_cards_min": 6,
        "expected_cards_max": 8,
        "sort_order": 5
    }
]

CARDS_DATA = [
    # 1. Thẻ LÌ XÌ (Đúng chuẩn đề bài - reviewed=True)
    {
        "slug": "li-xi",
        "term_vi": "Lì xì",
        "category_slug": "tet-le-hoi",
        "category_label": "Tết – Lễ hội",
        "tagline_en": "Small tradition, Big meaning",
        "suggested_translation": "lucky money / giving lucky money",
        "meaning": "Tiền được tặng trong phong bì đỏ, đặc biệt cho trẻ em và các thành viên trẻ trong gia đình vào dịp Tết Nguyên đán, kèm lời chúc sức khỏe, may mắn và thịnh vượng.",
        "cultural_note": "Lì xì là một tập tục truyền thống của Việt Nam, phản ánh các giá trị về sự hào phóng, gắn kết gia đình và cầu may đầu năm.",
        "translation_strategy": "Mô tả tập tục và ý nghĩa văn hóa của nó, tránh dịch từng chữ (literal translation).",
        "common_mistake": "give money for luck (dịch quá sát nghĩa đen).",
        "translation_tip": "Dùng các thuật ngữ tự nhiên và phổ biến: 'lucky money', 'give lucky money'.",
        "status": "published",
        "reviewed": True,
        "examples": [
            {
                "sentence_vi": "Trẻ em được nhận lì xì vào dịp Tết.",
                "sentence_en": "Children are given lucky money at Tết.",
                "sort_order": 1
            },
            {
                "sentence_vi": "Lì xì tượng trưng cho những lời chúc tốt lành về một năm mới an khang, thịnh vượng.",
                "sentence_en": "Li xi symbolizes good wishes for a prosperous new year.",
                "sort_order": 2
            }
        ],
        "practice": {
            "prompt": "Dịch câu: 'Ông bà thường lì xì cho cháu vào sáng mùng Một.'",
            "suggested_answer": "Grandparents usually give lucky money to their grandchildren on the morning of the first day of Tet.",
            "hint": "Dùng cụm 'give lucky money to someone' và 'the morning of the first day of Tet'."
        }
    },
    
    # 2. Thẻ ÁO DÀI (reviewed=False)
    {
        "slug": "ao-dai",
        "term_vi": "Áo dài",
        "category_slug": "trang-phuc-nghe-thuat",
        "category_label": "Trang phục – Nghệ thuật",
        "tagline_en": "Grace in Every Fold",
        "suggested_translation": "Ao Dai / Vietnamese traditional long dress",
        "meaning": "Trang phục truyền thống của người Việt, gồm tà áo dài xẻ hai bên mặc cùng quần ống rộng, tôn vinh nét duyên dáng, kín đáo và thanh lịch.",
        "cultural_note": "Áo dài gắn liền với bản sắc và niềm tự hào dân tộc, thường được mặc trong các dịp lễ tết, cưới hỏi, sự kiện ngoại giao và làm đồng phục học đường.",
        "translation_strategy": "Giữ nguyên từ mượn 'Ao Dai' (đã được công nhận trong từ điển Oxford) kèm cụm giải thích 'Vietnamese traditional long dress' khi giới thiệu cho độc giả quốc tế lần đầu tiếp cận.",
        "common_mistake": "long dress / Vietnamese dress (quá chung chung, làm mất đi tính định danh văn hóa đặc thù).",
        "translation_tip": "Viết hoa danh từ riêng 'Ao Dai' và tránh dịch thô thành 'long shirt' hay 'two-piece gown'.",
        "status": "published",
        "reviewed": False,
        "examples": [
            {
                "sentence_vi": "Nữ sinh Việt Nam thường mặc áo dài trắng tinh khôi vào ngày khai trường.",
                "sentence_en": "Vietnamese female students often wear pristine white Ao Dai on the school opening day.",
                "sort_order": 1
            },
            {
                "sentence_vi": "Áo dài là biểu tượng cho vẻ đẹp dịu dàng và thanh lịch của người phụ nữ Việt.",
                "sentence_en": "The Ao Dai is a symbol of the graceful and elegant beauty of Vietnamese women.",
                "sort_order": 2
            }
        ],
        "practice": {
            "prompt": "Dịch câu: 'Mẹ tôi chọn một bộ áo dài lụa màu xanh ngọc để dự lễ cưới.'",
            "suggested_answer": "My mother chose a jade-green silk Ao Dai to attend the wedding ceremony.",
            "hint": "Dùng cụm 'jade-green silk Ao Dai' và động từ 'choose / chose'."
        }
    },

    # 3. Thẻ BÁNH CHƯNG (reviewed=False)
    {
        "slug": "banh-chung",
        "term_vi": "Bánh chưng",
        "category_slug": "am-thuc",
        "category_label": "Ẩm thực truyền thống",
        "tagline_en": "Flavors of Gratitude and Earth",
        "suggested_translation": "Banh chung / Square sticky rice cake",
        "meaning": "Loại bánh truyền thống hình vuông làm từ gạo nếp, đỗ xanh, thịt lợn, gói bằng lá dong và luộc kỹ trong nhiều giờ, tượng trưng cho Đất và lòng biết ơn tổ tiên.",
        "cultural_note": "Gắn liền với sự tích Lang Liêu thời Hùng Vương, bánh chưng là linh hồn ẩm thực ngày Tết cổ truyền, thể hiện sự hòa hợp âm dương và đạo lý tri ân cội nguồn.",
        "translation_strategy": "Sử dụng tên gọi bản địa 'Banh chung' kết hợp định nghĩa mô tả 'square sticky rice cake filled with mung beans and pork' ở lần nhắc đầu tiên trong văn bản.",
        "common_mistake": "Chung cake (lai tạp không tự nhiên) hoặc square sticky rice cake đơn lẻ mà không có tên gốc.",
        "translation_tip": "Bảo tồn tên riêng 'Banh chung' như một yếu tố văn hóa đặc thù (CSI - Culture-Specific Item), bổ sung chú thích nguyên liệu ngắn gọn khi cần.",
        "status": "published",
        "reviewed": False,
        "examples": [
            {
                "sentence_vi": "Cả gia đình quây quần bên nồi bánh chưng nghi ngút khói trong đêm giao thừa.",
                "sentence_en": "The whole family gathered around the steaming pot of Banh chung on New Year's Eve.",
                "sort_order": 1
            },
            {
                "sentence_vi": "Bánh chưng là món ăn không thể thiếu trên mâm cỗ Tết của người Việt.",
                "sentence_en": "Banh chung is an indispensable dish on the Vietnamese Tet feast table.",
                "sort_order": 2
            }
        ],
        "practice": {
            "prompt": "Dịch câu: 'Gói bánh chưng đòi hỏi sự khéo léo và kiên nhẫn của người làm.'",
            "suggested_answer": "Making Banh chung requires great craftsmanship and patience.",
            "hint": "Dùng 'Wrapping/Making Banh chung' và 'craftsmanship/dexterity and patience'."
        }
    },

    # 4. Thẻ CÚNG GIAO THỪA (reviewed=False)
    {
        "slug": "cung-giao-thua",
        "term_vi": "Cúng giao thừa",
        "category_slug": "gia-dinh-tin-nguong",
        "category_label": "Gia đình – Tín ngưỡng",
        "tagline_en": "Sacred Transition of the Old and New",
        "suggested_translation": "New Year's Eve ritual / offering ceremony at the sacred transition",
        "meaning": "Lễ cúng trang trọng vào thời khắc chuyển giao giữa năm cũ và năm mới (đêm 30 Tết), gồm lễ cúng ngoài trời tiễn quan hành khiển cũ nghênh đón quan mới và lễ cúng trong nhà kính dâng gia tiên.",
        "cultural_note": "Nghi lễ mang ý nghĩa trừ bỏ những điều không may của năm cũ, nghênh đón điềm lành và cầu chúc bình an, thuận hòa cho cả gia đình trong năm mới.",
        "translation_strategy": "Áp dụng chiến lược dịch tương đương chức năng (functional equivalence), làm nổi bật ý nghĩa thiêng liêng của nghi lễ thay vì dịch từng chữ gây hiểu lầm.",
        "common_mistake": "Worship midnight / Pray at 12 PM (sai thuật ngữ nghi lễ trang trọng và sai mốc thời gian).",
        "translation_tip": "Dùng cụm 'offering ceremony' hoặc 'New Year's Eve ritual' kết hợp diễn đạt tự nhiên.",
        "status": "published",
        "reviewed": False,
        "examples": [
            {
                "sentence_vi": "Mâm cúng giao thừa ngoài trời luôn được chuẩn bị chu đáo trước nửa đêm.",
                "sentence_en": "The outdoor offering table for the New Year's Eve ritual is always meticulously prepared before midnight.",
                "sort_order": 1
            },
            {
                "sentence_vi": "Lễ cúng giao thừa thể hiện đạo lý tri ân tổ tiên sâu sắc của người Việt.",
                "sentence_en": "The New Year's Eve offering ceremony reflects the deep Vietnamese tradition of honoring ancestors.",
                "sort_order": 2
            }
        ],
        "practice": {
            "prompt": "Dịch câu: 'Vào thời khắc giao thừa, mọi người cùng thắp hương cầu mong một năm bình an.'",
            "suggested_answer": "At the stroke of midnight on New Year's Eve, everyone lights incense to pray for a peaceful year.",
            "hint": "Cụm 'vào thời khắc giao thừa' dịch tự nhiên là 'at the stroke of midnight on New Year's Eve'."
        }
    },

    # 5. Thẻ NÓN LÁ (reviewed=False)
    {
        "slug": "non-la",
        "term_vi": "Nón lá",
        "category_slug": "trang-phuc-nghe-thuat",
        "category_label": "Trang phục – Nghệ thuật",
        "tagline_en": "A Gentle Shade of Simplicity",
        "suggested_translation": "Vietnamese conical hat / Non la",
        "meaning": "Chiếc nón có hình chóp nhọn, đan thủ công từ lá cọ hoặc lá gồi phơi khô, vừa che mưa nắng vừa là phụ kiện tôn lên nét duyên của người phụ nữ Việt Nam.",
        "cultural_note": "Nón lá gắn bó mật thiết với nền văn minh lúa nước, làng quê truyền thống và là biểu tượng mộc mạc, bình dị của người lao động Việt Nam.",
        "translation_strategy": "Dùng thuật ngữ phổ biến 'Vietnamese conical hat' hoặc dùng tên riêng 'Non la' kèm mô tả chức năng 'traditional conical hat made of palm leaves'.",
        "common_mistake": "leaf hat (dịch quá sát nghĩa đen, nghe thô ráp và thiếu tính biểu tượng).",
        "translation_tip": "Luôn dùng 'conical hat' vì đặc điểm hình chóp (cone) là dấu hiệu nhận diện trực quan chuẩn xác nhất với người nước ngoài.",
        "status": "published",
        "reviewed": False,
        "examples": [
            {
                "sentence_vi": "Chiếc nón lá che mát cho người nông dân trên cánh đồng lúa chín vàng.",
                "sentence_en": "The conical hat shades farmers under the sun in golden ripe rice fields.",
                "sort_order": 1
            },
            {
                "sentence_vi": "Hình ảnh tà áo dài kết hợp cùng chiếc nón lá đã trở thành nét đẹp đặc trưng của Việt Nam.",
                "sentence_en": "The image of the Ao Dai paired with the conical hat has become an iconic cultural symbol of Vietnam.",
                "sort_order": 2
            }
        ],
        "practice": {
            "prompt": "Dịch câu: 'Những người phụ nữ làng Chuông đã gìn giữ nghề làm nón lá truyền thống qua nhiều thế hệ.'",
            "suggested_answer": "The women of Chuong village have preserved the craft of making traditional conical hats for generations.",
            "hint": "Dùng 'the craft of making traditional conical hats' hoặc 'traditional hat-making craft' và 'for generations'."
        }
    }
]

def seed():
    print("Bắt đầu khởi tạo dữ liệu mẫu cho VietTrans...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Nạp Danh mục (Categories)
        category_map = {}
        for cat_data in CATEGORIES_DATA:
            existing = db.query(Category).filter(Category.slug == cat_data["slug"]).first()
            if not existing:
                cat = Category(**cat_data)
                db.add(cat)
                db.flush()
                category_map[cat.slug] = cat.id
                print(f" [+] Đã tạo nhóm văn hóa: {cat.name_vi} ({cat.slug})")
            else:
                category_map[existing.slug] = existing.id
                print(f" [~] Nhóm văn hóa đã tồn tại: {existing.name_vi}")

        # 2. Nạp Thẻ mẫu (Cards)
        for c_data in CARDS_DATA:
            cat_id = category_map.get(c_data["category_slug"])
            if not cat_id:
                print(f" [!] Không tìm thấy category cho thẻ {c_data['term_vi']}")
                continue

            existing_card = db.query(Card).filter(Card.slug == c_data["slug"]).first()
            if existing_card:
                print(f" [~] Thẻ đã tồn tại: {existing_card.term_vi} ({existing_card.slug})")
                continue

            card = Card(
                slug=c_data["slug"],
                term_vi=c_data["term_vi"],
                category_id=cat_id,
                category_label=c_data["category_label"],
                tagline_en=c_data["tagline_en"],
                suggested_translation=c_data["suggested_translation"],
                meaning=c_data["meaning"],
                cultural_note=c_data["cultural_note"],
                translation_strategy=c_data["translation_strategy"],
                common_mistake=c_data.get("common_mistake"),
                translation_tip=c_data.get("translation_tip"),
                status=c_data.get("status", "published"),
                reviewed=c_data.get("reviewed", False),
                scan_count=0
            )
            db.add(card)
            db.flush()

            # Thêm ví dụ
            for ex in c_data.get("examples", []):
                card_ex = CardExample(
                    card_id=card.id,
                    sentence_vi=ex["sentence_vi"],
                    sentence_en=ex["sentence_en"],
                    sort_order=ex.get("sort_order", 0)
                )
                db.add(card_ex)

            # Thêm bài tập luyện tập mini
            if "practice" in c_data and c_data["practice"]:
                pr = c_data["practice"]
                practice_item = PracticeItem(
                    card_id=card.id,
                    prompt=pr["prompt"],
                    suggested_answer=pr["suggested_answer"],
                    hint=pr.get("hint")
                )
                db.add(practice_item)

            rev_status = "ĐÃ DUYỆT" if card.reviewed else "CHỜ DUYỆT"
            print(f" [+] Đã tạo thẻ: {card.term_vi} [{rev_status}]")

        db.commit()
        print("\nHoàn tất nạp dữ liệu mẫu thành công!")

    except Exception as e:
        db.rollback()
        print(f" [ERROR] Lỗi nạp dữ liệu: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed()
