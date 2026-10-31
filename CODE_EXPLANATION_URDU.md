# Code ki Line-by-Line Explanation — Simple Urdu Mein

Ye document **Personal Expense Tracker** project ke poore code ko line by line simple Urdu mein samjhata hai.
Har file ke liye pehle ye bataya gaya hai ke us file ka kaam kya hai, phir code ko usi tartib mein liya gaya hai jis tartib mein wo file mein likha hai: pehle chhota sa code snippet, phir uski explanation.

Ek baat zehan mein rakhein: **kharcha = expense**. Aur data file ko aap ek **register / daftar** ki tarah samajh sakte hain — jahan kharchay likhe jate hain taake baad mein bhi mil jayen.

Poora code in files mein hai:
1. `main.py`
2. `expense_tracker/__init__.py`
3. `expense_tracker/models.py`
4. `expense_tracker/storage.py`
5. `expense_tracker/analytics.py`
6. `expense_tracker/cli.py`
7. Tests: `tests/test_models.py`, `tests/test_storage.py`, `tests/test_analytics.py`

---

# File 1: `main.py`

**Is file ka kaam:** Ye poore program ka **darwaza (entry point)** hai. Jab aap terminal mein `python main.py ...` likhte hain, to sab se pehle yehi file chalti hai. Is ka apna koi khaas logic nahi — ye bas asli kaam `cli.py` wale `main()` function ko de deti hai.

```python
"""Entry point for the Personal Expense Tracker.

Run from this folder, for example:
    python main.py add --amount 250 --category Food --description "Lunch" --date 2026-10-05
"""
```

Ye teen `"""` ke darmiyan wala hissa **docstring** hai. Docstring code nahi hota, ye file ke sab se upar likhi gayi **note wali tehreer** hai jo parhne wale ko batati hai ke file hai kya. Is mein ye likha hai: "Ye Personal Expense Tracker ka entry point hai", aur neeche ek misal di hai ke program kaise chalana hai — `python main.py add --amount 250 ...` matlab 250 rupay ka kharcha "Food" category mein "Lunch" ke naam par add karna. Agar ye lines na bhi hon to program waisa hi chalega, lekin parhne wale ko samajh nahi aayegi ke shuru kahan se karna hai.

```python
from expense_tracker.cli import main
```

Ye line `expense_tracker` folder ke andar wali `cli.py` file se `main` naam ka **function import** karti hai. Import ka matlab: "doosri file mein bana banaya kaam yahan bula lo, dobara likhne ki zaroorat nahi". Agar ye line na ho, to neeche hum `main()` ko bula hi nahi sakte — Python error dega ke `main` naam ki koi cheez hai hi nahi.

```python
if __name__ == "__main__":
```

Ye Python ki ek mashhoor line hai, isay ghoor se samjhein. Har file ke paas chhupa hua ek variable hota hai jis ka naam `__name__` hai. Jab koi file **seedha chalayi jaye** (jaise hum `python main.py` karte hain), to us file ka `__name__` khud bakhud `"__main__"` ban jata hai. Lekin jab yehi file kisi doosri file mein **import** ki jaye, to `__name__` us file ka asli naam hota hai. To ye line poochti hai: "Kya mujhe seedha chalaya gaya hai?" Agar haan, to hi neeche wala kaam karo. Is se faida ye hai ke agar kal ko koi doosra program is file ko import kare, to tracker khud bakhud nahi chal parega.

```python
    raise SystemExit(main())
```

Ye line `main()` function ko chalati hai (jo `cli.py` mein hai) aur jo number `main()` wapas deta hai, usay program ka **exit code** bana kar program band kar deti hai. Exit code ek number hota hai jo computer ko batata hai ke program theek chala ya nahi: `0` matlab sab theek, `1` matlab koi ghalti hui. `raise SystemExit(...)` ka matlab hai "program ko yahin khatam kar do, aur ye number result ke tor par de do". Agar ye line na ho, to `main()` kabhi chalega hi nahi — file khulti aur foran band ho jati, kuch hota hi nahi.

---

# File 2: `expense_tracker/__init__.py`

**Is file ka kaam:** Ye bohat chhoti file hai, sirf 3 lines ki (ek docstring, ek khali line, ek code line). Is ka kaam sirf ye batana hai ke `expense_tracker` folder ek **package** hai — matlab code files ka ek munazzam group, jinhein doosri files `from expense_tracker.... import ...` karke istemal kar sakti hain.

```python
"""Personal Expense Tracker - a small CLI application for tracking expenses."""
```

Ek line wali docstring — file ka chhota sa taaruf: "Personal Expense Tracker — kharchay note karne wali ek chhoti CLI application". **CLI** ka matlab hai Command Line Interface, matlab wo program jo terminal mein commands likh kar chalaya jata hai, buttons wala nahi hota.

```python
__version__ = "1.0.0"
```

Ye line ek variable `__version__` banati hai jis mein program ka version number `"1.0.0"` rakha hai. Ye sirf maloomat ke liye hai — aaj program version 1.0.0 hai. Kal ko program mein baray changes aayen to isay 1.1.0 ya 2.0.0 kar diya jayega. Naam ke shuru aur aakhir mein `__` (double underscore) lagana Python mein is baat ki nishani hai ke ye ek khaas, andar ka variable hai. Agar ye line na bhi ho to program chalega, lekin phir kahin se pata nahi chalega ke software ka konsa version chal raha hai.

---

# File 3: `expense_tracker/models.py`

**Is file ka kaam:** Ye file tay karti hai ke **ek kharcha (expense) asal mein hai kya** — us mein konsi cheezein hongi (raqam, category, tafseel, tareekh), aur data ko sahi rakhne ke **usool (validation)** bhi yehi file check karti hai: raqam positive honi chahiye, tareekh sahi format mein honi chahiye, category khali nahi honi chahiye. Ghalat data ko ye file andar ghusne hi nahi deti.

```python
"""Data model for a single expense."""
```

Docstring: "Ek kharchay ka data model". **Model** ka matlab hai khaaka / template — jaise ek form hota hai jismein khaanay bane hote hain. Ye file wahi khaaka banati hai.

```python
from __future__ import annotations
```

Ye ek khaas import hai. Is ka asaan matlab: "Is file mein jahan jahan types likhe hain (jaise `-> str`, `: float`), unhein Python foran check na kare, unhein sirf note ke tor par rakhe." Is se nayi Python wali type likhai purani tarz par bhi masla nahi karti. Asaan alfaaz mein — ye ek safety wali setting hai, is ka program ke result par koi farq nahi parta.

```python
from dataclasses import dataclass, asdict
```

Ye line Python ki tayyar library `dataclasses` se do cheezein mangwati hai: `dataclass` aur `asdict`. **Dataclass** ek khaas sahulat hai jo neeche `Expense` class banane mein istemal hogi — ye khud bakhud wo code likh deti hai jo aam tor par haath se likhna parta hai (jaise object banane wala `__init__`). `asdict` ek function hai jo kisi dataclass object ko ek aam **dictionary** mein badal deta hai (dictionary matlab wo data jismein har cheez ka naam aur uski value joray ki surat mein hoti hai, jaise `"amount": 750`). Agar ye import na ho, to neeche `@dataclass` wala sira hi nahi chalega.

```python
from datetime import datetime
```

Ye line `datetime` library se `datetime` class mangwati hai. Is ka kaam tareekhen (dates) check karna hai — neeche ye batayegi ke jo tareekh user ne di hai, wo waqai ek sahi tareekh hai ya nahi, misal ke tor par "2026-13-01" (13wan maheena) ghalat hai.

```python
DATE_FORMAT = "%Y-%m-%d"
```

Ye ek **constant** hai — aisi value jo poore program mein ek hi rehti hai, is liye is ka naam baray harfon (capital) mein likha gaya hai, ye Python mein riwayat hai. `"%Y-%m-%d"` ek code hai jo tareekh ka format batata hai: `%Y` = saal 4 hisson mein (2026), `%m` = maheena 2 hisson mein (10), `%d` = din 2 hisson mein (05). Matlab poora format banta hai **saal-maheena-din**, jaise `2026-10-05`. Isay ek jagah rakhne ka faida: kal ko format badalna ho to sirf ye ek line badalni padegi, poori file nahi dhundni padegi.

```python
def validate_date(date_str: str) -> str:
```

Ye line ek **function** banana shuru karti hai jis ka naam `validate_date` hai. Function matlab kaam ka ek naam-daar hissa — jab bhi ye kaam chahiye ho, naam le kar bula lo. `def` Python ka lafz hai function banane ke liye. Brackets mein `date_str: str` hai — ye wo cheez hai jo function ko **di jayegi** (input), aur `: str` batata hai ke ye ek text (string) honi chahiye. Aakhir mein `-> str` batata hai ke function wapas bhi ek text hi dega. Asaan matlab: "Mujhe ek tareekh text mein do, mein check karke sahi tareekh text mein hi wapas dunga — ya ghalti bata dunga."

```python
    """Return the date string if it is a valid YYYY-MM-DD date, else raise ValueError."""
```

Function ki docstring — ek line mein function ka khulasa: "Agar tareekh sahi YYYY-MM-DD format mein hai to wohi wapas kar do, warna `ValueError` wali ghalti phenko." **ValueError** Python ki ek ghalti (error) ki qisam hai jo tab istemal hoti hai jab koi value ghalat ho.

```python
    try:
```

`try` ka matlab hai "koshish karo". Is ke andar wo code likha jata hai jismein ghalti honay ka khatra ho. Agar andar ghalti ho jaye, to program crash nahi hota — neeche wala `except` hissa us ghalti ko pakar leta hai. Isay **exception handling** kehte hain. Misal: aap kisi ko kehte hain "glass utha kar lao, agar gir jaye to mujhe bata dena, chillana mat".

```python
        parsed = datetime.strptime(date_str, DATE_FORMAT)
```

Ye line asal check hai. `datetime.strptime(...)` ek tayyar function hai jo text ko tareekh mein badalne ki koshish karta hai. Pehli cheez `date_str` hai (user ki di hui tareekh), doosri `DATE_FORMAT` hai (hamara format `"%Y-%m-%d"`). Agar text is format se match kare aur waqai sahi tareekh ho, to badli hui tareekh `parsed` naam ke variable mein save ho jati hai. Lekin agar tareekh ghalat ho — jaise `"05-10-2026"` ya `"2026-13-01"` — to yehi line `ValueError` phenkti hai, jo neeche pakra jayega. Agar koi aisi cheez de di jaye jo text hi na ho, to `TypeError` aata hai. Isi liye ye line `try` ke andar rakhi hai.

```python
    except (ValueError, TypeError):
```

Ye line `try` wali ghaltiyon ko pakarti hai. `except` matlab "agar ghalti ho to". Brackets mein do qisam ki ghaltiyan likhi hain: `ValueError` (tareekh ki value ghalat) aur `TypeError` (cheez hi ghalat qisam ki de di). Agar in dono mein se koi bhi ghalti upar wali line mein aayi, to program crash honay ke bajaye seedha yahan aa jayega.

```python
        raise ValueError(f"Invalid date '{date_str}'. Please use YYYY-MM-DD format, e.g. 2026-10-05.")
```

Jab ghalti pakri jati hai, to ye line ek **saaf aur asaan** `ValueError` phenkti hai jis mein user ko samjhaya gaya hai ke masla kya hai. `f"..."` ko **f-string** kehte hain — is se text ke andar `{date_str}` wali jagah par asli tareekh khud aa jati hai. Misal ke tor par agar user ne `"05-10-2026"` di, to message banega: `Invalid date '05-10-2026'. Please use YYYY-MM-DD format, e.g. 2026-10-05.` Ye is liye zaroori hai taake user ko Python ki mushkil english wali ghalti ke bajaye samajh aanay wala jawab mile. `raise` ka matlab hai ghalti ko jaan boojh kar aagay phenkna, taake bulane wala code faisla kare ke ab kya karna hai.

```python
    return parsed.strftime(DATE_FORMAT)
```

Agar koi ghalti nahi aayi, to function yahan pohanchta hai. `parsed.strftime(DATE_FORMAT)` us check ki hui tareekh ko wapas hamare format (`YYYY-MM-DD`) wale text mein badal kar **return** karta hai — return matlab function ka jawab wapas bhejna. Ek faida ye bhi hai ke tareekh ek hi standard surat mein wapas milti hai. Is ke baad function khatam ho jata hai.

```python
def validate_amount(amount) -> float:
```

Doosra function shuru hota hai: `validate_amount`, jo raqam (amount) check karega. Input ka naam sirf `amount` hai (is par koi type nahi likha, kyun ke user raqam kabhi number mein dega, kabhi text mein jaise `"250"` — dono ko sambhalna hai). `-> float` batata hai ke wapas hamesha **float** milega — float matlab dashariya wala number, jaise `99.50`.

```python
    """Return the amount as a positive float rounded to 2 decimals, else raise ValueError."""
```

Docstring ka khulasa: "Raqam ko positive float bana kar, 2 decimal tak round karke wapas karo, warna ValueError phenko."

```python
    try:
        value = float(amount)
```

Phir `try` block. Andar `float(amount)` di gayi cheez ko number mein badalne ki koshish karta hai. `"250"` de to `250.0` ban jayega, `250` de to bhi `250.0`. Badla hua number `value` variable mein save hota hai. Lekin agar `"abc"` jaisi cheez di jaye jo number ban hi nahi sakti, to yahan ghalti (`ValueError`) aayegi, aur agar bilkul hi ghalat qisam ki cheez di jaye to `TypeError` aayegi — dono neeche pakray jayenge.

