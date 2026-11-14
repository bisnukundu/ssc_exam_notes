#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate 2681 landscape infographic HTML templates (1920x1080)."""
import os

OUT_DIR = os.path.expanduser("~/workspace/ssc_exam_notes/tools")

CSS = '''
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { width: 1920px; background: #fdfcf9;
         font-family: 'Noto Sans Bengali', 'DejaVu Sans', sans-serif; color: #1a1a2e; }
  .header { background: #16265c; padding: 26px 60px 22px; text-align: center; }
  .header h1 { font-family: 'Noto Serif Bengali', serif; font-size: 58px; color: #f5c542; line-height: 1.15; }
  .header p { font-size: 26px; color: #ffffff; margin-top: 4px; }
  .wrap { padding: 22px 48px 0; }
  .row { display: flex; gap: 22px; margin-top: 20px; }
  .row:first-child { margin-top: 0; }
  .banner { border-radius: 24px; padding: 24px 36px; display: flex; align-items: center; gap: 30px; }
  .banner .ico { font-size: 72px; }
  .banner h2 { font-size: 38px; color: #ffffff; margin-bottom: 6px; }
  .banner p { font-size: 28px; line-height: 1.5; color: #f2f6ff; }
  .card { border-radius: 24px; padding: 24px 30px; }
  .card h2 { font-size: 36px; margin-bottom: 12px; }
  .card h3 { font-size: 32px; margin-bottom: 6px; }
  .card p { font-size: 26px; line-height: 1.5; color: #3a3a55; }
  .c-blue { background: #e8eef8; } .c-blue h2, .c-blue h3 { color: #2d4a8a; }
  .c-green { background: #e8f4ec; } .c-green h2, .c-green h3 { color: #2e6b41; }
  .c-purple { background: #f8e8f0; } .c-purple h2, .c-purple h3 { color: #8b2252; }
  .c-orange { background: #fdf3e0; } .c-orange h2, .c-orange h3 { color: #9a6208; }
  .c-red { background: #fdecec; } .c-red h2, .c-red h3 { color: #9a1c1c; }
  .c-teal { background: #e0f2f1; } .c-teal h2, .c-teal h3 { color: #0f5f5c; }
  .c-yellow { background: #fff8e1; } .c-yellow h2, .c-yellow h3 { color: #7a5c00; }
  .c-white { background: #ffffff; border: 2px solid #e0dbd0; }
  .c-white h2, .c-white h3 { color: #16265c; }
  .chips { display: flex; flex-wrap: wrap; gap: 12px; }
  .chip { background: #ffffff; border: 2px solid #d5dce8; border-radius: 999px;
          padding: 9px 20px; font-size: 27px; font-weight: bold; }
  .mini { flex: 1; border-radius: 20px; padding: 20px 22px; }
  .mini h3 { font-size: 32px; margin-bottom: 6px; }
  .mini p { font-size: 26px; line-height: 1.5; color: #3a3a55; }
  .tip { background: #16265c; border-radius: 24px; padding: 22px 32px;
         display: flex; align-items: center; gap: 22px; }
  .tip .ico { font-size: 52px; }
  .tip p { font-size: 28px; line-height: 1.5; color: #ffffff; }
  .tip b { color: #f5c542; }
  .warn { background: #9a1c1c; border-radius: 24px; padding: 20px 32px;
          display: flex; align-items: center; gap: 22px; }
  .warn .ico { font-size: 52px; }
  .warn p { font-size: 28px; line-height: 1.5; color: #ffffff; }
  .warn b { color: #ffd166; }
  .footer { text-align: center; font-size: 22px; color: #7a7a9a; padding: 22px 0 20px; }
  .compact .wrap { padding-top: 16px; }
  .compact .row { margin-top: 14px; }
  .compact .card { padding: 18px 26px; }
  .compact .banner { padding: 18px 30px; }
  .compact .tip, .compact .warn { padding: 16px 28px; }
  .compact .footer { padding: 10px 0 10px; }
  .compact .header { padding: 18px 60px 16px; }
  .timeline { position: relative; display: flex; gap: 14px; margin-top: 34px; }
  .timeline::before { content: ""; position: absolute; top: -16px; left: 30px; right: 30px;
                      height: 6px; background: #c94b4b; border-radius: 3px; }
  .titem { flex: 1; background: #ffffff; border: 2px solid #e0dbd0; border-radius: 18px;
           padding: 18px 14px; text-align: center; position: relative; }
  .titem::before { content: ""; position: absolute; top: -26px; left: 50%; margin-left: -11px;
                   width: 22px; height: 22px; border-radius: 50%; background: #c94b4b;
                   border: 4px solid #ffffff; box-shadow: 0 0 0 2px #c94b4b; }
  .titem b { display: block; font-size: 34px; color: #9a1c1c; margin-bottom: 4px; }
  .titem span { font-size: 24px; line-height: 1.4; color: #3a3a55; }
  .steps { display: flex; align-items: stretch; gap: 8px; }
  .step { flex: 1; border-radius: 18px; padding: 18px 16px; text-align: center; }
  .step .n { display: inline-block; background: #16265c; color: #ffffff; font-size: 26px;
             font-weight: bold; width: 44px; height: 44px; line-height: 44px;
             text-align: center; border-radius: 50%; margin-bottom: 8px; }
  .step b { display: block; font-size: 30px; color: #16265c; margin-bottom: 4px; }
  .step span { font-size: 24px; line-height: 1.45; color: #3a3a55; }
  .arrow { align-self: center; font-size: 44px; color: #16265c; flex: 0 0 auto; }
  .layers { display: flex; flex-direction: column; gap: 12px; }
  .layer { border-radius: 16px; padding: 14px 24px; text-align: center; }
  .layer b { font-size: 30px; }
  .layer span { font-size: 25px; color: #3a3a55; }
  .bigstat { text-align: center; }
  .bigstat b { display: block; font-size: 96px; line-height: 1; color: #2d4a8a; }
  .bigstat span { font-size: 28px; color: #3a3a55; }
  .numgrid { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 14px; }
  .numgrid .nc { background: #f4f6fb; border-radius: 16px; padding: 16px 14px; }
  .numgrid .nc b { display: block; font-size: 29px; color: #16265c; margin-bottom: 4px; }
  .numgrid .nc span { font-size: 24px; line-height: 1.45; color: #3a3a55; }
  .numgrid .nc .n { display: inline-block; background: #9a1c1c; color: #ffffff; font-size: 22px;
                    font-weight: bold; width: 34px; height: 34px; line-height: 34px;
                    text-align: center; border-radius: 50%; margin-right: 8px; }
'''

UNITS = []

