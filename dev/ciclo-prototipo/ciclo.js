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
function cicloFase(dia, largo) {
  largo = largo || 28; var ov = largo - 14;
  if (dia <= 5) return 'menstrual';
  if (dia < ov - 1) return 'folicular';
  if (dia <= ov + 1) return 'ovulacion';
  return 'lutea';
}
function cicloEnergia(dia, largo, sentir) {
  var f = CY_FASES[cicloFase(dia, largo)], e = f.base;
  if (sentir) e = Math.round(e * 0.4 + (sentir - 1) / 4 * 100 * 0.6); // lo que ella siente pesa más
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
  var caras = ['🪫', '😴', '😐', '🙂', '⚡'];
  h += '<div class="cy-feel"><p>¿Cómo sientes tu energía hoy?</p><div class="cy-feel-row">';
  caras.forEach(function(c, i) { h += '<button type="button" class="' + (o.sentir === i + 1 ? 'sel' : '') + '" onclick="cicloSentir(' + (i + 1) + ')" aria-label="Energía ' + (i + 1) + ' de 5">' + c + '</button>'; });
  h += '</div><small>Tu batería se ajusta a lo que tú sientes. Cada cuerpo es distinto 💙</small></div>';
  h += '<div class="cy-sci">🔬 ' + f.sci + ' Son guías generales: si algo no se siente bien, escucha a tu cuerpo.</div>';
  return h + '</div>';
}
