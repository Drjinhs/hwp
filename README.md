# hwp — 아래한글 문서 제작용 Codex 스킬

진형석 박사의 독립적인 `$hwp` 스킬입니다. HWPX 제작·편집·검사와, 사용 가능한 한글 프로그램 또는 변환기를 통한 HWP 작업을 안내합니다. 기존 `$hwpx` 설치나 코드를 사용하지 않습니다.

## 설치

Python 3.10 이상이 필요합니다. 아래 명령의 `python`은 본인 컴퓨터에서 사용할 수 있는 Python 실행 명령(Windows에서는 `py` 등)으로 바꿀 수 있습니다. 추가 패키지 설치는 필요하지 않습니다.

```sh
git clone https://github.com/Drjinhs/hwp.git
cd hwp
python install.py --check
python install.py
```

Git이 없다면 GitHub의 **Code → Download ZIP**으로 내려받고 압축을 푼 폴더에서 설치 명령을 실행하세요.

`CODEX_HOME`이 있으면 그 아래 `skills/hwp`, 없으면 사용자 홈의 `.codex/skills/hwp`에 설치합니다. 기존 hwp 폴더는 `.codex/skill-backups`(또는 CODEX_HOME/skill-backups)에 복사한 뒤 5개 스킬 파일을 갱신합니다. 다른 스킬을 삭제하지 않습니다. 사용자 지정 경로는 `python install.py --target "경로/hwp"`로 설정합니다.

설치 후 새 Codex 작업을 열고 `$hwp`를 호출하세요. 자동 선택도 기본으로 허용됩니다. 기존 `$hwpx`와 선택 범위가 겹칠 수 있으므로 이 스킬을 지정하려면 `$hwp`를 명시하세요.

## 사용 예시

```text
$hwp 첨부한 양식을 복사하여 사업계획 보고서를 작성해줘. 결과는 .hwpx로 저장해줘.
$hwp 첨부 문서의 표와 서식을 보존하고 날짜와 기관명을 수정해줘.
$hwp 회의록을 작성하고 모든 페이지의 글꼴·줄바꿈·표 넘침을 확인해줘.
$hwp 이 문서를 .hwp로 저장해줘. 먼저 사용 가능한 한글 변환 도구를 확인해줘.
```

한국어 보고서·회의록의 기본 본문은 휴먼명조 14pt, 줄간격 145%입니다. 주석·사례는 중고딕 13pt, 첫 제목 아래의 빈 문단은 14pt 한 줄, 그 밖의 구분용 빈 문단은 7pt입니다. 문단 보호·내어쓰기·페이지 분리와 전체 페이지 검수 기준은 [SKILL.md](hwp/SKILL.md)에 있습니다. 현재 사용자의 별도 지시가 우선합니다.

## 지원 범위와 확인 한계

- HWPX: ZIP/XML을 분석하고 원본을 보존하며 수정합니다. 생성용 실행기는 별도로 포함하지 않으며, 새 문서는 실제로 열리는 사용자 양식 또는 정상 HWPX 기본 문서가 필요합니다.
- HWP: 바이너리를 직접 작성하거나 확장자만 바꾸지 않습니다. 설치된 한글 자동화나 검증된 변환기를 사용합니다. Python만으로 HWP 변환을 보장하지 않습니다.
- 한글 프로그램·글꼴·변환기는 이 저장소에 포함하지 않습니다. 원본 프롬프트에 적힌 개인 양식도 포함되어 있지 않습니다.
- `validate_hwpx.py`는 구조 검사이며 내용·스타일 참조·쪽수·실제 렌더링을 보증하지 않습니다. 렌더러가 없으면 출력 검수 미확인 범위를 알립니다.

실제 결과물의 구조 검사는 다음과 같습니다.

```sh
python hwp/scripts/validate_hwpx.py result.hwpx
```

## 기초자료

- [원본 설치 프롬프트](sources/hwp_스킬_설치_프롬프트.md)
- [원본 5개 파일의 SHA-256](sources/baseline-sha256.json)
- [HWPX 구조와 편집 규칙](hwp/references/hwpx-format.md)
- [HWP 변환 안내](hwp/references/hwp-conversion.md)
- [현재 배포 파일의 SHA-256](checksums.json)

원본의 5개 파일은 원본 체크섬과 일치하도록 추출했습니다. 배포판의 SKILL.md에는 소유자가 요청한 GitHub 동시 갱신 지침만 추가했습니다. 원본 자료와 현재 배포판의 체크섬을 구분해서 보관합니다. 자료를 내려받아 설치하고 사용할 수 있는 공개 저장소입니다.

## 업데이트

사용자는 저장소 폴더에서 `git pull --ff-only` 후 `python install.py`를 실행하면 최신 버전으로 설치할 수 있습니다.

관리자는 `$hwp` 변경 요청 때 `hwp/`에 변경을 반영하고 다음 명령으로 체크섬과 설치 파일을 갱신합니다. 설명이 달라지면 이 README도 수정합니다.

```sh
python tools/release.py
python install.py --check
python install.py
git add hwp checksums.json README.md
git commit -m "Update hwp skill"
git push origin main
```

소유자의 현재 요청으로 이후 `$hwp` 수정과 GitHub 갱신이 함께 승인되었습니다. Codex가 실제로 수정하는 작업에서 적용되는 지침이며, 다른 프로그램에서 변경한 파일을 상시 감시하는 서비스는 아닙니다. 새 환경에서는 GitHub 쓰기 인증이 필요합니다. 공개 사용자 문서 작업에서 생성된 결과물은 자동으로 게시하지 않습니다.
