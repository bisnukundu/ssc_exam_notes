// Theme toggle
const html = document.documentElement;
const themeBtn = document.getElementById('themeBtn');
themeBtn.addEventListener('click', () => {
    const isDark = html.getAttribute('data-theme') === 'dark';
    html.setAttribute('data-theme', isDark ? 'light' : 'dark');
    themeBtn.textContent = isDark ? '🌙 Dark Mode' : '☀️ Light Mode';
    localStorage.setItem('theme', isDark ? 'light' : 'dark');
});
const saved = localStorage.getItem('theme');
if (saved) {
    html.setAttribute('data-theme', saved);
    themeBtn.textContent = saved === 'dark' ? '☀️ Light Mode' : '🌙 Dark Mode';
}

// Mobile sidebar
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('overlay');
const hamburger = document.getElementById('hamburger');
hamburger.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    overlay.classList.toggle('show');
});
overlay.addEventListener('click', () => {
    sidebar.classList.remove('open');
    overlay.classList.remove('show');
});

// Progress bar
const progress = document.getElementById('progress');
window.addEventListener('scroll', () => {
    const h = document.documentElement;
    const pct = (h.scrollTop / (h.scrollHeight - h.clientHeight)) * 100;
    progress.style.width = pct + '%';
    document.getElementById('backTop').classList.toggle('show', h.scrollTop > 400);
});

// Global observers reference to clean up when changing subjects
let activeSectionObserver = null;
let activeCardObserver = null;

// View Toggle Logic
const ebookView = document.getElementById('ebook-view');
const notesView = document.getElementById('notes-view');
const toggleViewBtn = document.getElementById('toggleViewBtn');
const siteLogo = document.getElementById('site-logo');
const sidebar2 = document.getElementById('sidebar');

function showNotesView() {
    ebookView.style.display = 'none';
    notesView.style.display = 'block';
    toggleViewBtn.innerHTML = '📚 ই-বুক';
    
    sidebar2.style.display = ''; // Restore CSS default
    document.getElementById('main-content').classList.remove('no-sidebar');
    document.getElementById('hamburger').style.display = '';
}

function showEbookView() {
    notesView.style.display = 'none';
    ebookView.style.display = 'block';
    toggleViewBtn.innerHTML = '📝 নোটস';
    
    sidebar2.style.display = 'none'; 
    document.getElementById('main-content').classList.add('no-sidebar');
    document.getElementById('hamburger').style.display = 'none'; // hide hamburger on ebook home
}

toggleViewBtn.addEventListener('click', () => {
    if (notesView.style.display === 'none') {
        showNotesView();
    } else {
        showEbookView();
    }
});

siteLogo.addEventListener('click', () => {
    showEbookView();
    window.scrollTo({top:0, behavior:'smooth'});
});

// Load Books from db/books.json
function loadBooks() {
    fetch('db/books.json')
        .then(res => res.json())
        .then(books => {
            const booksGrid = document.getElementById('books-grid');
            booksGrid.innerHTML = ''; // clear loading state
            
            books.forEach(book => {
                const card = document.createElement('div');
                card.className = 'book-card' + (book.official_url ? '' : ' no-pdf');
                card.onclick = () => book.official_url ? window.open(book.official_url, '_blank', 'noopener') : openSubjectChoice(book.code);
                
                // We use dynamic style for background if gradient is provided
                const bgStyle = book.gradient ? `background: ${book.gradient};` : '';
                const bookIcon = book.icon ? `<div class="book-icon">${book.icon}</div>` : '';
                
                card.innerHTML = `
                    <div class="book-cover" style="${bgStyle}">
                         <div class="book-spine"></div>
                         ${bookIcon}
                         <div class="book-title-overlay">${book.short_title}</div>
                         <div class="book-pages-edge"></div>
                    </div>
                    <div class="book-info">
                        ${book.code ? `<span class="book-code-badge">SSC-${book.code} • ২য় বর্ষ (নতুন)</span>` : ''}
                        <h3>${book.title}</h3>
                        <button class="read-btn">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 5px; margin-top: -2px;"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
                            ${book.official_url ? 'বই পড়ুন ↗' : 'ইউনিট দেখুন'}
                        </button>
                    </div>
                `;
                booksGrid.appendChild(card);
            });
        })
        .catch(err => {
            console.error("Error loading books:", err);
            document.getElementById('books-grid').innerHTML = '<p style="text-align:center;width:100%;">বই লোড করা যায়নি।</p>';
        });
}

