# VAI TRÒ
Bạn là senior full-stack developer (Python) kiêm UI/UX designer. Hãy xây dựng website "VietTrans" từ đầu cho tôi. Tôi là giảng viên đại học, có kiến thức chuyên môn về dịch thuật nhưng là người mới với vibe coding, nên hãy giải thích ngắn gọn bằng tiếng Việt các quyết định kỹ thuật quan trọng.

# 1. TỔNG QUAN DỰ ÁN
VietTrans là hệ thống "Bộ thẻ QR hỗ trợ biên dịch các yếu tố văn hóa Việt Nam sang tiếng Anh".
- Slogan: "Lan tỏa văn hóa Việt qua ngôn ngữ Anh".
- Đối tượng: sinh viên ngành Ngôn ngữ Anh (chính), giảng viên (có "Hướng dẫn sử dụng – Teacher's Guide").
- Ý tưởng chính:
  1. Hỗ trợ sinh viên dịch các yếu tố văn hóa Việt Nam sang tiếng Anh.
  2. Kết hợp thẻ học trực quan với QR code để truy cập nội dung chi tiết.
  3. Mỗi thẻ cung cấp: cách dịch, giải thích văn hóa, chiến lược dịch, ví dụ, lỗi thường gặp và bài luyện tập.
  4. Hỗ trợ học biên dịch nhanh, dễ nhớ, có tính ứng dụng thực tế.
- Luồng sử dụng cốt lõi: sinh viên cầm thẻ vật lý (6 cm x 9 cm) -> quét QR bằng điện thoại -> mở trang chi tiết thẻ trên web (tối ưu mobile). Vì vậy giao diện mobile là ưu tiên số 1 (mobile-first).
- Domain dự kiến: viettrans.edu.vn (dùng biến cấu hình BASE_URL, không hard-code).

# 2. CÔNG NGHỆ BẮT BUỘC
- Backend: Python 3.11+, FastAPI, SQLAlchemy 2.x, Pydantic, Jinja2 (render HTML phía server), Uvicorn.
- Database: SQLite (file viettrans.db), thiết kế để dễ chuyển sang PostgreSQL (dùng biến môi trường DATABASE_URL). Dùng Alembic cho migration.
- Frontend: HTML5 + CSS3 + JavaScript thuần (ES6+). KHÔNG dùng framework JS, KHÔNG cần bước build. CSS dùng CSS variables, Flexbox/Grid.
- QR: thư viện `qrcode[pil]`, sinh QR PNG và SVG cho mỗi thẻ.
- PDF in thẻ: dùng `reportlab` hoặc `weasyprint` (chọn cái cài đặt dễ nhất trên Windows/Mac và nói rõ lý do).
- Quản lý cấu hình: file .env (python-dotenv), có .env.example. Tuyệt đối không commit secret.
- Cấu trúc thư mục rõ ràng:
  app/ (main.py, config.py, database.py, models/, schemas/, routers/, services/, templates/, static/{css,js,img,audio,qr}), scripts/ (seed.py), tests/, requirements.txt, README.md, .gitignore, .env.example

# 3. THIẾT KẾ GIAO DIỆN (bám sát ảnh demo)
Phong cách: ấm áp, văn hóa Việt, tinh tế, hiện đại; cảm hứng hoa sen, Tết, kiến trúc truyền thống (Hồ Gươm, tháp Rùa), họa tiết hoa văn nhẹ ở góc.
- Bảng màu (đặt thành CSS variables):
  - Xanh lá đậm (chủ đạo, tiêu đề, nút): ~#1F5C3A
  - Kem/be nền: ~#FFF8EC
  - Cam/san hô (nhấn, nút CTA): ~#F28C5B
  - Đỏ Tết (tiêu đề thẻ như "LÌ XÌ"): ~#D63B2F
  - Hồng sen: ~#F4A6B8
  - Chữ chính: ~#2B2B2B
  Hãy tinh chỉnh cho hài hòa và đạt độ tương phản WCAG AA.
- Font: heading dùng font serif đậm, sang (ví dụ "Playfair Display" hoặc "Be Vietnam Pro"/"Lora"), body dùng sans-serif dễ đọc ("Be Vietnam Pro" hoặc "Inter"). BẮT BUỘC hỗ trợ đầy đủ dấu tiếng Việt (subset vietnamese).
- Logo: biểu tượng hoa sen cách điệu (vẽ bằng SVG, màu cam-hồng) + chữ "VietTrans" xanh đậm. Tạo logo SVG inline, không dùng ảnh bản quyền.
- Hình minh họa: dùng SVG/CSS tự tạo hoặc placeholder đẹp; đánh dấu rõ chỗ tôi sẽ thay bằng ảnh thật. Không tải ảnh có bản quyền.
- Responsive đầy đủ (360px -> 1440px), dark mode tùy chọn (giữ tông ấm), animation nhẹ (fade/slide khi cuộn, tôn trọng prefers-reduced-motion).

