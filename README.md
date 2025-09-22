### Django runserver -u propagation repro
This repo shows a concrete bug in Django’s autoreloader:

when you run `python -u manage.py runserver`, the autoreloader’s child process starts without the unbuffered intent. In practice, the child runs with `PYTHONUNBUFFERED=None`, so stdout is buffered again.

We log to stderr (immediate) and use stdout markers to visualize buffering.



## How to run

1. Baseline
  
```bash
python manage.py runserver
```

Expected:
- Parent META: run_main=None, PYTHONUNBUFFERED=None
- Child META: run_main=true, PYTHONUNBUFFERED=None
- Stdout markers often appear together after ~2s: "[STDOUT:A][STDOUT:B]" (buffered)


2. -u only
```bash
python -u manage.py runserver
```
Expected:
- Parent META cmd includes -u
- Child META cmd has no -u and PYTHONUNBUFFERED=None
- Stdout markers still together after ~2s (buffered)

***the autoreloader child does not inherit the unbuffered intent of -u.***

3. -u + --noreload
```bash
python -u manage.py runserver --noreload
```
Expected:
- Single process (mostly run_main=None)
- Stdout markers split: A immediately, B ~2s later (unbuffered)

4. environment variable propagation
```bash
PYTHONUNBUFFERED=1 python manage.py runserver
```
Expected:
- Parent & child show PYTHONUNBUFFERED='1'
- Stdout markers split: A immediately, B ~2s later (unbuffered)

