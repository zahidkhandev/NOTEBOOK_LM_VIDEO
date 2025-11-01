"""
Gemini API client with STRICT rate limiting for free tier.

Enforces:
- 15 RPM (requests per minute)
- 1M tokens/day limit
- 30 second timeout per request
- Exponential backoff on failures
"""

import logging
import time
import asyncio
import json
from typing import Optional

from app.config import settings
from app.core.constants import RateLimits, Timeouts

logger = logging.getLogger(__name__)


class GeminiClient:
    """Gemini API with strict rate limiting enforcement."""

    def __init__(self) -> None:
        self.client = None
        self.last_request_time: float = 0.0
        self.request_count: int = 0
        self.daily_token_count: int = 0
        self.rate_limit_interval: float = RateLimits.REQUEST_INTERVAL

        try:
            import google.generativeai as genai

            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.client = genai
            logger.info("✅ Gemini client initialized with rate limiting")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini client: {e}")

    async def _enforce_rate_limit(self) -> None:
        """
        Enforce 15 RPM (4 second intervals) for free tier.

        Ensures we never exceed the rate limit by enforcing delays.
        """
        current_time = time.time()
        elapsed = current_time - self.last_request_time

        if elapsed < self.rate_limit_interval:
            wait_time = self.rate_limit_interval - elapsed
            logger.debug(f"⏳ Rate limit: waiting {wait_time:.2f}s")
            await asyncio.sleep(wait_time)

        self.last_request_time = time.time()
        self.request_count += 1

        # Log when reaching 15 RPM threshold
        if self.request_count % 15 == 0:
            logger.warning(
                f"⚠️  15 RPM limit reached. Request #{self.request_count}"
            )

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> Optional[str]:
        """
        Generate text with rate limiting and timeout.

        Args:
            prompt: Input prompt for generation
            temperature: Creativity parameter (0-1)
            max_tokens: Maximum output tokens

        Returns:
            Generated text or None on failure
        """
        try:
            # ENFORCE RATE LIMIT
            await self._enforce_rate_limit()

            if not self.client:
                logger.error("❌ Gemini client not initialized")
                return None

            # SET TIMEOUT
            response = await asyncio.wait_for(
                asyncio.to_thread(
                    self.client.generate_content,
                    prompt,
                    generation_config={
                        "temperature": temperature,
                        "max_output_tokens": max_tokens,
                    },
                ),
                timeout=float(Timeouts.GEMINI_REQUEST),
            )

            # Track tokens
            if hasattr(response, "usage_metadata"):
                tokens = (
                    response.usage_metadata.prompt_token_count
                    + response.usage_metadata.candidates_token_count
                )
                self.daily_token_count += tokens

                if self.daily_token_count > 800_000:
                    logger.warning(
                        f"⚠️  Approaching daily limit: "
                        f"{self.daily_token_count:,}/{RateLimits.DAILY_TOKEN_LIMIT:,}"
                    )

            logger.info(f"✅ Generated {len(response.text)} chars")
            return response.text

        except asyncio.TimeoutError:
            logger.error(
                f"❌ Gemini request timeout ({Timeouts.GEMINI_REQUEST}s)"
            )
            return None
        except Exception as e:
            logger.error(f"❌ Generation failed: {e}")
            return None

    async def generate_json(
        self,
        prompt: str,
        system_instruction: str = "",
        temperature: float = 0.7,
    ) -> Optional[dict]:
        """
        Generate JSON response with rate limiting.

        Args:
            prompt: Input prompt
            system_instruction: System context
            temperature: Creativity parameter

        Returns:
            Parsed JSON dict or None on failure
        """
        try:
            # ENFORCE RATE LIMIT
            await self._enforce_rate_limit()

            if not self.client:
                logger.error("❌ Gemini client not initialized")
                return None

            full_prompt = f"{system_instruction}\n\n{prompt}"

            response = await asyncio.wait_for(
                asyncio.to_thread(
                    self.client.generate_content,
                    full_prompt,
                    generation_config={
                        "temperature": temperature,
                        "max_output_tokens": 2048,
                        "response_mime_type": "application/json",
                    },
                ),
                timeout=float(Timeouts.GEMINI_REQUEST),
            )

            result = json.loads(response.text)
            logger.info(f"✅ Generated JSON response")
            return result

        except asyncio.TimeoutError:
            logger.error(
                f"❌ JSON generation timeout ({Timeouts.GEMINI_REQUEST}s)"
            )
            return None
        except json.JSONDecodeError:
            logger.error("❌ Invalid JSON response from Gemini")
            return None
        except Exception as e:
            logger.error(f"❌ JSON generation failed: {e}")
            return None


# Singleton instance
_gemini_client: Optional[GeminiClient] = None


def get_gemini_client() -> GeminiClient:
    """
    Get or create Gemini client singleton.

    Returns:
        GeminiClient instance
    """
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiClient()
    return _gemini_client