```python
    except (TypeError, ValueError):
        raise ValueError(f"Invalid amount '{amount}'. Please enter a number, e.g. 250 or 99.50.")
```

Ghalti pakarne wala hissa. Number na ban sakne par ye saaf message ke saath `ValueError` phenkta hai: misal ke tor par `Invalid amount 'abc'. Please enter a number, e.g. 250 or 99.50.` Dhyaan dein, yahan ghaltiyon ki tartib `TypeError` pehle hai — tartib se koi farq nahi parta, dono pakri jani hain.

```python
    if value <= 0:
        raise ValueError("Amount must be greater than zero.")
```

Ab raqam number to ban gayi, lekin ek aur check baki hai: **raqam zero ya negative nahi honi chahiye**. `if value <= 0:` matlab "agar value zero ke barabar ya us se chhoti hai to". Aisi surat mein ye do lines `ValueError` phenkti hain message ke saath: "Amount must be greater than zero." Ye is liye zaroori hai kyun ke kharcha hamesha positive hota hai — "-50 rupay ka kharcha" ka koi matlab nahi. Agar ye check na ho, to log ghalti se negative raqam daal kar poora hisaab kharab kar sakte thay.

```python
    return round(value, 2)
```

Sab check pass ho jayen to ye line raqam ko **2 decimal tak round** karke wapas karti hai. `round(value, 2)` matlab `99.567` ko `99.57` bana do. Paison mein 2 decimal (paisay / cents) se zyada nahi hote, is liye ye safai zaroori hai — warna ajeeb se lambe number hisaab mein ghumte rahenge.

```python
@dataclass
class Expense:
```

Ab file ka sab se aham hissa shuru hota hai. `@dataclass` ek **decorator** hai — decorator ko aap ek tayyar sahulat samjhein jo class ke sar par laga di jati hai, aur wo class ke liye aam sa code khud likh deti hai. **Class** matlab ek khaaka (blueprint) — jaise ghar ka naqsha; naqshe se kai ghar ban sakte hain, wese hi is class se kai kharchay (objects) baneinge. Is class ka naam `Expense` hai. `@dataclass` lagane se Python khud bakhud object banane wala hissa (`__init__`), do kharchon ko barabar check karne wala hissa (`__eq__`), aur print karne ki surat (`__repr__`) bana deta hai. Agar `@dataclass` na lagayen, to ye sab code haath se lamba likhna parta, aur ghalti ka chance zyada hota.

```python
    """One expense entry."""
```

Class ki docstring: "Ek kharchay ki entry."

```python
    id: int
    amount: float
    category: str
    description: str
    date: str  # YYYY-MM-DD
```

Ye paanch lines `Expense` class ke **fields** hain — matlab har kharchay mein ye paanch cheezein hongi:
- `id: int` — kharchay ka khaas number (1, 2, 3...), `int` matlab poora number (integer). Ye number har kharchay ko doosron se alag pehchan deta hai, jaise register mein serial number.
- `amount: float` — kitne rupay kharch hue, dashariya wala number.
- `category: str` — kharcha kis qisam ka tha, text mein, jaise `"Food"`.
- `description: str` — chhoti si tafseel text mein, jaise `"Lunch"`.
- `date: str  # YYYY-MM-DD` — tareekh text mein. Aakhir mein `#` se shuru honay wala hissa **comment** hai — comment code nahi hota, sirf parhne wale ke liye note hai ke tareekh is format mein hogi: `YYYY-MM-DD`.

Dataclass mein ye sirf naam aur type likhna hi kaafi hai — Python inhi lines se samajh jata hai ke object banate waqt ye paanch cheezein deni hongi, aur kis tartib mein deni hongi.

```python
    def __post_init__(self):
```

Ye ek khaas function hai jis ka naam `__post_init__` hai. `self` har class function ka pehla input hota hai, jo usi khaas object ki taraf ishara karta hai jo abhi bana hai ("main khud"). `__post_init__` ki khaas baat: dataclass mein ye function **object bante hi khud bakhud chal jata hai**, aap ko alag se bulana nahi parta. Is ka kaam hai bane hue data ko foran check aur saaf karna. Naam ke shuru/aakhir mein `__` wale functions ko Python ke khaas (dunder) functions kehte hain.

```python
        self.amount = validate_amount(self.amount)
```

Object ki raqam ko upar wale `validate_amount` function se check karwaya jata hai, aur check ki hui saaf raqam wapas `self.amount` mein rakh di jati hai. `self.amount` matlab "is khaas kharchay ki raqam". Agar raqam ghalat thi (negative ya text), to `validate_amount` yahin `ValueError` phenk dega aur ghalat kharcha bane ga hi nahi. Asaan matlab: **darwazay par hi checking** — ghalat data andar ja hi nahi sakta.

```python
        self.date = validate_date(self.date)
```

Bilkul waisa hi kaam tareekh ke saath: `validate_date` se check karwa kar, sahi format wali tareekh wapas `self.date` mein rakh di. Ghalat tareekh par yahin ghalti aa jayegi aur object nahi banega.

```python
        self.category = str(self.category).strip()
```

Category ko pehle `str(...)` se lazmi text mein badla jata hai (agar kisi ne number de diya ho to wo text ban jaye), phir `.strip()` us ke aagay peeche wali **fazool khali jagah (spaces) hata** deta hai. Misal: `"  Food  "` ban jayega `"Food"`. Is safai ke baghair `"Food"` aur `" Food "` computer ke liye do alag categories ban jati, aur hisaab do hisson mein bant jata.

```python
        if not self.category:
            raise ValueError("Category cannot be empty.")
```

Agar safai ke baad category **khali reh gayi** (user ne sirf spaces di hon ya kuch na diya ho), to `if not self.category:` wala check pakar lega — `not` ke saath khali text ka matlab hai "agar ye khali hai to". Aisi surat mein `ValueError` phenka jata hai: "Category cannot be empty." Ye lazmi hai kyun ke baghair category ke kharcha hisaab mein kahin ginna mushkil ho jata hai.

```python
        self.description = str(self.description).strip()
        if not self.description:
            raise ValueError("Description cannot be empty.")
```

Ye do joray wali lines bilkul waisa hi kaam description (tafseel) ke liye karti hain: pehle text bana kar spaces saaf karo, phir agar khali reh jaye to `ValueError` phenko: "Description cannot be empty." Baghair tafseel ke baad mein yaad hi nahi rahega ke kharcha kis cheez par hua tha.

```python
    @property
    def month(self) -> str:
```

Ab ek aur khaas cheez: `@property`. Property matlab aisi cheez jo **function hoti hai lekin istemal variable ki tarah hota hai** — aap `expense.month` likhte hain (brackets nahi lagate), aur peeche se ye function chal kar jawab deta hai. `def month(self) -> str:` batata hai ke ye property ka naam `month` hai aur ye text wapas degi. Is ki zaroorat is liye padi kyun ke month alag se save nahi hai — wo tareekh ke andar hi chhupa hai, ye property usay nikal kar deti hai.

```python
        """The YYYY-MM month this expense belongs to."""
```

Property ki docstring: "Wo YYYY-MM wala maheena jis mein ye kharcha aata hai."

```python
        return self.date[:7]
```

Asal jaadoo is ek line mein hai. `self.date` kuch aisi hoti hai: `"2026-10-05"`. `[:7]` ko **slicing** kehte hain — is ka matlab hai "shuru se pehle 7 characters le lo". Pehle 7 characters hain `"2026-10"` — yani saal aur maheena. Bas yehi month hai. Misal se samjhein: poori tareekh mein se sirf "saal-maheena" wala hissa kaat kar de diya. Ye chhoti si line `analytics.py` mein month ke hisaab ko mumkin banati hai.

```python
    def to_dict(self) -> dict:
        return asdict(self)
```

`to_dict` function Expense object ko **dictionary** mein badalta hai. Andar sirf ek line hai: `return asdict(self)` — wahi `asdict` jo upar import kiya tha. Wo object ki har field ko naam-value ke joray mein badal deta hai, jaise `{"id": 1, "amount": 750.0, "category": "Food", "description": "Lunch", "date": "2026-10-05"}`. Ye is liye zaroori hai kyun ke file mein data save karne ke liye (JSON) pehle object ko is saada surat mein lana parta hai — object seedha file mein nahi likha ja sakta.

```python
    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
```

Ye `to_dict` ka ulta kaam hai: dictionary se wapas Expense object banana. `@classmethod` ek aur decorator hai — is ka matlab hai ke ye function kisi ek bane hue object par nahi, **poori class par** chalta hai, aur is liye is ka pehla input `self` nahi balkay `cls` hai, jo class ki taraf ishara karta hai ("class khud"). Aap isay yun bulate hain: `Expense.from_dict(data)`. Input `data: dict` hai (ek dictionary), aur `-> "Expense"` batata hai ke wapas ek Expense object milega. `"Expense"` ko commas (quotes) mein is liye likha hai kyun ke ye wada abhi class ke andar hi ho raha hai — Python ko pehle se type samajhne ki zaroorat nahi, isay sirf note rakho (ye wahi sahulat hai jo `from __future__ import annotations` deti hai).

```python
        return cls(
            id=int(data["id"]),
            amount=float(data["amount"]),
            category=str(data["category"]),
            description=str(data["description"]),
            date=str(data["date"]),
        )
```

Ye lines dictionary se har cheez naam le le kar nikalti hain, unhein sahi type mein badalti hain, aur phir `cls(...)` se — matlab `Expense(...)` se — naya object bana kar wapas bhejti hain. Har line ko samjhein:
- `id=int(data["id"])` — dictionary mein se `"id"` wali value nikali aur `int(...)` se poora number banaya. File se data hamesha sahi type mein nahi aata, is liye ye tabdeeli safety hai.
- `amount=float(data["amount"])` — raqam ko float banaya.
- `category=str(data["category"])`, `description=str(data["description"])`, `date=str(data["date"])` — baaki teenon ko lazmi text banaya.
- Aakhir mein ye object bante hi `__post_init__` khud chalega, to file se aaya hua data bhi dobara check ho jayega — agar file mein ghalat data ghus gaya ho, to wo yahin pakra jayega.

Is ke saath `models.py` khatam hoti hai. Khulasa: **is file ne tay kar diya ke sahi kharcha kaisa hota hai, aur ghalat data ko andar anay se rok diya.**

---

# File 4: `expense_tracker/storage.py`

**Is file ka kaam:** Ye file data ko **JSON file mein mehfooz rakhne aur wahan se wapas lanay** ki zimmedar hai. Program band ho jaye to data khatam nahi hona chahiye — is file ki wajah se kharchay ek file mein likhe jate hain, jaise register mein entry ho jati hai. Is file mein ek class hai `ExpenseStore`, aur sare kaam usi ke andar hain: file parhna, file likhna, kharcha add karna, delete karna.

```python
"""JSON file storage for expenses.

Data file format:
{
  "next_id": 4,
  "expenses": [ {expense}, ... ]
}
"""
```

File ki docstring sirf taaruf nahi hai — ye **data file ki surat** bhi samjhati hai. File ke andar do cheezein hongi: ek `"next_id"` (aglay naye kharchay ko konsa number milega), aur ek `"expenses"` wali list jismein sare kharchay honge. Misal mein `next_id` 4 dikhaya hai, matlab 3 kharchay pehle se hain aur aglay ko number 4 milega. Ye note is liye likha hai taake jo bhi ye file parhe, usay pehle se pata ho ke file khol kar andar kya nazar aayega.

```python
from __future__ import annotations
```

Wahi khaas import jo `models.py` mein tha: type wali likhai ko sirf note rakho, foran check mat karo. Safety setting, result par farq nahi.

```python
import json
```

Python ki tayyar `json` library mangwayi gayi. **JSON** data likhne ka ek mashhoor tareeqa hai jo dictionary jaisa lagta hai, aur har language/program isay parh sakta hai. Is library ke do kaam aagay bohat istemal honge: `json.load` (file se data parhna) aur `json.dump` (data file mein likhna). Agar ye import na ho, to file mein save karne ka poora kaam hi ruk jayega.

```python
from pathlib import Path
```

`pathlib` library se `Path` class mangwayi gayi. `Path` file ke **rastay (address)** ko sambhalne ka asaan aur mehfooz tareeqa hai — jaise `"data/expenses.json"`. Is se file hai ya nahi, us ka folder konsa hai, ye sab asani se check ho jata hai, aur Windows/Mac/Linux sab par ek hi tareeqa chalta hai.

```python
from .models import Expense
```

Ye line **apni hi doosri file** se `Expense` class mangwati hai. Naam se pehle laga hua `.` (dot) batata hai ke "yehi wala package, us ke andar wali `models` file". Expense class ki zaroorat is liye hai kyun ke file se parha hua saada data dobara Expense objects mein badalna hoga, aur naya kharcha add karte waqt bhi pehle Expense object hi banta hai.

```python
class ExpenseStore:
```

Class ki tareef shuru hoti hai. Naam `ExpenseStore` — **store** matlab godam / daftar, jahan data rakha jata hai. Is class ka ek object ek data file ko sambhalega: us file ka rasta is ke paas hoga, aur file par sare amal (parhna, likhna, add, delete) is ke functions se honge.

```python
    """Loads, saves and modifies expenses stored in a JSON file."""
```

Class ki docstring, ek line mein poora kaam: "JSON file mein rakhe kharchon ko load karta hai, save karta hai, aur un mein tabdeeli karta hai."

```python
    def __init__(self, file_path):
        self.file_path = Path(file_path)
```

