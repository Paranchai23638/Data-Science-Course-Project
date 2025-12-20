import json
from pathlib import Path

from tqdm import tqdm
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = PROJECT_ROOT / "Data"

YEARS = ["2018", "2019", "2020", "2021", "2022", "2023"]

def parse_paper(path: Path):
    """Read ONE JSON file and return a dict with clean fields.
       Returns None if something is wrong."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return None

    resp = data.get("abstracts-retrieval-response", {})
    core = resp.get("coredata", {})

    eid = core.get("eid")
    title = core.get("dc:title")
    cover_date = core.get("prism:coverDate")
    journal = core.get("prism:publicationName")
    citedby = core.get("citedby-count")
    doi = core.get("prism:doi")

    year = None
    if cover_date:
        year = cover_date.split("-")[0]

    authors_obj = resp.get("authors", {}).get("author", [])
    if isinstance(authors_obj, dict):
        authors_list = [authors_obj]
    elif isinstance(authors_obj, list):
        authors_list = authors_obj
    else:
        authors_list = []

    author_names = []
    author_ids = []

    for a in authors_list:
        if not isinstance(a, dict):
            continue
        name = a.get("ce:indexed-name") or a.get("preferred-name", {}).get("ce:indexed-name")
        if name:
            author_names.append(name)

        auid = a.get("@auid")
        if auid:
            author_ids.append(str(auid))

    authors_str = "; ".join(author_names) if author_names else None
    author_ids_str = "; ".join(author_ids) if author_ids else None

    subjects_obj = resp.get("subject-areas", {}).get("subject-area", [])
    if isinstance(subjects_obj, dict):
        subjects = [subjects_obj]
    elif isinstance(subjects_obj, list):
        subjects = subjects_obj
    else:
        subjects = []

    subj_names = []
    for s in subjects:
        if isinstance(s, dict):
            name = s.get("$")
            if name:
                subj_names.append(name)
    subject_areas_str = "; ".join(subj_names) if subj_names else None

    affils_obj = resp.get("affiliation", [])
    if isinstance(affils_obj, dict):
        affils = [affils_obj]
    elif isinstance(affils_obj, list):
        affils = affils_obj
    else:
        affils = []

    countries_set = set()
    for af in affils:
        if not isinstance(af, dict):
            continue
        c = af.get("affiliation-country")
        if c:
            countries_set.add(c)

    countries = sorted(countries_set)
    countries_str = "; ".join(countries) if countries else None

    if not eid:
        return None

    return {
        "eid": eid,
        "title": title,
        "cover_date": cover_date,
        "year": year,
        "journal": journal,
        "citedby_count": int(citedby) if citedby is not None else None,
        "doi": doi,
        "authors_str": authors_str,
        "author_ids_str": author_ids_str,
        "subject_areas_str": subject_areas_str,
        "countries_str": countries_str,
        "source_file": str(path),
    }


def main():
    records = []

    for y in YEARS:
        year_dir = DATA_ROOT / y
        print(f"Processing year {y} in {year_dir}...")

        files = sorted(
            f for f in year_dir.iterdir()
            if f.is_file() and not f.name.startswith(".")
        )

        for fpath in tqdm(files, desc=f"Year {y}"):
            rec = parse_paper(fpath)
            if rec:
                records.append(rec)

    df = pd.DataFrame(records)
    print("Total papers:", len(df))

    output_path = PROJECT_ROOT / "papers_all_years.csv"
    df.to_csv(output_path, index=False)
    print("Saved to", output_path)


if __name__ == "__main__":
    main()