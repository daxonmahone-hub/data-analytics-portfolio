"""Answer checker for practice.ipynb. Stores only hashes, so it can't reveal answers."""
import hashlib

# exercise id -> (required columns, column checked in row 1, expected row count, hashes of accepted answers)
EXPECTED = {
    "H1": [
        [
            "GENDER",
            "patients"
        ],
        "patients",
        2,
        [
            "05e300642513b2f6"
        ]
    ],
    "H2": [
        [
            "DESCRIPTION",
            "patients"
        ],
        "patients",
        5,
        [
            "17e70b2fd0afd679"
        ]
    ],
    "H3": [
        [
            "stays",
            "avg_los_days"
        ],
        "avg_los_days",
        1,
        [
            "fbd04e1aae9ce0b1"
        ]
    ],
    "H4": [
        [
            "ENCOUNTERCLASS",
            "encounters",
            "total_cost"
        ],
        "total_cost",
        6,
        [
            "57381909c66b664f"
        ]
    ],
    "H5": [
        [
            "gaps",
            "avg_days_between_visits"
        ],
        "avg_days_between_visits",
        1,
        [
            "0c02f415ba7784e2"
        ]
    ],
    "H6": [
        [
            "has_hypertension",
            "patients",
            "avg_systolic"
        ],
        "avg_systolic",
        2,
        [
            "eb2ac84bf66db0d3"
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
