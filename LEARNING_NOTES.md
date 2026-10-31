# Learning Notes — Personal Expense Tracker
### (Wasay ke liye — asaan Roman Urdu mein poori tafseel)

Ye notes tumhare liye hain, taake tum is project ko sirf "github par add" na karo,
balke waqai samjho bhi — aur kal ko koi teacher, dost ya interviewer pooche to
khud apni zubaan mein samjha bhi sako.

---

## 1. Ye project hai kya, aur kyun banaya?

Ye ek **Personal Expense Tracker** hai. Matlab: roz ke kharche (khana, kiraya,
rickshaw, kitaabein waghera) likhne ke liye ek chhota sa program.

Purana tareeqa ye tha ke banda copy par kharche likhta tha, phir mahine ke
aakhir mein hisaab lagana mushkil ho jata tha — kis cheez par kitne paise gaye,
pata hi nahi chalta tha.

Ye program wahi kaam computer se karwata hai:

- Kharcha add karo — kitne paise, kis cheez par (category), kis din
- Saare kharche list mein dekho
- Galat kharcha delete karo
- Mahine ki summary dekho — total kitna kharch hua, aur kis category par sab
  se zyada paisa gaya (masalan Food par 750, Education par 1500)

Ye **CLI application** hai. CLI ka matlab hai "Command Line Interface" —
matlab is mein buttons wali screen (GUI) nahi hai, tum terminal mein command
likhte ho aur program jawab deta hai. Chhote tools aur seekhne ke liye CLI
sab se acha pehla qadam hota hai, kyun ke saara focus code ki logic par hota
hai, design par nahi.

**Ek important baat:** data kahin internet par nahi jata. Saare kharche
tumhare apne computer ki ek file mein save hote hain. Program band karke
dobara kholo, data waisa hi milega. Program band honay se data zaya nahi
hota — isi ko computer ki duniya mein "persistence" kehte hain.

---

## 2. Project ki files — har file kya karti hai

Project ka folder is tarah bana hai:

```
week-01-project-01-expense-tracker/
│
├── main.py                    ← program yahan se start hota hai
├── expense_tracker/           ← ye asal code ka package (folder) hai
│   ├── __init__.py            ← is folder ko Python "package" banata hai
│   ├── models.py              ← ek kharche ki definition + checking (validation)
│   ├── storage.py             ← kharche file mein save / load karna
│   ├── analytics.py           ← hisaab kitaab (total, summary, category totals)
│   └── cli.py                 ← terminal commands (add, list, delete, summary)
├── tests/                     ← code ko check karne wale tests
│   ├── test_models.py
│   ├── test_storage.py
│   └── test_analytics.py
├── sample_data/
│   └── expenses.json          ← pehle se bhari hui misaal wali data file
├── requirements.txt           ← is project ko koi extra cheez install nahi karni
├── .gitignore                 ← git ko batata hai ke konsi files ignore karni hain
├── LICENSE                    ← MIT license — koi bhi code use kar sakta hai
└── README.md                  ← GitHub par dikhne wali project ki tafseel (English)
```

### Separation of concerns kya hota hai?

Har file ka **ek hi kaam** hai. Isi ko programming mein "separation of
concerns" kehte hain. Faida ye hai:

- Agar summary ka hisaab galat ho, tum seedha `analytics.py` khologe —
  poora project nahi dhoondna padega
- Agar file save na ho rahi ho, masla `storage.py` mein hoga
- Har hissa alag se test ho sakta hai

Ye bilkul waisa hi hai jese ek restaurant mein alag alag kaam hotay hain —
khana pakanay wala alag, bill bananay wala alag, samaan store karne wala
alag. Agar sab kaam ek hi banda kare to ghalti dhoondna mushkil ho jata hai.

Ab har file ko bari bari samjhte hain.

---

## 3. `models.py` — ek kharcha kya hota hai?

Ye file sab se basic sawal ka jawab deti hai: **"ek kharche mein kya kya
maloomat hoti hain?"**

