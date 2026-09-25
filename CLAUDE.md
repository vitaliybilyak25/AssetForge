# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Status

AssetForge is currently at **MVP0** — product vision and domain model stage. The codebase is being built from scratch. The primary reference is `Reqs/AssetForge_vision_01.docx`.

## What AssetForge Is

An AI-powered visual content metadata platform. Core value proposition: one visual asset → many accurate, channel-specific metadata packages.

Users upload photos/videos/vectors; the platform generates titles, descriptions, keywords, and structured metadata tailored to each distribution destination (stock marketplaces, social media, e-commerce, DAM systems, portfolios).

## Planned Modules

- **StockForge** — Stock marketplace metadata (iStock, Shutterstock, Adobe Stock, Alamy)
- **SocialForge** — Social media captions and hashtags
- **PortfolioForge** — Portfolio/website metadata
- **CommerceForge** — E-commerce product content
- **ArchiveForge** — DAM and personal archive metadata

## Core Architecture (3 Layers)

The critical architectural principle: **asset understanding, content generation, and channel formatting are strictly separated**.

### Layer 1 — Asset Intelligence
Analyzes the raw asset and produces a **Canonical Asset Record** — a neutral, factual, channel-agnostic description of the asset (objects, people, locations, text/logos, activities, risk/compliance flags, confidence scores).

### Layer 2 — Content Generation
Takes the Canonical Asset Record + a **Content Profile** → generates descriptions, titles, captions, or keyword lists. Content Profiles are configurable definitions per destination: audience, tone, field requirements, length limits, keyword rules, forbidden content, language, output format, validation rules.

### Layer 3 — Channel Adaptation
Formats and validates generated content for a specific destination format (Shutterstock CSV, IPTC/XMP metadata, Instagram post, DAM schema, etc.).

## Planned Content Profile Structure

```
profiles/
├── stock/        — shutterstock, adobe-stock, istock-editorial, alamy
├── marketing/    — instagram, facebook, linkedin, newsletter
├── web/          — portfolio-page, seo-page, accessibility-alt-text
├── commerce/     — ecommerce-product, marketplace-listing
└── library/      — dam, personal-archive
```

## MVP Roadmap

| MVP | Focus |
|-----|-------|
| MVP0 | Product vision and domain model |
| MVP1 | Canonical Asset Record specification |
| MVP2 | StockForge / Adobe Stock profile (first business case) |
| MVP3 | General description and keyword profiles |
| MVP4 | Human review UI, versioning, audit trail |
| MVP5 | Local folder and batch workflows |
| MVP6 | Additional stock profiles (Shutterstock, iStock, Dreamstime) |
| MVP7 | Social and portfolio profiles |
| MVP8 | CommerceForge — E-commerce and marketplace profiles |
| MVP9 | DAM and archive profiles |
| MVP10 | Video and vector workflows |
| MVP11 | Agile development agent team |
| MVP12 | Enterprise deployment (auth, governance, observability, cost controls) |

## Key Design Decisions

- **Profile-driven, not hardcoded per-site** — a Content Profile is the central abstraction; adding a new channel means adding a new profile, not new code.
- **Stock marketplaces are the first use case, not the scope** — every architectural decision should support eventual expansion to all channel types.
- **Planned output formats:** CSV, JSON, IPTC/XMP, REST API, CMS integration, filesystem export.
- **Enterprise target:** MVP12 plans Gemini Enterprise Agent Platform deployment with secret management, governance, and observability.
