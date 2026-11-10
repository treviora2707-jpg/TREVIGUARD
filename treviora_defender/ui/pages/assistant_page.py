"""
TREVIORA AI DEFENDER - Page 6: AI Security Assistant
Interactive cyber assistant answering malware queries, explaining scan telemetry,
and recommending mitigation actions.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QLineEdit, QFrame, QScrollArea
)
from PySide6.QtCore import Qt, QThread, Signal
from treviora_defender.ai_assistant.assistant import AIAssistant


class AIQueryWorker(QThread):
    response_signal = Signal(str)

    def __init__(self, assistant: AIAssistant, prompt: str):
        super().__init__()
        self.assistant = assistant
        self.prompt = prompt

    def run(self):
        resp = self.assistant.query(self.prompt)
        self.response_signal.emit(resp)


class AssistantPage(QWidget):
    def __init__(self):
        super().__init__()
        self.assistant = AIAssistant()
        self.worker = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        # Header
        header = QVBoxLayout()
        title = QLabel("AI Security Assistant")
        title.setProperty("class", "PageTitle")
        sub = QLabel("Threat forensics • Incident triage • Defensive cybersecurity knowledge base")
        sub.setProperty("class", "PageSubtitle")
        header.addWidget(title)
        header.addWidget(sub)
        layout.addLayout(header)

        # Privacy Notice Banner
        priv_frame = QFrame()
        priv_frame.setStyleSheet("background-color: #0E1E38; border: 1px solid #1E3A8A; border-radius: 8px;")
        priv_layout = QHBoxLayout(priv_frame)
        priv_layout.setContentsMargins(14, 10, 14, 10)
        priv_text = QLabel("🔒 Privacy Guarantee: Operates offline using local knowledge base. Never transmits private files externally without consent.")
        priv_text.setStyleSheet("color: #38BDF8; font-size: 11px; font-weight: 600;")
        priv_layout.addWidget(priv_text)
        layout.addWidget(priv_frame)

        # Quick Suggestion Pills Row
        pills_layout = QHBoxLayout()
        pills_layout.setSpacing(8)

        suggestions = [
            ("🛡️ System Security Health", "Evaluate current system security health and threat status"),
            ("🦠 Ransomware Indicators", "What are the primary indicators of ransomware and how to stop it?"),
            ("🧠 AI Risk Scoring", "How does the Treviora ONNX AI PE threat model calculate risk scores?"),
            ("🧪 EICAR Test String", "Explain what the EICAR standard antivirus test file is")
        ]

        for label, q_text in suggestions:
            btn = QPushButton(label)
            btn.setProperty("class", "SecondaryButton")
            btn.setFixedHeight(28)
            btn.clicked.connect(lambda _, p=q_text: self.send_prompt(p))
            pills_layout.addWidget(btn)

        pills_layout.addStretch()
        layout.addLayout(pills_layout)

        # Chat / Response Area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #0F172A;
                border: 1px solid #1E293B;
                border-radius: 10px;
                padding: 16px;
                color: #E2E8F0;
                font-size: 13px;
                line-height: 1.6;
            }
        """)
        layout.addWidget(self.chat_display, 1)

        # Bottom Input Row
        input_row = QHBoxLayout()
        input_row.setSpacing(10)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask a cybersecurity question or request threat analysis...")
        self.input_field.setFixedHeight(40)
        self.input_field.returnPressed.connect(self.on_submit)
        input_row.addWidget(self.input_field, 1)

        self.btn_send = QPushButton("Send Question")
        self.btn_send.setProperty("class", "PrimaryButton")
        self.btn_send.setFixedHeight(40)
        self.btn_send.clicked.connect(self.on_submit)
        input_row.addWidget(self.btn_send)

        layout.addLayout(input_row)

        # Initial greeting
        self.append_message("Assistant", (
            "Greetings! I am the **Treviora AI Security Assistant**.\n\n"
            "I can explain threat indicators, assist you with suspicious file analysis, explain PE characteristics, "
            "and suggest defensive best practices for your Windows 11 endpoint.\n\n"
            "How may I assist your system security today?"
        ))

    def on_submit(self):
        txt = self.input_field.text().strip()
        if not txt:
            return
        self.input_field.clear()
        self.send_prompt(txt)

    def send_prompt(self, prompt: str):
        self.append_message("User", prompt)
        self.btn_send.setEnabled(False)
        self.btn_send.setText("Analyzing...")

        self.worker = AIQueryWorker(self.assistant, prompt)
        self.worker.response_signal.connect(self._on_ai_response)
        self.worker.start()

    def _on_ai_response(self, response: str):
        self.btn_send.setEnabled(True)
        self.btn_send.setText("Send Question")
        self.append_message("Assistant", response)

    def append_message(self, sender: str, text: str):
        if sender == "User":
            bubble = f"<p style='color: #00D2FF; font-weight: bold;'>You:</p><p style='color: #F8FAFC;'>{text}</p><hr style='border: 1px solid #1E293B;'/>"
        else:
            formatted_text = text.replace("\n", "<br/>")
            bubble = f"<p style='color: #10B981; font-weight: bold;'>Treviora AI Assistant:</p><div style='color: #CBD5E1;'>{formatted_text}</div><hr style='border: 1px solid #1E293B;'/>"
        self.chat_display.append(bubble)
        # Auto-scroll to latest response
        sb = self.chat_display.verticalScrollBar()
        sb.setValue(sb.maximum())
