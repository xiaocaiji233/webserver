@echo off

python gprof2dot.py -f pstats TriFusion_00e5c44d5a_0.prof | dot -Tpng -o result.png
pause