`__init__` class ka wo khaas function hai jo **object bante hi sab se pehle khud bakhud chalta hai** — isay constructor bhi kehte hain. Jab koi `ExpenseStore("expenses.json")` likhta hai, to ye function chalta hai aur di gayi `file_path` ko `Path(file_path)` se Path object bana kar `self.file_path` mein mehfooz kar leta hai. `self.file_path` matlab "is store ki apni file ka rasta", jo baad mein har function istemal karega. Path mein badalne ka faida ye hai ke aagay `.exists()`, `.parent` jaisi sahulatein mil jati hain. Agar ye line na ho, to store ko pata hi nahi hoga ke us ki file hai kahan.

```python
    # -- internal helpers -------------------------------------------------
```

Ye ek **comment** hai jo sirf parhne wale ke liye nishan hai: "Is ke neeche andar ke madadgar (helper) functions hain." Naam se pehle `_` lage functions (jaise `_read_raw`) ka matlab hota hai "ye sirf is class ke andar ke istemal ke liye hain, bahir se seedha mat bulana". Comment ki ye line code ko khisson mein baant kar asaan banati hai.

```python
    def _read_raw(self) -> dict:
```

Helper function `_read_raw` shuru hota hai. **Raw** matlab kachha data — file se jaisa data aaya, waisa ka waisa, abhi Expense objects mein badla nahi gaya. `-> dict` batata hai ke wapas ek dictionary milegi.

```python
        if not self.file_path.exists():
            return {"next_id": 1, "expenses": []}
```

Pehla check: **agar file maujood hi nahi hai** (`.exists()` jhooth / False de), to ye samjho ke program pehli dafa chal raha hai — koi purana kharcha hai hi nahi. Aisi surat mein ek **khali khaaka** wapas kar do: `next_id` 1 (pehle kharchay ko number 1 milega) aur `expenses` khali list. Is line ki wajah se program pehli dafa chalane par crash nahi hota — bohat log ye check bhool jate hain aur un ka program pehli run par hi error de deta hai.

```python
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
```

Ab asal file parhne ka kaam, aur ye bhi `try` ke andar hai kyun ke file kharab bhi ho sakti hai. `with ... as f:` Python ka ek mehfooz tareeqa hai file kholne ka: is block ke khatam hotay hi file **khud bakhud band** ho jati hai, band karna bhoolne ka khatra nahi rehta.
- `self.file_path.open("r", ...)` — file ko parhne ke mode mein kholo; `"r"` matlab **read**.
- `encoding="utf-8"` — batata hai ke file ka text kis tarz par likha hai; `utf-8` duniya bhar ka standard hai, is se urdu/english har qism ka text sahi parha jata hai.
- `data = json.load(f)` — khuli hui file `f` se JSON data parho aur usay Python ki dictionary bana kar `data` mein rakh lo.

```python
        except json.JSONDecodeError:
            raise ValueError(
                f"Data file '{self.file_path}' is corrupted (not valid JSON). "
                "Fix it by hand or delete it to start fresh."
            )
```

Agar file ke andar likha hua data **kharab JSON** hai (misal, kisi ne file haath se edit karke bigaar di), to `json.load` ek khaas ghalti phenkta hai jis ka naam `json.JSONDecodeError` hai. Ye `except` usi ko pakarta hai aur us ki jagah ek **asaan insani message** wala `ValueError` phenkta hai: "Data file '...' kharab hai (sahi JSON nahi). Isay haath se theek karo, ya delete kar do aur nayi shuruaat karo." Do hisso mein likha message Python khud jor kar ek hi message bana deta hai. Is wrapping ka maqsad wahi hai jo `models.py` mein tha — user ko Python ki ghumao phirao wali ghalti nahi, seedha hal batana.

```python
        if not isinstance(data, dict) or "expenses" not in data:
            raise ValueError(f"Data file '{self.file_path}' has an unexpected format.")
```

Ek aur hifazati check. File sahi JSON to ho sakti hai, lekin us ki **surat ghalat** ho sakti hai — jaise andar dictionary ki bajaye sirf ek list ho, ya `"expenses"` wala khana hi na ho. `isinstance(data, dict)` poochta hai "kya data waqai dictionary hai?" aur `"expenses" not in data` poochta hai "kya is mein expenses wala khana ghayab hai?" Dono mein se koi ek bhi baat sahi hui (yani format ghalat hua), to `ValueError` phenko: "Data file ka format ajeeb hai." Agar ye check na ho, to aagay ja kar program kisi ajeeb si jagah crash hota aur asal wajah samajh hi na aati.

```python
        return data
```

Sab theek hai, to parhi hui dictionary wapas bhej do. `_read_raw` yahan khatam.

```python
    def _write_raw(self, data: dict) -> None:
```

Doosra helper: `_write_raw` — dictionary ko file mein likhna. Input `data: dict` hai, aur `-> None` ka matlab hai ye function **kuch wapas nahi deta**, is ka kaam sirf file mein likhna hai.

```python
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
```

Ye line pehle ye pakka karti hai ke file wala **folder maujood ho**. `.parent` file ke rastay se us ka folder nikalta hai (misal `data/expenses.json` ka parent `data` hai). `.mkdir(...)` folder banata hai. `parents=True` ka matlab: agar rastay mein kai folders ghayab hain to sare bana do. `exist_ok=True` ka matlab: agar folder pehle se hai to koi ghalti mat do, chup chaap aagay barho. Is line ke baghair, agar folder na ho to file likhte waqt program error de deta.

```python
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
```

Phir wohi `with` wala mehfooz tareeqa, lekin is dafa mode `"w"` hai matlab **write** — file khulegi aur purana content mita kar naya likha jayega. `json.dump(data, f, indent=2)` dictionary `data` ko JSON text bana kar file `f` mein likh deta hai. `indent=2` ka matlab hai har nayi line par 2 spaces ki indentation rakho, taake file insaan ke parhne ke liye bhi saaf nazar aaye — warna saara data ek hi lambi line mein chipka hota. Note karein: ye function poori file dobara likhta hai, sirf naya hissa nahi jorta. Is size ke program ke liye ye tareeqa theek aur simple hai.

```python
    # -- public API --------------------------------------------------------
```

Phir ek comment wala nishan: "Is ke neeche wo functions hain jinhein bahir wala code (jaise `cli.py`) istemal karega." Public API matlab bahir ke liye khulay darwazay — andar wale helpers (`_read_raw`, `_write_raw`) inhi ke peeche kaam karte hain.

```python
    def load_all(self) -> list[Expense]:
        data = self._read_raw()
        return [Expense.from_dict(item) for item in data["expenses"]]
```

`load_all` ka kaam: sare kharchay file se la kar Expense objects ki list bana kar dena. `-> list[Expense]` batata hai ke wapas Expense objects ki list milegi.
- Pehli line `_read_raw()` se kachhi dictionary mangwati hai.
- Doosri line ek **list comprehension** hai — list banane ka chhota tareeqa. Asaan alfaaz mein ye kehta hai: "Dictionary ke `expenses` khane mein jo items hain, har item ko `Expense.from_dict(item)` se Expense object banao, aur un sab ki ek list bana kar wapas kar do." Wahi kaam jo ek loop likh kar hota, yahan ek line mein ho gaya. Agar file khali thi, to list khali `[]` wapas jayegi — koi error nahi.

```python
    def add(self, amount, category, description, date) -> Expense:
```

`add` function naya kharcha shamil karta hai. Isay chaar cheezein di jati hain: raqam, category, tafseel, tareekh. Dhyaan dein id nahi di jati — **id store khud tay karega**, kyun ke user ko serial number ginne ki zimedari nahi deni chahiye.

```python
        data = self._read_raw()
```

Sab se pehle file ka maujooda data parho — naya kharcha purane data mein **jor** kar likhna hai, purane ko mitana nahi hai. Isi liye pehle parhna lazmi hai.

```python
        expense = Expense(
            id=int(data.get("next_id", 1)),
            amount=amount,
            category=category,
            description=description,
            date=date,
        )
```

Ab naya **Expense object** banta hai:
- `id=int(data.get("next_id", 1))` — dictionary se `"next_id"` wali value nikali. `.get("next_id", 1)` ki khoobi ye hai ke agar ye khana file mein na ho to ghalti ki bajaye **default value 1** mil jati hai. `int(...)` usay poora number bana deta hai.
- Baaki chaar lines di gayi raqam, category, tafseel aur tareekh waisi ki waisi object ko de deti hain.
- Jaise hi ye object banta hai, `models.py` wala `__post_init__` khud chal kar sare check kar leta hai — raqam ghalat ho to yahin `ValueError` aa jayega aur aagay ka koi kaam nahi hoga, file bhi kharab nahi hogi. Yehi is design ki khoobsurati hai: **checking ek hi jagah hoti hai, har jagah nahi likhni parti.**

```python
        data["expenses"].append(expense.to_dict())
```

Bane hue object ko `expense.to_dict()` se dictionary mein badla aur dictionary ki `expenses` wali list ke **aakhir mein jor diya** — `.append(...)` list ke aakhir mein nayi cheez lagata hai. Dhyaan dein file mein object nahi, us ki dictionary wali surat jati hai, kyun ke JSON sirf saada data hi save kar sakta hai.

```python
        data["next_id"] = expense.id + 1
```

`next_id` ko ek barha diya: jo number abhi istemal hua, us se ek zyada. Taake **agli dafa** add honay wale kharchay ko naya, na dohra hua number mile. Agar ye line na ho, to har naye kharchay ko wahi purana number milta rehta aur ids aapas mein takra jateen — phir delete karte waqt ghalat kharcha ur sakta tha.

```python
        self._write_raw(data)
        return expense
```

Badli hui poori dictionary `_write_raw` se file mein likh di — ab kharcha mehfooz hai, program band bhi ho jaye to data rahega. Phir bana hua `expense` object wapas bhej diya, taake bulane wala (CLI) user ko bata sake ke "kharcha #5 add ho gaya" waghera.

```python
    def delete(self, expense_id: int) -> bool:
        """Delete an expense by id. Returns True if one was removed."""
```

`delete` function id de kar ek kharcha mitata hai. Docstring kehta hai: "Id se kharcha mitao. Agar ek mita to True wapas karo." `-> bool` matlab jawab haan/naa (True/False) mein milega — is se bulane wala faisla kar sakta hai ke user ko "delete ho gaya" kehna hai ya "ye id mili hi nahi".

```python
        data = self._read_raw()
        before = len(data["expenses"])
```

Pehle data parha, phir `before` variable mein **mitane se pehle** kharchon ki tadaad note kar li — `len(...)` list ki lambai, yani kitni cheezein hain, gin kar deta hai. Ye number baad mein muqabla (compare) karne ke kaam aayega.

```python
        data["expenses"] = [e for e in data["expenses"] if int(e["id"]) != int(expense_id)]
```

Ye ek line poori list ko dobara banati hai — isay bhi list comprehension kehte hain, lekin is dafa **filter** ke saath. Asaan matlab: "Purani list ke har kharchay `e` ko nayi list mein sirf tab rakho jab us ki id, mitane wali id ke **barabar na ho**." Matlab jis id ko mitana tha, wo list se bahir reh gaya, baaki sab andar reh gaye. Dono taraf `int(...)` lagaya hai taake number ka number se hi muqabla ho (agar ek taraf text wala number aa gaya ho to bhi compare sahi ho). Ye tareeqa "jo mitana hai usay alag dhundo aur hatao" ki bajaye "sab ko rakho siwae us ek ke" wala hai — chhota aur mehfooz.

```python
        if len(data["expenses"]) == before:
            return False
```

Agar nayi list ki tadaad **pehle jitni hi** hai, is ka matlab hai kuch mita hi nahi — yani di gayi id wala kharcha file mein tha hi nahi. Aisi surat mein file ko dobara likhne ki zaroorat nahi, bas `False` wapas kar do: "nahi mila". Yahi True/False wala jawab CLI ko sahi message dikhane mein madad karta hai.

```python
        self._write_raw(data)
        return True
```

Agar tadaad kam ho gayi (kharcha mita), to badli hui data file mein likh do taake delete mehfooz ho jaye, aur `True` wapas kar do: "kaam ho gaya".

```python
    def clear(self) -> None:
        """Remove all expenses (used mainly by tests)."""
        self._write_raw({"next_id": 1, "expenses": []})
```

Aakhri function `clear` hai: ye poori file ko **khali khaakay** se badal deta hai — `next_id` wapas 1, expenses khali. Docstring khud kehta hai ke ye zyada tar tests mein istemal hota hai, taake har test nayi saaf file se shuru ho sakay. Aam istemal mein isay chalana khatarnak hoga kyun ke saara data ur jayega — is liye CLI mein is ki koi command rakhi hi nahi gayi.

`storage.py` ka khulasa: **ye file register (daftar) hai — parhna, likhna, naya kharcha darj karna, purana mitana, sab yehi sambhalti hai, aur kharab file par chillati nahi, saaf message deti hai.**

---

# File 5: `expense_tracker/analytics.py`

**Is file ka kaam:** Ye file sirf **hisaab kitab** karti hai — total nikalna, month ya category ke hisab se kharchay chhantna, month ka summary banana. Is file ki khaas baat ye hai ke ye na file parhti hai, na screen par kuch print karti hai. Isay kharchon ki list do, ye hisaab karke jawab de deti hai. Aisi saaf "sirf hisaab" wali files ko test karna bohat asaan hota hai, aur is liye docstring mein likha bhi hai: "pure logic, easy to test".

```python
"""Summary calculations over a list of expenses (pure logic, easy to test)."""
```

File ki docstring wohi baat kehti hai jo upar samjhayi: "Kharchon ki list par summary wale hisaab — saaf logic, test karna asaan."

```python
from __future__ import annotations

from .models import Expense
```

