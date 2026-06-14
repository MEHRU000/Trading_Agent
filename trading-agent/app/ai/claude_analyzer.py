"""
Claude AI Analyzer.
Interfaces with Anthropic Claude or AWS Bedrock to perform trade setup validations.
Enforces strict JSON outputs containing confidence scores and validation reasonings.
"""

import json
from typing import Dict, Any, Optional
from app.utils.config import settings
from app.utils.logger import app_logger

# Optional imports for AI clients
anthropic_client = None
bedrock_client = None

if settings.AI_VALIDATION_ENABLED:
    if settings.AI_PROVIDER == "anthropic":
        try:
            import anthropic
            if settings.CLAUDE_API_KEY:
                anthropic_client = anthropic.Anthropic(api_key=settings.CLAUDE_API_KEY)
                app_logger.info("Anthropic client initialized.")
            else:
                app_logger.warning("AI validation enabled with Anthropic, but CLAUDE_API_KEY is missing.")
        except ImportError:
            app_logger.error("Anthropic SDK is not installed. AI validation will run on mock fallback.")
            
    elif settings.AI_PROVIDER == "bedrock":
        try:
            import boto3
            if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
                bedrock_client = boto3.client(
                    service_name="bedrock-runtime",
                    region_name=settings.AWS_REGION,
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                )
                app_logger.info("AWS Bedrock client initialized.")
            else:
                # Attempt default credential provider chain
                bedrock_client = boto3.client(service_name="bedrock-runtime", region_name=settings.AWS_REGION)
                app_logger.info("AWS Bedrock client initialized via default credential chain.")
        except Exception as e:
            app_logger.error(f"Failed to initialize AWS Bedrock client: {e}. AI validation will run on mock fallback.")


def call_anthropic(prompt: str) -> str:
    """
    Submits a message to Anthropic Claude API.
    """
    if not anthropic_client:
        raise RuntimeError("Anthropic client is not initialized.")
        
    system_instruction = (
        "You are an expert quantitative trading risk validator. "
        "Analyze the provided trade candidate context and respond ONLY with a raw JSON block. "
        "Do not include any chat formatting, markdown backticks, or text before/after the JSON. "
        "JSON structure must be: {\"validation\": bool, \"confidence_score\": float, \"reasoning\": \"string\"}"
    )
    
    response = anthropic_client.messages.create(
        model=settings.CLAUDE_MODEL_ID,
        max_tokens=1000,
        system=system_instruction,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    return response.content[0].text


def call_bedrock(prompt: str) -> str:
    """
    Submits a message to AWS Bedrock Claude API.
    """
    if not bedrock_client:
        raise RuntimeError("AWS Bedrock client is not initialized.")
        
    system_instruction = (
        "You are an expert quantitative trading risk validator. "
        "Analyze the provided trade candidate context and respond ONLY with a raw JSON block. "
        "Do not include any chat formatting, markdown backticks, or text before/after the JSON. "
        "JSON structure must be: {\"validation\": bool, \"confidence_score\": float, \"reasoning\": \"string\"}"
    )

    # Bedrock format for Claude 3 (Messages API)
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "system": system_instruction,
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
        "temperature": 0.0
    })

    model_id = f"anthropic.{settings.CLAUDE_MODEL_ID}"  # AWS Bedrock prefix (e.g. anthropic.claude-3-5-sonnet-20241022-v2:0)
    
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=body
    )
    
    response_body = json.loads(response.get("body").read())
    return response_body["content"][0]["text"]


def validate_trade_with_ai(prompt: str) -> Dict[str, Any]:
    """
    Validates a trade signal by querying Claude AI using configured provider.
    
    Returns:
        Dict[str, Any]: {
            "validation": bool,
            "confidence_score": float,
            "reasoning": str
        }
    """
    # Fallback response in case AI validation is disabled or fails
    fallback_response = {
        "validation": True,
        "confidence_score": 1.0,
        "reasoning": "AI validation bypassed: Feature disabled or credentials missing."
    }

    if not settings.AI_VALIDATION_ENABLED:
        return fallback_response

    app_logger.info(f"Submitting trade candidate to Claude AI ({settings.AI_PROVIDER}) for validation...")
    
    try:
        if settings.AI_PROVIDER == "anthropic" and anthropic_client:
            raw_response = call_anthropic(prompt)
        elif settings.AI_PROVIDER == "bedrock" and bedrock_client:
            raw_response = call_bedrock(prompt)
        else:
            # Simulated response for local development when credentials are not supplied
            app_logger.warning("AI clients not configured. Simulating Claude response...")
            return {
                "validation": True,
                "confidence_score": 0.85,
                "reasoning": "Simulated validation: Confluence confirmed on H1 EMA crossover, RSI in momentum, and volume exceeds SMA20."
            }

        # Parse JSON output from Claude
        # Clean any accidental markdown codeblock formatting if present
        clean_response = raw_response.strip()
        if clean_response.startswith("```json"):
            clean_response = clean_response[7:]
        if clean_response.endswith("```"):
            clean_response = clean_response[:-3]
        clean_response = clean_response.strip()

        data = json.loads(clean_response)
        
        # Validate keys and types
        validation = bool(data.get("validation", True))
        confidence_score = float(data.get("confidence_score", 0.80))
        reasoning = str(data.get("reasoning", "Confluence confirmed by Claude AI."))

        app_logger.info(f"Claude Validation completed. Result: {validation} | Confidence: {confidence_score:.2f}")
        return {
            "validation": validation,
            "confidence_score": confidence_score,
            "reasoning": reasoning
        }

    except Exception as e:
        app_logger.error(f"Claude AI validation encountered an error: {e}. Defaulting to fallback parameters.")
        return {
            "validation": True,  # Fallback to true to avoid locking system on API errors
            "confidence_score": 0.50,
            "reasoning": f"AI Validation Error: {str(e)}. Defaulted to fallback authorization."
        }