# 4. CÁC TRANG VÀ TÍNH NĂNG

## 4.1. Trang chủ (/)
Gồm các section theo thứ tự:
1. Hero: logo, tiêu đề "VietTrans", phụ đề "Bộ thẻ QR hỗ trợ biên dịch các yếu tố văn hóa Việt Nam sang tiếng Anh", câu "Lan tỏa văn hóa Việt qua ngôn ngữ Anh", nút "Khám phá bộ thẻ" và "Quét thử một thẻ".
2. "Ý tưởng chính": 4 khối icon + mô tả (đúng 4 ý ở mục 1).
3. "Mẫu thẻ VietTrans": hiển thị mặt trước và mặt sau thẻ (tỉ lệ 6:9). Mặt trước: logo nhỏ, từ tiếng Việt lớn (vd "LÌ XÌ"), nhóm văn hóa trong ngoặc "(Tết – Lễ hội)", hình minh họa, QR + nút "Scan me". Mặt sau: logo, câu "Small tradition, Big meaning" (mỗi thẻ có tagline tiếng Anh riêng), chú thích "Vietnamese Culture in Translation". Cho phép bấm để lật thẻ (CSS 3D flip).
4. "Cấu trúc nội dung mỗi thẻ QR": liệt kê 10 mục có đánh số, nhãn tiếng Anh + giải thích tiếng Việt:
   1 Vietnamese term (Từ/cụm từ tiếng Việt) · 2 Suggested translation (Gợi ý cách dịch tiếng Anh) · 3 Meaning (Giải thích nghĩa) · 4 Cultural note (Thông tin văn hóa liên quan) · 5 Translation strategy (Chiến lược dịch phù hợp) · 6 Example (Ví dụ trong ngữ cảnh) · 7 Common mistake (Lỗi dịch thường gặp) · 8 Translation tip (Lưu ý khi dịch) · 9 Mini practice (Bài luyện tập ngắn) · 10 Audio (Phát âm nếu cần)
5. "Một số thẻ mẫu": carousel/lưới thẻ: Áo dài (Trang phục), Bánh chưng (Ẩm thực), Cúng giao thừa (Tín ngưỡng), Nón lá (Trang phục), Lì xì (Tết – Lễ hội).
6. "Các nhóm yếu tố văn hóa (dự kiến)": 5 nhóm, bấm vào để sang trang thư viện đã lọc:
   - Tết và lễ hội (8–10 thẻ)
   - Ẩm thực (6–8 thẻ)
   - Trang phục và nghệ thuật (6–8 thẻ)
   - Gia đình, tín ngưỡng (6–8 thẻ)
   - Đời sống và phong tục (6–8 thẻ)
7. "Bộ sản phẩm VietTrans": giới thiệu hộp thẻ "Vietnamese Culture in Translation", sách "Hướng dẫn sử dụng (Teacher's Guide)", ứng dụng/web trên điện thoại, bộ thẻ. Dùng mockup CSS/SVG đơn giản + nút liên hệ/đặt mua (chỉ giao diện, form liên hệ lưu vào DB).
8. Footer: liên hệ, liên kết, bản quyền.

## 4.2. Thư viện thẻ (/cards)
- Lưới thẻ dạng card đẹp, lọc theo nhóm văn hóa, tìm kiếm theo từ tiếng Việt/tiếng Anh (hỗ trợ tìm KHÔNG DẤU, ví dụ gõ "li xi" vẫn ra "Lì xì"), phân trang hoặc "tải thêm".
- Tìm kiếm tức thời bằng JavaScript (fetch API /api/cards?q=&category=) với debounce.

