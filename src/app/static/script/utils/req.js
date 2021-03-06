sync_get = (url) => {
    const req = new XMLHttpRequest();
    req.open('GET', url, false);
    req.send();
    return req.response;
}

sync_get_json = (url) => {
    return JSON.parse(sync_get(url));
}

sync_get_data = (url) => {
    res = sync_get_json(url);
    if (res.code !== 0) alert(res);
    return res.data;
}

sync_post = (url, payload = {}) => {
    const req = new XMLHttpRequest();
    req.open('POST', url, false);
    req.setRequestHeader('content-type', 'application/json');
    req.send(JSON.stringify(payload));
    return req.response;
}

