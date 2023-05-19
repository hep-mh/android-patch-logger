python3 plot_patch_history.py Nokia-6.1               patch_history 2018-02-25
python3 plot_patch_history.py OnePlus-6T              patch_history 2018-11-06
python3 plot_patch_history.py Samsung-Galaxy-Tab-S6   patch_history 2019-08-01 4
python3 plot_patch_history.py Samsung-Galaxy-Note-10+ patch_history 2019-08-23 4
python3 plot_patch_history.py Google-Pixel-6          patch_history 2021-10-28
python3 plot_patch_history.py Samsung-Galaxy-Tab-S8+  patch_history 2022-02-22

rm -rf all.pdf comparison.pdf
pdfjam *.pdf --nup 3x2 --landscape --outfile all.pdf

convert all.pdf all.png

#python3 plot_comparison.py
