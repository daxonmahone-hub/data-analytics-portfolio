"""Answer checker for practice.ipynb. Stores only hashes, so it can't reveal answers."""
import hashlib

# exercise id -> (required columns, column checked in row 1, expected row count, hashes of accepted answers)
EXPECTED = {
    "S1": [
        [
            "windows",
            "mac",
            "linux"
        ],
        "mac",
        1,
        [
            "6a1b1d39f6cbc671"
        ]
    ],
    "S2": [
        [
            "developer",
            "games"
        ],
        "games",
        10,
        [
            "02b3bd14b7d5b855"
        ]
    ],
    "S3": [
        [
            "year",
            "games",
            "avg_price"
        ],
        "avg_price",
        10,
        [
            "9c7f38a9ac4f5de5"
        ]
    ],
    "S4": [
        [
            "name",
            "avg_hours"
        ],
        "name",
        10,
        [
            "2ed9585aa91fd80e"
        ]
    ],
    "S5": [
        [
            "year",
            "name",
            "positive"
        ],
        "name",
        7,
        [
            "521fe5c9ece1aa1f"
        ]
    ],
    "S6": [
        [
            "is_indie",
            "games",
            "pct_positive",
            "pct_1m_plus"
        ],
        "pct_positive",
        2,
        [
            "8e46c22752c9f153"
        ]
    ]
}


def _norm(v):
    """Normalize a value the same way the answer key was built."""
    if isinstance(v, bool) or type(v).__name__ == "bool_":
        return str(bool(v)).lower()
    try:
        return f"{float(v):.1f}"
    except (TypeError, ValueError):
        return str(v).strip().lower()


def _h(s):
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def check(ex_id, df):
    """Check a query result against the answer key and print feedback."""
    cols, key_col, n_rows, hashes = EXPECTED[ex_id]
    if list(df.columns) == ["todo"]:
        print(f"{ex_id}: not attempted yet. Replace the placeholder query with yours.")
        return False
    lower = {c.lower(): c for c in df.columns}
    missing = [c for c in cols if c.lower() not in lower]
    if missing:
        print(f"{ex_id}: missing column(s) {missing}. Name your output columns exactly: {cols} (use AS).")
        return False
    if len(df) != n_rows:
        print(f"{ex_id}: expected {n_rows} row(s), got {len(df)}. Check your filters, GROUP BY, or LIMIT.")
        return False
    if _h(_norm(df[lower[key_col.lower()]].iloc[0])) not in hashes:
        print(f"{ex_id}: right shape, but '{key_col}' in the first row doesn't match. Check sort order, JOIN conditions, filters, and rounding.")
        return False
    print(f"{ex_id}: correct!")
    return True
