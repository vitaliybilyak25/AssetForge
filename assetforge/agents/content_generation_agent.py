"""ContentGenerationAgent — Layer 2: Content Generation.

Receives a Canonical Asset Record and a resolved Content Profile (identified by profile_id)
and produces Generated Content: human-readable text fields (Title, Keywords, Description,
Caption) conforming to the active Content Profile's rules.

Layer responsibility: produce Generated Content only.
Prohibited: analysing the raw asset, modifying the CAR, applying Output Format rules,
executing Validation Rules, or inferring content for absent/below-threshold CAR fields
(see docs/boundary-contracts.md).
"""

import logging
from typing import Any

from google.adk.agents import Agent

from assetforge.models.canonical_asset_record import CanonicalAssetRecord

logger = logging.getLogger(__name__)


class ContentGenerationAgent(Agent):
    """Layer 2 — Content Generation: transforms a CAR into Generated Content using a Content Profile.

    This agent reads the Canonical Asset Record produced by Layer 1 and the resolved
    Content Profile identified by ``profile_id`` to generate human-readable metadata fields
    (Title, Keywords, Description, Caption).  It applies the Content Profile's Audience,
    Tone, Length Limits, Keyword Rules, Forbidden Content, and Language dimensions.

    All Gemini prompt execution and business logic are deferred to the Layer 2 implementation
    story.  This class is a typed scaffold stub only.
    """

    def __init__(self) -> None:
        super().__init__(
            name="content_generation_agent",
            model="gemini-2.0-flash",
            description=(
                "Layer 2 — Content Generation: reads a CAR and a Content Profile and produces "
                "human-readable metadata fields (title, keywords, description, caption)."
            ),
            instruction=(
                "Given a Canonical Asset Record and a resolved Content Profile, generate "
                "the required metadata fields conforming to the profile's rules. Do not "
                "modify the CAR, apply output format structure, or execute validation rules."
            ),
        )

    def process(self, car: CanonicalAssetRecord, profile_id: str) -> dict[str, Any]:
        """Generate human-readable content fields from a CAR and Content Profile.

        Args:
            car: Sealed CanonicalAssetRecord produced by the Asset Intelligence Layer.
            profile_id: Identifier of the active Content Profile (e.g., "stock/adobe-stock").

        Returns:
            A dict of plain-text content fields (title, keywords, description, etc.)
            conforming to the active Content Profile's rules.
            Stub implementation returns a placeholder dict with empty string values.
        """
        logger.info(
            "ContentGenerationAgent.process called with profile_id=%s", profile_id
        )
        # Stub: real Gemini prompt execution deferred to Layer 2 implementation story.
        return {
            "title": "",
            "keywords": "",
            "description": "",
            "caption": "",
            "profile_id": profile_id,
        }
