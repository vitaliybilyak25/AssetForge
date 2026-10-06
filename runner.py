"""AssetForge runner — demonstrates ADK Runner and Session usage.

Instantiates OrchestratorAgent, wires it to an ADK Runner with an InMemorySessionService,
and executes a single-asset processing run with a placeholder asset path.

Usage:
    python runner.py
"""

import asyncio
import logging
import os

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from assetforge.agents.orchestrator_agent import OrchestratorAgent

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

APP_NAME = "assetforge"
USER_ID = "system"
PLACEHOLDER_ASSET = "/tmp/placeholder_asset.jpg"
PLACEHOLDER_PROFILE = "stock/adobe-stock"


async def main() -> None:
    """Run a single-asset demonstration of the AssetForge pipeline."""

    # 1. Instantiate the OrchestratorAgent.
    orchestrator = OrchestratorAgent()

    # 2. Create an ADK InMemorySessionService and Runner.
    session_service = InMemorySessionService()
    runner = Runner(  # noqa: F841 — kept to demonstrate ADK wiring
        agent=orchestrator,
        session_service=session_service,
        app_name=APP_NAME,
    )
    logger.info("ADK Runner created with app_name=%s", APP_NAME)

    # 3. Create an ADK session for this run (async as of google-adk 1.22.x).
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    logger.info("ADK session created: session_id=%s", session.id)

    # 4. Execute the AssetForge pipeline using OrchestratorAgent.run().
    #    The stub agents return typed placeholder instances — no Gemini API calls are made.
    output_package = orchestrator.run(
        asset_path=PLACEHOLDER_ASSET,
        profile_id=PLACEHOLDER_PROFILE,
    )
    logger.info(
        "Pipeline complete. OutputPackage: filename=%r title=%r profile_id=%r",
        output_package.filename,
        output_package.title,
        output_package.profile_id,
    )
    logger.info("runner.py completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())
