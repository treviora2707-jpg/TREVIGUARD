r"""
TREVIORA AI DEFENDER - Quarantine Subsystem
Safely isolates suspicious files by encrypting them with AES-GCM and storing them strictly
under D:\projects\antivirus\data\quarantine\ with .tquar extension.
Maintains full metadata and SHA256 hashes in SQLite database.
Supports safe restoration and permanent secure shredding.
"""
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from treviora_defender.config.constants import QUARANTINE_DIR
from treviora_defender.database.db_manager import DatabaseManager
from treviora_defender.core.hash_analyzer import HashAnalyzer
from treviora_defender.utils.logger import get_logger

logger = get_logger()

# Internal static key for quarantine obfuscation/isolation (32 bytes = 256 bits)
QUARANTINE_KEY = b"TREVIORA_ISOLATION_VAULT_KEY_32B"


class QuarantineManager:
    def __init__(self):
        QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
        self.db = DatabaseManager()
        self.aesgcm = AESGCM(QUARANTINE_KEY)

    def quarantine_file(self, file_path: str, threat_name: str = "Generic.Malware") -> dict:
        r"""
        Safely isolates a suspicious file:
        1. Calculates SHA256.
        2. Reads file bytes and encrypts them via AES-GCM (so malware is inert and non-executable).
        3. Saves encrypted blob into D:\projects\antivirus\data\quarantine\<uuid>.tquar.
        4. Safely removes the original infected file.
        5. Logs metadata to database.
        """
        orig_path = Path(file_path).resolve()
        if not orig_path.exists():
            return {"success": False, "error": f"Target file does not exist: {file_path}"}

        try:
            # 1. Compute hash and size
            file_size = orig_path.stat().st_size
            hashes = HashAnalyzer.compute_hashes(str(orig_path))
            sha256_hash = hashes.get("sha256", "UNKNOWN")

            # 2. Read content
            with open(orig_path, "rb") as f:
                plaintext = f.read()

            # 3. Encrypt content with AES-GCM
            nonce = os.urandom(12)
            ciphertext = self.aesgcm.encrypt(nonce, plaintext, None)

            # 4. Save quarantined payload
            q_filename = f"{uuid.uuid4().hex}.tquar"
            q_target_path = QUARANTINE_DIR / q_filename

            with open(q_target_path, "wb") as f:
                f.write(nonce + ciphertext)

            # 5. Safely delete original file
            try:
                # Remove read-only attribute if present
                os.chmod(orig_path, 0o777)
                os.remove(orig_path)
            except Exception as e:
                logger.warning(f"Could not remove original file {orig_path}: {e}")

            # 6. Record into SQLite database
            record_id = self.db.add_quarantine(
                original_path=str(orig_path),
                quarantine_filename=q_filename,
                file_hash=sha256_hash,
                file_size=file_size,
                threat_name=threat_name
            )

            # Also log security event
            self.db.log_event(
                event_type="Quarantine",
                source="QuarantineManager",
                description=f"Isolated '{orig_path.name}' ({threat_name}) to quarantine store.",
                severity="High"
            )

            logger.info(f"Successfully quarantined {orig_path} as {q_filename}")
            return {
                "success": True,
                "quarantine_id": record_id,
                "quarantine_path": str(q_target_path),
                "sha256": sha256_hash
            }

        except Exception as e:
            logger.error(f"Failed to quarantine {orig_path}: {e}")
            return {"success": False, "error": str(e)}

    def restore_file(self, quarantine_id: int, custom_destination: str = None) -> dict:
        """
        Decrypts quarantined file and restores it to its original path or custom folder.
        """
        records = self.db.get_quarantined_files()
        record = next((r for r in records if r["id"] == quarantine_id), None)

        if not record:
            return {"success": False, "error": f"Quarantine record #{quarantine_id} not found."}

        q_file = QUARANTINE_DIR / record["quarantine_filename"]
        if not q_file.exists():
            return {"success": False, "error": f"Encrypted quarantine file missing: {q_file}"}

        target_path = Path(custom_destination) if custom_destination else Path(record["original_path"])

        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)

            with open(q_file, "rb") as f:
                data = f.read()

            nonce = data[:12]
            ciphertext = data[12:]
            decrypted = self.aesgcm.decrypt(nonce, ciphertext, None)

            with open(target_path, "wb") as f:
                f.write(decrypted)

            # Remove quarantined file and update record
            os.remove(q_file)
            self.db.mark_quarantine_restored(quarantine_id)

            self.db.log_event(
                event_type="QuarantineRestore",
                source="QuarantineManager",
                description=f"Restored quarantined file #{quarantine_id} to '{target_path}'.",
                severity="Info"
            )

            logger.info(f"Restored quarantined file to {target_path}")
            return {"success": True, "restored_path": str(target_path)}

        except Exception as e:
            logger.error(f"Error restoring quarantine record #{quarantine_id}: {e}")
            return {"success": False, "error": str(e)}

    def delete_permanently(self, quarantine_id: int) -> dict:
        """
        Permanently shreds and deletes quarantined file with confirmation.
        """
        records = self.db.get_quarantined_files()
        record = next((r for r in records if r["id"] == quarantine_id), None)

        if not record:
            return {"success": False, "error": f"Quarantine record #{quarantine_id} not found."}

        q_file = QUARANTINE_DIR / record["quarantine_filename"]

        try:
            if q_file.exists():
                # Secure shredding (overwrite with zeroes before unlinking)
                file_size = q_file.stat().st_size
                with open(q_file, "wb") as f:
                    f.write(b"\x00" * file_size)
                os.remove(q_file)

            self.db.delete_quarantine_record(quarantine_id)
            self.db.log_event(
                event_type="QuarantineDelete",
                source="QuarantineManager",
                description=f"Permanently purged quarantine record #{quarantine_id} ({record['original_path']}).",
                severity="Info"
            )
            return {"success": True}

        except Exception as e:
            logger.error(f"Error deleting quarantine file #{quarantine_id}: {e}")
            return {"success": False, "error": str(e)}

    def list_quarantined(self) -> list:
        return self.db.get_quarantined_files()
