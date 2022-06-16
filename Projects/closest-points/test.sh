rm output.txt 

for file in data/*-tsp.txt

do 
    base=${file%-tsp.txt}
    echo "../"$base".tsp" >> output.txt 
    python3 solution.py < $file >> output.txt 
    
done

sed -i ':a;N;$!ba;s/tsp\n/tsp: /g' output.txt
sed -i ':a;N;$!ba;s/.0\n/\n/g' output.txt
diff output.txt data/closest-pair-out.txt