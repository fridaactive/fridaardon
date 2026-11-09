/*
 * Modo de prueba local del portal de clientas (solo para desarrollo).
 * Reemplaza Firebase por datos inventados en memoria para poder ver y probar
 * cada pantalla sin conexión y sin tocar datos reales. NO se carga en la web
 * publicada: solo lo inyecta el script de capturas (dev/capturas.js).
 */
(function () {
  var UID = 'demo-uid';
  var CLIENT = 'demo-client';
  var today = new Date();
  var monthKey = today.getFullYear() + '-' + String(today.getMonth() + 1).padStart(2, '0');
  function dk(offset) {
    var d = new Date(today); d.setDate(d.getDate() - offset);
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
  }
  var dias = {}; [0, 1, 2, 4, 6, 8, 9, 11].forEach(function (o) { dias[dk(o)] = true; });

  var DATA = {
    clientasPortal: {}, rutinas: {}, clients: {},
    exerciseBank: {
      b1: { nombre: 'Sentadilla búlgara', video: '', descripcion: 'Baja controlado, rodilla alineada con el pie.' },
      b2: { nombre: 'Hip thrust', video: '', descripcion: 'Aprieta glúteos arriba 1 segundo.' },
      b3: { nombre: 'Peso muerto rumano', video: '', descripcion: 'Espalda neutra, cadera atrás.' }
    },
    beneficios: {
      be1: { marca: 'Productos Tu Madre', descuento: '15% de descuento', descripcion: 'En bowls y shakes.', categoria: 'Comida saludable', logoUrl: 'FA_logozul-07.png', fotos: ['hero-frida.jpg'] },
      be2: { marca: 'Gym Wear SV', descuento: '10% en ropa deportiva', descripcion: 'Leggings y tops.', categoria: 'Ropa', logo: '' }
    },
    anuncios: { an1: { texto: '¡Nuevo programa Core en 15 días muy pronto!', activo: true } },
    linkCodes: {}, client_links: {}, landingLeads: {}
  };
  DATA.clientasPortal[UID] = {
    perfil: { nombre: 'Andrea Martínez', clientId: CLIENT, bio: 'Quiero sentirme fuerte y con energía.', fotoPerfil: '' },
    diasEntrenados: dias,
    chat: { m1: { from: 'admin', text: '¡Hola Andrea! ¿Cómo te sentiste con la rutina?', ts: Date.now() - 86400000 } },
    chatMeta: { lastReadByClient: 0 },
    entrenoLogs: {}, progreso: {}, ficha: { edad: 31 }
  };
  DATA.clients[CLIENT] = {
    name: 'Andrea Martínez', type: 'rutina-personalizada', initDate: dk(20), days: 4, sesionesMes: 12, status: 'activa'
  };
  function ex(id, name, series, reps, extra) { return Object.assign({ id: id, name: name, series: series, reps: reps }, extra || {}); }
  DATA.rutinas[CLIENT] = {
    mensajeInicial: '¡Bienvenida a tu rutina de noviembre! Vamos con todo 💪',
    aclaraciones: ['Calienta 5 minutos antes de empezar.', 'Descansa 60 a 90 segundos entre series.'],
    days: [
      { id: 'd1', name: 'Pierna y glúteo', notaAdmin: 'Enfócate en la técnica.', blocks: [
        { id: 'k1', name: 'Bloque 1', restSecs: 60, exercises: [ex('e1', 'Sentadilla búlgara', '4', '10'), ex('e2', 'Hip thrust', '4', '12')] },
        { id: 'k2', name: 'Bloque 2', restSecs: 45, mode: 'tiempo', workSecs: 40, exercises: [ex('e3', 'Peso muerto rumano', '3', '12'), ex('e4', 'Plancha', '3', '', { tipo: 'tiempo', segundos: 40 })] }
      ] },
      { id: 'd2', name: 'Espalda y brazos', blocks: [
        { id: 'k3', name: 'Bloque 1', restSecs: 60, exercises: [ex('e5', 'Remo con mancuerna', '4', '12'), ex('e6', 'Curl de bíceps', '3', '15')] }
      ] },
      { id: 'd3', name: 'Full body', blocks: [
        { id: 'k4', name: 'Circuito', restSecs: 30, exercises: [ex('e7', 'Burpees', '3', '10'), ex('e8', 'Sentadilla con salto', '3', '12')] }
      ] }
    ]
  };

  function get(path) {
    var parts = String(path || '').split('/').filter(Boolean), cur = DATA;
    for (var i = 0; i < parts.length; i++) { if (cur == null) return null; cur = cur[parts[i]]; }
    return cur === undefined ? null : JSON.parse(JSON.stringify(cur));
  }
  function set(path, val) {
    var parts = String(path || '').split('/').filter(Boolean), cur = DATA;
    for (var i = 0; i < parts.length - 1; i++) { cur[parts[i]] = cur[parts[i]] || {}; cur = cur[parts[i]]; }
    if (parts.length) cur[parts[parts.length - 1]] = val;
  }
  function snap(path) { var v = get(path); return { val: function () { return v; }, exists: function () { return v !== null; }, key: path.split('/').pop(), forEach: function (cb) { if (v && typeof v === 'object') Object.keys(v).forEach(function (k) { cb({ key: k, val: function () { return v[k]; } }); }); } }; }
  function ref(path) {
    path = path || '';
    var r = {
      once: function () { return Promise.resolve(snap(path)); },
      on: function (evt, cb) { var v = get(path); if (evt === 'child_added' && v) Object.keys(v).forEach(function (k) { cb({ key: k, val: function () { return v[k]; } }); }); else if (evt === 'value') cb(snap(path)); return cb; },
      off: function () {},
      set: function (v) { set(path, v); return Promise.resolve(); },
      update: function (obj) { Object.keys(obj).forEach(function (k) { set((path ? path + '/' : '') + k, obj[k]); }); return Promise.resolve(); },
      push: function (v) { var k = 'k' + Date.now() + Math.random().toString(36).slice(2, 6); if (v !== undefined) set(path + '/' + k, v); var c = ref(path + '/' + k); c.key = k; c.then = function (f) { return Promise.resolve().then(f); }; return c; },
      remove: function () { set(path, null); return Promise.resolve(); },
      child: function (p) { return ref(path + '/' + p); },
      orderByChild: function () { return r; }, equalTo: function () { return r; }, limitToLast: function () { return r; },
      transaction: function (fn) { set(path, fn(get(path))); return Promise.resolve(); }
    };
    return r;
  }
  var user = { uid: UID, email: 'andrea@demo.com', emailVerified: true, getIdToken: function () { return Promise.resolve('t'); }, reload: function () { return Promise.resolve(); } };
  var auth = {
    currentUser: user,
    onAuthStateChanged: function (cb) { setTimeout(function () { cb(user); }, 50); return function () {}; },
    signInWithEmailAndPassword: function () { return Promise.resolve({ user: user }); },
    createUserWithEmailAndPassword: function () { return Promise.resolve({ user: user }); },
    sendPasswordResetEmail: function () { return Promise.resolve(); },
    signOut: function () { return Promise.resolve(); },
    setPersistence: function () { return Promise.resolve(); }
  };
  window.firebase = {
    apps: [],
    initializeApp: function () { this.apps.push({}); return {}; },
    auth: Object.assign(function () { return auth; }, { Auth: { Persistence: { LOCAL: 'local' } } }),
    database: Object.assign(function () { return { ref: ref }; }, { ServerValue: { TIMESTAMP: Date.now() } }),
    storage: function () { return { ref: function () { return { put: function () { return Promise.resolve({ ref: { getDownloadURL: function () { return Promise.resolve(''); } } }); } }; } }; }
  };
  window.__MOCK_DATA__ = DATA;
})();
