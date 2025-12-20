import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = PROJECT_ROOT / "Data"
example_file = DATA_ROOT / "2018" / "201800000"

with open(example_file, encoding="utf-8") as f:
    data = json.load(f)

resp = data["abstracts-retrieval-response"]

core = resp.get("coredata", {})
authors = resp.get("authors", {}).get("author", [])
affils = resp.get("affiliation", [])
subjects = resp.get("subject-areas", {}).get("subject-area", [])

print("Title:", core.get("dc:title"))
print("Date :", core.get("prism:coverDate"))
print("Cited by:", core.get("citedby-count"))
print("Journal:", core.get("prism:publicationName"))

print("\nAuthors:")
for a in authors:
    print(" -", a.get("ce:indexed-name"), "| author id:", a.get("@auid"))

print("\nAffiliations:")
for af in affils:
    print(" -", af.get("affilname"), "|", af.get("affiliation-country"))

print("\nSubject areas:")
for s in subjects:
    print(" -", s.get("$"), "| code:", s.get("@code"))