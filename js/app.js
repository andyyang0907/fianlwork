// app.js - 单文件,所有页面共用
// 数据由 data/venues.json 加载,失败时用 DEFAULT_DATA 兜底
// ECharts / Chart.js / Three.js 走 CDN,失败时使用本地 fallback 图表 / Canvas 示意

// ============ 通用工具 ============

const ICONS = {
  篮球: '🏀', 足球: '⚽', 羽毛球: '🏸', 乒乓球: '🏓',
  健身: '💪', 网球: '🎾', 田径: '🏃'
};

const DEFAULT_DATA = [
  { name: '中心篮球场', type: '篮球', capacity: 40, status: '开放' },
  { name: '综合足球场', type: '足球', capacity: 60, status: '开放' },
  { name: '羽毛球馆', type: '羽毛球', capacity: 50, status: '开放' },
  { name: '乒乓球馆', type: '乒乓球', capacity: 30, status: '开放' },
  { name: '校园健身房', type: '健身', capacity: 80, status: '开放' },
  { name: '南区篮球场', type: '篮球', capacity: 30, status: '开放' },
  { name: '网球场', type: '网球', capacity: 24, status: '维护' },
  { name: '田径场', type: '田径', capacity: 120, status: '开放' }
];

const escapeHtml = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
}[c]));

const loadScript = url => new Promise((resolve, reject) => {
  const s = document.createElement('script');
  s.src = url;
  s.onload = () => resolve();
  s.onerror = () => reject(new Error('load failed: ' + url));
  document.head.appendChild(s);
});

const showStatus = msg => {
  const $s = $('#status');
  if ($s.length) $s.text(msg).show();
};

const statCards = items => items.map(s => `
  <div class="col-6 col-lg-3">
    <div class="card h-100">
      <div class="card-body">
        <div style="width: 34px; height: 4px; border-radius: 4px; background: ${s.color}; margin-bottom: 12px;"></div>
        <div class="text-muted small">${s.label}</div>
        <div class="h3 mb-0 fw-bold">${s.value}</div>
      </div>
    </div>
  </div>
`).join('');

const computeStats = () => {
  const types = [...new Set(venues.map(v => v.type))];
  const totalCapacity = venues.reduce((s, v) => s + Number(v.capacity || 0), 0);
  const openCount = venues.filter(v => v.status === '开放').length;
  let maxVenue = venues[0];
  venues.forEach(v => {
    if (Number(v.capacity || 0) > Number(maxVenue.capacity || 0)) maxVenue = v;
  });
  return { types, totalCapacity, openCount, maxVenue };
};

// ============ 首页 (index.html) ============

const renderIndex = () => {
  if (!$('#stats-cards').length) return;

  if (venues.length === 0) {
    showStatus('暂无场馆数据,请检查 data/venues.json。');
    return;
  }

  const { types, totalCapacity, openCount } = computeStats();

  $('#stats-cards').html(statCards([
    { label: '场馆数量', value: venues.length, color: '#0d6efd' },
    { label: '运动类型', value: types.length, color: '#198754' },
    { label: '总容量', value: totalCapacity, color: '#fd7e14' },
    { label: '当前开放', value: openCount, color: '#6f42c1' }
  ]));

  const cards = venues.slice(0, 6).map(v => `
    <div class="col-md-6 col-lg-4">
      <div class="card h-100">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-start">
            <div style="font-size: 28px;">${ICONS[v.type] || '🏟️'}</div>
            <span class="status-badge ${v.status === '开放' ? 'status-open' : 'status-maintenance'}">${escapeHtml(v.status)}</span>
          </div>
          <h3 class="h6 mt-3 mb-1">${escapeHtml(v.name)}</h3>
          <p class="text-muted small mb-1">${escapeHtml(v.location)} · ${escapeHtml(v.type)}</p>
          <p class="text-muted small mb-2">开放时间：${escapeHtml(v.hours)}</p>
          <a class="btn btn-sm btn-outline-primary" href="venues.html">查看场馆</a>
        </div>
      </div>
    </div>
  `).join('');

  $('#venue-list').html(cards);
};

// ============ 场馆 (venues.html) ============

