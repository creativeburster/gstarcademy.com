# -*- coding: utf-8 -*-
"""Extra quiz lessons: a visual "看图识操作" (identify-the-operation) image
lesson plus one advanced text lesson for each of the six career tracks.

Consumed by expand_quiz.py, which merges these into NEW_LESSONS and renders
them into quiz.js. Image questions carry an inline SVG diagram in the
``image`` field; the quiz engine renders it above the answer options.
"""

# --- inline SVG helpers -----------------------------------------------------

_S = ('<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg" '
      'role="img" aria-label="{alt}" style="background:#f8fafc">{body}</svg>')

_BLUE = "#2563eb"
_GREY = "#94a3b8"
_DARK = "#334155"
_RED = "#dc2626"


def _svg(alt, body):
    return _S.format(alt=alt, body=body)


def _label(x, y, text, anchor="middle", size=13, fill="#475569"):
    return ('<text x="{x}" y="{y}" text-anchor="{a}" font-family="Inter,'
            'sans-serif" font-size="{s}" fill="{f}">{t}</text>').format(
        x=x, y=y, a=anchor, s=size, f=fill, t=text)


# Reusable operation diagrams -------------------------------------------------

def sv_extrude():
    body = (
        '<rect x="40" y="70" width="70" height="70" fill="none" stroke="%s" stroke-width="2"/>' % _DARK +
        _label(75, 160, "2D profile") +
        '<path d="M150 105 h60" stroke="%s" stroke-width="2" marker-end="url(#a)"/>' % _BLUE +
        '<defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        '<path d="M0 0 L6 3 L0 6 z" fill="%s"/></marker></defs>' % _BLUE +
        # isometric box
        '<path d="M250 90 l60 0 l30 -25 l-60 0 z" fill="#dbeafe" stroke="%s" stroke-width="2"/>' % _BLUE +
        '<path d="M250 90 l0 60 l60 0 l0 -60 z" fill="#bfdbfe" stroke="%s" stroke-width="2"/>' % _BLUE +
        '<path d="M310 90 l30 -25 l0 60 l-30 25 z" fill="#93c5fd" stroke="%s" stroke-width="2"/>' % _BLUE +
        _label(300, 175, "solid")
    )
    return _svg("A 2D rectangle profile turned into a 3D box", body)


def sv_revolve():
    body = (
        '<line x1="120" y1="30" x2="120" y2="170" stroke="%s" stroke-width="1.5" stroke-dasharray="6 4"/>' % _RED +
        _label(120, 22, "axis", fill=_RED) +
        '<rect x="70" y="70" width="35" height="60" fill="none" stroke="%s" stroke-width="2"/>' % _DARK +
        '<path d="M170 100 a70 30 0 1 1 -2 0" fill="none" stroke="%s" stroke-width="2" marker-end="url(#r)"/>' % _BLUE +
        '<defs><marker id="r" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        '<path d="M0 0 L6 3 L0 6 z" fill="%s"/></marker></defs>' % _BLUE +
        '<ellipse cx="300" cy="100" rx="60" ry="55" fill="#dbeafe" stroke="%s" stroke-width="2"/>' % _BLUE +
        '<ellipse cx="300" cy="100" rx="25" ry="22" fill="#f8fafc" stroke="%s" stroke-width="2"/>' % _BLUE
    )
    return _svg("A profile swept 360 degrees around an axis to form a ring", body)


def sv_fillet():
    body = (
        '<path d="M60 40 L60 160 L180 160" fill="none" stroke="%s" stroke-width="6"/>' % _GREY +
        _label(120, 185, "before: sharp corner", fill=_GREY) +
        '<path d="M250 40 L250 130 Q250 160 280 160 L360 160" fill="none" stroke="%s" stroke-width="6"/>' % _BLUE +
        '<circle cx="278" cy="132" r="4" fill="%s"/>' % _RED +
        _label(305, 185, "after: rounded", fill=_BLUE)
    )
    return _svg("A sharp corner replaced by a smooth rounded arc", body)


def sv_chamfer():
    body = (
        '<path d="M60 40 L60 160 L180 160" fill="none" stroke="%s" stroke-width="6"/>' % _GREY +
        _label(120, 185, "before: sharp corner", fill=_GREY) +
        '<path d="M250 40 L250 130 L280 160 L360 160" fill="none" stroke="%s" stroke-width="6"/>' % _BLUE +
        _label(305, 185, "after: 45\u00b0 bevel", fill=_BLUE)
    )
    return _svg("A sharp corner replaced by an angled straight bevel", body)


def sv_mirror():
    body = (
        '<line x1="200" y1="20" x2="200" y2="180" stroke="%s" stroke-width="1.5" stroke-dasharray="6 4"/>' % _RED +
        _label(200, 195, "mirror line", fill=_RED) +
        '<path d="M120 60 L170 60 L170 140 L145 140 L145 90 L120 90 z" fill="#bfdbfe" stroke="%s" stroke-width="2"/>' % _BLUE +
        '<path d="M280 60 L230 60 L230 140 L255 140 L255 90 L280 90 z" fill="#e0e7ff" stroke="%s" stroke-width="2" stroke-dasharray="4 3"/>' % _BLUE
    )
    return _svg("A shape reflected across a line to create a symmetric copy", body)


def sv_linear_pattern():
    rects = "".join('<rect x="%d" y="80" width="34" height="40" fill="%s" stroke="%s" stroke-width="2"/>' %
                    (40 + i * 70, "#bfdbfe" if i else "#2563eb", _DARK) for i in range(5))
    body = rects + _label(200, 160, "equal spacing \u2192", fill=_BLUE)
    return _svg("One feature repeated in a straight row at equal spacing", body)


def sv_circular_pattern():
    import math
    parts = ['<circle cx="200" cy="100" r="8" fill="%s"/>' % _RED]
    for i in range(6):
        a = math.radians(i * 60)
        x = 200 + 70 * math.cos(a)
        y = 100 + 70 * math.sin(a)
        parts.append('<rect x="%d" y="%d" width="20" height="20" fill="%s" stroke="%s" stroke-width="2"/>' %
                     (x - 10, y - 10, "#bfdbfe", _DARK))
    parts.append('<circle cx="200" cy="100" r="70" fill="none" stroke="%s" stroke-width="1" stroke-dasharray="4 4"/>' % _GREY)
    return _svg("A feature copied evenly around a center point", "".join(parts))


def sv_shell():
    body = (
        '<rect x="120" y="50" width="160" height="110" fill="none" stroke="%s" stroke-width="3"/>' % _BLUE +
        '<rect x="132" y="62" width="136" height="98" fill="#f8fafc" stroke="%s" stroke-width="1.5" stroke-dasharray="4 3"/>' % _GREY +
        _label(200, 185, "walls hollowed to constant thickness", fill=_DARK)
    )
    return _svg("A solid box hollowed out leaving thin walls", body)


# 2D drafting diagrams --------------------------------------------------------

def sv_trim():
    body = (
        '<line x1="40" y1="100" x2="360" y2="100" stroke="%s" stroke-width="3"/>' % _GREY +
        '<line x1="200" y1="40" x2="200" y2="160" stroke="%s" stroke-width="3"/>' % _GREY +
        '<line x1="200" y1="100" x2="360" y2="100" stroke="%s" stroke-width="5"/>' % _RED +
        _label(280, 90, "segment removed", fill=_RED, size=12)
    )
    return _svg("A line segment cut back to a cutting edge", body)


def sv_offset():
    body = (
        '<path d="M80 60 L200 60 L200 150 L80 150 z" fill="none" stroke="%s" stroke-width="2.5"/>' % _DARK +
        '<path d="M65 45 L215 45 L215 165 L65 165 z" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="5 3"/>' % _BLUE +
        _label(260, 105, "parallel copy at\na set distance", anchor="start", fill=_BLUE, size=12)
    )
    return _svg("A parallel copy of a shape at a fixed distance", body)


def sv_rect_array():
    parts = []
    for r in range(2):
        for c in range(4):
            parts.append('<rect x="%d" y="%d" width="26" height="26" fill="%s" stroke="%s" stroke-width="1.5"/>' %
                         (80 + c * 55, 60 + r * 55, "#bfdbfe", _DARK))
    return _svg("Objects repeated in rows and columns", "".join(parts))


def sv_polar_array():
    return sv_circular_pattern()


def sv_hatch():
    lines = "".join('<line x1="%d" y1="60" x2="%d" y2="150" stroke="%s" stroke-width="1.5"/>' %
                    (120 + i * 12, 90 + i * 12, _BLUE) for i in range(11))
    body = ('<path d="M110 60 L260 60 L260 150 L110 150 z" fill="none" stroke="%s" stroke-width="2.5"/>' % _DARK +
            '<clipPath id="c"><rect x="110" y="60" width="150" height="90"/></clipPath>'
            '<g clip-path="url(#c)">' + lines + '</g>' +
            _label(185, 175, "region filled with a pattern", fill=_DARK))
    return _svg("A closed boundary filled with a repeating pattern", body)


