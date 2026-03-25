# 📝 Text Challenges Assignment
### Assignment Name: Text Challenges
**Description:** Collect 20 messy sentences and identify slang, emojis, typos; explain preprocessing needed.

---

## Introduction

Real-world text data is rarely clean. Social media posts, customer reviews, chat messages, and user-generated content are filled with **slang**, **emojis**, **typos**, **abbreviations**, and **grammatical errors**. Before feeding such text into any NLP (Natural Language Processing) model, careful **preprocessing** is essential to improve model accuracy and performance.

This assignment collects **20 messy sentences**, annotates them with the challenges they contain, and explains the preprocessing steps required.

---

## Legend / Annotation Key

| Symbol | Meaning |
|--------|---------|
| 🔵 **[SLANG]** | Informal/internet slang word or phrase |
| 🟠 **[EMOJI]** | Emoji present in text |
| 🔴 **[TYPO]** | Spelling mistake or typo |
| 🟣 **[ABBR]** | Abbreviation or acronym |
| 🟡 **[GRAMMAR]** | Grammatical error |
| 🟢 **[MIXED]** | Mixed-language text (code-switching) |

---

## 20 Messy Sentences with Annotations

---

### Sentence 1
> **"omg dis movie waz sooo gud i cant evn 😍😍"**

| Type | Identified Issues |
|------|-----------------|
| 🔵 SLANG | `omg` (oh my god) |
| 🔴 TYPO | `dis` → this, `waz` → was, `gud` → good, `evn` → even |
| 🟠 EMOJI | 😍😍 |
| 🟡 GRAMMAR | Missing apostrophe in `cant` → can't |

**Preprocessing Needed:**
- Expand slang: `omg` → "oh my god"
- Correct typos using spell-checker (e.g., TextBlob, pyspellchecker)
- Remove or replace emojis (convert to text: 😍 → "heart eyes" or remove)
- Normalize repeated characters: `sooo` → "so"
- Lowercase normalization

---

### Sentence 2
> **"i luv u sm babe 💕💕 ur the best frnd evr!!"**

| Type | Identified Issues |
|------|-----------------|
| 🔵 SLANG | `luv`, `sm` (so much), `frnd` (friend) |
| 🔴 TYPO | `ur` → your, `evr` → ever |
| 🟠 EMOJI | 💕💕 |
| 🟡 GRAMMAR | Missing punctuation, repeated `!!` |

**Preprocessing Needed:**
- Slang normalization: `luv` → love, `sm` → so much
- Spell correction: `ur` → your, `evr` → ever
- Emoji removal/conversion
- Punctuation normalization (remove repeated `!!`)

---

### Sentence 3
> **"lol this guy is such a noob he dnt even kno how 2 play 😂😂😂"**

| Type | Identified Issues |
|------|-----------------|
| 🔵 SLANG | `lol`, `noob` |
| 🔴 TYPO | `dnt` → don't, `kno` → know |
| 🟠 EMOJI | 😂😂😂 |
| 🟣 ABBR | `2` used as "to" |

**Preprocessing Needed:**
- Slang expansion: `lol` → laughing out loud, `noob` → beginner
- Typo correction: `dnt` → don't, `kno` → know
- Numeral-to-word: `2` → to
- Emoji handling

---

### Sentence 4
> **"I hv 2 submit da assignmnt tmrw nd i hvnt started 😭😭"**

| Type | Identified Issues |
|------|-----------------|
| 🔴 TYPO | `hv` → have, `da` → the, `assignmnt` → assignment, `hvnt` → haven't |
| 🟠 EMOJI | 😭😭 |
| 🟣 ABBR | `tmrw` → tomorrow, `nd` → and |

**Preprocessing Needed:**
- Abbreviation expansion: `tmrw` → tomorrow, `nd` → and
- Spell correction for all truncated words
- Emoji removal

---

### Sentence 5
> **"bruh the food ws cold an they still charged full price smh 😤"**

