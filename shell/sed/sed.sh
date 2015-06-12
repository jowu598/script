target=`echo $1 | sed 's/\./\_/g'`
echo $target
[ $(echo $1 | egrep '*.cpp$') ] && echo 'g++ $1 -o $target';g++ $1 -o $target
[ $(echo $1 | egrep '*.c$') ] && echo 'gcc $1 -o $target';gcc $1 -o $target
