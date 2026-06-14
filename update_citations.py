import json
import re
import urllib.request
from datetime import date
from pathlib import Path

path = Path("citation-metrics.json")
data = {
    "googleScholarCitations": 513,
    "googleScholarHIndex": 9,
    "lastUpdated": str(date.today())
}

if path.exists():
    try:
        data.update(json.loads(path.read_text(encoding="utf-8")))
    except Exception:
        pass

url = "https://scholar.google.com/citations?hl=en&user=tziEf2cAAAAJ"
request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

try:
    with urllib.request.urlopen(request, timeout=25) as response:
        html = response.read().decode("utf-8", errors="ignore")
    values = [int(x) for x in re.findall(r'class="gsc_rsb_std">(\d+)</td>', html)]
    if len(values) >= 3:
        data["googleScholarCitations"] = values[0]
        data["googleScholarHIndex"] = values[2]
        data["lastUpdated"] = str(date.today())
except Exception:
    data["lastUpdated"] = data.get("lastUpdated", str(date.today()))

path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
