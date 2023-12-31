FUNCTION_NAME=deepdanbooru
REGION=us-east1
USEROUTPUT=false

deploy:
	gcloud functions deploy $(FUNCTION_NAME) \
		--gen2 \
		--runtime python311 \
		--memory 2560MiB \
		--timeout 15s \
		--region $(REGION) \
		--source=. \
		--entry-point detect \
		--trigger-http \
		--user-output-enabled=$(USEROUTPUT)

delete:
	gcloud functions delete $(FUNCTION_NAME) --region $(REGION)