Pehli line wahi purani safety setting. Doosri line apne hi package ki `models` file se `Expense` class mangwati hai — ye sirf **types likhne** ke liye hai (jaise `list[Expense]`), taake parhne wale ko pata chale ke in functions ko Expense objects ki list milegi, koi aur cheez nahi.

```python
def total_amount(expenses: list[Expense]) -> float:
    return round(sum(e.amount for e in expenses), 2)
```

Pehla function `total_amount`: kharchon ki list lo, un ki kul raqam do.
- Andar wali cheez `e.amount for e in expenses` ko **generator expression** kehte hain — ye list ke har kharchay `e` ki sirf raqam (`e.amount`) ek ek karke deta jata hai.
- `sum(...)` un sab raqmon ko jor deta hai.
- `round(..., 2)` kul ko 2 decimal tak saaf karta hai, aur `return` jawab wapas bhejta hai.
Khali list do to `sum` zero deta hai — koi error nahi. Ye ek line is liye khoobsurat hai kyun ke loop likhne ki zaroorat hi nahi pari.

```python
def filter_by_month(expenses: list[Expense], month: str) -> list[Expense]:
    """month is YYYY-MM."""
    return [e for e in expenses if e.month == month]
```

`filter_by_month` list mein se sirf **ek maheenay** ke kharchay chhant kar deta hai. Docstring yaad dilati hai ke month `YYYY-MM` surat mein dena hai, jaise `"2026-10"`. Asal line ek list comprehension hai: "Har kharcha `e` nayi list mein sirf tab rakho jab `e.month` (wohi property jo `models.py` mein tareekh se maheena nikalti thi) diye gaye month ke barabar ho." Matlab poori list scan hoti hai, ghair mutaliqa kharchay bahir reh jate hain.

```python
def filter_by_category(expenses: list[Expense], category: str) -> list[Expense]:
    return [e for e in expenses if e.category.lower() == category.lower()]
```

`filter_by_category` waisa hi chhantne wala kaam category ke liye karta hai, lekin ek hoshiyari ke saath: dono taraf `.lower()` laga kar text ko **chhoti harfon** mein badal diya gaya hai, phir muqabla hota hai. Is se `"Food"`, `"food"` aur `"FOOD"` teeno ek hi cheez samjhe jate hain. Agar `.lower()` na lagaya jaye, to user `"food"` likhe aur kharcha `"Food"` par ho, to program kehta "koi kharcha nahi mila" — jo ke zahanat wala rawaiya nahi.

```python
def category_totals(expenses: list[Expense]) -> dict[str, float]:
    """Return {category: total} sorted by total, highest first."""
```

`category_totals` har category ka kul kharcha nikalta hai. `-> dict[str, float]` kehta hai jawab ek dictionary hoga jismein naam category ka aur value us ka total hoga, jaise `{"Food": 750.0, "Transport": 200.0}`. Docstring ek aur wada karti hai: ye dictionary **total ke hisaab se tartib** mein hogi, sab se bara total pehle.

```python
    totals: dict[str, float] = {}
```

Shuruaat mein ek **khali dictionary** `totals` banayi gayi. Abhi kuch nahi hai; loop chalte chalte ye bharti jayegi.

```python
    for expense in expenses:
```

**Loop** shuru hota hai — loop matlab ek kaam ko baar baar dohrana. Ye line kehti hai: list ke har kharchay ko ek ek karke lo, usay `expense` ka naam do, aur neeche wali line us par chalao. Jitne kharchay honge, neeche wali line utni dafa chalegi.

```python
        totals[expense.category] = round(totals.get(expense.category, 0.0) + expense.amount, 2)
```

Ye file ki sab se ghani (dense) line hai, isay khol kar samjhein. Maqsad: is kharchay ki raqam us ki category ke chalte hue total mein jama karna.
- `totals.get(expense.category, 0.0)` — dictionary se is category ka ab tak ka total nikalo; **agar category pehli dafa aa rahi hai** (dictionary mein hai hi nahi) to ghalti ki bajaye `0.0` le lo. `.get()` ki yehi khoobi hai — default value.
- `+ expense.amount` — us mein is kharchay ki raqam jor do.
- `round(..., 2)` — har jama ke baad 2 decimal tak safai, taake chhoti chhoti float wali ghaltiyan (jaise 0.1 + 0.2 = 0.30000000004) Jama na hoti jayen.
- `totals[expense.category] = ...` — naya total usi category ke naam par wapas rakh do.
Misal: Food ke kharchay 450 aur 300 aaye, to pehle totals mein Food = 0 + 450 = 450 banega, doosri dafa Food = 450 + 300 = 750.

```python
    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))
```

Aakhri line bhari hui dictionary ko tartib de kar wapas karti hai:
- `totals.items()` — dictionary ke (category, total) wale joray deta hai.
- `sorted(..., key=lambda item: item[1], reverse=True)` — in joron ko **total wali value** (`item[1]`, yani joray ki doosri cheez) ke hisaab se sort karo. `lambda` ek bina naam ka chhota function hai jo yahan sirf ye keh raha hai ke "sort karte waqt har joray ki doosri cheez (total) dekho, naam nahi". `reverse=True` tartib ulti kar deta hai — yani **sab se bara total sab se pehle**.
- `dict(...)` — sort kiye hue joron ko wapas dictionary bana deta hai. Python mein dictionary apni tartib yaad rakhti hai, is liye jo tartib yahan bani, wohi aagay screen par nazar aayegi.
Agar ye tartib wali mehnat na ki jaye, to categories be-tartib aati aur user ko khud dhundna parta ke sab se zyada kharcha kahan hua.

```python
def monthly_summary(expenses: list[Expense], month: str) -> dict:
    """Summary for one month: total, count, average and per-category totals."""
```

`monthly_summary` upar wale chhote functions ko **jod kar** ek poora month ka report card banata hai. Docstring batati hai ke is mein chaar cheezein hongi: total, tadaad (count), ausat (average), aur category ke hisaab se totals.

```python
    month_expenses = filter_by_month(expenses, month)
    total = total_amount(month_expenses)
    count = len(month_expenses)
```

Teen lines teen tayyariyan:
- Pehle `filter_by_month` se sirf us month ke kharchay alag kar liye — note karein, code dobara nahi likha gaya, **purana function hi istemal** hua. Yahi achhe code ki pehchan hai: ek kaam ek hi jagah likho, har jagah wahan se bulao.
- Phir `total_amount` se un ka kul jor nikala.
- Phir `len(...)` se gin liya ke kharchay kitne hain.

```python
    return {
        "month": month,
        "count": count,
        "total": total,
        "average": round(total / count, 2) if count else 0.0,
        "by_category": category_totals(month_expenses),
    }
```

Ab ek dictionary bana kar wapas ki jati hai jismein har cheez naam ke saath hai:
- `"month"` — konsa maheena tha.
- `"count"` — kharchon ki tadaad.
- `"total"` — kul raqam.
- `"average"` — ausat kharcha. Ye line khaas hai: `round(total / count, 2) if count else 0.0` matlab "agar count zero se zyada hai to total ko count par taqseem karke ausat nikalo, **warna 0.0 de do**". Ye hifazat is liye hai kyun ke kisi cheez ko zero par taqseem karna maths mein mumkin nahi aur Python mein is par program crash (ZeroDivisionError) ho jata hai. Khali maheenay ka summary mangna bilkul jaiz hai — is hifazat ki wajah se jawab aaram se "0 kharchay, total 0" aata hai, crash nahi hota.
- `"by_category"` — `category_totals(month_expenses)` chala kar us month ke category totals bhi isi report mein shamil kar diye.
Is dictionary ko phir `cli.py` screen par khoobsurat bana kar dikhata hai — hisaab yahan, dikhawa wahan. Yehi alag alag zimmedariyon wala design hai.

```python
def all_categories(expenses: list[Expense]) -> list[str]:
    """Unique category names, alphabetically sorted (case-insensitive)."""
    return sorted({e.category for e in expenses}, key=str.lower)
```

Aakhri function `all_categories`: tamam kharchon mein istemal hui categories ki **ek ek dafa wali** list deta hai.
- `{e.category for e in expenses}` — ghore ke brackets `{ }` wali ye surat ek **set** banati hai. Set ki khaas baat: is mein ek cheez **dobara nahi aa sakti** — "Food" das dafa bhi aaye, set mein ek hi dafa rahegi. Yahi duplicate hatane ka sab se asaan tareeqa hai.
- `sorted(..., key=str.lower)` — set ko list mein badal kar harfon ki tartib (alphabetical) mein sort karta hai, aur sort karte waqt `.lower()` is liye ke "food" aur "Food" apni jagah sahi payen (bari harfon wali cheezein warna ajeeb tartib mein aa jati hain).
Docstring bhi yehi kehti hai: unique naam, alphabetical tartib, case ka khayal kiye baghair.

`analytics.py` ka khulasa: **ye file munshi (accountant) hai — list do, hisaab laga kar saaf jawab de deti hai, na file ko haath lagati hai na screen ko.**

---

# File 6: `expense_tracker/cli.py`

**Is file ka kaam:** Ye file program ka **sab se samne wala hissa** hai — user se baat cheet yehi karti hai. Is ke teen bade kaam hain:
1. Terminal mein likhi gayi command ko samajhna (kaunsi command hai: `add`, `list`, `delete`, `summary`, `categories` — aur us ke saath diye gaye options).
2. Us command ke mutabiq peeche wali files (`storage.py`, `analytics.py`) se kaam karwana.
3. Natija screen par saaf suthri surat mein dikhana.

**CLI** ka matlab hai Command Line Interface. Is file ka dil Python ki `argparse` library hai, jo commands samajhne ka kaam bohat asaan kar deti hai.

```python
"""Command-line interface for the Personal Expense Tracker."""
```

Docstring: "Personal Expense Tracker ka command-line interface."

```python
from __future__ import annotations
```

Wahi purani safety setting — types foran check nahi honge.

```python
import argparse
import sys
```

Do imports:
- `argparse` — Python ki tayyar library jo terminal commands ko samajhti hai. Command ke hisse (jaise `--amount 750`) ko ye khud alag alag karke naam de deti hai, aur ghalat command par khud madad wala message bhi dikhati hai.
- `sys` — Python ke system se rabte wali library. Is file mein ye sirf ek kaam ke liye hai: ghalti wale messages ko aam output wali jagah ki bajaye **error wali jagah (`sys.stderr`)** par bhejna, aagay `cmd_delete` aur `main` mein nazar aayega.

```python
from datetime import date as date_cls
```

Ye line `datetime` library se `date` class mangwati hai, lekin usay naya naam `date_cls` de kar. Naam badalne ki wajah: is program mein lafz "date" har jagah kharchay ki tareekh ke liye istemal hota hai (jaise `args.date`, `expense.date`) — agar class ka naam bhi `date` rehta to uljhan hoti. `as date_cls` matlab "isay la to rahe hain, magar hamare yahan is ka naam date_cls hoga". Is class ka sirf ek kaam aagay aayega: **aaj ki tareekh** nikalna.

```python
from .analytics import (
    all_categories,
    category_totals,
    filter_by_category,
    filter_by_month,
    monthly_summary,
    total_amount,
)
```

Ye kai lines par phaila hua import hai — apne hi package ki `analytics` file se wo **saare hisaab wale functions** mangwaye gaye hain jo CLI ko chahiye honge: categories ki list, category totals, category/month ki chhantai, month ki summary, kul total. Brackets `( )` laga kar import ko kai lines mein toda gaya hai taake parhna asaan ho — kaam ek hi hai. Agar in mein se ek bhi function yahan na mangwaya jaye aur neeche istemal ho, to Python "ye naam mujhe nahi mila" wala error dega.

```python
from .storage import ExpenseStore
```

`storage` file se `ExpenseStore` class mangwayi gayi — data parhne likhne ka kaam yehi karegi.

```python
DEFAULT_DATA_FILE = "expenses.json"
SUGGESTED_CATEGORIES = ["Food", "Transport", "Bills", "Shopping", "Education", "Health", "Entertainment", "Other"]
```

Do constants (capital naam walay, poori file mein ek hi rehne wale):
- `DEFAULT_DATA_FILE = "expenses.json"` — agar user koi file na bataye, to data is naam ki file mein save hoga. Naam ek jagah rakhne se badalna asaan rehta hai.
- `SUGGESTED_CATEGORIES = [...]` — mashwara di gayi categories ki tayyar list: Food, Transport, Bills, Shopping, Education, Health, Entertainment, Other. Ye sirf **mashwara** hai, pabandi nahi — user apni marzi ki category bhi bana sakta hai. Ye list `categories` command mein dikhayi jati hai.

```python
def _print_table(expenses) -> None:
```

Ab madadgar function `_print_table` shuru hota hai. Naam ke shuru mein `_` ka matlab wohi: ye andar ka helper hai, bahir se koi isay seedha nahi bulata. Kaam: kharchon ki list ko ek **saaf table** ki surat mein print karna. `-> None` matlab ye kuch wapas nahi deta, sirf screen par likhta hai.

```python
    if not expenses:
        print("No expenses found.")
        return
```

Pehla check: agar list **khali** hai, to table banane ki zehmat hi mat karo — seedha `No expenses found.` print karo aur `return` se function se bahir nikal jao. Is chhoti si hifazat ke baghair khali list par neeche wali lines chalti aur ek ajeeb si khali table nazar aati. Ye "pehle khali wala case sambhalo" wala andaz achhe code mein har jagah milta hai.

```python
    print(f"{'ID':<5}{'Date':<12}{'Category':<16}{'Amount':>10}  Description")
```

