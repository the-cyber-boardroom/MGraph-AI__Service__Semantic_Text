#!/bin/bash
export PORT=10021
uvicorn mgraph_ai_service_semantic_text.fast_api.lambda_handler:app --reload --host 0.0.0.0 --port $PORT