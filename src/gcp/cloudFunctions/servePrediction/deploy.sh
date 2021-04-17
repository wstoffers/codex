#!/bin/bash
gcloud functions deploy servePrediction --region us-central1 --runtime python38 --memory=256MB --max-instances=1 --trigger-http --allow-unauthenticated