Har kharche ke 5 hisse hain:

| Field | Matlab | Misaal |
|---|---|---|
| `id` | har kharche ka apna number | 1, 2, 3... |
| `amount` | kitne paise | 450.00 |
| `category` | kis qisam ka kharcha | Food |
| `description` | tafseel | Groceries |
| `date` | kis din | 2026-10-02 |

Code mein ye is tarah likha hai:

```python
@dataclass
class Expense:
    id: int
    amount: float
    category: str
    description: str
    date: str
```

### Dataclass kya hai?

Normal class banane mein bohat saara repeat wala code likhna padta hai
(`__init__`, waghera). `@dataclass` ek shortcut hai — Python khud wo
code bana deta hai. Tumhe sirf ye batana padta hai ke fields konse hain
aur unki type kya hai (`int`, `float`, `str`).

### Validation — checking kyun zaroori hai?

Agar user galat cheez likh de — masalan amount `-50` (minus wala kharcha
to hota hi nahi), ya date `05-10-2026` ki jagah ghalat format mein —
to program crash nahi hona chahiye, balkay politely bataye ke ghalti kya hai.

Isi liye `models.py` mein do helper functions hain:

- `validate_amount()` — check karta hai: kya ye number hai? kya zero se
  bara hai? Agar nahi, to `ValueError` error uthata hai saaf message ke saath
- `validate_date()` — check karta hai ke date theek `YYYY-MM-DD` format
  mein hai ya nahi, Python ke `datetime.strptime()` se

Aur `Expense` class mein `__post_init__` naam ka ek khaas function hai.
Ye object bante hi khud chal jata hai aur saari values check kar leta hai.
Matlab: **galat data wala Expense object ban hi nahi sakta.** Ye ek
bohat achi aadat hai — ghalti ko sab se pehle wale darwaze par hi rok do.

Ek aur chhoti si cheez: `month` naam ki **property** hai. Ye `date` mein se
sirf saal-mehina nikaal deti hai — `2026-10-02` se `2026-10`. Ye is liye
chahiye kyun ke monthly summary ke liye humein mahina chahiye hota hai.

`to_dict()` aur `from_dict()` — ye do functions Expense object ko
dictionary mein badalte hain aur wapas object bana dete hain. Ye is liye
chahiye kyun ke JSON file mein object seedha save nahi hota, dictionary
save hoti hai.

---

## 4. `storage.py` — data file mein kese save hota hai?

Is file ka kaam sirf ek hai: **kharche file se parhna aur file mein likhna.**

Data **JSON format** mein save hota hai. JSON ek saada text format hai jo
insaan bhi parh sakta hai aur computer bhi. File kholo to kuch is tarah
dikhti hai:

```json
{
  "next_id": 4,
  "expenses": [
    {"id": 1, "amount": 450.0, "category": "Food",
     "description": "Groceries", "date": "2026-10-02"}
  ]
}
```

### ExpenseStore class kese kaam karti hai — step by step

**Jab naya kharcha add hota hai:**

1. Pehle file parho (`_read_raw`)
2. Agar file maujood hi nahi, to khaali list se shuru karo — error mat do
3. Naya `Expense` object banao, usay next id do
4. Usay list mein shamil karo, aur `next_id` ek barha do
5. Poori file dobara likh do (`_write_raw`)

**Ek khaas baat — `next_id` kyun rakha?**
Har kharche ko apna alag number (id) chahiye, taake delete karte waqt
ye confusion na ho ke konsa wala delete karna hai. Agar id sirf list ki
length se banayein to delete ke baad number repeat ho sakta hai. `next_id`
file mein hi save rehta hai, is liye number kabhi repeat nahi hota.

**Jab kharcha delete hota hai:**

1. File parho
2. Us id ke ilawa baaki sab kharche rakho, wo wala nikaal do
3. Agar list ki tadaad kam hui, matlab delete ho gaya — file dobara likho
   aur `True` wapas bhejo. Agar tadaad waisi hi rahi, matlab wo id tha hi
   nahi — `False` wapas bhejo, taake CLI user ko bata sake ke
   "ye id mila hi nahi"