## 4.3. Trang chi tiết thẻ (/card/{slug}) - ĐÂY LÀ TRANG QUÉT QR, ƯU TIÊN SỐ 1
Thiết kế như khung điện thoại trong ảnh demo, mobile-first, tải nhanh (< 2 giây trên 4G):
- Thanh trên: logo VietTrans + menu.
- Tiêu đề từ tiếng Việt lớn màu đỏ (vd "LÌ XÌ"), nhóm văn hóa nhỏ bên dưới, nút phát âm hình loa ở bên phải.
- Ảnh banner minh họa.
- Các khối thông tin xếp dọc, mỗi khối có icon + màu nền nhạt riêng, đúng thứ tự:
  1. Suggested translation (vd "lucky money / giving lucky money")
  2. Meaning
  3. Cultural note
  4. Translation strategy
  5. Example (có thể nhiều ví dụ, mỗi ví dụ gồm câu Việt + câu Anh)
  6. Common mistake (nhãn đỏ, ví dụ "give money for luck (too literal)")
  7. Translation tip (nhãn xanh, có dấu tick)
  8. Mini practice: câu cần dịch + nút "Xem gợi ý đáp án" (JS toggle) + ô nhập để sinh viên tự thử dịch và so sánh với đáp án gợi ý (chỉ xử lý phía client, chưa chấm điểm).
- Nút chia sẻ, nút "Thẻ liên quan" (cùng nhóm), nút điều hướng thẻ trước/sau.
- Nút phát audio: ưu tiên file mp3 của thẻ; nếu chưa có thì dùng Web Speech API (speechSynthesis) phát âm tiếng Việt và tiếng Anh.
- Ghi nhận lượt quét: route /c/{slug} (URL ngắn dùng trong QR) -> tăng bộ đếm scan_count (ẩn danh, không lưu thông tin cá nhân) -> redirect 302 sang /card/{slug}.

## 4.4. Trang quản trị (/admin) - dành cho giảng viên
- Đăng nhập đơn giản an toàn (một tài khoản admin, mật khẩu băm bằng bcrypt/argon2, session cookie HttpOnly, CSRF protection, giới hạn đăng nhập sai). Thông tin tài khoản lấy từ .env.
- CRUD thẻ: form nhập đủ các trường (xem mục 5), upload ảnh minh họa và audio (kiểm tra loại file, giới hạn dung lượng), xem trước trang chi tiết trước khi xuất bản, trạng thái Nháp/Đã xuất bản.
- Tự động sinh QR (PNG + SVG) cho mỗi thẻ khi lưu; QR trỏ tới {BASE_URL}/c/{slug}; có nút tải về.
- Xuất PDF để in: khổ thẻ 6 cm x 9 cm, có mặt trước (từ khóa, nhóm, hình, QR, "Scan me") và mặt sau (logo + tagline), có chọn xuất 1 thẻ hoặc cả bộ, bản in A4 xếp nhiều thẻ có vạch cắt (crop marks) và lề an toàn.
- Xem thống kê: số lượt quét theo thẻ, thẻ được xem nhiều nhất.
- Nhập/xuất dữ liệu thẻ bằng file JSON hoặc CSV.
- Xem các tin nhắn từ form liên hệ.

# 5. MÔ HÌNH DỮ LIỆU
Bảng Category: id, slug, name_vi, name_en, description, icon, expected_cards_min, expected_cards_max, sort_order.
Bảng Card: id, slug (unique, không dấu), term_vi, category_id, category_label (vd "Tết – Lễ hội"), tagline_en (vd "Small tradition, Big meaning"), suggested_translation, meaning, cultural_note, translation_strategy, common_mistake, translation_tip, image_path, audio_path, status (draft/published), scan_count, created_at, updated_at, reviewed (bool, đã được giảng viên duyệt nội dung).
Bảng CardExample: id, card_id, sentence_vi, sentence_en, sort_order.
Bảng PracticeItem: id, card_id, prompt (câu cần dịch), suggested_answer, hint.
Bảng ContactMessage: id, name, email, message, created_at.
Nhãn hiển thị song ngữ (tiếng Anh + giải thích tiếng Việt) được đặt trong file cấu hình/ngôn ngữ riêng để dễ sửa.

