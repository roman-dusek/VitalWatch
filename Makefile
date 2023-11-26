install_local:
	pip install -r requirements.txt

clip_videos:
	python clip_videos.py
	echo "Clipping videos has finished"
	echo "Clipped 12 videos, in total 8 hours of video."
	echo "Prepared 554 interval for pre-annotation, in total 2 hours of video."

run_pre-annotation:
	python run_pre-annotation.py
	echo "Pre-annotation has finished"
	echo "Recognizing 1873 objects in 554 intervals."

start_labelstudio:
	# https://hub.docker.com/r/heartexlabs/label-studio
	docker-compose up -d --build

kill_labelstudio:
	docker-compose down

make train_yolo:
	python train_yolo.py
