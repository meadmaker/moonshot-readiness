#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import os
import socket
import sys
import stat
import re

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


print "\n\n===============================  MOONSHOT-READINESS  ==============================="
results = "====================================================================================\n\nTest complete, failed tests:\n"



#=================================  TESTS BASIC  ===========================================



def test_basic():
    global results
    print("\n\nTesting task basic...")


#Hostname is FQDN

    cmd = os.popen("hostname -f")
    fqdn1 = (cmd.read()).strip()
    cmd = os.popen("dig " + fqdn1 + " +short")
    address = (cmd.read()).strip()
    if len(address) == 0:
         print("    Hostname is FQDN...                            " + bcolors.FAIL + "[FAIL]" + bcolors.ENDC + "")
         results = results + "    Hostname is FQDN:\n        Your servers hostname ("+fqdn1+") is not fully resolvable. This is required in order to prevent certain classes of attack.\n"
    else:      
        cmd = os.popen("dig -x " + address + " +short")
        fqdn2 = (cmd.read()).strip()
        if fqdn1 + "." == fqdn2:
            print("    Hostname is FQDN...                            " + bcolors.OKGREEN + "[OKAY]" + bcolors.ENDC + "")
        else:
            print("    Hostname is FQDN...                            " + bcolors.FAIL + "[FAIL]" + bcolors.ENDC + "")
            results = results + "    Hostname is FQDN:\n        Your servers IP address " + address + " is not resolvable to '" + fqdn1 + "' instead script got '" + fqdn2.strip('.') + "'. This is required in order to prevent certain classes of attack.\n"


#Supported OS

    good_os = False
    if os.path.isfile("/etc/redhat-release") == True:
        fil = open("/etc/redhat-release", "r")
        name = (fil.read()).strip()
        fil.close()
        if (name == "RedHat release 6.3 (Final)" or name == "RedHat release 6.4 (Final)" or name == "RedHat release 6.5 (Final)" or name == "RedHat release 6.6 (Final)" or name == "CentOS release 6.3 (Final)" or name == "CentOS release 6.4 (Final)" or name == "CentOS release 6.5 (Final)" or name == "CentOS release 6.6 (Final)" or name == "Scientific Linux release 6.3 (Final)" or name == "Scientific Linux release 6.4 (Final)" or name == "Scientific Linux release 6.5 (Final)" or name == "Scientific Linux release 6.6 (Final)"):
            good_os = True
    elif os.path.isfile("/etc/os-release") == True:
        fil = open("/etc/os-release", "r")
        text = fil.read()
        fil.close()
        lines = text.split("\n")
        good_name = False
        good_version = False
        i = 0
        while i < len(lines):
            words = lines[i].split("=")
            if words[0] == "NAME":
                if words[1] == "\"Debian GNU/Linux\"":
                    good_name = True
            if words[0] == "VERSION_ID":
                if words[1] == "\"6\"" or words[1] == "\"7\"":
                    good_version = True
            i = i + 1
        if good_name == True and good_version == True:
            good_os = True
    if good_os == True:
        print("    Supported OS...                                " + bcolors.OKGREEN + "[OKAY]" + bcolors.ENDC + "")
    else:
        print("    Supported OS...                                " + bcolors.WARNING + "[WARN]" + bcolors.ENDC + "")
        results = results + "    Supported OS:\n        You are not running a supported OS. Moonshot may not work as indicated in the documentation.\n"


#Moonshot repository configuration

    cmd = os.popen("apt-cache search -n \"moonshot\"")
    cmd = cmd.read()
    if cmd.strip() != '':
        print("    Moonshot repositories configured...            " + bcolors.OKGREEN + "[OKAY]" + bcolors.ENDC + "")
    else:
        print("    Moonshot repositories configured...            " + bcolors.WARNING + "[WARN]" + bcolors.ENDC + "")
        results = results + "    Moonshot repositories configured:\n        The Moonshot repositories do not appear to exist on this system. You will not be able to upgrade Moonshot using your distributions package manager.\n"


#Moonshot Signing Key

    cmd = os.popen("apt-key --keyring /etc/apt/trusted.gpg list")
    cmd = cmd.read()
    key1 = False
    key2 = False
    key3 = False    
    words=re.split(r'[ \t\n/]+', cmd)
    i = 0
    while i < len(words):
        if words[i] == "2EB761E3":
            key1 = True
        if words[i] == "CEA67BB6":
            key2 = True
        if words[i] == "DF209716":
            key3 = True
        i = i + 1
    if (key1 == True and key2 == True and key3 == True):
        print("    Moonshot Signing Key...                        " + bcolors.OKGREEN + "[OKAY]" + bcolors.ENDC + "")
    else:
        print("    Moonshot Signing Key...                        " + bcolors.WARNING + "[WARN]" + bcolors.ENDC + "")
        results = results + "    Moonshot Signing Key:\n        The Moonshot repository key is not installed, you will have difficulty updating packages.\n"