UNITS.append({
 "n": 1, "slug": "andolon-jatiotabad",
 "title": "পূর্ব বাংলার আন্দোলন ও জাতীয়তাবাদের উত্থান (ইউনিট-০১)",
 "pages": "পৃ. ১–২২",
 "alt": "পূর্ব বাংলার আন্দোলন ও জাতীয়তাবাদের উত্থান — Unit 1 ইনফোগ্রাফিক (Timeline ডিজাইন): ১৯৪৭–১৯৭০-এর ৬টি ঘটনা, ছয় দফা, গণঅভ্যুত্থান",
 "body": '''
    <div class="row">
      <div class="banner" style="flex:1; background: linear-gradient(120deg, #9a1c1c, #4b134f);">
        <div class="ico">✊</div>
        <div>
          <h2>কীভাবে জাতীয়তাবাদ জন্ম নিল?</h2>
          <p>১৯৪৭-এ বিভাগের পর ভাষা, অর্থনীতি ও শাসনক্ষমতায় বৈষম্যের বিরুদ্ধে ধাপে ধাপে আন্দোলন গড়ে ওঠে — ভাষা আন্দোলন থেকে শুরু হয়ে ছয় দফা, গণঅভ্যুত্থান ও নির্বাচনের মধ্য দিয়ে তা স্বাধীনতার দিকে এগিয়ে যায়।</p>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="card c-white" style="flex:1">
        <h2>📅 ১৯৪৭ → ১৯৭০: ধারাবাহিকতা</h2>
        <div class="timeline">
          <div class="titem"><b>১৯৪৭</b><span>ভারত বিভাগ; পূর্ব বাংলা পাকিস্তানের অংশ</span></div>
          <div class="titem"><b>১৯৫২</b><span>ভাষা আন্দোলন — ২১ ফেব্রুয়ারি শহিদ দিবস</span></div>
          <div class="titem"><b>১৯৫৪</b><span>নির্বাচনে যুক্তফ্রন্টের জয়</span></div>
          <div class="titem"><b>১৯৬৬</b><span>ছয় দফা — স্বায়ত্তশাসনের রূপরেখা</span></div>
          <div class="titem"><b>১৯৬৯</b><span>গণঅভ্যুত্থান — স্বৈরশাসনের বিরুদ্ধে ঐক্য</span></div>
          <div class="titem"><b>১৯৭০</b><span>নির্বাচনে আওয়ামী লীগের নিরঙ্কুশ জয়</span></div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="card c-red" style="flex:1">
        <h2>⚠️ মনে রাখবে</h2>
        <p>ছয় দফা <b>স্বায়ত্তশাসনের</b> দাবি ছিল, স্বাধীনতার নয়। ভাষা আন্দোলন শুধু ভাষার দাবি নয় — এটি ছিল জাতীয়তাবাদের সূচনা।</p>
      </div>
      <div class="card c-orange" style="flex:1">
        <h2>💡 পরীক্ষার টিপস</h2>
        <p>তারিখগুলো ধারাবাহিকভাবে মনে রাখবে: ১৯৪৭, ১৯৫২, ১৯৫৪, ১৯৬৬, ১৯৬৯, ১৯৭০। প্রতিটি ঘটনার কারণ ও ফলাফল আলাদা করে লিখতে শিখবে।</p>
      </div>
    </div>
'''
})

UNITS.append({
 "n": 2, "slug": "swadhin-bangladesh",
 "title": "স্বাধীন বাংলাদেশ (ইউনিট-০২)",
 "pages": "পৃ. ২৩–৪২",
 "alt": "স্বাধীন বাংলাদেশ — Unit 2 ইনফোগ্রাফিক (Date Cards ডিজাইন): ৭ মার্চ ভাষণ, ২৬ মার্চ স্বাধীনতা ঘোষণা, ১৬ ডিসেম্বর বিজয়, সংবিধানের ৪ মূলনীতি",
 "body": '''
    <div class="row">
      <div class="banner" style="flex:1; background: linear-gradient(120deg, #0f5f3c, #16265c);">
        <div class="ico">🇧🇩</div>
        <div>
          <h2>৭ মার্চ ভাষণ → ১৬ ডিসেম্বর বিজয়</h2>
          <p>১৯৭১ সালের ৭ মার্চ বঙ্গবন্ধুর ভাষণ, ২৬ মার্চ স্বাধীনতা ঘোষণা, নয় মাসের মুক্তিযুদ্ধের পর ১৬ ডিসেম্বর বিজয়। এরপর যুদ্ধবিধ্বস্ত দেশ পুনর্গঠন ও সংবিধান প্রণয়নের কাজ শুরু হয়।</p>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="card c-green" style="flex:1">
        <h2>🎙️ ৭ মার্চ ১৯৭১</h2>
        <p><b>বঙ্গবন্ধুর ভাষণ</b> — ‘এবারের সংগ্রাম আমাদের মুক্তির সংগ্রাম, এবারের সংগ্রাম স্বাধীনতার সংগ্রাম’। ঢাকার রেসকোর্স ময়দানে ঐতিহাসিক ভাষণ।</p>
      </div>
      <div class="card c-blue" style="flex:1">
        <h2>📢 ২৬ মার্চ ১৯৭১</h2>
        <p><b>স্বাধীনতা ঘোষণা</b> — এই দিনটি স্বাধীনতা দিবস হিসেবে পালিত হয়।</p>
      </div>
      <div class="card c-red" style="flex:1">
        <h2>🏆 ১৬ ডিসেম্বর ১৯৭১</h2>
        <p><b>বিজয় দিবস</b> — মুক্তিযুদ্ধে বিজয়ের মাধ্যমে স্বাধীন বাংলাদেশ প্রতিষ্ঠিত হয়।</p>
      </div>
    </div>
    <div class="row">
      <div class="card c-white" style="flex:1.4">
        <h2>📜 সংবিধান ১৯৭২ — ৪ মূলনীতি</h2>
        <div class="chips">
          <span class="chip">জাতীয়তাবাদ</span>
          <span class="chip">গণতন্ত্র</span>
          <span class="chip">সমাজতন্ত্র</span>
          <span class="chip">ধর্মনিরপেক্ষতা</span>
        </div>
      </div>
      <div class="card c-orange" style="flex:1">
        <h2>🤝 মুক্তিযুদ্ধে সবাই</h2>
        <p>ছাত্র, কৃষক, শ্রমিক, নারী ও শিশুরাও নানাভাবে অবদান রাখে।</p>
      </div>
    </div>
    <div class="row">
      <div class="tip" style="flex:1">
        <div class="ico">💡</div>
        <p><b>পরীক্ষার টিপস:</b> স্বাধীনতা দিবস (২৬ মার্চ) ও বিজয় দিবস (১৬ ডিসেম্বর) গুলিয়ে ফেলবে না। সংবিধানের চার মূলনীতি নামসহ মুখস্থ রাখবে।</p>
      </div>
    </div>
'''
})