const renderVenuesList = (list, total) => {
  if ($('#venue-list').length === 0 || $('#detail-modal').length === 0) return;

  $('#result-count').text('共 ' + list.length + ' 个场馆');
  $('#empty-state').toggle(total === 0);
  $('#no-result').toggle(list.length === 0 && total > 0);

  $('#venue-list').html(list.map(v => `
    <div class="col-md-6 col-xl-4">
      <div class="card h-100">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <div style="font-size: 28px;">${ICONS[v.type] || '🏟️'}</div>
            <span class="status-badge ${v.status === '开放' ? 'status-open' : 'status-maintenance'}">${escapeHtml(v.status)}</span>
          </div>
          <h2 class="h6 mb-2">${escapeHtml(v.name)}</h2>
          <p class="text-muted small mb-1">${escapeHtml(v.type)} · ${escapeHtml(v.location)}</p>
          <p class="text-muted small mb-3">${escapeHtml(v.hours)} · 容量 ${Number(v.capacity || 0)} 人</p>
          <button class="btn btn-outline-primary btn-sm detail-btn" data-id="${escapeHtml(v.id)}">查看详情</button>
        </div>
      </div>
    </div>
  `).join(''));
};

const filterVenues = () => {
  if ($('#search-input').length === 0) return;

  const keyword = $('#search-input').val().trim();
  const type = $('#type-select').val();
  const status = $('#status-select').val();

  $('#input-error').hide();
  if (keyword.length > 20) {
    $('#input-error').text('搜索内容不能超过 20 个字符。').show();
    return;
  }

  const result = venues.filter(v => {
    const matchText = !keyword ||
      (v.name && v.name.indexOf(keyword) !== -1) ||
      (v.type && v.type.indexOf(keyword) !== -1) ||
      (v.location && v.location.indexOf(keyword) !== -1);
    const matchType = type === '全部' || v.type === type;
    const matchStatus = status === '全部' || v.status === status;
    return matchText && matchType && matchStatus;
  });

  renderVenuesList(result, venues.length);
};

const showDetail = id => {
  const v = venues.find(x => String(x.id) === String(id));
  if (!v) return;

  $('#detail-title').text(v.name);
  const fields = [
    ['运动类型', v.type],
    ['位置', v.location],
    ['开放时间', v.hours],
    ['容纳人数', v.capacity + ' 人'],
    ['当前状态', v.status],
    ['场馆简介', v.description]
  ];
  const $body = $('#detail-content').empty();
  fields.forEach(([label, value]) => {
    $('<p>').append(
      $('<strong>').text(label + '：'),
      document.createTextNode(value == null ? '' : value)
    ).appendTo($body);
  });

  bootstrap.Modal.getOrCreateInstance($('#detail-modal')[0]).show();
};

const bindVenuesPageEvents = () => {
  if ($('#search-input').length === 0) return;

  $('#type-select').val('全部');
  $('#status-select').val('全部');
  $('#search-input').on('input', filterVenues);
  $('#type-select, #status-select').on('change', filterVenues);

  $('#reset-btn').click(() => {
    $('#search-input').val('');
    $('#type-select').val('全部');
    $('#status-select').val('全部');
    filterVenues();
  });

  $('#venue-list').click(e => {
    const $target = $(e.target);
    if (!$target.hasClass('detail-btn')) return;
    showDetail($target.data('id'));
  });
};

// ============ 数据统计 (data.html) ============

const getTypes = () => [...new Set(venues.map(v => v.type))];
const getCounts = () => getTypes().map(t => venues.filter(v => v.type === t).length);

const renderBarFallback = (types, counts) => {
  if (types.length === 0) {
    $('#bar-chart').empty();
    return;
  }
  const max = Math.max(...counts, 1);
  const html = types.map((t, i) => {
    const h = Math.max(20, counts[i] / max * 180);
    return `
        <div class="bar-item">
          <div class="bar-value">${counts[i]}</div>
          <div class="bar" style="height: ${h}px;"></div>
          <div class="bar-name">${escapeHtml(t)}</div>
        </div>`;
  }).join('');
  $('#bar-chart').html('<div class="bar-chart-fallback">' + html + '</div>');
};

let barChartInstance = null;
const renderBarECharts = (types, counts) => {
  if (!window.echarts || types.length === 0) return;
  if (barChartInstance) {
    barChartInstance.dispose();
    barChartInstance = null;
  }
  $('#bar-chart').empty();
  barChartInstance = echarts.init(document.getElementById('bar-chart'));
  barChartInstance.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: 40, right: 20, top: 20, bottom: 40 },
    xAxis: { type: 'category', data: types },
    yAxis: { type: 'value', minInterval: 1 },
    series: [{ type: 'bar', data: counts }]
  });
};

