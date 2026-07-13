#!/usr/bin/env python3
"""AI-assisted, per-page re-enrichment of 20 sample KB concept pages.

Unlike the earlier batch generator, every entry below is hand-authored and
unique: no shared skeleton, no term-substitution. Content is limited to
mainstream, well-documented concepts so the technical detail is verifiable.
Each page gets 2-3 topic-specific sections + a references block with real
outbound links, then its robots meta is flipped noindex -> index.

Insertion point: immediately before the "<software> Ecosystem Context"
spotlight card (i.e. after Definition / Why it matters / Common pitfalls).

Idempotent: re-running detects the inserted marker and skips.
"""

from __future__ import annotations

import glob
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MARKER = "data-enriched=\"sample20\""


def sec(title: str, body: str) -> str:
    return (
        '\n        <section class="kb-concept-section" ' + MARKER + ">\n"
        f"          <h2>{title}</h2>\n          {body}\n        </section>"
    )


def refs(items: list[tuple[str, str]]) -> str:
    lis = "\n".join(
        f'            <li><a href="{u}" target="_blank" rel="nofollow noopener">{t}</a></li>'
        for t, u in items
    )
    body = (
        '<p>Primary and vendor documentation used while writing this page '
        "(external links, not republished):</p>\n"
        f"          <ul>\n{lis}\n          </ul>"
    )
    return sec("References", body)


# ---------------------------------------------------------------------------
# Per-page content. Each value is a full HTML fragment (one or more sections).
# ---------------------------------------------------------------------------
PAGES: dict[str, str] = {}

PAGES["mates-solidworks"] = (
    sec(
        "How the mate solver removes degrees of freedom",
        "<p>Each unconstrained rigid body in an assembly has six degrees of freedom (DOF): "
        "three translational, three rotational. Every mate you add is an equation the solver "
        "must satisfy simultaneously at rebuild. A concentric mate removes two translational "
        "and two rotational DOF; a coincident face-to-face mate removes one translational and "
        "two rotational DOF. When the remaining DOF reach zero the component is "
        "<em>fully defined</em>; add one more consistent mate and it is over-defined but valid; "
        "add a contradictory one and SOLIDWORKS reports <code>Mate cannot be satisfied</code> "
        "and marks the mate with a red error.</p>",
    )
    + sec(
        "Picking a mate scheme that survives edits",
        "<p>Reference stable, permanent geometry — origin planes, axes, and published "
        "reference geometry — rather than model edges or faces that regenerate. For "
        "kinematics, prefer <strong>mechanical mates</strong> (gear, cam, rack-and-pinion, "
        "screw, hinge) over stacks of angle/limit mates: they express intent directly and "
        "rebuild faster. Group rigidly-moving parts into a subassembly and set it to "
        "<em>Rigid</em> so the top level only solves the moving interfaces. Use "
        "<code>View &gt; Hide/Show &gt; Mates</code> and the <em>Mate</em> folder's "
        "<em>View Mates</em> to audit what actually constrains a part.</p>",
    )
    + refs(
        [
            ("SOLIDWORKS Web Help — Mates", "https://help.solidworks.com/"),
            (
                "Dassault Systèmes SOLIDWORKS product site",
                "https://www.solidworks.com/",
            ),
        ]
    )
)

PAGES["configurations-solidworks"] = (
    sec(
        "What a configuration actually stores",
        "<p>A configuration is a named variation of the <em>same</em> document. It can "
        "suppress/unsuppress features and components, override dimension and equation values, "
        "change custom properties, and switch mate states — all without a second file. "
        "Configurations are stored inside the part/assembly and surfaced through the "
        "ConfigurationManager tab. Derived configurations inherit from a parent so shared "
        "changes propagate automatically.</p>",
    )
    + sec(
        "Driving configurations at scale",
        "<p>For a handful of variants, right-click in the ConfigurationManager and edit values "
        "manually. For a family (fasteners, fittings, standard frames), drive them from a "
        "<a href=\"./design-tables-solidworks\">Design Table</a> so an Excel grid owns every "
        "parameter. Keep a lightweight <em>as-machined</em> vs <em>as-cast</em> split with "
        "derived configurations, and expose only the properties downstream drawings and BOMs "
        "need via configuration-specific custom properties.</p>",
    )
    + refs([("SOLIDWORKS Web Help — Configurations", "https://help.solidworks.com/")])
)