UNITS.append({
 "n": 3, "slug": "sourojogot-bhumondol",
 "compact": True,
 "title": "সৌরজগৎ ও ভূ-মন্ডল (ইউনিট-০৩)",
 "pages": "পৃ. ৪৩–৬৪",
 "alt": "সৌরজগৎ ও ভূ-মন্ডল — Unit 3 ইনফোগ্রাফিক (Orbit ডিজাইন): ৮টি গ্রহ, আহ্নিক ও বার্ষিক গতি, ভূ-মন্ডলের ৩ স্তর",
 "body": '''
    <div class="row">
      <div class="banner" style="flex:1; background: linear-gradient(120deg, #1a1a4e, #0f5f8a);">
        <div class="ico">☀️</div>
        <div>
          <h2>সৌরজগৎ কাকে বলে?</h2>
          <p>সূর্য ও তার চারপাশে ঘূর্ণায়মান গ্রহ, উপগ্রহ, গ্রহাণু ও ধূমকেতু মিলে সৌরজগৎ গঠিত। পৃথিবী সূর্যের তৃতীয় গ্রহ এবং একমাত্র গ্রহ যেখানে প্রাণের অস্তিত্ব জানা আছে।</p>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="card c-white" style="flex:1">
        <h2>🪐 সৌরজগতের গ্রহ ৮টি (ক্রমানুসারে)</h2>
        <div class="chips">
          <span class="chip">বুধ</span>
          <span class="chip">শুক্র</span>
          <span class="chip" style="background:#e8f4ec; border-color:#2e6b41; color:#2e6b41;">🌍 পৃথিবী</span>
          <span class="chip">মঙ্গল</span>
          <span class="chip">বৃহস্পতি</span>
          <span class="chip">শনি</span>
          <span class="chip">ইউরেনাস</span>
          <span class="chip">নেপচুন</span>
        </div>
        <p style="margin-top:12px;">⚠️ প্লুটোকে গ্রহ বলা ভুল — বর্তমানে এটি <b>বামন গ্রহ</b> হিসেবে গণ্য হয়।</p>
      </div>
    </div>
    <div class="row">
      <div class="card c-blue" style="flex:1">
        <h2>🔄 আহ্নিক গতি</h2>
        <p>পৃথিবীর নিজ অক্ষের চারপাশে ঘূর্ণন — <b>দিন-রাত</b> সৃষ্টি করে।</p>
      </div>
      <div class="card c-orange" style="flex:1">
        <h2>🌍 বার্ষিক গতি</h2>
        <p>সূর্যের চারপাশে পরিক্রমণ — <b>ঋতু পরিবর্তন</b> ঘটায়।</p>
      </div>
      <div class="card c-teal" style="flex:1">
        <h2>🌙 চাঁদ</h2>
        <p>পৃথিবীর একমাত্র উপগ্রহ; চাঁদের আকর্ষণে <b>জোয়ার-ভাটা</b> হয়।</p>
      </div>
    </div>
    <div class="row">
      <div class="card c-purple" style="flex:1.4">
        <h2>🧱 ভূ-মন্ডলের ৩ স্তর</h2>
        <div style="display:flex; gap:12px; align-items:center;">
          <div class="layer" style="flex:1; background:#f8e8f0;"><b>ভূত্বক</b><br><span>সবচেয়ে উপরের স্তর</span></div>
          <div style="font-size:36px; color:#8b2252;">→</div>
          <div class="layer" style="flex:1; background:#f3d9e6;"><b>গুরুমন্ডল</b><br><span>মাঝের স্তর</span></div>
          <div style="font-size:36px; color:#8b2252;">→</div>
          <div class="layer" style="flex:1; background:#ecd0de;"><b>কেন্দ্রমন্ডল</b><br><span>সবচেয়ে ভেতরের স্তর</span></div>
        </div>
      </div>
      <div class="card c-green" style="flex:1">
        <h2>📍 অবস্থান নির্ণয়</h2>
        <p><b>অক্ষাংশ ও দ্রাঘিমাংশ</b> দিয়ে পৃথিবীর যেকোনো স্থানের অবস্থান নির্ণয় করা যায়। ভূপৃষ্ঠে স্থলভাগ ও জলভাগ রয়েছে।</p>
      </div>
    </div>
'''
})

UNITS.append({
 "n": 4, "slug": "bhuprakriti-jalbayu",
 "title": "বাংলাদেশের ভূ-প্রকৃতি ও জলবায়ু (ইউনিট-০৪)",
 "pages": "পৃ. ৬৫–৮৬",
 "alt": "বাংলাদেশের ভূ-প্রকৃতি ও জলবায়ু — Unit 4 ইনফোগ্রাফিক (Region Cards ডিজাইন): ভূ-প্রকৃতির ৩ ভাগ, ছয় ঋতু, মৌসুমি জলবায়ু",
 "body": '''
    <div class="row">
      <div class="banner" style="flex:1; background: linear-gradient(120deg, #5c4a1e, #2e6b41);">
        <div class="ico">⛰️</div>
        <div>
          <h2>নদীমাতৃক সমতল দেশ — তবু একরকম নয়</h2>
          <p>দেশের দক্ষিণ-পূর্বে পাহাড়ি অঞ্চল, উত্তরে ও মধ্যাঞ্চলে প্রাচীন পললভূমি এবং বাকি অংশ নদীর পলিতে গড়া সমভূমি রয়েছে। জলবায়ু ক্রান্তীয় মৌসুমি ধরনের।</p>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="card c-orange" style="flex:1">
        <h2>⛰️ পার্বত্য অঞ্চল</h2>
        <p>মূলত চট্টগ্রাম ও পার্বত্য চট্টগ্রামে অবস্থিত; <b>দেশের সর্বোচ্চ পাহাড়</b> এই অঞ্চলে রয়েছে।</p>
      </div>
      <div class="card c-yellow" style="flex:1">
        <h2>🏜️ উচ্চভূমি</h2>
        <p><b>বরেন্দ্রভূমি ও মধুপুর গড়</b> উল্লেখযোগ্য; এগুলো প্লাবন সমভূমির চেয়ে উঁচু।</p>
      </div>
      <div class="card c-green" style="flex:1">
        <h2>🌾 প্লাবন সমভূমি</h2>
        <p>নদীর পলিতে গড়া — দেশের বেশিরভাগ অংশ জুড়ে রয়েছে।</p>
      </div>
    </div>
    <div class="row">
      <div class="card c-white" style="flex:1.5">
        <h2>🌸 ছয় ঋতু (ক্রমানুসারে)</h2>
        <div class="chips">
          <span class="chip">গ্রীষ্ম</span>
          <span class="chip">বর্ষা</span>
          <span class="chip">শরৎ</span>
          <span class="chip">হেমন্ত</span>
          <span class="chip">শীত</span>
          <span class="chip">বসন্ত</span>
        </div>
      </div>
      <div class="card c-blue" style="flex:1">
        <h2>🌧️ মৌসুমি বায়ু</h2>
        <p>বর্ষায় প্রচুর বৃষ্টিপাত হয় — কৃষির জন্য গুরুত্বপূর্ণ, আবার <b>বন্যার কারণও</b> হতে পারে।</p>
      </div>
    </div>
    <div class="row">
      <div class="tip" style="flex:1">
        <div class="ico">💡</div>
        <p><b>পরীক্ষার টিপস:</b> প্লাবন সমভূমি ও উচ্চভূমিকে এক করে ফেলবে না — বরেন্দ্রভূমি ও মধুপুর গড় <b>উচ্চভূমি</b>, সমভূমি নয়।</p>
      </div>
    </div>
'''
})

UNITS.append({
 "n": 5, "slug": "nodi-sompod",
 "compact": True,
 "title": "বাংলাদেশের নদী ব্যবস্থা ও প্রাকৃতিক সম্পদ (ইউনিট-০৫)",
 "pages": "পৃ. ৮৭–১০৮",
 "alt": "বাংলাদেশের নদী ব্যবস্থা ও প্রাকৃতিক সম্পদ — Unit 5 ইনফোগ্রাফিক (River Flow ডিজাইন): পদ্মা, মেঘনা, যমুনা; নদীর উপকার ও ক্ষতি; নবায়নযোগ্য ও অনবায়নযোগ্য সম্পদ",
 "body": '''
    <div class="row">
      <div class="banner" style="flex:1; background: linear-gradient(120deg, #0f5f8a, #0f5f5c);">
        <div class="ico">🌊</div>
        <div>
          <h2>নদীমাতৃক দেশ</h2>
          <p>পদ্মা, মেঘনা ও যমুনা দেশের প্রধান নদী, যাদের শাখা-প্রশাখা সারা দেশে ছড়িয়ে আছে। নদী কৃষি, মৎস্য, পরিবহন ও ব্যবসা-বাণিজ্যে গুরুত্বপূর্ণ ভূমিকা রাখে।</p>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="card c-blue" style="flex:1">
        <h2>🌊 পদ্মা</h2>
        <p>দেশের প্রধান নদীগুলোর একটি; শাখা-প্রশাখা সারা দেশে ছড়িয়ে আছে।</p>
      </div>
      <div class="card c-teal" style="flex:1">
        <h2>🌊 মেঘনা</h2>
        <p>দেশের প্রধান নদীগুলোর একটি; শাখা-প্রশাখা সারা দেশে ছড়িয়ে আছে।</p>
      </div>
      <div class="card c-purple" style="flex:1">
        <h2>🌊 যমুনা</h2>
        <p>দেশের প্রধান নদীগুলোর একটি; শাখা-প্রশাখা সারা দেশে ছড়িয়ে আছে।</p>
      </div>
    </div>
    <div class="row">
      <div class="card c-green" style="flex:1">
        <h2>✅ নদীর উপকারিতা</h2>
        <div class="chips">
          <span class="chip">সেচ</span>
          <span class="chip">মাছ ধরা</span>
          <span class="chip">নৌপরিবহন</span>
          <span class="chip">উর্বর পলিমাটি</span>
        </div>
      </div>
      <div class="card c-red" style="flex:1">
        <h2>⚠️ নদীর ক্ষতি</h2>
        <div class="chips">
          <span class="chip">বন্যা</span>
          <span class="chip">নদীভাঙন</span>
          <span class="chip">নাব্যতা কমে যাওয়া</span>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="card c-white" style="flex:1.3">
        <h2>🌿 প্রাকৃতিক সম্পদ — ২ ধরন</h2>
        <div class="cols" style="display:flex; gap:16px;">
          <div class="mini" style="background:#e8f4ec; border-radius:16px; padding:16px 18px;"><h3 style="color:#2e6b41;">♻️ নবায়নযোগ্য</h3><p>বন, মাছ, সৌরশক্তি</p></div>
          <div class="mini" style="background:#fdecec; border-radius:16px; padding:16px 18px;"><h3 style="color:#9a1c1c;">⛏️ অনবায়নযোগ্য</h3><p>গ্যাস, কয়লা — একবার শেষ হলে আর ফিরে পাওয়া যায় না</p></div>
        </div>
      </div>
      <div class="card c-green" style="flex:1">
        <h2>🌳 সুন্দরবন</h2>
        <p>দেশের সবচেয়ে বড় <b>ম্যানগ্রোভ বন</b>; প্রাকৃতিক দুর্যোগ থেকে উপকূল রক্ষায় গুরুত্বপূর্ণ ভূমিকা রাখে।</p>
      </div>
    </div>
'''
})

