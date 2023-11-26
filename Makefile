install_local:
	pip install -r requirements.txt

clip_videos:
	python clip_videos.py

run_pre-annotation:
	python run_pre-annotation.py

start_labelstudio:
	# https://hub.docker.com/r/heartexlabs/label-studio
	docker-compose up -d --build

kill_labelstudio:
	docker-compose down