def sv_rotate():
    body = (
        '<rect x="60" y="80" width="60" height="40" fill="none" stroke="%s" stroke-width="2"/>' % _GREY +
        '<g transform="rotate(35 200 100)"><rect x="170" y="80" width="60" height="40" fill="#bfdbfe" stroke="%s" stroke-width="2"/></g>' % _BLUE +
        '<path d="M150 150 a60 60 0 0 1 40 -55" fill="none" stroke="%s" stroke-width="2" marker-end="url(#rot)"/>' % _RED +
        '<defs><marker id="rot" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        '<path d="M0 0 L6 3 L0 6 z" fill="%s"/></marker></defs>' % _RED +
        _label(300, 105, "turned about\na base point", anchor="start", fill=_DARK, size=12)
    )
    return _svg("A shape turned by an angle about a base point", body)


# BIM diagrams ----------------------------------------------------------------

def sv_wall_join():
    body = (
        '<rect x="80" y="80" width="180" height="18" fill="#cbd5e1" stroke="%s" stroke-width="1.5"/>' % _DARK +
        '<rect x="80" y="80" width="18" height="90" fill="#cbd5e1" stroke="%s" stroke-width="1.5"/>' % _DARK +
        '<path d="M98 98 L98 98" /><rect x="80" y="80" width="18" height="18" fill="%s"/>' % _BLUE +
        _label(200, 150, "two walls cleaned up at a corner", fill=_DARK)
    )
    return _svg("Two walls meeting and cleaning up at an L corner", body)


def sv_section_box():
    body = (
        '<path d="M100 60 l120 0 l40 -25 l-120 0 z" fill="#dbeafe" stroke="%s" stroke-width="1.5"/>' % _BLUE +
        '<path d="M100 60 l0 90 l120 0 l0 -90 z" fill="#bfdbfe" stroke="%s" stroke-width="1.5"/>' % _BLUE +
        '<path d="M220 60 l40 -25 l0 90 l-40 25 z" fill="#93c5fd" stroke="%s" stroke-width="1.5"/>' % _BLUE +
        '<line x1="160" y1="30" x2="160" y2="175" stroke="%s" stroke-width="2" stroke-dasharray="6 4"/>' % _RED +
        _label(160, 195, "cut plane through the model", fill=_RED)
    )
    return _svg("A cut plane slicing through a 3D building model", body)


def sv_levels_grids():
    body = (
        "".join('<line x1="60" y1="%d" x2="340" y2="%d" stroke="%s" stroke-width="1.5"/>'
                '<circle cx="52" cy="%d" r="9" fill="none" stroke="%s" stroke-width="1.5"/>' %
                (50 + i * 40, 50 + i * 40, _BLUE, 50 + i * 40, _BLUE) for i in range(3)) +
        "".join('<line x1="%d" y1="30" x2="%d" y2="180" stroke="%s" stroke-width="1" stroke-dasharray="4 4"/>' %
                (120 + i * 80, 120 + i * 80, _GREY) for i in range(3)) +
        _label(200, 195, "datum levels & column grids", fill=_DARK)
    )
    return _svg("Horizontal datum levels and vertical column grid lines", body)


def sv_clash():
    body = (
        '<rect x="60" y="95" width="200" height="20" rx="10" fill="#bfdbfe" stroke="%s" stroke-width="2"/>' % _BLUE +
        '<rect x="180" y="50" width="20" height="120" rx="10" fill="#fecaca" stroke="%s" stroke-width="2"/>' % _RED +
        '<circle cx="190" cy="105" r="18" fill="none" stroke="%s" stroke-width="3"/>' % _RED +
        _label(300, 105, "hard clash", anchor="start", fill=_RED)
    )
    return _svg("A pipe and a duct physically overlapping - a clash", body)


def sv_room():
    body = (
        '<rect x="90" y="55" width="220" height="110" fill="#dbeafe" stroke="%s" stroke-width="3"/>' % _DARK +
        '<line x1="200" y1="55" x2="200" y2="165" stroke="%s" stroke-width="2"/>' % _DARK +
        '<text x="145" y="115" text-anchor="middle" font-family="Inter" font-size="13" fill="%s">Office 101\\n12 m\u00b2</text>' % _BLUE +
        _label(255, 115, "Corr. 102", fill=_BLUE) +
        _label(200, 185, "bounded spaces with data", fill=_DARK)
    )
    return _svg("Enclosed spaces tagged with names and areas", body)


def sv_stair():
    steps = "".join('<rect x="%d" y="%d" width="30" height="12" fill="#bfdbfe" stroke="%s" stroke-width="1.5"/>' %
                    (90 + i * 28, 150 - i * 16, _DARK) for i in range(7))
    return _svg("A run of stair treads rising between levels", steps + _label(200, 185, "stair run", fill=_DARK))


# Civil diagrams --------------------------------------------------------------

def sv_alignment():
    body = (
        '<path d="M50 150 L150 150 Q250 150 280 90 L360 40" fill="none" stroke="%s" stroke-width="3"/>' % _BLUE +
        '<circle cx="150" cy="150" r="4" fill="%s"/><circle cx="280" cy="90" r="4" fill="%s"/>' % (_RED, _RED) +
        _label(150, 172, "PC", fill=_RED, size=11) + _label(295, 90, "PT", fill=_RED, size=11) +
        _label(200, 195, "horizontal alignment (tangent + curve)", fill=_DARK)
    )
    return _svg("A road centerline of straight tangents joined by a curve", body)


def sv_profile():
    body = (
        '<line x1="50" y1="40" x2="50" y2="170" stroke="%s" stroke-width="1.5"/>' % _DARK +
        '<line x1="50" y1="170" x2="360" y2="170" stroke="%s" stroke-width="1.5"/>' % _DARK +
        '<path d="M50 150 L140 120 Q190 100 240 110 L360 70" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="5 3"/>' % _GREY +
        '<path d="M50 145 L200 105 L360 65" fill="none" stroke="%s" stroke-width="3"/>' % _BLUE +
        _label(200, 190, "ground vs design grade (profile)", fill=_DARK)
    )
    return _svg("An elevation view showing existing ground and design grade", body)


def sv_corridor():
    body = (
        '<path d="M80 150 L160 90 L240 90 L320 150" fill="none" stroke="%s" stroke-width="3"/>' % _BLUE +
        '<line x1="160" y1="90" x2="240" y2="90" stroke="%s" stroke-width="5"/>' % _DARK +
        '<path d="M80 150 L60 165 M320 150 L340 165" stroke="%s" stroke-width="2"/>' % _GREY +
        _label(200, 75, "crown", fill=_DARK, size=11) +
        _label(200, 185, "typical road cross-section", fill=_DARK)
    )
    return _svg("A road cross section with crown, lanes and side slopes", body)


def sv_contours():
    body = "".join('<path d="M%d 60 Q200 %d %d 160" fill="none" stroke="%s" stroke-width="1.5"/>' %
                   (70 + i * 20, 40 + i * 25, 330 - i * 20, _BLUE) for i in range(5)) + \
        _label(200, 185, "surface contour lines", fill=_DARK)
    return _svg("Nested contour lines representing a terrain surface", body)


def sv_pipe_network():
    body = (
        '<circle cx="80" cy="70" r="10" fill="none" stroke="%s" stroke-width="2"/>' % _DARK +
        '<circle cx="200" cy="130" r="10" fill="none" stroke="%s" stroke-width="2"/>' % _DARK +
        '<circle cx="330" cy="90" r="10" fill="none" stroke="%s" stroke-width="2"/>' % _DARK +
        '<line x1="88" y1="76" x2="192" y2="124" stroke="%s" stroke-width="3"/>' % _BLUE +
        '<line x1="210" y1="127" x2="322" y2="95" stroke="%s" stroke-width="3"/>' % _BLUE +
        _label(200, 185, "structures joined by pipes", fill=_DARK)
    )
    return _svg("Manhole structures connected by pipe runs", body)


def sv_cutfill():
    body = (
        '<path d="M50 90 L360 90" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="5 3"/>' % _GREY +
        '<path d="M50 130 L200 130 L360 70" fill="none" stroke="%s" stroke-width="2.5"/>' % _BLUE +
        '<path d="M50 90 L50 130 L200 130 L200 90 z" fill="#fee2e2"/>' +
        '<path d="M200 90 L360 90 L360 70 z" fill="#dcfce7"/>' +
        _label(120, 115, "FILL", fill=_RED, size=12) + _label(300, 85, "CUT", fill="#16a34a", size=12)
    )
    return _svg("Earthwork cut and fill between existing and design surfaces", body)


# CAE / simulation diagrams ---------------------------------------------------

def sv_mesh():
    import math
    tris = []
    for r in range(3):
        for c in range(6):
            x = 80 + c * 40
            y = 60 + r * 35
            tris.append('<path d="M%d %d L%d %d L%d %d z" fill="#dbeafe" stroke="%s" stroke-width="1"/>' %
                        (x, y, x + 40, y, x + 20, y + 35, _BLUE))
    return _svg("A part discretized into a triangular finite-element mesh",
                "".join(tris) + _label(200, 185, "finite-element mesh", fill=_DARK))


def sv_fixed_support():
    body = (
        '<rect x="120" y="60" width="160" height="60" fill="#dbeafe" stroke="%s" stroke-width="2"/>' % _BLUE +
        '<line x1="120" y1="60" x2="120" y2="120" stroke="%s" stroke-width="3"/>' % _DARK +
        "".join('<line x1="120" y1="%d" x2="108" y2="%d" stroke="%s" stroke-width="2"/>' %
                (62 + i * 12, 72 + i * 12, _DARK) for i in range(5)) +
        _label(200, 150, "fully fixed (encastre) edge", fill=_DARK)
    )
    return _svg("A fixed/encastre boundary condition hatched on an edge", body)


