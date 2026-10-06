"""Canonical Asset Record — the single output artifact of the Asset Intelligence Layer.

The CAR is a sealed, channel-agnostic record of neutral, factual observations about an
asset, organised into seven categories that match the CAR spec in docs/canonical-asset-record.md
and docs/car-field-catalogue.md.  It is immutable after production and must never contain
titles, descriptions, keywords, or any content shaped by a Content Profile.
"""

from dataclasses import dataclass, field


@dataclass
class CanonicalAssetRecord:
    """Immutable record of factual, channel-agnostic asset observations (Layer 1 output).

    Top-level fields correspond one-to-one with the seven CAR categories defined in
    docs/canonical-asset-record.md, Section 3.  Sub-field names follow the dot-notation
    convention from docs/car-field-catalogue.md (e.g., ``objects.detected_subjects``).

    All fields are typed ``dict`` at this scaffold stage.  MVP1 implementation stories
    will replace each ``dict`` with a dedicated sub-model once the field catalogue is
    finalised (story #78).
    """

    # Category 1 — Objects and Subjects
    # Fields: objects.detected_subjects, objects.primary_subject, objects.scene_type,
    #         objects.colour_palette, objects.brand_objects_detected,
    #         objects.foreground_elements, objects.background_elements,
    #         objects.confidence_score
    objects: dict = field(default_factory=dict)

    # Category 2 — People
    # Fields: persons.present, persons.count, persons.faces_detected,
    #         persons.age_range_signals, persons.group_composition,
    #         persons.activity_posture, persons.confidence_score
    persons: dict = field(default_factory=dict)

    # Category 3 — Activities
    # Fields: activities.detected_activities, activities.confidence_score
    activities: dict = field(default_factory=dict)

    # Category 4 — Locations
    # Fields: location.environment_type, location.setting_descriptor,
    #         location.gps_coordinates, location.gps_derived_region,
    #         location.visual_landmark, location.urban_rural_signal,
    #         location.confidence_score
    location: dict = field(default_factory=dict)

    # Category 5 — Text and Logos
    # Fields: text.detected_strings, text.logos_detected, text.confidence_score
    text: dict = field(default_factory=dict)

    # Category 6 — Confidence Scores (aggregate / cross-category summary)
    # Holds any top-level or cross-category confidence metadata not attached to
    # an individual category's own confidence_score field.
    confidence: dict = field(default_factory=dict)

    # Category 7 — Risk Flags
    # Fields: risk.flags_evaluated, risk.identifiable_person, risk.property_release,
    #         risk.adult_content, risk.violence, risk.editorial_only
    # Per CAR Consumer Rule 4, Risk Flags must be propagated regardless of confidence.
    risk: dict = field(default_factory=dict)
