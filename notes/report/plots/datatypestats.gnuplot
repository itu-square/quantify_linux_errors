set terminal eps enhanced color font 'palatino,11'
set output 'datatypestats.eps'
#set pointsize 2
set boxwidth 1
set grid
set style fill solid 1.0 border -1
set xrange[-.5:*]
set yrange[0:*]
set ylabel 'Count'
set xlabel 'Data type'
set key font "palatino,11"
set xtics border in scale 0,10 nomirror rotate by -45 font "palatino,11" noenhanced
plot 'datatypestats.dat' u ($0):2:(50+$0):xticlabels(1) w boxes lc variable notitle,\
     'datatypestats.dat' u ($0):2:2 with labels offset 0,0.8 notitle
