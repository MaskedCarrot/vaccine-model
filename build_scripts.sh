cd scripts
pwd
for script in *; do
	echo $script;
	python3 $script;
done

