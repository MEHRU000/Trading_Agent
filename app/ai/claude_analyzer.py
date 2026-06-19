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


def generate_ai_text(system_prompt: str, user_prompt: str) -> str:
    """
    Unified AI text generator. Tries Gemini, OpenAI, Claude, or Bedrock depending on settings,
    with a mock fallback if no keys are configured.
    """
    import urllib.request
    
    # 1. Try Gemini
    if settings.GEMINI_API_KEY and not settings.GEMINI_API_KEY.startswith("placeholder") and len(settings.GEMINI_API_KEY) > 15:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
            payload = {
                "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
                "systemInstruction": {"parts": [{"text": system_prompt}]},
                "generationConfig": {"temperature": 0.2, "maxOutputTokens": 1000}
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=12) as response:
                res_json = json.loads(response.read().decode("utf-8"))
                return res_json["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            app_logger.error(f"Unified AI: Gemini call failed: {e}")

    # 2. Try OpenAI
    if settings.OPENAI_API_KEY and not settings.OPENAI_API_KEY.startswith("sk-proj-testkey") and len(settings.OPENAI_API_KEY) > 15:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.2,
                "max_tokens": 1000
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {settings.OPENAI_API_KEY}"
                }
            )
            with urllib.request.urlopen(req, timeout=12) as response:
                res_json = json.loads(response.read().decode("utf-8"))
                return res_json["choices"][0]["message"]["content"]
        except Exception as e:
            app_logger.error(f"Unified AI: OpenAI call failed: {e}")

    # 3. Try Claude / Bedrock
    if settings.AI_VALIDATION_ENABLED or (settings.CLAUDE_API_KEY and len(settings.CLAUDE_API_KEY) > 15):
        try:
            if settings.AI_PROVIDER == "anthropic" and anthropic_client:
                response = anthropic_client.messages.create(
                    model=settings.CLAUDE_MODEL_ID,
                    max_tokens=1000,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}],
                    temperature=0.2
                )
                return response.content[0].text
            elif settings.AI_PROVIDER == "bedrock" and bedrock_client:
                body = json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1000,
                    "system": system_prompt,
                    "messages": [{"role": "user", "content": [{"type": "text", "text": user_prompt}]}],
                    "temperature": 0.2
                })
                model_id = f"anthropic.{settings.CLAUDE_MODEL_ID}"
                response = bedrock_client.invoke_model(modelId=model_id, body=body)
                response_body = json.loads(response.get("body").read())
                return response_body["content"][0]["text"]
        except Exception as e:
            app_logger.error(f"Unified AI: Claude/Bedrock call failed: {e}")

    # 4. Fallback/Mock Responses
    user_prompt_lower = user_prompt.lower()
    if "coach" in user_prompt_lower or "psychology" in user_prompt_lower or "evaluat" in user_prompt_lower:
        return json.dumps({
            "won_lost_reason": "The trade won due to strong momentum confluence. The entry was aligned with the H1 EMA crossover and a positive breakout of the key resistance level at 2320.50.",
            "mistakes": "Slight entry delay of 1.5 pips. Although the trade was successful, executing closer to the crossover alert would improve the risk-to-reward ratio.",
            "strengths": "Disciplined risk management. Stop loss was set correctly at 1% of balance, and the profit target was held patiently without manual exit panic.",
            "risk_observations": "Spread was slightly wide (32 points) at execution, which increased initial slippage slightly but remained within whitelisted boundaries.",
            "improvements": "Consider adjusting order execution rules to execute limit orders at key support retests rather than market buying during high-momentum breakouts."
        })
    elif "outlook" in user_prompt_lower or "brief" in user_prompt_lower or "outlook" in system_prompt.lower():
        return (
            "### AI Market Intelligence Outlook\n\n"
            "**Market Context:** Gold (XAUUSD) has stabilized around $2,325 after a brief test of the support at $2,310. "
            "Technical structures indicate consolidation on the H1 timeframe, with price hovering between the 20 EMA and 50 EMA.\n\n"
            "**Economic News Drivers:** The upcoming US Retail Sales and Philly Fed Manufacturing index releases represent the main market volatility drivers. "
            "Low-impact news across EUR/GBP has minimal effect, but USD strength index (DXY) shows neutral structure.\n\n"
            "**Tactical Recommendation:** Hold positions until a clear structural breakout of the $2,332 resistance or $2,315 support occurs. "
            "The AI Trade Committee score sits at a neutral 58/100."
        )
    else:
        return "Local simulated AI response. Please configure active API credentials in the settings panel to activate real LLM analytics."