# 6. API (FastAPI, có tài liệu tự sinh tại /docs)
GET /api/categories · GET /api/cards (q, category, page, limit) · GET /api/cards/{slug} · GET /api/cards/{slug}/qr?format=png|svg · POST /api/contact · các endpoint /api/admin/* (yêu cầu đăng nhập) cho CRUD, upload, xuất PDF, thống kê. Dùng Pydantic để validate, trả lỗi rõ ràng, có rate limiting cho endpoint công khai (đặc biệt /api/contact).

# 7. DỮ LIỆU MẪU (scripts/seed.py)
Tạo 5 nhóm văn hóa ở trên và 5 thẻ mẫu: Lì xì, Áo dài, Bánh chưng, Cúng giao thừa, Nón lá.
Thẻ LÌ XÌ (nhóm "Tết – Lễ hội") dùng đúng nội dung sau:
- Suggested translation: "lucky money / giving lucky money"
- Meaning: Tiền được tặng trong phong bì đỏ, đặc biệt cho trẻ em và các thành viên trẻ trong gia đình vào dịp Tết Nguyên đán, kèm lời chúc sức khỏe, may mắn và thịnh vượng.
- Cultural note: Lì xì là một tập tục truyền thống của Việt Nam, phản ánh các giá trị về sự hào phóng, gắn kết gia đình và cầu may đầu năm.
- Translation strategy: Mô tả tập tục và ý nghĩa văn hóa của nó, tránh dịch từng chữ (literal translation).
- Example: "Children are given lucky money at Tết." / "Li xi symbolizes good wishes for a prosperous new year."
- Common mistake: "give money for luck" (dịch quá sát nghĩa đen).
- Translation tip: Dùng các thuật ngữ tự nhiên và phổ biến: "lucky money", "give lucky money".
- Mini practice: Dịch câu "Ông bà thường lì xì cho cháu vào sáng mùng Một."
- Tagline: "Small tradition, Big meaning"
Với 4 thẻ còn lại, hãy soạn đủ 10 trường nội dung chuẩn xác về học thuật, đặt reviewed=false và hiển thị ghi chú "Nội dung đang chờ giảng viên duyệt" trong admin để tôi kiểm tra lại trước khi xuất bản. Không bịa số liệu lịch sử cụ thể nếu không chắc.

# 8. YÊU CẦU CHẤT LƯỢNG
- Hiệu năng: ảnh nén/lazy-load, CSS/JS gọn, cache header cho static, điểm Lighthouse mục tiêu > 90 (Performance, Accessibility, SEO) trên trang chi tiết thẻ.
- Accessibility: HTML ngữ nghĩa, alt cho ảnh, điều hướng bàn phím, aria-label cho nút audio, tương phản màu đạt chuẩn.
- SEO: title/meta description riêng cho mỗi trang, Open Graph, sitemap.xml, robots.txt, thuộc tính lang="vi".
- Bảo mật: validate input, escape output (chống XSS), chống SQL injection (dùng ORM), kiểm tra file upload, CORS chặt, header bảo mật cơ bản, không lộ secret.
- Kiểm thử: pytest cho API chính (danh sách thẻ, chi tiết thẻ, tìm kiếm không dấu, redirect /c/{slug}, sinh QR).
- Code sạch, có comment tiếng Việt ở các đoạn quan trọng, type hints đầy đủ.
- README.md bằng tiếng Việt: cách cài đặt, chạy local, seed dữ liệu, thêm thẻ mới, in thẻ, deploy.

# 9. CÁCH LÀM VIỆC (BẮT BUỘC TUÂN THỦ)
1. TRƯỚC KHI viết code: đưa ra kế hoạch gồm cấu trúc thư mục, mô hình dữ liệu, danh sách trang/route, các giai đoạn. Chờ tôi xác nhận.
2. Sau khi tôi đồng ý, làm tuần tự, mỗi giai đoạn xong phải chạy thử và báo cáo:
   - Giai đoạn 1: khởi tạo dự án, cấu hình, database, model, seed dữ liệu.
   - Giai đoạn 2: API + trang chi tiết thẻ (/card/{slug}) và /c/{slug} + sinh QR (đây là phần cốt lõi, làm trước).
   - Giai đoạn 3: trang chủ và thư viện thẻ, tìm kiếm.
   - Giai đoạn 4: trang admin (đăng nhập, CRUD, upload, thống kê).
   - Giai đoạn 5: xuất PDF thẻ in 6x9 cm, import/export.
   - Giai đoạn 6: responsive, dark mode, animation, SEO, accessibility, tối ưu hiệu năng.
   - Giai đoạn 7: kiểm thử, README, hướng dẫn đẩy lên GitHub và deploy (đề xuất Render/Railway/VPS + tên miền, HTTPS).
3. Sau mỗi giai đoạn: dùng trình duyệt tích hợp để kiểm tra giao diện (cả khung mobile 390px và desktop), chụp ảnh kết quả, nêu rõ lệnh chạy và đường dẫn để tôi xem; gợi ý nội dung commit git.
4. Khi gặp điểm chưa rõ, hãy hỏi tôi tối đa vài câu ngắn thay vì tự đoán những thứ ảnh hưởng lớn.
5. Không làm thêm tính năng ngoài danh sách trên khi chưa hỏi tôi.

Hãy bắt đầu bằng bản kế hoạch (bước 1).