PAGES["design-tables-solidworks"] = (
    sec(
        "The Excel-to-model contract",
        "<p>A Design Table is an embedded Excel worksheet where each row is a configuration and "
        "each column controls a parameter using a keyword syntax: <code>D1@Sketch1</code> for a "
        "dimension, <code>$STATE@Feature</code> for suppression, <code>$CONFIGURATION@name</code> "
        "for the row's configuration name, and <code>$PARTNUMBER</code>/<code>$COMMENT</code> for "
        "metadata. On close, SOLIDWORKS regenerates one configuration per row.</p>",
    )
    + sec(
        "Keeping tables robust",
        "<p>Rename features and dimensions <em>before</em> building the table so the column "
        "headers stay meaningful (<code>Length@BaseExtrude</code> beats <code>D1@Sketch1</code>). "
        "Use <em>Insert &gt; Tables &gt; Design Table &gt; Auto-create</em> to seed columns from "
        "existing configurations. Watch units — the table uses document units — and avoid "
        "circular equation references, which surface as rebuild errors on the affected rows "
        "only.</p>",
    )
    + refs([("SOLIDWORKS Web Help — Design Tables", "https://help.solidworks.com/")])
)

PAGES["rebuild-errors-solidworks"] = (
    sec(
        "Why the feature tree breaks",
        "<p>Most rebuild errors are <strong>dangling references</strong>: a sketch relation or "
        "feature pointed at an edge/face that no longer exists after an upstream change, so the "
        "reference turns dangling (shown with a red/yellow overlay). Common triggers are deleting "
        "a parent face, reordering features past their parents, or importing dumb geometry and "
        "then editing it. The tree evaluates top-down, so a single early break cascades into many "
        "downstream warnings.</p>",
    )
    + sec(
        "A repeatable triage",
        "<p>1) Read the first error, not the last — fixing the topmost usually clears the rest. "
        "2) Right-click the feature &gt; <em>What's Wrong</em> for the full diagnostic list. "
        "3) Use <em>Display/Delete Relations</em> to find and repair dangling sketch relations. "
        "4) Force a full rebuild with <kbd>Ctrl+Q</kbd> (vs <kbd>Ctrl+B</kbd> which only rebuilds "
        "changed features) to confirm the fix is stable. 5) Prevent recurrence by referencing "
        "planes and datums instead of transient faces.</p>",
    )
    + refs([("SOLIDWORKS Web Help — Rebuild and errors", "https://help.solidworks.com/")])
)

PAGES["weldments-solidworks"] = (
    sec(
        "Structural members, trim, and the cut list",
        "<p>Weldments build a frame from a single multibody part: sketch the skeleton, then "
        "<em>Insert &gt; Weldments &gt; Structural Member</em> sweeps a library profile "
        "(ISO/ANSI/DIN sections) along each segment. <em>Trim/Extend</em> resolves corner "
        "conditions (end-miter, butt). Each member becomes a solid body, and SOLIDWORKS "
        "auto-populates a <strong>Cut List</strong> that groups identical bodies with lengths and "
        "quantities — the basis of a cut-length BOM.</p>",
    )
    + sec(
        "Gussets, end caps, and weld beads",
        "<p>Add <em>Gusset</em> and <em>End Cap</em> features for real fabrication detail, and "
        "<em>Weld Bead</em> features to document fillet/groove welds; weld beads carry size and "
        "length data into the cut list and drawing weld symbols. Create custom profiles by saving "
        "a sketch as a <em>Library Feature Part</em> (.sldlfp) under the weldment profiles folder "
        "so they appear in the Structural Member picker.</p>",
    )
    + refs([("SOLIDWORKS Web Help — Weldments", "https://help.solidworks.com/")])
)

PAGES["sheet-metal-solidworks"] = (
    sec(
        "Bends, K-factor, and the flat pattern",
        "<p>Sheet metal parts carry a constant thickness and a bend model so they can unfold to a "
        "manufacturable flat. The neutral axis position is set by the <strong>K-factor</strong> "
        "(typically ~0.3–0.5 for steel), which — with thickness and bend radius — determines the "
        "<em>bend allowance</em> and <em>bend deduction</em>. Start with <em>Base Flange/Tab</em> "
        "or convert a solid with <em>Insert Bends</em>/<em>Convert to Sheet Metal</em>; the "
        "<em>Flat-Pattern</em> feature at the tree bottom generates the DXF-ready unfold.</p>",
    )
    + sec(
        "Getting parts that fab correctly",
        "<p>Drive bend behaviour from a shop <strong>bend table</strong> or gauge table rather "
        "than a single K-factor guess, so allowances match the press brake. Add relief cuts and "
        "correct corner treatments to avoid tearing, and export the flat pattern to DXF for "
        "laser/turret. Model with fabrication tolerances in mind — flanges shorter than a few "
        "material thicknesses cannot be bent reliably.</p>",
    )
    + refs([("SOLIDWORKS Web Help — Sheet Metal", "https://help.solidworks.com/")])
)