UNITS.append({
 "n": 6, "slug": "poribar-samajikikoron",
 "title": "বাংলাদেশে পরিবার কাঠামো ও সামাজিকীকরণ (ইউনিট-০৬)",
 "pages": "পৃ. ১০৯–১২০",
 "alt": "বাংলাদেশে পরিবার কাঠামো ও সামাজিকীকরণ — Unit 6 ইনফোগ্রাফিক (Compare ডিজাইন): একক বনাম যৌথ পরিবার, সামাজিকীকরণের ৫ মাধ্যম, পরিবারের কাজ",
 "body": '''
    <div class="row">
      <div class="banner" style="flex:1; background: linear-gradient(120deg, #8b2252, #5c2d91);">
        <div class="ico">👨‍👩‍👧</div>
        <div>
          <h2>পরিবার — সমাজের ক্ষুদ্রতম একক</h2>
          <p>পরিবার শিশুর জীবনের প্রথম শিক্ষালয়। এখানে শিশু ভাষা, আচার-আচরণ, মূল্যবোধ ও সামাজিক নিয়ম শেখে — এই প্রক্রিয়াকেই সামাজিকীকরণ বলে।</p>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="card c-blue" style="flex:1">
        <h2>🏠 একক পরিবার</h2>
        <p>বাবা-মা ও সন্তান নিয়ে গঠিত <b>ছোট পরিবার</b>।</p>
      </div>
      <div style="align-self:center; flex:0 0 auto; background:#16265c; color:#f5c542; font-size:34px; font-weight:bold; width:76px; height:76px; line-height:76px; text-align:center; border-radius:50%;">VS</div>
      <div class="card c-purple" style="flex:1">
        <h2>🏡 যৌথ পরিবার</h2>
        <p>দাদা-দাদি, চাচা-চাচিসহ <b>একাধিক প্রজন্ম</b> একসঙ্গে বাস করে।</p>
      </div>
    </div>
    <div class="row">
      <div class="card c-white" style="flex:1.4">
        <h2>🔄 সামাজিকীকরণের ৫ মাধ্যম</h2>
        <div class="chips">
          <span class="chip">পরিবার</span>
          <span class="chip">বিদ্যালয়</span>
          <span class="chip">সমবয়সী বন্ধু</span>
          <span class="chip">গণমাধ্যম</span>
          <span class="chip">ধর্মীয় প্রতিষ্ঠান</span>
        </div>
        <p style="margin-top:12px;">সামাজিকীকরণ: সমাজের নিয়ম, মূল্যবোধ ও আচরণ শেখার প্রক্রিয়া, যার মাধ্যমে ব্যক্তি সমাজের সদস্য হয়ে ওঠে।</p>
      </div>
      <div class="card c-green" style="flex:1">
        <h2>🛡️ পরিবারের কাজ</h2>
        <p>সন্তান লালন-পালন, শিক্ষা, অর্থনৈতিক নিরাপত্তা, মানসিক আশ্রয় ও সামাজিক পরিচয় দেওয়া।</p>
      </div>
    </div>
    <div class="row">
      <div class="tip" style="flex:1">
        <div class="ico">💡</div>
        <p><b>পরীক্ষার টিপস:</b> সামাজিকীকরণ জন্ম থেকে শুরু হয়, পরিবারই প্রথম মাধ্যম — শুধু বিদ্যালয়ের কাজ মনে করা ভুল।</p>
      </div>
    </div>
'''
})

UNITS.append({
 "n": 7, "slug": "rashtro-nagorikota-ain",
 "compact": True,
 "title": "রাষ্ট্র, নাগরিকতা ও আইন (ইউনিট-০৭)",
 "pages": "পৃ. ১২১–১৩৪",
 "alt": "রাষ্ট্র, নাগরিকতা ও আইন — Unit 7 ইনফোগ্রাফিক (Pillars ডিজাইন): রাষ্ট্রের ৪ উপাদান, নাগরিকের অধিকার ও কর্তব্য, আইনের শাসন",
 "body": '''
    <div class="row">
      <div class="banner" style="flex:1; background: linear-gradient(120deg, #16265c, #0f5f5c);">
        <div class="ico">🏛️</div>
        <div>
          <h2>রাষ্ট্র কাকে বলে?</h2>
          <p>রাষ্ট্র হলো একটি নির্দিষ্ট ভূখণ্ডে বসবাসকারী জনগণের সংগঠিত রাজনৈতিক প্রতিষ্ঠান। নাগরিক হলো রাষ্ট্রের স্থায়ী সদস্য, যার অধিকার ও কর্তব্য রয়েছে।</p>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="card c-white" style="flex:1">
        <h2>🧱 রাষ্ট্রের ৪ অপরিহার্য উপাদান</h2>
        <div style="display:flex; gap:14px; margin-top:8px;">
          <div style="flex:1; background:#e8eef8; border-radius:16px; padding:20px 10px; text-align:center;"><b style="font-size:32px; color:#2d4a8a;">👥 জনসংখ্যা</b></div>
          <div style="flex:1; background:#e8f4ec; border-radius:16px; padding:20px 10px; text-align:center;"><b style="font-size:32px; color:#2e6b41;">🗺️ ভূখণ্ড</b></div>
          <div style="flex:1; background:#fdf3e0; border-radius:16px; padding:20px 10px; text-align:center;"><b style="font-size:32px; color:#9a6208;">🏛️ সরকার</b></div>
          <div style="flex:1; background:#f8e8f0; border-radius:16px; padding:20px 10px; text-align:center;"><b style="font-size:32px; color:#8b2252;">👑 সার্বভৌমত্ব</b></div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="card c-green" style="flex:1">
        <h2>✅ নাগরিকের অধিকার</h2>
        <div class="chips">
          <span class="chip">ভোটাধিকার</span>
          <span class="chip">মত প্রকাশের স্বাধীনতা</span>
          <span class="chip">শিক্ষা</span>
          <span class="chip">চলাচলের অধিকার</span>
        </div>
      </div>
      <div class="card c-orange" style="flex:1">
        <h2>📋 নাগরিকের কর্তব্য</h2>
        <div class="chips">
          <span class="chip">আইন মানা</span>
          <span class="chip">কর দেওয়া</span>
          <span class="chip">দেশের প্রতি অনুগত থাকা</span>
          <span class="chip">ভোট দেওয়া</span>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="card c-blue" style="flex:1.4">
        <h2>⚖️ আইনের উৎস</h2>
        <div class="chips">
          <span class="chip">সংবিধান</span>
          <span class="chip">সংসদ প্রণীত আইন</span>
          <span class="chip">প্রথা</span>
          <span class="chip">বিচার বিভাগের সিদ্ধান্ত</span>
        </div>
      </div>
      <div class="card c-white" style="flex:1">
        <h2>⚖️ আইনের শাসন</h2>
        <p>সুশাসনের জন্য আইনের শাসন অপরিহার্য — <b>আইনের চোখে সবাই সমান</b>।</p>
      </div>
    </div>
    <div class="row">
      <div class="tip" style="flex:1">
        <div class="ico">💡</div>
        <p><b>পরীক্ষার টিপস:</b> রাষ্ট্র ও সরকারকে এক মনে করা ভুল — সরকার রাষ্ট্রের একটি উপাদান মাত্র; রাষ্ট্র স্থায়ী, সরকার পরিবর্তনশীল।</p>
      </div>
    </div>
'''
})