def sv_force_load():
    body = (
        '<rect x="80" y="90" width="160" height="50" fill="#dbeafe" stroke="%s" stroke-width="2"/>' % _BLUE +
        '<line x1="300" y1="40" x2="300" y2="90" stroke="%s" stroke-width="3" marker-end="url(#f)"/>' % _RED +
        '<defs><marker id="f" markerWidth="10" markerHeight="10" refX="5" refY="8" orient="auto">'
        '<path d="M0 0 L5 8 L10 0 z" fill="%s"/></marker></defs>' % _RED +
        _label(320, 65, "F", anchor="start", fill=_RED, size=16) +
        _label(200, 165, "point force applied to a face", fill=_DARK)
    )
    return _svg("A concentrated point force arrow applied to a face", body)


def sv_pressure():
    arrows = "".join('<line x1="%d" y1="55" x2="%d" y2="90" stroke="%s" stroke-width="2" marker-end="url(#p)"/>' %
                     (100 + i * 30, 100 + i * 30, _RED) for i in range(7))
    body = (
        '<defs><marker id="p" markerWidth="9" markerHeight="9" refX="4" refY="7" orient="auto">'
        '<path d="M0 0 L4 7 L8 0 z" fill="%s"/></marker></defs>' % _RED +
        arrows +
        '<rect x="90" y="90" width="200" height="45" fill="#dbeafe" stroke="%s" stroke-width="2"/>' % _BLUE +
        _label(200, 165, "uniform pressure over a face", fill=_DARK)
    )
    return _svg("A uniformly distributed pressure load over a face", body)


def sv_stress_contour():
    body = (
        '<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#2563eb"/>'
        '<stop offset="0.5" stop-color="#22c55e"/><stop offset="0.75" stop-color="#eab308"/>'
        '<stop offset="1" stop-color="#dc2626"/></linearGradient></defs>'
        '<path d="M60 120 L200 120 L200 60 L340 60 L340 90 L230 90 L230 150 L60 150 z" '
        'fill="url(#g)" stroke="%s" stroke-width="1.5"/>' % _DARK +
        _label(200, 185, "color-mapped stress distribution", fill=_DARK)
    )
    return _svg("A color contour plot of stress magnitude over a part", body)


def sv_deformed():
    body = (
        '<rect x="60" y="80" width="200" height="30" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="5 3"/>' % _GREY +
        '<path d="M60 95 Q160 95 260 150" fill="none" stroke="%s" stroke-width="3"/>' % _BLUE +
        _label(150, 75, "undeformed", fill=_GREY, size=11) +
        _label(230, 175, "deflected shape", fill=_BLUE, size=12)
    )
    return _svg("A cantilever beam shown deflecting under load", body)


# Visualization diagrams ------------------------------------------------------

def sv_three_point():
    body = (
        '<circle cx="200" cy="110" r="35" fill="#cbd5e1" stroke="%s" stroke-width="2"/>' % _DARK +
        '<circle cx="90" cy="50" r="10" fill="#fde047"/>' + _label(90, 38, "key", fill=_DARK, size=11) +
        '<circle cx="320" cy="70" r="10" fill="#bfdbfe"/>' + _label(320, 58, "fill", fill=_DARK, size=11) +
        '<circle cx="250" cy="180" r="10" fill="#fca5a5"/>' + _label(255, 178, "rim", anchor="start", fill=_DARK, size=11) +
        '<line x1="98" y1="58" x2="175" y2="95" stroke="%s" stroke-width="1"/>' % _GREY +
        '<line x1="312" y1="76" x2="230" y2="100" stroke="%s" stroke-width="1"/>' % _GREY
    )
    return _svg("Three lights placed as key, fill and rim around a subject", body)


def sv_camera_frustum():
    body = (
        '<rect x="40" y="90" width="40" height="30" fill="%s"/>' % _DARK +
        '<path d="M80 105 L320 50 L320 170 z" fill="#dbeafe" fill-opacity="0.6" stroke="%s" stroke-width="1.5"/>' % _BLUE +
        _label(200, 190, "camera view frustum", fill=_DARK)
    )
    return _svg("A camera and its pyramid-shaped view frustum", body)


def sv_material_sphere():
    body = (
        '<defs><radialGradient id="ms" cx="0.35" cy="0.3"><stop offset="0" stop-color="#ffffff"/>'
        '<stop offset="0.4" stop-color="#60a5fa"/><stop offset="1" stop-color="#1e3a8a"/></radialGradient></defs>'
        '<circle cx="200" cy="100" r="60" fill="url(#ms)"/>'
        '<circle cx="180" cy="80" r="10" fill="#ffffff" fill-opacity="0.85"/>' +
        _label(200, 185, "PBR material preview sphere", fill=_DARK)
    )
    return _svg("A shaded preview sphere showing a physically based material", body)


def sv_hdri_dome():
    body = (
        '<path d="M60 150 A140 110 0 0 1 340 150 z" fill="#dbeafe" stroke="%s" stroke-width="2"/>' % _BLUE +
        '<circle cx="120" cy="90" r="14" fill="#fde047"/>' +
        '<rect x="170" y="130" width="60" height="20" fill="#cbd5e1" stroke="%s" stroke-width="1.5"/>' % _DARK +
        _label(200, 185, "environment dome lighting the scene", fill=_DARK)
    )
    return _svg("An environment dome (HDRI) surrounding and lighting a model", body)


def sv_dof():
    body = (
        '<circle cx="110" cy="110" r="28" fill="#93c5fd" fill-opacity="0.4" stroke="%s" stroke-width="1" stroke-dasharray="3 3"/>' % _GREY +
        '<circle cx="210" cy="110" r="34" fill="#2563eb"/>' + _label(210, 165, "in focus", fill=_BLUE, size=11) +
        '<circle cx="320" cy="110" r="28" fill="#93c5fd" fill-opacity="0.4" stroke="%s" stroke-width="1" stroke-dasharray="3 3"/>' % _GREY +
        _label(110, 165, "blurred", fill=_GREY, size=11) + _label(320, 165, "blurred", fill=_GREY, size=11)
    )
    return _svg("A sharp subject between blurred foreground and background", body)


def sv_ao():
    body = (
        '<defs><radialGradient id="ao" cx="0.5" cy="1"><stop offset="0" stop-color="#334155"/>'
        '<stop offset="0.5" stop-color="#94a3b8"/><stop offset="1" stop-color="#f8fafc"/></radialGradient></defs>'
        '<rect x="120" y="60" width="90" height="90" fill="#cbd5e1"/>'
        '<rect x="210" y="60" width="90" height="90" fill="#cbd5e1"/>'
        '<rect x="120" y="130" width="180" height="20" fill="url(#ao)"/>' +
        _label(200, 185, "contact shadows in crevices", fill=_DARK)
    )
    return _svg("Darkening where surfaces meet - ambient occlusion", body)


# --- question factories ------------------------------------------------------

def img_q(node, slug, diff, image, question, options, correct, why, pitfall):
    return {
        "type": "image", "nodeId": node, "slug": slug, "difficulty": diff,
        "image": image, "question": question, "options": options,
        "correctIdx": correct, "why": why, "pitfall": pitfall,
    }


def txt_q(node, slug, diff, question, options, correct, why, pitfall):
    return {
        "type": "single", "nodeId": node, "slug": slug, "difficulty": diff,
        "question": question, "options": options, "correctIdx": correct,
        "why": why, "pitfall": pitfall,
    }


EXTRA_LESSONS = {}