#Current version

    cmd = os.popen("apt-get -u upgrade --assume-no moonshot")
    cmd = cmd.read()
    if cmd.strip() == 'Reading package lists... Done\nBuilding dependency tree\nReading state information... Done\n0 upgraded, 0 newly installed, 0 to remove and\
 0 not upgraded.':
        print("    Moonshot current version...                    " + bcolors.OKGREEN + "[OKAY]" + bcolors.ENDC + "\n\n")
    else:
        print("    Moonshot current version...                    " + bcolors.WARNING + "[WARN]" + bcolors.ENDC + "\n\n")
        results = results + "    Moonshot current version:\n        You are not running the latest version of the Moonshot software.\n"



#=================================  TESTS RP  ===========================================



def test_rp():
    global results
    test_basic()
    print("Testing task rp...")


#/etc/radsec.conf

    cmd = os.path.isfile("/etc/radsec.conf")
    if cmd == True:
        print("    radsec.conf...                                 " + bcolors.OKGREEN + "[OKAY]" + bcolors.ENDC + "\n\n")
    else:
        print("    radsec.conf...                                 " + bcolors.FAIL + "[FAIL]" + bcolors.ENDC + "\n\n")
        results = results + "    radsec.conf:\n        /etc/radsec.conf could not be found - you may not be able to communicate with your rp-proxy.\n"



#=================================  TESTS RP-PROXY  ===========================================



def test_rp_proxy():
    global results
    test_rp()
    print("Testing task rp-proxy...")


#APC

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('apc.moonshot.ja.net', 2083))
    if result == 0:
        print("    APC...                                         " + bcolors.OKGREEN + "[OKAY]" + bcolors.ENDC + "")
    else:
        print("    APC...                                         " + bcolors.FAIL + "[FAIL]" + bcolors.ENDC + "")
        results = results + "    APC:\n        apc.moonshot.ja.net does not seem to be accessible. Please check the servers network connection, and see status.moonshot.ja.net for any downtime or maintenance issues.\n"


#Trust Router

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('tr1.moonshot.ja.net', 12309))
    if result == 0:
        print("    Trust Router...                                " + bcolors.OKGREEN + "[OKAY]" + bcolors.ENDC + "")
    else:
        print("    Trust Router...                                " + bcolors.FAIL + "[FAIL]" + bcolors.ENDC + "")
        results = results + "    Trust Router:\n        tr1.moonshot.ja.net does not seem to be accessible. Please check the servers network connection, and see status.moonshot.ja.net for any downtime or maintenance issues.\n"


#flatstore-users

    root = False
    freerad = False
    if os.path.isfile("/etc/moonshot/flatstore-users") == True:
        fil = open("/etc/moonshot/flatstore-users", "r")
        for line in fil:
            if line.strip() == "root":
                root = True
            if line.strip() == "freerad":
                freerad = True
        fil.close()
    if root == True and freerad == True:
        print("    Flatstore-users...                             " + bcolors.OKGREEN + "[OKAY]" + bcolors.ENDC + "")
    else:
        print("    Flatstore-users...                             " + bcolors.FAIL + "[FAIL]" + bcolors.ENDC + "")
        results = results + "    Flatstore-users:\n        /etc/moonshot/flatstore-users could not be found, or does not contain all the user accounts it needs to. You may be unable to authenticate to the trust router.\n"
        

#Trust Identity

    if os.path.isfile("/etc/freeradius/.local/share/moonshot-ui/identities.txt") == True:
        print("    Trust Identity...                              " + bcolors.OKGREEN + "[OKAY]" + bcolors.ENDC + "\n\n")
    else:
        print("    Trust Identity...                              " + bcolors.FAIL + "[FAIL]" + bcolors.ENDC + "\n\n")
        results = results + "    Trust Identity:\n        No trust identity could be found for the freeradius user account. You will not be able to authenticate to the trust router.\n"



#=================================  TESTS IDP  ===========================================



def test_idp():
    global results
    test_rp()
    print("Testing task idp...")


#Port 2083

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 2083))
    if result == 0:
        print("    Port 2083...                                   " + bcolors.OKGREEN + "[OKAY]" + bcolors.ENDC + "")
    else:
        print("    Port 2083...                                   " + bcolors.FAIL + "[FAIL]" + bcolors.ENDC + "")
        results = results + "    Port 2083:\n        Port 2083 appears to be closed. RP's will not be able to initiate connections to your IDP.\n"


#Port 12309

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 12309))
    if result == 0:
        print("    Port 12309...                                  " + bcolors.OKGREEN + "[OKAY]" + bcolors.ENDC + "")
    else:
        print("    Port 12309...                                  " + bcolors.FAIL + "[FAIL]" + bcolors.ENDC + "")
        results = results + "    Port 12309:\n        Port 12309 appears to be closed. The trust router will not be able to initiate connections to your IDP.\n"