UNITS.append({
 "n": 8, "slug": "sarkar-ongo-proshashon",
 "title": "বাংলাদেশ সরকারের বিভিন্ন অঙ্গ ও প্রশাসন ব্যবস্থা (ইউনিট-০৮)",
 "pages": "পৃ. ১৩৫–১৫০",
 "alt": "বাংলাদেশ সরকারের বিভিন্ন অঙ্গ ও প্রশাসন ব্যবস্থা — Unit 8 ইনফোগ্রাফিক (Branches ডিজাইন): সরকারের ৩ অঙ্গ, ক্ষমতার স্বতন্ত্রীকরণ, স্থানীয় সরকারের স্তর",
 "body": '''
    <div class="row">
      <div class="banner" style="flex:1; background: linear-gradient(120deg, #2d4a8a, #16265c);">
        <div class="ico">⚖️</div>
        <div>
          <h2>সরকারের তিন অঙ্গ — তিনটি আলাদা কাজ</h2>
          <p>আইন বিভাগ আইন তৈরি করে, শাসন বিভাগ আইন বাস্তবায়ন করে এবং বিচার বিভাগ আইনের ব্যাখ্যা দিয়ে ন্যায়বিচার করে। তিন অঙ্গের মধ্যে ক্ষমতার ভারসাম্য থাকলে গণতন্ত্র টেকসই হয়।</p>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="steps" style="flex:1">
        <div class="step" style="background:#e8eef8;">
          <span class="n">১</span>
          <b>আইন বিভাগ</b>
          <span>জাতীয় সংসদ — আইন প্রণয়ন করে</span>
        </div>
        <div class="arrow">→</div>
        <div class="step" style="background:#e8f4ec;">
          <span class="n">২</span>
          <b>শাসন বিভাগ</b>
          <span>রাষ্ট্রপতি, প্রধানমন্ত্রী ও মন্ত্রিসভা — আইন বাস্তবায়ন ও দেশ পরিচালনা করে</span>
        </div>
        <div class="arrow">→</div>
        <div class="step" style="background:#fdf3e0;">
          <span class="n">৩</span>
          <b>বিচার বিভাগ</b>
          <span>সুপ্রিম কোর্টসহ আদালত — ন্যায়বিচার করে ও সংবিধান রক্ষা করে</span>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="card c-purple" style="flex:1">
        <h2>⚖️ ক্ষমতার স্বতন্ত্রীকরণ</h2>
        <p>তিন অঙ্গ আলাদা কাজ করলেও একে অপরের উপর নিয়ন্ত্রণ রাখে, যাতে কেউ <b>স্বেচ্ছাচারী হতে না পারে</b>।</p>
      </div>
      <div class="card c-white" style="flex:1.4">
        <h2>🏘️ স্থানীয় সরকারের স্তর</h2>
        <div class="steps">
          <div class="step" style="background:#f4f6fb; padding:14px 8px;"><b>ইউনিয়ন পরিষদ</b></div>
          <div class="arrow" style="font-size:32px;">→</div>
          <div class="step" style="background:#f4f6fb; padding:14px 8px;"><b>উপজেলা পরিষদ</b></div>
          <div class="arrow" style="font-size:32px;">→</div>
          <div class="step" style="background:#f4f6fb; padding:14px 8px;"><b>জেলা পরিষদ</b></div>
          <div class="arrow" style="font-size:32px;">→</div>
          <div class="step" style="background:#f4f6fb; padding:14px 8px;"><b>পৌরসভা</b></div>
          <div class="arrow" style="font-size:32px;">→</div>
          <div class="step" style="background:#f4f6fb; padding:14px 8px;"><b>সিটি কর্পোরেশন</b></div>
        </div>
        <p style="margin-top:10px;">স্থানীয় সরকার স্থানীয় উন্নয়ন ও সেবা দেয়।</p>
      </div>
    </div>
    <div class="row">
      <div class="tip" style="flex:1">
        <div class="ico">💡</div>
        <p><b>পরীক্ষার টিপস:</b> আইন বিভাগ ও বিচার বিভাগের কাজ গুলিয়ে ফেলবে না — সংসদ আইন বানায়, আদালত আইনের ব্যাখ্যা দেয়।</p>
      </div>
    </div>
'''
})

UNITS.append({
 "n": 9, "slug": "ganotantro-nirbachon",
 "title": "বাংলাদেশের গণতন্ত্র ও নির্বাচন (ইউনিট-০৯)",
 "pages": "পৃ. ১৫১–১৬২",
 "alt": "বাংলাদেশের গণতন্ত্র ও নির্বাচন — Unit 9 ইনফোগ্রাফিক (Ballot ডিজাইন): ভোটের বয়স ১৮, গণতন্ত্রের বৈশিষ্ট্য, সুষ্ঠু নির্বাচনের শর্ত, নির্বাচন কমিশন",
 "body": '''
    <div class="row">
      <div class="banner" style="flex:1; background: linear-gradient(120deg, #0f5f3c, #2d4a8a);">
        <div class="ico">🗳️</div>
        <div>
          <h2>গণতন্ত্র = জনগণের শাসন</h2>
          <p>জনগণ ভোট দিয়ে তাদের প্রতিনিধি নির্বাচন করে, আর সেই প্রতিনিধিরা দেশ পরিচালনা করে। নির্বাচন হলো গণতন্ত্রের প্রাণ — সুষ্ঠু ও নিরপেক্ষ নির্বাচনের মাধ্যমে জনগণের মতামতের প্রতিফলন ঘটে।</p>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="card c-blue" style="flex:0 0 420px;">
        <div class="bigstat"><b>১৮</b><span>বছর পূর্ণ হলে<br>ভোট দেওয়া যায়</span></div>
      </div>
      <div class="card c-green" style="flex:1">
        <h2>⭐ গণতন্ত্রের বৈশিষ্ট্য</h2>
        <div class="chips">
          <span class="chip">জনগণের সার্বভৌমত্ব</span>
          <span class="chip">মত প্রকাশের স্বাধীনতা</span>
          <span class="chip">আইনের শাসন</span>
          <span class="chip">নিয়মিত নির্বাচন</span>
        </div>
      </div>
      <div class="card c-orange" style="flex:1">
        <h2>🏛️ নির্বাচন কমিশন</h2>
        <p>নির্বাচন আয়োজন ও পরিচালনার দায়িত্বে থাকা <b>সাংবিধানিক প্রতিষ্ঠান</b>।</p>
      </div>
    </div>
    <div class="row">
      <div class="card c-white" style="flex:1.4">
        <h2>✅ সুষ্ঠু নির্বাচনের শর্ত</h2>
        <div class="chips">
          <span class="chip">স্বাধীন নির্বাচন কমিশন</span>
          <span class="chip">নিরপেক্ষ প্রশাসন</span>
          <span class="chip">ভোটারদের সচেতনতা</span>
          <span class="chip">গণমাধ্যমের স্বাধীনতা</span>
        </div>
      </div>
      <div class="card c-purple" style="flex:1">
        <h2>🎤 রাজনৈতিক দল</h2>
        <p>নির্বাচনে অংশ নিয়ে জনগণের সামনে <b>কর্মসূচি উপস্থাপন</b> করে।</p>
      </div>
    </div>
    <div class="row">
      <div class="tip" style="flex:1">
        <div class="ico">💡</div>
        <p><b>পরীক্ষার টিপস:</b> ভোটের বয়স আঠারো — এটি MCQ-তে বারবার আসে। গণতন্ত্র মানে শুধু ভোট দেওয়া নয়; মত প্রকাশের স্বাধীনতা, আইনের শাসন ও মানবাধিকারও গণতন্ত্রের অংশ।</p>
      </div>
    </div>
'''
})

