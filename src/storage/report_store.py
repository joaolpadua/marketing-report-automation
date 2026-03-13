import datetime
from pathlib import Path


def save_report(run_id: str, client_name: str, message: str):

    base_path = Path("reports") / run_id
    base_path.mkdir(parents=True, exist_ok=True)

    filename = client_name.lower().replace(" ", "_") + ".txt"

    filepath = base_path / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(message)

    return filepath