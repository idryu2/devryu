import { describe, expect, it } from "vitest";

import { SEVERITY_STYLE, type Severity } from "./api";

describe("SEVERITY_STYLE", () => {
  it("3등급 모두 매핑되어 있다", () => {
    const severities: Severity[] = ["CRITICAL", "WARNING", "INFO"];
    for (const s of severities) {
      expect(SEVERITY_STYLE[s]).toBeDefined();
      expect(SEVERITY_STYLE[s].label).toBeTruthy();
    }
  });

  it("CRITICAL은 위험 라벨을 가진다", () => {
    expect(SEVERITY_STYLE.CRITICAL.label).toBe("위험");
  });
});
