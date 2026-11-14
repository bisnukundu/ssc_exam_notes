# Bisnu SSC Notes

🌐 **লাইভ সাইট: https://bisnu-ssc-notes.vercel.app/**

বাংলাদেশ উন্মুক্ত বিশ্ববিদ্যালয় (BOU) SSC পরীক্ষার্থীদের জন্য ই-বুক লাইব্রেরি ও শর্ট নোটস।
তৈরি করেছেন: **বিষ্ণু কুন্ডু (Bisnu Kundu)** — Web Developer & Freelancer.

## 🎓 SSC 2nd Year – New Version (নতুন)

Official Source: https://www.ebookbou.edu.bd/ssc.php — **২য় বর্ষ নতুন ভার্সন** সেকশন।

শুধু এই ১৩টি বিষয়: 2651 বাংলা দ্বিতীয় পত্র, 2652 English Two, 2669 শারীরিক শিক্ষা,
2671 অর্থনীতি, 2672 পৌরনীতি ও নাগরিকতা, 2673 বিজ্ঞান, 2676 ফিন্যান্স ও ব্যাংকিং,
2679 জীববিজ্ঞান, 2680 উচ্চতর গণিত, 2681 বাংলাদেশ ও বিশ্বপরিচয়, 2685 গার্হস্থ্য বিজ্ঞান,
2686 কৃষি শিক্ষা, 2358 ক্যারিয়ার শিক্ষা।

- প্রতিটি বিষয় Subject Card আকারে, আলাদা Unit/Chapter Navigation সহ।
- **2651 বাংলা দ্বিতীয় পত্র সম্পূর্ণ:** ১১টি Unit-এর সহজ ব্যাখ্যা, গুরুত্বপূর্ণ পয়েন্ট,
  পরীক্ষার প্রস্তুতি ও Quick Revision (`db/notes-2651.json`)।
- ১ম বর্ষ ও পুরাতন ভার্সনের কোনো বিষয় এখানে নেই।
- বিস্তারিত: [docs/SECOND-YEAR-NEW-VERSION.md](docs/SECOND-YEAR-NEW-VERSION.md)

## চালানো

এটি একটি static ওয়েবসাইট (HTML + CSS + JavaScript) — কোনো build step নেই।

```bash
# যেকোনো static সার্ভার, যেমন:
python3 -m http.server 8000
# তারপর ব্রাউজারে: http://localhost:8000/
```

> `file://` দিয়ে সরাসরি খুললে `fetch()` দিয়ে JSON লোড হবে না — HTTP সার্ভার দিয়ে চালাতে হবে।

## কাঠামো

```
index.html / index.css / index.js   — ওয়েবসাইট (ই-বুক লাইব্রেরি + নোটস ভিউ)
db/
  ssc-2nd-year-new-version.json     — ২য় বর্ষ নতুন ভার্সনের ১৩ বিষয়ের তথ্য
  notes-2651.json                   — ২৬৫১-এর সম্পূর্ণ নোট
  books.json                        — ২৭টি বইয়ের তালিকা (২য় বর্ষ ১৩ + ১ম বর্ষ ১৪, সবগুলো BOU অফিসিয়াল সাইটের লিংক)
  bangla_note.json / vugol.json     — আগের নোটস (১৬৫১ বাংলা ১ম পত্র, ভূগোল)
docs/SECOND-YEAR-NEW-VERSION.md    — যাচাই, নিয়ম ও Database Mapping
tools/                              — JSON ডেটা তৈরির Python স্ক্রিপ্ট
```

## নিয়ম

- যাচাই হয়নি এমন Unit/নম্বর অনুমান করে লেখা হয় না — `Not Yet Verified` হিসেবে থাকে।
- AI কনটেন্ট শিক্ষক অনুমোদন ছাড়া Published নয়।
