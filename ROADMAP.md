# Tech-Me Roadmap

สถานะ ณ 19 พ.ย. 2026 · เวอร์ชันปัจจุบัน v0.3.0 (GitHub Latest release; cross-agent evals ยังไม่ครบ v1.0) · เอกสารนี้เป็นข้อเสนอเพื่อวางแผน ไม่ใช่คำมั่นสัญญา ขนาดงานเป็นการประมาณคร่าว ๆ (S = ไม่เกิน 1 วัน, M = 1-3 วัน, L = มากกว่า 3 วัน)

## 1. หลักการจัดลำดับ

1. **หลักฐานก่อนการโปรโมต**: ไม่ประชาสัมพันธ์ก่อนมีผลทดสอบที่ทำซ้ำได้
2. **แก้ช่องโหว่ที่เห็นแล้วก่อนเพิ่มฟีเจอร์**
3. **ความซับซ้อนใหม่** (โหมด, plugin, command) ต้องมีเหตุผลจากการใช้งานจริง ไม่ใช่เพราะ skill อื่นมี
4. **ซื่อสัตย์กับผู้ใช้**: ป้าย pre-release และหัวข้อ Limitations ต้องตรงกับหลักฐานเสมอ

## 2. จุดเริ่มต้น (ณ v0.1.0)

**ตรวจแล้ว**

- Release v0.1.0 เป็น pre-release, tag เป็น annotated ชี้ commit 2a3c59b บน main
- มี SKILL.md, references (discovery, evaluation, output), ADR template, validator, tests, CI, PUBLISHING.md, SECURITY.md, CONTRIBUTING.md
- evals: 14 สถานการณ์ใน scenarios.json (มี multi-turn 1 อัน), rubric 8 ด้าน, ผลรันจริง 3 สถานการณ์ (n=1, โมเดลเดียว) ได้ 14/16, 15/16, 16/16 เทียบ baseline 12, 7, 15

**ช่องว่างที่รู้แล้ว**

- ตัวเลขไม่ตรงกัน: RESULTS.md เขียน 13 สถานการณ์ แต่ scenarios.json มี 14
- SKILL.md มีประโยคอนุญาตให้รวมคำถามที่เกี่ยวข้องกัน ขัดกับ discovery.md ที่ให้ถามทีละข้อ
- template คำตอบสั้นใน output.md ไม่มีช่อง “ทบทวนเมื่อไร”
- ตัวเลขประมาณการที่ไม่ได้วัด (เช่น RAM) ยังไม่มีกฎกำกับ
- นิยามของ bias check ใน SKILL.md กับ evaluation.md ถามคนละคำถาม
- ยังไม่มี fixture ที่ให้ skill อ่าน repo จริง (ความสามารถที่ README โฆษณาไว้ยังไม่ถูกทดสอบ)
- multi-turn ใช้สคริปต์คำตอบตายตัว
- ขั้นสกัด release notes ใน PUBLISHING.md ยังเสี่ยงเรื่อง encoding เมื่อรันด้วย PowerShell (เคยเจอจริงตอน release)

> **อัปเดตหลัง v0.1.1:** ข้อ 1-5 และ 8 ของรายการด้านบนถูกปิดแล้วด้วย Phase 0 ข้อ 0.1-0.6 (ด้านล่าง) ที่เหลือ — fixture อ่าน repo จริง และ multi-turn สคริปต์ตายตัว — ย้ายไปภารกิจ 1.1-1.3 ตามจริง

**ยังไม่ได้ตรวจ (ต้องเช็กกับเอกสารทางการก่อนลงมือ)**

