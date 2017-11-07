def get_all_repos():
    t = get_token("admin", "keadmin")
    token_json = json.loads(t)
    t_str = token_json["token"]
    url="https://reg-dev.cloudappl.com/v2/_catalog?n=1000000"
    print(url)
    req = urllib2.Request(url = url)
    req.add_header("Authorization", "Bearer "+t_str)
    res = urllib2.urlopen(req)
    res = res.read()
    return res