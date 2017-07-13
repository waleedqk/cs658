default: git

clean:
	find . -type f -name '*~' -delete

pull:
	git pull --all

push: 
	git add *
	git commit -m "Commit"
	git push origin master	

git: clean push

