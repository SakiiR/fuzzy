<p align="center">
  <img width="500" src="./images/logo.png">
</p>

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

## Demo

[![asciicast](https://asciinema.org/a/152121.png)](https://asciinema.org/a/152121)

## Usage

```sh
$ fuzzy --url 'http://localhost:8000/#FUZZ#' --wordlist '~/wordlists/rockyou.txt'
```

## Limiting requests

The fuzzer is by default sending only one worker to consume the tasks queue.
The `--limit` option give you a way to configure this amount of worker consuming the task queue.

## Fuzzing tag

By default, the fuzzing tag is `#FUZZ#` but you can change it by whateve you want using the `--tag` option.

It can be placed in the request headers, url or data.

TODO: Possibility to add the Fuzz tag in an encrypted block (for http simple auth for exemple)

## Overriding headers

For this, you can use `--headers` like this:

```sh
$ fuzzy --url 'http://localhost:8000/#FUZZ#' --wordlist '~/wordlists/rockyou.txt' --headers 'Content-Type: application/json' 'Authorization: Bearer foo'
```

## Filter request

You can use the filter options like this:

```sh
$ # Will hide all the HTTP 404 and 403 responses
$ fuzzy --url 'http://localhost:8000/#FUZZ#' --wordlist '~/wordlists/rockyou.txt' --hc='404, 403'
$ # Will hide all the responses that contains the word 'foo'
$ fuzzy --url 'http://localhost:8000/#FUZZ#' --wordlist '~/wordlists/rockyou.txt' --ht='foo'
$ # Will show only the responses that contains the word 'foo'
$ fuzzy --url 'http://localhost:8000/#FUZZ#' --wordlist '~/wordlists/rockyou.txt' --st='foo'
```

## Proxy

As it is said in the `aiohttp` documentation the `trust_env` option is used to trust the HTTP_PROXY, HTTPS_PROXY environnement variable (https://aiohttp.readthedocs.io/en/stable/client.html#proxy-support)

```sh
$ # Fish
$ set -gx HTTP_PROXY localhost:8080
$ set -gx HTTPS_PROXY localhost:8080
$ # Bash / ZSH / Others
$ export HTTP_PROXY localhost:8080
$ export HTTPS_PROXY localhost:8080
```

For fish, I am currently using this script for my prompt:

```sh
function prompt_proxy -d 'Display the proxy status (HTTP_PROXY env variable)'
    set -l proxy_value 'None'
    if test "$HTTPS_PROXY"
        set proxy_value "$HTTPS_PROXY"
    end
    if test "$https_proxy"
        set proxy_value "$https_proxy"
    end
    if test "$HTTP_PROXY"
        set proxy_value "$HTTP_PROXY"
    end
    if test "$http_proxy"
        set proxy_value "$http_proxy"
    end
    if [ "$proxy_value" != "None" ]
        prompt_segment purple black "  $proxy_value"
    else
        prompt_segment purple black "  No Proxy"
    end
end
```