PAGES["smart-dimensions-solidworks"] = (
    sec(
        "Driving vs. driven dimensions",
        "<p>The <em>Smart Dimension</em> tool infers the dimension type from what you select "
        "(linear, radial, angular, arc-length). In a sketch these are <strong>driving</strong> "
        "dimensions: changing the value moves the geometry, and a fully-dimensioned sketch turns "
        "black (fully defined). In drawings, dimensions are <strong>driven</strong> by the model "
        "by default; a driven dimension (shown in grey/parentheses) reports geometry but cannot "
        "change it.</p>",
    )
    + sec(
        "Productivity options worth knowing",
        "<p>Enable <em>rapid dimension</em> to place dimensions on a snapping ring without cursor "
        "jitter, and use <em>DimXpert</em> to auto-apply a tolerance-aware dimension scheme for "
        "MBD. Tab-cycle witness-line attach points, and type equations directly into the modify "
        "box (e.g. <code>=\"Length\"/2</code>) to link a dimension to a global variable.</p>",
    )
    + refs([("SOLIDWORKS Web Help — Dimensions", "https://help.solidworks.com/")])
)

PAGES["model-based-definition-solidworks"] = (
    sec(
        "PMI as the authority, not the drawing",
        "<p>Model-Based Definition (MBD) attaches Product and Manufacturing Information — "
        "dimensions, GD&amp;T, datums, surface finish, notes — directly to the 3D model as "
        "annotations organised on <em>3D Views</em>. The 3D dataset becomes the authority, "
        "reducing or eliminating the 2D drawing. GD&amp;T here follows <strong>ASME Y14.5</strong> "
        "(2009/2018) or the ISO GPS system (e.g. <strong>ISO 1101</strong>), and MBD practice is "
        "codified in <strong>ASME Y14.41</strong> and <strong>ISO 16792</strong>.</p>",
    )
    + sec(
        "Publishing a consumable package",
        "<p>SOLIDWORKS MBD publishes to <strong>3D PDF</strong> (with rotatable views and a parts "
        "list) and to <strong>STEP AP242</strong>, which — unlike AP203/AP214 — carries semantic "
        "PMI that downstream CMM and CAM tools can read programmatically. Validate that datums, "
        "tolerances, and surface finish survive the export before releasing, and organise 3D Views "
        "so each captures a coherent set of features for inspection.</p>",
    )
    + refs(
        [
            ("SOLIDWORKS MBD product page", "https://www.solidworks.com/"),
            ("ISO 16792 — Technical product documentation (ISO catalogue)", "https://www.iso.org/"),
        ]
    )
)

PAGES["ilogic-inventor"] = (
    sec(
        "Rules, parameters, and triggers",
        "<p>iLogic embeds design logic in Inventor documents as <strong>rules</strong> written in "
        "a VB.NET-based language. Rules read and write model <em>parameters</em> "
        "(<code>Length = 120</code>), suppress features, drive iProperties, swap components, and "
        "control configurations. Rules fire on events — <em>After Open Document</em>, parameter "
        "change, or manual run — so a model can reconfigure itself when an input changes.</p>",
    )
    + sec(
        "Building maintainable automation",
        "<p>Expose user inputs through a <em>form</em> so non-authors drive the model without "
        "editing code, and centralise shared logic in an external rule stored in the project so "
        "many documents reuse it. Prefer <code>Parameter(\"name\")</code> and the iLogic snippet "
        "library over hard-coded strings, guard against missing references, and keep rule "
        "execution order explicit to avoid circular triggering.</p>",
    )
    + refs([("Autodesk Inventor Help — iLogic", "https://help.autodesk.com/view/INVNTOR/2024/ENU/")])
)

