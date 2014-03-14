rule dexter_strings
{
    meta:
        author = "Brian Wallace @botnet_hunter"
        author_email = "bwall@ballastsecurity.net"
        date = "2014-03-13"
        description = "Identify Dexter POSGrabber"
    strings:
        $c = "UpdateMutex:"
        $str5 = "response="
        $str6 = "&view="
    condition:
        all of them
}