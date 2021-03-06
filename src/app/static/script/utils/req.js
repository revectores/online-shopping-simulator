sync_get = (url) => {
    const req = new XMLHttpRequest();
    req.open('GET', url, false);
    req.send();
    let res = JSON.parse(req.response);
    return res;
}

sync_post = (url, payload = {}) => {
	const req = new XMLHttpRequest();
	req.open('POST', url, false);
	req.setRequestHeader('content-type', 'application/json');
	req.send(JSON.stringify(payload));
	let res = JSON.parse(req.response);
	return res;
}

sync_get_data = (url) => {
    res = sync_get(url);
    if (res.code !== 0) alert(res);
    return res.data;
}
