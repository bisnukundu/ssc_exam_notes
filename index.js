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

// Handle subject selection
const subjectSelect = document.getElementById('subjectSelect');
subjectSelect.addEventListener('change', (e) => {
    loadSubject(e.target.value);
});

// Load default subject initially
loadSubject(subjectSelect.value);

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
        chapters: { title: "অধ্যায় (Chapters)", icon: "🌍", colorClass: "green" }
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
