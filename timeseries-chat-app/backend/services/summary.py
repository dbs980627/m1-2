from statistics import mean


def build_summary(rows: list) -> dict:
    """rows: [{'date','value','memo'}] -> 요약 dict"""
    if not rows:
        return {"count": 0, "message": "저장된 데이터가 없습니다."}
    rows = sorted(rows, key=lambda r: r["date"])
    vals = [r["value"] for r in rows]
    hi = max(rows, key=lambda r: r["value"])
    lo = min(rows, key=lambda r: r["value"])
    n = min(7, len(vals) // 2) or 1
    recent, prev = vals[-n:], vals[-2 * n:-n] or vals[:n]
    r_avg, p_avg = mean(recent), mean(prev)
    change = (r_avg - p_avg) / p_avg * 100 if p_avg else 0.0
    trend = "증가" if change > 3 else "감소" if change < -3 else "유지"
    return {
        "count": len(vals),
        "start_date": rows[0]["date"],
        "end_date": rows[-1]["date"],
        "mean": round(mean(vals), 2),
        "max": {"value": hi["value"], "date": hi["date"]},
        "min": {"value": lo["value"], "date": lo["date"]},
        "latest": {"value": rows[-1]["value"], "date": rows[-1]["date"]},
        "trend": trend,
        "trend_change_pct": round(change, 1),
        "trend_basis": f"최근 {n}개 평균 vs 직전 {n}개 평균",
        "recent_points": [{"date": r["date"], "value": r["value"], "memo": r.get("memo", "")} for r in rows[-5:]],
    }


def summary_to_text(s: dict) -> str:
    if s.get("count", 0) == 0:
        return "저장된 데이터가 없습니다."
    pts = ", ".join(f"{p['date']}={p['value']}" for p in s["recent_points"])
    return (
        f"- 기간: {s['start_date']} ~ {s['end_date']} (데이터 {s['count']}개)\n"
        f"- 평균: {s['mean']}, 최대: {s['max']['value']}({s['max']['date']}), 최소: {s['min']['value']}({s['min']['date']})\n"
        f"- 최근값: {s['latest']['value']}({s['latest']['date']})\n"
        f"- 최근 추세: {s['trend']} ({s['trend_change_pct']}%, {s['trend_basis']})\n"
        f"- 최근 5개: {pts}"
    )