# ============================ MCAD ==========================================
EXTRA_LESSONS["mcad"] = [
    {
        "id": 6,
        "title": "Lesson 6: 看图识操作 (Visual Feature ID)",
        "desc": "Identify the modeling operation from the diagram",
        "questions": [
            img_q("parametrics", "img-extrude", "beginner", sv_extrude(),
                  "The diagram shows a 2D profile becoming a 3D solid. Which feature operation is this?",
                  ["Extrude — push a closed profile a linear distance to add material",
                   "Revolve — spin a profile about an axis",
                   "Sweep — drive a profile along a path",
                   "Loft — blend between two profiles"], 0,
                  "Extrude linearly projects a closed 2D sketch by a specified depth to create a prismatic solid — the most common base feature.",
                  "A profile must be closed and non-self-intersecting to extrude as a solid; open profiles create surfaces instead."),
            img_q("parametrics", "img-revolve", "beginner", sv_revolve(),
                  "A profile is spun around the dashed axis to form the shape at right. Which operation is this?",
                  ["Revolve — rotate a profile about an axis",
                   "Extrude — linear projection",
                   "Shell — hollow a solid",
                   "Fillet — round an edge"], 0,
                  "Revolve rotates a profile about a centerline (0–360°) to create axisymmetric parts such as shafts, wheels, and bottles.",
                  "The profile must not cross the axis of revolution, or the feature will fail or self-intersect."),
            img_q("brep", "img-fillet", "beginner", sv_fillet(),
                  "The sharp corner on the left becomes the rounded one on the right. Which operation is this?",
                  ["Fillet — round a sharp edge with a radius",
                   "Chamfer — bevel an edge at an angle",
                   "Draft — taper a face",
                   "Offset — parallel copy"], 0,
                  "A fillet replaces a sharp edge with a tangent arc of a set radius, reducing stress concentrations and easing manufacturing.",
                  "Very large fillets can fail if the radius exceeds adjacent face sizes; add fillets late in the feature tree."),
            img_q("brep", "img-chamfer", "beginner", sv_chamfer(),
                  "The corner is replaced by a straight angled cut. Which operation is shown?",
                  ["Chamfer — bevel an edge with a straight cut",
                   "Fillet — round an edge",
                   "Shell — hollow the part",
                   "Mirror — reflect geometry"], 0,
                  "A chamfer bevels an edge (distance-distance or distance-angle), commonly used to break sharp edges and ease part assembly/insertion.",
                  "Don't confuse chamfers with fillets on drawings — call out the angle and distance, since a 1×45° is not the same as a fillet R1."),
            img_q("parametrics", "img-linear-pattern", "beginner", sv_linear_pattern(),
                  "One feature is repeated in a straight row at equal spacing. Which operation is this?",
                  ["Linear pattern — repeat along one or two directions",
                   "Circular pattern — repeat around a center",
                   "Mirror — reflect across a plane",
                   "Sweep — follow a path"], 0,
                  "A linear (rectangular) pattern instances a feature at a set spacing and count, keeping parametric links to the seed feature.",
                  "Pattern the feature, not the faces, so edits to the seed propagate; patterning bodies instead often breaks downstream references."),
            img_q("brep", "img-shell", "intermediate", sv_shell(),
                  "The solid box becomes a thin-walled open box. Which operation produced this?",
                  ["Shell — hollow a solid to a constant wall thickness",
                   "Extrude cut — remove a prism",
                   "Draft — add taper",
                   "Fillet — round edges"], 0,
                  "Shell removes selected faces and offsets the remaining faces inward (or outward) to a uniform thickness — essential for plastic and cast parts.",
                  "Apply shell before adding fillets where possible; shelling after large fillets can create thin slivers or fail."),
        ],
    },
    {
        "id": 7,
        "title": "Lesson 7: Advanced Modeling & Data",
        "desc": "Configurations, MBD, top-down design, and file exchange",
        "questions": [
            txt_q("parametrics", "config-design-tables", "intermediate",
                  "What is the purpose of a design table (configurations driven by a spreadsheet) in parametric CAD?",
                  ["Generate a family of part variants (sizes/options) from one model by driving dimensions and suppression states from a table",
                   "Render photorealistic images of each variant automatically",
                   "Convert the model to a neutral STEP file",
                   "Store the part's manufacturing cost history"], 0,
                  "Design tables create configurations — e.g. M6, M8, M10 bolts — from a single parametric model, keeping variants consistent and maintainable.",
                  "Keep the number of configurations manageable; hundreds of table rows bloat the file and slow rebuilds. Consider a library part instead."),
            txt_q("mbd", "mbd-pmi", "advanced",
                  "In Model-Based Definition (MBD), where does the authoritative dimensioning and tolerancing information live?",
                  ["As semantic PMI attached directly to the 3D model, making the 3D dataset the master rather than a 2D drawing",
                   "Only in a separately maintained 2D PDF drawing",
                   "In the CAM post-processor configuration",
                   "In the assembly bill of materials"], 0,
                  "MBD embeds GD&T, notes, and datums as machine-readable PMI on the 3D model, so downstream CMM/CAM can consume it without a 2D drawing.",
                  "MBD only pays off if downstream tools consume semantic PMI. Cosmetic (graphical-only) PMI that isn't associative defeats the purpose."),
            txt_q("assembly", "top-down-skeleton", "advanced",
                  "What characterizes a top-down assembly design approach using a skeleton/layout?",
                  ["Key dimensions and interfaces are defined in a central skeleton, and component geometry references it so a change propagates to all parts",
                   "Each part is modeled in isolation and mated later with no shared references",
                   "The assembly is built only from purchased library components",
                   "Parts are created by scanning physical prototypes"], 0,
                  "Top-down design drives components from a shared skeleton/layout, capturing design intent for interfaces so system-level changes update all affected parts.",
                  "Uncontrolled external references create fragile circular dependencies; route references through a single skeleton to keep them manageable."),
            txt_q("brep", "brep-vs-mesh", "intermediate",
                  "Why is a B-Rep (boundary representation) solid generally preferred over a triangle mesh for engineering CAD?",
                  ["B-Rep stores exact analytic surfaces and topology, enabling precise dimensions, booleans, and editable features; meshes only approximate the surface with facets",
                   "Meshes cannot be displayed on screen",
                   "B-Rep files are always smaller than meshes",
                   "Meshes cannot be exported to any format"], 0,
                  "B-Rep captures exact geometry (planes, cylinders, NURBS) with topological relationships, so measurements and modifications stay accurate; meshes are faceted approximations.",
                  "Converting a scan mesh straight to B-Rep without surfacing rework usually yields a heavy, un-editable body; rebuild with proper surfaces for parametric use."),
            txt_q("assembly", "mate-references", "intermediate",
                  "What is the benefit of defining mate references on frequently reused components (fasteners, fittings)?",
                  ["Components snap into place automatically with predefined mate relationships when dragged into an assembly, speeding assembly and reducing errors",
                   "They reduce the mass of the component",
                   "They convert the part into sheet metal",
                   "They encrypt the part file"], 0,
                  "Mate references pre-tag faces/edges so a bolt drops into a hole with the correct coincident/concentric mates automatically — a big time-saver for standard hardware.",
                  "Ambiguous or over-general mate references can snap parts to the wrong geometry; name and scope them carefully in library components."),
            txt_q("parametrics", "feature-order-intent", "intermediate",
                  "Why does feature order in the model tree matter for robust parametric models?",
                  ["Later features depend on earlier geometry; a poor order creates fragile references that break when upstream features change",
                   "The tree order sets the part's color",
                   "Feature order determines the export file format",
                   "It has no effect — order is purely cosmetic"], 0,
                  "Parametric history is sequential — each feature builds on prior geometry. Logical ordering (base → detail → fillets) keeps rebuilds stable and edits predictable.",
                  "Referencing a downstream face in an early feature (out-of-order dependency) causes rebuild errors; capture design intent with sketches/planes, not incidental faces."),
            txt_q("mbd", "gdt-datum-reference", "advanced",
                  "In GD&T, what does a datum reference frame established by datums A|B|C provide?",
                  ["A repeatable 3-2-1 coordinate origin that constrains six degrees of freedom so features are measured consistently in inspection",
                   "A color scheme for the drawing border",
                   "The order in which features are machined",
                   "A list of purchased components"], 0,
                  "Datums A|B|C lock the six degrees of freedom (3-2-1 principle), giving inspection a repeatable reference frame so tolerances mean the same thing every time.",
                  "Choosing functional datums that match how the part is actually located in assembly is critical; arbitrary datum choice yields parts that pass CMM but don't fit."),
        ],
    },
]


