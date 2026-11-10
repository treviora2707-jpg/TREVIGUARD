"""
TREVIORA AI DEFENDER - AI Malware Detection Engine
Modular AI detection system analyzing PE header anomalies, entropy, API imports,
and behavioral indicators.
Includes Explainable AI (XAI) feature breakdown.
Notice: Never claims AI detection is 100% accurate.
"""
import os
from pathlib import Path
from treviora_defender.core.ml_model import MLMalwareModel
from treviora_defender.core.signature_verifier import SignatureVerifier
from treviora_defender.utils.pe_extractor import extract_pe_features
from treviora_defender.config.constants import (
    RISK_THRESHOLD_SAFE, RISK_THRESHOLD_SUSPICIOUS, RISK_THRESHOLD_MALICIOUS,
    SEVERITY_CLEAN, SEVERITY_LOW, SEVERITY_MEDIUM, SEVERITY_HIGH, SEVERITY_CRITICAL
)
from treviora_defender.utils.logger import get_logger

logger = get_logger()


class AIEngine:
    def __init__(self):
        self.ml_model = MLMalwareModel()
        self.sig_verifier = SignatureVerifier()

    def analyze_file(self, file_path: str) -> dict:
        """
        Performs AI evaluation of a file.
        Returns:
            {
                "risk_score": float (0-100),
                "classification": "Safe" | "Suspicious" | "Malicious",
                "severity": "Clean" | "Low" | "Medium" | "High" | "Critical",
                "is_threat": bool,
                "reasons": list of str,
                "ai_summary": str,
                "model_engine": str,
                "disclaimer": str
            }
        """
        disclaimer = "AI detection is probabilistic and assists human analysts; it is never claimed to be 100% accurate."
        
        if not os.path.exists(file_path):
            return {
                "risk_score": 0.0,
                "classification": "Safe",
                "severity": SEVERITY_CLEAN,
                "is_threat": False,
                "reasons": ["File not found"],
                "ai_summary": "Clean (No file accessible).",
                "model_engine": self.ml_model.model_type,
                "disclaimer": disclaimer
            }

        reasons = []

        # 1. Digital Signature Check
        sig_info = self.sig_verifier.verify(file_path)
        is_signed = 1 if sig_info.get("signed", False) else 0
        if is_signed:
            reasons.append("Verified Authenticode digital signature from trusted authority.")
        else:
            if "Tampered" in sig_info.get("status", ""):
                reasons.append("CRITICAL: Invalid or tampered digital signature detected!")
            else:
                reasons.append("File is unsigned (no valid vendor digital signature).")

        # 2. Extract PE Features
        pe_feats = extract_pe_features(file_path)

        if not pe_feats["is_pe"]:
            # Non-PE file analysis (scripts, text, docs)
            overall_ent = pe_feats.get("overall_entropy", 0.0)
            if overall_ent > 7.5:
                risk = 45.0
                reasons.append(f"Unusually high file entropy ({overall_ent}/8.0), possible obfuscation or payload.")
                cls_name = "Suspicious"
                sev = SEVERITY_MEDIUM
            else:
                risk = 5.0
                reasons.append("Standard data file or document with normal entropy.")
                cls_name = "Safe"
                sev = SEVERITY_CLEAN

            return {
                "risk_score": risk,
                "classification": cls_name,
                "severity": sev,
                "is_threat": (risk >= RISK_THRESHOLD_SUSPICIOUS),
                "reasons": reasons,
                "ai_summary": f"Classified as {cls_name} (Risk: {risk:.1f}%).",
                "model_engine": "Heuristic Entropy",
                "disclaimer": disclaimer
            }

        # 3. Build Feature Vector for ML Model
        # [overall_entropy, max_sec_entropy, num_sections, has_wx_sections,
        #  has_packed_names, inj_apis, crypto_apis, spy_apis, evasion_apis, net_apis, is_signed]
        apis = pe_feats["suspicious_apis_found"]
        inj_count = len(apis.get("Process Injection", []))
        crypto_count = len(apis.get("Ransomware / Cryptography", []))
        spy_count = len(apis.get("Keylogging & Spyware", []))
        evasion_count = len(apis.get("Anti-Analysis & Evasion", []))
        net_count = len(apis.get("Network / C2 Communication", []))

        vec = [
            pe_feats["overall_entropy"],
            pe_feats["max_section_entropy"],
            pe_feats["num_sections"],
            1 if pe_feats["has_wx_sections"] else 0,
            1 if pe_feats["has_packed_section_names"] else 0,
            inj_count,
            crypto_count,
            spy_count,
            evasion_count,
            net_count,
            is_signed
        ]

        # 4. Predict Risk using ONNX / scikit-learn
        raw_risk = self.ml_model.predict_risk(vec)

        # 5. Add Explainable AI (XAI) breakdown points
        for ind in pe_feats["anomaly_indicators"]:
            reasons.append(ind)

        if inj_count > 0:
            inj_names = ", ".join(apis["Process Injection"][:3])
            reasons.append(f"Imports {inj_count} process injection API(s): {inj_names}")

        if crypto_count > 0:
            reasons.append(f"Contains cryptographic encryption APIs ({crypto_count} functions)")

        if spy_count > 0:
            reasons.append(f"Contains input monitoring/keylogging APIs ({spy_count} functions)")

        if evasion_count > 0:
            reasons.append(f"Imports anti-debugging / evasion detection APIs ({evasion_count} functions)")

        # Classification mapping
        if raw_risk >= RISK_THRESHOLD_MALICIOUS:
            classification = "Malicious"
            severity = SEVERITY_CRITICAL if raw_risk >= 90 else SEVERITY_HIGH
            is_threat = True
        elif raw_risk >= RISK_THRESHOLD_SUSPICIOUS:
            classification = "Suspicious"
            severity = SEVERITY_MEDIUM
            is_threat = True
        else:
            classification = "Safe"
            severity = SEVERITY_CLEAN
            is_threat = False

        summary_text = (
            f"Treviora AI classified as {classification} with {raw_risk:.1f}% risk score. "
            f"Evaluated via {self.ml_model.model_type} model."
        )

        return {
            "risk_score": raw_risk,
            "classification": classification,
            "severity": severity,
            "is_threat": is_threat,
            "reasons": reasons,
            "ai_summary": summary_text,
            "model_engine": self.ml_model.model_type,
            "disclaimer": disclaimer,
            "pe_details": {
                "sections": pe_feats["num_sections"],
                "entropy": pe_feats["overall_entropy"],
                "max_section_entropy": pe_feats["max_section_entropy"],
                "is_signed": bool(is_signed)
            }
        }
