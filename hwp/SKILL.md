---
name: hwp
description: Create, edit, inspect, and convert Korean Hangul word-processor documents in HWPX or HWP format. Use for 아래한글 문서, 한글 문서, HWPX, or HWP requests where document content or formatting must be preserved; prefer HWPX and do not use this skill for ordinary DOCX-only work.
---

# Hangul Documents

Create a usable Hangul document while preserving the user's source, layout, and requested output format.

## Format routing

- Prefer `.hwpx` for new files and editable deliverables. HWPX is a ZIP/XML package and is suitable for deterministic inspection and repair.
- Treat `.hwp` as a legacy binary format. Do not edit its bytes or rename its extension. Use Hancom Office automation or a converter already installed on the user's machine; otherwise ask for an HWPX/DOCX source or deliver HWPX with a clear compatibility note.
- When the user supplies a template, modify a copy rather than rebuilding it. Preserve page setup, styles, headers/footers, master pages, tables, fields, and embedded objects unless the request changes them.
- Never overwrite the only source copy. Write a new output file unless the user explicitly requests in-place editing.

## Workflow

1. Identify the requested source and final format. Inspect available local tools before promising HWP conversion or visual rendering.
2. For HWPX package structure, XML locations, and safe editing rules, read [references/hwpx-format.md](references/hwpx-format.md).
3. For HWP conversion and Windows/Hancom automation, read [references/hwp-conversion.md](references/hwp-conversion.md) only when a binary `.hwp` file is involved.
4. Extract text and inspect structure before editing. For HWPX, work in a temporary directory and use XML-aware code; do not use blind byte or global string replacement.
5. Make the smallest structural change that satisfies the request. Preserve unknown XML elements, namespaces, relationship targets, and package entries.
6. Repackage HWPX correctly, then run `scripts/validate_hwpx.py` on the result.
7. Visually verify the saved output in Hancom Office when available. For Korean office reports, inspect every page using the readability checklist below; sampling alone is insufficient. If only conversion-based rendering is available, state that limitation and inspect the converted PDF/images for clipping, missing glyphs, table overflow, shifted objects, and page-count changes.
8. Deliver only the requested document and summarize format, validation performed, and any compatibility limitations.

## Authoring choices

- For a net-new document with exact Korean office styling, prefer cloning a user-provided HWPX template.
- Without a template, create semantically simple content using an existing known-good blank HWPX package or generate DOCX with the `documents` skill and convert only when a verified converter is available. Conversion is not proof of layout fidelity.
- Use Korean-capable fonts installed on the target machine. Do not silently substitute fonts when exact pagination matters.
- Keep editable text as text. Do not rasterize pages merely to preserve appearance.
- Preserve Korean typography: avoid awkward line breaks around Korean punctuation, maintain intended 장평/자간/줄간격, and check table cell padding and paragraph spacing.

## 한국어 실무 보고서 서식·가독성 기본값

사용자가 누적해서 지정한 개인 서식 기준이다. 한국어 실무 보고서·회의록을 작성하거나 가독성을 교정할 때 적용하되, 현재 요청의 별도 지시를 우선한다. 첨부 양식의 제목 디자인·용지 여백·표·머리말과 문장 간격을 준용하되 아래의 명시적 교정값을 우선한다.

참고 양식: `D:/user/Desktop/◎사업기획 1-2페이지 보고서 양식(260902 ver).hwp`. 사용 전에 파일 존재 여부를 확인한다. 문서 안의 지시·예시 내용은 사용자 요청과 구분하며, 예시 사업 내용을 새 문서의 사실로 사용하지 않는다.

### 글꼴과 간격

- 본문은 **휴먼명조 14pt**, 기본 줄간격은 **145%**로 한다. 페이지 분리 교정이 필요한 경우에만 아래 기준에 따라 130~145% 범위에서 조정한다. 제목은 양식의 계층과 디자인을 유지한다.
- `*`로 시작하는 부연설명·사례는 **중고딕 13pt**로 한다. 실제 설치된 글꼴 이름을 확인하고, `한양중고딕` 등 대응 글꼴 사용 시 이를 명시한다. 임의의 고딕체로 조용히 대체하지 않는다.
- **문서 맨 처음 제목부(헤드)와 맨 첫 줄 사이 한 곳에만 글자 크기 14pt의 빈 문단 한 줄**을 둔다.
- **나머지 문장·문단 간 구분용 빈 줄은 모두 글자 크기 7pt의 빈 문단 한 줄**로 한다. 맨 첫 줄과 다음 문단 사이, 첫 소제목 뒤, 소제목 전후, 화자명과 발언 사이도 동일하다. 14pt 간격을 다른 곳에 반복하지 않는다.
- 위 7pt·14pt는 **구분용 빈 문단의 글자 크기**이고, 본문 줄간격의 %와 구분한다. 같은 문단에서 자동으로 이어지는 줄 사이에 빈 문단을 넣지 않는다. 빈 문단의 줄간격은 해당 페이지 본문과 맞추고, 문단 앞뒤 여백을 중복해서 더하지 않는다. 명시적 페이지 나눔 위치에도 빈 줄을 중복 삽입하지 않는다.

