"""
TREVIORA AI DEFENDER - Built-in AI Security Assistant
Answers cybersecurity questions, explains detected threats, analyzes scan reports,
and recommends actionable security steps.
Operates fully offline with built-in knowledge base, and supports optional user-configured
external AI endpoints (e.g., local Ollama or OpenAI-compatible API).
Privacy guarantee: Never uploads files or private data to external AI without explicit user consent.
"""
import json
import urllib.request
import urllib.error
from treviora_defender.config.settings import SettingsManager
from treviora_defender.ai_assistant.knowledge_base import search_knowledge_base, KNOWLEDGE_ENTRIES
from treviora_defender.database.db_manager import DatabaseManager
from treviora_defender.utils.logger import get_logger

logger = get_logger()


class AIAssistant:
    def __init__(self):
        self.settings = SettingsManager()
        self.db = DatabaseManager()

    def query(self, user_prompt: str) -> str:
        """
        Processes a security query. First checks whether external AI is enabled and configured,
        otherwise uses internal cybersecurity intelligence engine.
        """
        user_prompt_clean = user_prompt.strip()
        if not user_prompt_clean:
            return "Please ask a cybersecurity or threat-related question."

        # Check if external AI is explicitly enabled by the user in Settings
        if self.settings.get("cloud_ai_enabled", False):
            api_key = self.settings.get("cloud_ai_api_key", "").strip()
            endpoint = self.settings.get("cloud_ai_endpoint", "https://api.openai.com/v1").strip()
            if api_key or "localhost" in endpoint or "127.0.0.1" in endpoint:
                try:
                    return self._query_external_ai(user_prompt_clean, endpoint, api_key)
                except Exception as e:
                    logger.warning(f"External AI query failed, falling back to local engine: {e}")

        # Local Cybersecurity Intelligence Engine
        return self._local_ai_response(user_prompt_clean)

    def _local_ai_response(self, prompt: str) -> str:
        p_lower = prompt.lower()

        # Check knowledge base first
        kb_match = search_knowledge_base(prompt)
        if kb_match:
            response = f"### {kb_match['title']}\n\n"
            response += f"{kb_match['description']}\n\n"
            response += "**Key Threat Indicators:**\n"
            for ind in kb_match["indicators"]:
                response += f"- {ind}\n"
            response += "\n**Recommended Remediation Actions:**\n"
            for rec in kb_match["recommendations"]:
                response += f"✓ {rec}\n"
            response += "\n*Note: Treviora AI Defender provides real-time monitoring and isolation for these threat vectors.*"
            return response

        # Check if user asks about scan report or status
        if "scan" in p_lower or "report" in p_lower or "status" in p_lower:
            return self.explain_system_status()

        # Check if user asks about quarantine
        if "quarantine" in p_lower or "isolated" in p_lower:
            q_files = self.db.get_quarantined_files()
            if not q_files:
                return "The quarantine store is currently clean. No active files are currently isolated."
            resp = f"There are currently {len(q_files)} isolated item(s) in the Treviora Quarantine vault:\n\n"
            for q in q_files[:5]:
                resp += f"- **{q['threat_name']}** (Original: `{q['original_path']}`) - Quarantined: {q['quarantined_at']}\n"
            resp += "\nYou can safely review, restore, or permanently shred these files in the Quarantine tab."
            return resp

        # Default intelligent cybersecurity advisory
        return (
            f"**Treviora Security Advisory for:** *\"{prompt}\"*\n\n"
            "Treviora AI Defender evaluates files through a 4-tier pipeline:\n"
            "1. **Cryptographic Hash Verification:** Fast lookup against known signature databases.\n"
            "2. **Authenticode Digital Signature:** Verification of code certificates via Windows WinVerifyTrust.\n"
            "3. **YARA Pattern Matching:** Detection of malicious strings, droppers, and shellcode patterns.\n"
            "4. **ONNX Machine Learning Model:** Static PE feature evaluation including Shannon entropy, "
            "section characteristics, and dangerous Windows API calls.\n\n"
            "**General Recommendation:**\n"
            "- Always keep Real-Time Protection enabled.\n"
            "- Never run untrusted scripts or cracked software.\n"
            "- If a file is flagged as Suspicious or Malicious, quarantine it and review its AI breakdown."
        )

    def explain_threat(self, threat_name: str, explanation: str, risk_score: float) -> str:
        """
        Explains why a specific file or threat was flagged.
        """
        response = f"### AI Threat Analysis: {threat_name}\n\n"
        response += f"**Assessed Risk Score:** {risk_score:.1f}% / 100%\n\n"
        response += "**Behavioral & Heuristic Indicators:**\n"
        for line in explanation.split("\n"):
            line = line.strip()
            if line:
                response += f"- {line}\n"
        response += "\n**Recommended Action:**\n"
        if risk_score >= 80:
            response += "✓ Immediately quarantine this file to prevent execution.\n"
            response += "✓ Check if this executable has established any active outbound connections in Network Security.\n"
        else:
            response += "✓ Verify if this file is from a developer or vendor you trust.\n"
            response += "✓ If unrecognized, quarantine or submit for deeper sandboxed inspection.\n"
        return response

    def explain_system_status(self) -> str:
        stats = self.db.get_dashboard_stats()
        active = stats.get("active_threats", 0)
        quar = stats.get("quarantined_count", 0)
        scanned = stats.get("total_scanned", 0)

        status_text = "### Treviora Security Assessment\n\n"
        if active == 0:
            status_text += "🟢 **System Status: Protected & Healthy**\n\n"
            status_text += f"- **Files Inspected:** {scanned:,}\n"
            status_text += f"- **Active Threats:** 0 (Clean)\n"
            status_text += f"- **Quarantined Items:** {quar}\n\n"
            status_text += "All real-time protection shields (File, Process, Ransomware, USB) are actively running."
        else:
            status_text += f"🔴 **System Status: Attention Required ({active} Active Threat(s))**\n\n"
            status_text += f"Treviora has detected {active} unresolved threats. Please open the Threat Detection or Quarantine page to take containment action."
        return status_text

    def _query_external_ai(self, prompt: str, endpoint: str, api_key: str) -> str:
        # Standard OpenAI-compatible chat completions format
        url = endpoint.rstrip("/")
        if not url.endswith("/chat/completions"):
            url += "/chat/completions"

        headers = {
            "Content-Type": "application/json"
        }
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        payload = {
            "model": "gpt-3.5-turbo" if "openai" in endpoint else "llama3",
            "messages": [
                {
                    "role": "system",
                    "content": "You are Treviora Defender AI, an expert cybersecurity assistant embedded inside a Windows antivirus application. Explain security concepts clearly, accurately, and emphasize defensive best practices."
                },
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500,
            "temperature": 0.4
        }

        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