# ============================ 2D DRAFT ======================================
EXTRA_LESSONS["draft"] = [
    {
        "id": 6,
        "title": "Lesson 6: 看图识操作 (Visual Command ID)",
        "desc": "Identify the AutoCAD/GstarCAD editing command from the diagram",
        "questions": [
            img_q("editing", "img-trim", "beginner", sv_trim(),
                  "The highlighted segment is removed up to a crossing line. Which command does this?",
                  ["TRIM — cut objects at a cutting edge",
                   "EXTEND — lengthen to a boundary",
                   "OFFSET — parallel copy",
                   "FILLET — join with an arc"], 0,
                  "TRIM removes the portion of an object beyond (or between) selected cutting edges — one of the most-used editing commands.",
                  "Objects must actually cross or meet the cutting edge; in newer releases 'Quick' mode auto-selects edges, which can trim more than intended."),
            img_q("editing", "img-offset", "beginner", sv_offset(),
                  "A parallel copy of the shape is created at a fixed distance. Which command is this?",
                  ["OFFSET — create parallel copies at a set distance",
                   "COPY — duplicate at any point",
                   "MIRROR — reflect across a line",
                   "SCALE — resize"], 0,
                  "OFFSET creates concentric/parallel copies of lines, polylines, and arcs at a specified distance — ideal for wall thicknesses and road edges.",
                  "Offsetting a polyline keeps it as one object; offsetting individual lines leaves gaps at corners that must be cleaned up."),
            img_q("editing", "img-array-rect", "beginner", sv_rect_array(),
                  "Objects are repeated in evenly spaced rows and columns. Which command is this?",
                  ["ARRAY (Rectangular) — repeat in rows and columns",
                   "COPY — single duplicate",
                   "DIVIDE — place points along an object",
                   "HATCH — fill a region"], 0,
                  "A rectangular ARRAY creates a grid of copies with defined row/column counts and spacing; associative arrays stay editable as one object.",
                  "Associative arrays behave as a single object — use the array's grips or the ribbon to edit counts, not EXPLODE, which loses associativity."),
            img_q("editing", "img-hatch", "beginner", sv_hatch(),
                  "A closed boundary is filled with a diagonal line pattern. Which command produced this?",
                  ["HATCH — fill a bounded area with a pattern",
                   "SOLID — fill with a color",
                   "SKETCH — freehand draw",
                   "WIPEOUT — mask an area"], 0,
                  "HATCH fills an enclosed boundary with a pattern (ANSI31, solid, gradient) used to indicate materials in sections; associative hatches update with the boundary.",
                  "If the boundary isn't fully closed, HATCH fails or leaks; use 'Gap tolerance' or close gaps first, and keep hatches on their own layer."),
            img_q("editing", "img-rotate", "beginner", sv_rotate(),
                  "The object is turned by an angle about a base point. Which command is this?",
                  ["ROTATE — turn objects about a base point",
                   "MOVE — translate objects",
                   "MIRROR — reflect objects",
                   "STRETCH — deform with a crossing window"], 0,
                  "ROTATE turns selected objects around a chosen base point by an angle (or with the Reference option to align to existing geometry).",
                  "Pick the base point deliberately — rotating about the wrong point sends geometry far off; use the Reference option to rotate to a known alignment."),
            img_q("editing", "img-mirror-2d", "beginner", sv_mirror(),
                  "A symmetric copy is produced across the dashed line. Which command is this?",
                  ["MIRROR — reflect objects across an axis",
                   "OFFSET — parallel copy",
                   "ARRAY — repeat objects",
                   "ALIGN — move and rotate to match"], 0,
                  "MIRROR reflects objects across a defined line; MIRRTEXT controls whether text is also reversed. Ideal for symmetric parts and layouts.",
                  "Leave MIRRTEXT=0 so mirrored text stays readable; a value of 1 flips text backwards, which is rarely wanted on drawings."),
        ],
    },
    {
        "id": 7,
        "title": "Lesson 7: Standards & Productivity",
        "desc": "Layers, annotation scale, dynamic blocks, and data extraction",
        "questions": [
            txt_q("cad-basics", "layer-standards", "intermediate",
                  "Why do drawing offices enforce a layer naming standard (e.g. AIA/ISO 13567 layer conventions)?",
                  ["Consistent layer names/colors/linetypes make drawings predictable across teams and enable reliable exchange, plotting, and Xref management",
                   "It reduces the DWG file size dramatically",
                   "It automatically dimensions the drawing",
                   "It is required to open the file"], 0,
                  "Layer standards map object types to defined layers with set color/linetype/lineweight, so plot styles and Xref overlays behave consistently across a project.",
                  "Ad-hoc 'Layer1/Layer2' naming makes CTB/plot-style control and Xref layer overrides unmanageable on large multi-consultant projects."),
            txt_q("annotation", "annotative-scaling", "intermediate",
                  "What problem do annotative objects (text, dimensions, hatches) solve?",
                  ["They automatically display at the correct size in each viewport scale, so one annotation object serves multiple layout scales",
                   "They convert the drawing to 3D",
                   "They encrypt annotation content",
                   "They remove the need for layouts entirely"], 0,
                  "Annotative scaling ties text/dimension height to viewport scale, so a note reads correctly at 1:50 and 1:100 without duplicating annotations per scale.",
                  "Mixing annotative and fixed-height text on the same drawing causes inconsistent plotted sizes; standardize on annotative styles across the sheet set."),
            txt_q("blocks", "dynamic-blocks", "intermediate",
                  "What advantage do dynamic blocks provide over ordinary blocks?",
                  ["A single block definition can flex through parameters and actions (stretch, flip, array, visibility states) instead of needing many separate blocks",
                   "They automatically 3D-print the geometry",
                   "They cannot be inserted more than once",
                   "They store the drawing's revision history"], 0,
                  "Dynamic blocks embed parameters/actions and visibility states so one door or bolt block covers many sizes/types, reducing library clutter.",
                  "Overly complex dynamic blocks with many parameters become hard to edit and error-prone; document their grips or split into simpler blocks."),
            txt_q("data", "attribute-extraction", "intermediate",
                  "How does block attribute extraction (DATAEXTRACTION) support documentation?",
                  ["It harvests attribute data from block instances into a table or spreadsheet, automating schedules and bills of materials",
                   "It deletes all blocks to reduce file size",
                   "It converts blocks into 3D solids",
                   "It renders the drawing photorealistically"], 0,
                  "DATAEXTRACTION reads attributes (part number, size, count) from blocks and outputs a live table/CSV, keeping schedules synchronized with the drawing.",
                  "Attributes must be populated consistently; blocks with blank or misspelled attribute values corrupt the extracted schedule."),
            txt_q("output", "plot-styles-ctb-stb", "intermediate",
                  "What is the difference between color-dependent (CTB) and named (STB) plot styles?",
                  ["CTB maps plotted lineweight/color to object color; STB assigns a named style to objects/layers independent of their color",
                   "CTB is for 3D and STB is for 2D only",
                   "STB files cannot be shared between drawings",
                   "There is no functional difference"], 0,
                  "CTB ties output appearance to the 255 AutoCAD colors (color = pen), while STB decouples appearance from color via named styles — more flexible but requires discipline.",
                  "Never mix CTB and STB in one project; a drawing is set to one plot-style mode, and converting mid-project causes plotting surprises."),
            txt_q("output", "etransmit-references", "intermediate",
                  "Why use eTransmit (or Pack-and-Go) when sending DWGs to a consultant?",
                  ["It bundles the DWG with all dependent Xrefs, fonts, images, and plot styles and repaths them, so the recipient opens the drawing with nothing missing",
                   "It converts the DWG to a video file",
                   "It permanently locks the drawing from editing",
                   "It uploads the file to a public website"], 0,
                  "eTransmit packages every dependency and fixes paths to relative, preventing 'missing Xref/font/shape' errors on the recipient's machine.",
                  "Emailing a bare DWG with external Xrefs almost always breaks references; always eTransmit or bind Xrefs before external issue."),
            txt_q("cad-basics", "purge-file-hygiene", "beginner",
                  "What does running PURGE followed by AUDIT accomplish on a working drawing?",
                  ["PURGE removes unused named objects (layers, blocks, styles) to shrink the file; AUDIT finds and fixes internal database errors",
                   "They print the drawing to PDF",
                   "They convert the drawing to metric units",
                   "They renumber all layers automatically"], 0,
                  "Regular PURGE + AUDIT keeps files lean and healthy, reducing bloat from imported blocks and repairing minor corruption before it worsens.",
                  "Run PURGE more than once (nested items) and back up before aggressive purging of shared files, since regapps/zero-length geometry may need extra passes."),
        ],
    },
]


# ============================ BIM ===========================================
EXTRA_LESSONS["bim"] = [
    {
        "id": 6,
        "title": "Lesson 6: 看图识操作 (Visual BIM ID)",
        "desc": "Identify the BIM concept from the diagram",
        "questions": [
            img_q("clash", "img-clash", "beginner", sv_clash(),
                  "The diagram circles where a duct and a pipe occupy the same space. What is this called?",
                  ["A hard clash — two elements physically intersecting",
                   "A soft clash — a clearance/tolerance violation only",
                   "A workflow clash — a scheduling conflict",
                   "A duplicate element warning"], 0,
                  "A hard clash is a true geometric overlap between elements; detecting these in Navisworks/Solibri before construction avoids costly on-site rework.",
                  "Not every reported clash matters — filter by discipline and tolerance so the team resolves genuine hard clashes, not thousands of trivial insulation grazes."),
            img_q("bim", "img-section-box", "beginner", sv_section_box(),
                  "A plane cuts through the 3D model to reveal its interior. Which BIM tool is shown?",
                  ["A section/cut plane (section box) through the model",
                   "A clash detection sphere",
                   "A rendering camera",
                   "A point cloud scan"], 0,
                  "Section planes/boxes slice the model to produce coordinated sections and to isolate a region for review — a core BIM navigation and documentation tool.",
                  "Section views in BIM are live cuts of the model; editing the model updates them, so don't 'draft over' errors — fix the source geometry."),
            img_q("shared-coords", "img-levels-grids", "beginner", sv_levels_grids(),
                  "The diagram shows horizontal reference planes and vertical reference lines. What are these?",
                  ["Levels and grids — the project's datums",
                   "Rooms and areas",
                   "Clash zones",
                   "Rendering guides"], 0,
                  "Levels define floor heights and grids define the structural column layout; together they are the shared datums every discipline hosts elements to.",
                  "Levels, grids, and shared coordinates must be locked and owned centrally — never place them in a user workset where they can be accidentally moved."),
            img_q("bim", "img-rooms", "beginner", sv_room(),
                  "The enclosed areas are tagged with names and areas. Which BIM element is this?",
                  ["Rooms/spaces — bounded areas carrying data",
                   "Hatches on a 2D drawing",
                   "Clash results",
                   "Rendering materials"], 0,
                  "Rooms/spaces are data-carrying objects bounded by walls; they drive area schedules, occupancy, and MEP load calculations from the model.",
                  "Rooms rely on continuous bounding elements — a gap in walls lets a room 'bleed' into adjacent spaces, corrupting area schedules."),
            img_q("revit", "img-stair", "beginner", sv_stair(),
                  "The diagram shows treads rising between two levels. Which element is this?",
                  ["A stair (component) hosted between levels",
                   "A ramp gradient plot",
                   "A structural grid",
                   "A contour surface"], 0,
                  "Stair components are parametric elements defined by base/top level, tread/riser rules, and code constraints, updating automatically when levels change.",
                  "Stairs are governed by code (max riser/min tread); overriding sketch geometry without respecting the rules produces non-compliant, hard-to-maintain stairs."),
            img_q("bim", "img-wall-join", "intermediate", sv_wall_join(),
                  "Two walls meet at a corner and clean up into one continuous junction. What is this behavior?",
                  ["Wall join/cleanup — walls resolve their intersection automatically",
                   "A clash between two walls",
                   "A section cut",
                   "A dimension constraint"], 0,
                  "BIM walls auto-join at corners, merging layers of compatible structure so the junction cleans up in plan without manual line editing.",
                  "Dissimilar wall types may not clean up automatically; use 'disallow/allow join' and matching layer structure to control corner behavior."),
        ],
    },
]


