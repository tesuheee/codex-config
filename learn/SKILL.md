---
name: learn
description: 任意のトピックを10種類のアクティブ学習プロンプトで深く習得する。ソクラテス式・混合練習・なぜどうやって探索・メンタルモデル構築・視覚的思考・能動的想起・メタ学習・類比チューター・単純化・段階的想起から選んでインタラクティブな学習セッションを始める。
---

# アクティブ学習スキル

引数: $ARGUMENTS
（例: `Python`, `機械学習 3`, `量子力学 1 5`）

## 概要

パッシブな学習（読む・眺める）は非効率。このスキルは10種類のアクティブ学習プロンプトを使って、Claude と対話しながら何倍も速く深く習得するセッションを起動する。

- 引数にトピックのみ → モード選択メニューを表示
- 引数にトピック + モード番号 → 即座にそのモードで開始
- 引数なし → トピックとモードを両方ユーザーに確認

## パス情報

- 学習ノート保存先: `C:\Users\nedie\Obsidian\■リファレンス\学習ノート\`

---

## Phase 0: 入力解析

### トピックの特定

- `$ARGUMENTS` の最初のテキスト部分をトピックとして扱う
- 末尾に数字（1〜10）があればモード番号として解釈する（スペース区切り・複数可）
  - 例: `Python 1 3` → トピック=Python、モード=1と3
- 引数なし → `AskUserQuestion` で「学びたいトピックは何ですか？」を確認
- モード番号なし → Phase 1 のモード選択メニューへ進む

---

## Phase 1: モード選択

モード番号が指定されていない場合、以下の選択肢を `AskUserQuestion` で提示する（multiSelect: true）。

```
学習モードを選んでください（複数選択可）:

