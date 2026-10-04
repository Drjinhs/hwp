# Binary HWP conversion guide

Read this reference only when a `.hwp` binary file is an input or required output.

## Tool order

1. Prefer an installed Hancom Office application or its documented Windows automation interface when available and authorized.
2. Use LibreOffice headless conversion only after confirming the installed build can open the specific file. Treat the result as a conversion, not a lossless edit.
3. If neither route is available, do not fabricate an HWP file by changing an extension. Request HWPX/DOCX input or provide an HWPX deliverable if that meets the user's goal.

## Conversion safety

- Convert a copy in a temporary directory and write the final result to a new path.
- Open or render both source and converted versions when possible. Compare page count, fonts, tables, fields, equations, footnotes, headers/footers, images, and tracked changes.
- Macros, scripts, OLE objects, signatures, DRM, password protection, and external links may not survive conversion. Do not bypass protection or enable macros without explicit authorization.
- If Windows automation opens a visible application, avoid dismissing unexpected dialogs blindly. Stop and report prompts involving recovery, passwords, signatures, macros, or format repair.
- A successful converter exit code does not guarantee fidelity. Report the converter used and the scope of visual verification.
