"""Structural checks: every skill loads, the plugin manifests parse, and install/uninstall round-trip."""
import json, os, re, subprocess, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = ["autonomous", "ship-safe", "deploy-audit", "dreamer", "summary"]
FRONT = re.compile(r"\A---\nname: (?P<name>[a-z0-9-]+)\ndescription: (?P<desc>.+?)\n---\n", re.S)


class Skills(unittest.TestCase):
    def test_frontmatter(self):
        for s in SKILLS:
            with self.subTest(skill=s):
                text = open(os.path.join(ROOT, "skills", s, "SKILL.md"), encoding="utf-8").read()
                m = FRONT.match(text)
                self.assertIsNotNone(m, "frontmatter must be name + description")
                self.assertEqual(m.group("name"), s, "name must match folder")
                self.assertLessEqual(len(m.group("desc")), 1024, "description over 1024 chars")
                self.assertGreater(len(text), 1500, "body looks empty")

    def test_no_stray_skills(self):
        self.assertEqual(sorted(os.listdir(os.path.join(ROOT, "skills"))), sorted(SKILLS))

    def test_manifests(self):
        p = json.load(open(os.path.join(ROOT, ".claude-plugin", "plugin.json")))
        m = json.load(open(os.path.join(ROOT, ".claude-plugin", "marketplace.json")))
        self.assertEqual(p["name"], "unattended")
        self.assertEqual(m["plugins"][0]["name"], p["name"])
        self.assertTrue(os.path.exists(os.path.join(ROOT, p["icon"])))

    def test_install_round_trip(self):
        with tempfile.TemporaryDirectory() as d:
            env = dict(os.environ, CLAUDE_CONFIG_DIR=d)
            os.makedirs(os.path.join(d, "skills", "summary"))          # a foreign skill of the same name
            open(os.path.join(d, "skills", "summary", "SKILL.md"), "w").write("theirs")
            subprocess.run([os.path.join(ROOT, "install.sh")], env=env, check=True, capture_output=True)
            for s in SKILLS:
                self.assertTrue(os.path.exists(os.path.join(d, "skills", s, "SKILL.md")))
            self.assertEqual(open(os.path.join(d, "skills", "summary", "SKILL.md")).read(), "theirs",
                             "installer overwrote a skill it doesn't own")
            subprocess.run([os.path.join(ROOT, "uninstall.sh")], env=env, check=True, capture_output=True)
            self.assertEqual(os.listdir(os.path.join(d, "skills")), ["summary"], "uninstall left ours or took theirs")


if __name__ == "__main__":
    unittest.main()
