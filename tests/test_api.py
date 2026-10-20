import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models.card import Card

client = TestClient(app)

def test_get_categories():
    response = client.get("/api/categories")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 5
    slugs = [c["slug"] for c in data]
    assert "tet-le-hoi" in slugs
    assert "am-thuc" in slugs

def test_get_cards_list():
    response = client.get("/api/cards")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 5
    assert len(data["items"]) >= 5

def test_unaccented_search():
    # Tìm kiếm không dấu 'li xi' phải tìm ra 'Lì xì'
    response = client.get("/api/cards?q=li xi")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    terms = [item["term_vi"] for item in data["items"]]
    assert "Lì xì" in terms

    # Tìm kiếm 'ao dai' phải tìm ra 'Áo dài'
    response_ao = client.get("/api/cards?q=ao dai")
    assert response_ao.status_code == 200
    assert response_ao.json()["total"] >= 1
    assert "Áo dài" in [item["term_vi"] for item in response_ao.json()["items"]]

def test_get_card_detail_api():
    response = client.get("/api/cards/li-xi")
    assert response.status_code == 200
    card = response.json()
    assert card["slug"] == "li-xi"
    assert card["term_vi"] == "Lì xì"
    assert "lucky money" in card["suggested_translation"]
    assert len(card["examples"]) >= 2
    assert len(card["practice_items"]) >= 1

def test_get_qr_png_and_svg():
    # Kiểm tra QR dạng PNG
    res_png = client.get("/api/cards/li-xi/qr?format=png")
    assert res_png.status_code == 200
    assert res_png.headers["content-type"] == "image/png"
    assert len(res_png.content) > 100

    # Kiểm tra QR dạng SVG
    res_svg = client.get("/api/cards/li-xi/qr?format=svg")
    assert res_svg.status_code == 200
    assert "image/svg+xml" in res_svg.headers["content-type"]
    assert "<svg" in res_svg.text

def test_qr_redirect_and_scan_count():
    db = SessionLocal()
    card_before = db.query(Card).filter(Card.slug == "li-xi").first()
    count_before = card_before.scan_count or 0
    db.close()

    # Quét route ngắn /c/li-xi (không tự follow redirect để kiểm tra mã 302)
    response = client.get("/c/li-xi", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "/card/li-xi"

    # Kiểm tra bộ đếm đã tăng đúng 1
    db = SessionLocal()
    card_after = db.query(Card).filter(Card.slug == "li-xi").first()
    assert card_after.scan_count == count_before + 1
    db.close()

def test_card_detail_html_page():
    response = client.get("/card/li-xi")
    assert response.status_code == 200
    html = response.text
    # Kiểm tra hiển thị tiêu đề và các khối thông tin
    assert "LÌ XÌ" in html or "Lì xì" in html
    assert "lucky money / giving lucky money" in html
    assert "Small tradition, Big meaning" in html
    assert "audio-play-btn" in html
    assert "practice-toggle-btn" in html
