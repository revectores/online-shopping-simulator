sync_get_obj = (url) => {
    const req = new XMLHttpRequest();
    req.open('GET', url, false);
    req.send();
    let res = JSON.parse(req.response);
    if (res.code !== 0) alert(res);
    return res.data;
}
