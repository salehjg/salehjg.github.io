// shared: highlight current nav link based on data-page attr on <body>
(function () {
  const page = document.body.getAttribute('data-page');
  if (!page) return;
  document.querySelectorAll('.nav a').forEach(a => {
    if (a.getAttribute('data-nav') === page) a.classList.add('active');
  });
})();