- รูปแบบ marketplace/plugin ของ Claude Code และกฎชื่อที่สงวนไว้ — ✅ ตรวจเอกสารแล้ว ณ 2 พ.ย. 2026 · เลื่อนลงมือไป Phase 2 (ข้อ 2.2)
- วิธีที่ /tech-me ทำงานใน Claude Code — ✅ ตรวจเอกสารแล้ว: skill ที่ติดตั้งแบบสแตนด์อโลนเรียกเป็นคำสั่ง `/tech-me` ได้ (README เขียนตามนี้แล้วในข้อ 0.7) · พฤติกรรมของ disable-model-invocation **ยังไม่ได้ตรวจ**
- รูปแบบ zip ที่ claude.ai รับสำหรับอัปโหลด skill — ✅ ตรวจเอกสารแล้ว · เลื่อนลงมือไป Phase 2 (ข้อ 2.1)
- เงื่อนไขการแสดงผลของ skills.sh — **ยังไม่ได้ตรวจ**

## 3. Phase 0 — v0.1.1: เก็บงานหลัง release

**เป้าหมาย**: ปิดช่องโหว่ที่เห็นแล้วด้วยการแก้เล็ก ๆ ทีละจุด · **ขนาด**: S-M (1-2 PR)

**งาน**

- [x] 0.1 PUBLISHING.md: สกัด release notes ด้วย Python ที่ระบุ encoding เป็น utf-8 ทั้งอ่านและเขียน และเพิ่มขั้นตรวจว่าไฟล์ขึ้นต้นด้วย ### โดยไม่มี BOM หรือ NUL
- [x] 0.2 ทำตัวเลขสถานการณ์ให้ตรงกัน (แก้ RESULTS.md) และถ้าทำได้ให้ validator เช็กจำนวนให้ตรงกันอัตโนมัติ
- [x] 0.3 ช่องโหว่ถามสองข้อ: ตัดประโยคใน SKILL.md หรือจำกัดว่าข้อที่สองต้องเป็นตัวเลือกให้กดเลือก ให้สอดคล้องกับ discovery.md
- [x] 0.4 output.md: เพิ่มบรรทัด “ทบทวนเมื่อ…” ใน template คำตอบสั้น และบังคับให้ทุกค่า default ชั่วคราวมีเงื่อนไขทบทวนติดมา
- [x] 0.5 เพิ่มกฎ: ตัวเลขประมาณการที่ไม่ได้วัดต้องติดป้าย “ประมาณการ ไม่ได้วัด” หรือเปลี่ยนเป็นคำบรรยายเชิงเปรียบเทียบ
- [x] 0.6 เลือก bias check เหลือแบบเดียว หรืออธิบายชัดว่าแต่ละแบบใช้ตอนไหน
- [x] 0.7 README: ตัวอย่างก่อน-หลังจากเคส unknown-scale-defaults, วิธีเรียกด้วย /tech-me (ยืนยันกับเอกสาร Claude Code ก่อนเขียน), ตั้ง Topics และ description ของ repo
- [x] 0.8 CHANGELOG: เพิ่มหัวข้อ \[0.1.1\] และระบุว่าผล evals เดิมวัดจาก SKILL.md ก่อนแก้ข้อ 0.3-0.6

**เกณฑ์ผ่าน**: validator, tests และ CI ผ่าน · ไฟล์ notes ที่สกัดบน Windows ทั้ง PowerShell และ Git Bash เป็น UTF-8 เหมือนกัน · รันสถานการณ์ที่เกี่ยวข้องซ้ำอย่างน้อย 1 รอบหลังแก้ SKILL.md แล้วไม่แย่ลง
**ผล (2 พ.ย. 2026)**: ✅ ผ่านทั้งหมด — แบ่งเป็น 2 PR: #7 (ข้อ 0.1-0.2: validator + 36 tests + CI พร้อมสคริปต์ notes ที่เขียนไฟล์เอง จึงได้ผลของไบต์เดียวกันโดยไม่ขึ้นกับ shell) และ #8 (ข้อ 0.3-0.8) · spot-check ซ้ำ 2 สถานการณ์หลังแก้ SKILL.md ไม่พบความถอย (`evals/runs/run_20261102_spotcheck.json`; n=1, non-blind, คนละโมเดลกับ report 2026-10-29 จึงไม่ใช้เทียบกัน)

**ความเสี่ยง**: แก้ SKILL.md แล้วพฤติกรรมเปลี่ยนโดยไม่ได้วัด → แก้ทีละจุด ทำเป็น commit แยก และบันทึกใน CHANGELOG

