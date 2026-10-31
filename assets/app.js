(function () {
  var root = document.documentElement;
  var themeBtn = document.getElementById('theme');
  if (themeBtn) {
    var syncTheme = function () { themeBtn.setAttribute('aria-pressed', root.dataset.theme === 'dark' ? 'true' : 'false'); };
    syncTheme();
    themeBtn.addEventListener('click', function () {
      if (root.dataset.theme === 'dark') delete root.dataset.theme; else root.dataset.theme = 'dark';
      try { localStorage.setItem('bc-theme', root.dataset.theme || 'light'); } catch (e) {}
      syncTheme();
    });
  }

  var table = document.querySelector('#ranking .rank-t');
  if (!table) return;

  var LIMIT = 50;
  var TIERS = ['goat', 'lenda', 'estrela', 'coadjuvante', 'existe'];
  var tbody = table.tBodies[0];
  var rows = Array.prototype.slice.call(tbody.rows);
  var q1 = document.getElementById('q'), q2 = document.getElementById('q2');
  var fct = document.getElementById('fct'), ftier = document.getElementById('ftier');
  var count = document.getElementById('count'), reset = document.getElementById('reset');
  var more = document.getElementById('more'), empty = document.getElementById('empty');
  var ranking = document.getElementById('ranking');
  var state = { sort: 'rank', dir: 1, expanded: false };

  function norm(s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
  rows.forEach(function (r) { r._q = norm(r.dataset.q); });

  function value(r, key) {
    if (key === 'name') return r.dataset.name;
    if (key === 'tier') return TIERS.indexOf(r.dataset.tier);
    return Number(r.dataset[key]);
  }

  function apply() {
    var words = norm(q2.value.trim()).split(/\s+/).filter(Boolean);
    var filtered = words.length || fct.value || ftier.value;
    var shown = 0, total = 0;
    rows.forEach(function (r) {
      var hit = (!fct.value || r.dataset.ct === fct.value) && (!ftier.value || r.dataset.tier === ftier.value) &&
        words.every(function (w) { return r._q.indexOf(w) !== -1; });
      if (hit) total++;
      var visible = hit && (filtered || state.expanded || shown < LIMIT);
      if (visible) shown++;
      r.hidden = !visible;
    });
    count.textContent = total + ' ' + (total === 1 ? count.dataset.one : count.dataset.many);
    reset.hidden = !filtered;
    empty.hidden = total !== 0;
    table.parentNode.hidden = total === 0;
    more.parentNode.hidden = shown >= total;
    fct.classList.toggle('active', !!fct.value);
    ftier.classList.toggle('active', !!ftier.value);
  }

  function sortBy(key, fresh) {
    if (state.sort === key && !fresh) state.dir = -state.dir;
    else { state.sort = key; state.dir = (key === 'rank' || key === 'name' || key === 'tier') ? 1 : -1; }
    var sorted = rows.slice().sort(function (a, b) {
      var x = value(a, key), y = value(b, key);
      var c = key === 'name' ? x.localeCompare(y) : x - y;
      return (c * state.dir) || (Number(a.dataset.rank) - Number(b.dataset.rank));
    });
    sorted.forEach(function (r) { tbody.appendChild(r); });
    rows = sorted;
    table.querySelectorAll('th').forEach(function (th) {
      var b = th.querySelector('button');
      th.setAttribute('aria-sort', b && b.dataset.sort === key ? (state.dir === 1 ? 'ascending' : 'descending') : 'none');
    });
    apply();
  }

  function jump() { ranking.scrollIntoView(); }

  table.querySelectorAll('th button').forEach(function (b) {
    b.addEventListener('click', function () { sortBy(b.dataset.sort); });
  });
  q2.addEventListener('input', function () { q1.value = q2.value; apply(); });
  q1.addEventListener('input', function () { q2.value = q1.value; apply(); });
  q1.addEventListener('keydown', function (ev) { if (ev.key === 'Enter') { ev.preventDefault(); jump(); } });
  fct.addEventListener('change', apply);
  ftier.addEventListener('change', apply);
  document.getElementById('fsort').addEventListener('change', function (ev) { sortBy(ev.target.value, true); });
  document.getElementById('fsort').addEventListener('change', function (ev) { sortBy(ev.target.value, true); });
  more.addEventListener('click', function () { state.expanded = true; apply(); });
  reset.addEventListener('click', function () { q1.value = q2.value = ''; fct.value = ftier.value = ''; apply(); });
  document.querySelectorAll('[data-tier-pick]').forEach(function (b) {
    b.addEventListener('click', function () { ftier.value = b.dataset.tierPick; apply(); jump(); });
  });
  document.addEventListener('keydown', function (ev) {
    var tag = (ev.target.tagName || '').toLowerCase();
    if (ev.key === '/' && tag !== 'input' && tag !== 'select' && tag !== 'textarea') { ev.preventDefault(); q1.focus(); }
  });
  apply();
})();
