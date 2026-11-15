# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 18:33:33 2026

@author: Russell
"""

def calculate_segment_intersection(
        p1,
        p2,
        p3,
        p4
    ):

    x1, y1 = p1
    x2, y2 = p2

    x3, y3 = p3
    x4, y4 = p4

    denominator = (
        (x1 - x2) * (y3 - y4)
        - (y1 - y2) * (x3 - x4)
    )

    # Parallel or coincident lines.
    if denominator == 0:

        return None

    x = (
        (x1 * y2 - y1 * x2) * (x3 - x4)
        - (x1 - x2) * (x3 * y4 - y3 * x4)
    ) / denominator

    y = (
        (x1 * y2 - y1 * x2) * (y3 - y4)
        - (y1 - y2) * (x3 * y4 - y3 * x4)
    ) / denominator

    # Check whether the intersection lies on segment 1.
    if not (
        min(x1, x2) <= x <= max(x1, x2)
        and
        min(y1, y2) <= y <= max(y1, y2)
    ):

        return None

    # Check whether the intersection lies on segment 2.
    if not (
        min(x3, x4) <= x <= max(x3, x4)
        and
        min(y3, y4) <= y <= max(y3, y4)
    ):

        return None

    return (int(x), int(y))


# Test
# =============================================================================
# p1 = (100, 300)
# p2 = (700, 300)
# 
# p3 = (400, 100)
# p4 = (400, 500)
# 
# intersection = calculate_segment_intersection(
#     p1,
#     p2,
#     p3,
#     p4
# )
# 
# print(intersection)
# =============================================================================
