# AUTODNS

A friendly little python app for a DIY inspired DynDNS client, leveraging AWS Route53


### Installation

I'm not presently publishing this on Pypi - so you'll need to fetch and install it as if
it were a development release (which it is). 

    git clone http://github.com/chuckbutler/autodns.git
    cd autodns
    python setup.py install

This will fetch all of the required dependencies and place autodns in your `/usr/local/bin` path.

It may be saner/cleaner to use a virtualenv. This is documented all over the web so I'll let you
use your google skills to determine how/if you want to do this.


### Configuration / Usage

AutoDNS works on a few basic principals:

- Each domain is their own configuration file
- We wont be editing APEX records, only A records
- You have internet connectivity
- You want DNS updated on a regular schedule
- You have exported your AWS Access Credentials to your environment


To get familiar with all of AutoDNS's commands, simply pass it a `-h` flag.

    autodns -h

    Update DNS entries on rt53 quickly and easily.

    positional arguments:
      config             Specify configuration file to parse

      optional arguments:
      -h, --help         show this help message and exit
      -l LOG, --log LOG  log to PATH
      -v, --debug        display debug output


Autodns uses configuration files (one per parent-level domain, or ZONEID) to not only configure,
but also to cache the last IP it sent to the server - it adds this field automatically, so dont
worry about adding that to begin with. The configuration has a few levels of keys in YAML format
and will look like the following:

    ZONEID: P23QZY95VZHATG
    DOMAINS:
      - pad.autodns.net
      - minecraft.autodns.net
    TTL: 300

> **Note:** Ensure you use a FQDN in the DOMAINS array - as this is how we tell AWS Rt53 what we
> are adding / modifying. Without a FQDN the request will fail and you'll be left to dig through
> the logs to see what went wrong.

The required keys are:
- ZONEID
- DOMAINS
- TTL

Notice that they are all CAPS, and this is by design. Where possible, meaningful error messages
were attempted to be raised. If you encounter any bugs - simply submit them to the issue tracker.


### I ran autodns after adding a record and it said "nothing to do" - what gives?

The ADDRESS key will be parsed out of the YAML and is the determinent if an update needs to take
place. If you are adding a dns entry to the configuration - you will want to **completely remove**
the ADDRESS key, so it is forced to push a fresh update. This will send a request to all of the
subdomains in the configuration, and once completed - will resume normal operation.

### I want to run this periodically like a DynDNS client, how do I do that?

Glad you asked! This is exactly why I built AutoDNS. To get AutoDNS to run on a schedule
you will need to place it in your users crontab:

    crontab -e

    export AWS_ACCESS_KEY_ID=XXXXX
    export AWS_SECRET_ACCESS_KEY=XXXXX
    * */1 * * * autodns path/to/config.yml -l $HOME/autodns.log

This will run AutoDNS every hour, and log the output to $HOME/autodns.log - effectively
replacing any legacy DynDNS client functionality you may have had on your router. Note that this
only gets run while the machine running AutoDNS is on.

### Where do I get the ZONEID field?

Log into your AWS Rt53 control panel, and it will be listed by your Domain Name

![Rt 53 control panel](http://i.imgur.com/2QrkI2j.png)

