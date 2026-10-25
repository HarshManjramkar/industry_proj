"""Normalization and cleaning utilities for Indian currency, dates, and Marathi names.
Enforces Article I & II of Constitution.
"""

import re
from datetime import date, datetime
from typing import Optional


def parse_inr_value(value_str: str) -> float:
    """Deterministically parse Indian currency string into float INR.
    Handles '₹ 18,50,00,000', '18.50 crore', '425 lakh', 'Rs. 50,000'.
    """
    if not value_str:
        return 0.0

    cleaned = value_str.strip().lower()
    cleaned = cleaned.replace("₹", "").replace("rs.", "").replace("rs", "").strip()

    # Match crore notation (e.g., '18.50 crore', '18.5 cr')
    crore_match = re.search(r"([\d\.]+)\s*(?:crore|cr)", cleaned)
    if crore_match:
        val = float(crore_match.group(1))
        return round(val * 10_000_000.0, 2)

    # Match lakh notation (e.g., '425 lakh', '42.5 lac')
    lakh_match = re.search(r"([\d\.]+)\s*(?:lakh|lac|lacs)", cleaned)
    if lakh_match:
        val = float(lakh_match.group(1))
        return round(val * 100_000.0, 2)

    # Standard comma-separated number: '18,50,00,000'
    cleaned_num = cleaned.replace(",", "").strip()
    try:
        return float(cleaned_num)
    except ValueError:
        return 0.0


def parse_iso_date(date_str: str) -> Optional[date]:
    """Parse various date formats into standard ISO date object."""
    if not date_str:
        return None
    cleaned = date_str.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d %b %Y", "%d-%b-%Y"):
        try:
            return datetime.strptime(cleaned, fmt).date()
        except ValueError:
            continue
    return None
