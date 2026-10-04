# HWPX package guide

Read this reference when inspecting, creating, or editing an HWPX file.

## Package invariants

HWPX is an OPC-like ZIP package. A typical document contains `mimetype`, `META-INF/manifest.xml`, `Contents/content.hpf`, `Contents/header.xml`, and one or more `Contents/section*.xml` files. Exact contents vary, so preserve entries that are not part of the requested change.

- `mimetype` should be the first ZIP entry and stored without compression. Its content is normally `application/hwp+zip`.
- XML is UTF-8. Parse it with a namespace-aware XML library and serialize without discarding unknown elements or namespace declarations.
- Body text normally appears in section XML under text elements such as namespaced `t` nodes, but text can be split across runs. Search semantically across adjacent runs before deciding a phrase is absent.
- Styles, numbering, fonts, border/fill definitions, and character/paragraph properties are referenced by IDs. Reuse existing compatible definitions where possible; if adding definitions, keep IDs unique and update every reference.
- Images and embedded objects require both the binary package entry and matching manifest/relationship metadata. Do not add only one side.

## Safe editing

1. Copy the source to a temporary working file and extract it into a new temporary directory.
2. Reject archive entries containing absolute paths or `..` path traversal before extraction.
3. Parse only the XML files needed for the requested edit. Preserve all other files byte-for-byte.
4. For phrase replacement across runs, build a logical text map from text nodes to character offsets, then redistribute replacement text deliberately. Avoid replacing raw serialized XML because it can corrupt escaping or cross element boundaries.
5. When inserting paragraphs or table rows, clone a structurally similar element from the same document and change only the necessary content and IDs.
6. Repackage with forward-slash paths. Put `mimetype` first and store it uncompressed; preserve compression for other entries.
7. Run `scripts/validate_hwpx.py OUTPUT.hwpx`. Validation is structural, not a substitute for opening and visually reviewing the document.

## Layout review

Compare page count and inspect the first page, every page containing an edit, and the final page. Check Korean font fallback, line wrapping, tables split across pages, header/footer positioning, footnotes, captions, equations, and anchored objects.
