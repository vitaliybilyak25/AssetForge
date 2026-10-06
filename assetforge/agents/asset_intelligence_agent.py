"""AssetIntelligenceAgent — Layer 1: Asset Intelligence.

Receives a raw asset file path, analyses the asset without any knowledge of the intended
channel, and produces a Canonical Asset Record (CAR).  The CAR is a sealed, channel-agnostic
record of factual observations organised into seven categories (Objects, People, Activities,
Locations, Text/Logos, Confidence Scores, Risk Flags).

Layer responsibility: produce the CAR only.
Prohibited: reading the Content Profile, generating titles/descriptions/keywords, making
channel or distribution decisions (see docs/boundary-contracts.md).
"""

import logging

from google.adk.agents import Agent

from assetforge.models.canonical_asset_record import CanonicalAssetRecord

logger = logging.getLogger(__name__)


class AssetIntelligenceAgent(Agent):
    """Layer 1 — Asset Intelligence: analyses a raw asset and produces a CanonicalAssetRecord.

    This agent is the sole producer of the Canonical Asset Record.  It receives an asset
    file path and a pass-through Profile Identifier (which it must not read or act on) and
    returns a CAR populated with neutral, factual, channel-agnostic observations.

    All Gemini vision API calls and business logic are deferred to the Layer 1 implementation
    story.  This class is a typed scaffold stub only.
    """

    def __init__(self) -> None:
        super().__init__(
            name="asset_intelligence_agent",
            model="gemini-2.0-flash",
            description=(
                "Layer 1 — Asset Intelligence: analyses a raw asset file and produces a "
                "Canonical Asset Record (CAR) containing channel-agnostic factual observations."
            ),
            instruction=(
                "Analyse the provided asset and record neutral, factual observations across "
                "the seven CAR categories: objects, persons, activities, location, text, "
                "confidence, and risk. Do not generate titles, descriptions, or keywords. "
                "Do not read or act on the Content Profile."
            ),
        )

    def process(self, asset_path: str) -> CanonicalAssetRecord:
        """Analyse a raw asset and return a CanonicalAssetRecord.

        Args:
            asset_path: Absolute or relative file system path to the raw asset file.

        Returns:
            A CanonicalAssetRecord populated with factual observations about the asset.
            Stub implementation returns a placeholder record with empty category dicts.
        """
        logger.info("AssetIntelligenceAgent.process called for asset: %s", asset_path)
        # Stub: real Gemini vision analysis deferred to Layer 1 implementation story.
        return CanonicalAssetRecord(
            objects={},
            persons={},
            activities={},
            location={},
            text={},
            confidence={},
            risk={"flags_evaluated": False},
        )
