echo $1
convert -size 1010x85 xc:transparent -font meiryo.ttc -pointsize 82 -fill black -draw "text 30,65 '${1}'" images/convert.png
