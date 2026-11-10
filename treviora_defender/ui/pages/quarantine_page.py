r"""
TREVIORA AI DEFENDER - Page 5: Quarantine Vault
Secure isolation chamber storing encrypted (.tquar) payloads strictly under
D:\projects\antivirus\data\quarantine\.
Provides SHA-256 hash auditing, secure restoration, and cryptographic shredding.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt
from treviora_defender.quarantine.quarantine_manager import QuarantineManager
from treviora_defender.database.db_manager import DatabaseManager


class QuarantinePage(QWidget):
    def __init__(self):
        super().__init__()
        self.quarantine_mgr = QuarantineManager()
        self.db = DatabaseManager()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)

        # Header
        header_row = QHBoxLayout()
        header = QVBoxLayout()
        title = QLabel("Quarantine Vault")
        title.setProperty("class", "PageTitle")
        sub = QLabel("Inert AES-GCM encrypted vault preventing accidental execution • Located in D:\\projects\\antivirus\\data\\quarantine")
        sub.setProperty("class", "PageSubtitle")
        header.addWidget(title)
        header.addWidget(sub)
        header_row.addLayout(header)
        header_row.addStretch()

        btn_refresh = QPushButton("🔄 Refresh Vault")
        btn_refresh.setProperty("class", "SecondaryButton")
        btn_refresh.clicked.connect(self.refresh_quarantine)
        header_row.addWidget(btn_refresh)
        layout.addLayout(header_row)

        # Quarantine table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Original File Path", "Detected Threat", "SHA-256 Checksum", "Size (Bytes)", "Quarantined Date", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        self.refresh_quarantine()

    def refresh_quarantine(self):
        records = self.quarantine_mgr.list_quarantined()
        self.table.setRowCount(0)

        for r, rec in enumerate(records):
            self.table.insertRow(r)

            # Original path
            p_item = QTableWidgetItem(rec.get("original_path", ""))
            p_item.setToolTip(rec.get("original_path", ""))
            self.table.setItem(r, 0, p_item)

            # Threat name
            self.table.setItem(r, 1, QTableWidgetItem(rec.get("threat_name", "Malware")))

            # Hash (truncate display)
            h = rec.get("file_hash", "")
            h_disp = (h[:8] + "..." + h[-8:]) if len(h) > 16 else h
            h_item = QTableWidgetItem(h_disp)
            h_item.setToolTip(h)
            self.table.setItem(r, 2, h_item)

            # Size
            self.table.setItem(r, 3, QTableWidgetItem(f"{rec.get('file_size', 0):,}"))

            # Date
            dt = rec.get("quarantined_at", "").replace("T", " ")[:19]
            self.table.setItem(r, 4, QTableWidgetItem(dt))

            # Action buttons
            btn_box = QWidget()
            btn_layout = QHBoxLayout(btn_box)
            btn_layout.setContentsMargins(4, 2, 4, 2)
            btn_layout.setSpacing(6)

            btn_restore = QPushButton("Restore")
            btn_restore.setProperty("class", "SecondaryButton")
            btn_restore.setFixedHeight(26)
            btn_restore.clicked.connect(lambda _, q_id=rec["id"]: self.restore_item(q_id))

            btn_delete = QPushButton("Shred")
            btn_delete.setProperty("class", "DangerButton")
            btn_delete.setFixedHeight(26)
            btn_delete.clicked.connect(lambda _, q_id=rec["id"]: self.delete_item(q_id))

            btn_layout.addWidget(btn_restore)
            btn_layout.addWidget(btn_delete)
            self.table.setCellWidget(r, 5, btn_box)

    def restore_item(self, q_id: int):
        reply = QMessageBox.question(
            self, "Confirm Restoration",
            "Are you sure you want to restore this file back to its original location?\n"
            "Only proceed if you are confident this file is safe.",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            res = self.quarantine_mgr.restore_file(q_id)
            if res["success"]:
                QMessageBox.information(self, "Restored", f"File restored to:\n{res['restored_path']}")
                self.refresh_quarantine()
            else:
                QMessageBox.critical(self, "Restore Error", res.get("error", "Failed"))

    def delete_item(self, q_id: int):
        reply = QMessageBox.question(
            self, "Confirm Shredding",
            "Permanently shred and delete this quarantined payload?\n"
            "This action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            res = self.quarantine_mgr.delete_permanently(q_id)
            if res["success"]:
                QMessageBox.information(self, "Shredded", "Quarantined file has been zero-overwritten and shredded.")
                self.refresh_quarantine()
            else:
                QMessageBox.critical(self, "Delete Error", res.get("error", "Failed"))
