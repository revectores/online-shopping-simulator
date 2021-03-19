document.getElementById('logout').addEventListener('click', () => {
	sync_post('../api/user/logout');

    if (res.code === 0){
      open('../user/login', '_self');
    } else {
      alert(res.msg);
    }
});
