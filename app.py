from flask import Flask, render_template_string, jsonify
import json

app = Flask(__name__)

# --- VOREX CENTRAL HIERARCHICAL DATABASE ---
VOREX_DATABASE = {
    "arjuna-jee-3": {
        "title": "Arjuna JEE 3.0",
        "description": "Class 11 complete Physics, Chemistry & Maths preparation by expert faculties.",
        "subjects": {
            "physics": {
                "title": "Physics (Arjuna 3.0)",
                "chapters": [
                    {
                        "title": "Chapter 01: Basic Mathematics & Vectors",
                        "lectures": [
                            {
                                "title": "Lecture 01: Mathematical Tools & Calculus", 
                                "faculty": "Physics Expert", 
                                "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
                            }
                        ],
                        "notes": [{"title": "Class Notes PDF", "desc": "Detailed handwritten notes."}],
                        "dpp": [{"title": "DPP 01: Practice Sheet", "desc": "High-yield questions."}]
                    }
                ]
            }
        }
    }
}

VOREX_APP_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>VOREX - Luxury Free Education Suite</title>
    <!-- PWA Manifest & Theme -->
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#030303">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    
    <!-- HLS.js Library -->
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; -webkit-tap-highlight-color: transparent; }
        body { background-color: #030303; color: #ffffff; height: 100vh; overflow: hidden; }

        .screen { display: none; width: 100%; height: 100vh; position: absolute; top: 0; left: 0; }
        .screen.active { display: flex; flex-direction: column; }

        /* LANDING PAGE */
        #landingPage {
            background: radial-gradient(circle at center, #121212 0%, #030303 100%);
            padding: 25px 50px; overflow-y: auto; justify-content: space-between; z-index: 10;
        }
        .landing-navbar { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 215, 0, 0.15); padding-bottom: 15px; }
        .luxury-logo { display: flex; align-items: center; gap: 14px; text-decoration: none; cursor: pointer; }
        .logo-emblem {
            width: 46px; height: 46px; background: linear-gradient(135deg, #ffd700, #ff8c00);
            border-radius: 14px; display: flex; align-items: center; justify-content: center;
            font-size: 26px; font-weight: 900; color: #030303; border: 1.5px solid #fff;
            box-shadow: 0 0 25px rgba(255, 215, 0, 0.4);
        }
        .logo-texts { display: flex; flex-direction: column; }
        .logo-title {
            font-size: 22px; font-weight: 900;
            background: linear-gradient(135deg, #ffd700, #ffaa00);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 2px;
        }
        .logo-subtitle { font-size: 9px; color: #888; letter-spacing: 1.5px; text-transform: uppercase; font-weight: bold; }

        .hero-section { display: flex; flex-direction: column; align-items: center; text-align: center; max-width: 900px; margin: auto; padding: 20px 0; }
        .launch-pill {
            background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(255, 140, 0, 0.05));
            border: 1px solid #ffd700; color: #ffd700; padding: 8px 22px; border-radius: 30px;
            font-size: 13px; font-weight: bold; margin-bottom: 15px; box-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
        }
        .hero-section h1 { font-size: 42px; font-weight: 900; color: #fff; margin-bottom: 12px; line-height: 1.2; }
        .hero-section h1 span { color: #ffd700; }
        .hero-section p { color: #aaa; font-size: 15px; margin-bottom: 25px; line-height: 1.6; max-width: 750px; }
        
        .explore-btn {
            background: linear-gradient(135deg, #ffd700, #ff8c00); color: #000; border: none;
            padding: 14px 40px; border-radius: 35px; font-size: 16px; font-weight: 800;
            cursor: pointer; transition: 0.3s; box-shadow: 0 0 30px rgba(255, 215, 0, 0.4); text-decoration: none; display: inline-block;
        }
        .explore-btn:hover { transform: translateY(-3px); box-shadow: 0 0 40px rgba(255, 215, 0, 0.6); }
        
        .whatsapp-banner {
            margin-top: 20px; background: rgba(37, 211, 102, 0.1); border: 1px solid #25d366; padding: 12px 25px;
            border-radius: 30px; display: inline-flex; align-items: center; gap: 10px; color: #25d366; font-weight: bold; font-size: 14px; text-decoration: none;
        }
        .footer-credit { text-align: center; color: #777; font-size: 13px; padding-bottom: 5px; }
        .footer-credit span { color: #ffd700; font-weight: bold; }

        /* DASHBOARD LAYOUT */
        #dashboardScreen { background: #080808; flex-direction: column; }
        @media(min-width: 768px) { #dashboardScreen { flex-direction: row; } }

        .sidebar { width: 100%; background: #0e0e0e; border-bottom: 1px solid rgba(255, 215, 0, 0.15); display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; }
        @media(min-width: 768px) {
            .sidebar { width: 260px; height: 100vh; border-bottom: none; border-right: 1px solid rgba(255, 215, 0, 0.15); flex-direction: column; align-items: flex-start; padding: 20px; }
        }
        .sidebar-logo { font-size: 20px; font-weight: 900; color: #ffd700; letter-spacing: 2px; }
        
        .nav-links { list-style: none; display: flex; gap: 10px; }
        @media(min-width: 768px) { .nav-links { flex-direction: column; width: 100%; flex-grow: 1; margin-top: 20px; } }
        .nav-links li a {
            color: #aaa; text-decoration: none; padding: 10px 14px; border-radius: 10px; display: block; font-weight: 600; font-size: 14px; transition: 0.2s;
        }
        .nav-links li a:hover, .nav-links li a.active { background: linear-gradient(135deg, rgba(255,215,0,0.2), rgba(255,140,0,0.05)); color: #ffd700; border-left: 3px solid #ffd700; }

        .main-content { flex-grow: 1; display: flex; flex-direction: column; overflow-y: auto; }
        .dash-header { padding: 20px 30px; border-bottom: 1px solid rgba(255, 215, 0, 0.15); display: flex; justify-content: space-between; align-items: center; background: #0a0a0a; }
        .dash-title { font-size: 20px; font-weight: 800; color: #fff; }
        .free-badge { background: #ffd700; color: #000; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 900; box-shadow: 0 0 15px rgba(255,215,0,0.4); }

        .dash-body { padding: 30px; overflow-y: auto; flex-grow: 1; }
        .section-title { font-size: 18px; font-weight: 700; color: #ffd700; margin-bottom: 15px; }

        .batches-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .batch-card {
            background: #111; border: 1px solid #222; border-radius: 14px; padding: 22px;
            transition: 0.3s; box-shadow: 0 4px 20px rgba(0,0,0,0.5); position: relative; overflow: hidden;
        }
        .batch-card:hover { border-color: #ffd700; transform: translateY(-4px); box-shadow: 0 0 25px rgba(255,215,0,0.2); }
        .batch-tag { position: absolute; top: 15px; right: 15px; background: rgba(37,211,102,0.2); color: #25d366; padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: bold; }
        .batch-card h3 { font-size: 18px; color: #fff; margin-bottom: 8px; }
        .batch-card p { color: #888; font-size: 13px; margin-bottom: 15px; }
        .access-btn {
            background: linear-gradient(135deg, #ffd700, #ff8c00); color: #000; border: none;
            padding: 10px 20px; border-radius: 8px; font-weight: 700; cursor: pointer; width: 100%; transition: 0.2s;
        }
        .access-btn:hover { opacity: 0.9; }

        .back-btn {
            background: #222; color: #ffd700; border: 1px solid #ffd700; padding: 8px 16px; border-radius: 8px;
            font-weight: bold; cursor: pointer; margin-bottom: 20px; width: fit-content; transition: 0.2s; display: inline-block;
        }
        .back-btn:hover { background: #ffd700; color: #000; }

        .hierarchy-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .hierarchy-card {
            background: #111; border: 1px solid #222; border-radius: 14px; padding: 22px; cursor: pointer; transition: 0.3s;
        }
        .hierarchy-card:hover { border-color: #ffd700; background: #161616; transform: translateY(-3px); box-shadow: 0 0 20px rgba(255,215,0,0.2); }
        .hierarchy-card h3 { color: #ffd700; font-size: 17px; margin-bottom: 6px; }
        .hierarchy-card p { color: #888; font-size: 13px; }

        .chapter-box { background: #111; border: 1px solid #222; border-radius: 14px; padding: 20px; margin-bottom: 15px; }
        .chapter-title { font-size: 17px; font-weight: bold; color: #fff; margin-bottom: 15px; border-bottom: 1px solid #222; padding-bottom: 10px; }
        
        .content-item-list { display: flex; flex-direction: column; gap: 12px; }
        .content-card {
            background: #161616; border: 1px solid #2a2a2a; border-radius: 12px; padding: 16px 20px;
            display: flex; justify-content: space-between; align-items: center; transition: 0.2s;
        }
        .content-card:hover { border-color: #ffd700; background: #1c1c1c; }
        .content-info h4 { color: #fff; font-size: 15px; margin-bottom: 4px; }
        .content-info p { color: #888; font-size: 12px; }
        .action-link-btn {
            background: rgba(255,215,0,0.15); color: #ffd700; border: 1px solid #ffd700; padding: 8px 18px;
            border-radius: 8px; font-weight: bold; font-size: 13px; cursor: pointer; text-decoration: none; transition: 0.2s;
        }
        .action-link-btn:hover { background: #ffd700; color: #000; }

        /* VIDEO MODAL */
        #videoModal {
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.9); z-index: 2000; justify-content: center; align-items: center; padding: 20px;
        }
        .video-modal-content {
            background: #111; border: 1px solid #ffd700; border-radius: 16px; width: 100%; max-width: 900px;
            padding: 25px; display: flex; flex-direction: column; box-shadow: 0 0 40px rgba(255,215,0,0.3);
        }
        .video-modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .video-modal-header h3 { color: #ffd700; font-size: 18px; }
        .close-modal-btn { background: #333; color: #fff; border: none; padding: 6px 14px; border-radius: 8px; cursor: pointer; font-weight: bold; }
        .close-modal-btn:hover { background: #ff4444; }
        
        .video-responsive-container {
            position: relative; width: 100%; padding-bottom: 56.25%; background: #000; border-radius: 10px; overflow: hidden;
        }
        .video-responsive-container video {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%; outline: none;
        }
    </style>
</head>
<body>

    <!-- LANDING PAGE -->
    <div id="landingPage" class="screen active">
        <div class="landing-navbar">
            <a href="#" class="luxury-logo">
                <div class="logo-emblem">V</div>
                <div class="logo-texts">
                    <span class="logo-title">VOREX</span>
                    <span class="logo-subtitle">Luxury Suite</span>
                </div>
            </a>
            <button class="explore-btn" style="padding: 8px 22px; font-size: 13px;" onclick="goToDashboard()">Student Portal 🔑</button>
        </div>

        <div class="hero-section">
            <div class="launch-pill">🚀 VOREX STREAM ENGINE ACTIVE</div>
            <h1>Master Your Concepts. <span>Conquer Your Goals.</span></h1>
            <p>India's upcoming premium free education suite with direct robust HLS streaming, study material, and official batch layouts.</p>
            <div>
                <button class="explore-btn" onclick="goToDashboard()">Explore Vorex →</button>
            </div>
            <div>
                <a href="https://whatsapp.com" target="_blank" class="whatsapp-banner">
                    💬 Join Official Vorex WhatsApp Community
                </a>
            </div>
        </div>
        <div class="footer-credit">© 2027 Vorex Education Suite | Created by <span>Ankit (MR. AKP)</span> 👑</div>
    </div>

    <!-- DASHBOARD -->
    <div id="dashboardScreen" class="screen">
        <div class="sidebar">
            <div class="sidebar-logo">VOREX SUITE</div>
            <ul class="nav-links">
                <li><a href="#" class="active" onclick="switchTab('batches')">📚 Official Batches</a></li>
                <li><a href="#" onclick="goToLanding()">🏠 Back to Home</a></li>
            </ul>
        </div>
        
        <div class="main-content">
            <div class="dash-header">
                <div class="dash-title" id="dashTitleHeading">Official Batches (100% Free Access)</div>
                <div class="free-badge">STREAM READY ⚡</div>
            </div>

            <div class="dash-body">
                <!-- VIEW 1: BATCH LIST -->
                <div id="viewBatchList" class="dash-view">
                    <div class="section-title">All Available Batches</div>
                    <div class="batches-grid" id="batchesGrid">
                        <div class="batch-card" data-name="arjuna jee 3.0">
                            <div class="batch-tag">ACTIVE</div>
                            <h3>Arjuna JEE 3.0</h3>
                            <p>Class 11 complete Physics, Chemistry & Maths preparation.</p>
                            <button class="access-btn" onclick="openBatch('arjuna-jee-3')">Open Batch 🚀</button>
                        </div>
                    </div>
                </div>

                <!-- VIEW 2: SUBJECT LIST -->
                <div id="viewSubjectList" class="dash-view" style="display:none;">
                    <button class="back-btn" onclick="backToBatches()">← Back to Batches</button>
                    <div class="section-title" id="subjectBatchTitle">Select Subject</div>
                    <div class="hierarchy-grid" id="subjectsGridContainer"></div>
                </div>

                <!-- VIEW 3: CHAPTER LIST -->
                <div id="viewChapterList" class="dash-view" style="display:none;">
                    <button class="back-btn" onclick="backToSubjects()">← Back to Subjects</button>
                    <div class="section-title" id="subjectHeaderTitle">Chapters & Content</div>
                    <div id="chaptersContainer"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- HLS VIDEO PLAYER MODAL -->
    <div id="videoModal">
        <div class="video-modal-content">
            <div class="video-modal-header">
                <h3 id="modalVideoTitle">Lecture Title</h3>
                <button class="close-modal-btn" onclick="closeVideoPlayer()">✕ Close</button>
            </div>
            <div class="video-responsive-container">
                <video id="hlsVideoPlayer" controls controlsList="nodownload" playsinline></video>
            </div>
        </div>
    </div>

    <script>
        const vorexDb = {{ db_json | safe }};
        let hlsInstance = null;
        let currentBatchKey = null;

        function goToDashboard() {
            document.getElementById('landingPage').classList.remove('active');
            document.getElementById('dashboardScreen').classList.add('active');
        }

        function goToLanding() {
            document.getElementById('dashboardScreen').classList.remove('active');
            document.getElementById('landingPage').classList.add('active');
        }

        function switchTab(tabName) {
            document.querySelectorAll('.nav-links a').forEach(el => el.classList.remove('active'));
            event.target.classList.add('active');
        }

        function openBatch(batchKey) {
            currentBatchKey = batchKey;
            let batchData = vorexDb[batchKey];
            if(!batchData) return;

            document.getElementById('viewBatchList').style.display = 'none';
            document.getElementById('viewSubjectList').style.display = 'block';
            document.getElementById('subjectBatchTitle').innerText = batchData.title + " - Select Subject";

            let grid = document.getElementById('subjectsGridContainer');
            grid.innerHTML = '';

            for(let subKey in batchData.subjects) {
                let sub = batchData.subjects[subKey];
                grid.innerHTML += `
                    <div class="hierarchy-card" onclick="openSubject('${subKey}')">
                        <h3>📖 ${sub.title}</h3>
                        <p>Click to access chapters and lectures.</p>
                    </div>
                `;
            }
        }

        function backToBatches() {
            document.getElementById('viewSubjectList').style.display = 'none';
            document.getElementById('viewBatchList').style.display = 'block';
        }

        function openSubject(subKey) {
            let batchData = vorexDb[currentBatchKey];
            let subData = batchData.subjects[subKey];

            document.getElementById('viewSubjectList').style.display = 'none';
            document.getElementById('viewChapterList').style.display = 'block';
            document.getElementById('subjectHeaderTitle').innerText = subData.title + " - Chapters";

            let container = document.getElementById('chaptersContainer');
            container.innerHTML = '';

            subData.chapters.forEach(ch => {
                let lecturesHtml = '';
                ch.lectures.forEach(lec => {
                    lecturesHtml += `
                        <div class="content-card">
                            <div class="content-info">
                                <h4>${lec.title}</h4>
                                <p>Faculty: ${lec.faculty}</p>
                            </div>
                            <a href="#" class="action-link-btn" onclick="openVideoPlayer('${lec.title}', '${lec.url}')">Watch Stream ▶</a>
                        </div>
                    `;
                });

                container.innerHTML += `
                    <div class="chapter-box">
                        <div class="chapter-title">📌 ${ch.title}</div>
                        <div style="margin-bottom: 10px; font-weight: bold; color: #ffd700; font-size: 14px;">Lectures:</div>
                        <div class="content-item-list">${lecturesHtml}</div>
                    </div>
                `;
            });
        }

        function backToSubjects() {
            document.getElementById('viewChapterList').style.display = 'none';
            document.getElementById('viewSubjectList').style.display = 'block';
        }

        function openVideoPlayer(title, streamUrl) {
            document.getElementById('modalVideoTitle').innerText = title;
            let video = document.getElementById('hlsVideoPlayer');
            document.getElementById('videoModal').style.display = 'flex';

            if (Hls.isSupported()) {
                if (hlsInstance) { hlsInstance.destroy(); }
                hlsInstance = new Hls();
                hlsInstance.loadSource(streamUrl);
                hlsInstance.attachMedia(video);
                hlsInstance.on(Hls.Events.MANIFEST_PARSED, function() {
                    video.play();
                });
            } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
                video.src = streamUrl;
                video.addEventListener('loadedmetadata', function() {
                    video.play();
                });
            }
        }

        function closeVideoPlayer() {
            let video = document.getElementById('hlsVideoPlayer');
            video.pause();
            video.src = "";
            if (hlsInstance) {
                hlsInstance.destroy();
                hlsInstance = null;
            }
            document.getElementById('videoModal').style.display = 'none';
        }
    </script>
</body>
</html>
"""

# PWA Manifest Route for Phone App Installation Support
@app.route('/manifest.json')
def manifest():
    manifest_data = {
        "name": "VOREX Education Suite",
        "short_name": "Vorex",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#030303",
        "theme_color": "#ffd700",
        "icons": [
            {
                "src": "https://img.icons8.com/fluency/96/graduation-cap.png",
                "sizes": "96x96",
                "type": "image/png"
            }
        ]
    }
    return jsonify(manifest_data)

@app.route('/')
def home():
    return render_template_string(VOREX_APP_CODE, db_json=json.dumps(VOREX_DATABASE))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)