"""Signal interpreter adapter: what the athlete said, as typed signals with the source sentence."""
from __future__ import annotations

import re


BODY = re.compile(r'\b(elbows?|wrists?|shoulders?|knees?|(?:lower )?back|hips?|glutes?)\b', re.I)
PAIN = re.compile(r'\b(pain\w*|hurts?|hurting|sore|weird|pop(?:s|ping|ped)?|tweak\w*|ach(?:e|es|ing)|twinge\w*|injur\w*|strain\w*|discomfort|fatigued|tired)\b', re.I)
NEAR = 6  # words between a body part and a sensation for them to belong together
EASY = re.compile(r'\b(easy|flying|flew|too light|could have gone heavier|should have gone heavier)\b', re.I)
HARD = re.compile(r"\b(too heavy|struggl\w*|grind\w*|missed|failed|couldn.?t finish|so much harder)\b", re.I)
REDUCE = re.compile(r'\b(drop|lower|reduce|decrease)\b.{0,30}\b(weight|load)\b', re.I)
STATE_HOLD = re.compile(r'\b(exhausted|exhaustion|sick(?! of)|ill|fever|burn(?:t|ed) out|super tired|extremely tired)\b', re.I)
STATE_NOTE = re.compile(r'\b(stress\w*|unmotivated|not into it|anxious|low mood|hungry|starving|mentally)\b', re.I)


class KeywordSignals:
    """First interpreter: transparent word patterns, sentence by sentence. Replaceable by an
    interpreter that stores a language model's reading of each message (same signal shape)."""

    @staticmethod
    def _sentences(text):
        return [s for s in re.split(r'(?<=[.!?\n])\s+', text) if s.strip()]

    def read(self, messages):
        found = []
        for m in messages:
            for sentence in self._sentences(m['text']):
                ref = {'source': m['source'], 'id': m['ref'], 'at': str(m['at']), 'text': sentence.strip()[:300]}
                words = sentence.split()
                regional = False
                for i, word in enumerate(words):
                    following = re.sub(r'[^\w]', '', words[i + 1]).lower() if i + 1 < len(words) else ''
                    if following.startswith(('thrust', 'extension', 'press', 'raise', 'abduct', 'adduct', 'hinge', 'curl')):
                        continue
                    body = BODY.fullmatch(re.sub(r'[^\w]', '', word)) or (i + 1 < len(words) and BODY.fullmatch(
                        re.sub(r'[^\w ]', '', word + ' ' + words[i + 1])))
                    if body and any(PAIN.search(w) for w in words[max(0, i - NEAR):i + NEAR + 1]):
                        part = body.group(1).lower().rstrip('s').replace('lower ', '')
                        found.append({'kind': 'pain', 'region': 'hip' if part == 'glute' else part, **ref})
                        regional = True
                        break
                for kind, pattern in (('reduce', REDUCE), ('hard', HARD), ('easy', EASY),
                                      ('state_hold', STATE_HOLD), ('state_note', STATE_NOTE)):
                    # A sensation tied to a body part is regional, not a whole-body state; "less exhausted" is not exhaustion.
                    hit = pattern.search(sentence)
                    negated = hit and re.search(r"\b(less|not|no longer|never|isn't|wasn't|don't)\W+(?:\w+\W+){0,2}$",
                                                sentence[:hit.start()], re.I)
                    if hit and not negated and not (regional and kind in ('hard', 'state_hold')):
                        found.append({'kind': kind, **ref})
        return found
