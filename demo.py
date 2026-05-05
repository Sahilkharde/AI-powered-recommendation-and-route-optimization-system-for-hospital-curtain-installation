"""Demo: test all AI Automation Hospital AI agent endpoints."""

import requests
import sys

BASE = "http://localhost:8000/api/v1"


def scan_curtain(barcode: str):
    print(f"\n{'='*60}")
    print(f"  SCAN CURTAIN: {barcode}")
    print(f"{'='*60}")

    resp = requests.post(f"{BASE}/suggest-location", json={"curtain_barcode": barcode})
    if resp.status_code != 200:
        print(f"  ERROR ({resp.status_code}): {resp.json().get('detail', resp.text)}")
        return

    data = resp.json()
    print(f"  Status   : {data['curtain_status']}")
    print(f"  Category : {data['curtain_category']}")
    print(f"  Hospital : {data['hospital_name']}")
    print(f"  Disposable: {data['is_disposable']}  |  Spare: {data['is_spare']}")
    print(f"  Candidates evaluated: {data['total_candidates']}")
    print(f"\n  >> {data['message']}")
    print(f"\n  Top 3 Recommendations:")
    for rec in data["recommendations"][:3]:
        loc = rec["location"]
        print(f"\n    #{rec['rank']} [Score: {rec['score']}/100]")
        print(f"      Building : {loc['building_name']}")
        print(f"      Floor    : {loc['floor']}")
        print(f"      Unit     : {loc['unit_name']}")
        print(f"      Room     : {loc['room_name']}")
        print(f"      Track    : {loc['track_barcode']}")
        if rec["warnings"]:
            for w in rec["warnings"]:
                print(f"      ! {w}")


def scan_track(barcode: str):
    print(f"\n{'='*60}")
    print(f"  SCAN TRACK: {barcode}")
    print(f"{'='*60}")

    resp = requests.post(f"{BASE}/match-curtains", json={"track_barcode": barcode})
    if resp.status_code != 200:
        print(f"  ERROR ({resp.status_code}): {resp.json().get('detail', resp.text)}")
        return

    data = resp.json()
    print(f"  Track Type : {data['track_type']}  |  Length: {data['track_length']}\"  |  Height: {data['track_height']}\"")
    print(f"  Location   : {data['hospital_name']} > {data['building_name']} > Floor {data['floor']} > {data['room_name']}")
    print(f"  Candidates : {data['total_candidates']}")
    print(f"\n  >> {data['message']}")
    print(f"\n  Top 5 Matching Curtains:")
    for m in data["matches"][:5]:
        best = " <-- BEST MATCH" if m["is_best_match"] else ""
        print(f"    {m['curtain_barcode']} [{m['score']}/100] {m['curtain_type']} {m['width']}\"x{m['height']}\" ({m['status']}){best}")
        if m["warnings"]:
            for w in m["warnings"]:
                print(f"      ! {w}")


def installer_route(installer_id: int):
    print(f"\n{'='*60}")
    print(f"  INSTALLER ROUTE: Installer #{installer_id}")
    print(f"{'='*60}")

    resp = requests.get(f"{BASE}/installer/{installer_id}/route")
    if resp.status_code != 200:
        print(f"  ERROR ({resp.status_code}): {resp.json().get('detail', resp.text)}")
        return

    data = resp.json()
    print(f"  Date      : {data['route_date']}")
    print(f"  Hospitals : {data['total_hospitals']}")
    print(f"  Stops     : {data['total_stops']}")
    print(f"\n  >> {data['message']}")

    for seg in data["segments"]:
        print(f"\n  --- {seg['hospital_name']} ({seg['total_tracks']} tracks) ---")
        for s in seg["stops"][:5]:
            print(f"    Stop #{s['order']}: {s['building_name']} > Floor {s['floor']} > {s['unit_name']} > {s['room_name']} > Track {s['track_barcode']}")


def cache_stats():
    print(f"\n{'='*60}")
    print(f"  CACHE STATS")
    print(f"{'='*60}")
    resp = requests.get(f"{BASE}/cache/stats")
    data = resp.json()
    print(f"  Backend    : {data['backend']}")
    print(f"  Total Keys : {data['total_keys']}")


def health_check():
    print(f"\n{'='*60}")
    print(f"  HEALTH CHECK")
    print(f"{'='*60}")
    resp = requests.get(f"{BASE}/health")
    data = resp.json()
    print(f"  Status   : {data['status']}")
    print(f"  Version  : {data['version']}")
    print(f"  DB OK    : {data['db_ok']}")
    print(f"  Cache OK : {data['cache_ok']}")


def list_curtains():
    """Peek at the seeded curtain barcodes so we know what to scan."""
    import sqlite3, os
    db_path = os.path.join(os.path.dirname(__file__), "ai_automation_hospital_ai.db")
    if not os.path.exists(db_path):
        print("  [No local DB yet]")
        return [], [], []

    conn = sqlite3.connect(db_path)
    regular = conn.execute(
        "SELECT CurtBarCode FROM Hosp_Curtains WHERE HID NOT IN (99,1001) LIMIT 3"
    ).fetchall()
    spare = conn.execute(
        "SELECT CurtBarCode FROM Hosp_Curtains WHERE HID=1001 LIMIT 1"
    ).fetchall()
    disposable = conn.execute(
        "SELECT CurtBarCode FROM Hosp_Curtains WHERE HID=99 LIMIT 1"
    ).fetchall()
    tracks = conn.execute(
        "SELECT TrackBarCode FROM Hosp_Track LIMIT 1"
    ).fetchall()
    conn.close()
    return (
        [str(r[0]) for r in regular],
        [str(r[0]) for r in spare],
        [str(r[0]) for r in disposable],
        [r[0] for r in tracks],
    )


if __name__ == "__main__":
    regular, spare, disposable, tracks = list_curtains()

    health_check()

    if regular:
        for bc in regular:
            scan_curtain(bc)
    if disposable:
        scan_curtain(disposable[0])
    if spare:
        scan_curtain(spare[0])
    if tracks:
        scan_track(tracks[0])

    installer_route(1)

    cache_stats()

    print()
