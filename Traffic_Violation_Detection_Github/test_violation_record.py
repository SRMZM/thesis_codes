# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 14:58:01 2026

@author: Russell
"""

from violation_record import ViolationRecord


# =========================================================
# Create a test violation record
# =========================================================

record = ViolationRecord(

    track_id=17,

    plate="۶۷ن۲۵۵۹۳",

    entry_side="north",
    exit_side="east",

    violation=True,
    violation_type="Illegal Left Turn",

    entry_frame=1520,
    violation_frame=1842,
    exit_frame=1910,

    entry_timestamp="00:00:50.666",
    violation_timestamp="00:01:01.400",
    exit_timestamp="00:01:03.666",

    date="1405/06/08",
    time="14:37:21"
)


# =========================================================
# Print record
# =========================================================

print(record)


# =========================================================
# Print dictionary
# =========================================================

print(
    record.to_dict()
)
