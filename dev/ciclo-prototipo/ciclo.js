// MI CICLO · tarjeta "Tu energía de hoy". cicloCardHtml({ dia, largo, sentir })
//   dia: día del ciclo (1 = primer día del período), largo: duración promedio (28 por defecto),
//   sentir: 1..5 lo que la clienta marcó hoy (opcional; ajusta la batería a lo que ella siente).
var CY_FASES = {
  menstrual: { tag:'Fase menstrual', name:'Modo <span>recarga</span>', icon:'🌙', base:30, intens:2,
    glow:'rgba(255,120,130,.35)', accent:'#FF9AA5', chip:'#FFD6DA', ink:'#5A1420', fill:['#FF8F9B','#E8546A'],
    msg:'Tu energía puede estar más baja estos días. Moverte suave también cuenta: hoy escucha a tu cuerpo.',
    ideal:'Movilidad, caminata o fuerza ligera', cuida:'Hidrátate y descansa bien',
    sci:'Al inicio del ciclo, estrógeno y progesterona están en su punto más bajo; muchas mujeres sienten menos energía o molestias.' },
  folicular: { tag:'Fase folicular', name:'Energía en <span>subida</span>', icon:'🌱', base:70, intens:4,
    glow:'rgba(91,139,245,.4)', accent:'#9DBBFF', chip:'#D8E4FF', ink:'#0F2E78', fill:['#8FB0FF','#3A6CF0'],
    msg:'Tu cuerpo se está recargando. Es un gran momento para retarte y subirle un poquito al peso.',
    ideal:'Fuerza y subir cargas', cuida:'Calienta bien antes de pesado',
    sci:'El estrógeno va subiendo: muchas mujeres se sienten con más energía y se recuperan mejor entre entrenos.' },
  ovulacion: { tag:'Ovulación', name:'Tu pico de <span>poder</span>', icon:'⚡', base:95, intens:5,
    glow:'rgba(245,236,203,.5)', accent:'#F5ECCB', chip:'#F5ECCB', ink:'#3d330c', fill:['#FFF3C4','#F4C542'],
    msg:'¡Batería a tope! Si te sientes así, hoy es el día para dar lo mejor de ti en el gym.',
    ideal:'Entreno intenso o tu mejor marca', cuida:'Técnica y calentamiento',
    sci:'Alrededor de la ovulación el estrógeno llega a su pico; es cuando muchas se sienten más fuertes y con más ánimo.' },
  lutea: { tag:'Fase lútea', name:'Modo <span>constante</span>', icon:'🍂', base:50, intens:3,
    glow:'rgba(214,170,120,.35)', accent:'#F0C79A', chip:'#F6DFC6', ink:'#4A2E0E', fill:['#F3CFA3','#C98A4E'],
    msg:'La energía va bajando poco a poco. Mantén tu rutina a tu ritmo: la constancia es lo que da resultados.',
    ideal:'Tu rutina normal, sin forzar', cuida:'Duerme bien y come suficiente',
    sci:'La progesterona sube y puede dar más cansancio, calor o antojos; es normal y no significa que estés fallando.' }
};
// Cómo se siente hoy: caritas dibujadas (SVG propio) y un consejo para cada una.
var CY_SENTIR = [
  { id:'dolor', label:'Con dolor', val:1, fill:'#FFD6DA',
    face:'<path d="M12 15l4 2M28 15l-4 2" /><path d="M13 21l3 2-3 2M27 21l-3 2 3 2"/><path d="M14 31q3-3 6 0t6 0"/><path d="M33 7l1.5 3M36 11l-3 .5" stroke="#E8546A"/>',
    tip:'Si tienes cólicos, hoy prioriza moverte suave: caminar, estiramientos o movilidad. El calor en el vientre ayuda a muchas. Si el dolor es muy fuerte, descansa y consulta a tu médico.' },
  { id:'nauseas', label:'Con náuseas', val:1, fill:'#DDF3CC',
    face:'<path d="M13 19h5M22 19h5"/><path d="M14 29q2-2 4 0t4 0t4 0"/><path d="M31 11q1.5 2.5 0 4q-1.5-1.5 0-4z" fill="#7CC4F0" stroke="#7CC4F0"/>',
    tip:'Hoy toma agua a sorbos, come algo ligero y, si te animas, haz algo suave. No pasa nada si hoy solo descansas.' },
  { id:'cansada', label:'Cansada', val:2, fill:'#E4E8F7',
    face:'<path d="M12 20q3 2 6 0M22 20q3 2 6 0"/><path d="M17 29h6"/><text x="29" y="12" font-size="8" font-weight="800" fill="#0B1B3F" stroke="none">z</text>',
    tip:'Haz tu rutina más ligera: menos series o menos peso también suma. Y esta noche, a dormir temprano.' },
  { id:'bien', label:'Bien', val:4, fill:'#F5ECCB',
    face:'<path d="M12 20q3-3 6 0M22 20q3-3 6 0"/><path d="M14 27q6 5 12 0"/>',
    tip:'¡Qué bueno! Haz tu rutina normal y disfrútala.' },
  { id:'contodo', label:'¡Con todo!', val:5, fill:'#FFF0B8',
    face:'<path d="M15 15l1 2.2 2.3.3-1.7 1.6.4 2.3-2-1.1-2 1.1.4-2.3-1.7-1.6 2.3-.3z" fill="#0B1B3F"/><path d="M25 15l1 2.2 2.3.3-1.7 1.6.4 2.3-2-1.1-2 1.1.4-2.3-1.7-1.6 2.3-.3z" fill="#0B1B3F"/><path d="M13 26q7 8 14 0z" fill="#0B1B3F"/><path d="M34 4l-3 6h2.5l-1.5 5 4.5-7H34l1.5-4z" fill="#F4C542" stroke="#B07D10" stroke-width=".8"/>',
    tip:'¡Aprovéchala! Hoy es un gran día para retarte un poquito más.' }
];
function cicloCaraSvg(s) {
  return '<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="21" r="16" fill="' + s.fill + '" stroke="#0B1B3F" stroke-width="2"/>'
    + '<g fill="none" stroke="#0B1B3F" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">' + s.face + '</g></svg>';
}
function cicloSentirInfo(id) { for (var i = 0; i < CY_SENTIR.length; i++) if (CY_SENTIR[i].id === id) return CY_SENTIR[i]; return null; }
function cicloFase(dia, largo) {
  largo = largo || 28; var ov = largo - 14;
  if (dia <= 5) return 'menstrual';
  if (dia < ov - 1) return 'folicular';
  if (dia <= ov + 1) return 'ovulacion';
  return 'lutea';
}
function cicloEnergia(dia, largo, sentir) {
  var f = CY_FASES[cicloFase(dia, largo)], e = f.base;
  var si = cicloSentirInfo(sentir);
  if (si) e = Math.round(e * 0.4 + (si.val - 1) / 4 * 100 * 0.6); // lo que ella siente pesa más
  return Math.max(8, Math.min(100, e));
}
function cicloBateriaSvg(pct, key, uid) {
  var f = CY_FASES[key], top = 18 + (1 - pct / 100) * 120, g = 'cyg' + uid, c = 'cyc' + uid;
  var wave = function(y, cls, op) {
    return '<path class="' + cls + '" opacity="' + op + '" d="M0 ' + y + ' q15 -8 30 0 t30 0 t30 0 t30 0 t30 0 V160 H0 Z" fill="url(#' + g + ')"/>';
  };
  var bubbles = '';
  for (var i = 0; i < 5; i++) bubbles += '<circle class="cy-bub" cx="' + (22 + i * 12) + '" cy="132" r="' + (2 + (i % 3)) + '" fill="#fff" style="--t:' + (2.4 + i * .5) + 's;--d:' + (i * .6) + 's"/>';
  var extra = key === 'ovulacion' || key === 'folicular'
    ? '<path class="cy-bolt" d="M50 30 L38 54 h9 l-5 18 l15 -25 h-9 l6 -17 z" fill="#fff" opacity=".9"/>'
    : key === 'menstrual' ? '<text class="cy-zz" x="62" y="42" font-size="14" font-weight="800" fill="#fff">z</text><text class="cy-zz" x="70" y="30" font-size="10" font-weight="800" fill="#fff" style="animation-delay:.8s">z</text>' : '';
  return '<svg viewBox="0 0 92 150" aria-hidden="true"><defs>'
    + '<linearGradient id="' + g + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="' + f.fill[0] + '"/><stop offset="1" stop-color="' + f.fill[1] + '"/></linearGradient>'
    + '<clipPath id="' + c + '"><rect x="9" y="14" width="74" height="130" rx="20"/></clipPath></defs>'
    + '<rect x="32" y="2" width="28" height="12" rx="5" fill="rgba(255,255,255,.55)"/>'
    + '<rect x="5" y="10" width="82" height="138" rx="24" fill="rgba(255,255,255,.06)" stroke="rgba(255,255,255,.75)" stroke-width="3"/>'
    + '<g clip-path="url(#' + c + ')">' + wave(top + 4, 'cy-wave2', .6) + wave(top, 'cy-wave', 1) + bubbles + '</g>'
    + '<path d="M18 30 Q16 60 18 96" stroke="#fff" stroke-opacity=".35" stroke-width="4" stroke-linecap="round" fill="none"/>'
    + extra + '</svg>';
}
var CY_N = 0;
function cicloCardHtml(o) {
  var dia = o.dia, largo = o.largo || 28, key = cicloFase(dia, largo), f = CY_FASES[key];
  var pct = cicloEnergia(dia, largo, o.sentir), uid = ++CY_N, falta = largo - dia + 1;
  var ov = largo - 14, seg = function(n, col) { return '<i style="width:' + (n / largo * 100) + '%;background:' + col + '"></i>'; };
  var h = '<div class="cy-card" style="--cy-glow:' + f.glow + ';--cy-accent:' + f.accent + ';--cy-chip:' + f.chip + ';--cy-ink:' + f.ink + '">';
  h += '<div class="cy-top"><div class="cy-batt">' + cicloBateriaSvg(pct, key, uid) + '<div class="cy-pct">' + pct + '<small>%</small></div></div>';
  h += '<div class="cy-info"><span class="cy-tag">' + f.icon + ' ' + f.tag + '</span><div class="cy-name">' + f.name + '</div>';
  h += '<div class="cy-day">Día ' + dia + ' de ' + largo + ' · tu período llega en ' + falta + (falta === 1 ? ' día' : ' días') + '</div>';
  h += '<div class="cy-msg">' + f.msg + '</div></div></div>';
  h += '<div class="cy-wheel"><div class="cy-track">' + seg(5, '#E8546A') + seg(ov - 7, '#3A6CF0') + seg(3, '#F4C542') + seg(largo - ov - 1, '#C98A4E') + '</div>';
  h += '<div class="cy-now" style="left:' + ((dia - 0.5) / largo * 100) + '%">' + f.icon + '</div></div>';
  var lg = function(txt, col, k) { return '<span class="' + (k === key ? 'on' : '') + '"><i style="background:' + col + '"></i>' + txt + '</span>'; };
  h += '<div class="cy-legend">' + lg('Menstrual', '#E8546A', 'menstrual') + lg('Folicular', '#3A6CF0', 'folicular') + lg('Ovulación', '#F4C542', 'ovulacion') + lg('Lútea', '#C98A4E', 'lutea') + '</div>';
  var dots = ''; for (var i = 1; i <= 5; i++) dots += '<i class="' + (i <= f.intens ? 'on' : '') + '"></i>';
  h += '<div class="cy-plan"><div class="cy-box"><b>Ideal para hoy</b><span>' + f.ideal + '</span><div class="cy-dots">' + dots + '</div></div>';
  h += '<div class="cy-box"><b>Cuida</b><span>' + f.cuida + '</span></div></div>';
  var sel = cicloSentirInfo(o.sentir);
  h += '<div class="cy-feel"><p>¿Cómo te sientes hoy?</p><div class="cy-feel-row">';
  CY_SENTIR.forEach(function(si) { h += '<button type="button" class="' + (sel && sel.id === si.id ? 'sel' : '') + '" onclick="cicloSentir(\'' + si.id + '\')" aria-label="' + si.label + '">' + cicloCaraSvg(si) + '<span>' + si.label + '</span></button>'; });
  h += '</div>' + (sel ? '<div class="cy-feel-tip">💙 ' + sel.tip + '</div>' : '<small>Tu batería se ajusta a cómo te sientes. Cada cuerpo es distinto 💙</small>') + '</div>';
  h += '<div class="cy-sci">🔬 ' + f.sci + ' Son guías generales: si algo no se siente bien, escucha a tu cuerpo.</div>';
  return h + '</div>';
}