PAGES["frame-generator-inventor"] = (
    sec(
        "Skeleton-driven framing",
        "<p>Frame Generator places standard structural shapes (ISO/AISC/DIN angle, channel, HSS, "
        "I-beam) along the edges of a <em>skeleton</em> sketch or existing geometry. Each member "
        "is inserted as its own part in a dedicated frame subassembly and linked back to the "
        "skeleton, so moving a skeleton line updates the framing. End treatments — "
        "<em>Miter</em>, <em>Trim/Extend</em>, <em>Notch</em>, <em>Lengthen/Shorten</em> — resolve "
        "how members meet at joints.</p>",
    )
    + sec(
        "From frame to BOM",
        "<p>Because every member is a real part with a category and size, the assembly BOM and "
        "structured parts list report cut lengths and quantities directly. Reuse authored members "
        "by publishing custom profiles into the Content Center, and drive repeated frames from the "
        "skeleton so a single sketch edit re-cuts the whole structure.</p>",
    )
    + refs([("Autodesk Inventor Help — Frame Generator", "https://help.autodesk.com/view/INVNTOR/2024/ENU/")])
)

PAGES["content-centre-inventor"] = (
    sec(
        "A managed library of standard parts",
        "<p>Content Center is a database of standard parts and features — fasteners, steel "
        "shapes, shaft parts, bearings — organised into <em>libraries</em> and <em>families</em> "
        "keyed by standard (ISO, ANSI, DIN, GB). Placing a member generates a concrete part sized "
        "from the family table. Read-only supplied libraries stay pristine; custom content goes "
        "into a separate read/write library you can back up and share.</p>",
    )
    + sec(
        "Standard vs. custom, and file hygiene",
        "<p>Choose the <em>Standard</em> part option to reuse one file across the project, or "
        "<em>Custom</em> to generate a uniquely-numbered instance. Point the Content Center Files "
        "location at a managed folder (or Vault) so generated parts are governed, and prune unused "
        "families to keep the library — which can be large — responsive.</p>",
    )
    + refs([("Autodesk Inventor Help — Content Center", "https://help.autodesk.com/view/INVNTOR/2024/ENU/")])
)

PAGES["iparts-inventor"] = (
    sec(
        "Table-driven part and assembly families",
        "<p>An iPart turns one part into a factory: an embedded table where each row is a member "
        "with its own dimensions, feature suppression, iProperties, and file name. iAssemblies do "
        "the same for assemblies, additionally controlling component inclusion. Placing an iPart "
        "prompts for the member row and generates the corresponding concrete file.</p>",
    )
    + sec(
        "Authoring clean factories",
        "<p>Rename parameters before building the table so columns are legible, mark key columns "
        "as <em>keys</em> to drive the placement dialog, and keep member counts sane — very large "
        "tables are better served by Content Center or iLogic. Use custom (versus standard) member "
        "behaviour when each placement must be an independently-numbered file.</p>",
    )
    + refs([("Autodesk Inventor Help — iParts and iAssemblies", "https://help.autodesk.com/view/INVNTOR/2024/ENU/")])
)

PAGES["constraints-joints-inventor"] = (
    sec(
        "Two ways to assemble the same DOF",
        "<p>Classic <strong>assembly constraints</strong> (Mate, Flush, Angle, Tangent, Insert, "
        "Symmetry) each remove specific degrees of freedom and often require several to define one "
        "connection. The newer <strong>Joint</strong> command expresses the connection directly — "
        "Rigid, Rotational, Slider, Cylindrical, Planar, Ball — usually with a single placement, "
        "and shows remaining motion immediately. Both can coexist in one assembly.</p>",
    )
    + sec(
        "Choosing constraints vs. joints",
        "<p>Use joints for mechanisms where motion is the point (a hinge, a slider) — they are "
        "faster to place and clearer to read. Use constraints for precise, incremental positioning "
        "and legacy compatibility. In either case reference origin work features rather than "
        "transient faces so the assembly rebuilds predictably, and grounding the first component "
        "removes its six DOF as the fixed datum.</p>",
    )
    + refs([("Autodesk Inventor Help — Assemble (constraints and joints)", "https://help.autodesk.com/view/INVNTOR/2024/ENU/")])
)

PAGES["timeline-fusion"] = (
    sec(
        "Parametric history you can scrub",
        "<p>With <em>Capture Design History</em> on, Fusion records every operation as an ordered "
        "node on the Timeline at the bottom of the canvas. Dragging the marker rolls the model "
        "back and forth; double-clicking a node re-opens that operation for editing, and "
        "dependent downstream features recompute. Right-click nodes to reorder, suppress, or "
        "roll edits, and group related nodes to keep long histories readable.</p>",
    )
    + sec(
        "Parametric vs. direct trade-off",
        "<p>Turning history <em>off</em> switches Fusion into direct modelling — no timeline, "
        "faster edits on imported or messy geometry, but no parametric replay. Keep history on for "
        "design intent and configurations; switch off (or use a base feature) when working with "
        "large imported bodies where a full history would be costly. See "
        "<a href=\"./parametric-vs-direct-fusion\">parametric vs. direct modelling</a>.</p>",
    )
    + refs([("Autodesk Fusion Help — Timeline", "https://help.autodesk.com/view/fusion360/ENU/")])
)

