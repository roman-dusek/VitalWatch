start_labelstudio:
	# https://hub.docker.com/r/heartexlabs/label-studio
	docker pull heartexlabs/label-studio:latest
	docker run -it \
		-p 8080:8080 \
		-v `pwd`/labelstudio-data:/label-studio/data \
		--env LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true \
		--env LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/label-studio/images \
		-v `pwd`/images:/label-studio/images \
		heartexlabs/label-studio:latest label-studio
