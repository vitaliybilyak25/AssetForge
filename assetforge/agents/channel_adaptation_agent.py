"""ChannelAdaptationAgent — Layer 3: Channel Adaptation.

Receives Generated Content (dict of plain-text fields from Layer 2) and a profile_id,
applies the Output Format and Validation Rules from the active Content Profile, and
produces a validated, channel-ready OutputPackage.

Layer responsibility: format and validate only.
Prohibited: generating any content field, altering meaning of Generated Content,
reading the raw asset or the CAR, applying content-generation rules
(see docs/boundary-contracts.md).
"""

import logging

from google.adk.agents import Agent

from assetforge.models.output_package import OutputPackage

logger = logging.getLogger(__name__)


class ChannelAdaptationAgent(Agent):
    """Layer 3 — Channel Adaptation: formats and validates Generated Content into an OutputPackage.

    This agent reads the Generated Content produced by Layer 2 and the Output Format plus
    Validation Rules dimensions of the resolved Content Profile identified by ``profile_id``.
    It validates each generated field against the Validation Rules and formats the validated
    fields into the channel-ready Output Format specified by the profile.

    All CSV/JSON formatting and validation logic are deferred to the Layer 3 implementation
    story.  This class is a typed scaffold stub only.
    """

    def __init__(self) -> None:
        super().__init__(
            name="channel_adaptation_agent",
            model="gemini-2.0-flash",
            description=(
                "Layer 3 — Channel Adaptation: validates Generated Content against a Content "
                "Profile's Validation Rules and formats it into a channel-ready OutputPackage."
            ),
            instruction=(
                "Given Generated Content and a Content Profile identifier, validate every "
                "field against the profile's Validation Rules and format the validated fields "
                "into the Output Format specified by the profile. Do not generate new content."
            ),
        )

    def process(self, content: dict, profile_id: str) -> OutputPackage:
        """Format and validate Generated Content into a channel-ready OutputPackage.

        Args:
            content: Dict of plain-text fields produced by the Content Generation Layer.
                     Keys include at minimum: title, keywords, description, profile_id.
            profile_id: Identifier of the active Content Profile (e.g., "stock/adobe-stock").

        Returns:
            A validated, channel-ready OutputPackage.
            Stub implementation returns a placeholder OutputPackage with empty/zero values.
        """
        logger.info(
            "ChannelAdaptationAgent.process called with profile_id=%s", profile_id
        )
        # Stub: real validation and formatting deferred to Layer 3 implementation story.
        return OutputPackage(
            filename="",
            title=content.get("title", ""),
            keywords=content.get("keywords", ""),
            category=0,
            releases="",
            profile_id=profile_id,
            prompt_version="",
        )
