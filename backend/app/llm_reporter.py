import os
import httpx

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")


def generate_investigation_report(transaction_data: dict, risk_score: float, reasons: list) -> str:
    """
    Calls Claude API to generate a natural language fraud investigation report.
    Falls back to a structured template if API key is not set.
    """
    if not ANTHROPIC_API_KEY:
        return _fallback_report(transaction_data, risk_score, reasons)

    prompt = f"""You are a senior fraud analyst at a financial institution. 
Analyze the following flagged transaction and write a concise investigation report (3-4 sentences) 
that a fraud analyst can act on immediately. Be specific about the risk signals and recommend a clear action.

Transaction Details:
- User ID: {transaction_data.get('user_id')}
- Amount: ₹{transaction_data.get('amount'):,.0f}
- Device: {transaction_data.get('device_id')}
- Location: {transaction_data.get('location')}
- New Device: {transaction_data.get('device_new', False)}
- Location Change: {transaction_data.get('location_change', False)}
- Rapid Transactions: {transaction_data.get('rapid_transactions', False)}

Risk Score: {risk_score}/100
Triggered Signals: {', '.join(reasons) if reasons else 'None'}

Write only the investigation report, no preamble."""

    try:
        response = httpx.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 300,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=10.0,
        )
        data = response.json()
        return data["content"][0]["text"].strip()
    except Exception:
        return _fallback_report(transaction_data, risk_score, reasons)


def _fallback_report(transaction_data: dict, risk_score: float, reasons: list) -> str:
    """Template-based fallback when API key is unavailable."""
    action = "Immediate account freeze and manual review recommended." if risk_score >= 80 \
        else "Flag for analyst review within 24 hours."
    signals = ", ".join(reasons) if reasons else "general anomaly pattern"
    return (
        f"Transaction of ₹{transaction_data.get('amount'):,.0f} by User {transaction_data.get('user_id')} "
        f"has been flagged with a risk score of {risk_score}/100. "
        f"Key signals detected: {signals}. "
        f"{action}"
    )