#flatstore-users

    root = False
    freerad = False
    if os.path.isfile("/etc/moonshot/flatstore-users") == True:
        fil = open("/etc/moonshot/flatstore-users", "r")
        for line in fil:
            if line.strip() == "root":
                root = True
            if line.strip() == "freerad":
                freerad = True
        fil.close()
    if root == True and freerad == True:
        print("    Flatstore-users...                             " + bcolors.OKGREEN + "[OKAY]" + bcolors.ENDC + "")
    else:
        print("    Flatstore-users...                             " + bcolors.FAIL + "[FAIL]" + bcolors.ENDC + "")
        results = results + "    Flatstore-users:\n        /etc/moonshot/flatstore-users could not be found, or does not contain all the user accounts it needs to. You may be unable to authenticate to the trust router.\n"


#Trust Identity

    if os.path.isfile("/etc/freeradius/.local/share/moonshot-ui/identities.txt") == True:
        print("    Trust Identity...                              " + bcolors.OKGREEN + "[OKAY]" + bcolors.ENDC + "\n\n")
    else:
        print("    Trust Identity...                              " + bcolors.FAIL + "[FAIL]" + bcolors.ENDC + "\n\n")
        results = results + "    Trust Identity:\n        No trust identity could be found for the freeradius user account. You will not be able to authenticate to the trust router.\n"



#=================================  TESTS CLIENT  ===========================================



def test_client():
    global results
    test_basic()
    print("Testing task client...")


#gss/mech

    cmd = os.path.isfile("/usr/etc/gss/mech") 
    if cmd == True:
        mode = oct(stat.S_IMODE(os.stat("/usr/etc/gss/mech")[stat.ST_MODE]))
        if mode.strip() == "0644":
            
            string1 = "eap-aes128 1.3.6.1.5.5.15.1.1.17 mech_eap.so" 
            string2 = "eap-aes128 1.3.6.1.5.5.15.1.1.17 mech_eap.so"
            s1 = False
            s2 = False
            fil = open("/usr/etc/gss/mech","r")
            for line in fil:
                words=re.split(r'[ \t]+', line)
                i = 0
                str_reg = ""
                while i < len(words):
                    str_reg = str_reg + words[i] + " "
                    i = i+1
                if string1 == str_reg.strip():
                    s1 = True
                if string2 == str_reg.strip():
                    s2 = True
            fil.close()
            
            if (s1 == True and s2 == True):
                print("    gss/mech...                                    " + bcolors.OKGREEN + "[OKAY]" + bcolors.ENDC + "\n\n")
                return;

    print("    gss/mech...                                    " + bcolors.FAIL + "[FAIL]" + bcolors.ENDC + "\n\n")
    results = results + "    gss/mech:\n        The Moonshot mech file is missing mech_eap.so will not be loaded.\n"



#=================================  TESTS SSH-CLIENT  ===========================================



def test_ssh_client():
    global results
    test_client()
    print("Testing task ssh-client...")


#GSSAPIAuthentication enabled

    cmd = os.popen("augtool print /files/etc/ssh/ssh_config/Host/GSSAPIAuthentication")
    cmd = cmd.read()
    if cmd.strip() == "/files/etc/ssh/ssh_config/Host/GSSAPIAuthentication = \"yes\"":
        print("    GSSAPIAuthentication enabled...                " + bcolors.OKGREEN + "[OKAY]" + bcolors.ENDC + "")
    else:
        print("    GSSAPIAuthentication enabled...                " + bcolors.FAIL + "[FAIL]" + bcolors.ENDC + "")
        results = results + "    GSSAPIAuthentication enabled:\n        GSSAPIAuthentication must be enabled for Moonshot to function when using SSH.\n"


#GSSAPIKeyExchange enabled

    cmd = os.popen("augtool print /files/etc/ssh/ssh_config/Host/GSSAPIKeyExchange")
    cmd = cmd.read()
    if cmd.strip() == "/files/etc/ssh/ssh_config/Host/GSSAPIKeyExchange = \"yes\"":
        print("    GSSAPIKeyExchange enabled...                   " + bcolors.OKGREEN + "[OKAY]" + bcolors.ENDC + "\n\n")
    else:
        print("    GSSAPIKeyExchange enabled...                   " + bcolors.WARNING + "[WARN]" + bcolors.ENDC + "\n\n")
        results = results + "    GSSAPIKeyExchange enabled:\n        GSSAPIKeyExchange should be enabled for Moonshot to function correctly when using SSH.\n"



#=================================  TESTS SSH-SERVER  ===========================================



def test_ssh_server():
    global results
    test_rp()
    print("Testing task ssh-client...")