| Type | Identified Issues |
|------|-----------------|
| 🔵 SLANG | `bruh`, `smh` (shaking my head) |
| 🔴 TYPO | `ws` → was, `an` → and |
| 🟠 EMOJI | 😤 |

**Preprocessing Needed:**
- Slang normalization: `bruh` → brother/expression of disbelief, `smh` → shaking my head
- Spell correction
- Emoji removal or sentiment tagging

---

### Sentence 6
> **"yasss queen u slayyyyed that look 🔥🔥 periodt!!"**

| Type | Identified Issues |
|------|-----------------|
| 🔵 SLANG | `yasss`, `queen`, `slayyyyed`, `periodt` |
| 🔴 TYPO | `slayyyyed` → slayed (character elongation) |
| 🟠 EMOJI | 🔥🔥 |

**Preprocessing Needed:**
- Character repetition normalization: `yasss` → yes, `slayyyyed` → slayed
- Slang dictionary lookup
- Emoji conversion

---

### Sentence 7
> **"cant blv they r selling dis 4 $500 😱 its a total ripoff tbh"**

| Type | Identified Issues |
|------|-----------------|
| 🔵 SLANG | `tbh` (to be honest), `ripoff` |
| 🔴 TYPO | `blv` → believe, `dis` → this |
| 🟠 EMOJI | 😱 |
| 🟣 ABBR | `r` → are, `4` → for, `tbh` |
| 🟡 GRAMMAR | Missing apostrophe in `cant` |

**Preprocessing Needed:**
- Abbreviation expansion: `r` → are, `4` → for, `tbh` → to be honest
- Typo correction
- Emoji handling

---

### Sentence 8
> **"jst wke up nd alredy hv a headache rip 😪 nd its only mondayyyy"**

| Type | Identified Issues |
|------|-----------------|
| 🔴 TYPO | `jst` → just, `wke` → woke, `alredy` → already, `hv` → have |
| 🟠 EMOJI | 😪 |
| 🟣 ABBR | `nd` → and |
| 🔵 SLANG | `rip` (rest in peace / expression) |
| 🔴 TYPO | `mondayyyy` → Monday (elongation) |

**Preprocessing Needed:**
- Spell correction for all truncated words
- Character elongation normalization: `mondayyyy` → Monday
- Slang mapping: `rip` → context-dependent
- Emoji removal

---

### Sentence 9
> **"ngl the vibes were off 2day fr fr everyone was being sus 👀"**

| Type | Identified Issues |
|------|-----------------|
| 🔵 SLANG | `ngl` (not gonna lie), `vibes`, `fr fr` (for real for real), `sus` (suspicious) |
| 🟠 EMOJI | 👀 |
| 🟣 ABBR | `2day` → today |

**Preprocessing Needed:**
- Slang expansion: `ngl` → not going to lie, `fr` → for real, `sus` → suspicious
- Abbreviation normalization: `2day` → today
- Internet slang dictionary lookup
- Emoji removal

---

### Sentence 10
> **"Teh quik brwn fox jmped ovr teh lzy dog"**

| Type | Identified Issues |
|------|-----------------|
| 🔴 TYPO | `Teh` → The, `quik` → quick, `brwn` → brown, `jmped` → jumped, `ovr` → over, `lzy` → lazy |

**Preprocessing Needed:**
- Extensive spell checking (this is a keyboard-speed typo pattern)
- Lowercasing
- Use context-aware spell correction (e.g., SymSpell, TextBlob)

---

### Sentence 11
> **"wtf is dis weather?? its lyk 40 degrees outside rn 🥵 no cap"**

| Type | Identified Issues |
|------|-----------------|
| 🔵 SLANG | `wtf`, `lyk`, `rn` (right now), `no cap` (no lie) |
| 🔴 TYPO | `dis` → this, `lyk` → like |
| 🟠 EMOJI | 🥵 |

