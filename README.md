# Fuzzy !

An other python web fuzzer.

It is used to test website URLs with a wordlist.

## TL;DR

```
Fuzzing or fuzz testing is an automated software testing technique that involves providing invalid, unexpected, or random data as inputs to a computer program.
The program is then monitored for exceptions such as crashes, or failing built-in code assertions or for finding potential memory leaks.
Typically, fuzzers are used to test programs that take structured inputs. This structure is specified, e.g., in a file format or protocol and distinguishes valid from invalid input.
An effective fuzzer generates semi-valid inputs that are "valid enough" in that they are not directly rejected by the parser, but do create unexpected behaviors deeper in the program and are "invalid enough" to expose corner cases that have not been properly dealt with.
- Wikipedia
```

## Usage

```
   ______   __  __     ______     ______     __  __
  /\  ___\ /\ \/\ \   /\___  \   /\___  \   /\ \_\ \
  \ \  __\ \ \ \_\ \  \/_/  /__  \/_/  /__  \ \____ \
   \ \_\    \ \_____\   /\_____\   /\_____\  \/\_____\
    \/_/     \/_____/   \/_____/   \/_____/   \/_____/



  An other web fuzzer (  https://sakiir.ovh  )
  - SakiiR

usage: fuzzy.py [-h] [--verb {GET,HEAD,TRACE,OPTION}] --url URL
                [--threads THREADS] [--headers [HEADERS [HEADERS ...]]]
                [--data DATA] [--verbose [VERBOSE]] [--proxies PROXIES]
                [--timeout TIMEOUT] [--report REPORT] [--hc HC] [--ht HT]
                [--st ST]

Python Web Fuzzer by SakiiR

optional arguments:
  -h, --help            show this help message and exit
  --verb {GET,HEAD,TRACE,OPTION}, -m {GET,HEAD,TRACE,OPTION}
                        HTTP verb to be used (default GET)
  --url URL, -u URL     URL to fuzz
  --threads THREADS, -t THREADS
                        Number of threads to be used (default 1)
  --headers [HEADERS [HEADERS ...]], -he [HEADERS [HEADERS ...]]
                        Additional HTTP headers, eg: --headers "foo: bar"
                        "Content-Type: application/json" (default none)
  --data DATA, -d DATA  Data to send to the website via POST requests, eg:
                        --data "foo=bar&password=#FUZZ#" (default none)
  --verbose [VERBOSE], -v [VERBOSE]
                        Verbose mode - Display more information (default
                        false)
  --proxies PROXIES, -p PROXIES
                        Simple http proxies to use (default none)
  --timeout TIMEOUT, -ti TIMEOUT
                        Max timeout duration in ms (default 3000ms)
  --report REPORT, -r REPORT
                        Report file to write in (default none)
  --hc HC               Hide given status code responses eg: --hc "404, 400"
                        (default none)
  --ht HT               Hide responses that match given str (default none)
  --st ST               Show responses that match given str (default none)
```
