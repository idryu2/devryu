"""규칙 엔진 테스트용 공용 픽스처."""
from __future__ import annotations

import pytest

from app.cdss.engine import RuleEngine
from app.cdss.loader import load_ruleset


@pytest.fixture(scope="session")
def engine() -> RuleEngine:
    """실제 JSON 규칙셋을 그대로 로드한 엔진."""
    return RuleEngine(load_ruleset())
