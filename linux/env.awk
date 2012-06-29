#!/usr/bin/gawk -f

BEGIN {
    RS = "\0"
    OFS = "="
    ORS = ""
    n = 0
}

/^(XAUTHORITY|DISPLAY|DBUS_SESSION_BUS_ADDRESS)=/ {
    env[n++] = $0
}

END {
    if (3 == length(env)) {
	for (var in env)
	    print env[var] ";"
	print "\n"
    }
}