const renderLineFallback = () => {
  const canvas = document.getElementById('line-chart');
  if (!canvas || venues.length === 0) return;

  const wrap = canvas.parentElement;
  const width = wrap.clientWidth || 500;
  const height = 300;
  const dpr = window.devicePixelRatio || 1;
  const left = 45, right = 20, top = 20, bottom = 55;

  // 动态算 max,避免硬编码 120 导致容量超过时出界
  const max = Math.max(...venues.map(v => Number(v.capacity || 0)), 10);
  // 守卫 venues.length === 1 时 step 为 0,避免除零
  const step = venues.length > 1 ? (width - left - right) / (venues.length - 1) : 0;

  canvas.width = width * dpr;
  canvas.height = height * dpr;
  canvas.style.width = width + 'px';
  canvas.style.height = height + 'px';

  const ctx = canvas.getContext('2d');
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, width, height);

  // 网格
  ctx.strokeStyle = '#dfe6ee';
  ctx.lineWidth = 1;
  for (let y = 0; y <= 3; y++) {
    const gy = top + y * 75;
    ctx.beginPath();
    ctx.moveTo(left, gy);
    ctx.lineTo(width - right, gy);
    ctx.stroke();
  }

  // 折线
  ctx.strokeStyle = '#2f6fed';
  ctx.lineWidth = 3;
  ctx.beginPath();
  venues.forEach((v, i) => {
    const x = left + i * step;
    const y = height - bottom - Number(v.capacity || 0) / max * (height - top - bottom);
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.stroke();

  // 数据点 + 标签
  venues.forEach((v, i) => {
    const x = left + i * step;
    const y = height - bottom - Number(v.capacity || 0) / max * (height - top - bottom);
    ctx.fillStyle = '#2f6fed';
    ctx.beginPath();
    ctx.arc(x, y, 4, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#71808e';
    ctx.font = '11px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(v.name, x, height - 18);
  });
};

let lineChartInstance = null;
const renderLineChartJs = () => {
  const canvas = document.getElementById('line-chart');
  if (!canvas || !window.Chart || venues.length === 0) return;

  if (lineChartInstance) {
    lineChartInstance.destroy();
    lineChartInstance = null;
  }

  lineChartInstance = new Chart(canvas, {
    type: 'line',
    data: {
      labels: venues.map(v => v.name),
      datasets: [{
        label: '容纳人数',
        data: venues.map(v => Number(v.capacity || 0)),
        borderWidth: 2,
        tension: 0.25
      }]
    },
    options: { responsive: true, maintainAspectRatio: false }
  });
};

const renderStats = () => {
  if ($('#bar-chart').length === 0) return;

  if (venues.length === 0) {
    showStatus('暂无场馆数据');
    return;
  }

  const { types, totalCapacity, openCount, maxVenue } = computeStats();

  $('#stats-cards').html(statCards([
    { label: '场馆数量', value: venues.length, color: '#0d6efd' },
    { label: '运动类型', value: types.length, color: '#198754' },
    { label: '总容量', value: totalCapacity, color: '#fd7e14' },
    { label: '当前开放', value: openCount, color: '#6f42c1' }
  ]));

  $('#largest-venue').text(maxVenue.name + '（' + maxVenue.capacity + ' 人）');

  const counts = getCounts();

  // fallback 总是先渲染,确保 CDN 失败时也能看到图表
  renderBarFallback(types, counts);
  renderLineFallback();

  // 覆盖 fallback(如果库可用)
  if (window.echarts) renderBarECharts(types, counts);
  if (window.Chart) renderLineChartJs();
};

// CDN 库加载完后,如果数据也已就绪,补一次图表渲染
const retryStatsCharts = () => {
  if (venues.length === 0) return;
  const types = getTypes();
  const counts = getCounts();
  if (window.echarts) renderBarECharts(types, counts);
  if (window.Chart) renderLineChartJs();
};

// ============ 三维展示 (scene.html) ============

let fallbackCleanup = null;
let threeResizeListener = null;

const startThree = box => {
  if (!window.THREE) return;

  // 清理 fallback 监听器
  if (fallbackCleanup) {
    fallbackCleanup();
    fallbackCleanup = null;
  }
  if (threeResizeListener) {
    window.removeEventListener('resize', threeResizeListener);
    threeResizeListener = null;
  }
  box.innerHTML = '';

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0xdce8f0);

  const camera = new THREE.PerspectiveCamera(45, box.clientWidth / box.clientHeight, 0.1, 100);
  camera.position.set(8, 7, 9);

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(box.clientWidth, box.clientHeight);
  box.appendChild(renderer.domElement);

  let controls = null;
  if (THREE.OrbitControls) {
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.target.set(0, 0, 0);
    controls.minDistance = 6;
    controls.maxDistance = 18;
  } else {
    showStatus('OrbitControls 加载失败,场景可看但不能拖动。');
  }

  scene.add(new THREE.AmbientLight(0xffffff, 0.8));
  const light = new THREE.DirectionalLight(0xffffff, 1.1);
  light.position.set(5, 10, 6);
  scene.add(light);

  // 地面
  const floor = new THREE.Mesh(
    new THREE.PlaneGeometry(18, 18),
    new THREE.MeshStandardMaterial({ color: 0xb9c9b3 })
  );
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = -0.2;
  scene.add(floor);

  // 球场底座
  const base = new THREE.Mesh(
    new THREE.BoxGeometry(8.6, 0.3, 14),
    new THREE.MeshStandardMaterial({ color: 0x4e5966 })
  );
  base.position.y = -0.05;
  scene.add(base);

  // 球场
  const court = new THREE.Mesh(
    new THREE.BoxGeometry(7.6, 0.18, 13),
    new THREE.MeshStandardMaterial({ color: 0xc9854e })
  );
  court.position.y = 0.18;
  scene.add(court);

  const lineMaterial = new THREE.LineBasicMaterial({ color: 0xffffff });
  const addLine = points => {
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    scene.add(new THREE.Line(geometry, lineMaterial));
  };

  addLine([
    new THREE.Vector3(-3.8, 0.3, -6.5),
    new THREE.Vector3(3.8, 0.3, -6.5),
    new THREE.Vector3(3.8, 0.3, 6.5),
    new THREE.Vector3(-3.8, 0.3, 6.5),
    new THREE.Vector3(-3.8, 0.3, -6.5)
  ]);
  addLine([new THREE.Vector3(0, 0.3, -6.5), new THREE.Vector3(0, 0.3, 6.5)]);

  const circle = new THREE.LineLoop(
    new THREE.CircleGeometry(1.15, 48),
    lineMaterial
  );
  circle.rotation.x = -Math.PI / 2;
  circle.position.y = 0.31;
  scene.add(circle);

  // 篮球架
  const addHoop = z => {
    const pole = new THREE.Mesh(
      new THREE.CylinderGeometry(0.08, 0.08, 3, 16),
      new THREE.MeshStandardMaterial({ color: 0x34495e })
    );
    pole.position.set(0, 1.7, z);
    scene.add(pole);

    const board = new THREE.Mesh(
      new THREE.BoxGeometry(1.8, 1.1, 0.08),
      new THREE.MeshStandardMaterial({ color: 0xf4f4f4 })
    );
    board.position.set(0, 3.0, z);
    scene.add(board);

    const rim = new THREE.Mesh(
      new THREE.TorusGeometry(0.32, 0.045, 12, 32),
      new THREE.MeshStandardMaterial({ color: 0xe05a3f })
    );
    rim.rotation.x = Math.PI / 2;
    rim.position.set(0, 2.45, z + (z > 0 ? -0.28 : 0.28));
    scene.add(rim);
  };
  addHoop(-5.8);
  addHoop(5.8);

  // 篮球
  const ball = new THREE.Mesh(
    new THREE.SphereGeometry(0.28, 24, 16),
    new THREE.MeshStandardMaterial({ color: 0xe67e22 })
  );
  ball.position.set(1.3, 0.55, 0.8);
  scene.add(ball);

  const animate = () => {
    requestAnimationFrame(animate);
    if (controls) controls.update();
    ball.rotation.x += 0.006;
    ball.rotation.z += 0.008;
    renderer.render(scene, camera);
  };
  animate();

  threeResizeListener = () => {
    camera.aspect = box.clientWidth / box.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(box.clientWidth, box.clientHeight);
  };
  window.addEventListener('resize', threeResizeListener);
};

const startFallback = box => {
  box.innerHTML = '';
  const canvas = document.createElement('canvas');
  box.appendChild(canvas);
  const ctx = canvas.getContext('2d');

  let angle = 0, zoom = 1, dragging = false, lastX = 0;

  const resize = () => {
    const dpr = window.devicePixelRatio || 1;
    canvas.width = box.clientWidth * dpr;
    canvas.height = box.clientHeight * dpr;
    canvas.style.width = box.clientWidth + 'px';
    canvas.style.height = box.clientHeight + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    draw();
  };

  const draw = () => {
    const w = box.clientWidth;
    const h = box.clientHeight;
    const scale = Math.min(w / 760, h / 500) * zoom;
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#dce8f0';
    ctx.fillRect(0, 0, w, h);

    ctx.save();
    ctx.translate(w / 2, h * 0.52);
    ctx.rotate(angle * 0.06);
    ctx.transform(1, 0.22, 0, 0.68, 0, 0);
    ctx.scale(scale, scale);

    ctx.fillStyle = '#4e5966';
    ctx.fillRect(-260, -205, 520, 410);
    ctx.fillStyle = '#c9854e';
    ctx.fillRect(-230, -190, 460, 380);
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 4;
    ctx.strokeRect(-230, -190, 460, 380);
    ctx.beginPath();
    ctx.moveTo(0, -190);
    ctx.lineTo(0, 190);
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(0, 0, 70, 0, Math.PI * 2);
    ctx.stroke();

    ctx.fillStyle = '#f4f4f4';
    ctx.fillRect(-70, -190, 140, 8);
    ctx.fillRect(-70, 182, 140, 8);
    ctx.fillStyle = '#e05a3f';
    ctx.beginPath();
    ctx.arc(0, -182, 20, 0, Math.PI * 2);
    ctx.arc(0, 182, 20, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    ctx.fillStyle = '#17324d';
    ctx.font = 'bold 18px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('篮球场三维示意', w / 2, 30);
    ctx.font = '13px sans-serif';
    ctx.fillStyle = '#71808e';
    ctx.fillText('拖动旋转 · 滚轮缩放', w / 2, h - 18);
  };

  canvas.onmousedown = e => { dragging = true; lastX = e.clientX; };
  canvas.onmousemove = e => {
    if (!dragging) return;
    angle += (e.clientX - lastX) / 80;
    lastX = e.clientX;
    draw();
  };
  canvas.onmouseup = () => { dragging = false; };
  canvas.onwheel = e => {
    e.preventDefault();
    zoom += e.deltaY < 0 ? 0.08 : -0.08;
    zoom = Math.max(0.75, Math.min(1.35, zoom));
    draw();
  };

  window.addEventListener('resize', resize);
  resize();

  fallbackCleanup = () => {
    window.removeEventListener('resize', resize);
    canvas.onmousedown = null;
    canvas.onmousemove = null;
    canvas.onmouseup = null;
    canvas.onwheel = null;
  };
};

const renderScene = () => {
  if ($('#three-box').length === 0) return;

  const box = $('#three-box')[0];

  // 总是先渲染 fallback,避免 CDN 加载中页面空白
  startFallback(box);

  // 异步加载 Three.js + OrbitControls(OrbitControls 本地化避免 CDN 路径不稳)
  loadScript('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js')
    .then(() => loadScript('libs/OrbitControls.js').catch(() => null))
    .then(() => startThree(box))
    .catch(err => {
      console.warn('Three.js 加载失败,继续使用 fallback:', err);
      showStatus('三维库加载失败,当前显示静态示意。如需 3D 效果,请检查网络后刷新。');
    });
};

// ============ 启动 ============

let venues = [];
let echartsLoaded = false;
let chartJsLoaded = false;

$(function () {
  // nav 当前项高亮
  $('.navbar .nav-link.active').attr('aria-current', 'page');

  // 异步加载 ECharts / Chart.js (data 页用)
  loadScript('https://cdn.jsdelivr.net/npm/echarts@5.6.0/dist/echarts.min.js')
    .then(() => { echartsLoaded = true; retryStatsCharts(); })
    .catch(() => console.warn('ECharts 加载失败,使用本地柱状图 fallback'));

  loadScript('https://cdn.jsdelivr.net/npm/chart.js@4.5.0/dist/chart.umd.min.js')
    .then(() => { chartJsLoaded = true; retryStatsCharts(); })
    .catch(() => console.warn('Chart.js 加载失败,使用 Canvas 折线图 fallback'));

  // 加载 JSON 数据
  // 注意:libs/jquery 是 slim build,没有 ajax 模块,所以用原生 fetch
  fetch('data/venues.json')
    .then(r => {
      if (!r.ok) throw new Error('http ' + r.status);
      return r.json();
    })
    .then(data => {
      if (!Array.isArray(data) || data.length === 0) {
        showStatus('本地 JSON 数据为空,请检查 data/venues.json。');
        return;
      }
      venues = data;
      tryRenderAll();
    })
    .catch(() => {
      venues = DEFAULT_DATA;
      showStatus('本地 JSON 加载失败,当前显示备用数据。');
      tryRenderAll();
    });
});

const tryRenderAll = () => {
  renderIndex();
  renderStats();
  renderVenuesList(venues, venues.length);
  renderScene();
  bindVenuesPageEvents();
};