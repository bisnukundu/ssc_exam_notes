# SSC 2nd Year – New Version (১৩টি বিষয়)

## Official Source (একমাত্র উৎস)

- **BOU eBook Catalogue:** https://www.ebookbou.edu.bd/ssc.php
- **Section:** ২য় বর্ষ নতুন ভার্সন
- **যাচাই:** ১১ নভেম্বর ২০২৬

## নিয়ম (Strict)

- শুধু SSC ২য় বর্ষের **নতুন ভার্সনের** ১৩টি বিষয়।
- ১ম বর্ষের কোনো বিষয় নেই। পুরাতন ভার্সনের কোনো বিষয় নেই।
- NCTB-এর সাধারণ SSC Subject List থেকে অতিরিক্ত বিষয় নেই।
- প্রতিটি Subject-এর Course Code Official Source অনুযায়ী।

## ১৩টি বিষয়

| Code | বিষয় | Unit তালিকা | নম্বর বণ্টন | বই PDF |
|------|------|-------------|-------------|---------|
| 2651 | বাংলা দ্বিতীয় পত্র | ১১টি Unit — যাচাইকৃত (পাঠ ও পৃষ্ঠাসহ) | ১০০ (সৃজনশীল ৬০ + MCQ ৪০) — যাচাইকৃত | ✅ আছে |
| 2652 | English Two | ১৭টি Unit (শুধু প্রথম ও শেষ শিরোনাম সংরক্ষিত) | ১০০ (Grammar ৬০ + Writing ৪০) — যাচাইকৃত | ✅ আছে |
| 2669 | শারীরিক শিক্ষা, স্বাস্থ্য বিজ্ঞান ও খেলাধুলা | শুধু Unit 8 যাচাইকৃত | Not Yet Verified | ✅ আছে |
| 2671 | অর্থনীতি | ১২টি Unit — যাচাইকৃত | Not Yet Verified | ✅ আছে |
| 2672 | পৌরনীতি ও নাগরিকতা | ১২টি Unit — যাচাইকৃত | Not Yet Verified | ✅ আছে |
| 2673 | বিজ্ঞান | ১৪টি Unit — যাচাইকৃত | Not Yet Verified | ✅ আছে |
| 2676 | ফিন্যান্স ও ব্যাংকিং | ১৩টি Unit — যাচাইকৃত | Not Yet Verified | ⏳ শীঘ্রই আসছে |
| 2679 | জীববিজ্ঞান | ১৪টি Unit + ব্যবহারিক — যাচাইকৃত | Not Yet Verified | ⏳ শীঘ্রই আসছে |
| 2680 | উচ্চতর গণিত | ১৪টি Unit — যাচাইকৃত | Not Yet Verified | ⏳ শীঘ্রই আসছে |
| 2681 | বাংলাদেশ ও বিশ্বপরিচয় | ১৫টি Unit — যাচাইকৃত | Not Yet Verified | ✅ আছে |
| 2685 | গার্হস্থ্য বিজ্ঞান | ১৭টি Unit — যাচাইকৃত | Not Yet Verified | ⏳ শীঘ্রই আসছে |
| 2686 | কৃষি শিক্ষা | ১৩টি Unit — যাচাইকৃত | Not Yet Verified | ✅ আছে |
| 2358 | ক্যারিয়ার শিক্ষা | শুধু Unit 4 যাচাইকৃত | Not Yet Verified | ✅ আছে |

সতর্কতা: ২০২২ সালের সিলেবাসের নম্বর ২০২৬-এর জন্য আমদানি করা যাবে না
(যেমন ২৬৫২-তে ২০২২-এ Grammar ৩৫ দেখালেও ২০২৬-এর বইয়ে Grammar ৬০ + Writing ৪০ যাচাই হয়েছে)।

## ফাইল কাঠামো

```
index.html   — নতুন "SSC 2nd Year – New Version" সেকশন + মেনু বোতাম (🎓 ২য় বর্ষ নতুন)
index.css    — নতুন সেকশন/কার্ডের স্টাইল (ফাইলের শেষে যুক্ত; পুরোনো স্টাইল অপরিবর্তিত)
index.js     — loadSecondYearSubjects(), showSubjectUnits(), openNotes2651()
db/
  ssc-2nd-year-new-version.json  — ১৩ বিষয়ের একমাত্র উৎস (canonical data)
  notes-2651.json                — ২৬৫১-এর সম্পূর্ণ নোট (১১ Unit: ব্যাকরণ ৫ + নির্মিতি ৬)
  books.json                     — ১৩টি বই (আগের ৯টি অপরিবর্তিত + ৪টি নতুন, pdf_pending)
  bangla_note.json               — আগের মতো (১৬৫১ বাংলা ১ম পত্র)
  vugol.json                     — আগের মতো
tools/
  generate-second-year-data.py   — ssc-2nd-year-new-version.json তৈরির স্ক্রিপ্ট
  generate-notes-2651.py         — notes-2651.json তৈরির স্ক্রিপ্ট
```

