# backend/metrics/snyk_metrics.py

from .base_metric import BaseMetric
from .result_model import MetricResult
import time

class SnykMetrics(BaseMetric):
    def calculate(self, raw_data: dict) -> MetricResult:
        vulns = raw_data.get("vulnerabilities", [])

        counts = {"critical":0, "high":0, "medium":0, "low":0}

        for v in vulns:
            sev = v.get("severity")
            if sev in counts:
                counts[sev] += 1

        return MetricResult(
            tool_name="Snyk Code",
            critical=counts["critical"],
            high=counts["high"],
            medium=counts["medium"],
            low=counts["low"],
            total_issues=len(vulns),
            scan_duration=raw_data.get("scanDuration", 0.0)
        )