# ============================ CIVIL =========================================
EXTRA_LESSONS["civil"] = [
    {
        "id": 6,
        "title": "Lesson 6: 看图识操作 (Visual Civil ID)",
        "desc": "Identify the civil/infrastructure concept from the diagram",
        "questions": [
            img_q("civil3d", "img-alignment", "beginner", sv_alignment(),
                  "The diagram shows a road centerline of straight tangents joined by a curve, with PC/PT points. What is this?",
                  ["A horizontal alignment",
                   "A vertical profile",
                   "A surface TIN",
                   "A pipe network"], 0,
                  "A horizontal alignment defines the roadway centerline geometry (tangents, curves, spirals) that all corridor and profile design references.",
                  "Editing alignment geometry ripples to profiles, corridors, and stationing; lock the alignment once design is fixed to avoid cascading changes."),
            img_q("civil3d", "img-profile", "beginner", sv_profile(),
                  "The diagram shows existing ground versus a proposed design line in elevation along a route. What is this?",
                  ["A profile (vertical alignment) view",
                   "A horizontal alignment plan",
                   "A cross section",
                   "A contour map"], 0,
                  "A profile plots elevation against station, comparing existing ground to the design grade so vertical curves and grades can be set.",
                  "Design grades must respect maximum gradients and vertical curve sight distance; a steep profile that ignores standards fails design review."),
            img_q("civil3d", "img-corridor-section", "beginner", sv_corridor(),
                  "The diagram shows a road cross-section with a crowned surface, lanes, and side slopes. What is this?",
                  ["A typical cross section / corridor assembly",
                   "A horizontal alignment",
                   "A surface contour",
                   "A pipe profile"], 0,
                  "A cross section (assembly) defines the roadway template — lanes, crown, curbs, and daylight slopes — applied along the alignment to build the corridor.",
                  "The assembly must include daylighting (tie-in) subassemblies, or the corridor won't meet existing ground and earthwork quantities will be wrong."),
            img_q("civil3d", "img-contours", "beginner", sv_contours(),
                  "The nested curved lines represent equal-elevation lines on terrain. What are these?",
                  ["Contour lines of a surface",
                   "Pipe network runs",
                   "Alignment tangents",
                   "Property boundaries"], 0,
                  "Contours connect points of equal elevation on a surface (TIN/DEM); their spacing reveals slope — closely spaced means steep terrain.",
                  "Contours are a display of the surface, not the surface itself; edit the TIN (add breaklines/points), not the contour lines, to change terrain."),
            img_q("civil3d", "img-pipe-network", "beginner", sv_pipe_network(),
                  "The diagram shows structures (circles) joined by connecting runs. What civil system is this?",
                  ["A pipe network (structures + pipes)",
                   "A road alignment",
                   "A surface contour set",
                   "A parcel layout"], 0,
                  "A pipe network models structures (manholes/inlets) and connecting pipes with invert elevations and flow direction for storm/sanitary design.",
                  "Pipe inverts and rim elevations must reference the surface and hydraulic grade; disconnected structures or reversed slopes break the network analysis."),
            img_q("civil3d", "img-cutfill", "intermediate", sv_cutfill(),
                  "The shaded areas between existing ground and design surface represent what quantity?",
                  ["Earthwork cut and fill volumes",
                   "Pavement layer thickness",
                   "Drainage catchment area",
                   "Right-of-way width"], 0,
                  "Cut (excavation) and fill (embankment) areas between surfaces drive earthwork volume takeoff and haul/balance planning.",
                  "Apply shrinkage/swell factors to raw cut and fill volumes; treating in-situ and compacted volumes as equal underestimates material needs."),
        ],
    },
]


# ============================ SIM / CAE =====================================
EXTRA_LESSONS["sim"] = [
    {
        "id": 6,
        "title": "Lesson 6: 看图识操作 (Visual FEA ID)",
        "desc": "Identify the simulation setup element from the diagram",
        "questions": [
            img_q("mesh", "img-mesh", "beginner", sv_mesh(),
                  "The part is subdivided into many small triangular elements. What is this?",
                  ["A finite-element mesh (discretization)",
                   "A stress contour plot",
                   "A rendering wireframe",
                   "A hatch pattern"], 0,
                  "Meshing subdivides the geometry into elements over which the governing equations are solved; mesh quality directly controls solution accuracy.",
                  "A single coarse mesh isn't trustworthy — run a mesh-convergence study, refining in high-gradient regions until results stabilize."),
            img_q("fea", "img-fixed-support", "beginner", sv_fixed_support(),
                  "The hatched edge indicates the model is fully restrained there. What boundary condition is this?",
                  ["A fixed (encastre) support — all DOF restrained",
                   "An applied force",
                   "A pressure load",
                   "A symmetry plane"], 0,
                  "A fixed support removes all translational (and rotational, for shells) degrees of freedom at that face/edge, anchoring the model for static analysis.",
                  "Over-constraining with fixed supports where the real part is only partially restrained artificially stiffens the model and hides true deflection."),
            img_q("fea", "img-force", "beginner", sv_force_load(),
                  "The single arrow 'F' applied to a face represents which load type?",
                  ["A concentrated (point) force",
                   "A fixed support",
                   "A distributed pressure",
                   "A thermal load"], 0,
                  "A concentrated force applies a total load at a point/face; reaction forces should balance applied loads as a basic sanity check.",
                  "A point load on a single node creates an artificial stress singularity; distribute it over a realistic contact area for meaningful local stress."),
            img_q("fea", "img-pressure", "beginner", sv_pressure(),
                  "The row of equal arrows pushing on a face represents which load type?",
                  ["A uniform pressure over the face",
                   "A point force",
                   "A fixed constraint",
                   "A bolt preload"], 0,
                  "Pressure applies force per unit area normal to a face; it's the correct way to represent fluid, contact, or bearing loads over a region.",
                  "Confusing total force with pressure (force/area) is a common unit error; check whether your input expects N or Pa/MPa."),
            img_q("fea", "img-stress-contour", "intermediate", sv_stress_contour(),
                  "The color-mapped result showing red hotspots and blue low regions is which output?",
                  ["A stress (or displacement) contour plot",
                   "A finite-element mesh",
                   "A boundary condition",
                   "A load definition"], 0,
                  "Contour plots map a result field (von Mises stress, displacement) across the model with color, quickly revealing critical regions.",
                  "Peak stress at sharp re-entrant corners is often a mesh singularity that grows with refinement — evaluate stress at a small fillet or via linearization, not the corner node."),
            img_q("fea", "img-deformed", "intermediate", sv_deformed(),
                  "The dashed straight shape and solid curved shape show a beam before and after loading. What is displayed?",
                  ["The deformed (deflected) shape versus undeformed",
                   "A mesh refinement",
                   "A contact pair",
                   "A symmetry condition"], 0,
                  "Plotting the deformed shape (usually scaled) confirms the model deflects in a physically sensible way under the applied loads and constraints.",
                  "Deformation is shown with an exaggerated scale factor for visibility; don't read the on-screen displacement as the true magnitude — check the legend value."),
        ],
    },
]


