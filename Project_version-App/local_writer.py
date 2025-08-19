import os
import json
from datetime import datetime

class LocalWriter:
    """
    - latest_info.json'a ATOMİK yazım yapar (tmp -> replace).
    - history/ YYYY-MM-DD.ndjson dosyasına tek satır JSON ekler (append_history).
    - Gerekirse snapshot kopyalama işini web veya manager tetikler (burada sadece JSON işleri).
    """

    def write_latest(self, payload: dict, path: str = "latest_info.json") -> bool:
        """
        Atomik yazım: önce path + ".tmp" dosyasına yaz, sonra os.replace ile final dosyayı değiştir.
        """
        try:
            tmp_path = path + ".tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False)
            os.replace(tmp_path, path)
            return True
        except Exception as e:
            print(f"Error: write_latest failed: {e}")
            # tmp kalırsa temizlemeyi deneyebiliriz
            try:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except Exception:
                pass
            return False

    def append_history(self, payload: dict, history_dir: str = "history") -> bool:
        """
        NDJSON (Newline-Delimited JSON): Her kayıt için tek satır JSON eklenir.
        Günlük dosya: history/YYYY-MM-DD.ndjson
        """
        try:
            os.makedirs(history_dir, exist_ok=True)
            day = datetime.utcnow().strftime("%Y-%m-%d")
            hist_file = os.path.join(history_dir, f"{day}.ndjson")
            line = json.dumps(payload, ensure_ascii=False)
            with open(hist_file, "a", encoding="utf-8") as f:
                f.write(line + "\n")
            return True
        except Exception as e:
            print(f"Error: append_history failed: {e}")
            return False