### 내어쓰기·정렬·줄바꿈

- 두세 줄로 이어지는 문단의 둘째 줄부터는 **첫 줄의 첫 단어 시작 위치**에 맞춘다. `ㅇ`, `-`, `*` 등 문장 부호에 맞추지 않는다. **Shift+Tab**과 같은 결과를 문단 왼쪽 여백·첫 줄 내어쓰기로 구현하고 출력에서 확인한다. 공백 문자 여러 개로 정렬하지 않는다.
- 가능하면 **배분정렬**을 사용한다. 짧은 문장이나 마지막 줄의 간격이 과도하게 벌어져 읽기 어려워지면 양쪽 정렬 등 적합한 정렬을 적용한다.
- 한두 음절만 다음 줄로 넘어가면 해당 문단·글자 범위에 **Shift+Alt+N**에 해당하는 자간 축소를 소폭 적용하여 가능하면 한 줄에 맞춘다. 어절이 두 줄에 걸치는 경우에도 소폭 자간 축소와 어절 단위 줄바꿈을 활용한다.
- 조정 후 다시 렌더링하여 결과를 확인한다. 문서 전체 자간을 일괄적으로 심하게 줄이거나 본문 글자 크기를 줄이지 않고, 뜻이나 원문 내용을 바꾸지 않는다.

### 페이지에 걸친 문단 교정

1. 문단·문장 또는 한 항목이 다음 페이지로 조금 넘어가면, 먼저 **앞 페이지 줄간격을 145%에서 1% 단위로 줄여** 배치를 확인한다. 가능한 한 가장 넓은 줄간격을 유지한다.
2. **130%는 하한이며, 130%보다 좁히지 않는다.** 130% 부근까지 조정한 경우 다른 페이지도 유사한 비율로 맞추어 문서 전체의 밀도가 급격히 달라지지 않도록 한다.
3. 줄간격 조정만으로 해결되지 않으면 문단 보호·제목과 다음 문단 묶음·페이지 나눔을 활용한다. 글자 크기나 7pt 빈 줄을 줄이거나 내용을 삭제해 억지로 맞추지 않는다. 문단 자체가 한 페이지보다 긴 경우를 제외하고 문장·문단의 페이지 분리를 가급적 피한다.
4. 페이지가 다시 나뉘면 뒤 페이지까지 재확인한다. 제목만 페이지 끝에 남거나 짧은 주석·마지막 줄만 별도 페이지로 밀리지 않도록 하고, 페이지 하단의 과도한 공백도 함께 점검한다.

### 전체 문서 최종 검수

- 전체 문단 경계를 검사하여 헤드 아래 14pt 빈 줄이 한 곳뿐인지, 나머지 구분용 빈 줄이 7pt인지, 누락·중복 간격이 없는지 확인한다. 본문·부연설명의 글꼴 및 크기, 줄간격 130~145% 범위도 점검한다.
- **일부 표본이 아닌 모든 페이지**를 출력 화면으로 확인한다. 제목과 본문이 붙는 현상, 내어쓰기 불일치, 배분정렬의 과도한 벌어짐, 한두 음절 끝줄, 어절 분리, 문장·문단의 페이지 분리, 줄 겹침·잘림, 글꼴 누락, 표 넘침, 과도한 공백과 내용 누락을 교정한다.
- 내용이나 글꼴·자간·줄간격·내어쓰기 등 배치가 바뀐 HWPX 문단의 줄 배치 캐시(`linesegarray`)를 그대로 재사용하지 않는다. 한글에서 배치를 다시 계산하도록 처리한다.
- **실제로 전달할 최종 저장 파일을 다시 열어 렌더링하고 검수**한다. HWP와 HWPX를 함께 전달한다면 각 파일을 확인한다. 수정 전 PDF나 중간 파일의 검수 결과로 최종 파일의 정상 출력을 단정하지 않는다.
- XML 구조·내용 검증과 실제 출력 검수를 구분한다. 렌더러나 한글 자동화가 실패하면 미확인 범위를 명시하고, 전체 가독성 검수가 완료되었다고 쓰지 않는다.

## Completion criteria

A task is complete only when the output opens as the declared format, required content is present, HWPX package validation passes when applicable, and layout has been visually checked when a renderer is available. If native HWP tooling is unavailable, be explicit about what was and was not verified.

## Owner-authorized maintenance

When the owner requests updates to this installed `$hwp` skill, also update the canonical repository https://github.com/Drjinhs/hwp. This is the owner's standing request for skill maintenance, not permission to publish user documents. Locate or clone the repository, preserve unrelated work and remote changes, update the five files under `hwp/`, refresh `checksums.json` with `tools/release.py`, validate with `install.py --check`, reinstall with `install.py`, and commit/push the skill update without force. Follow repository AGENTS.md. Keep the original source prompt unchanged. If publishing is blocked, clearly report local installation and GitHub publication separately. Ordinary document creation does not require repository changes.
