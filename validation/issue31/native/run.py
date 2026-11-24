"""Run a localized, reset native fixture against a separate KNIME 5.12 configuration.

Usage: python3 run.py /path/to/unpacked-fixture /new/scratch/dir [Eclipse-install-dir]
Uses the installed JRE, Eclipse compiler and KNIME workflow test APIs; does not
install anything into KNIME or reuse an existing workspace.
"""
import os
from pathlib import Path
import shutil
import subprocess
import sys
from zipfile import ZipFile

fixture, scratch = [Path(x).resolve() for x in sys.argv[1:3]]
eclipse = Path(sys.argv[3] if len(sys.argv) > 3 else "/Applications/KNIME 5.12.0.app/Contents/Eclipse")
scratch.mkdir(parents=True, exist_ok=False)
plugins = eclipse / "plugins"


def plugin(pattern):
    path, = plugins.glob(pattern)
    return path


classes = scratch / "classes"
classes.mkdir()
cp = [plugin("org.eclipse.equinox.app_*.jar"), plugin("org.knime.core_*/knime-core.jar"),
      plugin("org.eclipse.core.runtime_*.jar"), plugin("org.eclipse.equinox.common_*.jar"),
      plugin("org.eclipse.osgi_*.jar"), plugin("org.knime.core.util_*.jar")]
subprocess.run([plugin("org.knime.binary.jre*/jre/Contents/Home/bin/java"), "-jar",
                plugin("org.eclipse.jdt.core.compiler.batch_*.jar"), "-21", "-classpath",
                os.pathsep.join(map(str, cp)), "-d", classes, Path(__file__).with_name("ReviewTest.java")], check=True)
jar = scratch / "review.nativecheck.jar"
with ZipFile(jar, "w") as z:
    z.write(classes / "review/ReviewTest.class", "review/ReviewTest.class")
    z.writestr("META-INF/MANIFEST.MF", """Manifest-Version: 1.0
Bundle-ManifestVersion: 2
Bundle-Name: Issue 31 workflow integration test
Bundle-SymbolicName: review.nativecheck;singleton:=true
Bundle-Version: 1.0.0
Require-Bundle: org.eclipse.equinox.app,org.knime.core

""")
    z.writestr("plugin.xml", """<plugin><extension id="test" point="org.eclipse.core.runtime.applications">
<application><run class="review.ReviewTest"/></application></extension></plugin>""")
config = scratch / "configuration"
simple = Path("org.eclipse.equinox.simpleconfigurator/bundles.info")
(config / simple.parent).mkdir(parents=True)
shutil.copy(eclipse / "configuration/config.ini", config)
with (config / simple).open("w") as out:
    out.write((eclipse / "configuration" / simple).read_text())
    out.write(f"review.nativecheck,1.0.0,{jar.as_uri()},4,false\n")
cmd = [eclipse.parent / "MacOS/knime", "-nosplash", "-consoleLog", "-configuration", config,
       "-data", scratch / "workspace", "-application", "review.nativecheck.test"]
sys.exit(subprocess.run(cmd, env={**os.environ, "REVIEW_FIXTURE": str(fixture)}).returncode)
