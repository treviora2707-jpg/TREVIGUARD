r"""
TREVIORA AI DEFENDER - Machine Learning PE Malware Classifier
Supports ONNX Runtime and scikit-learn models.
Trains and exports models strictly to D:\projects\antivirus\data\models\.
"""
import os
import joblib
import numpy as np
from pathlib import Path
from treviora_defender.config.constants import MODELS_DIR
from treviora_defender.utils.logger import get_logger

logger = get_logger()

ONNX_MODEL_PATH = MODELS_DIR / "treviora_pe_classifier.onnx"
SKLEARN_MODEL_PATH = MODELS_DIR / "treviora_pe_classifier.joblib"


class MLMalwareModel:
    def __init__(self):
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        self.onnx_session = None
        self.sklearn_model = None
        self.model_type = "heuristic"
        self._load_or_train_model()

    def _train_default_model(self):
        """
        Synthesizes a robust training set representing PE characteristics of benign vs malicious software,
        trains a Random Forest classifier, and exports both ONNX and Joblib formats.
        """
        logger.info("Training initial Treviora PE AI threat model...")
        from sklearn.ensemble import RandomForestClassifier

        np.random.seed(42)
        n_samples = 4000

        # Features:
        # [0: overall_entropy (0-8),
        #  1: max_sec_entropy (0-8),
        #  2: num_sections (1-20),
        #  3: has_wx_sections (0/1),
        #  4: has_packed_names (0/1),
        #  5: injection_apis (0-15),
        #  6: crypto_apis (0-10),
        #  7: spyware_apis (0-10),
        #  8: evasion_apis (0-10),
        #  9: network_apis (0-10),
        #  10: is_signed (0/1)]

        # Benign distribution (2000 samples)
        benign_entropy = np.random.normal(5.8, 0.6, n_samples // 2).clip(2.0, 7.1)
        benign_max_entropy = np.random.normal(6.2, 0.5, n_samples // 2).clip(3.0, 7.2)
        benign_sections = np.random.randint(3, 8, n_samples // 2)
        benign_wx = np.random.choice([0, 1], p=[0.98, 0.02], size=n_samples // 2)
        benign_packed = np.random.choice([0, 1], p=[0.97, 0.03], size=n_samples // 2)
        benign_inj = np.random.poisson(0.2, n_samples // 2).clip(0, 3)
        benign_crypto = np.random.poisson(0.4, n_samples // 2).clip(0, 4)
        benign_spy = np.random.poisson(0.1, n_samples // 2).clip(0, 2)
        benign_evasion = np.random.poisson(0.3, n_samples // 2).clip(0, 2)
        benign_net = np.random.poisson(0.5, n_samples // 2).clip(0, 5)
        benign_signed = np.random.choice([0, 1], p=[0.20, 0.80], size=n_samples // 2)
        y_benign = np.zeros(n_samples // 2)

        X_benign = np.column_stack([
            benign_entropy, benign_max_entropy, benign_sections, benign_wx,
            benign_packed, benign_inj, benign_crypto, benign_spy,
            benign_evasion, benign_net, benign_signed
        ])

        # Malicious distribution (2000 samples)
        mal_entropy = np.random.normal(7.3, 0.5, n_samples // 2).clip(6.0, 8.0)
        mal_max_entropy = np.random.normal(7.6, 0.4, n_samples // 2).clip(6.8, 8.0)
        mal_sections = np.random.randint(1, 12, n_samples // 2)
        mal_wx = np.random.choice([0, 1], p=[0.40, 0.60], size=n_samples // 2)
        mal_packed = np.random.choice([0, 1], p=[0.35, 0.65], size=n_samples // 2)
        mal_inj = np.random.poisson(2.5, n_samples // 2).clip(0, 15)
        mal_crypto = np.random.poisson(1.8, n_samples // 2).clip(0, 10)
        mal_spy = np.random.poisson(1.5, n_samples // 2).clip(0, 10)
        mal_evasion = np.random.poisson(2.0, n_samples // 2).clip(0, 10)
        mal_net = np.random.poisson(1.5, n_samples // 2).clip(0, 10)
        mal_signed = np.random.choice([0, 1], p=[0.88, 0.12], size=n_samples // 2)
        y_mal = np.ones(n_samples // 2)

        X_mal = np.column_stack([
            mal_entropy, mal_max_entropy, mal_sections, mal_wx,
            mal_packed, mal_inj, mal_crypto, mal_spy,
            mal_evasion, mal_net, mal_signed
        ])

        X = np.vstack([X_benign, X_mal]).astype(np.float32)
        y = np.hstack([y_benign, y_mal]).astype(np.int64)

        clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
        clf.fit(X, y)

        # Save scikit-learn model
        joblib.dump(clf, str(SKLEARN_MODEL_PATH))
        self.sklearn_model = clf
        self.model_type = "scikit-learn"

        # Export to ONNX if skl2onnx is available
        try:
            from skl2onnx import convert_sklearn
            from skl2onnx.common.data_types import FloatTensorType

            initial_type = [("float_input", FloatTensorType([None, 11]))]
            onx = convert_sklearn(clf, initial_types=initial_type, target_opset=14)
            with open(ONNX_MODEL_PATH, "wb") as f:
                f.write(onx.SerializeToString())
            logger.info(f"Exported ONNX model to {ONNX_MODEL_PATH}")
        except Exception as e:
            logger.warning(f"ONNX export skipped: {e}")

    def _load_or_train_model(self):
        # Try loading ONNX first
        if ONNX_MODEL_PATH.exists():
            try:
                import onnxruntime as ort
                self.onnx_session = ort.InferenceSession(str(ONNX_MODEL_PATH))
                self.model_type = "ONNX"
                logger.info(f"Loaded ONNX model from {ONNX_MODEL_PATH}")
                return
            except Exception as e:
                logger.warning(f"Error loading ONNX model: {e}")

        # Try loading scikit-learn model
        if SKLEARN_MODEL_PATH.exists():
            try:
                self.sklearn_model = joblib.load(str(SKLEARN_MODEL_PATH))
                self.model_type = "scikit-learn"
                logger.info(f"Loaded scikit-learn model from {SKLEARN_MODEL_PATH}")
                return
            except Exception as e:
                logger.warning(f"Error loading Joblib model: {e}")

        # If neither exists or both failed, train fresh model
        try:
            self._train_default_model()
            if ONNX_MODEL_PATH.exists():
                import onnxruntime as ort
                self.onnx_session = ort.InferenceSession(str(ONNX_MODEL_PATH))
                self.model_type = "ONNX"
        except Exception as e:
            logger.error(f"Failed to train or load ML model: {e}")
            self.model_type = "heuristic"

    def predict_risk(self, feature_vector: list) -> float:
        """
        Runs inference on feature vector of length 11.
        Returns risk score from 0.0 to 100.0.
        """
        x = np.array(feature_vector, dtype=np.float32).reshape(1, -1)

        # 1. Try ONNX Runtime
        if self.onnx_session is not None:
            try:
                input_name = self.onnx_session.get_inputs()[0].name
                raw_out = self.onnx_session.run(None, {input_name: x})
                # Output 1 contains probability maps or arrays in ONNX scikit-learn format
                prob_data = raw_out[1]
                if isinstance(prob_data, list) and isinstance(prob_data[0], dict):
                    mal_prob = prob_data[0].get(1, 0.5)
                elif isinstance(prob_data, np.ndarray):
                    mal_prob = prob_data[0][1]
                else:
                    mal_prob = 0.5
                return round(float(mal_prob) * 100.0, 2)
            except Exception as e:
                logger.debug(f"ONNX inference fallback: {e}")

        # 2. Try scikit-learn
        if self.sklearn_model is not None:
            try:
                probs = self.sklearn_model.predict_proba(x)[0]
                return round(float(probs[1]) * 100.0, 2)
            except Exception as e:
                logger.debug(f"Sklearn inference fallback: {e}")

        # 3. Rule-based heuristic fallback if ML engine unavailable
        return self._heuristic_fallback(feature_vector)

    def _heuristic_fallback(self, f: list) -> float:
        # f: [overall_ent, max_sec_ent, n_sec, wx, packed, inj, crypto, spy, evasion, net, signed]
        score = 10.0
        if f[0] > 7.0: score += 20.0
        if f[1] > 7.4: score += 25.0
        if f[3] == 1: score += 20.0   # WX section
        if f[4] == 1: score += 20.0   # Packed section name
        score += min(f[5] * 12.0, 30.0) # Injection
        score += min(f[7] * 10.0, 20.0) # Spyware
        if f[10] == 1: score -= 30.0  # Signed
        return round(float(np.clip(score, 0.0, 100.0)), 2)