Ye line table ki **heading** print karti hai, aur is mein ek nayi cheez hai: **format specifiers** — ghore brackets ke andar colon ke baad wala hissa batata hai ke har cheez ko kitni jagah mein aur kis taraf rakhna hai:
- `{'ID':<5}` — "ID" ko 5 characters ki jagah mein **left** taraf rakho (`<` matlab left). Yani "ID" ke baad 3 khali jagahen ayengi.
- `{'Date':<12}` — "Date" ko 12 characters ki jagah, left par.
- `{'Category':<16}` — "Category" ko 16 characters ki jagah, left par.
- `{'Amount':>10}` — "Amount" ko 10 characters ki jagah mein **right** taraf rakho (`>` matlab right). Numbers right par rakhna hisaab ki riwayat hai — akhri digit ek line mein aayen to jor parhna asaan hota hai.
- Aakhir mein do spaces aur `Description` seedha likh diya, us ke liye koi fix jagah nahi kyun ke tafseel lambi chhoti ho sakti hai.
In fix jagahon ki wajah se sare columns seedhi line mein khade nazar aate hain — yehi chhoti chhoti cheezein program ko "professional" feel deti hain.

```python
    print("-" * 75)
```

Ye ek line ki **lakeer** print karti hai. `"-" * 75` matlab dash `-` ko 75 dafa dohra do. Heading ke neeche ye lakeer table ko upar wale hisse se alag karti hai.

```python
    for e in expenses:
        print(f"{e.id:<5}{e.date:<12}{e.category:<16}{e.amount:>10.2f}  {e.description}")
```

Loop chalta hai: list ke har kharchay `e` ke liye ek line print hoti hai, bilkul heading wali hi jagahon ke saath:
- `e.id` 5 jagah left par, `e.date` 12 jagah left par, `e.category` 16 jagah left par.
- `{e.amount:>10.2f}` — raqam 10 jagah mein right par, aur `.2f` ka matlab hai float ko **hamesha 2 decimal** ke saath dikhao: `750` nahi, `750.00`. Is se numbers ek dosre ke neeche seedhe khade hote hain.
- Aakhir mein do spaces ke baad `e.description`.
Jitne kharchay honge, utni lines print hongi — tees kharchay hon to tees lines.

```python
    print("-" * 75)
    print(f"{'Total':<33}{total_amount(expenses):>10.2f}")
```

Table ke aakhir mein dobara lakeer, phir **Total wali line**. `{'Total':<33}` mein Total ko 33 characters ki jagah mili hai — ye number ghore se dekhein: 5 (ID) + 12 (Date) + 16 (Category) = **33**. Yani "Total" ka lafz teeno columns ke barabar jagah le kar khatam hota hai, aur us ke foran baad kul raqam bilkul Amount wale column ke neeche aa kar khadi hoti hai. Total nikalne ke liye yahan `analytics` wala `total_amount(expenses)` bulaya gaya — hisaab dobara **nahi likha gaya**, tayyar function istemal hua hai. Yahi asal khoobi hai files alag rakhne ki.

```python
def cmd_add(args, store: ExpenseStore) -> int:
```

Ab asal commands wale functions shuru hote hain. Har command ka apna function hai, aur sab ka andaz ek jaisa hai: do cheezein milti hain — `args` (user ki command se niklay hue hisse) aur `store` (data sambhalne wala object) — aur jawab mein ek **int** wapas jata hai jo exit code hai: `0` matlab kaam ho gaya, `1` matlab ghalti. `cmd_add` ka kaam: naya kharcha add karna.

```python
    expense_date = args.date or date_cls.today().isoformat()
```

Ye line tareekh tay karti hai, aur is mein ek pyara sa tareeqa hai: `args.date or ...` matlab "**agar** user ne `--date` di hai to wohi lo, **warna** doosri cheez lo". User ne tareekh na di ho to `args.date` khali (None) hota hai, aur tab `date_cls.today()` **aaj ki tareekh** deta hai, jisay `.isoformat()` hamare `YYYY-MM-DD` wale format ke text mein badal deta hai. Aam tor par kharcha aaj hi ka hota hai, is liye ye default user ka time bachata hai — usay roz tareekh likhne ki zaroorat nahi.

```python
    expense = store.add(args.amount, args.category, args.description, expense_date)
```

Command ka asal amal: store ke `add` function ko chaar cheezein de do — user ki raqam, category, tafseel, aur upar tay ki gayi tareekh. Store peeche Expense object banayega, check karega (ghalat raqam par wahin `ValueError` aa jayega jo aakhir mein `main` pakrega), file mein likhega, aur bana hua kharcha wapas dega jo yahan `expense` mein save ho jata hai. Dhyaan dein: CLI ne khud na check kiya, na file likhi — **har kaam usi file ka hai jis ki wo zimmedari hai.**

```python
    print(f"Added expense #{expense.id}: {expense.amount:.2f} [{expense.category}] {expense.description} on {expense.date}")
    return 0
```

User ko tasdeeq (confirmation) wala message print hota hai. F-string ke andar bane hue kharchay ki asal values aa jati hain: usay mila hua naya id, 2 decimal wali raqam (`:.2f` phir wohi format), category ghore brackets mein, tafseel, aur tareekh. Misal: `Added expense #5: 750.00 [Food] Lunch on 2026-10-05`. Ye message bohat zaroori hai — is ke baghair user andhere mein rehta ke kaam hua bhi ya nahi. Phir `return 0` — "kaam theek ho gaya" wala exit code.

```python
def cmd_list(args, store: ExpenseStore) -> int:
    expenses = store.load_all()
```

`cmd_list` kharchay dikhane wali command ka function hai. Pehli line store se `load_all()` bulwa kar sare kharchay file se mangwa leti hai — Expense objects ki list `expenses` mein aa gayi.

```python
    if args.month:
        expenses = filter_by_month(expenses, args.month)
```

Agar user ne `--month` diya hai (jaise `--month 2026-10`), to poori list ko `filter_by_month` se chhan kar sirf us maheenay wali kar do, aur **wohi naam** `expenses` dobara istemal karo — ab aagay ka kaam chhoti hui list par hoga. User ne month na diya ho to ye `if` chalta hi nahi, poori list rehti hai. Isay kehte hain **optional filter** — ek hi code dono suraton ko sambhalta hai.

```python
    if args.category:
        expenses = filter_by_category(expenses, args.category)
```

Bilkul waisa hi doosra filter category ke liye. Note karein dono filters ek saath bhi lag sakte hain: pehle month chhana, phir us chhani hui list mein se category chhani — yani "October mein sirf Food wale kharchay" wali command bhi chalegi.

```python
    expenses = sorted(expenses, key=lambda e: (e.date, e.id))
```

Ab list ko **tartib** di jati hai: `sorted(...)` list ko sort karta hai. `key=lambda e: (e.date, e.id)` wo chhota sa bina-naam function hai jo batata hai ke sort kis hisaab se ho: pehle **tareekh** ke hisaab se (purani tareekh pehle), aur agar do kharchon ki tareekh ek hi ho to phir **id** ke hisaab se. Is tartib ke baghair kharchay file wali be-tartib surat mein nazar aate aur parhna mushkil hota.

```python
    _print_table(expenses)
    return 0
```

Tayar list ko upar wale helper `_print_table` ke hawale kar do jo table bana kar dikha dega — table banana ka code yahan dobara nahi likha gaya. Phir `return 0`, kaam khatam.

```python
def cmd_delete(args, store: ExpenseStore) -> int:
    if store.delete(args.id):
```

`cmd_delete` kharcha mitane wali command ka function hai. Pehli hi line mein store ka `delete` function bulaya gaya hai user ki di hui id (`args.id`) ke saath, aur us ka True/False wala jawab seedha `if` mein check ho raha hai: agar jawab **True** hai (kharcha mil kar mit gaya) to andar wala hissa chalega.

```python
        print(f"Deleted expense #{args.id}.")
        return 0
```

Mita to tasdeeq ka message print karo ("Deleted expense #3.") aur kamyabi wala `return 0` do.

```python
    print(f"Error: no expense with ID {args.id} was found.", file=sys.stderr)
    return 1
```

Agar jawab **False** tha (wo id file mein thi hi nahi), to function upar wale hisse se bahir aa kar yahan pohanchta hai. Ghalti wala message print hota hai, lekin ek farq ke saath: `file=sys.stderr` likha hai — matlab ye message aam output par nahi, **error wali khaas jagah (stderr)** par bhejo. Faida: computer ke doosre programs aur scripts aam jawab aur ghalti ko alag alag pehchan sakte hain. Phir `return 1` — ghalti wala exit code. Note karein program crash nahi hua, shanti se bata kar band hone ki taraf gaya.

```python
def cmd_summary(args, store: ExpenseStore) -> int:
    expenses = store.load_all()
```

`cmd_summary` summary dikhane wali command ka function hai. Pehle waisa hi `load_all()` se sare kharchay mangwa liye.

```python
    if args.month:
        summary = monthly_summary(expenses, args.month)
```

Agar user ne month diya hai, to `analytics` wale `monthly_summary` se us maheenay ki poori report (dictionary) mangwa lo — hisaab wahan hoga, yahan sirf dikhawa.

```python
        print(f"Summary for {summary['month']}")
        print(f"  Expenses: {summary['count']}")
        print(f"  Total:    {summary['total']:.2f}")
        print(f"  Average:  {summary['average']:.2f} per expense")
        by_category = summary["by_category"]
```

Summary ki pehli chaar lines print hoti hain. Dictionary se har cheez us ke **naam wale khaanay** se nikali gayi hai: `summary['month']`, `summary['count']`, waghera. Total aur average ke aakhir mein `:.2f` phir wohi 2 decimal wala format hai. "Total:" ke baad zyada spaces aur "Average:" ke baad kam spaces jaan boojh kar rakhi hain taake saare numbers ek seedh mein khade nazar ayen — chhoti si safai, par professional feel yehi deti hai. Aakhir mein category totals ko alag variable `by_category` mein nikal liya, kyun ke aagay dono suraton (month wali aur overall wali) mein yehi data ek hi tareeqay se print hona hai.

```python
    else:
        print("Overall summary (all months)")
        print(f"  Expenses: {len(expenses)}")
        print(f"  Total:    {total_amount(expenses):.2f}")
        by_category = category_totals(expenses)
```

Agar month **nahi** diya gaya, to `else` wala hissa chalta hai — yani **overall summary**, tamam maheenon ki mila kar:
- Heading print hoti hai: "Overall summary (all months)".
- Tadaad ke liye summary dictionary ki zaroorat nahi, seedha `len(expenses)` gin liya.
- Total ke liye `total_amount(expenses)` bulaya gaya — purana function, naya hisaab nahi.
- Aur `by_category` ke liye is dafa `category_totals(expenses)` bulaya — poori list par.
Ghoor karein dono raste (if aur else) aakhir mein **ek hi cheez** tayyar karte hain: `by_category` naam ki dictionary. Isi liye aagay ka code dono suraton ke liye ek hi dafa likha gaya hai — ye code dobara likhne se bachne ki ek aur achhi misal hai.

```python
    if by_category:
        print("\nBy category:")
        for category, total in by_category.items():
            print(f"  {category:<16}{total:>10.2f}")
```

Agar category totals **khali nahi** hain (yani kharchay maujood thay), to unhein print karo:
- `print("\nBy category:")` — `\n` ek khaas code hai jo print se pehle **ek khali line** deta hai, taake ye hissa upar wale hisse se alag saaf nazar aaye.
- `for category, total in by_category.items():` — loop dictionary ke har (category, total) joray ko ek ek karke nikalta hai; joray ki pehli cheez `category` mein aur doosri `total` mein jati hai. Dictionary pehle hi baray total se chhote ki taraf sort ki hui aayi thi (analytics wali mehnat), to yahan wohi khoobsurat tartib nazar aayegi.
- Print wali line mein `{category:<16}` category ko 16 ki jagah left par aur `{total:>10.2f}` total ko 10 ki jagah right par 2 decimal ke saath rakhta hai — bilkul table wali hi tartib, taake saari lines ek jaise columns mein nazar ayen.
Khali dictionary par `if` jhooth hota hai, to ye hissa chalta hi nahi — "By category:" ke neeche khali jagah dekh kar user confuse nahi hota.

```python
    return 0
```

Summary dikha di, kamyabi ka `0` wapas.

```python
def cmd_categories(args, store: ExpenseStore) -> int:
    used = all_categories(store.load_all())
```

`cmd_categories` aakhri command ka function hai jo categories ki list dikhata hai. Dhyaan dein, is function ne `args` ka koi hissa istemal hi nahi kiya — `categories` command ke saath koi option hota hi nahi — lekin function ko baaki commands jaisa hi rakha gaya hai taake saara system ek andaz ka rahe. Pehli line mein `all_categories` ko `store.load_all()` ki list de kar wo categories mangwa li jo user **asal mein istemal kar chuka** hai.

```python
    print("Suggested categories:")
    for category in SUGGESTED_CATEGORIES:
        print(f"  - {category}")
```

Pehle mashwara wali categories print hoti hain: heading ke baad loop file ke upar wali `SUGGESTED_CATEGORIES` list ko ek ek karke "  - Food" wali surat mein chap deta hai.

```python
    if used:
        print("\nCategories you have used:")
        for category in used:
            print(f"  - {category}")
    return 0
```

Agar user ne asal mein kuch categories istemal ki hain (`used` khali nahi), to khali line ke baad doosri heading aur wo categories bhi isi andaz mein print ho jati hain. Naye user ke liye `used` khali hoga, to ye hissa nahi chalega aur sirf mashwara wali list nazar aayegi. Phir `return 0`.

```python
def build_parser() -> argparse.ArgumentParser:
```