**Agar file kharab (corrupt) ho jaye?**
Agar koi file haath se edit karke bigaar de aur JSON kharab ho jaye, to
program ajeeb se error ki jagah saaf message deta hai:
*"Data file corrupted hai, usay theek karo ya delete karke fresh shuru karo."*
Isi ko **error handling** kehte hain — program ko har haal mein samajhdari
se behave karna chahiye.

File parhne/likhne ke liye Python ka `json` module aur `pathlib` ka `Path`
use hua hai. `Path` se file ke raaste (paths) handle karna asaan aur safe
hota hai.

---

## 5. `analytics.py` — hisaab kitaab kese hota hai?

Is file mein saare **calculations** hain. Khaas baat: is file ki functions
na file parhti hain, na screen par kuch print karti hain — bas list leti
hain aur jawab (result) wapas deti hain. Aisi functions ko "pure functions"
kehte hain, aur inhe test karna sab se asaan hota hai.

Har function kya karta hai:

- **`total_amount()`** — saare kharchon ki amounts jama kar do.
  Python ka `sum()` ek generator expression ke saath use hua hai:
  `sum(e.amount for e in expenses)`

- **`filter_by_month()`** — sirf usi mahine ke kharche rakho jo maanga gaya
  hai. Ye list comprehension se hota hai:
  `[e for e in expenses if e.month == month]`

- **`filter_by_category()`** — sirf ek category ke kharche. Yahan ek
  samajhdari ki gayi hai: `lower()` use karke check hota hai, taake user
  `Food` likhe ya `food` — dono chal jayein

- **`category_totals()`** — dictionary ka sab se acha use yahan samajh aata
  hai. Ek khaali dictionary lo, har kharche ke liye:
  - Agar us ki category dictionary mein pehle se hai, to amount jama kar do
  - Agar nahi hai, to nayi entry bana do starting amount ke saath

  Phir dictionary ko total ke hisaab se bari-se-chhoti tartib (descending
  sort) mein laga do, taake sab se bari category sab se pehle dikhe

- **`monthly_summary()`** — ek mahine ki poori report (report ko bhi ek
  dictionary ki shakal mein wapas deta hai): kitne kharche, total kitna,
  average kitna (total ÷ tadaad), aur category-wise totals. Agar mahine
  mein koi kharcha hi nahi, to average `0` aata hai — division-by-zero wala
  crash nahi hota, kyun ke pehle check lagaya gaya hai

- **`all_categories()`** — saari alag alag (unique) categories ki list.
  Yahan Python ka `set` use hua hai — set mein koi cheez dobara nahi aati,
  is liye duplicates khud khatam ho jate hain

---

## 6. `cli.py` — user command kese deta hai?

CLI wo hissa hai jo user se baat karta hai. Is ke liye Python ka
**`argparse`** module use hua hai — ye terminal ki command ko samajhne ka
standard tareeqa hai.

Command ki shakal aisi hoti hai:

```
python main.py add --amount 450 --category Food --description "Groceries"
│       │      │    └──────────────── options / details ────────────────┘
│       │      └ subcommand — karna kya hai?
│       └ file jo chalani hai
└ Python ko bulana
```

Program mein 5 subcommands hain: `add`, `list`, `delete`, `summary`,
`categories`.

### Ek command chalne ka poora safar — step by step

Misaal: tum ye likhte ho:

```bash
python main.py add --amount 450 --category Food --description "Groceries" --date 2026-10-02
```

Phir andar ye hota hai:

1. `main.py` chalta hai, wo `expense_tracker/cli.py` ke `main()` ko bulata hai
2. `argparse` command ko parh kar samajhta hai: command hai `add`, amount
   hai `450`, category hai `Food`, waghera. Ye saari values `args` naam ke
   object mein milti hain