# ============================ VIZ ===========================================
EXTRA_LESSONS["viz"] = [
    {
        "id": 6,
        "title": "Lesson 6: 看图识操作 (Visual Rendering ID)",
        "desc": "Identify the visualization/rendering concept from the diagram",
        "questions": [
            img_q("rendering", "img-three-point", "beginner", sv_three_point(),
                  "The diagram shows three lights placed around a subject as key, fill, and rim. What technique is this?",
                  ["Three-point lighting",
                   "Global illumination baking",
                   "Ambient occlusion",
                   "Depth of field"], 0,
                  "Three-point lighting (key + fill + rim) is the classic setup that models form, softens shadows, and separates the subject from the background.",
                  "Balance the key-to-fill ratio for the mood you want; equal key and fill flattens the subject and removes the sense of form."),
            img_q("rendering", "img-material-sphere", "beginner", sv_material_sphere(),
                  "The shaded preview ball with a bright highlight represents what?",
                  ["A PBR material preview (base color, roughness, metalness)",
                   "A camera frustum",
                   "A light source",
                   "A mesh density check"], 0,
                  "Material preview spheres show how a physically based material responds to light — its albedo, roughness, and metalness — before applying it to models.",
                  "Authoring albedo values outside the physically plausible range (too dark/bright) breaks PBR energy conservation and looks wrong under different lighting."),
            img_q("rendering", "img-hdri-dome", "beginner", sv_hdri_dome(),
                  "The dome surrounding the model, lit by a sun, provides scene illumination and reflections. What is it?",
                  ["An HDRI environment map lighting the scene",
                   "A clipping plane",
                   "A wireframe overlay",
                   "A UV unwrap"], 0,
                  "An HDRI environment captures real-world light across a high dynamic range, providing physically plausible ambient light, reflections, and soft shadows from one image.",
                  "Rotate the HDRI so its dominant light aligns with the intended sun/shadow direction; the default orientation rarely matches the desired composition."),
            img_q("rendering", "img-camera", "beginner", sv_camera_frustum(),
                  "The pyramid extending from the camera icon represents what?",
                  ["The camera's view frustum (field of view)",
                   "A light cone",
                   "A shadow volume",
                   "A reflection probe"], 0,
                  "The view frustum defines what the camera sees — its field of view, aspect, and near/far clipping — framing the composition of the render.",
                  "Very wide FOV (short focal length) exaggerates perspective distortion on architecture; match focal length to the look (e.g. 24–35 mm for interiors)."),
            img_q("rendering", "img-dof", "intermediate", sv_dof(),
                  "The middle object is sharp while the foreground and background are blurred. Which effect is this?",
                  ["Depth of field (focus falloff)",
                   "Motion blur",
                   "Ambient occlusion",
                   "Bloom"], 0,
                  "Depth of field blurs objects outside the focal plane, drawing the eye to the subject and adding photographic realism to product/arch shots.",
                  "Heavy DOF on architectural walkthroughs looks unnatural and hides detail; use it sparingly and keep the hero subject within the focal range."),
            img_q("rendering", "img-ao", "intermediate", sv_ao(),
                  "The darkening where two surfaces meet in a crevice represents which effect?",
                  ["Ambient occlusion (contact shadows)",
                   "Specular reflection",
                   "Depth of field",
                   "Chromatic aberration"], 0,
                  "Ambient occlusion approximates how ambient light is blocked in crevices and contact points, adding soft grounding shadows that improve depth perception.",
                  "AO is an approximation, not physically accurate global illumination; cranking AO too dark produces dirty-looking corners that read as smudges."),
        ],
    },
]


# --- L7 advanced text lessons for the remaining tracks ----------------------

EXTRA_LESSONS["bim"].append({
    "id": 7,
    "title": "Lesson 7: Advanced BIM Delivery",
    "desc": "openBIM exchange, model authoring discipline, and handover data",
    "questions": [
        txt_q("ifc", "ifc-mvd-purpose", "advanced",
              "What does a Model View Definition (MVD) specify within the IFC ecosystem?",
              ["A defined subset of the IFC schema for a particular exchange purpose (e.g. Coordination View, Reference View), so senders and receivers agree on what data is included",
               "The rendering quality of the exported model",
               "The compression algorithm used to shrink the IFC file",
               "The color scheme applied to elements in the viewer"], 0,
              "An MVD constrains the full IFC schema to the entities/properties needed for a use case, making exchanges predictable and certifiable between tools.",
              "Exporting a generic 'full IFC' without agreeing the MVD leads to receivers getting either missing data or bloated files with irrelevant entities."),
        txt_q("bim", "worksharing-sync", "intermediate",
              "In Revit worksharing, why should users Synchronize with Central (SWC) frequently and reload latest regularly?",
              ["Frequent sync merges each user's changes into the central model and pulls others' work, minimizing element-borrowing conflicts and data loss risk",
               "It increases the rendering resolution",
               "It is required to place a single wall",
               "It permanently locks the model for other users"], 0,
              "Regular SWC keeps the distributed local copies converged with central, reducing conflicts and the blast radius if a local file corrupts.",
              "Editing for hours without syncing risks large merge conflicts and losing work if the local file corrupts; sync at logical breakpoints."),
        txt_q("bim", "shared-coordinates-workflow", "advanced",
              "Why are shared coordinates (survey point / project base point) critical in a multi-model BIM project?",
              ["They give every discipline model a common real-world origin and orientation so federated models align correctly in the coordination environment",
               "They set the units of the drawing to metric",
               "They control the sun position for renderings only",
               "They define the print scale of sheets"], 0,
              "Shared coordinates tie models to a common survey origin; without them, linked models land in different locations and coordination is impossible.",
              "Never move the project base/survey point after links are established; do coordinate setup once, early, and lock it to avoid misaligned federations."),
        txt_q("bim", "cobie-handover", "advanced",
              "What is the primary deliverable value of COBie at project handover?",
              ["Structured asset and maintenance data (equipment, spaces, warranties, spares) that facility managers load directly into a CAFM/CMMS system",
               "A photorealistic flythrough video of the building",
               "A compressed archive of all design emails",
               "A set of 2D PDF drawings only"], 0,
              "COBie captures non-graphic asset information progressively so operators get a usable digital asset register at handover instead of boxes of manuals.",
              "Populating COBie only at 100% completion is hugely expensive; capture the data as elements are designed and specified, not retroactively."),
        txt_q("clash", "clash-workflow-cadence", "intermediate",
              "What is a healthy clash-detection workflow cadence on a live project?",
              ["Regular (e.g. weekly) coordination runs with grouped, prioritized, and assigned clashes tracked to resolution via BCF, not a single end-of-project sweep",
               "One clash check at the very end of design",
               "Never checking, trusting each discipline's model",
               "Only checking clashes after construction starts"], 0,
              "Frequent, grouped clash runs with assigned owners and tracked status catch issues while they're cheap to fix and keep the coordination model trustworthy.",
              "Dumping thousands of ungrouped clashes with no owner or priority overwhelms the team; group by system pairing and triage by severity."),
        txt_q("bim", "level-of-information-need", "advanced",
              "Under ISO 19650, how should the required detail of model information be specified?",
              ["By Level of Information Need tied to each deliverable's purpose and milestone, defining geometry, alphanumeric data, and documentation only as needed",
               "By demanding the maximum detail everywhere from day one",
               "By leaving it undefined and letting each modeler decide",
               "By copying detail levels from an unrelated past project"], 0,
              "Level of Information Need scopes information to what each purpose/milestone requires, preventing both under- and over-modeling.",
              "Requesting maximum detail globally wastes effort modeling elements not yet needed and bloats models; scope information to actual decisions being made."),
    ],
})

EXTRA_LESSONS["civil"].append({
    "id": 7,
    "title": "Lesson 7: Advanced Civil Design",
    "desc": "Surfaces, corridors, drainage, and survey data management",
    "questions": [
        txt_q("civil3d", "breaklines-surface", "advanced",
              "Why are breaklines important when building a TIN surface from survey data?",
              ["They force triangulation edges along linear features (curbs, ridges, ditches) so the surface honors abrupt grade changes instead of smoothing across them",
               "They reduce the file size of the drawing",
               "They set the contour line color",
               "They convert the surface to a solid"], 0,
              "Breaklines constrain the triangulation so the TIN represents real edges (top/bottom of curb, swale bottoms) rather than interpolating through them.",
              "Omitting breaklines lets triangles cross features like a ditch, flattening it and producing wrong volumes and drainage; add breaklines before analysis."),
        txt_q("civil3d", "corridor-targets", "advanced",
              "What role do 'targets' play in a Civil 3D corridor model?",
              ["They let subassemblies follow external geometry — widening to an offset alignment or daylighting to a surface — so the corridor adapts along its length",
               "They set the rendering material of the road",
               "They define the plot sheet size",
               "They store the project coordinate system"], 0,
              "Targets drive dynamic behavior (lane widening, daylight to surface) so the corridor responds to alignments/profiles/surfaces rather than being static.",
              "Unset or mis-assigned targets cause daylight subassemblies to miss the surface, leaving gaps and wrong earthwork; verify targets per region."),
        txt_q("civil3d", "superelevation", "advanced",
              "What is superelevation in road design and how is it applied?",
              ["The banking (cross-slope rotation) of the roadway through curves to counteract lateral acceleration, applied per design-speed standards along the alignment",
               "The vertical clearance under a bridge",
               "The thickness of the asphalt layer",
               "The width of the shoulder"], 0,
              "Superelevation rotates the pavement cross-section through curves so vehicles can maintain speed safely; it's computed from design speed and curve radius per standards (AASHTO).",
              "Transition (runoff) lengths must be adequate; abrupt superelevation application creates uncomfortable, unsafe rotation and drainage flat spots."),
        txt_q("civil3d", "pipe-hgl", "advanced",
              "In storm/sanitary network design, what does the hydraulic grade line (HGL) represent?",
              ["The elevation to which water would rise in the pipe under flow conditions; it must stay below rim elevations to avoid surcharging/flooding",
               "The centerline of the road above the pipe",
               "The property boundary along the pipe",
               "The color used to plot the pipe"], 0,
              "The HGL indicates pressure/energy along the network; keeping it below structure rims ensures gravity flow without surcharge or backup.",
              "Designing on pipe slope alone without checking the HGL can hide surcharging at junctions where head losses push water above the rim."),
        txt_q("civil3d", "survey-figure-prefix", "intermediate",
              "How do figure prefix libraries speed up survey processing?",
              ["Field codes on survey points automatically generate linework (curbs, edges of pavement) with the right layer and style as points are imported",
               "They compress the point cloud",
               "They set the drawing's plot scale",
               "They render the terrain photorealistically"], 0,
              "Figure prefixes map field codes to linework rules, so importing coded points builds edges and breaklines automatically instead of manual drafting.",
              "Inconsistent field coding by survey crews breaks automatic linework; agree and enforce a coding standard before fieldwork begins."),
        txt_q("civil3d", "grading-feature-lines", "intermediate",
              "What is the purpose of feature lines and grading objects in site design?",
              ["They define 3D linework with elevations/grades that drive a design surface, letting you model pads, ponds, and slopes that update as inputs change",
               "They are 2D annotation only with no elevation",
               "They set the sun angle for shadows",
               "They export the model to IFC"], 0,
              "Feature lines carry elevation and grade so grading objects project slopes to targets, building a dynamic finished-ground surface for earthwork.",
              "Feature lines that aren't connected to a target surface won't compute daylight/earthwork correctly; establish the reference surface first."),
    ],
})

