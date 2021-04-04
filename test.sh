echo starting
scripts=/scripts/*.py
pwd
cd scripts
pwd
for script in *; do
	pwd
	echo $script
	python3 $script

done
echo finish
