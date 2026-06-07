"""
Slang & Dialect Dictionary - Maps slang to standard English.
"""
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class Region(str, Enum):
    INDIA = "india"
    US = "us"
    UK = "uk"
    AUSTRALIA = "australia"
    GENERAL = "general"
    INTERNET = "internet"


class Tone(str, Enum):
    CASUAL = "casual"
    SARCASTIC = "sarcastic"
    AGGRESSIVE = "aggressive"
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


@dataclass
class SlangEntry:
    slang: str
    meaning: str
    region: Region = Region.GENERAL
    tone: Tone = Tone.CASUAL
    alternatives: List[str] = field(default_factory=list)


SLANG_DB: Dict[str, SlangEntry] = {}


def _reg(s, m, r=Region.GENERAL, t=Tone.CASUAL, alts=None):
    e = SlangEntry(s, m, r, t, alts or [])
    SLANG_DB[s.lower().strip()] = e
    for a in (alts or []):
        SLANG_DB[a.lower().strip()] = e


# Indian / Hinglish
_reg("scene kya hai", "what's going on", Region.INDIA, Tone.CASUAL, ["scene kya he", "scene kya h"])
_reg("kya kar raha hai", "what are you doing", Region.INDIA, Tone.CASUAL, ["kya kar rha hai"])
_reg("bhai", "brother / dude", Region.INDIA, Tone.CASUAL, ["bhaii", "bhaiii"])
_reg("yaar", "friend / dude", Region.INDIA, Tone.CASUAL, ["yar", "yaaar"])
_reg("jhakaas", "awesome / fantastic", Region.INDIA, Tone.POSITIVE, ["jhakas", "jhakkas"])
_reg("full tight hai", "it's amazing", Region.INDIA, Tone.POSITIVE, ["full tight h"])
_reg("mast", "great / cool", Region.INDIA, Tone.POSITIVE, ["masst", "maast"])
_reg("bakwas", "nonsense / rubbish", Region.INDIA, Tone.NEGATIVE, ["bakvas"])
_reg("jugaad", "creative workaround", Region.INDIA, Tone.CASUAL, ["jugad"])
_reg("timepass", "killing time", Region.INDIA, Tone.CASUAL, ["time pass"])
_reg("chill", "relax / take it easy", Region.INDIA, Tone.CASUAL)
_reg("acha", "okay / good", Region.INDIA, Tone.NEUTRAL, ["accha", "achha"])
_reg("thik hai", "it's okay / alright", Region.INDIA, Tone.NEUTRAL, ["theek hai", "thik h"])
_reg("pataka", "stunning / gorgeous", Region.INDIA, Tone.POSITIVE, ["patakha"])
_reg("bindaas", "carefree / bold", Region.INDIA, Tone.POSITIVE, ["bindas"])
_reg("fadu", "excellent / top-notch", Region.INDIA, Tone.POSITIVE, ["faadu"])
_reg("ghanta", "nothing / as if", Region.INDIA, Tone.SARCASTIC)
_reg("pakau", "boring / annoying", Region.INDIA, Tone.NEGATIVE, ["pakao"])
_reg("lafda", "trouble / fight / mess", Region.INDIA, Tone.AGGRESSIVE, ["lafde"])
_reg("sahi hai", "that's right / nice", Region.INDIA, Tone.POSITIVE, ["sahi h"])
_reg("khatam", "finished / done / over", Region.INDIA, Tone.NEUTRAL)
_reg("mazaa aa gaya", "had a great time", Region.INDIA, Tone.POSITIVE, ["maza aa gaya"])
_reg("phat gayi", "got scared", Region.INDIA, Tone.NEGATIVE, ["phat gyi"])
_reg("kadak", "strong / awesome", Region.INDIA, Tone.POSITIVE)
_reg("bawal", "crazy / insane", Region.INDIA, Tone.CASUAL, ["baval"])
_reg("chal be", "come on / get lost", Region.INDIA, Tone.CASUAL)
_reg("kya scene hai", "what's the situation", Region.INDIA, Tone.CASUAL, ["kya seen hai"])

