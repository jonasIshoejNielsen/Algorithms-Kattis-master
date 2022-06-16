#python3 PrintTable.py >> output.txt

for file in data/*.txt

do 
    base=${file%.txt}
    var1="$base"
    var2=$(python3 run.py < $file)
    echo "$var1$var2\\\\" >> output2.txt 
    #echo "../"$base"" >> output.txt 
    #python3 run.py < $file >> output.txt 
    #echo "" >> output.txt 
    
done
