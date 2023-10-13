FUNCTION_NAME=deepdanbooru
REGION=asia-southeast1

deploy:
	gcloud functions deploy $(FUNCTION_NAME) \
		--gen2 \
		--runtime python311 \
		--memory 2560MiB \
		--timeout 10s \
		--region $(REGION) \
		--source=. \
		--entry-point detect \
		--trigger-http \
		--allow-unauthenticated

delete:
	gcloud functions delete $(FUNCTION_NAME) --region $(REGION)
