"""
TREVIORA AI DEFENDER - File Signature Verifier
Verifies Microsoft Authenticode digital certificates on PE binaries.
"""
from pathlib import Path
from treviora_defender.utils.win_utils import verify_authenticode_signature
from treviora_defender.utils.logger import get_logger

logger = get_logger()


class SignatureVerifier:
    @staticmethod
    def verify(file_path: str) -> dict:
        """
        Verifies Authenticode signature for a file.
        Returns dict with signed status, trust status, and human-readable explanation.
        """
        res = verify_authenticode_signature(file_path)
        is_signed = res.get("signed", False)
        status = res.get("status", "Unknown")

        if is_signed:
            summary = "Valid digital signature from trusted certificate authority."
            trust_level = "Trusted"
        elif "NotSigned" in status:
            summary = "File is not digitally signed (unsigned binary)."
            trust_level = "Unsigned"
        elif "Untrusted" in status:
            summary = "Digital signature exists but is untrusted, self-signed, or expired."
            trust_level = "Untrusted"
        elif "Tampered" in status or "BadDigest" in status:
            summary = "WARNING: Digital signature hash does not match binary (Possible file tampering!)."
            trust_level = "Tampered"
        else:
            summary = f"Signature status: {status}"
            trust_level = "Unknown"

        return {
            "signed": is_signed,
            "status": status,
            "trust_level": trust_level,
            "summary": summary
        }
