from dangle_equal_angle_200 import d_angle_fast, a_rule

def main():
    bad = []
    for n in range(1, 201):
        d = d_angle_fast(n)
        r = a_rule(n)
        if d != r:
            bad.append((n, d, r))
    if bad:
        for n, d, r in bad:
            print(f"DIFF at n={n}: fast={d}, rule={r}")
        raise SystemExit(1)
    print("OK: d_angle_fast(n) == a_rule(n) for n=1..200")

if __name__ == "__main__":
    main()
