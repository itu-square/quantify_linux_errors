set terminal  eps enhanced color font 'palatino,11'
set output 'archsizes.eps'
#set pointsize 2
set boxwidth 1
set grid
set style fill solid 1.0 border -1
set xrange[-.5:*]
set yrange[0:*]
set ylabel '[kB]'
set xlabel 'Architecture directories'
set key font "palatino,11"
set xtics border in scale 0,10 nomirror rotate by -45 font "palatino,11"
plot 'archsizes.dat' u ($0):1:($0):xticlabels(2) w boxes lc variable notitle
