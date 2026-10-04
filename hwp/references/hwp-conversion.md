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

## Observed Windows automation pitfalls

- A hidden Hancom window can wait at `SaveAs` for a file-access approval that is not visible. Show the test window and have the user approve the expected output path when necessary. Do not suppress unrelated recovery, password, signature, or macro dialogs.
- Hancom supplies an official Automation file-path security module. If using it, verify that `RegisterModule` returns true before claiming it is active. A false return must not be treated as a successful unattended setup. Avoid changing Windows security settings to force it to load. Use the normal user approval flow instead.
- In a tested Hancom 2024 environment, an LF-only multiline `HInsertText.Text` string lost its paragraph breaks. Insert paragraphs explicitly with the `BreakPara` action and verify the saved document's paragraph count and rendered page. Do not assume that the input string's newlines became paragraphs.
- Verify all expected paragraph text after reopening the saved HWP and HWPX. Then export the reopened documents to PDF, inspect every page, and compare the output where format fidelity matters. A one-page text-only smoke test does not establish table, image, equation, or multi-page fidelity.

Sources: [Hancom hidden-window/file-access guidance](https://forum.developer.hancom.com/t/c/1889), [Hancom 2024 module registration diagnosis](https://forum.developer.hancom.com/t/ai/3242). The repository's `tools/native-smoke.ps1` demonstrates the tested paragraph and interactive approval workflow; find it in the repository, not inside the five-file installed skill.
