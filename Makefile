.PHONY: deploy
deploy:
	gcloud app deploy app.yaml cron.yaml
