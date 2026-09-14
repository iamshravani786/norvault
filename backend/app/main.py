"""NORVAULT FastAPI application factory."""

from __future__ import annotations

import logging
from pathlib import Path
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import get_settings
from app.database import init_db, close_db

logger = logging.getLogger("norvault")

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application startup and shutdown lifecycle."""
    settings = get_settings()
    logging.basicConfig(level=getattr(logging, settings.log_level))
    logger.info("NORVAULT starting up — Every company fact comes with its proof.")

    await init_db()
    logger.info("Database initialized.")

    from app.adapters.registry import seed_default_sources
    await seed_default_sources()
    logger.info("Source registry seeded.")

    yield

    await close_db()
    logger.info("NORVAULT shut down.")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="NORVAULT",
        description=(
            "Competition-grade Norwegian company intelligence engine. "
            "Every company fact comes with its proof."
        ),
        version="1.0.0",
        lifespan=lifespan,
    )

    # CORS — wide-open for tunnel deployments
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API routes
    from app.api.routes import companies, evidence, benchmark, admin, health
    app.include_router(health.router, tags=["health"])
    app.include_router(companies.router, prefix="/api/v1", tags=["companies"])
    app.include_router(evidence.router, prefix="/api/v1", tags=["evidence"])
    app.include_router(benchmark.router, prefix="/api/v1", tags=["benchmark"])
    app.include_router(admin.router, prefix="/api/v1", tags=["admin"])

    # Serve frontend static files (if the build exists)
    if STATIC_DIR.exists() and (STATIC_DIR / "index.html").exists():
        # Mount assets directory for JS/CSS
        assets_dir = STATIC_DIR / "assets"
        if assets_dir.exists():
            app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

        # SPA catch-all: any non-API route serves index.html
        @app.get("/{full_path:path}")
        async def serve_spa(request: Request, full_path: str):
            # Try to serve the exact file first
            file_path = STATIC_DIR / full_path
            if full_path and file_path.exists() and file_path.is_file():
                return FileResponse(str(file_path))
            # Otherwise serve index.html for SPA routing
            return FileResponse(str(STATIC_DIR / "index.html"))

    return app


app = create_app()

