import time
from datetime import datetime

GLOBAL_PULSE = []
PROTOCOL_STATS = {
    "total_audits": 0,
    "adal_count": 0,
    "aram_count": 0,
    "total_impact_score": 0.0,
    "boot_time": datetime.utcnow().isoformat(),
    "_start_ts": time.time()
}