// ══════════════════════════════════════
//   SSC 2nd Year – New Version (13 subjects)
//   Data: db/ssc-2nd-year-new-version.json
//   Official source: https://www.ebookbou.edu.bd/ssc.php
// ══════════════════════════════════════
let secondYearSubjects = [];

function loadSecondYearSubjects() {
    fetch('db/ssc-2nd-year-new-version.json')
        .then(res => res.json())
        .then(data => {
            secondYearSubjects = data.subjects || [];
            renderSecondYearCards();
        })
        .catch(err => {
            console.error("Error loading 2nd year subjects:", err);
            const grid = document.getElementById('second-year-grid');
            if (grid) grid.innerHTML = '<p style="text-align:center;width:100%;">বিষয়ের তালিকা লোড করা যায়নি।</p>';
        });
}

function verificationBadge(s) {
    if (s.verification_status === 'verified') return '<span class="subject-badge verified">✓ যাচাইকৃত</span>';
    if (s.verification_status === 'verified_units') return '<span class="subject-badge verified">✓ Unit তালিকা যাচাইকৃত</span>';
    return '<span class="subject-badge partial">◐ আংশিক যাচাইকৃত</span>';
}

function renderSecondYearCards() {
    const grid = document.getElementById('second-year-grid');
    if (!grid) return;
    grid.innerHTML = '';
    secondYearSubjects.forEach(s => {
        const unitCount = s.units ? s.units.length : (s.unit_count || '—');
        const unitLabel = s.verification_status === 'partial' ? 'আংশিক Unit' : unitCount + ' Unit';
        const marks = s.marks && s.marks.total ? `${s.marks.total} নম্বর` : 'নম্বর: যাচাই হয়নি';
        const card = document.createElement('div');
        card.className = 'subject-card';
        card.onclick = () => openSubjectChoice(s.code);
        card.innerHTML = `
            <div class="subject-card-top" style="background: ${s.gradient};">
                <div class="subject-card-icon">${s.icon}</div>
                <div><div class="subject-card-code">SSC-${s.code}</div>
                <div style="font-size:13px;opacity:0.9;">২য় বর্ষ • নতুন ভার্সন</div></div>
            </div>
            <div class="subject-card-body">
                <h3>${s.title_bn}</h3>
                <div class="subject-card-en">${s.title_en}</div>
                <div class="subject-meta">
                    ${verificationBadge(s)}
                    <span class="subject-badge">${unitLabel}</span>
                    <span class="subject-badge">${marks}</span>
                    ${s.book_status === 'pdf_pending' ? '<span class="subject-badge pdf-pending">বই PDF শীঘ্রই আসছে</span>' : ''}
                </div>
                <button class="subject-card-btn">📖 Unit / Chapter দেখুন</button>
            </div>`;
        grid.appendChild(card);
    });
}

// Notes files for all 13 Second Year subjects (db/notes-<code>.json)
const NOTES_FILES = {
    '2651': 'db/notes-2651.json', '2652': 'db/notes-2652.json', '2669': 'db/notes-2669.json',
    '2671': 'db/notes-2671.json', '2672': 'db/notes-2672.json', '2673': 'db/notes-2673.json',
    '2676': 'db/notes-2676.json', '2679': 'db/notes-2679.json', '2680': 'db/notes-2680.json',
    '2681': 'db/notes-2681.json', '2685': 'db/notes-2685.json', '2686': 'db/notes-2686.json',
    '2358': 'db/notes-2358.json'
};

let currentChoiceSubject = null;
let pendingUnit = null; // { no } — modal unit click waits for notes render, then jumps to that unit

