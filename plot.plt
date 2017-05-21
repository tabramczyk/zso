set terminal png size 800,600

# tym trzeba kombinowac zaleznie od zbieznosci
set xrange[3:3000]
set yrange [:700]

#
set out  "img/zakharov-best_fitness-_speed=1_zombies=5.png"
set xl "iteration"
set yl "value"

plot for [i=1:30] 'out/zakharov_speed=1_zombies=5_call='.i.'.dat' using 1:2 with lines lw 2 title 'best fitness '.i

# tym tez trzeba kombinowac zaleznie od zbieznosci
set xrange[:50]
set yrange [:5]
#
set out  "img/zakharov-humans_number-_speed=1_zombies=5.png"
set xl "iteration"
set yl "value"

plot for [i=1:30] 'out/zakharov_speed=1_zombies=5_call='.i.'.dat' using 1:4 with lines lw 3 title 'humans number '.i