3. `ExpenseStore` banta hai — usay bataya jata hai ke data file konsi hai
   (by default `expenses.json`; `--file` se badli ja sakti hai — aur yaad
   rakho, `--file` command se **pehle** likha jata hai)
4. `cmd_add()` function chalta hai. Agar date nahi di gayi, to aaj ki date
   khud le li jati hai (`date.today()`)
5. Store naya kharcha banata hai — is doran `models.py` ki validation
   chalti hai. Amount ya date galat ho to `ValueError` aata hai
6. Agar sab theek ho, to kharcha file mein save ho jata hai aur screen par
   confirmation aata hai: `Added expense #1: 450.00 [Food] Groceries on 2026-10-02`
7. Agar validation fail ho, to `main()` us error ko pakad (catch) kar
   saaf message print karta hai — `Error: Amount must be greater than zero.`
   — aur program exit code `1` ke saath band hota hai (exit code 0 ka matlab
   hota hai "sab theek hua", 1 ka matlab "ghalti hui")
8. `list` command data ko pehle date, phir id ke hisaab se sort karke ek
   saaf table ki shakal mein print karta hai

Ye flow samajhna sab se ahem hai — **har command isi pattern par chalti
hai: command parho → store se data lo/do → result print karo.**

---

## 7. Tests kya hain, aur kyun likhe gaye?

`tests/` folder mein **24 tests** hain. Test ek chhota sa code hota hai jo
check karta hai ke asal code sahi kaam kar raha hai ya nahi — khud bakhud,
baghair haath se chalaye.

Tests teen files mein hain:

- **`test_models.py`** — validation ki checking: minus amount reject hota
  hai ya nahi, galat date reject hoti hai ya nahi, khaali category reject
  hoti hai ya nahi, `month` property sahi hai ya nahi
- **`test_storage.py`** — file wale kaam: add karke wapas parho to milta
  hai, ids barhte hain, delete sahi hota hai, jo id hai hi nahi usay delete
  karne par sahi jawab aata hai, kharab (corrupt) file par saaf error aata
  hai. Yahan khaas baat: ye tests tumhari asal data file ko haath nahi
  lagate — `tempfile` se ek temporary file banti hai, test usi par hota
  hai, phir wo file khud delete ho jati hai
- **`test_analytics.py`** — hisaab ki checking: total sahi hai, month filter
  sahi hai, category totals sahi aur sahi order mein hain, khaali mahine
  ki summary mein crash nahi hota

### Tests ka faida kya hai?

Kal ko tum code mein koi change karo aur galti se kuch tor do, to tests
fauran bata denge ke kya toota. Bina tests ke, har change ke baad poora
program haath se dobara check karna padta hai. Professional developers
isi liye tests likhte hain — ye is project ki sab se professional aadat hai.

Sab tests Python ke built-in **`unittest`** framework se likhe hain, to
koi extra cheez install hi nahi karni padti.

---

## 8. Is project mein use hue Python concepts — ek nazar mein

| Concept | Kahan use hua | Asaan matlab |
|---|---|---|
| Class / Dataclass | `models.py` — `Expense` | ek cheez ki definition, jis ki copies (objects) banti hain |
| `__post_init__` | `models.py` | object bante hi khud chalne wali checking |
| Property | `models.py` — `month` | ek value jo doosri value se khud calculate ho |
| Dictionary | `analytics.py`, JSON data | `key: value` ki joriyon mein data rakhna |
| List comprehension | `analytics.py`, `storage.py` | ek line mein list ko filter / badalna |
| Set | `analytics.py` — `all_categories` | duplicates khud khatam karne wala collection |
| File I/O + JSON | `storage.py` | file parhna/likhna taake data mehfooz rahe |
| Error handling (`try/except`, `raise`) | `storage.py`, `cli.py` | ghalti par crash ki jagah saaf message |
| Functions & modules | har file | code ko chhote, saaf tukron mein baantna |
| Package (`__init__.py`) | `expense_tracker/` | kai modules ko ek group mein jodna |
| `argparse` | `cli.py` | terminal commands ko samajhna |
| `pathlib.Path` | `storage.py` | file ke raaste safe tareeqay se handle karna |
| Unit testing (`unittest`) | `tests/` | code ko khud bakhud check karna |
| Type hints (`int`, `str`, `float`) | har jagah | padhne wale ko batana ke value kis qisam ki hai |
| Exit codes | `cli.py` | 0 = kamyabi, 1 = ghalti — doosre programs bhi ye samajhte hain |