PAGES["joints-fusion"] = (
    sec(
        "Joint types and the motion they allow",
        "<p>Fusion joints define both position and permitted motion between two components: "
        "<strong>Rigid</strong> (0 DOF), <strong>Revolute</strong> (1 rotational), "
        "<strong>Slider</strong> (1 translational), <strong>Cylindrical</strong> (rotate + slide "
        "on one axis), <strong>Pin-Slot</strong> (rotate + translate), <strong>Planar</strong>, "
        "and <strong>Ball</strong> (spherical). You locate a joint by picking joint origins "
        "(face/edge/point snaps) on each component.</p>",
    )
    + sec(
        "As-built joints, motion links, and limits",
        "<p>Use a normal <em>Joint</em> to snap parts together, or an <em>As-Built Joint</em> to "
        "add motion to components already in their final position (common for imported "
        "assemblies). Add <em>Joint Limits</em> to bound travel/rotation, <em>Motion Link</em> to "
        "couple two joints (e.g. gear ratios), and <em>Contact Sets</em> so parts collide instead "
        "of passing through during motion study.</p>",
    )
    + refs([("Autodesk Fusion Help — Joints", "https://help.autodesk.com/view/fusion360/ENU/")])
)

PAGES["generative-design-fusion"] = (
    sec(
        "Setting up a study",
        "<p>Generative Design explores many shapes from your engineering intent rather than a "
        "single modelled form. You define <strong>preserve</strong> geometry (must keep — mounting "
        "faces, bosses), <strong>obstacle</strong> geometry (keep-out zones), then apply "
        "<strong>structural loads</strong>, <strong>constraints</strong>, a target (minimise mass "
        "at a safety factor), materials, and manufacturing methods (additive, milling 2.5–5 axis, "
        "die casting). Fusion solves the studies in the cloud and returns a range of outcomes.</p>",
    )
    + sec(
        "Reading and using outcomes",
        "<p>Compare outcomes by mass, max displacement, and safety factor in the explore view; "
        "each is a mesh you can promote into the design and then reconstruct as editable geometry "
        "for downstream detailing. Loads and manufacturing constraints drive the result more than "
        "anything else — under-constrained studies produce unusable organic shapes, so anchor them "
        "in real service conditions.</p>",
    )
    + refs([("Autodesk Fusion Help — Generative Design", "https://help.autodesk.com/view/fusion360/ENU/")])
)

PAGES["sketchup-term-1"] = (
    sec(
        "Turning faces into volume",
        "<p>Push/Pull (<kbd>P</kbd>) extrudes a flat face into 3D along its normal: click a face, "
        "drag, and type an exact distance. Double-clicking a face repeats the last push/pull "
        "value, and holding <kbd>Ctrl</kbd> (Option on macOS) starts a new face so you stack "
        "volume instead of moving the existing one. Push/Pull only operates on planar faces — "
        "curved surfaces need Follow Me or an extension.</p>",
    )
    + sec(
        "Working with it cleanly",
        "<p>Because SketchUp uses connected edge/face geometry, pushing one face can unintentionally "
        "merge or delete neighbouring geometry — isolate objects inside "
        "<a href=\"./sketchup-term-2\">groups or components</a> before editing. Pull a face back to "
        "zero thickness on a solid to punch a hole through it, and re-type a distance immediately "
        "after an operation to correct it without redoing the drag.</p>",
    )
    + refs([("SketchUp Help Center — Drawing tools", "https://help.sketchup.com/")])
)