UNITS.append({
 "n": 10, "slug": "jatisongho-bangladesh",
 "compact": True,
 "title": "জাতিসংঘ ও বাংলাদেশ (ইউনিট-১০)",
 "pages": "পৃ. ১৬৩–১৭০",
 "alt": "জাতিসংঘ ও বাংলাদেশ — Unit 10 ইনফোগ্রাফিক (Globe ডিজাইন): ১৯৪৫-এ জাতিসংঘ প্রতিষ্ঠা, ১৭ সেপ্টেম্বর ১৯৭৪ বাংলাদেশের সদস্যপদ, প্রধান অঙ্গ, বিশেষায়িত সংস্থা",
 "body": '''
    <div class="row">
      <div class="banner" style="flex:1; background: linear-gradient(120deg, #0f4a6b, #16265c);">
        <div class="ico">🌐</div>
        <div>
          <h2>জাতিসংঘ — বিশ্বশান্তির সংস্থা</h2>
          <p>দ্বিতীয় বিশ্বযুদ্ধের পর বিশ্বশান্তি ও সহযোগিতা প্রতিষ্ঠার লক্ষ্যে জাতিসংঘ গঠিত হয়। জাতিসংঘ শান্তিরক্ষা, উন্নয়ন, মানবাধিকার ও দুর্যোগ মোকাবিলায় কাজ করে।</p>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="card c-blue" style="flex:1">
        <div class="bigstat"><b>১৯৪৫</b><span>জাতিসংঘ প্রতিষ্ঠিত হয়<br>উদ্দেশ্য: বিশ্বশান্তি রক্ষা ও<br>দেশগুলোর মধ্যে সহযোগিতা</span></div>
      </div>
      <div style="align-self:center; flex:0 0 auto; font-size:56px;">→</div>
      <div class="card c-green" style="flex:1">
        <div class="bigstat"><b style="color:#2e6b41;">১৭ সেপ্টেম্বর ১৯৭৪</b><span>বাংলাদেশ জাতিসংঘের<br>সদস্যপদ লাভ করে</span></div>
      </div>
    </div>
    <div class="row">
      <div class="card c-white" style="flex:1.5">
        <h2>🏛️ জাতিসংঘের প্রধান অঙ্গ</h2>
        <div class="chips">
          <span class="chip">সাধারণ পরিষদ</span>
          <span class="chip">নিরাপত্তা পরিষদ</span>
          <span class="chip">অর্থনৈতিক ও সামাজিক পরিষদ</span>
          <span class="chip">আন্তর্জাতিক বিচার আদালত</span>
          <span class="chip">সচিবালয়</span>
        </div>
      </div>
      <div class="card c-orange" style="flex:1">
        <h2>🤝 বিশেষায়িত সংস্থা</h2>
        <p><b>ইউনেস্কো, বিশ্ব স্বাস্থ্য সংস্থা, বিশ্বব্যাংক</b> — শিক্ষা, স্বাস্থ্য ও উন্নয়নে কাজ করে।</p>
      </div>
    </div>
    <div class="row">
      <div class="tip" style="flex:1">
        <div class="ico">🕊️</div>
        <p><b>বাংলাদেশের অবদান:</b> বাংলাদেশ জাতিসংঘ শান্তিরক্ষা মিশনে সৈন্য পাঠিয়ে বিশ্বশান্তিতে গুরুত্বপূর্ণ অবদান রাখছে। মনে রাখবে — ইউনেস্কো জাতিসংঘের একটি সংস্থা, জাতিসংঘ নয়।</p>
      </div>
    </div>
'''
})

UNITS.append({
 "n": 11, "slug": "jatio-sompod-orthoniti",
 "title": "জাতীয় সম্পদ ও অর্থনৈতিক ব্যবস্থা (ইউনিট-১১)",
 "pages": "পৃ. ১৭১–১৮৬",
 "alt": "জাতীয় সম্পদ ও অর্থনৈতিক ব্যবস্থা — Unit 11 ইনফোগ্রাফিক (System Cards ডিজাইন): ধনতান্ত্রিক, সমাজতান্ত্রিক ও মিশ্র অর্থনীতি; বাংলাদেশ মিশ্র অর্থনীতির দেশ",
 "body": '''
    <div class="row">
      <div class="banner" style="flex:1; background: linear-gradient(120deg, #7a5c00, #2e6b41);">
        <div class="ico">💰</div>
        <div>
          <h2>জাতীয় সম্পদ ও অর্থনৈতিক ব্যবস্থা</h2>
          <p>জাতীয় সম্পদ বলতে দেশের মানুষ, ভূমি, বন, পানি, খনিজ ও অন্যান্য সব সম্পদকে বোঝায়, যা দিয়ে দেশের অর্থনীতি চলে। অর্থনৈতিক ব্যবস্থা হলো সম্পদ উৎপাদন, বণ্টন ও ব্যবহারের নিয়ম।</p>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="card c-blue" style="flex:1">
        <h2>💼 ধনতান্ত্রিক</h2>
        <p>উৎপাদনের উপায় <b>ব্যক্তিগত মালিকানায়</b> থাকে; বাজার দাম নির্ধারণ করে।</p>
      </div>
      <div class="card c-red" style="flex:1">
        <h2>🏭 সমাজতান্ত্রিক</h2>
        <p>উৎপাদনের উপায় <b>রাষ্ট্রের মালিকানায়</b> থাকে; রাষ্ট্র পরিকল্পনা করে।</p>
      </div>
      <div class="card c-green" style="flex:1; border: 4px solid #2e6b41;">
        <h2>🇧🇩 মিশ্র — বাংলাদেশ ✅</h2>
        <p>সরকারি ও বেসরকারি খাত একসঙ্গে কাজ করে; <b>বাংলাদেশ এই ব্যবস্থা অনুসরণ করে</b>।</p>
      </div>
    </div>
    <div class="row">
      <div class="card c-white" style="flex:1.4">
        <h2>🌿 জাতীয় সম্পদের ধরন</h2>
        <div class="chips">
          <span class="chip">মানবসম্পদ</span>
          <span class="chip">প্রাকৃতিক সম্পদ — ভূমি, বন, পানি, খনিজ</span>
          <span class="chip">মূলধন</span>
        </div>
      </div>
      <div class="card c-orange" style="flex:1">
        <h2>🎓 সবচেয়ে গুরুত্বপূর্ণ বিনিয়োগ</h2>
        <p>মানবসম্পদ উন্নয়নে <b>শিক্ষা ও স্বাস্থ্য</b> সবচেয়ে গুরুত্বপূর্ণ বিনিয়োগ।</p>
      </div>
    </div>
    <div class="row">
      <div class="tip" style="flex:1">
        <div class="ico">💡</div>
        <p><b>পরীক্ষার টিপস:</b> মিশ্র অর্থনীতিকে ধনতান্ত্রিক বা সমাজতান্ত্রিক বলে লেখা ভুল — বাংলাদেশে দুটি খাতই আছে বলেই এটি মিশ্র অর্থনীতি।</p>
      </div>
    </div>
'''
})

