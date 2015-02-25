echo "Categorizing the errors"

for line in $(cat "$logdir"/buginfo)
do
    echo line
    #cat "$line" | grep "\[\-W.*\]" -o
done

