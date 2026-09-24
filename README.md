# AssetForge

> One visual asset, many descriptions and metadata packages.

AssetForge is an AI-powered visual content metadata platform. It transforms photos, videos, and vectors into accurate, channel-specific metadata packages — titles, descriptions, keywords, captions, and structured exports — tailored to any distribution destination.

Stock marketplaces are the first use case. The platform is designed to extend to any content channel.

---

## How it works

```
         ┌──────────────────────┐
         │  Photo / Video / Vector│
         └──────────┬───────────┘
                    │
                    ▼
      ┌─────────────────────────┐
      │  Asset Intelligence     │  ← What is in the asset?
      │  Layer                  │    What is factually known?
      └──────────┬──────────────┘    What should be flagged?
                 │
                 ▼
      ┌─────────────────────────┐
      │  Canonical Asset Record  │  ← Facts, objects, people,
      │                         │    locations, risk, confidence
      └──────────┬──────────────┘
                 │
    ┌────────────┼────────────┐
    ▼            ▼            ▼
 Stock        Social      Portfolio
 profile      profile     profile
 E-commerce   DAM         SEO
 Editorial    Accessibility  Custom
```

Three strictly separated layers:

1. **Asset Intelligence** — Neutral, factual analysis of the raw asset (objects, people, locations, text/logos, activities, risk/compliance flags, confidence scores). Produces a **Canonical Asset Record**.
2. **Content Generation** — Takes the Canonical Asset Record + a **Content Profile** and generates descriptions, titles, captions, or keyword lists for a specific purpose.
3. **Channel Adaptation** — Formats and validates the output for a specific destination (Shutterstock CSV, IPTC/XMP, Instagram post, DAM schema, etc.).

---

## Product modules

```
AssetForge
├── StockForge     — Stock marketplace metadata (iStock, Shutterstock, Adobe Stock, Alamy, …)
├── SocialForge    — Social media captions and hashtags
├── PortfolioForge — Personal portfolio and website metadata
├── CommerceForge  — E-commerce product content
└── ArchiveForge   — Digital asset management and personal archives
```

---

## Content profiles

Content Profiles are the central abstraction. Each profile defines audience, tone, required/optional fields, length limits, keyword rules, forbidden content, language, output format, validation rules, and approval requirements.

```
profiles/
├── stock/        — shutterstock, adobe-stock, istock-editorial, alamy, dreamstime, …
├── marketing/    — instagram, facebook, linkedin, newsletter, pinterest
├── web/          — portfolio-page, seo-page, accessibility-alt-text
├── commerce/     — ecommerce-product, marketplace-listing
└── library/      — dam, personal-archive
```

Adding a new channel means adding a new profile, not new code.

---

## Delivery formats

CSV · JSON · IPTC/XMP · REST API · CMS integration · Filesystem export

---

## MVP roadmap

| MVP | Focus |
|-----|-------|
| MVP0 | Product vision and domain model |
| MVP1 | Canonical Asset Record specification |
| MVP2 | StockForge — iStock editorial profile (first business case) |
| MVP3 | General description and keyword profiles |
| MVP4 | Human review UI, versioning, audit trail |
| MVP5 | Local folder and batch workflows |
| MVP6 | Additional stock profiles (Shutterstock, Adobe Stock, Dreamstime, Depositphotos, Alamy, Pond5, Pixta) |
| MVP7 | Social and portfolio profiles |
| MVP8 | DAM and archive profiles |
| MVP9 | Video and vector workflows |
| MVP10 | Agile development agent team |
| MVP11 | Enterprise deployment (Gemini Enterprise, auth, governance, observability, cost controls) |

---

## Status

**MVP0** — Product vision and domain model. No source code yet.
