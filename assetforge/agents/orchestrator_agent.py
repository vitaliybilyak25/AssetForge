"""OrchestratorAgent — coordinates the three AssetForge layer agents.

Accepts an asset file path and a profile identifier, calls the three layer agents in
the sequence mandated by docs/data-flow.md (Layer 1 → Layer 2 → Layer 3), and returns
the final OutputPackage.

Architecture rule: layer agents must not call each other directly.  All inter-layer
coordination flows exclusively through this OrchestratorAgent.
"""

import logging

from google.adk.agents import Agent
from pydantic import PrivateAttr

from assetforge.agents.asset_intelligence_agent import AssetIntelligenceAgent
from assetforge.agents.content_generation_agent import ContentGenerationAgent
from assetforge.agents.channel_adaptation_agent import ChannelAdaptationAgent
from assetforge.models.canonical_asset_record import CanonicalAssetRecord
from assetforge.models.output_package import OutputPackage

logger = logging.getLogger(__name__)


class OrchestratorAgent(Agent):
    """Orchestrator: drives the three-layer AssetForge pipeline for a single asset run.

    Accepts a raw asset path and a Content Profile identifier, then:
      1. Delegates to AssetIntelligenceAgent (Layer 1) to produce a CanonicalAssetRecord.
      2. Delegates to ContentGenerationAgent (Layer 2) with the CAR and profile_id to
         produce Generated Content (dict).
      3. Delegates to ChannelAdaptationAgent (Layer 3) with the Generated Content and
         profile_id to produce the final OutputPackage.

    No layer agent calls any other layer agent directly; all coordination flows here.
    """

    # PrivateAttr keeps typed refs to the sub-agents without Pydantic wiping them.
    _layer1: AssetIntelligenceAgent = PrivateAttr()
    _layer2: ContentGenerationAgent = PrivateAttr()
    _layer3: ChannelAdaptationAgent = PrivateAttr()

    def __init__(self) -> None:
        layer1 = AssetIntelligenceAgent()
        layer2 = ContentGenerationAgent()
        layer3 = ChannelAdaptationAgent()
        super().__init__(
            name="orchestrator_agent",
            model="gemini-2.0-flash",
            description=(
                "Orchestrator: coordinates AssetIntelligenceAgent, ContentGenerationAgent, "
                "and ChannelAdaptationAgent in sequence to process a single asset."
            ),
            instruction=(
                "You are the AssetForge orchestrator. Coordinate the three-layer pipeline: "
                "first call the Asset Intelligence Agent to analyse the asset, then call the "
                "Content Generation Agent with the resulting CAR and profile, then call the "
                "Channel Adaptation Agent to produce the final Output Package."
            ),
            sub_agents=[layer1, layer2, layer3],
        )
        # Assign after super().__init__() so Pydantic does not wipe the values.
        self._layer1 = layer1
        self._layer2 = layer2
        self._layer3 = layer3

    def run(self, asset_path: str, profile_id: str) -> OutputPackage:
        """Execute the full three-layer pipeline for one asset.

        Step 1 — Layer 1: AssetIntelligenceAgent analyses the raw asset → CanonicalAssetRecord
        Step 2 — Layer 2: ContentGenerationAgent reads CAR + profile → Generated Content (dict)
        Step 3 — Layer 3: ChannelAdaptationAgent validates + formats → OutputPackage

        Args:
            asset_path: File system path to the raw asset file submitted by the user.
            profile_id: Content Profile identifier (e.g., "stock/adobe-stock").

        Returns:
            A validated, channel-ready OutputPackage, the sole artifact delivered at the
            platform's outbound Integration Touch-point.
        """
        logger.info(
            "OrchestratorAgent.run: asset=%s profile=%s", asset_path, profile_id
        )

        # Step 1 — Layer 1: Asset Intelligence
        car: CanonicalAssetRecord = self._layer1.process(asset_path)
        logger.debug("Layer 1 complete: CAR produced")

        # Step 2 — Layer 2: Content Generation (CAR + profile → Generated Content)
        generated_content: dict = self._layer2.process(car, profile_id)
        logger.debug("Layer 2 complete: Generated Content produced")

        # Step 3 — Layer 3: Channel Adaptation (Generated Content + profile → OutputPackage)
        output_package: OutputPackage = self._layer3.process(generated_content, profile_id)
        logger.debug("Layer 3 complete: OutputPackage produced")

        return output_package
