#!/usr/bin/python
# coding:utf-8
# app/daemon.py

import os
import sys
import logging
import atexit
import signal

PIDFILE = sys.path[0]+"/.pidfile"

def daemonize(pidfile=PIDFILE):
    if os.path.exists(pidfile):
        raise RuntimeError('Already running')
    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError('fork #1 failed.')
    os.chdir("/")
    os.umask(0)
    os.setsid()
    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError as e:
         raise RuntimeError('fork #2 failed.')
    with open(pidfile,"w") as f:
		f.write(os.getpid())
    atexit.register(lambda: os.remove(pidfile))
    def sigterm_handler(signo, frame):
        raise SystemExit(1)
    signal.signal(signal.SIGTERM, sigterm_handler)

def start(func, *args):
    try:
		daemonize(PIDFILE)
	except RuntimeError as e:
		print(e, file=sys.stderr)
		raise SystemExit(1)
	func(*args)

def stop():
	if os.path.exists(PIDFILE):
		with open(PIDFILE) as f:
			os.kill(int(f.read()), signal.SIGTERM)
	else:
		raise RuntimeError('Not running')