UNITS.append({
 "n": 12, "slug": "orthonoitik-nirdharok",
 "title": "অর্থনৈতিক নির্ধারকসমূহ ও বাংলাদেশের অর্থনীতির প্রকৃতি (ইউনিট-১২)",
 "pages": "পৃ. ১৮৭–২০৮",
 "alt": "অর্থনৈতিক নির্ধারকসমূহ ও বাংলাদেশের অর্থনীতির প্রকৃতি — Unit 12 ইনফোগ্রাফিক (Balance ডিজাইন): চাহিদা বনাম যোগান, দামের নিয়ম, অর্থনীতির ৩ খাত",
 "body": '''
    <div class="row">
      <div class="banner" style="flex:1; background: linear-gradient(120deg, #2d4a8a, #7a5c00);">
        <div class="ico">📈</div>
        <div>
          <h2>দাম নির্ধারিত হয় চাহিদা ও যোগানের ভারসাম্যে</h2>
          <p>অর্থনীতির মূল বিষয়গুলো হলো চাহিদা, যোগান, দাম ও বাজার। বাংলাদেশের অর্থনীতি কৃষিনির্ভর হলেও এখন শিল্প ও সেবা খাতও দ্রুত বাড়ছে।</p>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="card c-blue" style="flex:1">
        <h2>🛒 চাহিদা</h2>
        <p>নির্দিষ্ট দামে <b>ক্রেতা</b> যে পরিমাণ পণ্য কিনতে চায়।</p>
        <p style="margin-top:10px;">দাম বাড়লে চাহিদা <b>কমে</b> ⬇️</p>
        <p>দাম কমলে চাহিদা <b>বাড়ে</b> ⬆️</p>
      </div>
      <div style="align-self:center; flex:0 0 auto; background:#16265c; color:#f5c542; font-size:34px; font-weight:bold; width:76px; height:76px; line-height:76px; text-align:center; border-radius:50%;">⚖️</div>
      <div class="card c-orange" style="flex:1">
        <h2>🏪 যোগান</h2>
        <p>নির্দিষ্ট দামে <b>বিক্রেতা</b> যে পরিমাণ পণ্য বিক্রি করতে চায়।</p>
        <p style="margin-top:10px;">দাম বাড়লে যোগান <b>বাড়ে</b> ⬆️</p>
        <p>দাম কমলে যোগান <b>কমে</b> ⬇️</p>
      </div>
    </div>
    <div class="row">
      <div class="card c-white" style="flex:1.4">
        <h2>🏭 বাংলাদেশের অর্থনীতির ৩ খাত</h2>
        <div class="chips">
          <span class="chip">🌾 কৃষি</span>
          <span class="chip">🏭 শিল্প</span>
          <span class="chip">💼 সেবা</span>
        </div>
      </div>
      <div class="card c-green" style="flex:1">
        <h2>📊 অর্থনীতির প্রকৃতি</h2>
        <p>কৃষিনির্ভর থেকে ধীরে ধীরে <b>শিল্প ও সেবানির্ভর</b> হচ্ছে; তৈরি পোশাক শিল্প ও প্রবাসীদের পাঠানো অর্থ গুরুত্বপূর্ণ ভূমিকা রাখে।</p>
      </div>
    </div>
    <div class="row">
      <div class="tip" style="flex:1">
        <div class="ico">💡</div>
        <p><b>পরীক্ষার টিপস:</b> চাহিদা ও যোগানকে একই জিনিস মনে করা ভুল — চাহিদা ক্রেতার দিক, যোগান বিক্রেতার দিক। দাম নির্ধারণে দুটোরই ভূমিকা ব্যাখ্যা করতে পারতে হবে।</p>
      </div>
    </div>
'''
})

UNITS.append({
 "n": 13, "slug": "ortho-bank-byabostha",
 "title": "বাংলাদেশ সরকারের অর্থ ও ব্যাংক ব্যবস্থা (ইউনিট-১৩)",
 "pages": "পৃ. ২০৯–২২০",
 "alt": "বাংলাদেশ সরকারের অর্থ ও ব্যাংক ব্যবস্থা — Unit 13 ইনফোগ্রাফিক (Money Flow ডিজাইন): অর্থের ৩ কাজ, বাজেট, প্রত্যক্ষ ও পরোক্ষ কর, কেন্দ্রীয় বনাম বাণিজ্যিক ব্যাংক",
 "body": '''
    <div class="row">
      <div class="banner" style="flex:1; background: linear-gradient(120deg, #0f5f3c, #7a5c00);">
        <div class="ico">💵</div>
        <div>
          <h2>অর্থ ও ব্যাংক ব্যবস্থা</h2>
          <p>অর্থ হলো বিনিময়ের মাধ্যম — টাকা দিয়ে আমরা পণ্য ও সেবা কিনি। সরকার প্রতি বছর বাজেটের মাধ্যমে আয় ও ব্যয়ের হিসাব দেয়। ব্যাংক মানুষের টাকা জমা রাখে, ঋণ দেয় ও লেনদেন সহজ করে।</p>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="card c-green" style="flex:1.2">
        <h2>💰 অর্থের ৩ কাজ</h2>
        <div class="chips">
          <span class="chip">বিনিময়ের মাধ্যম</span>
          <span class="chip">মূল্যের পরিমাপক</span>
          <span class="chip">সঞ্চয়ের বাহন</span>
        </div>
      </div>
      <div class="card c-blue" style="flex:1">
        <h2>📋 বাজেট</h2>
        <p>সরকারের এক বছরের <b>আয়-ব্যয়ের পরিকল্পনা</b>; আয়ের প্রধান উৎস কর। শিক্ষা, স্বাস্থ্য, সড়কসহ নানা খাতে ব্যয় হয়।</p>
      </div>
    </div>
    <div class="row">
      <div class="card c-orange" style="flex:1">
        <h2>🧾 প্রত্যক্ষ কর</h2>
        <p>যেমন: <b>আয়কর</b></p>
      </div>
      <div class="card c-purple" style="flex:1">
        <h2>🧾 পরোক্ষ কর</h2>
        <p>যেমন: <b>মূল্য সংযোজন কর</b></p>
      </div>
      <div class="card c-teal" style="flex:1">
        <h2>🏦 বাংলাদেশ ব্যাংক</h2>
        <p><b>কেন্দ্রীয় ব্যাংক</b> — নোট ছাপানো, ব্যাংক নিয়ন্ত্রণ ও মুদ্রানীতি পরিচালনা করে।</p>
      </div>
      <div class="card c-white" style="flex:1">
        <h2>🏧 বাণিজ্যিক ব্যাংক</h2>
        <p>জনগণের আমানত গ্রহণ করে ও ব্যবসা-বাণিজ্যে <b>ঋণ দেয়</b>।</p>
      </div>
    </div>
    <div class="row">
      <div class="tip" style="flex:1">
        <div class="ico">💡</div>
        <p><b>পরীক্ষার টিপস:</b> কেন্দ্রীয় ব্যাংক ও বাণিজ্যিক ব্যাংককে এক মনে করা ভুল — বাংলাদেশ ব্যাংক নোট ছাপায় ও নিয়ন্ত্রণ করে, বাণিজ্যিক ব্যাংক সাধারণ মানুষকে সেবা দেয়।</p>
      </div>
    </div>
'''
})

