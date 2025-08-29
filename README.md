# equal-angle-cevian-concurrency
Python code for the equal-angle cevian concurrency sequence d_angle(n):
number of interior triple intersections when each vertex is split into n+1
equal angular sectors. Fast O(n^2) trigonometric–Ceva method and a simple
closed-form rule for odd n.

## Quick start
python dangle_equal_angle_200.py
python dangle_equal_angle_200.py --csv
python dangle_equal_angle_200.py --no-table --oeis-line
python dangle_equal_angle_200.py --list-triples 39

## Make an OEIS b-file (lines "n a(n)" for n=1..200)
python dangle_equal_angle_200.py --no-table --max-n 200 --csv \
| awk -F, '{print $1 " " $2}' > bfile.txt

## Files
- dangle_equal_angle_200.py — main script
- test_rule.py — sanity check (fast method vs rule)
- LICENSE — MIT
- CITATION.cff — citation metadata
