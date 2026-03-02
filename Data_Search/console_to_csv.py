import json
import csv
import re
from typing import List, Dict, Any, Optional

# ====== CONFIG ======
LOG_FILES = [
    "run_test_api_fuzzy.txt"
]
OUTPUT_CSV = "gleif_results_test_2.csv"

# If True: keep one best row per source_address
# If False: keep all rows (including duplicates)
DEDUP_BY_SOURCE_ADDRESS = True


def extract_json_from_line(line: str) -> Optional[Dict[str, Any]]:
    """
    Extract first JSON object found in a log line and parse it.
    Returns dict or None.
    """
    line = line.strip()
    if not line:
        return None

    m = re.search(r'(\{.*\})', line)
    if not m:
        return None

    try:
        obj = json.loads(m.group(1))
        return obj if isinstance(obj, dict) else None
    except json.JSONDecodeError:
        return None


def load_rows_from_logs(files: List[str]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []

    for path in files:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                obj = extract_json_from_line(line)
                if not obj:
                    continue

                # Keep only rows that look like your output schema
                if "source_address" not in obj:
                    continue

                row = {
                    "source_address": obj.get("source_address"),
                    "matched_address": obj.get("matched_address"),
                    "lei": obj.get("lei"),
                    "entity_name": obj.get("entity_name"),
                    "lei_record_url": obj.get("lei_record_url"),
                    "error": obj.get("error"),
                }
                rows.append(row)

    return rows


def row_quality_score(row: Dict[str, Any]) -> int:
    """
    Higher score = better row when deduplicating.
    Prioritize complete successful rows.
    """
    score = 0
    if row.get("lei"):
        score += 3
    if row.get("entity_name"):
        score += 3
    if row.get("matched_address"):
        score += 2
    if not row.get("error"):
        score += 2
    return score


def dedup_best_by_source(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Keep best row per source_address.
    """
    best: Dict[str, Dict[str, Any]] = {}

    for row in rows:
        key = (row.get("source_address") or "").strip()
        if not key:
            # keep blank keys as unique by appending index-like behavior
            key = f"__blank__{id(row)}"

        if key not in best:
            best[key] = row
            continue

        existing = best[key]
        if row_quality_score(row) > row_quality_score(existing):
            best[key] = row

    return list(best.values())


def write_csv(rows: List[Dict[str, Any]], out_path: str) -> None:
    fieldnames = [
        "source_address",
        "matched_address",
        "lei",
        "entity_name",
        "lei_record_url",
        "error",
    ]

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def print_error_summary(rows: List[Dict[str, Any]]) -> None:
    from collections import Counter

    def norm_err(e: Any) -> str:
        if e is None:
            return ""
        return str(e).strip().lower()

    errors = [norm_err(r.get("error")) for r in rows]
    non_blank = [e for e in errors if e != ""]
    counts = Counter(non_blank)

    no_match_count = counts.get("no_match", 0)
    errored_count = len(non_blank)
    success_count = len(rows) - errored_count

    print("\n===== Summary =====")
    print(f"Total rows: {len(rows)}")
    print(f"Success rows (blank error): {success_count}")
    print(f"Errored rows (non-blank error): {errored_count}")
    print(f"no_match rows: {no_match_count}")

    if counts:
        print("\nError breakdown:")
        for err, cnt in counts.most_common():
            print(f"  {err}: {cnt}")


def main():
    all_rows = load_rows_from_logs(LOG_FILES)

    if DEDUP_BY_SOURCE_ADDRESS:
        final_rows = dedup_best_by_source(all_rows)
    else:
        final_rows = all_rows

    write_csv(final_rows, OUTPUT_CSV)
    print_error_summary(final_rows)   # <-- add this line

    print(f"Loaded rows: {len(all_rows)}")
    print(f"Final rows written: {len(final_rows)}")
    print(f"Output file: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
