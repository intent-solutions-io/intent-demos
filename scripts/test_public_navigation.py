import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import stamp_public_navigation as navigation


class NavigationPublicationTests(unittest.TestCase):
    def test_missing_route_prevents_any_write(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / 'site/assets/estate-bar/fragments'
            config.mkdir(parents=True)
            (config / 'estate-bar.demos.html').write_text('canonical')
            (root / 'site/assets/public-page-routes.json').write_text(json.dumps({'pages': ['one.html', 'missing.html']}))
            page = root / 'one.html'
            page.write_text('<html><head></head><body>Keep this page</body></html>')
            before = page.read_bytes()
            with patch.object(navigation, 'ROOT', root), patch('sys.argv', ['stamp', '--root', str(root)]):
                with self.assertRaisesRegex(SystemExit, 'Missing public page'):
                    navigation.main()
            self.assertEqual(page.read_bytes(), before)

    def test_route_cannot_escape_deployment_via_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            site = root / 'site/assets/estate-bar/fragments'
            site.mkdir(parents=True)
            (site / 'estate-bar.demos.html').write_text('canonical')
            (root / 'site/assets/public-page-routes.json').write_text(json.dumps({'pages': ['linked.html']}))
            deploy = root / 'deploy'; deploy.mkdir()
            private = root / 'outside.html'; private.write_text('Keep private')
            (deploy / 'linked.html').symlink_to(private)
            with patch.object(navigation, 'ROOT', root), patch('sys.argv', ['stamp', '--root', str(deploy)]):
                with self.assertRaisesRegex(SystemExit, 'escapes deployment root'):
                    navigation.main()
            self.assertEqual(private.read_text(), 'Keep private')


if __name__ == '__main__':
    unittest.main()
