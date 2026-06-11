import numpy as np

class ChronisClassifier:
    def __init__(self, window=7, threshold=0.35, min_logs=7, min_mentions=3):
        self.w = window
        self.t = threshold
        self.ml = min_logs
        self.mm = min_mentions

    def check_data(self, n, b):
        # Valid logs
        v_logs = np.sum(~np.isnan(b))
        v_ents = np.sum(~np.isnan(n))
        
        ok = v_logs >= self.ml and v_ents >= self.mm
        return ok, {"valid_logs": int(v_logs), "valid_entries": int(v_ents)}

    def classify(self, n, b):
        ok, ev = self.check_data(n, b)
        if not ok:
            return "INSUFFICIENT_EVIDENCE", 0.0, ev

        # Means
        mn = np.nanmean(n)
        mb = np.nanmean(b)
        diff = mn - mb

        # Aspiration
        if mn > 0.6:
            # Filter NaNs
            mask = ~np.isnan(b)
            if np.sum(mask) > 1:
                x = np.arange(len(b))[mask]
                y = b[mask]
                slope, _ = np.polyfit(x, y, 1)
                if slope <= 0:
                    conf = float(np.clip((mn - 0.6) + abs(slope), 0, 1))
                    return "ASPIRATION_GAP", conf, {"mean_n": float(mn), "slope_b": float(slope), "delta": float(diff), "mean_b": float(mb)}

        # Blindspot
        if mn < 0.15 and mb > 0.55:
            conf = float(np.clip((0.15 - mn) + (mb - 0.55), 0, 1))
            return "BLIND_SPOT", conf, {"mean_n": float(mn), "mean_b": float(mb), "delta": float(diff)}

        # Overstatement
        if diff > self.t and mb < 0.5:
            conf = float(np.clip(diff, 0, 1))
            return "OVERSTATEMENT", conf, {"mean_n": float(mn), "mean_b": float(mb), "delta": float(diff)}

        # Understatement
        if diff < -self.t and mb > 0.5:
            conf = float(np.clip(abs(diff), 0, 1))
            return "UNDERSTATEMENT", conf, {"mean_n": float(mn), "mean_b": float(mb), "delta": float(diff)}

        # Aligned
        return "ALIGNED", 1.0, {"mean_n": float(mn), "mean_b": float(mb), "delta": float(diff)}
