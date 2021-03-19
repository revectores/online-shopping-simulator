document.getElementById('back').addEventListener('click', () => {
	sync_post('../api/product/back', {
		pathname: window.location.pathname,
		search: window.location.search
	});
	window.history.back();
});