EXTRA_LESSONS["sim"].append({
    "id": 7,
    "title": "Lesson 7: Advanced Analysis Practice",
    "desc": "Element choice, convergence, nonlinearity, and result validation",
    "questions": [
        txt_q("fea", "element-order", "advanced",
              "Why do second-order (quadratic) elements often give better accuracy than first-order (linear) elements for the same mesh?",
              ["Their mid-side nodes let element edges curve and represent bending/stress gradients more accurately, reducing shear locking on coarse meshes",
               "They always solve faster than linear elements",
               "They eliminate the need for boundary conditions",
               "They automatically apply loads"], 0,
              "Quadratic elements capture curved geometry and strain gradients better, so they resist the overstiff 'shear locking' that plagues linear elements in bending.",
              "Second-order elements cost more DOF and memory; for contact-dominated or explicit analyses, linear elements with a finer mesh are sometimes preferred."),
        txt_q("mesh", "mesh-convergence", "intermediate",
              "What does a mesh convergence study establish?",
              ["That the result of interest (e.g. peak stress) stops changing significantly as the mesh is refined, indicating a mesh-independent solution",
               "That the model renders faster",
               "That the material is linear elastic",
               "That the loads are correct"], 0,
              "Refining the mesh until the monitored quantity stabilizes confirms the discretization error is acceptable and results aren't mesh-dependent.",
              "Stresses at geometric singularities never converge — they keep rising with refinement; evaluate at a fillet or use stress linearization instead."),
        txt_q("fea", "geometric-nonlinearity", "advanced",
              "When must a geometrically nonlinear (large-deflection) analysis be used instead of linear static?",
              ["When deflections are large enough that the structure's stiffness changes as it deforms (e.g. slender beams, membranes, snap-through)",
               "Whenever the part is made of steel",
               "Only when thermal loads are present",
               "Only for 2D problems"], 0,
              "Large-deflection effects change the geometry and thus stiffness during loading; linear static (small-strain) assumptions then break down and under/over-predict response.",
              "Blindly running linear static on a slender or membrane structure can grossly mispredict behavior; check deflection magnitude relative to thickness/length."),
        txt_q("fea", "st-venant-boundary", "advanced",
              "How should Saint-Venant's principle guide interpretation of stresses near load/constraint points?",
              ["Local stresses right at idealized loads/constraints are unreliable, but away from them (a few characteristic lengths) the solution is valid",
               "Stresses are only valid at the constraints themselves",
               "The principle says all stresses are always uniform",
               "It applies only to thermal analysis"], 0,
              "Saint-Venant's principle says the details of how a load is applied only affect stresses locally; global response and stresses away from the region are trustworthy.",
              "Reporting the artificially high stress at a point constraint or point load is a classic error; move the evaluation away from the idealization or model the real contact."),
        txt_q("fea", "modal-analysis", "intermediate",
              "What does a modal (natural frequency) analysis compute, and why does it matter?",
              ["The structure's natural frequencies and mode shapes, used to avoid resonance with operating excitation frequencies",
               "The maximum static stress under a fixed load",
               "The heat transfer coefficient",
               "The manufacturing cost"], 0,
              "Modal analysis finds the frequencies at which a structure naturally vibrates; keeping excitation away from these avoids resonance and fatigue failure.",
              "Modal analysis is typically unloaded/linear; if preload significantly stiffens the structure (e.g. tensioned cable), run prestressed modal instead."),
        txt_q("fea", "units-consistency", "beginner",
              "Why is a consistent unit system essential in FEA even when the solver is 'unitless'?",
              ["The solver interprets all inputs in one consistent set (e.g. SI: m, kg, s, Pa); mixing mm with SI material data yields results wrong by orders of magnitude",
               "Units change the mesh density",
               "Units determine the element type",
               "Units only affect the plot colors"], 0,
              "Solvers do arithmetic on raw numbers; length, force, mass, and stress units must form a consistent system or forces/stresses come out grossly wrong.",
              "A very common blunder is modeling in mm but entering modulus in Pa instead of MPa, giving displacements 1000× off; fix the unit system up front."),
    ],
})

EXTRA_LESSONS["viz"].append({
    "id": 7,
    "title": "Lesson 7: Advanced Rendering Practice",
    "desc": "Color management, sampling, texturing, and output workflow",
    "questions": [
        txt_q("rendering", "linear-color-workflow", "advanced",
              "Why do production renderers compute lighting in linear color space and apply gamma/tone-mapping only at output?",
              ["Light adds linearly in reality; computing in linear space keeps blends and lighting physically correct, and the display transform is applied last for correct viewing",
               "Linear space makes files smaller",
               "It removes the need for lights in the scene",
               "It converts the render to grayscale"], 0,
              "Lighting math is only correct in linear space; textures are de-gammaed on input and the final image is tone-mapped/gamma-encoded for display, avoiding washed-out or muddy results.",
              "Feeding sRGB color textures into lighting math without linearizing (or double-applying gamma) produces incorrect, often over-bright or dull, renders."),
        txt_q("rendering", "sampling-noise", "intermediate",
              "In path-traced rendering, what is the relationship between samples per pixel and noise?",
              ["More samples average more light paths and reduce noise, but with diminishing returns — roughly halving noise requires ~4× the samples (and time)",
               "Fewer samples always produce cleaner images",
               "Samples only affect resolution, not noise",
               "Sample count cannot be changed"], 0,
              "Monte-Carlo noise falls with the square root of samples, so quality improvements get progressively more expensive; denoisers help bridge the gap.",
              "Cranking raw samples to kill fireflies/noise wastes hours; use adaptive sampling, light/portal optimization, and a denoiser instead of brute force."),
        txt_q("rendering", "uv-unwrapping", "intermediate",
              "Why is proper UV unwrapping necessary for textured models?",
              ["UVs map 2D texture coordinates onto 3D surfaces; poor unwrapping causes stretched, seamed, or misaligned textures regardless of texture quality",
               "UVs define the model's mass",
               "UVs control the render resolution",
               "UVs set the camera position"], 0,
              "UV coordinates determine how textures wrap onto geometry; clean, low-distortion UVs with sensible seams are prerequisite to good texturing.",
              "Auto-generated UVs on complex meshes often stretch or overlap; check with a checker texture and place seams in hidden areas before painting."),
        txt_q("rendering", "render-passes-aov", "advanced",
              "Why do studios render separate passes/AOVs (diffuse, specular, reflection, depth, cryptomatte) instead of a single beauty image?",
              ["They allow compositing adjustments (relight, tweak reflections, add depth-of-field, isolate objects) in post without re-rendering the whole scene",
               "They reduce the number of lights needed to zero",
               "They convert the scene to 2D vectors",
               "They are required to open the file"], 0,
              "Rendering to AOVs gives the compositor control to balance components and fix issues cheaply, avoiding costly full re-renders for small changes.",
              "Passes must sum back to the beauty correctly; mismatched color spaces or missing passes make the composite fail to reconstruct the original image."),
        txt_q("rendering", "proxy-instancing", "intermediate",
              "How do render proxies and instancing help with heavy scenes (vegetation, furniture, crowds)?",
              ["They reference one geometry definition many times so memory holds a single copy while the renderer places thousands of instances, enabling scenes too large to load as unique meshes",
               "They increase the polygon count of each object",
               "They disable lighting to save memory",
               "They convert meshes to point clouds permanently"], 0,
              "Instancing/proxies keep one master mesh in memory and replicate transforms, making forests or filled auditoriums feasible without exhausting RAM.",
              "Editing an instanced master affects every copy; when unique variation is needed, use randomized instancing rather than duplicating unique geometry."),
        txt_q("rendering", "camera-exposure", "beginner",
              "What does a physically based camera's exposure (ISO/shutter/f-stop or EV) control in a render?",
              ["The overall brightness mapping of the linear render to the final image, analogous to a real camera's exposure triangle",
               "The polygon count of the scene",
               "The number of lights allowed",
               "The file format of the output"], 0,
              "Physical camera exposure maps scene luminance to image tones; setting it deliberately (like a photographer) gives consistent, controllable brightness.",
              "Fixing a too-dark/bright render by scaling light intensities instead of exposure breaks physical light ratios; adjust exposure/tone-mapping first."),
    ],
})
