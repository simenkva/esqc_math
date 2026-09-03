import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "update_recommendations.py"
SPEC = importlib.util.spec_from_file_location("update_recommendations", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class RecommendationGeneratorTests(unittest.TestCase):
    def test_selection_lines_groups_exercises_by_chapter(self):
        exercises = [
            MODULE.Exercise("exr-recommended-first", "Chapter one"),
            MODULE.Exercise("exr-ordinary", "Chapter one"),
            MODULE.Exercise("exr-recommended-second", "Chapter two"),
        ]

        self.assertEqual(
            MODULE.selection_lines(exercises, "exr-recommended-"),
            "- **Chapter one**\n"
            "  - @exr-recommended-first\n\n"
            "- **Chapter two**\n"
            "  - @exr-recommended-second",
        )

    def test_replace_region_changes_only_generated_content(self):
        text = (
            "Before\n"
            "<!-- BEGIN GENERATED CURIOUS EXERCISES -->\n"
            "old\n"
            "<!-- END GENERATED CURIOUS EXERCISES -->\n"
            "After\n"
        )

        self.assertEqual(
            MODULE.replace_region(text, "CURIOUS", "new"),
            "Before\n"
            "<!-- BEGIN GENERATED CURIOUS EXERCISES -->\n"
            "new\n"
            "<!-- END GENERATED CURIOUS EXERCISES -->\n"
            "After\n",
        )


if __name__ == "__main__":
    unittest.main()
