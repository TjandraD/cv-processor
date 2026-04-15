import re
import unicodedata

ABBREV_MAP = {
    "manajer proyek": "project manager",
    "pengembang perangkat lunak": "software developer",
    "s1": "bachelor",
    "s2": "master",
    "s3": "doctorate",
    "smk": "vocational high school",
    "sma": "high school",
}


def normalize(text: str) -> str:
    """Normalize raw CV text: unicode normalization, whitespace collapse, strip, lowercase, abbreviation mapping."""
    # 1. Unicode normalization
    text = unicodedata.normalize("NFKC", text)

    # 2. Collapse multiple spaces/tabs into a single space
    text = re.sub(r'\s+', ' ', text)

    # 3. Strip leading/trailing whitespace
    text = text.strip()

    # 4. Lowercase
    text = text.lower()

    # 5. Apply abbreviation map
    for abbrev, replacement in ABBREV_MAP.items():
        text = text.replace(abbrev, replacement)

    return text
