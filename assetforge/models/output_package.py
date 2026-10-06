"""OutputPackage — the single output artifact of the Channel Adaptation Layer.

The Output Package is the only artifact AssetForge delivers at the outbound Integration
Touch-point.  It is a complete, channel-ready, formatted, and validated metadata artifact
as defined in docs/boundary-contracts.md (Layer 3 Output Artifact section).
"""

from dataclasses import dataclass, field


@dataclass
class OutputPackage:
    """Channel-ready metadata artifact produced by the Channel Adaptation Layer (Layer 3 output).

    Fields reflect the Adobe Stock CSV column structure used as the first concrete profile
    (stock/adobe-stock).  All field names and types are authoritative as of story #102;
    Layer 3 implementation stories will populate them with validated content.
    """

    # Name of the source asset file, carried through from the inbound submission.
    filename: str = ""

    # Generated title conforming to the active Content Profile's Length Limits.
    title: str = ""

    # Comma-separated keyword list conforming to the active Content Profile's Keyword Rules.
    keywords: str = ""

    # Numeric category code for the destination channel (e.g., Adobe Stock category integer).
    category: int = 0

    # Release documentation reference(s) required by the destination channel.
    releases: str = ""

    # Profile Identifier used to generate this package (e.g., "stock/adobe-stock").
    profile_id: str = ""

    # Version identifier of the prompt template used during content generation.
    prompt_version: str = ""
