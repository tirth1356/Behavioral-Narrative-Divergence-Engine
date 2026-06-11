import json

class JSONFormatter:
    @staticmethod
    def get_evidence(cls_type):
        ev = {
            "OVERSTATEMENT": "Narrative intensity significantly exceeds behavioral prominence.",
            "UNDERSTATEMENT": "Behavioral prominence significantly exceeds narrative intensity.",
            "BLIND_SPOT": "Consistent behavioral activity with negligible narrative mention.",
            "ASPIRATION_GAP": "High narrative intent paired with stagnant or declining behavioral metrics.",
            "ALIGNED": "Narrative and behavior are aligned.",
            "INSUFFICIENT_EVIDENCE": "Data density below minimum thresholds."
        }
        return ev.get(cls_type, "Unknown")

    @staticmethod
    def format_output(uid, domain, start, end, n, b, diff, cls_type, conf, status="SUCCESS"):
        # JSON structure matching exact brief
        out = {
            "user_id": uid,
            "domain": domain,
            "metrics": {
                "narrative_intensity": round(float(n), 2),
                "behavioral_prominence": round(float(b), 2),
                "calculated_delta": round(float(diff), 2)
            },
            "status": status,
            "divergence_classification": cls_type,
            "evidence_summary": JSONFormatter.get_evidence(cls_type)
        }
        return json.dumps(out, indent=2)

    @staticmethod
    def format_abstention(uid, domain, start, end, ev):
        out = {
            "user_id": uid,
            "domain": domain,
            "metrics": {
                "narrative_intensity": None,
                "behavioral_prominence": None,
                "calculated_delta": None
            },
            "status": "INSUFFICIENT_EVIDENCE",
            "divergence_classification": "INSUFFICIENT_EVIDENCE",
            "evidence_summary": f"Only {ev['valid_logs']} logs, {ev['valid_entries']} entries."
        }
        return json.dumps(out, indent=2)
