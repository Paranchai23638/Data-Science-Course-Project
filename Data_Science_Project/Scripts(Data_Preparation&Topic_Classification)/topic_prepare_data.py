import json
from pathlib import Path
from tqdm import tqdm
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = PROJECT_ROOT / "Data"
YEARS = ["2018", "2019", "2020", "2021", "2022", "2023"]


def extract_abstract(resp: dict):
    """Extract abstract text from different possible Scopus locations."""
    core = resp.get("coredata", {})

    abstract = core.get("dc:description")
    if abstract:
        return abstract

    try:
        item = resp.get("item", {})
        bibrecord = item.get("bibrecord", {})
        head = bibrecord.get("head", {})
        abstracts = head.get("abstracts", {})

        if isinstance(abstracts, dict):
            text = abstracts.get("abstract", {}).get("ce:para")
            if text:
                return text
        elif isinstance(abstracts, list):
            for ab in abstracts:
                if not isinstance(ab, dict):
                    continue
                text = ab.get("abstract", {}).get("ce:para")
                if text:
                    return text
    except:
        pass

    return None


def parse_file(path: Path):
    """Extract fields needed for topic modeling."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return None

    resp = data.get("abstracts-retrieval-response", {})
    core = resp.get("coredata", {})

    eid = core.get("eid")
    if not eid:
        return None

    abstract = extract_abstract(resp)
    if not abstract:
        return None

    title = core.get("dc:title")
    cover_date = core.get("prism:coverDate")
    year = cover_date.split("-")[0] if cover_date else None

    subjects_obj = resp.get("subject-areas", {}).get("subject-area", [])
    if isinstance(subjects_obj, dict):
        subjects = [subjects_obj]
    else:
        subjects = subjects_obj if isinstance(subjects_obj, list) else []

    subject_list = [s.get("$") for s in subjects if isinstance(s, dict) and s.get("$")]
    subject_areas_str = "; ".join(subject_list) if subject_list else None

    return {
        "eid": eid,
        "title": title,
        "year": year,
        "abstract": abstract,
        "subject_areas_str": subject_areas_str,
        "source_file": str(path),
    }


def main():
    records = []

    for y in YEARS:
        year_dir = DATA_ROOT / y
        print(f"Processing {y} ...")
        files = sorted(f for f in year_dir.iterdir() if f.is_file() and not f.name.startswith("."))

        for path in tqdm(files, desc=f"Year {y}"):
            rec = parse_file(path)
            if rec:
                records.append(rec)

    df = pd.DataFrame(records)
    print("TOTAL papers with abstract:", len(df))

    out = PROJECT_ROOT / "topic_data.csv"
    df.to_csv(out, index=False)
    print("Saved:", out)


if __name__ == "__main__":
    main()
