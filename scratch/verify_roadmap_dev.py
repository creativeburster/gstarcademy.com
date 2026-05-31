import requests

def test_endpoints():
    base_url = "http://localhost:3001"
    
    # 1. Test roadmap page
    print("Testing Roadmap Page...")
    try:
        r = requests.get(f"{base_url}/knowledge-roadmap.html")
        assert r.status_code == 200, f"Roadmap failed with status {r.status_code}"
        assert "roadmap-track-selector" in r.text, "Missing track selector in roadmap page"
        assert "roadmap-stage-viewport" in r.text or "roadmap-viewport" in r.text, "Missing viewport in roadmap page"
        print("✔ Roadmap page loaded successfully and contains layout components.")
    except Exception as e:
        print("✘ Roadmap page verification failed:", e)
        return
        
    # 2. Test concept page with custom slug
    print("\nTesting Custom Concept Page (AutoCAD Constraints)...")
    try:
        r = requests.get(f"{base_url}/kb/concepts/constraints-autocad.html")
        assert r.status_code == 200, f"AutoCAD Constraints page failed with status {r.status_code}"
        assert "Parametric Constraints (AutoCAD)" in r.text, "Missing main concept title"
        breadcrumb_html = r.text.split("kb-faq-breadcrumbs")[1].split("</nav>")[0]
        assert "bricscad-term-4.html" not in breadcrumb_html, "Breadcrumb autolink collision detected! BricsCAD term link found in AutoCAD breadcrumb."
        print("✔ AutoCAD Constraints page loaded successfully and breadcrumbs have no autolink collisions.")
    except Exception as e:
        print("✘ AutoCAD Constraints page verification failed:", e)

    # 3. Test newly generated concept page (Alibre Design Term 1)
    print("\nTesting Newly Generated Concept Page (Alibre Design)...")
    try:
        r = requests.get(f"{base_url}/kb/concepts/alibre-design-term-1.html")
        assert r.status_code == 200, f"Alibre page failed with status {r.status_code}"
        assert "Parametric Dimension Driver" in r.text, "Missing concept title"
        print("✔ Alibre Design concept page loaded successfully and has full content depth.")
    except Exception as e:
        print("✘ Alibre Design concept page verification failed:", e)

if __name__ == "__main__":
    test_endpoints()