Ab file ka wo function aata hai jo **commands ka naksha** banata hai — `build_parser`. Isay samajhne se pehle **parser** ka matlab samjhein: parser wo cheez hai jo terminal mein likhi hui puri line ko parh kar us ke hisse alag alag karti hai — kaunsi command hai, konsa option hai, us ki value kya hai. Ye function sirf naksha tayyar karta hai, command abhi chalti nahi. `-> argparse.ArgumentParser` batata hai ke wapas ek parser object milega.

```python
    parser = argparse.ArgumentParser(
        prog="expense-tracker",
        description="Track personal expenses from the command line.",
    )
```

Asli parser banta hai. `prog="expense-tracker"` program ka wo naam hai jo help aur error messages mein nazar aayega. `description="Track personal expenses from the command line."` wo ek line hai jo user `--help` likhe to sab se upar dikhti hai — program apna taaruf khud karata hai. Ye dono cheezein program ke chalne par asar nahi dalti, sirf user ki rehnumai ke liye hain — lekin professional program ki pehchan yehi chhoti rehnumaiyan hoti hain.

```python
    parser.add_argument(
        "--file",
        default=DEFAULT_DATA_FILE,
        help=f"Path to the data file (default: {DEFAULT_DATA_FILE})",
    )
```

Parser ko pehla option sikhaya jata hai: `--file`. Ye **sab commands se pehle** lagne wala aam (global) option hai, jis se user bata sakta hai ke data kis file mein rakha jaye. `default=DEFAULT_DATA_FILE` matlab user na bataye to wohi `expenses.json` wali file istemal hogi. `help=...` wo madad wala text hai jo `--help` mein dikhega; us mein f-string se file ka asli naam khud aa jata hai.

```python
    sub = parser.add_subparsers(dest="command", required=True)
```

Ye is file ki sab se aham lines mein se ek hai. **Subparsers** argparse ki wo sahulat hai jis se ek program ke andar **kai commands** ban jati hain — jaise asal zindagi mein ek hi counter par alag alag kaam hote hain. `add_subparsers(...)` ek khali "commands wala khana" banata hai, jis mein aagay har command apni jagah banayegi. `dest="command"` ka matlab hai ke user ne jo command likhi, us ka naam `args.command` mein mehfooz ho jayega. `required=True` lafz bohat zaroori hai: is ka matlab hai user ko **koi na koi command dena lazmi hai** — khali `python main.py` chalane par argparse khud samjhaye ga ke command ghayab hai, program ajeeb tareeqay se crash nahi hoga.

```python
    p_add = sub.add_parser("add", help="Add a new expense")
```

Commands banna shuru hoti hain. `sub.add_parser("add", ...)` us khane mein `add` naam ki command ka apna chhota parser banata hai, jo `p_add` mein save hua. `help="Add a new expense"` wo line hai jo `--help` wali list mein is command ke samne dikhegi.

```python
    p_add.add_argument("--amount", required=True, help="Amount spent, e.g. 250 or 99.50")
    p_add.add_argument("--category", required=True, help="Category, e.g. Food")
    p_add.add_argument("--description", required=True, help="What the expense was for")
    p_add.add_argument("--date", default=None, help="Date in YYYY-MM-DD format (default: today)")
```

Ab `add` command ko us ke chaar options sikhahe jate hain. Har `add_argument` ek option ki tareef hai:
- `--amount`, `--category`, `--description` — teeno par `required=True` hai, matlab ye **lazmi** hain. User in mein se ek bhi bhool jaye to argparse khud rok kar bata dega ke konsa option reh gaya — ye check humein haath se nahi likhna parta. Har ek ke saath misal wala help text bhi hai.
- `--date` par `default=None` hai — ye **optional** hai. Na do to value `None` rahegi, aur yaad karein `cmd_add` mein yehi `None` dekh kar aaj ki tareekh laga di jati thi. Help text bhi yehi kehta hai: "default: today".
Is tareef ki khoobi ye hai ke command ki surat pehle se tay hai — ghalat ya adhuri command program ke logic tak pohanchti hi nahi.

```python
    p_add.set_defaults(func=cmd_add)
```

Bohat aham chhoti line. `set_defaults(func=cmd_add)` parser ko kehta hai: "Jab user `add` command chune, to yaad rakhna ke us ka kaam karne wala function `cmd_add` hai." Ye function ko **abhi nahi chalata**, sirf us ka naam-pata note kar leta hai. Aagay `main` mein `args.func(...)` likh kar yehi note hua function bulaya jayega. Isi tareeqay ki wajah se `main` ko lambi `if command == "add": ... elif ...` wali list nahi likhni parti — har command apna function apne saath bandh kar laati hai.

```python
    p_list = sub.add_parser("list", help="List expenses")
    p_list.add_argument("--month", default=None, help="Only show this month, YYYY-MM")
    p_list.add_argument("--category", default=None, help="Only show this category")
    p_list.set_defaults(func=cmd_list)
```

`list` command bhi bilkul usi andaz mein banti hai: apna parser `p_list`, phir us ke do options aur aakhir mein apne function `cmd_list` se bandhan. Farq ye hai ke is ke dono options (`--month`, `--category`) **optional** hain — `default=None` — kyun ke ye sirf filter hain: na do to tamam kharchay dikhte hain, do to chhan kar dikhte hain. Yaad karein `cmd_list` mein yehi do `None` wale check (`if args.month:` waghera) istemal hue thay.

```python
    p_delete = sub.add_parser("delete", help="Delete an expense by its ID")
    p_delete.add_argument("--id", required=True, type=int, help="ID of the expense to delete")
    p_delete.set_defaults(func=cmd_delete)
```

`delete` command: is ka sirf ek option hai `--id`, lazmi (`required=True`). Is line mein ek nayi cheez hai: **`type=int`**. Ye argparse ko kehta hai ke user jo value de, usay khud **poora number (int) bana kar** do. Misal user `--id 3` likhe to terminal se hamesha text aata hai `"3"`, lekin `type=int` ki wajah se `args.id` mein number `3` milega. Agar user `--id abc` likh de, to argparse wahin ghalti bata dega — hamare code tak ghalat cheez pohanchay gi hi nahi. Aakhir mein function bandhan: `cmd_delete`.

```python
    p_summary = sub.add_parser("summary", help="Show totals and a monthly / category summary")
    p_summary.add_argument("--month", default=None, help="Month to summarise, YYYY-MM (default: all months)")
    p_summary.set_defaults(func=cmd_summary)
```

`summary` command: ek hi optional option `--month`. Na do to overall summary (default ka lafz help mein bhi likha hai), do to sirf us month ki. Function bandhan `cmd_summary` ke saath.

```python
    p_categories = sub.add_parser("categories", help="Show suggested and used categories")
    p_categories.set_defaults(func=cmd_categories)
```

`categories` command sab se saada hai — is ka koi option hi nahi, is liye sirf parser bana aur function (`cmd_categories`) bandh diya. Commands ki factory yahan khatam.

```python
    return parser
```

Poora tayyar parser wapas bhej diya. Note karein is function ne koi command **chalayi nahi** — sirf naksha banaya hai, bilkul wese jese form chhapna ek kaam hai aur form bharna doosra.

```python
def main(argv=None) -> int:
```

Ab file ka sab se aakhri aur sab se aham function: `main`. Yehi wo function hai jisay `main.py` bulata hai. `argv=None` ek khaas sahulat hai: aam tor par `None` rehta hai, lekin test karte waqt program ko command ki jagah list haath se di ja sakti hai (jaise `main(["add", "--amount", "250", ...])`). `-> int` kehta hai jawab exit code hoga.

```python
    parser = build_parser()
    args = parser.parse_args(argv)
```

Do lines mein poori command samajh li gayi:
- Pehli line `build_parser()` se naksha mangwaya.
- Doosri line `parser.parse_args(argv)` asal terminal wali line ko us nakhsay par parhti hai. `argv` None ho to argparse khud terminal (`sys.argv`) se command utha leta hai. Parhne ke baad har option ek naam ke saath `args` object mein mil jata hai: `args.amount`, `args.category`, `args.date`, aur sab se aham — `args.func`, wo function jo chuni gayi command ke saath bandha gaya tha. Agar command ghalat ya adhuri ho, to argparse **yahi par** madad wala message dikha kar program ko izzat se band kar deta hai — hamare logic ko takleef hi nahi hoti.

```python
    store = ExpenseStore(args.file)
```

Ab data wala store banta hai: `ExpenseStore` class ka object, us file ke rastay ke saath jo user ne `--file` mein di (ya default `expenses.json`). Dhyaan dein abhi file **parhi nahi gayi** — sirf store tayyar hua hai; parhna tab hoga jab command wala function `load_all` ya `add` bulayega.

```python
    try:
        return args.func(args, store)
```

Ab asal command chalti hai — aur ye do lines poore design ka khulasa hain. `args.func` mein wohi function hai jo chuni gayi command ke saath bandha tha (add hai to `cmd_add`, list hai to `cmd_list`, waghera). Usay do cheezein de kar bulaya gaya: `args` (saare options) aur `store` (data wala). Jo exit code wo function wapas karega, wohi `return` se `main` ka jawab ban jayega aur `main.py` mein wohi number SystemExit ko jayega. Ye sab `try` ke andar hai kyun ke neeche us ki ghalti pakarni hai.

```python
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
```

Agar command chalte hue kahin se **ValueError** aaya — aur yaad karein, hamari saari checking wali ghaltiyan ValueError hi hain: ghalat raqam neeche `models.py` se, ghalat tareekh wahan se, kharab data file `storage.py` se — to ye `except` usay ek hi jagah pakar leta hai. `as exc` ghalti ko `exc` naam de deta hai taake us ka message istemal ho sake. Message `Error: ...` ki surat mein **stderr** par print hota hai (wohi error wali khaas jagah, `cmd_delete` wali tarah), aur `return 1` ghalti wala exit code deta hai. Is ek hisse ki wajah se poore program mein har jagah alag alag error sambhalne ki zaroorat nahi pari — **saari ghaltiyon ka ek hi ilaj yahan likha hai**, aur user ko kabhi Python ka lamba crash wala text (traceback) nazar nahi aata, sirf saaf ek line ka message milta hai.

```python
if __name__ == "__main__":
    raise SystemExit(main())
```

File ki aakhri do lines waisa hi andaz hai jo `main.py` mein tha: agar **ye file seedha chalayi jaye** (koi aisa to nahi karta aam tor par, lekin ho sakta hai) to `main()` chala kar us ke exit code ke saath band ho jao. Aur agar ye file import hui hai (jaise `main.py` karta hai), to ye hissa nahi chalega — sirf functions dastiyab honge. Is se file do suraton mein sahi rehti hai.

---

# Tests — pehle ye samajh lein "test" hota kya hai

Upar wali teen files (`test_models.py`, `test_storage.py`, `test_analytics.py`) program ka hissa **nahi** hain jo user chalata hai. Ye **khud-kar check-up** hain: chhote chhote programs jo asal code ko mukhtalif values de kar dekhte hain ke jawab wohi aata hai jo aana chahiye. Misal: "total nikalne wale function ko ye 4 kharchay do — kya jawab 2450 hi aata hai?"

Is se faida ye hota hai ke kal ko aap code mein koi tabdeeli karein aur galti se kuch tor dein, to tests foran bata denge "falana hisaab galat ho gaya" — bajaye is ke ke user baad mein shikayat kare.

Teeno files Python ki tayyar `unittest` library istemal karti hain. Kuch alfaz har jagah aayenge, pehle samajh lein:
- `class Test...(unittest.TestCase):` — teston ka ek group. `unittest.TestCase` se ye class wo saari sahulatein virasat mein leti hai jin se check hote hain.
- `def test_...` — har wo function jis ka naam `test_` se shuru ho, ek alag test hai. Library khud inhein dhund kar ek ek chala deti hai.
- `self.assertEqual(a, b)` — **check karo ke a aur b barabar hain**. Barabar na hon to test FAIL ho jata hai aur library bata deti hai ke ummeed kya thi aur mila kya.
- `self.assertTrue(x)` / `self.assertFalse(x)` — check karo ke jawab sach (True) / jhooth (False) hai.
- `with self.assertRaises(ValueError):` — ye ulta check hai: is ke andar wali line se **ValueError ghalti aani hi chahiye**. Agar ghalti aayi to test PASS, na aayi to FAIL. Ghalat input walay code ko test karne ka yehi tareeqa hai.

---

# File 7: `tests/test_models.py`

**Is file ka kaam:** Ye `models.py` ko test karti hai — yani raqam aur tareekh ki checking (`validate_amount`, `validate_date`) aur `Expense` class ke usool: khali category manzoor nahi, month sahi nikalta hai ya nahi, aur object dictionary ban kar wapas object ban sakta hai ya nahi.

```python
import unittest

from expense_tracker.models import Expense, validate_amount, validate_date
```

Do imports: `unittest` library, aur apne `models` se wo teen cheezein jo test hon gi — `Expense` class aur do validation functions. Jo cheez test karni ho, pehle usay mangwana parta hai.

```python
class TestValidation(unittest.TestCase):
```

Teston ka group `TestValidation` banta hai. Is file ke saare tests isi class ke andar hain.

```python
    def test_valid_amount(self):
        self.assertEqual(validate_amount("99.5"), 99.5)
        self.assertEqual(validate_amount(250), 250.0)
```

Pehla test: **sahi raqam theek se badalti hai ya nahi**. Do check hain:
- Text wali raqam `"99.5"` de kar dekha — jawab float `99.5` aana chahiye.
- Number `250` de kar dekha — jawab `250.0` (float surat mein) aana chahiye.
Dono suratein is liye check ki gayi kyun ke asal program mein raqam kabhi terminal se text ban kar aati hai aur kabhi code ke andar se number ban kar.

