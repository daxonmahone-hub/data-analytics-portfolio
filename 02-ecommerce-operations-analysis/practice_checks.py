"""Answer checker for practice.ipynb. Stores only hashes, so it can't reveal answers."""
import hashlib

# exercise id -> (required columns, column checked in row 1, expected row count, hashes of accepted answers)
EXPECTED = {
    "E1": [
        [
            "order_status",
            "orders"
        ],
        "orders",
        8,
        [
            "24e892504ddf2384"
        ]
    ],
    "E2": [
        [
            "category",
            "items",
            "avg_freight"
        ],
        "avg_freight",
        5,
        [
            "9aeff0dcfe8245e0"
        ]
    ],
    "E3": [
        [
            "weekday",
            "orders"
        ],
        "weekday",
        7,
        [
            "d618fb157a4b382e"
        ]
    ],
    "E4": [
        [
            "review_score",
            "reviews",
            "pct_with_comment"
        ],
        "pct_with_comment",
        5,
        [
            "1be4d31d4559b688"
        ]
    ],
    "E5": [
        [
            "month",
            "revenue",
            "mom_growth_pct"
        ],
        "mom_growth_pct",
        3,
        [
            "be272f8fe2f9a584"
        ]
    ],
    "E6": [
        [
            "same_state",
            "items",
            "avg_days"
        ],
        "avg_days",
        2,
        [
            "1e81bf048f2b3ca9"
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