PAGES["sketchup-term-2"] = (
    sec(
        "Instances vs. unique copies",
        "<p>Both groups and components isolate geometry from the surrounding model, but a "
        "<strong>component</strong> is an <em>instance</em> of a shared definition: edit one and "
        "every instance updates, which is ideal for repeated elements (windows, chairs, bolts) and "
        "keeps file size down. A <strong>group</strong> is effectively a one-off component whose "
        "edits stay local — best for a unique assembly you want to keep separate.</p>",
    )
    + sec(
        "Why it matters for performance and structure",
        "<p>Reusing components instead of copying groups dramatically reduces file size and "
        "redraw cost in large models, and components carry axes, a name, and metadata usable in "
        "reports and <a href=\"./sketchup-term-9\">dynamic components</a>. Use <em>Make Unique</em> "
        "to split an instance you want to diverge, and nest groups/components deliberately so the "
        "Outliner mirrors your real object hierarchy.</p>",
    )
    + refs([("SketchUp Help Center — Groups and components", "https://help.sketchup.com/")])
)

PAGES["rhinoceros-term-1"] = (
    sec(
        "What defines a NURBS surface",
        "<p>NURBS (Non-Uniform Rational B-Splines) represent curves and surfaces exactly from a "
        "few parameters: a grid of <strong>control points</strong>, a <strong>degree</strong> "
        "(degree 3 is the common smooth default), <strong>knots</strong> (the non-uniform "
        "parameter spacing), and per-point <strong>weights</strong> (the rational part, which lets "
        "NURBS capture conics like true circles and ellipses). The curve/surface passes near — not "
        "through — its control points, and editing a point produces predictable local change.</p>",
    )
    + sec(
        "Continuity and clean geometry",
        "<p>Adjacent surfaces meet with a defined continuity: <strong>G0</strong> (touching), "
        "<strong>G1</strong> (tangent), or <strong>G2</strong> (curvature-continuous, required for "
        "class-A reflections). Keep degree and point counts as low as the shape allows — "
        "over-heavy control grids cause waviness and heavy downstream trims. See "
        "<a href=\"./rhinoceros-term-4\">Mesh vs. NURBS</a> for when a polygon mesh is the better "
        "representation.</p>",
    )
    + refs(
        [
            ("Rhino Help — What are NURBS?", "https://docs.mcneel.com/rhino/8/help/en-us/"),
            ("McNeel Rhinoceros product site", "https://www.rhino3d.com/"),
        ]
    )
)

PAGES["rhinoceros-term-2"] = (
    sec(
        "Visual programming for geometry",
        "<p>Grasshopper is Rhino's node-based visual programming environment: you wire "
        "<strong>components</strong> (each a small operation) on a canvas, feeding geometry and "
        "numbers through their inputs/outputs to build a live, parametric definition. Changing a "
        "slider or input re-runs the graph and updates the preview in Rhino instantly — no manual "
        "remodelling. It ships inside Rhino and needs no separate install on current versions.</p>",
    )
    + sec(
        "Data trees and good habits",
        "<p>Grasshopper organises data in <strong>data trees</strong> (hierarchical branches), and "
        "most confusion comes from mismatched tree structure — learn <em>Graft</em>, "
        "<em>Flatten</em>, and <em>Simplify</em> early. Bake only when you need permanent Rhino "
        "geometry, group and label clusters for readability, and reach for scripting components "
        "(Python/C#) when a graph grows unwieldy.</p>",
    )
    + refs(
        [
            ("Rhino Help — Grasshopper", "https://docs.mcneel.com/rhino/8/help/en-us/"),
            ("Grasshopper community & docs", "https://www.grasshopper3d.com/"),
        ]
    )
)


def insert_before_spotlight(html: str, block: str) -> str:
    idx = html.find('<div class="kb-spotlight-card"')
    if idx == -1:
        return html
    sec_idx = html.rfind('<section class="kb-concept-section"', 0, idx)
    if sec_idx == -1:
        return html
    return html[:sec_idx] + block.lstrip("\n") + "\n\n        " + html[sec_idx:]


def main() -> int:
    dry = "--apply" not in sys.argv
    changed = 0
    for slug, block in PAGES.items():
        f = REPO / "kb" / "concepts" / f"{slug}.html"
        if not f.exists():
            print("MISSING", slug)
            continue
        html = f.read_text(encoding="utf-8")
        if MARKER in html:
            continue  # idempotent
        new = insert_before_spotlight(html, block)
        new = new.replace(
            '<meta name="robots" content="noindex, follow, max-image-preview:large" />',
            '<meta name="robots" content="index, follow, max-image-preview:large" />',
        )
        if new != html:
            changed += 1
            if not dry:
                f.write_text(new, encoding="utf-8")
    mode = "DRY-RUN (use --apply)" if dry else "APPLIED"
    print(f"{mode}: {changed}/{len(PAGES)} pages enriched + re-indexed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