```python
    def test_amount_must_be_positive(self):
        for bad in (0, -5, "-1"):
            with self.assertRaises(ValueError):
                validate_amount(bad)
```

Test: **zero ya negative raqam par ghalti aani chahiye**. `for bad in (0, -5, "-1"):` wala loop teen kharab values ek ek karke chalata hai — zero, negative number, aur negative text. Har dafa `assertRaises(ValueError)` ke andar `validate_amount` bulaya gaya: teeno dafa ghalti aayi to test pass. Ek loop mein teen suratein check karna code bachane ka tareeqa hai.

```python
    def test_amount_must_be_a_number(self):
        with self.assertRaises(ValueError):
            validate_amount("abc")
```

Test: **jo cheez number ban hi nahi sakti** (`"abc"`) us par bhi ValueError aaye. Ye wala case alag test mein is liye hai kyun ke ye doosri qisam ki ghalti hai — upar wala "number hai magar ghalat hai" tha, ye "number hai hi nahi" hai.

```python
    def test_valid_date(self):
        self.assertEqual(validate_date("2026-10-05"), "2026-10-05")
```

Test: sahi tareekh `"2026-10-05"` do, to wohi saaf surat mein wapas mile.

```python
    def test_invalid_date(self):
        for bad in ("05-10-2026", "2026-13-01", "not-a-date", ""):
            with self.assertRaises(ValueError):
                validate_date(bad)
```

Test: **chaar qisam ki ghalat tareekhon** par ghalti aani chahiye. Har misal ek alag galti dikhati hai:
- `"05-10-2026"` — tareekh sahi hai magar **format ulta** hai (din pehle).
- `"2026-13-01"` — format sahi lagta hai magar **13wan maheena hota hi nahi**.
- `"not-a-date"` — bekaar text.
- `""` — bilkul khali.
Chaaroon par ValueError aaye to pass. Ye misalein soch samajh kar chuni gayi hain — achhe test wohi hote hain jo har qisam ki galti ko pakrein.

```python
    def test_expense_rejects_empty_category(self):
        with self.assertRaises(ValueError):
            Expense(id=1, amount=10, category="  ", description="x", date="2026-10-01")
```

Test: **khali category wala Expense banna hi nahi chahiye**. Yahan `category="  "` di gayi hai — sirf spaces. Yaad karein `models.py` mein `__post_init__` pehle `.strip()` se spaces hatata hai, phir khali honay par ghalti phenkta hai. Ye test bilkul usi usool ko pakarta hai: spaces wali category asal mein khali category hi hai. Agar kal ko koi wo check hata de, to ye test foran fail ho kar bata dega.

```python
    def test_expense_month_property(self):
        e = Expense(id=1, amount=10, category="Food", description="x", date="2026-10-01")
        self.assertEqual(e.month, "2026-10")
```

Test: **month property** sahi kaam karti hai ya nahi. Ek Expense banaya jis ki tareekh `"2026-10-01"` hai, phir check kiya ke `e.month` (bina brackets ke — property hai) `"2026-10"` deta hai. Wahi slicing wali line (`self.date[:7]`) yahan imtehan de rahi hai.

```python
    def test_expense_round_trip_dict(self):
        e = Expense(id=3, amount=12.5, category="Food", description="Tea", date="2026-10-01")
        self.assertEqual(Expense.from_dict(e.to_dict()), e)
```

Test ka naam hai **round trip** — ana jana. Ek kharcha banaya (id 3, 12.5 rupay, "Tea"), usay `e.to_dict()` se dictionary banaya, phir `Expense.from_dict(...)` se wapas object banaya, aur check kiya ke naya object **bilkul asal jaisa** hai. Ye test bohat aham hai kyun ke file mein save karna aur wapas parhna bilkul yehi ana jana hai — agar raaste mein koi cheez badal jaye (raqam, tareekh), to data kharab ho jayega, aur ye test usay pakar lega.

```python
if __name__ == "__main__":
    unittest.main()
```

Teeno test files ke aakhir mein yehi do lines hain. Matlab: agar **ye test file seedha chalayi jaye** (`python -m unittest` ki bajaye seedha `python tests/test_models.py`), to `unittest.main()` saare test dhund kar chala de. Warna import honay par kuch nahi hoga.

---

# File 8: `tests/test_storage.py`

**Is file ka kaam:** Ye `storage.py` ko test karti hai — file mein add karna, wapas parhna, ids ka barhna, delete karna, aur kharab file par saaf ghalti ana. Ek khaas baat: ye tests **asli file istemal nahi karte**. Har test ke liye ek aarzi (temporary) folder banta hai jo test ke baad delete ho jata hai — taake tests chalane se user ka asal kharchon wala data kabhi kharab na ho.

```python
import tempfile
import unittest
from pathlib import Path

from expense_tracker.storage import ExpenseStore
```

Imports: `tempfile` — aarzi folders/files banane wali library. `unittest` — test library. `Path` — rastay sambhalne ke liye. Aur apni `storage` file se `ExpenseStore` class, jo asal cheez hai jo test hogi.

```python
class TestExpenseStore(unittest.TestCase):
```

Test group: `TestExpenseStore`.

```python
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.file = Path(self.tmp.name) / "expenses.json"
        self.store = ExpenseStore(self.file)
```

`setUp` unittest ka khaas function hai jo **har test se pehle khud bakhud chalta hai** — yani har test ko bilkul nayi, saaf surat milti hai. Teen kaam hote hain:
- `tempfile.TemporaryDirectory()` ek naya aarzi folder banata hai, `self.tmp` mein mehfooz.
- Us folder ke andar `expenses.json` ka rasta banaya gaya — `Path(self.tmp.name) / "expenses.json"`. Note karein `/` yahan taqseem nahi hai; Path ke saath `/` ka matlab hai "is ke andar ye file joro".
- Uss rastay ke saath ek naya `ExpenseStore` bana kar `self.store` mein rakh diya, taake har test usi ko istemal kare.

```python
    def tearDown(self):
        self.tmp.cleanup()
```

`tearDown` is ka ulta hai: **har test ke baad** chalta hai. `self.tmp.cleanup()` aarzi folder ko us ke andar ki file samet delete kar deta hai. Is safai ki wajah se tests sou dafa bhi chalein, computer mein kachra jama nahi hota. `setUp`/`tearDown` ki ye jodi har test ko doosro se alag (isolated) rakhti hai — ek test ka data doosre ko asar nahi karta.

```python
    def test_missing_file_loads_empty(self):
        self.assertEqual(self.store.load_all(), [])
```

Test: file **hai hi nahi** (aarzi folder khali hai), phir bhi `load_all()` crash ki bajaye khali list `[]` de. Ye bilkul wahi `_read_raw` wala check hai jo file na honay par khali khaaka deta tha — program ki pehli run wali surat ka imtehan.

```python
    def test_add_and_load(self):
        added = self.store.add(250, "Food", "Lunch", "2026-10-05")
        self.assertEqual(added.id, 1)
        loaded = self.store.load_all()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].description, "Lunch")
        self.assertEqual(loaded[0].amount, 250.0)
```

Test: **add karna aur wapas parhna** — storage ka sab se bunyadi kaam. Pehle ek kharcha add kiya (250, Food, Lunch). Phir chaar check:
- Add se wapas mile kharchay ki id `1` hai — pehle kharchay ko pehla number mila.
- `load_all()` dobara parhne par list mein **kul 1** kharcha hai.
- Us pehle kharchay `loaded[0]` ki description `"Lunch"` hi hai (list mein `[0]` ka matlab hai pehli cheez — computer ginti zero se shuru karta hai).
- Aur us ki raqam `250.0` hai.
Agar save ya load mein kuch bhi ulta seedha hota, in mein se koi check fail ho jata.

```python
    def test_ids_increase(self):
        first = self.store.add(10, "Food", "a", "2026-10-01")
        second = self.store.add(20, "Food", "b", "2026-10-02")
        self.assertEqual((first.id, second.id), (1, 2))
```

Test: **ids barhti jani chahiye, dohrani nahi**. Do kharchay add kiye, phir ek hi check mein dono ki ids ka jora `(first.id, second.id)` asal joray `(1, 2)` se milaya. Ye wahi `next_id` wali mehnat hai jo `storage.py` mein thi — agar wo line ghayab ho, doosri id bhi 1 aa jayegi aur ye test pakar lega.

```python
    def test_add_rejects_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.store.add(-10, "Food", "Lunch", "2026-10-05")

    def test_add_rejects_invalid_date(self):
        with self.assertRaises(ValueError):
            self.store.add(10, "Food", "Lunch", "05/10/2026")
```

Do chhote tests, ek hi baat ki do suratein: **store se add karte waqt bhi ghalat data rukna chahiye**. Pehle mein raqam `-10` (negative), doosre mein tareekh `"05/10/2026"` (ghalat format, slashon wali). Dono par ValueError aana chahiye. Ye is liye aham hai kyun ke ye saabit karta hai ke `models.py` wali checking store ke zariye bhi kaam karti hai — koi peeche ke darwazay se ghalat data nahi ghus sakta.

```python
    def test_delete_existing(self):
        added = self.store.add(10, "Food", "a", "2026-10-01")
        self.assertTrue(self.store.delete(added.id))
        self.assertEqual(self.store.load_all(), [])
```

Test: **jo kharcha hai, wo delete ho**. Pehle ek kharcha add kiya, phir usi ki mili hui id se delete kiya:
- `assertTrue(...)` check karta hai ke delete ka jawab True aaya (kharcha mil kar mita).
- Phir `load_all()` se dobara parh kar dekha ke list **waqai khali** hai — sirf jawab par bharosa nahi, asal natija bhi dekha. Ye dohra check achhe test ki nishani hai.

```python
    def test_delete_missing_returns_false(self):
        self.assertFalse(self.store.delete(999))
```

Test: **jo id hai hi nahi (999), usay delete karne par jawab False aaye**, crash na ho. Khali store par 999 mitana matlab "nahi mila" — aur CLI bilkul isi False par "no expense with ID 999 was found" wala message dikhata hai.

```python
    def test_data_survives_new_store_instance(self):
        self.store.add(10, "Food", "a", "2026-10-01")
        reloaded = ExpenseStore(self.file).load_all()
        self.assertEqual(len(reloaded), 1)
```

Test ka naam hi is ka maqsad hai: **data naye store par bhi zinda rahe**. Ek kharcha add kiya, phir **bilkul naya** `ExpenseStore` object banaya usi file ke saath aur us se parha — jawab mein 1 kharcha mila. Ye bilkul asal zindagi ki surat hai: program band karke dobara kholna matlab naya store object banta hai, lekin file wala data waisa ka waisa milna chahiye. Agar data sirf yaad-dasht (memory) mein rehta, file mein na likha jata, to ye test fail ho jata.

```python
    def test_corrupted_file_raises_helpful_error(self):
        self.file.write_text("{ not json", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.store.load_all()
```

Test: **kharab file par saaf ghalti aaye**. Pehle jaan boojh kar file mein bigra hua text `"{ not json"` likh diya — ye sahi JSON nahi hai. Phir `load_all()` bulaya aur check kiya ke ValueError aati hai. Ye wahi surat hai jo `storage.py` mein `json.JSONDecodeError` ko pakar kar asaan message wale ValueError mein badalti thi. "Helpful error" naam mein is liye hai ke ghalti aani chahiye, magar dostana wali.

```python
if __name__ == "__main__":
    unittest.main()
```

Wohi aakhri do lines: file seedha chalayi jaye to tests chal jayein.

---

# File 9: `tests/test_analytics.py`

**Is file ka kaam:** Ye `analytics.py` ke hisaab kitab ko test karti hai — total, month/category ki chhantai, category totals ki tartib, aur month ki summary. Is file ki khaas baat: hisaab check karne ke liye pehle ek **tayyar namuna list** banayi jati hai jis ka har jawab pehle se maloom hai — jaise imtehan mein wo sawal jinka jawab teacher ko pehle se pata ho.

```python
import unittest

from expense_tracker.analytics import (
    all_categories,
    category_totals,
    filter_by_category,
    filter_by_month,
    monthly_summary,
    total_amount,
)
from expense_tracker.models import Expense
```

Imports: `unittest`, phir `analytics` file ke **saare chhe (6) functions** — is file mein har function ka test hai, is liye sab mangwaye — aur `models` se `Expense` class, kyun ke namuna kharchay banane ke liye wohi chahiye.

```python
def make_expenses():
    return [
        Expense(id=1, amount=450, category="Food", description="Groceries", date="2026-10-02"),
        Expense(id=2, amount=200, category="Transport", description="Rickshaw", date="2026-10-03"),
        Expense(id=3, amount=300, category="Food", description="Lunch", date="2026-10-05"),
        Expense(id=4, amount=1500, category="Education", description="Book", date="2026-09-15"),
    ]
```

Ye ek helper function hai (ye test nahi hai, is ka naam `test_` se shuru nahi hota) jo **chaar namuna kharchay** bana kar deta hai. Har test yehi list istemal karega taake har dafa naye kharchay na likhne parein. In chaar ko ghoor se dekhein — ye be-tarteeb nahi chune gaye:
- Food ke **do** kharchay hain (450 + 300 = 750) — taake jorna aur category ka total check ho sakay.
- Ek Transport (200), ek Education (1500) — Education sab se bara hai, taake **sort ki tartib** check ho sakay.
- Teen kharchay **October 2026** ke hain aur ek **September** ka — taake month ki chhantai check ho sakay (October ka total 450+200+300 = 950, kul total 2450).
Har test ke jawab inhi numbers se nikleinge.