**Preprocessing Needed:**
- Profanity/slang handling: `wtf` → what the, or flag and remove
- Slang normalization: `rn` → right now, `no cap` → no lie/truly
- Typo correction
- Emoji removal or sentiment label

---

### Sentence 12
> **"just binge watched da entir season in 1 nite n hv 0 regrets lmaooo 😴"**

| Type | Identified Issues |
|------|-----------------|
| 🔵 SLANG | `binge watched`, `lmaooo` |
| 🔴 TYPO | `da` → the, `entir` → entire, `nite` → night |
| 🟠 EMOJI | 😴 |
| 🟣 ABBR | `n` → and, `hv` → have |
| 🔴 TYPO | `lmaooo` → character elongation of `lmao` |

**Preprocessing Needed:**
- Spell correction: `entir` → entire, `nite` → night
- Slang expansion: `lmao` → laughing my (ass) off
- Character normalization
- Emoji handling

---

### Sentence 13
> **"This prouduct is amazng!! best purches i evr made 10/10 wud recomend 🌟"**

| Type | Identified Issues |
|------|-----------------|
| 🔴 TYPO | `prouduct` → product, `amazng` → amazing, `purches` → purchase, `evr` → ever, `wud` → would, `recomend` → recommend |
| 🟠 EMOJI | 🌟 |

**Preprocessing Needed:**
- Spell correction (multiple errors per word — use edit-distance based correction)
- Emoji removal or conversion to sentiment label
- Normalize rating patterns: `10/10`

---

### Sentence 14
> **"arey yaar kya scene hai 😂 itna traffic and still got late to da office"**

| Type | Identified Issues |
|------|-----------------|
| 🟢 MIXED | `arey yaar kya scene hai` (Hindi/Hinglish) |
| 🔵 SLANG | `scene` used informally |
| 🔴 TYPO | `da` → the |
| 🟠 EMOJI | 😂 |

**Preprocessing Needed:**
- Language detection (identify Hinglish / code-mixed text)
- Transliteration or translation: `arey yaar kya scene hai` → "Oh man, what's happening"
- Handle code-switching with multilingual NLP models (e.g., mBERT)
- Emoji removal

---

### Sentence 15
> **"my wifi is ded and i hv a zoom call in 10 mins k bye panic mode on 😤🙏"**

| Type | Identified Issues |
|------|-----------------|
| 🔵 SLANG | `ded` (dead/done), `panic mode`, `k` |
| 🔴 TYPO | `hv` → have |
| 🟠 EMOJI | 😤🙏 |
| 🟣 ABBR | `mins` → minutes |

**Preprocessing Needed:**
- Slang mapping: `ded` → very tired / done
- Abbreviation expansion: `mins` → minutes
- Spell correction
- Multi-emoji handling

---

### Sentence 16
> **"i swer 2 god if they cancel anotha season of dis show imma cry 😤💔"**

| Type | Identified Issues |
|------|-----------------|
| 🔵 SLANG | `imma` (I am going to) |
| 🔴 TYPO | `swer` → swear, `anotha` → another, `dis` → this |
| 🟠 EMOJI | 😤💔 |
| 🟣 ABBR | `2` → to |

**Preprocessing Needed:**
- Slang expansion: `imma` → I am going to
- Typo correction for phonetic spellings
- Numeral-to-word: `2` → to
- Emoji removal

---

### Sentence 17
> **"NEED COFFEE NOW ☕ cant human without it tbqh fam"**

