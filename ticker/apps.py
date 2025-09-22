import logging, os, sys, time, subprocess
from django.apps import AppConfig

logger = logging.getLogger("ticker")

def _ps_cmdline(pid: int) -> str:
    try:
        return subprocess.check_output(["ps", "-o", "command=", "-p", str(pid)], text=True).strip()
    except Exception as e:
        return f"<ps failed: {e!r}>"

class TickerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ticker"

    def ready(self):
        pid = os.getpid()
        run_main = os.environ.get("RUN_MAIN")
        py_unbuf = os.environ.get("PYTHONUNBUFFERED")
        cmdline = _ps_cmdline(pid)

        logger.info(
            "META pid=%s run_main=%s PYTHONUNBUFFERED=%r cmd=%s",
            pid, run_main, py_unbuf, cmdline
        )

        sys.stdout.write("[STDOUT:A]")
        time.sleep(2)
        sys.stdout.write("[STDOUT:B]\n")
        sys.stdout.flush()

        logger.info("READY[A] pid=%s run_main=%s", pid, run_main)
        time.sleep(2)
        logger.info("READY[B] pid=%s run_main=%s", pid, run_main)