Ek aur baat khaas note karo: is project mein **koi external library
install nahi karni padti** (koi `pip install` nahi). Sab kuch Python ke
saath pehle se anay wali standard library se bana hai. Chhote project
ke liye ye acha faisla hai — kam cheezein, kam uljhan. `requirements.txt`
mein ye baat wazeh likhi bhi hai.

---

## 9. Program chalana kese hai — poori rehnumai

### Pehli shart

Computer mein Python 3.10 ya us se naya hona chahiye. Check karne ke liye:

```bash
python --version
```

Phir terminal mein project wale folder mein jao:

```bash
cd week-01-project-01-expense-tracker
```

### Roz ke commands

**Kharcha add karna:**
```bash
python main.py add --amount 450 --category Food --description "Groceries" --date 2026-10-02
```
Jawab ayega: `Added expense #1: 450.00 [Food] Groceries on 2026-10-02`
(`--date` na likho to aaj ki date khud lag jayegi.)

**Saare kharche dekhna:**
```bash
python main.py list
```

**Sirf ek mahine ya ek category ke kharche:**
```bash
python main.py list --month 2026-10
python main.py list --category Food
```

**Mahine ki summary:**
```bash
python main.py summary --month 2026-10
```
Aur bina `--month` ke `python main.py summary` likho to saare mahinon ki
mila kar summary ayegi.

**Kharcha delete karna** (id list mein se dekh kar):
```bash
python main.py delete --id 2
```

**Categories dekhna:**
```bash
python main.py categories
```

**Help dekhna** (kabhi bhool jao to):
```bash
python main.py --help
python main.py add --help
```

### Pehle se bhari hui sample file try karna

Shuru mein apna data na bharna chaho to project mein ek sample file
pehle se maujood hai. `--file` wala option command se **pehle** likhna hai:

```bash
python main.py --file sample_data/expenses.json list
python main.py --file sample_data/expenses.json summary --month 2026-10
```

Us file par summary ka jawab ye ayega:

```
Summary for 2026-10
  Expenses: 6
  Total:    5750.00
  Average:  958.33 per expense

By category:
  Bills              2500.00
  Education          1500.00
  Entertainment       800.00
  Food                750.00
  Transport           200.00
```

### Tests chalana

```bash
python -m unittest discover -s tests -v
```

Sab theek ho to aakhir mein ayega: `Ran 24 tests` aur `OK`.

---

## 10. Interview / viva ke sawal — simple jawabon ke saath

### Sawal 1: Apne project ke bare mein kuch batayein — ye karta kya hai?

**Jawab:** Ye ek Python CLI program hai jo roz ke kharche record karta hai.
User amount, category aur date ke saath kharcha add karta hai, phir list,
monthly summary aur category-wise totals dekh sakta hai. Data JSON file mein
save hota hai, is liye program band karne ke baad bhi mehfooz rehta hai.

### Sawal 2: Aap ne code ko alag alag files (modules) mein kyun rakha? Ek hi file mein kyun nahi?

**Jawab:** Har module ka ek hi kaam hai — `models.py` data ki definition aur
validation, `storage.py` file parhna/likhna, `analytics.py` hisaab kitaab,
aur `cli.py` user se baat. Isay separation of concerns kehte hain. Faida ye
hai ke ghalti dhoondna asaan hota hai, har hissa alag test ho sakta hai, aur
kal ko CLI ki jagah koi aur interface lagana ho to baaki code waisa hi
rahega.