| Type | Identified Issues |
|------|-----------------|
| 🔵 SLANG | `cant human` (can't function as a human), `tbqh` (to be quite honest), `fam` |
| 🟠 EMOJI | ☕ |
| 🟡 GRAMMAR | All caps, missing apostrophe |

**Preprocessing Needed:**
- Lowercasing: `NEED COFFEE NOW` → "need coffee now"
- Slang expansion: `tbqh` → to be quite honest, `fam` → family/friend
- Emoji removal or replacement
- Punctuation correction

---

### Sentence 18
> **"dis song hitssss different at 3am no jokes 🎵🌙 dey rly outdid demslvs"**

| Type | Identified Issues |
|------|-----------------|
| 🔵 SLANG | `hits different`, `no jokes` |
| 🔴 TYPO | `dis` → this, `dey` → they, `rly` → really, `demslvs` → themselves |
| 🟠 EMOJI | 🎵🌙 |
| 🔴 TYPO | `hitssss` → character elongation |

**Preprocessing Needed:**
- Character elongation normalization: `hitssss` → hits
- Phonetic typo correction: `dey` → they, `demslvs` → themselves
- Slang handling
- Emoji removal

---

### Sentence 19
> **"plsss sum1 hlp me wid dis math problem i literally cryng 😭📚"**

| Type | Identified Issues |
|------|-----------------|
| 🔵 SLANG | `literally` (used for emphasis) |
| 🔴 TYPO | `plsss` → please, `sum1` → someone, `hlp` → help, `wid` → with, `dis` → this, `cryng` → crying |
| 🟠 EMOJI | 😭📚 |

**Preprocessing Needed:**
- Numeral embedded abbreviation: `sum1` → someone
- Spell correction for heavily truncated words
- Character elongation normalization: `plsss` → please
- Emoji handling

---

### Sentence 20
> **"tfw u study all nite 4 da xam and it gets postpond lol rip 😂🤦‍♂️"**

| Type | Identified Issues |
|------|-----------------|
| 🔵 SLANG | `tfw` (that feeling when), `lol`, `rip` |
| 🔴 TYPO | `nite` → night, `da` → the, `postpond` → postponed |
| 🟠 EMOJI | 😂🤦‍♂️ |
| 🟣 ABBR | `u` → you, `4` → for, `xam` → exam |

**Preprocessing Needed:**
- Slang expansion: `tfw` → that feeling when, `lol` → laughing out loud
- Abbreviation normalization: `u` → you, `4` → for, `xam` → exam
- Spell correction: `postpond` → postponed
- Emoji removal

---

## Summary Table: Challenges Across All 20 Sentences

| Sentence # | Slang | Emojis | Typos | Abbreviations | Grammar | Mixed Language |
|:-----------:|:-----:|:------:|:-----:|:-------------:|:-------:|:--------------:|
| 1  | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| 2  | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| 3  | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| 4  | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| 5  | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| 6  | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| 7  | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| 8  | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| 9  | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| 10 | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| 11 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| 12 | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| 13 | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| 14 | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| 15 | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| 16 | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| 17 | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| 18 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| 19 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| 20 | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |

---

## Preprocessing Pipeline Overview

When working with messy text like the examples above, the following preprocessing pipeline should be applied:

```
Raw Messy Text
      │
      ▼
1. Lowercasing
      │
      ▼
2. Emoji Handling (Remove / Convert to text label)
      │
      ▼
3. Expand Abbreviations & Slang
      │
      ▼
4. Spell Correction (typo fixing)
      │
      ▼
5. Character Repetition Normalization (sooo → so)
      │
      ▼
6. Punctuation Normalization
      │
      ▼
7. Tokenization
      │
      ▼
8. Stopword Removal (optional, task-dependent)
      │
      ▼
9. Stemming / Lemmatization
      │
      ▼
Clean, Processed Text → NLP Model
```

---

## Detailed Preprocessing Steps Explained

### 1. 🔡 Lowercasing
Convert all text to lowercase to treat "OMG", "Omg", and "omg" as the same word.
```python
text = text.lower()
```

### 2. 😀 Emoji Handling
Emojis carry sentiment information. Two approaches:
- **Remove** them if they clutter the model input
- **Convert** them to text (e.g., 😂 → `:joy:` or `laughing`) to preserve sentiment
```python
import emoji
text = emoji.demojize(text)  # 😂 → :face_with_tears_of_joy:
```

### 3. 📖 Abbreviation & Slang Expansion
Use a custom dictionary to expand internet slang and abbreviations.
```python
slang_dict = {
    "omg": "oh my god", "lol": "laughing out loud",
    "tbh": "to be honest", "ngl": "not gonna lie",
    "brb": "be right back", "smh": "shaking my head",
    "fr": "for real", "rn": "right now", "imma": "i am going to",
    "tfw": "that feeling when", "ngl": "not gonna lie"
}
words = text.split()
text = " ".join([slang_dict.get(w, w) for w in words])
```

### 4. ✏️ Spell Correction
Use spell-checking libraries to fix typos.
```python
from textblob import TextBlob
text = str(TextBlob(text).correct())
```

### 5. 🔁 Character Repetition Normalization
Reduce elongated characters (e.g., `sooooo` → `so`, `yassss` → `yas`).
```python
import re
text = re.sub(r'(.)\1{2,}', r'\1\1', text)
```

### 6. 🔢 Number/URL/Mention Removal
Remove unnecessary tokens like URLs, user mentions, and standalone numbers.
```python
text = re.sub(r'http\S+', '', text)         # Remove URLs
text = re.sub(r'@\w+', '', text)            # Remove mentions
text = re.sub(r'#\w+', '', text)            # Remove hashtags
text = re.sub(r'\d+', '', text)             # Remove standalone numbers
```

### 7. ✂️ Punctuation Normalization
Remove or standardize punctuation.
```python
import string
text = text.translate(str.maketrans('', '', string.punctuation))
```

### 8. 🗂️ Tokenization
Split text into individual tokens (words).
```python
from nltk.tokenize import word_tokenize
tokens = word_tokenize(text)
```

### 9. 🚫 Stopword Removal *(task-dependent)*
Remove common words that carry little meaning (for classification tasks).
```python
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
tokens = [w for w in tokens if w not in stop_words]
```

### 10. 🌱 Stemming / Lemmatization
Reduce words to their root form.
```python
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
tokens = [lemmatizer.lemmatize(w) for w in tokens]
```

---

## Why Preprocessing Matters

| Issue | Impact Without Preprocessing | Solution |
|-------|------------------------------|---------|
| Typos | Model treats `dis` and `this` as different words → sparse feature space | Spell correction |
| Emojis | Non-ASCII characters cause encoding errors | Emoji removal/conversion |
| Slang | Sentiment/meaning is lost (`lmao` isn't in standard vocab) | Slang dictionary |
| Case differences | `OMG` ≠ `omg` doubles vocabulary size | Lowercasing |
| Elongation | `sooooo` ≠ `so` → unseen tokens | Regex normalization |
| Code-mixing | Standard English NLP models fail on Hinglish/mixed text | Multilingual models |

---

## Tools & Libraries for Text Preprocessing

| Library | Use Case |
|---------|----------|
| `TextBlob` | Spell correction, sentiment analysis |
| `NLTK` | Tokenization, stopwords, stemming, lemmatization |
| `spaCy` | Advanced NLP, NER, lemmatization |
| `emoji` | Emoji conversion to text |
| `pyspellchecker` | Spell checking |
| `re` (regex) | Pattern-based cleaning |
| `langdetect` | Language detection for code-mixed text |
| `SymSpell` | Fast spell correction using edit distance |

---

## Conclusion

Messy text data is a significant challenge in NLP. The 20 sentences collected above showcase real-world issues including **internet slang**, **emojis**, **typos**, **abbreviations**, **character elongation**, and **code-mixed language**. A well-designed preprocessing pipeline — covering lowercasing, emoji handling, slang expansion, spell correction, and normalization — is essential for transforming this noisy data into clean, machine-readable format that NLP models can learn from effectively.

---

*Assignment Completed: Text Challenges | AIML Internship Assignment-19*
