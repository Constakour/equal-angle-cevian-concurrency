# dangle_equal_angle_200.py
# ------------------------------------------------------------
# Compute d_angle(n) for the equal-angle model (n cevians per vertex,
# splitting each angle into n+1 equal sectors).
# - Fast O(n^2) method using trigonometric Ceva with analytic inversion.
# - Includes a conjectural closed-form rule a_rule(n) and a side-by-side check.
# - Can list all solution triples (i,j,k) for a chosen n.
# - Can write an OEIS-style b-file with lines "n a(n)".
# Pure Python (no external deps).
# ------------------------------------------------------------

import math
import argparse

SQRT3 = math.sqrt(3.0)

def precompute_R(n: int):
    """Return (theta, R[1..n]) where R(k*theta) = 2*tan(k*theta)/(sqrt(3)-tan(k*theta))."""
    if n <= 0:
        return (None, [])
    theta = math.pi / (3.0 * (n + 1))
    R = [0.0] * (n + 1)  # 1-based
    for k in range(1, n + 1):
        t = math.tan(k * theta)
        R[k] = (2.0 * t) / (SQRT3 - t)
    return theta, R

def d_angle_fast(n: int, tol: float = 1e-12) -> int:
    """
    Return d_angle(n) using:
      R(x) = 2*tan(x)/(sqrt(3) - tan(x)),  theta = pi/(3*(n+1)).
      Ceva: R(i*theta)*R(j*theta)*R(k*theta) = 1.
    For each (i,j) we invert R to get a candidate k and verify within 'tol'.
    """
    if n <= 0:
        return 0

    theta, R = precompute_R(n)

    count = 0
    for i in range(1, n + 1):
        Ri = R[i]
        for j in range(1, n + 1):
            r_target = 1.0 / (Ri * R[j])  # target = R(k*theta)
            if r_target <= 0.0:
                continue
            # Invert R:  r = 2t/(sqrt(3)-t)  ==>  t = r*sqrt(3)/(2+r)
            t = (r_target * SQRT3) / (2.0 + r_target)
            if t <= 0.0:
                continue
            x = math.atan(t)               # in (0, pi/3)
            k = int(round(x / theta))
            if 1 <= k <= n:
                prod = Ri * R[j] * R[k]
                if abs(prod - 1.0) <= tol:
                    count += 1

    return count

def list_solutions(n: int, tol: float = 1e-12):
    """
    Enumerate all triples (i,j,k) in {1..n}^3 satisfying
       R(i*theta)*R(j*theta)*R(k*theta) = 1
    within tolerance 'tol'. Returns a list of tuples (i,j,k).
    """
    if n <= 0:
        return []

    theta, R = precompute_R(n)
    sols = []
    for i in range(1, n + 1):
        Ri = R[i]
        for j in range(1, n + 1):
            r_target = 1.0 / (Ri * R[j])
            if r_target <= 0.0:
                continue
            t = (r_target * SQRT3) / (2.0 + r_target)
            if t <= 0.0:
                continue
            x = math.atan(t)
            k = int(round(x / theta))
            if 1 <= k <= n:
                prod = Ri * R[j] * R[k]
                if abs(prod - 1.0) <= tol:
                    sols.append((i, j, k))
    return sols

def a_rule(n: int) -> int:
    """
    Conjectural closed-form (matches all computed values up to at least n=200):
      a(n) = 0                if n is even
           = 3n - 2           if n is odd and n % 10 != 9
           = 3n + 10          if n is odd and n % 10 == 9
    """
    if n % 2 == 0:
        return 0
    return (3*n - 2) + (12 if n % 10 == 9 else 0)

def write_bfile(vals, path):
    """
    Write an OEIS b-file:
      1 a(1)
      2 a(2)
      ...
    The offset here is 1.
    """
    with open(path, "w", encoding="utf-8") as f:
        for n, v in enumerate(vals, start=1):
            f.write(f"{n} {v}\n")

def main():
    ap = argparse.ArgumentParser(description="d_angle(n) for equal-angle cevians; list solution triples; write b-file.")
    ap.add_argument("--max-n", type=int, default=200, help="Compute table for n=1..MAX_N (default 200).")
    ap.add_argument("--tol", type=float, default=1e-12, help="Tolerance for Ceva verification (default 1e-12).")
    ap.add_argument("--csv", action="store_true", help="Also print CSV (n,d_angle(n)) lines.")
    ap.add_argument("--oeis-line", action="store_true", help="Also print a single OEIS-style data line for n=1..MAX_N.")
    ap.add_argument("--no-table", action="store_true", help="Suppress the side-by-side table.")
    ap.add_argument("--list-triples", type=int, default=None,
                    help="If set to N, list all solution triples (i,j,k) for that N (with --tol).")
    ap.add_argument("--bfile", default=None, help="Write b-file to this path (n a(n) for n=1..MAX_N).")
    args = ap.parse_args()

    vals = []
    if not args.no_table:
        print("n :  d_angle_fast  |  a_rule   check")
    for n in range(1, args.max_n + 1):
        d = d_angle_fast(n, tol=args.tol)
        vals.append(d)
        if not args.no_table:
            r = a_rule(n)
            print(f"{n:3d}: {d:12d}  |  {r:6d}   {'OK' if d == r else 'DIFF'}")

    if args.csv:
        for n, d in enumerate(vals, start=1):
            print(f"{n},{d}")

    if args.oeis_line:
        print("OEIS data (offset 1):")
        print(", ".join(str(d) for d in vals))

    if args.list_triples is not None:
        N = args.list_triples
        sols = list_solutions(N, tol=args.tol)
        print(f"\nSolution triples for n={N} (tol={args.tol}): count = {len(sols)}")
        sols.sort()
        for t in sols:
            print(t)
        print(f"Rule a_rule({N}) = {a_rule(N)}")

    if args.bfile:
        write_bfile(vals, args.bfile)
        print(f"Wrote b-file: {args.bfile}")

if __name__ == "__main__":
    main()