## ২৬৫১ বাংলা দ্বিতীয় পত্র — সম্পূর্ণ নোট

- উৎস: BOU SSC-2651 বই (ISBN 984-34-3000-x, পরিমার্জিত সংস্করণ জানুয়ারি ২০২৬)।
- ১১টি Unit-এর প্রতিটিতে: সহজ ব্যাখ্যা, গুরুত্বপূর্ণ পয়েন্ট, পরীক্ষার প্রস্তুতি, Quick Revision।
- বইয়ের নিজস্ব MCQ শুধু Unit 1, পাঠ ১.১-এ আছে (পৃ. ২-এর পাঠোত্তর মূল্যায়ন থেকে, ৪টি) —
  অন্য Unit-এর বইয়ের MCQ বলে কিছু বানানো হয়নি।
- সৃজনশীল ৬০-এর মধ্যে প্রতিবেদন প্রণয়ন ১০ নম্বর বইয়ের মানবণ্টনে আছে;
  সূচিপত্রের ১১ Unit-এর মধ্যে প্রতিবেদনের আলাদা Unit নেই — নোটে তা স্পষ্ট লেখা আছে।
- স্থিতি: **Under Teacher Review** — শিক্ষক অনুমোদন ছাড়া কোনো পাঠ Published নয়।

## Database Mapping (Laravel Backend)

Backend: `bou-ssc-laravel-backend/` (এই রিপোতে নেই, আলাদা প্রজেক্ট)।
কোনো migration বা schema পরিবর্তন লাগেনি — টেবিলগুলো আগে থেকেই year-agnostic:

| এই রিপোর ডেটা | Laravel টেবিল | ম্যাপিং |
|---|---|---|
| `subjects[].code` | `subjects.code` | unique(`curriculum_id`, `code`) — duplicate অসম্ভব |
| `subjects[].title_bn / title_en` | `subjects.title_bn / title_en` | |
| `year = second`, `version = new` | `subjects.year_level = 'second'`, `status = 'in_production'` | First Year: `catalogue_only` |
| `subjects[].units[]` | `units` (`subject_id`, `sort_order`, `page_range`) | |
| `units[].lessons[]` | `lessons` (`unit_id`, `subject_id`, `slug`, `source_pages`, `review_status`) | নতুন পাঠ `review_status = draft` |
| নম্বর বণ্টন | `exams` + `questions` (`verification_status = not_yet_verified` যতক্ষণ না যাচাই হয়) | যাচাই হয়নি এমন নম্বর seed করা হয় না |

`SubjectSeeder`-এ ২৭টি বিষয়ই আছে; ১৩টি Second Year বিষয় `in_production`,
১৪টি First Year বিষয় `catalogue_only` — এই নিয়ম অপরিবর্তিত আছে।

## নতুন বিষয় / পাঠ যুক্ত করার নিয়ম

1. প্রথমে BOU উৎস (eBook PDF বা সূচিপত্র) থেকে Unit/নম্বর যাচাই করো।
2. `tools/generate-second-year-data.py` বা `tools/generate-notes-2651.py`-তে যুক্ত করে
   JSON regenerate করো — হাতে JSON সম্পাদনা নয়।
3. যাচাই হয়নি এমন কিছু `null` + "Not Yet Verified" রাখো; অনুমান করে লিখো না।
4. নতুন পাঠ সবসময় Under Teacher Review — শিক্ষক অনুমোদন ছাড়া Published নয়।

## Test Checklist (Push-এর আগে)

- [x] `db/ssc-2nd-year-new-version.json`: ঠিক ১৩টি বিষয়, code unique, ১ম বর্ষের code নেই
- [x] `db/books.json`: ১৩টি এন্ট্রি, আগের ৯টি PDF অপরিবর্তিত, কোনো duplicate নেই
- [x] `db/notes-2651.json`: ১১টি Unit (ব্যাকরণ ৫ + নির্মিতি ৬), Unit 1-এ বইয়ের ৪টি MCQ
- [x] `node --check index.js` পাস
- [x] স্থানীয় HTTP সার্ভারে পাতা খুলে ১৩টি কার্ড, Unit প্যানেল ও ২৬৫১ নোট যাচাই
- [x] পুরোনো ভিউ (ই-বুক, নোটস, ১৬৫১, ভূগোল, থিম, বই রিডার) অপরিবর্তিত
