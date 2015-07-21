set terminal  eps enhanced color font 'palatino,11'
set output 'kconfig_sizes.eps'
#set pointsize 2
set boxwidth 1
set grid
set style fill solid 1.0 border -1
set xrange[-.5:*]
set yrange[9000:*]
set ylabel 'Number of features'
set xlabel 'Architecture'
set key font "palatino,11"
set xtics border in scale 0,10 nomirror rotate by -45 font "palatino,11"
plot 'kconfig_sizes.dat' u ($0):2:($0):xticlabels(1) w boxes lc variable notitle