## 3.5 Phase 0.5 — v0.2.0: ใช้งานเป็น skill จริง (เสร็จสิ้น 18 พ.ย. 2026)

**เหตุผลที่ปรับลำดับ**: เจ้าของโปรเจกต์ตัดสินใจเน้นให้ใช้งานได้จริงก่อนทำชุด eval ใหญ่ และมีผู้ทดลองใช้ภายนอก 1 คนให้ feedback แล้ว จึงดึงงานโหมด คำสั่ง และ marketplace ขึ้นมาก่อนชุด eval ใหญ่ · นี่เป็นการเบี่ยงจากหลัก "หลักฐานก่อนการโปรโมต" โดยรู้ตัว จึงยังไม่ทำข้อโปรโมตในวงกว้างจนกว่า Phase 2 (หลักฐาน) จะผ่าน

**ผล (PR #9, #10, #11, #12, #13 → `main` `48c7a5d`, tag `v0.2.0`)**: ✅

- [x] โหมด `/tech-me [quick|review|migrate|adr|help]` เขียนเป็นภาษาธรรมชาติใน SKILL.md (รองรับทั้ง inline และ `ARGUMENTS:` ของ `teveus` / Claude Code) และการเรียกแบบ hybrid
- [x] Anti-rationalization guard ใน SKILL.md และลำดับอ่าน `review` (manifests → README/ARCHITECTURE/docs/adr → config → เฉพาะ interface ที่จำเป็น)
- [x] `commands/tech-me-{quick,review,migrate,adr}.md` พร้อม `argument-hint` และกฎเหล็กในตัว สำหรับเมนู `/` ของ Claude Code plugin และ `teveus`
- [x] `.claude-plugin/plugin.json` (`0.2.0`) + `marketplace.json` ชี้ `source: "./"`
- [x] `validate_repo.py` ตรวจ plugin parity (`version`/`name`/marketplace), `commands/`, และ `mode` fixture (19 scenarios, 43 unit tests ผ่านครบ)
- [x] README (workflow diagram, ตารางโหมด, plugin/teveus install, verify step), CHANGELOG `v0.2.0`, และ GitHub Release `v0.2.0` (`dist/tech-me-0.2.0.zip`)

*(งานที่ยกยอดไป v0.3.0: `claude plugin validate .`, `--skill-zip`, และ dogfood จริง)*

## 4. Phase 1 — v0.3.0: ความคมของ Skill + ช่องทางใช้จริง

**เป้าหมาย**: เติม Playbook การตัดสินใจเฉพาะทางให้คำแนะนำคมขึ้น และทดสอบใช้งานจริงทุกช่องทาง · **ขนาด**: M

**งาน**

- [x] 1.1 Domain Playbooks ใน `skills/tech-me/references/` (โหลดเมื่อจำเป็น ไม่ใส่ราคา/เลขเวอร์ชันที่เน่าเร็ว): Database/Storage (`playbook-database.md`), Hosting/Compute (`playbook-hosting.md`), และ Boundary/Migration (`playbook-migration.md`)
- [x] 1.2 เพิ่ม `--skill-zip` ใน `pack_release.py` ให้ได้ `tech-me-skill-<ver>.zip` ที่รากเป็นโฟลเดอร์ `tech-me/` สำหรับอัปโหลดบน claude.ai พร้อม unit tests (3 tests) และคู่มือใน `PUBLISHING.md`
- [ ] 1.3 รัน `claude plugin validate .` และทดสอบติดตั้งจริงผ่าน `/plugin marketplace add L4ncelotz/tech-me-skills` ยืนยันชื่อคำสั่ง (`/tech-me:tech-me` และ `/tech-me:tech-me-*`) รวมถึงทดสอบอัปโหลด `tech-me-skill-0.3.0.zip` บน `claude.ai`
- [x] 1.4 Dogfood: ทดสอบโหมด `review`, `migrate`, `quick`, `help` ผ่าน read-only subagent บน fixture repos จริง (`tight-monolith`, `small-healthy-app`) และแก้จุดฝืด 3 จุดแล้ว *(ยังเหลือ interactive dogfood บน `teveus` และ Claude Code)*

**เกณฑ์ผ่าน**: Playbook ไม่มีตัวเลขที่ตรวจสอบไม่ได้ · plugin และ zip ติดตั้งใช้งานได้จริง · README ตรงกับชื่อคำสั่งที่ทดสอบจริง

## 5. Phase 2 — v0.4.0: หลักฐานและ Eval ข้ามเอเจนต์

**เป้าหมาย**: พิสูจน์ว่า skill ชนะ baseline จริง ทดสอบการอ่าน repo จริง และวัดผลข้ามเอเจนต์ · **ขนาด**: L · เป็นหัวใจของความน่าเชื่อถือ

**งาน**

- [x] 2.1 สร้าง fixture repo จริงใน `evals/fixtures/` 3 แบบ: `tight-monolith`, `multi-service-compose`, `small-healthy-app` พร้อมไฟล์กับดัก `env.trap.fixture` (ปลอดภัยต่อ `.gitignore` และ `pack_release.py`) และเพิ่มการตรวจใน `validate_repo.py`
- [x] 2.2 กำหนดพฤติกรรมที่คาดหวังของการอ่าน repo ใน `evals/scenarios.json` (`fixture_dir`, รวม 21 scenarios) และส่งออกใน `scripts/run_evals.py`
- [x] 2.3 ตัวจำลองผู้ใช้สำหรับ multi-turn: เพิ่ม schema `user_simulator` (`persona`, `known_facts`, `unknowns`, `stop_rule`) ใน `scenarios.json`, validate ใน `validate_repo.py` และสร้าง `simulator_system_prompt` ใน `scripts/run_evals.py`
- [x] 2.4 Baseline 3 แบบ: เพิ่ม `evals/short_prompt_baseline.md` และส่งออกครบ 3 เงื่อนไข (`baseline`, `short-prompt`, `tech-me`) พร้อมโหมด `--blind` ใน `scripts/run_evals.py` (ครอบคลุมทั้ง 21 scenarios)
- [ ] 2.5 โปรโตคอลรัน: ทุก fixture `n >= 3` ที่ `temperature > 0` (และรอบอ้างอิงที่ 0) ข้ามอย่างน้อย 2 เอเจนต์นอกจากตัวที่ใช้อยู่ (เช่น `teveus`, Claude Code, Cursor) บันทึกตาราง เอเจนต์ × fixture
- [ ] 2.6 การให้คะแนน: ซ่อนป้ายเงื่อนไข ผู้ให้คะแนนต่างจากผู้สร้างคำตอบ รายงาน critical failures แยกจากค่าเฉลี่ย และรายงานความแปรปรวนระหว่างรอบ
- [ ] 2.7 เขียน `evals/RESULTS.md` ใหม่แบบรายสถานการณ์ ไม่สรุปเกินหลักฐาน และอัปเดต `compatibility` ใน frontmatter ให้ตรงผลจริง
- [ ] 2.8 ตัดสินใจจากผล: ถ้าพรอมต์สั้นสู้ได้ ให้ย่อ `SKILL.md` · วัดงบ token ของ `SKILL.md` และ `references/`

**เกณฑ์ผ่าน**: ผลเทียบ baseline ทั้งสองแบบทำซ้ำได้ในอย่างน้อย 2 เอเจนต์ · ไม่มี critical failure ในกรณีอ่าน repo · `RESULTS.md` ระบุข้อจำกัดครบ

**ความเสี่ยง**: ต้นทุน token และเวลา · ผู้ให้คะแนนเอนเอียง · fixture repo กลายเป็นภาระดูแล → ทำ repo ให้เล็ก และให้ validator เช็กโครงสร้าง

## 6. Phase 3 — v0.5.0: การแพร่กระจายและโปรโมต

**เป้าหมาย**: ขยายการค้นพบและการรับ feedback จากผู้ใช้ภายนอก หลังมีหลักฐานจาก Phase 2 · **ขนาด**: S-M · **เงื่อนไขเริ่ม**: Phase 2 ผ่านเกณฑ์

**งาน**

- [ ] 3.1 การค้นพบ: ส่ง PR เข้า awesome-lists ของ agent skills, ตรวจเงื่อนไข `skills.sh`, โพสต์ในชุมชนพร้อมตัวอย่างและผล evals ตามจริง (ระบุ `n` และข้อจำกัด)
- [ ] 3.2 ช่องทาง feedback: เพิ่มวิธีรายงานเคสที่ skill ตอบผิดโดยแนบบทสนทนา
- [ ] 3.3 ภาษา: เพิ่ม fixture ภาษาไทยหลายแบบ, อังกฤษ และอย่างน้อยอีก 1 ภาษา ตรวจว่าตอบตามภาษาผู้ใช้และอธิบายศัพท์ได้เหมาะสม

**เกณฑ์ผ่าน**: มีผู้ใช้ภายนอกลองจริง และ feedback ถูกนำมาปรับปรุงแล้ว · ไม่มี critical failure จากภาษาที่ไม่ใช่อังกฤษ

**ความเสี่ยง**: โปรโมตก่อนหลักฐานพร้อม → เลื่อนข้อ 3.1 ถ้า Phase 2 ไม่ผ่าน

## 7. Phase 4 — เกณฑ์ก่อนเรียกว่า v1.0

ไม่กำหนดวัน ใช้เกณฑ์เท่านั้น

- [ ] ทุก fixture รันที่ n≥3 กับอย่างน้อย 2 เอเจนต์ และไม่มี critical failure
- [ ] ชนะ baseline ทั้งสองแบบในผลที่ทำซ้ำได้
- [ ] มีผู้ใช้ภายนอกลองจริง และ feedback ที่ได้ถูกนำมาแก้แล้ว
- [ ] เอกสารติดตั้งและการใช้งานตรงกับของจริงทุกช่องทาง
- [ ] ถึงตอนนั้นจึงเลิกติดป้าย pre-release

## 8. การตัดสินใจที่ค้างอยู่

| เรื่อง | ตัวเลือก | การตัดสินใจ ณ 18 พ.ย. 2026 |
| --- | --- | --- |
| source ของ marketplace | ทั้ง repo หรือ skills/tech-me | **ตัดสินชั่วคราว (17 พ.ย.): ทั้ง repo (`./`)** · ข้อเสีย: ติดตั้งแล้วได้ evals/tests/scripts ไปด้วย · ทบทวนเมื่อทดสอบติดตั้งจริง (ข้อ 1.3) |
| การเรียกใช้ | อัตโนมัติ + เรียกเอง หรือเรียกเองอย่างเดียว | **ตัดสินแล้ว (17 พ.ย.): hybrid** (อัตโนมัติ + เรียกเอง) ไม่ใช้ disable-model-invocation |
| การแก้ encoding | Python utf-8 หรือบังคับ Git Bash | **ตัดสินแล้ว: ใช้สคริปต์** `scripts/make_release_notes.py` (เขียนไฟล์เอง fail-closed) · workflow เดียวใช้ได้ทุก shell · ปิดใน v0.1.1 |
| โหมด quick/review/adr | ทำหรือรอ | **ตัดสินแล้ว (17–18 พ.ย.): ทำ** · ได้ feedback จากผู้ทดลองจริง · เพิ่ม `migrate` และ `help` ด้วย (v0.2.0) |
| shortcut commands | 1 skill หรือเพิ่ม `commands/` | **ตัดสินแล้ว (18 พ.ย.): เพิ่ม `commands/tech-me-*.md`** เป็น wrapper ชี้ไป `tech-me` โดยไม่คัดลอกกฎซ้ำ สำหรับเมนู `/` ของ plugin และ `teveus` |
| รูปแบบ zip สำหรับ claude.ai | โฟลเดอร์ tech-me/ ที่ราก | **ตัดสินแล้ว (19 พ.ย.): ใช้ `--skill-zip`** ใน `pack_release.py` สร้าง `tech-me-skill-<ver>.zip` ที่มีรากเป็น `tech-me/` (`SKILL.md`, `references/`, `assets/`, ไม่มี `README.md`) |

## 9. ความเสี่ยงโดยรวม

- **อ้างเกินหลักฐาน**: ทุกตัวเลขในผลทดสอบต้องระบุ n โมเดล และวันที่
- **ความซับซ้อนเกินจำเป็น**: ถ้าพรอมต์สั้นสู้ skill ได้ ให้ย่อ skill
- **ผูกกับเอเจนต์เดียว**: เก็บ SKILL.md ให้พกพา ส่วนเฉพาะเอเจนต์แยกไฟล์
- **ภาระดูแลคนเดียว**: จำกัดขอบเขตแต่ละเฟส และไม่เปิดฟีเจอร์ใหม่ก่อนปิดเฟสเดิม

## 10. นอกขอบเขต

- การแก้ไขโค้ด ติดตั้งแพ็กเกจ หรือ deploy แทนผู้ใช้ (skill เป็น advisory และอ่านอย่างเดียว)
- การรับประกันว่า stack ที่แนะนำเป็นตัวเลือกที่ดีที่สุดในเชิงสัมบูรณ์
- การให้ราคา โควตา หรือตัวเลข benchmark ปัจจุบันโดยไม่ตรวจสอบกับแหล่งหลัก

## 11. การดูแลเอกสารนี้

- ปรับสถานะของแต่ละข้อ (เช็กกล่อง) เมื่อ PR ที่เกี่ยวข้อง merge แล้ว
- เมื่อจบแต่ละเฟส ให้บันทึกสิ่งที่เรียนรู้และปรับเฟสถัดไปตามหลักฐานที่ได้
- ข้อที่ระบุว่ายังไม่ได้ตรวจ ต้องยืนยันกับเอกสารทางการก่อนลงมือ และอัปเดตเอกสารนี้หลังยืนยัน

## 12. สิ่งที่เรียนรู้จาก Phase 0

1. **การเขียนไฟล์ไม่ควรให้ shell เป็นคนกำหนด encoding**: PowerShell redirect เขียน UTF-16 เมื่อไม่ระวัง สคริปต์ที่เขียนไฟล์เองและ fail-closed เมื่อไฟล์ไม่ขึ้นต้นด้วย `###` หรือมี BOM/NUL ปิดปัญหาที่ตรวจซ้ำได้โดยไม่ต้องจำกันจาก workflow ของแต่ละคน
2. **claim ในเอกสารที่ validator เช็กได้ ควรถูกเช็ก**: ตัวเลข scenario ที่พิมพ์ผิดใน RESULTS.md อยู่ได้เพราะไม่มีใครอ่านเทียบอัตโนมัติ เมื่อ `"N of M"` กลายเป็น regex ของ validator อาการแบบนี้จะขึ้น CI สีแดงแทนการถูกพบตอนออก release
3. **แก้พฤติกรรมทีละจุด พร้อม spot-check สั้น ๆ ก่อน tag ทำให้กล้าแก้โดยไม่ต้องรอ suite ใหญ่**: แต่ต้องติดป้ายข้อจำกัดครบ (n=1, non-blind, คนละโมเดล ไม่เทียบกัน) ตั้งแต่ใน CHANGELOG ไม่ใช่รอจนคนถาม
4. **เช็กเอกสารทางการก่อนเขียน README**: การยืนยัน `/tech-me` ใน Claude Code ก่อนเขียน ทำให้คู่มือติดตั้งพูดเฉพาะสิ่งที่เป็นจริง และไม่ overclaim การ activate อัตโนมัติบนเอเจนต์อื่น
5. **ไฟล์ที่ไม่ถูก commit คือตัวดีดงาน release**: `Tech-Me Roadmap.md` ค้างเป็น untracked จริง ๆ จึงเปลี่ยนชื่อเป็น `ROADMAP.md` และขึ้น tree ใน v0.1.1 — เอกสารกลางของโปรเจกต์ที่ release ระบุถึงควรอยู่ใน tree เสมอ