### Sawal 3: Dataclass kya hai, aur aap ne kyun use ki?

**Jawab:** Dataclass Python ka shortcut hai aisi classes ke liye jin ka kaam
sirf data rakhna hota hai. Python fields dekh kar `__init__` jaisa repeat
wala code khud bana deta hai. Meine isay `Expense` ke liye use kiya, aur
`__post_init__` mein validation daali — is liye galat amount ya galat date
wala expense object ban hi nahi sakta.

### Sawal 4: Data file mein kyun save kiya? Database kyun nahi use kiya?

**Jawab:** Is size ke project ke liye JSON file kaafi hai — koi setup nahi
chahiye, file insaan bhi parh sakta hai, aur data mehfooz (persistent) bhi
ho jata hai. Database (masalan SQLite) tab zaroori hota hai jab data bohat
zyada ho ya ek saath kai users hon. Agar project bara karun ga to SQLite
agle steps mein hai — ye README ke future improvements mein likha bhi hai.

### Sawal 5: Aap ka program galat input kese handle karta hai?

**Jawab:** Do jaga checking hoti hai. Pehle model layer mein —
`validate_amount` aur `validate_date` galat value par `ValueError` uthate
hain, saaf message ke saath, jese "Amount must be greater than zero."
Phir CLI layer us error ko `try/except` se pakad kar user ko wahi message
dikhata hai aur exit code 1 ke saath band hota hai — poora traceback (lamba
ajeeb error) nahi dikhta. Khaali / corrupt data file ke liye bhi alag saaf
message hai.

### Sawal 6: Aap ne tests kyun likhe, aur wo kya check karte hain?

**Jawab:** Tests is liye likhe ke kal ko code mein change karun to fauran
pata chal jaye ke kuch toota to nahi. 24 tests hain, aur wo printed output
ki jagah asal logic check karte hain — validation, storage ka add/load/delete,
aur analytics ke totals aur summaries. Storage wale tests temporary file
istemaal karte hain, taake asal data file kharab na ho.

### Sawal 7: Agar kharche delete karne ke baad ids ka masla ho — naya kharcha purani id le le to?

**Jawab:** Isi liye ids list ki length se nahi bante. File mein ek `next_id`
hamesha save rehta hai jo sirf barhta hai, kabhi kam nahi hota. Delete ke
baad bhi naya kharcha hamesha ek nayi, pehle kabhi na ayi hui id leta hai —
is liye kabhi do kharchon ki id ek nahi hoti.

### Sawal 8 (bonus): Is project ko aage kese behtar banayenge?

**Jawab:** Agle steps ye hain: CSV export, har category ke liye monthly
budget aur budget cross honay par warning, expense edit karne ki command,
description mein search, data ke liye SQLite, aur spending ke charts.
Ye sab README ke "Future Improvements" mein likha hai.

---

## 11. Aakhri mashwara — khud samajhne ka tareeqa

Is file ko ek dafa parhna kaafi nahi. Ye teen kaam karo, phir ye project
waqai tumhara ho jayega:

1. **Ek kharcha apne haath se add karo**, phir `expenses.json` file khol
   kar dekho ke andar kya change aya. Data ka safar (command → code → file)
   apni aankhon se dekh lo.
2. **Ek test khud chalao aur ek value badal kar dekho** — masalan test mein
   amount galat likh do aur dekho ke test fail kese hota hai. Fail hota
   test dekhna bhi seekhna hai.
3. **Har file ko apne kisi dost ko samjhane ki koshish karo** apni zubaan
   mein. Jahan atak jao, wahi hissa is file se dobara parho. Jo cheez tum
   doosre ko samjha sakte ho, wo tumhe waqai ati hai.

Aur ek seedhi baat: agar koi pooche ke ye project kis ne banaya, to
mehnet aur samajh tumhari apni honi chahiye. Code tab hi kaam ka hai jab
tum usay samjho, badal sako, aur us ke sawalon ka jawab de sako — isi liye
ye notes bane hain.