# US / American
_reg("he's cooked", "he's in serious trouble", Region.US, Tone.CASUAL, ["bro is cooked", "she's cooked"])
_reg("no cap", "no lie / for real", Region.US, Tone.CASUAL, ["nocap"])
_reg("bussin", "really good / delicious", Region.US, Tone.POSITIVE, ["bussing"])
_reg("cap", "lie / false", Region.US, Tone.CASUAL, ["capping"])
_reg("fire", "amazing / excellent", Region.US, Tone.POSITIVE)
_reg("lit", "exciting / amazing", Region.US, Tone.POSITIVE)
_reg("slay", "did amazingly well", Region.US, Tone.POSITIVE, ["slayed", "slaying"])
_reg("bet", "okay / sure / agreed", Region.US, Tone.CASUAL, ["bett"])
_reg("vibe", "mood / feeling", Region.US, Tone.CASUAL, ["vibes", "vibing"])
_reg("lowkey", "secretly / kind of", Region.US, Tone.CASUAL, ["low key"])
_reg("highkey", "openly / very much", Region.US, Tone.CASUAL, ["high key"])
_reg("flex", "show off / boast", Region.US, Tone.CASUAL, ["flexing"])
_reg("ghosted", "suddenly stopped responding", Region.US, Tone.NEGATIVE, ["ghosting"])
_reg("salty", "bitter / upset", Region.US, Tone.NEGATIVE)
_reg("sus", "suspicious / shady", Region.US, Tone.CASUAL, ["sussy"])
_reg("fam", "close friend / family", Region.US, Tone.CASUAL)
_reg("drip", "stylish outfit", Region.US, Tone.POSITIVE, ["dripping"])
_reg("goat", "greatest of all time", Region.US, Tone.POSITIVE, ["GOAT"])
_reg("hits different", "feels uniquely good", Region.US, Tone.POSITIVE)
_reg("stan", "obsessive fan", Region.US, Tone.CASUAL, ["stanning"])
_reg("simp", "someone who does too much for a crush", Region.US, Tone.SARCASTIC, ["simping"])
_reg("bruh", "bro / expression of disbelief", Region.US, Tone.CASUAL, ["bruhhh"])
_reg("deadass", "seriously / for real", Region.US, Tone.CASUAL)
_reg("based", "bold / unapologetically true", Region.US, Tone.POSITIVE)
_reg("mid", "mediocre / not impressive", Region.US, Tone.NEGATIVE)
_reg("ate", "did extremely well", Region.US, Tone.POSITIVE)
_reg("rizz", "charm / charisma", Region.US, Tone.POSITIVE, ["rizzler"])
_reg("npc", "person acting robotic", Region.US, Tone.SARCASTIC, ["NPC"])
_reg("aura", "personal energy / presence", Region.US, Tone.CASUAL)
_reg("caught in 4k", "caught red-handed with proof", Region.US, Tone.SARCASTIC)
_reg("main character", "center of attention energy", Region.US, Tone.CASUAL)

# UK
_reg("innit", "isn't it / right", Region.UK, Tone.CASUAL, ["init"])
_reg("mandem", "group of male friends", Region.UK, Tone.CASUAL)
_reg("bruv", "brother / friend", Region.UK, Tone.CASUAL)
_reg("peng", "attractive / beautiful", Region.UK, Tone.POSITIVE)
_reg("bare", "a lot / very", Region.UK, Tone.CASUAL)
_reg("wagwan", "what's going on", Region.UK, Tone.CASUAL, ["wag1"])
_reg("cheeky", "playfully mischievous", Region.UK, Tone.CASUAL)
_reg("gutted", "very disappointed", Region.UK, Tone.NEGATIVE)
_reg("mint", "excellent / perfect", Region.UK, Tone.POSITIVE)
_reg("knackered", "very tired / exhausted", Region.UK, Tone.NEGATIVE)
_reg("dodgy", "suspicious / unreliable", Region.UK, Tone.NEGATIVE)
_reg("buzzing", "very excited", Region.UK, Tone.POSITIVE)
_reg("chuffed", "very pleased", Region.UK, Tone.POSITIVE)
_reg("skint", "broke / no money", Region.UK, Tone.NEGATIVE)

