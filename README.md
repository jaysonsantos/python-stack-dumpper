# python-stack-dumpper
Dump stack traces when SIGQUIT is received

## Installing
```
pip install stack_dummper
```

## Usage
Import `stack_dumpper` anywhere in your code and call `stack_dumpper.setup_dumpper()`.

To try it, run your code and press `CRTL + \` or send a **SIGQUIT** to your process ie:
```
kill -SIGQUIT PID
```

And if you want, you can call `stack_dumpper.dump_data()` at any time on your code or debug session.