```python
class TestAnalytics(unittest.TestCase):
    def setUp(self):
        self.expenses = make_expenses()
```

Test group `TestAnalytics` banta hai. Is dafa `setUp` bohat chhota hai: har test se pehle `make_expenses()` chala kar taza list `self.expenses` mein rakh di jati hai. Har test ko apni saaf copy milti hai — ek test list mein kuch badal bhi de to doosra test mutasir nahi hota.

```python
    def test_total_amount(self):
        self.assertEqual(total_amount(self.expenses), 2450.0)
        self.assertEqual(total_amount([]), 0.0)
```

Test: kul total. Pehla check: chaaron kharchon ka total `2450.0` (450+200+300+1500) aana chahiye. Doosra check bhi utna hi aham hai: **khali list** ka total `0.0` aaye, crash na ho. Khali wali surat (edge case) test karna aksar bhool jate hain — asal program mein naya user bilkul khali list ke saath hi shuru karta hai.

```python
    def test_filter_by_month(self):
        october = filter_by_month(self.expenses, "2026-10")
        self.assertEqual(len(october), 3)
        self.assertTrue(all(e.month == "2026-10" for e in october))
```

Test: month ki chhantai. `"2026-10"` se filter kiya:
- Pehla check: chhani hui list mein **3** kharchay hain (September wala ek bahir reh gaya).
- Doosra check zyada mazboot hai: `all(...)` poochta hai "kya list ki **har** cheez par ye baat sach hai ke us ka month `2026-10` hi hai?" Agar ghalti se September wala bhi andar aa gaya ho, to sirf tadaad wala check to pehle hi fail hota — lekin agar koi aur kharcha nikal kar September wala ghus gaya ho (tadaad phir bhi 3), to ye doosra check pakar lega. `assertTrue` is purey jawab ko sach honay par pass karta hai.

```python
    def test_filter_by_category_is_case_insensitive(self):
        food = filter_by_category(self.expenses, "food")
        self.assertEqual(len(food), 2)
```

Test ka naam hi is ka maqsad hai: **category wali chhantai chhote baray harfon ka farq nahi karti**. Ghoor karein — filter `"food"` (chhote harf) se kiya gaya, jabke list mein category `"Food"` (bara F) likhi hai. Phir bhi jawab **2** aana chahiye (dono Food wale kharchay). Ye seedha `filter_by_category` mein lage `.lower()` walay hisse ka imtehan hai — wo hatayen to ye test fail.

```python
    def test_category_totals_sorted_highest_first(self):
        totals = category_totals(self.expenses)
        self.assertEqual(totals["Food"], 750.0)
        self.assertEqual(totals["Education"], 1500.0)
        self.assertEqual(list(totals)[0], "Education")
```

Test: category totals **aur un ki tartib**. Teen check:
- Food ka total `750.0` — yani ek category ke do kharchay (450+300) sahi joray.
- Education ka total `1500.0`.
- Teesra check tartib ka hai: `list(totals)[0]` — dictionary ko list ki surat mein dekh kar us ki **pehli** cheez — `"Education"` honi chahiye, kyun ke us ka total (1500) sab se bara hai. Ye wahi `sorted(..., reverse=True)` wali line hai jo yahan apna rang dikha rahi hai.

```python
    def test_monthly_summary(self):
        summary = monthly_summary(self.expenses, "2026-10")
        self.assertEqual(summary["count"], 3)
        self.assertEqual(summary["total"], 950.0)
        self.assertEqual(summary["average"], round(950 / 3, 2))
        self.assertEqual(summary["by_category"]["Food"], 750.0)
```

Test: October ki poori summary report. `monthly_summary` se dictionary mili, aur us ke har khaanay ko ek ek karke check kiya:
- `count` = 3 (October ke teen kharchay).
- `total` = 950.0 (450+200+300 — September wala 1500 is mein **nahi** hai; yehi is test ki jaan hai).
- `average` = 950 ko 3 par taqseem karke 2 decimal tak round ki hui value. Yahan jawab ko bhi `round(950 / 3, 2)` likh kar hisaab se nikala gaya hai, taake test likhne wale ko decimal yaad na karna pare — aur taake test aur code dono ek hi usool par chal rahe hon.
- `by_category` ke andar Food ka total 750.0 — yani summary ke andar wali category wali report bhi sahi hai.

```python
    def test_monthly_summary_empty_month(self):
        summary = monthly_summary(self.expenses, "2026-12")
        self.assertEqual(summary["count"], 0)
        self.assertEqual(summary["total"], 0.0)
        self.assertEqual(summary["average"], 0.0)
```

Test: **khali maheena** — December 2026, jismein koi kharcha hai hi nahi. Teen check: count 0, total 0.0, average 0.0. Ye wohi surat hai jahan average nikalte waqt zero par taqseem wala crash ho sakta tha — `monthly_summary` wali `if count else 0.0` hifazat ka asal imtehan yehi test hai. Is test ka pass hona matlab: naya user pehle din summary mang le to program izzat se "0" dega, crash nahi hoga.

```python
    def test_all_categories(self):
        self.assertEqual(all_categories(self.expenses), ["Education", "Food", "Transport"])
```

Aakhri test: categories ki list. Jawab mein **teen** naam ek ek dafa hone chahiye, alphabetical tartib mein: Education, Food, Transport. Note karein Food list mein do dafa tha, magar jawab mein **ek** dafa hai — ye wahi set wali khoobi hai jo duplicates hatati hai. Tartib bhi check ho rahi hai: agar sort na hota to jawab kisi aur tartib mein aa kar fail ho jata.

```python
if __name__ == "__main__":
    unittest.main()
```

Wohi aakhri do lines — teesri test file bhi is par khatam.

**Teeno test files mila kar kul 24 tests hain: `test_models.py` mein 8, `test_storage.py` mein 9, aur `test_analytics.py` mein 7.** Teeno chalao to sub ka jawab "OK" aana chahiye — matlab har check pass.

---

# Poora program ek saath kaise chalta hai

Ab saari files ko jod kar dekhte hain. User terminal mein ye command likhta hai:

```
python main.py add --amount 750 --category Food --description "Lunch"
```

Note karein user ne `--date` nahi diya. Ab dekhein peeche kya hota hai, qadam ba qadam:

**Qadam 1 — `main.py` se shuruaat.**
`python main.py` likhte hi `main.py` chalti hai. Us ki `if __name__ == "__main__":` wali shart sach hoti hai (file seedha chalayi gayi hai), to `raise SystemExit(main())` wali line `cli.py` se import kiye hue `main()` ko bula deti hai. Kaam ab `cli.py` ke hawale.

**Qadam 2 — `cli.py` ka `main()` command ko parhta hai.**
`main()` pehle `build_parser()` se commands ka naksha banata hai. Phir `parser.parse_args(argv)` terminal wali line ko tod kar samajhta hai:
- Command hai `add` — aur nakhsay mein `add` ke saath `cmd_add` function bandha hua tha, to `args.func` mein `cmd_add` mehfooz ho jata hai.
- `args.amount` mein `"750"` milta hai (terminal se har cheez pehle text ban kar ati hai).
- `args.category` mein `"Food"`, `args.description` mein `"Lunch"`.
- `args.date` mein `None` — kyun ke user ne date di hi nahi, aur nakhsay mein date ka default None tha.
- `args.file` mein default wali `"expenses.json"` — user ne `--file` bhi nahi diya tha.

**Qadam 3 — Store banta hai.**
`store = ExpenseStore(args.file)` — `storage.py` ki class ka object banta hai, us ka `__init__` chalta hai aur file ka rasta `Path("expenses.json")` ban kar save ho jata hai. Abhi file khuli nahi, sirf dukaan (store) tayyar hai.

**Qadam 4 — Command wala function chalta hai, `try` ke andar.**
`return args.func(args, store)` — yani asal mein `cmd_add(args, store)` bulaya jata hai. Ye saara amal `try` ke andar hai, taake kahin se ValueError aaye to `main()` ke `except` wala hissa usay pakar kar saaf message de (is misal mein sab theek hoga, to wo hissa nahi chalega).

**Qadam 5 — `cmd_add` tareekh tay karta hai.**
`cmd_add` ki pehli line: `expense_date = args.date or date_cls.today().isoformat()`. `args.date` None hai, yani "khali", to `or` ke doosri taraf wala hissa istemal hota hai — `date_cls.today()` se aaj ki tareekh milti hai aur `.isoformat()` usay aaj ki date ke `YYYY-MM-DD` wale text mein badal deta hai. Misal ke tor par aaj `2026-10-31` hai to `expense_date` ban jata hai `"2026-10-31"`.

**Qadam 6 — `cmd_add` store ko kaam deta hai.**
`store.add(args.amount, args.category, args.description, expense_date)` bulaya jata hai — yani raqam `"750"`, category `"Food"`, tafseel `"Lunch"`, tareekh `"2026-10-31"` store ke hawale. Kaam ab `storage.py` mein chala jata hai.

**Qadam 7 — `storage.py` ka `add` pehle purani file parhta hai.**
`add` ki pehli line `data = self._read_raw()` hai. `_read_raw` dekhta hai ke `expenses.json` file hai ya nahi:
- Agar pehli dafa program chal raha hai aur file nahi hai, to khali khaaka `{"next_id": 1, "expenses": []}` wapas aa jata hai.
- Agar file hai, to `with` wale tareeqay se khol kar `json.load` se us ka data dictionary ban kar aa jata hai. Misal ke tor par pehle se 4 kharchay hon to `next_id` 5 hoga.

**Qadam 8 — `models.py` mein Expense object banta hai aur check hota hai.**
Store ab `Expense(id=..., amount="750", category="Food", description="Lunch", date="2026-10-31")` banata hai — id ke liye dictionary ka `next_id` istemal hota hai. Object bante hi `models.py` ka `__post_init__` khud bakhud chalta hai:
- `validate_amount("750")` — `float("750")` se `750.0` banta hai, zero se bara hai, `round(..., 2)` ke baad `750.0` hi rehta hai. Raqam saaf ho kar object mein beth jati hai. (Agar user `--amount -750` ya `--amount abc` deta, to bilkul yahin ValueError aa jata, aur agla koi qadam na uthta — file bhi kharab na hoti, aur `main()` ka `except` user ko saaf message de deta: `Error: Amount must be greater than zero.`)
- `validate_date("2026-10-31")` — `datetime.strptime` check karta hai ke tareekh sahi format aur asl mein maujood tareekh hai. Theek nikalti hai, to wohi text wapas `self.date` mein reh jata hai.
- Category aur description par `.strip()` se fazool spaces saaf hote hain — `"Food"` aur `"Lunch"` pehle se saaf hain, aur khali bhi nahi hain, to dono check pass.

Ab hamare paas ek **pakka, check shuda Expense object** hai.

**Qadam 9 — Kharcha dictionary mein jata hai aur `next_id` barhta hai.**
Store `expense.to_dict()` se object ko dictionary banata hai — `asdict` har field ko naam-value bana deta hai: `{"id": 5, "amount": 750.0, "category": "Food", "description": "Lunch", "date": "2026-10-31"}` (id misal ke tor par 5 liya hai). Phir `.append(...)` se ye dictionary `data["expenses"]` wali list ke aakhir mein lag jati hai. Us ke baad `data["next_id"] = expense.id + 1` se agli id tayyar ho jati hai — 5 istemal hua, to agli dafa 6 milega.

**Qadam 10 — File mein mehfooz ho jata hai.**
`self._write_raw(data)` chalta hai: pehle ye pakka hota hai ke file wala folder maujood hai (`mkdir` wali line), phir file `"w"` mode mein khulti hai aur `json.dump(data, f, indent=2)` poori updated dictionary ko saaf indentation ke saath file mein likh deta hai. `with` block khatam hotay hi file khud band ho jati hai. **Ab kharcha mehfooz hai** — program band karke kal kholo, to bhi ye kharcha file mein milega.

**Qadam 11 — Jawab wapas CLI ko jata hai.**
`add` function bana hua `expense` object wapas bhejta hai. `cmd_add` usay le kar tasdeeq wala message print karta hai:

```
Added expense #5: 750.00 [Food] Lunch on 2026-10-31
```

(Raqam `750.00` is liye nazar aayi kyun ke print mein `:.2f` wala format laga tha.) Phir `cmd_add` `return 0` karta hai — kamyabi ka code.

**Qadam 12 — Program izzat se band hota hai.**
`cmd_add` ka `0` `main()` mein `try` wali line se wapas aata hai — koi ValueError nahi aaya, to `except` wala hissa chalta hi nahi. `main()` wohi `0` wapas karta hai, aur `main.py` mein `raise SystemExit(0)` program ko band kar deta hai — exit code 0 ke saath, yani computer ko bhi pata chal jata hai ke sab theek raha.

**Ek line mein poora safar:**
Terminal ki command → `main.py` ne darwaza khola → `cli.py` ne command samjhi aur tareekh mukammal ki → `storage.py` ne purana register parha → `models.py` ne naya kharcha check karke banaya → `storage.py` ne register mein darj karke mehfooz kar diya → `cli.py` ne user ko tasdeeq dikhayi → program band.

Har file ne **sirf apna kaam** kiya: CLI ne hisaab nahi lagaya, models ne file nahi kholi, storage ne screen par kuch nahi likha, aur analytics is command mein to istemal hi nahi hua (wo `list` aur `summary` commands mein kaam aata hai). Code ko is tarah alag alag zimmedariyon mein baantna hi wo cheez hai jo is chhote se project ko ek "professional" project banati hai — aur viva ya interview mein agar ye safar aap apne alfaaz mein suna dein, to samajh jayen ke project asal mein aap ka apna ho gaya hai.