# Australian
_reg("arvo", "afternoon", Region.AUSTRALIA, Tone.CASUAL)
_reg("brekkie", "breakfast", Region.AUSTRALIA, Tone.CASUAL, ["brekky"])
_reg("reckon", "think / believe", Region.AUSTRALIA, Tone.CASUAL)
_reg("stoked", "extremely happy", Region.AUSTRALIA, Tone.POSITIVE)
_reg("heaps", "a lot / very", Region.AUSTRALIA, Tone.CASUAL)
_reg("no worries", "you're welcome", Region.AUSTRALIA, Tone.CASUAL)
_reg("servo", "gas station", Region.AUSTRALIA, Tone.CASUAL)

# Internet / Gen-Z
_reg("lmao", "laughing my ass off", Region.INTERNET, Tone.CASUAL, ["lmfao"])
_reg("ngl", "not gonna lie", Region.INTERNET, Tone.CASUAL)
_reg("fr", "for real", Region.INTERNET, Tone.CASUAL, ["fr fr"])
_reg("ong", "on god / I swear", Region.INTERNET, Tone.CASUAL)
_reg("smh", "shaking my head", Region.INTERNET, Tone.NEGATIVE)
_reg("idk", "I don't know", Region.INTERNET, Tone.NEUTRAL)
_reg("tbh", "to be honest", Region.INTERNET, Tone.NEUTRAL)
_reg("imo", "in my opinion", Region.INTERNET, Tone.NEUTRAL, ["imho"])
_reg("goated", "greatest / exceptional", Region.INTERNET, Tone.POSITIVE)
_reg("copium", "coping mechanism / denial", Region.INTERNET, Tone.SARCASTIC)
_reg("touch grass", "go outside", Region.INTERNET, Tone.SARCASTIC)
_reg("rent free", "constantly on one's mind", Region.INTERNET, Tone.CASUAL)
_reg("valid", "acceptable / reasonable", Region.INTERNET, Tone.POSITIVE)
_reg("shook", "shocked / in disbelief", Region.INTERNET, Tone.CASUAL)
_reg("snatched", "looking perfect", Region.INTERNET, Tone.POSITIVE)
_reg("delulu", "delusional", Region.INTERNET, Tone.SARCASTIC)
_reg("it's giving", "it has the energy of", Region.INTERNET, Tone.CASUAL)

# Context phrases
_reg("that's sick", "that's amazing", Region.GENERAL, Tone.POSITIVE)
_reg("it slaps", "it's really good", Region.GENERAL, Tone.POSITIVE)
_reg("spill the tea", "share the gossip", Region.GENERAL, Tone.CASUAL)
_reg("i'm dead", "that's extremely funny", Region.GENERAL, Tone.POSITIVE)
_reg("big yikes", "very awkward / cringe", Region.GENERAL, Tone.NEGATIVE)
_reg("catch feelings", "develop romantic interest", Region.GENERAL, Tone.CASUAL)
_reg("throw shade", "subtly insult someone", Region.GENERAL, Tone.NEGATIVE)


def get_all_entries() -> List[SlangEntry]:
    seen = set()
    unique = []
    for entry in SLANG_DB.values():
        if entry.slang not in seen:
            seen.add(entry.slang)
            unique.append(entry)
    return unique


def get_entries_by_region(region: Region) -> List[SlangEntry]:
    return [e for e in get_all_entries() if e.region == region]


def lookup(term: str) -> Optional[SlangEntry]:
    return SLANG_DB.get(term.lower().strip())


def get_stats() -> dict:
    entries = get_all_entries()
    region_counts = {}
    for e in entries:
        region_counts[e.region.value] = region_counts.get(e.region.value, 0) + 1
    return {
        "total_entries": len(entries),
        "total_mappings": len(SLANG_DB),
        "by_region": region_counts,
    }