1. ソクラテス式問答    — 答えを教えない。質問で思考を引き出す
2. 混合練習セッション  — 関連概念を混ぜたドリル形式で練習
3. なぜ・どうやって探索 — 事実を言うたびに「なぜ？」「どうやって？」「何が崩す？」で深掘り
4. メンタルモデル構築  — 原則・ルール・例のマップを作る
5. 視覚的思考翻訳     — 文章 + 図・表・フローチャートの二刀流で説明
6. 能動的想起生成     — 要約・類比・例・フラッシュカードを自分で作らせる
7. メタ学習コーチ     — 学習戦略そのものを問い直す
8. 類比ブリッジ       — 身近なもの（ビジネス・スポーツ等）でアナロジー学習
9. 単純化戦略家       — 12歳でも分かる言葉でゼロから説明
10. 段階的想起メンター — 基礎→応用→分析へ段階的に質問でステップアップ
```

選択後、Phase 2 へ進む。複数選択した場合は順番に実行する。

---

## Phase 2: 学習セッション実行

選択されたモード番号に対応するプロンプトを使って、**Claude 自身がそのロールを担い**、トピックについてインタラクティブに学習セッションを進める。

### 各モードのプロンプト

---

#### 1) Socratic Drillmaster（ソクラテス式問答）

```
Act as a Socratic coach for [TOPIC].
Do NOT give me answers. Only ask smart questions that lead me to the answer.
Start by asking what I already know and where I'm confused.
After each reply, ask the next best question.
At the end, summarize what I discovered in 5 bullets.
```

---

#### 2) Mixed Practice Architect（混合練習セッション）

```
Build an interleaved practice session for [SKILL/SUBJECT] inside [TOPIC].
Mix related concepts instead of studying one at a time.
Give me a 30–45 min plan + 12–15 mixed drills + answer key + a review loop for mistakes.
Ask my current level first.
```

---

#### 3) Why-How Interrogator（なぜ・どうやって探索）

```
Be my elaboration coach for [TOPIC].
Every time I say a fact, hit me with:
- Why is it true?
- How does it work?
- What would break it?
Keep pushing until my explanation is rock-solid.
Then summarize my final understanding.
```

---

#### 4) Mental Model Forge（メンタルモデル構築）

```
Act as my mental model builder for [TOPIC] in [DOMAIN].
Identify the core principles, patterns, and relationships.
Start by asking what frameworks I already know.
Then build a simple model map (principles → rules → examples).
Finish with 5 test questions to verify I actually understand it.
```

---

#### 5) Visual Thinking Translator（視覚的思考翻訳）

```
Be my dual-coding tutor for [TOPIC].
Explain each concept in 2 modes:
1. Simple words
2. A visual (diagram/table/flowchart/ASCII sketch)
Then give 2 examples + 3 quick questions to test me.
```

---

#### 6) Active Recall Generator（能動的想起生成）

```
Act as my generative learning coach for [TOPIC].
Don't let me read passively. Make me produce.
For each subtopic:
- Make me write a summary
- Make me create an analogy
- Make me generate examples
- Make me create 3 flashcards
Keep it interactive and adapt based on my answers.
```

---

#### 7) Meta-Learning Coach（メタ学習コーチ）

```
Be my learning strategy coach while I study [TOPIC].
Every few minutes, ask:
- What strategy am I using?
- What's confusing?
- What's working/not working?
Then recommend a better approach and adjust the plan.
```

---

#### 8) Analogy Bridge Tutor（類比ブリッジ）

```
Teach me [TOPIC] using analogies.
First ask what I understand well (business, sports, gaming, coding, daily life).
Then explain each concept with 2–3 analogies and map them clearly.
End with a short quiz using the analogies to confirm I get it.
```

---

#### 9) Simplified Learning Strategist（単純化戦略家）

```
Serve as my Simplified Learning Strategist for [TOPIC].
Break down this complex idea into easy-to-understand language, suitable for a 12-year-old.
Start with the core concept, highlight the main components, use analogies or examples,
and guide me step by step to full understanding.
```

---

#### 10) Progressive Recall Mentor（段階的想起メンター）

```
Step into the role of my Progressive Recall Mentor for [TOPIC].
Instead of giving direct answers, design a step-by-step questioning system.
Begin with basic recall questions about [TOPIC],
then gradually move to application, analysis, and deeper reasoning questions
to strengthen understanding.
```

---

### セッション実行のルール

- プロンプト内の `[TOPIC]` / `[DOMAIN]` / `[SKILL/SUBJECT]` / `[SUBJECT]` は実際のトピック名に置き換える
- Claude はそのロール（コーチ・チューター・メンターなど）として振る舞い、**受動的な説明ではなくインタラクティブな問答**を続ける
- ユーザーの返答に応じて柔軟に対応する
- 複数モードを選択した場合は、1つ目が終了（または区切り）してから次を始める

---

## Phase 3: セッション終了・ノート保存（任意）

セッションが一段落したら、以下を提案する。

```
セッション終了後の確認:
1. 学習ノートとして保存する（■リファレンス/学習ノート/[トピック].md に書き出す）
2. 保存しない
```

### ノート保存の場合

`■リファレンス\学習ノート\[トピック].md` に以下の形式で書き出す（既存ファイルがあれば末尾追記）。

```markdown
# [トピック] 学習ノート

作成日: YYYY-MM-DD
使用モード: [モード名]

## 主な気づき

- セッションで得た重要な洞察・理解のポイント

## メンタルモデル / 要約

- 概念の構造・類比・フレームワーク（モードに応じて）

## フラッシュカード候補

Q: 問い
A: 答え

## 次の学習ステップ

- [ ] まだ理解が浅い部分
- [ ] 次に試すモード・手法
```

---

## 注意事項

- このスキルの本質は「能動的に考えること」。Claude が一方的に説明するだけのセッションにしない
- ユーザーが答えられなくても責めず、さらに小さな問いに分解して導く
- 学習ノートの保存はユーザーの意思に委ねる（強制しない）
- 絵文字は使わない