function openSubjectChoice(code) {
    const s = secondYearSubjects.find(x => x.code === code);
    const modal = document.getElementById('subject-choice-modal');
    if (!s || !modal) return;
    currentChoiceSubject = s;
    document.getElementById('choice-modal-title').innerText = `SSC-${s.code} — ${s.title_bn}`;
    const unitCount = s.units ? s.units.length : (s.unit_count || '—');
    const unitLabel = s.verification_status === 'partial' ? 'আংশিক Unit যাচাইকৃত' : unitCount + ' Unit';
    const marks = s.marks && s.marks.total ? `মোট ${s.marks.total} নম্বর` : 'নম্বর: যাচাই হয়নি';
    document.getElementById('choice-modal-meta').innerText = `${s.title_en} • ${unitLabel} • ${marks}`;
    const notesBtn = document.getElementById('choiceNotesBtn');
    const bookBtn = document.getElementById('choiceBookBtn');
    const noteEl = document.getElementById('choice-modal-note');
    notesBtn.disabled = false;
    notesBtn.innerText = '📝 নোট পড়ুন';
    if (s.official_url) {
        bookBtn.disabled = false;
        bookBtn.innerText = '📕 বই পড়ুন ↗';
    } else {
        bookBtn.disabled = true;
        bookBtn.innerText = '📕 বই শীঘ্রই আসছে';
    }
    let note = 'কী পড়তে চাও? নোটে আছে সহজ ব্যাখ্যা, MCQ ও সৃজনশীল প্রশ্নোত্তর। বইয়ে আছে মূল পাঠ্যবই।';
    if (s.official_url) note += ' বই পড়তে চাপ দিলে BOU-র অফিসিয়াল সাইটে খুলবে।';
    if (s.verification_status === 'partial') note += ' (এই বিষয়ের কিছু Unit এখনো যাচাই হয়নি।)';
    noteEl.innerText = note;
    const unitsEl = document.getElementById('choice-modal-units');
    if (s.units && s.units.length > 0) {
        unitsEl.innerHTML = '<div class="choice-units-label">📚 Unit তালিকা</div><div class="choice-units-hint">👆 যেকোনো Unit-এ চাপ দিলে সরাসরি সেই Unit-এর নোট খুলবে</div>' + s.units.map(u => {
            const meta = [u.pages || '', u.marks ? `${u.marks} নম্বর` : ''].filter(Boolean).join(' • ');
            return `<div class="choice-unit-row" role="button" tabindex="0" data-unit-no="${u.no}"><strong>Unit ${u.no} — ${u.title_bn}</strong>${meta ? `<span> ${meta}</span>` : ''}<span class="choice-unit-go">›</span></div>`;
        }).join('');
    } else {
        unitsEl.innerHTML = s.unit_note ? `<div class="choice-units-label">📚 Unit তালিকা</div><p class="units-panel-note">${s.unit_note}</p>` : '';
    }
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closeSubjectChoice() {
    const modal = document.getElementById('subject-choice-modal');
    if (modal) modal.style.display = 'none';
    document.body.style.overflow = '';
    currentChoiceSubject = null;
}

function openSubjectNotes() {
    if (!currentChoiceSubject) return;
    const file = NOTES_FILES[currentChoiceSubject.code];
    if (!file) return;
    closeSubjectChoice();
    showNotesView();
    const sel = document.getElementById('subjectSelect');
    if (sel) sel.value = file;
    loadSubject(file);
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function openSubjectBook() {
    if (!currentChoiceSubject || !currentChoiceSubject.official_url) return;
    const url = currentChoiceSubject.official_url;
    closeSubjectChoice();
    window.open(url, '_blank', 'noopener');
}

// Modal → Unit deep-link: open the subject's notes, then jump to that unit
function openSubjectUnit(unitNo) {
    if (!currentChoiceSubject) return;
    const file = NOTES_FILES[currentChoiceSubject.code];
    if (!file) return;
    pendingUnit = { no: Number(unitNo) };
    closeSubjectChoice();
    showNotesView();
    const sel = document.getElementById('subjectSelect');
    if (sel) sel.value = file;
    loadSubject(file);
}

function scrollToPendingUnit() {
    if (!pendingUnit) return;
    const no = pendingUnit.no;
    pendingUnit = null;
    const cards = document.querySelectorAll('#dynamic-content .card');
    let target = null;
    const re = new RegExp('^Unit\\s+' + no + '\\s*[\u2014\u2013-]');
    cards.forEach(c => {
        const t = c.querySelector('.card-title');
        if (t && re.test(t.textContent.trim())) target = c;
    });
    if (!target && cards[no - 1]) target = cards[no - 1]; // fallback: Nth card = Unit N
    if (!target) { window.scrollTo({ top: 0, behavior: 'smooth' }); return; }
    target.classList.add('unit-flash');
    setTimeout(() => target.classList.remove('unit-flash'), 3400);
    const jump = () => target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    jump();
    // Late-loading images above the target (unit infographics, profile photo)
    // expand after the first jump and push the target down — re-assert the
    // scroll while the page settles, unless the user scrolls manually.
    const until = Date.now() + 4500;
    let userScrolled = false;
    const stopOnUserScroll = () => { userScrolled = true; };
    window.addEventListener('wheel', stopOnUserScroll, { once: true, passive: true });
    window.addEventListener('touchmove', stopOnUserScroll, { once: true, passive: true });
    const reassert = () => {
        if (userScrolled || Date.now() >= until) return;
        if (target.getBoundingClientRect().top > 220) jump();
    };
    const imgs = document.querySelectorAll('#notes-view img');
    const onImg = () => reassert();
    imgs.forEach(im => { im.addEventListener('load', onImg); im.addEventListener('error', onImg); });
    const timer1 = setTimeout(reassert, 900);
    const timer2 = setTimeout(reassert, 2000);
    setTimeout(() => {
        imgs.forEach(im => { im.removeEventListener('load', onImg); im.removeEventListener('error', onImg); });
        clearTimeout(timer1);
        clearTimeout(timer2);
        if (!userScrolled && target.getBoundingClientRect().top > 220) jump();
    }, 4600);
}

document.getElementById('choiceNotesBtn').addEventListener('click', openSubjectNotes);
document.getElementById('choice-modal-units').addEventListener('click', (e) => {
    const row = e.target.closest('.choice-unit-row');
    if (row && row.dataset.unitNo) openSubjectUnit(row.dataset.unitNo);
});
document.getElementById('choice-modal-units').addEventListener('keydown', (e) => {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    const row = e.target.closest('.choice-unit-row');
    if (row && row.dataset.unitNo) { e.preventDefault(); openSubjectUnit(row.dataset.unitNo); }
});
document.getElementById('choiceBookBtn').addEventListener('click', openSubjectBook);
document.getElementById('closeChoiceModal').addEventListener('click', closeSubjectChoice);
document.getElementById('choiceModalBackdrop').addEventListener('click', closeSubjectChoice);

document.getElementById('secondYearBtn').addEventListener('click', () => {
    showEbookView();
    document.getElementById('second-year-new-version').scrollIntoView({ behavior: 'smooth' });
});

// Initial View Setup
showEbookView();
loadBooks();
loadSecondYearSubjects();

// Handle subject selection
const subjectSelect = document.getElementById('subjectSelect');
subjectSelect.addEventListener('change', (e) => {
    showNotesView(); // Switch to notes view when a subject is picked
    loadSubject(e.target.value);
});

// Deep-link: index.html#s=2651 or #s=2651&u=5 (used by the static SEO pages)
const deepLink = location.hash.match(/s=(\d{4})(?:&u=(\d+))?/);
if (deepLink && NOTES_FILES[deepLink[1]]) {
    if (deepLink[2]) pendingUnit = { no: Number(deepLink[2]) };
    showNotesView();
    subjectSelect.value = NOTES_FILES[deepLink[1]];
    loadSubject(NOTES_FILES[deepLink[1]]);
} else {
    // Load default subject initially
    loadSubject(subjectSelect.value);
}

function loadSubject(url) {
    // Clear old contents
    document.getElementById('toc-container').innerHTML = '';
    document.getElementById('dynamic-content').innerHTML = '';
    
    // Clean up old observers
    if (activeSectionObserver) activeSectionObserver.disconnect();
    if (activeCardObserver) activeCardObserver.disconnect();
    
    fetch(url)
        .then(res => res.json())
        .then(data => renderData(normalizeData(data, url)))
        .catch(err => {
            pendingUnit = null;
            console.error("Error loading JSON: ", err);
            document.getElementById('dynamic-content').innerHTML = '<p style="text-align:center; padding: 40px; color: var(--text3);">ডাটা লোড করতে সমস্যা হয়েছে বা ডাটা পাওয়া যায়নি।</p>';
        });
}

// Convert db/vugol.json custom schema to standardized layout
function normalizeData(data, url) {
    if (data.contents) return data; // Already valid Bangla schema
    
    // Convert Vugol schema
    if (data.units) {
        return {
            course: {
                code: "Geography / ভূগোল",
                title: "ভূগোল ও পরিবেশ",
                exam_type: "এসএসসি শর্ট নোট",
                total_marks: "100"
            },
            contents: {
                "chapters": data.units.map(u => ({
                    id: u.id,
                    title: u.title,
                    summary: u.summary,
                    mcq: u.mcq,
                    creative: u.creative,
                    genre: "অধ্যায়"
                }))
            }
        };
    }
    return data;
}

function renderData(data) {
    // Render Hero
    if (data.course) {
        document.getElementById('hero').style.display = 'block';
        document.getElementById('hero-badge').innerText = '📚 ' + data.course.code;
        document.getElementById('hero-title').innerHTML = data.course.title + '<br><span style="font-size:22px; color:rgba(255,255,255,0.7)">' + data.course.exam_type + '</span>';

        let distributionText = '';
        if (data.course.distribution) {
            distributionText = Object.values(data.course.distribution).join(', ');
        }

        document.getElementById('hero-desc').innerText = distributionText || 'এসএসসি পরীক্ষার্থীদের জন্য একটি পরিপূর্ণ বিষয়ভিত্তিক নোটস ও গাইডলাইন।';

        let statsHtml = '';
        if (data.course.total_marks) {
            statsHtml += `<div class="hero-stat"><div class="num">${data.course.total_marks}</div><div class="lbl">Total Marks</div></div>`;
        }
        document.getElementById('hero-stats').innerHTML = statsHtml;
    }

    const tocContainer = document.getElementById('toc-container');
    const dynamicContent = document.getElementById('dynamic-content');

    const sectionMeta = {
        prose: { title: "গদ্য (Prose)", icon: "📘", colorClass: "blue" },
        poetry: { title: "কবিতা (Poetry)", icon: "🌿", colorClass: "green" },
        novel: { title: "উপন্যাস (Novel)", icon: "📙", colorClass: "red" },
        drama: { title: "নাটক (Drama)", icon: "🎭", colorClass: "orange" },
        creative: { title: "সৃজনশীল (Creative)", icon: "🎨", colorClass: "blue" },
        chapters: { title: "অধ্যায় (Chapters)", icon: "🌍", colorClass: "green" },
        grammar: { title: "ব্যাকরণ (Grammar)", icon: "📖", colorClass: "blue" },
        composition: { title: "নির্মিতি (Composition)", icon: "✍️", colorClass: "green" },
        units: { title: "ইউনিট (Units)", icon: "📚", colorClass: "green" },
        writing: { title: "রাইটিং (Writing)", icon: "✍️", colorClass: "green" }
    };

    let globalItemIndex = 0;

    for (const [key, sectionArray] of Object.entries(data.contents)) {
        if (!sectionArray || sectionArray.length === 0) continue;

        const meta = sectionMeta[key] || { title: key.charAt(0).toUpperCase() + key.slice(1), icon: "📌", colorClass: "blue" };

        // Sidebar section
        const tocSection = document.createElement('div');
        tocSection.className = 'toc-section';
        tocSection.innerHTML = `<div class="toc-section-label">${meta.title}</div>`;

        // Main content section divider
        const divider = document.createElement('div');
        divider.className = 'section-divider';
        divider.id = 'section-' + key;
        divider.innerHTML = `
        <div class="section-divider-icon ${meta.colorClass}">${meta.icon}</div>
        <div class="section-divider-text">
          <h2>${meta.title}</h2>
          <p>${sectionArray.length} items</p>
        </div>
        <div class="section-line"></div>
      `;
        dynamicContent.appendChild(divider);

        sectionArray.forEach((item, idx) => {
            globalItemIndex++;
            const itemId = `${key}-${item.id || idx}`;

            // Sidebar link
            const tocLink = document.createElement('a');
            tocLink.setAttribute('href', `#${itemId}`);
            tocLink.className = `toc-link ${meta.colorClass}`;
            let displayNum = globalItemIndex.toLocaleString('bn-BD'); // Bangla numerals
            tocLink.innerHTML = `<div class="toc-num">${displayNum}</div> ${item.title}`;
            tocSection.appendChild(tocLink);

            // Card content
            const card = document.createElement('article');
            card.className = 'card';
            card.id = itemId;

            // MCQs HTML
            let mqHtml = '';
            if (item.mcq && item.mcq.length > 0) {
                let mcqItems = item.mcq.map((m, mIdx) => {
                    let opts = m.options.map(opt => `<span class="mcq-opt">${opt}</span>`).join('');
                    return `
                  <div class="mcq-item">
                    <div class="mcq-q">${(mIdx + 1).toLocaleString('bn-BD')}. ${m.question}</div>
                    <div class="mcq-opts">${opts}</div>
                    <div class="mcq-ans">✔ ${m.answer}</div>
                  </div>`;
                }).join('');

                mqHtml = `
              <div class="mcq-section">
                <div class="mcq-header-bar">📝 বহুনির্বাচনি প্রশ্ন (MCQ)</div>
                <div class="mcq-body">${mcqItems}</div>
              </div>`;
            }

            // Creative Question HTML
            let creativeHtml = '';
            if (item.creative && item.creative.question) {
                const cq = item.creative;
                const ans = cq.answer;
                let cqPoints = '';
                const pointLabels = ['ক', 'খ', 'গ', 'ঘ'];
                ['k', 'kh', 'g', 'gh'].forEach((p, idx) => {
                    if (ans[p]) {
                        cqPoints += `<div class="point-item"><div class="point-dot ${meta.colorClass}"></div><div><strong>(${pointLabels[idx]})</strong> ${ans[p]}</div></div>`;
                    }
                });

                creativeHtml = `
              <div style="margin-bottom: 20px;">
                  <div class="box-label ${meta.colorClass}">💡 সৃজনশীল প্রশ্ন (Creative Question)</div>
                  <div style="font-size:16.5px; font-weight:600; margin-bottom:12px; color:var(--text); line-height: 1.5;">${cq.question}</div>
                  <div class="points-grid">${cqPoints}</div>
              </div>`;
            }

            card.innerHTML = `
            <div class="card-header ${meta.colorClass}">
              <div class="card-num">${displayNum}</div>
              <div style="flex:1;">
                <div class="card-title">${item.title}</div>
                ${item.author ? `<div class="card-author">${item.author}</div>` : ''}
              </div>
              <div class="card-type-badge">${item.genre || meta.title}</div>
            </div>
            <div class="card-body">
              <div class="summary-box ${meta.colorClass}">
                <div class="box-label ${meta.colorClass}">📋 সারসংক্ষেপ</div>
                <p class="summary-text">${item.summary || 'কোনো সারসংক্ষেপ নেই।'}</p>
              </div>
              ${item.infographic ? `<div class="infographic-wrap"><img class="unit-infographic" src="${item.infographic}" alt="${item.infographic_alt || 'ইনফোগ্রাফিক'}" loading="lazy"><div class="infographic-caption">📊 ইনফোগ্রাফিক — এক নজরে Unit-টি</div></div>` : ''}
              ${creativeHtml}
              ${mqHtml}
            </div>
          `;

            dynamicContent.appendChild(card);
        });

        tocContainer.appendChild(tocSection);
    }

    // Initialize scrolling interactions manually after DOM is updated
    initDynamicInteractions();
    scrollToPendingUnit();
}

function initDynamicInteractions() {
    const sections = document.querySelectorAll('[id]');
    const tocLinks = document.querySelectorAll('.toc-link');

    activeSectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.id;
                tocLinks.forEach(l => {
                    l.classList.remove('active');
                    if (l.getAttribute('href') === '#' + id) l.classList.add('active');
                });
            }
        });
    }, { rootMargin: '-20% 0px -70% 0px' });

    sections.forEach(s => activeSectionObserver.observe(s));

    tocLinks.forEach(l => l.addEventListener('click', () => {
        document.getElementById('sidebar').classList.remove('open');
        document.getElementById('overlay').classList.remove('show');
    }));

    const cards = document.querySelectorAll('.card');
    activeCardObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, i) => {
            if (entry.isIntersecting) {
                setTimeout(() => entry.target.classList.add('visible'), 50);
                activeCardObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.08 });

    cards.forEach(c => activeCardObserver.observe(c));
}

// Close modal on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeSubjectChoice();
});