UNITS.append({
 "n": 14, "slug": "samajik-poriborton",
 "compact": True,
 "title": "সামাজিক পরিবর্তন (ইউনিট-১৪)",
 "pages": "পৃ. ২২১–২৩০",
 "alt": "সামাজিক পরিবর্তন — Unit 14 ইনফোগ্রাফিক (Causes Grid ডিজাইন): পরিবর্তনের ৬ কারণ, নগরায়ণ, ইতিবাচক ও নেতিবাচক দিক",
 "body": '''
    <div class="row">
      <div class="banner" style="flex:1; background: linear-gradient(120deg, #5c2d91, #0f5f8a);">
        <div class="ico">🔄</div>
        <div>
          <h2>সামাজিক পরিবর্তন কাকে বলে?</h2>
          <p>সমাজ স্থির থাকে না; সময়ের সঙ্গে সমাজের কাঠামো, মূল্যবোধ, আচরণ ও জীবনযাত্রায় পরিবর্তন আসে — একেই সামাজিক পরিবর্তন বলে। পরিবর্তনকে বুঝে সঠিক দিকে পরিচালিত করা জরুরি।</p>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="card c-white" style="flex:1.5">
        <h2>⚙️ পরিবর্তনের ৬ কারণ</h2>
        <div class="chips">
          <span class="chip">📚 শিক্ষা</span>
          <span class="chip">💻 প্রযুক্তি</span>
          <span class="chip">🏙️ নগরায়ণ</span>
          <span class="chip">🏭 শিল্পায়ন</span>
          <span class="chip">📡 যোগাযোগ</span>
          <span class="chip">💹 অর্থনৈতিক উন্নয়ন</span>
        </div>
        <p style="margin-top:12px;"><b>নগরায়ণ:</b> গ্রাম থেকে শহরে মানুষের আগমন ও শহরের বিস্তার।</p>
      </div>
      <div class="card c-blue" style="flex:1">
        <h2>🎓 প্রধান চালিকাশক্তি</h2>
        <p><b>শিক্ষা</b> — শিক্ষার প্রসারই পরিবর্তনের প্রধান চালিকাশক্তি হিসেবে কাজ করে।</p>
      </div>
    </div>
    <div class="row">
      <div class="card c-green" style="flex:1">
        <h2>✅ ইতিবাচক পরিবর্তন</h2>
        <div class="chips">
          <span class="chip">শিক্ষার প্রসার</span>
          <span class="chip">নারীশিক্ষা</span>
          <span class="chip">স্বাস্থ্যসেবার উন্নতি</span>
        </div>
      </div>
      <div class="card c-red" style="flex:1">
        <h2>⚠️ নেতিবাচক দিক</h2>
        <div class="chips">
          <span class="chip">যৌথ পরিবার ভেঙে যাওয়া</span>
          <span class="chip">পরিবেশ দূষণ</span>
          <span class="chip">সামাজিক বন্ধন দুর্বল হওয়া</span>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="tip" style="flex:1">
        <div class="ico">💡</div>
        <p><b>পরীক্ষার টিপস:</b> সব পরিবর্তনকে ভালো মনে করা ভুল — পরিবর্তনের ইতিবাচক ও নেতিবাচক দুই দিকই লিখতে হয়।</p>
      </div>
    </div>
'''
})

UNITS.append({
 "n": 15, "slug": "samajik-somosya",
 "title": "সামাজিক সমস্যা (ইউনিট-১৫)",
 "pages": "পৃ. ২৩১–২৪১",
 "alt": "সামাজিক সমস্যা — Unit 15 ইনফোগ্রাফিক (Problem List ডিজাইন): ৭টি সামাজিক সমস্যা, যৌতুক ও বাল্যবিবাহ আইনত নিষিদ্ধ, প্রতিকার",
 "body": '''
    <div class="row">
      <div class="banner" style="flex:1; background: linear-gradient(120deg, #9a1c1c, #7a1c1c);">
        <div class="ico">⚠️</div>
        <div>
          <h2>সামাজিক সমস্যা কাকে বলে?</h2>
          <p>সামাজিক সমস্যা বলতে সমাজের এমন অবস্থাকে বোঝায়, যা জনগণের জীবনযাত্রা ও উন্নয়নে বাধা সৃষ্টি করে। এসব সমস্যার কারণ বুঝে প্রতিকারমূলক ব্যবস্থা নিলে সমাজের উন্নয়ন সম্ভব।</p>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="card c-white" style="flex:1">
        <h2>📋 বাংলাদেশের প্রধান সামাজিক সমস্যা — ৭টি</h2>
        <div class="numgrid">
          <div class="nc"><b><span class="n">১</span>দারিদ্র্য</b><span>মৌলিক চাহিদা পূরণে অক্ষমতা; শিক্ষা ও স্বাস্থ্যসেবা থেকে বঞ্চিত করে</span></div>
          <div class="nc"><b><span class="n">২</span>নিরক্ষরতা</b><span>শিক্ষার অভাবে সচেতন সিদ্ধান্ত নিতে পারে না, কুসংস্কারে আচ্ছন্ন থাকে</span></div>
          <div class="nc"><b><span class="n">৩</span>জনসংখ্যা বৃদ্ধি</b><span>বাংলাদেশের প্রধান সামাজিক সমস্যাগুলোর একটি</span></div>
          <div class="nc"><b><span class="n">৪</span>যৌতুক</b><span>বিয়েতে কনের পরিবারের কাছ থেকে অর্থ বা সম্পদ দাবি করা</span></div>
          <div class="nc"><b><span class="n">৫</span>বাল্যবিবাহ</b><span>নির্ধারিত বয়সের আগে বিয়ে — মেয়েদের শিক্ষা ও স্বাস্থ্যের জন্য ক্ষতিকর</span></div>
          <div class="nc"><b><span class="n">৬</span>মাদকাসক্তি</b><span>ব্যক্তি, পরিবার ও সমাজের জন্য মারাত্মক ক্ষতিকর</span></div>
          <div class="nc"><b><span class="n">৭</span>পরিবেশ দূষণ</b><span>জনগণের জীবনযাত্রা ও উন্নয়নে বাধা সৃষ্টি করে</span></div>
          <div class="nc" style="background:#e8f4ec;"><b><span class="n" style="background:#2e6b41;">✓</span>প্রতিকার</b><span>শিক্ষার প্রসার, সচেতনতা, আইনের প্রয়োগ — শিক্ষার ভূমিকা প্রধান</span></div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="warn" style="flex:1">
        <div class="ico">🚫</div>
        <p><b>মনে রাখবে:</b> যৌতুক ও বাল্যবিবাহ <b>আইনত নিষিদ্ধ</b> — এটি পরীক্ষায় অবশ্যই লিখবে।</p>
      </div>
    </div>
    <div class="row">
      <div class="tip" style="flex:1">
        <div class="ico">💡</div>
        <p><b>পরীক্ষার টিপস:</b> সমস্যার শুধু বর্ণনা দিয়ে প্রতিকার না লেখা ভুল — পরীক্ষায় কারণ ও প্রতিকার দুটোই লিখতে হয়।</p>
      </div>
    </div>
'''
})

def main():
    for u in UNITS:
        html = (
            "<!DOCTYPE html>\n<html lang=\"bn\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<style>\n" + CSS + "\n</style>\n</head>\n<body" + (" class=\"compact\"" if u.get("compact") else "") + ">\n"
            "  <div class=\"header\">\n"
            "    <h1>" + u["title"] + "</h1>\n"
            "    <p>SSC-2681 • বাংলাদেশ ও বিশ্বপরিচয়</p>\n"
            "  </div>\n\n"
            "  <div class=\"wrap\">\n" + u["body"] +
            "\n    <div class=\"footer\">তথ্য: BOU SSC-2681 বই (" + u["pages"] + ")</div>\n"
            "  </div>\n</body>\n</html>\n"
        )
        path = os.path.join(OUT_DIR, "infographic-2681-unit%d-landscape.html" % u["n"])
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", path)

if __name__ == "__main__":
    main()