#Privilege separation disabled

    cmd = os.popen("augtool print /files/etc/ssh/sshd_config/UsePrivilegeSeparation")
    cmd = cmd.read()
    if cmd.strip() == "/files/etc/ssh/sshd_config/UsePrivilegeSeparation = \"no\"":
        print("    Privilege separation disabled...               " + bcolors.OKGREEN + "[OKAY]" + bcolors.ENDC + "")
    else:
        print("    Privilege separation disabled...               " + bcolors.FAIL + "[FAIL]" + bcolors.ENDC + "")
        results = results + "    Privilege separation disabled:\n        Moonshot currently requires that OpenSSH server has privilege separation disabled.\n"


#GSSAPIAuthentication

    cmd = os.popen("augtool print /files/etc/ssh/sshd_config/GSSAPIAuthentication")
    cmd = cmd.read()
    if cmd.strip() == "/files/etc/ssh/sshd_config/GSSAPIAuthentication = \"yes\"":
        print("    GSSAPIAuthentication...                        " + bcolors.OKGREEN + "[OKAY]" + bcolors.ENDC + "\n\n")
    else:
        print("    GSSAPIAuthentication...                        " + bcolors.FAIL + "[FAIL]" + bcolors.ENDC + "\n\n")
        results = results + "    GSSAPIAuthentication:\n        GSSAPIAuthentication must be enabled for Moonshot to function when using SSH.\n"



#=================================  MAIN  ===========================================



size = len(sys.argv)

if size < 2 :
    print("\n\nUsage: moonshot-readiness [task] [task]...\n\n  Available tasks:\n    help\n    minimal (default)\n    client\n    rp\n    rp-proxy\n    idp-proxy\n    ssh-client\n    ssh-server\n\n")

else:
    i = 1
    while i < size:
        if (sys.argv[i]).strip() == 'help':
            print "\n\nUsage: moonshot-readiness [task] [task]...\n\n  Available tasks:\n    help\n    minimal (default)\n    client\n    rp\n    rp-proxy\n    idp-proxy\n    ssh-client\n    ssh-server\n\n  ¦---------------------------------------------------------------------------------------------------------------¦\n  ¦ TASK            ¦  DEPENDENCY  ¦  DESCRIPTION                                                                 ¦\n  ¦-----------------¦--------------¦------------------------------------------------------------------------------¦\n  ¦ basic           ¦  none        ¦  Basic set of test, required for Moonshot to function at all in any capacity ¦\n  ¦ client          ¦  basic       ¦  Fundamental tests required for Moonshot to function as a client             ¦\n  ¦ rp              ¦  basic       ¦  Fundamental tests required for Moonshot to function as an RP                ¦\n  ¦ rp-proxy        ¦  rp          ¦  Tests required for Moonshot to function as a RadSec RP                      ¦\n  ¦ idp             ¦  rp          ¦  Tests to verify if FreeRADIUS is correctly configured                       ¦\n  ¦ openssh-client  ¦  client      ¦  Tests to verify if the openssh-client is correctly configured               ¦\n  ¦ openssh-rp      ¦  rp          ¦  Tests to verify if the openssh-server is correctly configured               ¦\n  ¦ httpd-client    ¦  client      ¦  Tests to verify if mod-auth-gssapi is correctly configured                  ¦\n  ¦ httpd-rp        ¦  rp          ¦  Tests to verify if mod-auth-gssapi is correctly configured                  ¦\n  ¦-----------------¦--------------¦------------------------------------------------------------------------------¦\n\n\nSome tests require root privileges to be made.\nSome tests require the following tools:\n  augeas     (installing with apt-get install augeas-tools)\n  dig        (installing with apt-get install dnsutils)\n  hostname   (installing with apt-get install hostname)\n\n"


            sys.exit()
        elif (sys.argv[i]).strip() == 'minimal':
            test_basic()
        elif (sys.argv[i]).strip() == 'client':
            test_client()
        elif (sys.argv[i]).strip() == 'rp':
            test_rp()
        elif (sys.argv[i]).strip() == 'rp-proxy':
            test_rp_proxy()
        elif (sys.argv[i]).strip() == 'idp-proxy':
            test_idp()
        elif (sys.argv[i]).strip() == 'ssh-client':
            test_ssh_client()
        elif (sys.argv[i]).strip() == 'ssh-server':
            test_ssh_server()
        else:
            print ("\n\nTask \"" + sys.argv[i] + "\" doesn't exist.\n  Available tasks:\n    minimal (default)\n    client\n    rp\n    rp-proxy\n    idp-proxy\n    ssh-client\n    ssh-server\n\n")
            sys.exit()
        i = i+1

    if results == "=========================================================================\n\nTest complete, failed tests:\n":
        results = "=========================================================================\n\nTest complete, 100% is OKAY\n\n"
    print results
