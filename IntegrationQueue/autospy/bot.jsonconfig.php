<?php 
set_time_limit(0); 
//error_reporting(0); 
date_default_timezone_set('UTC');

function aLog($message, $config, $in = True)
{
    $entry = array(
        "timestamp" => date("r"), 
        "server" => $config["server"], 
        "channel" => $config["chan"], 
        "payload" => $config["payload"], 
        "message" => $message, 
        "inbound" => $in
    );

    $log = json_encode($entry)."\r\n";
    
    print $log;
    
    $fp = fopen($config["lockfile"], "r");
    flock($fp, LOCK_EX);
    
    file_put_contents("log.txt", $log, FILE_APPEND | LOCK_EX);
    
    file_put_contents($config["logfile"], $log, FILE_APPEND | LOCK_EX);
    
    flock($fp, LOCK_UN);
    fclose($fp);
}

class pBot 
{
    var $config = array();
    var $users = array(); 

    function start() 
    {
        $this->config = json_decode(file_get_contents("config.json"), true); 
        if(!($this->conn = fsockopen($this->config['server'], $this->config['port'], $e, $s, 30))) 
            $this->start();

        $ident = $this->config['prefix'];
        $alph = range("0","9");
        for($i=0; $i<$this->config['maxrand']; $i++) 
            $ident .= $alph[rand(0,9)];

        if(strlen($this->config['pass'])>0) 
            $this->send("PASS ".$this->config['pass']);

        $this->send("USER ".$ident." 127.0.0.1 localhost :Linux etmortemtuam 3.11.0-12-generic #19-Ubuntu SMP Wed Oct 9 16:20:46 UTC 2013 x86");
        $this->set_nick();
        $this->main();
    }

    function main() 
    { 
        while(!feof($this->conn)) 
        { 
            $this->buf = trim(fgets($this->conn,512)); 
            aLog($this->buf, $this->config);
            $cmd = explode(" ",$this->buf); 
            if(substr($this->buf,0,6)=="PING :") 
            { 
                $this->send("PONG :".substr($this->buf,6)); 
            } 
            if(isset($cmd[1]) && $cmd[1] =="001") 
            { 
                $this->send("MODE ".$this->nick." ".$this->config['modes']);

                // Change to list of channels
                $this->join($this->config['chan'],$this->config['key']);
            } 
            if(isset($cmd[1]) && $cmd[1]=="433") 
            { 
                $this->set_nick(); 
            } 
            $old_buf = $this->buf; 
        } 
        $this->start(); 
    }

    function send($msg) 
    { 
        aLog($this->conn, $this->config, False);
        fwrite($this->conn, "$msg\r\n"); 
    } 

    function join($chan, $key=NULL) 
    { 
        $this->send("JOIN $chan $key"); 
    }

    function privmsg($to, $msg)
    {
        $this->send("PRIVMSG $to :$msg");
    }

    function notice($to, $msg)
    {
        $this->send("NOTICE $to :$msg");
    }

    function set_nick() 
    { 
        $this->nick = "[A]";
        $this->nick .= $this->config['prefix']; 
        for($i=0; $i<$this->config['maxrand']; $i++) 
            $this->nick .= mt_rand(0,9); 
        $this->send("NICK ".$this->nick);
    } 
} 

$bot = new pBot; 
$bot->start(); 
?>