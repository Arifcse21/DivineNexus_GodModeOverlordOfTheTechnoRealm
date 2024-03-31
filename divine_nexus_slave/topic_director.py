from cli_master import cli_master

def mqtt_topic_cli(msg):
    if msg:
        print(f"full_content: {msg}")
        msg = msg.decode()
        
        cli_id, cli, topic = msg.split("#")
        
        exec_stat, exec_resp = cli_master(cli)
        
        return cli_id, cli, topic, exec_resp
        
    else:
        return "no msg provided"
