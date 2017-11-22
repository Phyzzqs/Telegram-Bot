#!/usr/bin/python
# coding:utf-8
# app/daemon.py

import os
import atexit
import signal

class Daemon:
        
    def __init__(self, pidfile=os.getcwd()+"/.pidfile"):
        self.PIDFILE = pidfile
    
    def daemonize(self):
        if os.path.exists(self.PIDFILE):
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
        with open(self.PIDFILE,"w") as f:
            f.write(str(os.getpid()))
        atexit.register(lambda: os.remove(self.PIDFILE))
        def sigterm_handler(signo, frame):
            raise SystemExit(1)
        signal.signal(signal.SIGTERM, sigterm_handler)
    
    def start(self, func, *args):
        try:
            self.daemonize()
        except RuntimeError as e:
            raise SystemExit(1)
        func(*args)
    
    def stop(self):
        if os.path.exists(self.PIDFILE):
            with open(self.PIDFILE) as f:
                os.kill(int(f.read()), signal.SIGTERM)
        else:
            raise RuntimeError('Not running')
    
